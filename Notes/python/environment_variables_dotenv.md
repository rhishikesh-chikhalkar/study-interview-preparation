# Python Environment Variables and python-dotenv

## Overview

Environment variables are key-value pairs stored in the operating system's execution environment.
In Python applications, they manage configuration settings, secrets (API keys, credentials),
and environment-specific flags (e.g., `DEBUG`, `STAGE`) without hardcoding them into source code.

---

## 1. Core Concepts & python-dotenv

`python-dotenv` is a Python library that reads key-value pairs from a `.env` file and adds them
to `os.environ`.

### Basic Usage

```python
import os
from dotenv import load_dotenv

# Load variables from .env into os.environ
load_dotenv()

api_key = os.getenv("API_KEY")
```

### The `override` Parameter

By default (`override=False`), `python-dotenv` preserves existing environment variables.

```python
# System shell environment: API_KEY="prod-key-123"
# .env file content: API_KEY="local-key-456"

load_dotenv(override=False)
# os.getenv("API_KEY") -> "prod-key-123" (System wins)

load_dotenv(override=True)
# os.getenv("API_KEY") -> "local-key-456" (.env file wins)
```

---

## 2. Best Practices & Security

1. **Never Commit `.env` Files**:
   Add `.env` to `.gitignore`. Use `.env.example` as a template with placeholder values.

2. **Explicit Parsing via `dotenv_values()`**:
   Instead of mutating global `os.environ`, parse values into a dict:
   ```python
   from dotenv import dotenv_values

   config = dotenv_values(".env")
   ```

3. **Validation with `pydantic-settings`**:
   Production applications should use structured validation:
   ```python
   from pydantic_settings import BaseSettings

   class Settings(BaseSettings):
       api_key: str
       debug: bool = False

       class Config:
           env_file = ".env"

   settings = Settings()
   ```

---

## 3. Interview Questions & Answers (5 YOE Level)

### Q1: Conceptual
**Question**: What is the difference between `override=False` (default) and `override=True`
in `load_dotenv()`? Why might using `override=True` pose a risk in production?

**Answer**:
- `override=False` (default) means pre-existing process environment variables (set by OS,
  Docker, Kubernetes, CI/CD) take precedence over values defined in `.env`.
- `override=True` forces values from `.env` to overwrite matching keys in `os.environ`.
- **Production Risk**: Cloud platforms (AWS ECS, Kubernetes, Cloud Run) inject secrets directly
  into container environment variables. If `override=True` is enabled and a `.env` file is
  accidentally shipped in the container image, it will override production secrets with stale
  local development values.

*Follow-up*: How can you disable `.env` loading entirely in production without code changes?
*Answer*: Set the environment variable `PYTHON_DOTENV_DISABLED=1`.

---

### Q2: Practical / Scenario
**Question**: You are building a multi-tenant Python application where environment settings
need to be loaded dynamically per request or worker task without polluting global `os.environ`.
How would you achieve this using `python-dotenv`?

**Answer**:
Instead of calling `load_dotenv()`, which mutates global `os.environ`, use `dotenv_values()`:

```python
from dotenv import dotenv_values

def load_tenant_config(tenant_env_path: str) -> dict:
    # Returns a dict without modifying os.environ
    return dotenv_values(dotenv_path=tenant_env_path)
```
This isolates configuration loading to local scopes and avoids race conditions in multi-threaded
or concurrent environments.

---

### Q3: Architecture / Production Design
**Question**: How should configuration management be structured for a 12-Factor Python microservice
moving from local dev to staging and production?

**Answer**:
1. **Local Dev**: Use `.env` file loaded via `pydantic-settings` or `dotenv_values()`.
2. **CI/CD & Staging/Prod**: Omit `.env` files entirely. Inject environment variables directly
   via container orchestrator (Kubernetes ConfigMaps/Secrets, AWS SSM Parameter Store / Vault).
3. **Validation**: Use Pydantic `BaseSettings` to enforce type checking and fail fast at startup
   if required keys are missing or invalid.

---

## References

- [python-dotenv Official Repository](https://github.com/theskumar/python-dotenv)
- [12-Factor App: Config](https://12factor.net/config)
- [Pydantic Settings Documentation](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)
