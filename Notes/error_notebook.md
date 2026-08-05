# Error & Debugging Notebook

This notebook documents common errors, their root causes, and how to resolve them.

---

## 1. Python `unittest`: `assertEqual()` Missing Required Argument

### Problem
When running tests via `unittest`, the test execution fails with a `TypeError`:

```traceback
ERROR: test_pop_remove_item (__main__.TestStack.test_pop_remove_item)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "python/tests/test_stack.py", line 47, in test_pop_remove_item
    self.assertEqual(self.stack.is_empty())
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^
TypeError: TestCase.assertEqual() missing 1 required positional argument: 'second'
```

### Cause
The method `assertEqual(first, second)` requires exactly **two** positional arguments to compare them for equality (e.g., `self.assertEqual(a, b)`). Passing only a single argument (like the boolean `self.stack.is_empty()`) leaves the second argument undefined, raising a `TypeError`.

### Solution

#### Option A: Use `assertTrue()` (Recommended for Booleans)
If you are asserting that a condition or method return value is `True`, use `assertTrue()`:
```diff
- self.assertEqual(self.stack.is_empty())
+ self.assertTrue(self.stack.is_empty())
```

#### Option B: Provide the Second Parameter
Explicitly compare the result against `True` or another expected value:
```diff
- self.assertEqual(self.stack.is_empty())
+ self.assertEqual(self.stack.is_empty(), True)
```

---

## 2. Python `RecursionError` in Stack Class

### Problem
Tests fail with a stack overflow / recursion error:
```traceback
E   RecursionError: maximum recursion depth exceeded
!!! Recursion detected (same locals & position)
```

### Cause
In python, if an instance method calls itself (using `self.method_name()`) without a base case that resolves or delegation to an underlying list/object, it creates an infinite recursive loop. 
For example, writing `return self.pop()` inside a class's custom `pop()` method:
```python
def pop(self):
    if self.is_empty():
        raise IndexError("pop from empty list")
    return self.pop()  # RecursionError: calls itself infinitely
```

### Solution
Delegate to the underlying data structure (like `self._data`):
```diff
- return self.pop()
+ return self._data.pop()
```

---

## 3. `NameError: name 'self' is not defined`

### Problem
Test collections fail globally with:
```traceback
E   NameError: name 'self' is not defined
```

### Cause
This typically happens when transitioning from `unittest` (which uses class methods referencing `self`) to generic pytest functions. If code like `self.assertEqual(...)` is copied directly to a top-level function, `self` is not defined in that context.

### Solution
Remove `self` and convert to standard assertions:
```diff
- self.assertEqual(result, 42)
+ assert result == 42
```

---

## 4. `can't open file 'pytest': [Errno 2] No such file or directory`

### Problem
Running tests under `uv` fails with a missing file error:
```traceback
/Users/rhishikesh/GITHUB/study-interview-preparation/.venv/bin/python3: can't open file '/Users/rhishikesh/GITHUB/study-interview-preparation/python/tests/pytest': [Errno 2] No such file or directory
```

### Cause
Executing `uv run python pytest .` commands Python to run a script file named `pytest` in the current working directory, which does not exist.

### Solution
Invoke the command-line utility `pytest` directly via `uv run`:
```diff
- uv run python pytest .
+ uv run pytest .
```

---

## 5. CI/CD: Un-gated Continuous Deployment (CD Deploying on Failed CI)

### Problem
In GitHub Actions, code pushed to `main` triggered both `ci.yml` and `cd.yml` in parallel. When `CI` failed due to linting errors (`ruff`) or broken tests, `CD` still proceeded and deployed unverified code to the production server.

### Cause
`cd.yml` was configured with `on: push: branches: [main]` independently of `ci.yml`, without a `workflow_run` dependency or job condition checking whether CI passed.

### Solution
Update `cd.yml` to trigger on `workflow_run` of `CI` and add a job guard:
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

## 6. Python/Pytest: Module Import-Time Side-Effects Crashing Test Collection Without Keys

### Problem
Running `uv run pytest` in a fresh CI runner without local `.env` or API keys failed during test collection with:
```traceback
RuntimeError: No Gemini API keys configured.
```

### Cause
Service modules (`gemini_transcriber.py` and `post_vision_analyzer.py`) instantiated `KEY_MANAGER = GeminiKeyManager()` at module scope (import-time). `GeminiKeyManager.__init__()` checked for keys immediately and raised `RuntimeError` if `GEMINI_API_KEYS` was empty, blocking pytest module collection.

### Solution
1. **Defer Key Validation**: Move non-empty key checks from `__init__()` to `get_client()` in `GeminiKeyManager`:
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
2. **Autouse Fixture in `conftest.py`**: Add fixture to populate mock keys and reset `KEY_MANAGER._clients` pools between tests:
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

## 7. Python Logging: `ValueError` from Direct `.index()` on Un-indexed Keys

### Problem
During unit test execution with mock keys or fallback keys, logging metadata calls threw:
```traceback
ValueError: 'dummy_test_key' is not in list
```

### Cause
Logging calls used `extra={"key_index": GEMINI_API_KEYS.index(api_key)}`. If `api_key` was a mock key (e.g., `"dummy_test_key"`) not present in global `GEMINI_API_KEYS`, `.index()` raised `ValueError`.

### Solution
Replace direct `.index()` lookups with a safe helper:
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

## 8. Docker Multi-Stage Build: `hatchling` Readme Validation Failure

### Problem
Docker image build failed during `RUN uv sync --no-dev --frozen` inside the builder stage with:
```traceback
OSError: Readme file does not exist: README.md
```

### Cause
`pyproject.toml` declared package metadata requiring `README.md`. The Dockerfile builder stage only copied `pyproject.toml` and `uv.lock*` before running `uv sync`, leaving `README.md` missing during `hatchling` wheel metadata validation.

### Solution
Copy `README.md*` alongside dependency locks in the Dockerfile builder stage:
```dockerfile
# Copy dependency files and README for layer caching
COPY pyproject.toml uv.lock* README.md* ./

RUN uv sync --no-dev --frozen
```

---

## 9. Unit Testing: `os.path.exists` vs `pathlib.Path.exists` Mocking Discrepancy

### Problem
A test asserting secrets loading failed on Linux CI runners:
```traceback
AssertionError: assert [] == ['test1', 'test2']
```

### Cause
The unit test patched `os.path.exists`, but the production code evaluated `SECRET_PATH.exists()` using `pathlib.Path.exists()`. Because `Path.exists()` was unmocked, it returned `False` on the runner filesystem.

### Solution
Patch `Path.exists` in the test context:
```python
with (
    patch("os.path.exists", return_value=True),
    patch.object(Path, "exists", return_value=True),
    patch("builtins.open", mock_open(read_data=fake_secrets)),
):
    ...
```

