# Production Challenges & Engineering Solutions

This document summarizes real-world production engineering challenges, root cause analyses, and robust resolutions from active projects.

---

## 1. Un-gated Continuous Deployment (CD Deploying on Failed CI)

### Problem
Code pushed to `main` triggered both `ci.yml` and `cd.yml` in parallel in GitHub Actions. When `CI` failed due to linting errors (`ruff`) or broken tests, `CD` still proceeded and deployed unverified code directly to the production VM over SSH.

### Root Cause
`cd.yml` was configured with `on: push: branches: [main]` independently of `ci.yml`, without a `workflow_run` dependency or job condition verifying whether CI succeeded.

### Solution
Refactored `cd.yml` to trigger on `workflow_run` of `CI` and added a strict job guard:
```yaml
name: CD (Post-Merge)

on:
  workflow_run:
    workflows: ["CI"]
    branches:
      - main
    types:
      - completed

jobs:
  deploy:
    name: Deploy to Production VM
    runs-on: ubuntu-latest
    if: ${{ github.event.workflow_run.conclusion == 'success' }}
```

---

## 2. Python/Pytest: Module Import-Time Side-Effects Crashing Test Collection Without Keys

### Problem
Running `uv run pytest` in a fresh CI runner without local `.env` or API keys failed during test collection with:
```traceback
RuntimeError: No Gemini API keys configured.
```

### Root Cause
Service modules (`gemini_transcriber.py` and `post_vision_analyzer.py`) instantiated `KEY_MANAGER = GeminiKeyManager()` at module scope (import-time). `GeminiKeyManager.__init__()` checked for keys immediately and raised `RuntimeError` if `GEMINI_API_KEYS` was empty, blocking pytest module collection.

### Solution
1. **Deferred Key Validation**: Deferred non-empty key checks from `__init__()` to `get_client()` in `GeminiKeyManager`:
```python
def _ensure_keys(self) -> None:
    if not self._keys and not self._custom_keys:
        from trigger_engine.core.constants import GEMINI_API_KEYS
        self._keys = [k for k in GEMINI_API_KEYS if k]
    if not self._keys:
        raise RuntimeError("No Gemini API keys configured.")

def get_client(self) -> tuple[str, genai.Client]:
    self._ensure_keys()
    ...
```
2. **Autouse Fixture in `conftest.py`**: Added a fixture to populate mock keys and reset `KEY_MANAGER._clients` pools between tests:
```python
@pytest.fixture(autouse=True)
def mock_gemini_keys_if_empty():
    from trigger_engine.core import constants
    from trigger_engine.core.services import gemini_transcriber, post_vision_analyzer

    orig_keys = list(constants.GEMINI_API_KEYS)
    if not orig_keys:
        constants.GEMINI_API_KEYS.append("dummy_test_key")

    gemini_transcriber.KEY_MANAGER._clients.clear()
    post_vision_analyzer.KEY_MANAGER._clients.clear()
    yield
    gemini_transcriber.KEY_MANAGER._clients.clear()
    post_vision_analyzer.KEY_MANAGER._clients.clear()
    if not orig_keys:
        constants.GEMINI_API_KEYS.clear()
```

---

## 3. Python Logging: `ValueError` from Direct `.index()` on Un-indexed Keys

### Problem
During unit test execution with mock keys or fallback keys, logging metadata calls threw:
```traceback
ValueError: 'dummy_test_key' is not in list
```

### Root Cause
Logging calls used `extra={"key_index": GEMINI_API_KEYS.index(api_key)}`. If `api_key` was a mock key (e.g., `"dummy_test_key"`) not present in global `GEMINI_API_KEYS`, `.index()` raised `ValueError`.

### Solution
Replaced direct `.index()` lookups with a safe helper:
```python
def _safe_key_index(api_key: str) -> int:
    try:
        return GEMINI_API_KEYS.index(api_key)
    except ValueError:
        return -1

# In logger call:
logger.info("Gemini transcription attempt", extra={"key_index": _safe_key_index(api_key)})
```

---

## 4. Docker Multi-Stage Build: `hatchling` Readme Validation Failure

### Problem
Docker image build failed during `RUN uv sync --no-dev --frozen` inside the builder stage with:
```traceback
OSError: Readme file does not exist: README.md
```

### Root Cause
`pyproject.toml` declared package metadata requiring `README.md`. The Dockerfile builder stage only copied `pyproject.toml` and `uv.lock*` before running `uv sync`, leaving `README.md` missing during `hatchling` wheel metadata validation.

### Solution
Copied `README.md*` alongside dependency locks in the Dockerfile builder stage:
```dockerfile
# Copy dependency files and README for layer caching
COPY pyproject.toml uv.lock* README.md* ./

RUN uv sync --no-dev --frozen
```

---

## 5. Unit Testing: `os.path.exists` vs `pathlib.Path.exists` Mocking Discrepancy

### Problem
A test asserting secrets loading failed on Linux CI runners:
```traceback
AssertionError: assert [] == ['test1', 'test2']
```

### Root Cause
The unit test patched `os.path.exists`, but the production code evaluated `SECRET_PATH.exists()` using `pathlib.Path.exists()`. Because `Path.exists()` was unmocked, it returned `False` on the runner filesystem.

### Solution
Patched `Path.exists` in the test context:
```python
with (
    patch("os.path.exists", return_value=True),
    patch.object(Path, "exists", return_value=True),
    patch("builtins.open", mock_open(read_data=fake_secrets)),
):
    ...
```

---

## 6. Flask RAG API Render Deployment: Hardcoded Port Binding & Connection Refusal

### Problem
Deploying the Flask RAG microservice to Render failed container port detection (triggering
repeated deployment restarts), and querying `/ask` returned:
`[Mock Answer - API Error: [Errno 111] Connection refused]` alongside empty retrieved chunks.

### Root Cause
1. **Hardcoded Port Binding**: `Dockerfile` used JSON array exec form `CMD ["gunicorn", "--bind", "0.0.0.0:5001", "wsgi:app"]`, which prevented expansion of Render's dynamic `$PORT` environment variable (`PORT=10000`).
2. **Unreachable Local Fallback**: Missing API keys on Render caused the pipeline to fall back to calling local Ollama (`http://localhost:11434`), which is not present in cloud container environments, raising `[Errno 111] Connection refused`.
3. **Empty Vector Store Fallback**: An unpopulated ChromaDB collection (`retrieved_chunks: []`) triggered strict prompt rules returning *"The context does not contain enough information to answer."*

### Solution
1. **Dynamic Shell CMD**: Updated `Dockerfile` CMD to shell format:
```dockerfile
CMD gunicorn --bind 0.0.0.0:${PORT:-5001} wsgi:app
```
2. **Native OpenRouter Support**: Configured `RAGPipeline` to detect OpenRouter keys (`sk-or-v1-...`) and automatically route base URLs to `https://openrouter.ai/api/v1`.
3. **Smart Dual-Mode System Prompt**: Refactored prompt logic in `generate_answer()`:
```python
if retrieved_chunks:
    system_message = (
        "Answer the user's question based strictly on the provided context below:\n\n"
        f"### Context:\n{context_text}"
    )
else:
    system_message = (
        "Note that no document context was matched in the vector database.\n"
        "Answer the question using general knowledge while briefly mentioning that "
        "no specific document context was retrieved."
    )
```
4. **Root Health Check Route**: Bound `@health_bp.route("/", methods=["GET"])` alongside `/health` and set `healthCheckPath: /health` in `render.yaml` to prevent 404 logs during PaaS health probing.

---

## 7. Cloud PaaS Ephemeral Disks & Vector DB State Persistence

### Problem
PDF document embeddings indexed in local ChromaDB storage (`./_tmp/chroma_db`) vanished on every code push or service restart on Render.

### Root Cause
Render Web Service instances use ephemeral Docker filesystem containers. Any disk writes to local folders are destroyed when instances restart or redeploy.

### Solution
1. **PaaS Disk Attachment**: Configured environment variable `CHROMA_DB_DIR=/data/chroma_db` backed by a Render Persistent Disk volume.
2. **Stateless Microservice Decoupling**: Documented cloud migration path to managed vector stores (Qdrant Cloud, Pinecone, or PostgreSQL `pgvector`), decoupling vector state from Flask web containers to allow horizontal scaling across Gunicorn workers.

