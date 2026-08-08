# Industry Production-Grade Flask RAG API

Enterprise-ready, modular Retrieval-Augmented Generation (RAG) REST microservice built with Flask, Gunicorn, ChromaDB, OpenAI, and Astral `uv`.

## Enterprise Architecture Highlights

- **Application Factory Pattern (`create_app()`)**: Dynamically configures the application across Development, Testing, and Production environments without global side-effects.
- **Flask Blueprints (`src/flask_rag_api/api/`)**: Domain-driven routing separation (`health_bp`, `rag_bp`).
- **Strongly-Typed Configuration (`config.py`)**: Environment-driven setting parsing.
- **Structured Production Logging (`logging.py`)**: Standardized Python logging instead of raw print statements.
- **Global Exception Handling (`errors.py`)**: Unified JSON error schema across HTTP exceptions and uncaught server errors.
- **Multi-Stage Dockerization (`Dockerfile`)**: Optimized Python container image build.
- **Package Layout (`src/`)**: PEP 621 compliant wheel build via `hatchling` and `pyproject.toml`.

---

## Directory Layout

```text
ai-engineering/production/flask-rag-api/
├── Dockerfile                   # Multi-stage production Docker container build
├── .dockerignore                # Container context build exclusions
├── .env.example                 # Environment variable template
├── Procfile                     # Gunicorn startup file (`web: gunicorn wsgi:app`)
├── pyproject.toml               # PEP 621 package dependencies & metadata (uv managed)
├── README.md                    # Production architecture documentation
├── render.yaml                  # Render Infrastructure Blueprint
├── wsgi.py                      # Production WSGI entrypoint
├── src/
│   └── flask_rag_api/
│       ├── __init__.py          # Application Factory (`create_app()`)
│       ├── config.py            # Strongly-typed environment configuration
│       ├── api/                 # Flask Blueprints
│       │   ├── health.py        # Health & readiness endpoint
│       │   └── rag.py           # RAG REST API endpoints
│       ├── core/                # RAG Engine core logic
│       │   └── pipeline.py      # Vector search & OpenAI generation engine
│       └── utils/               # Production utilities
│           ├── errors.py        # Global exception handling
│           └── logging.py       # Structured logging setup
└── tests/
    ├── conftest.py              # Pytest client fixtures
    ├── integration/
    │   └── test_api_routes.py   # Blueprint integration tests
    └── unit/
        └── test_pipeline.py     # Core pipeline unit tests
```

---

## Quick Start (Local Development)

```bash
# 1. Navigate to directory
cd ai-engineering/production/flask-rag-api

# 2. Copy environment template
cp .env.example .env

# 3. Run production WSGI server with uv
uv run wsgi.py
```

---

## Running Automated Tests

```bash
# Run unit and integration tests
uv run pytest
```

---

## Deploy to Cloud / Render PaaS

1. Connect your repository on [Render](https://render.com).
2. Set **Root Directory** to `ai-engineering/production/flask-rag-api`.
3. Set **Build Command** to `pip install uv && uv pip install --system .`.
4. Set **Start Command** to `gunicorn --bind 0.0.0.0:$PORT wsgi:app`.
5. Add `OPENAI_API_KEY` in Render Service Environment Settings.
