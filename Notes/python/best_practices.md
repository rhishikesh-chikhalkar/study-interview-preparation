# Python Best Practices

This document outlines key best practices for writing clean, robust, and idiomatic Python code.

---

## 1. Use Context Managers (`with` statement) for Resource Management

Instead of manually opening and closing resources (like files, database connections, or sockets), always use a context manager (`with` statement). This ensures that resources are properly cleaned up and released, even if exceptions are raised during execution.

### 🚫 Bad Practice (Manual Close)
```python
file = open("data.txt", "r")
try:
    content = file.read()
    # If an exception occurs here, the file might remain open
finally:
    file.close()
```

### ✅ Best Practice (Using Context Manager)
```python
with open("data.txt", "r") as file:
    content = file.read()
# The file is automatically closed here, even if an exception occurs
```

---

## 2. Add Type Annotations

Type annotations (Type Hinting) improve code readability, enable IDEs to provide better autocompletion/linting, and allow static analysis tools (like `mypy`) to catch type-related bugs before runtime.

### 🚫 Bad Practice (Untyped)
```python
def process_user_data(user, age, active):
    greeting = f"Hello {user}"
    years_to_hundred = 100 - age
    return {"greeting": greeting, "active": active}
```

### ✅ Best Practice (Type Annotated)
```python
from typing import Dict, Union

def process_user_data(user: str, age: int, active: bool) -> Dict[str, Union[str, bool]]:
    greeting: str = f"Hello {user}"
    years_to_hundred: int = 100 - age
    return {"greeting": greeting, "active": active}
```

---

## 3. Ask for Forgiveness Instead of Permission (EAFP)

Python embraces the **EAFP** coding style: *"Easier to Ask for Forgiveness than Permission"*. Instead of checking if conditions are met before performing an operation (LBYL - *Look Before You Leap*), perform the operation directly and handle any exceptions that might occur. This is cleaner, more pythonic, and avoids race conditions.

### 🚫 Bad Practice (Checking First - LBYL)
```python
import os

filename = "config.json"
if os.path.exists(filename):
    with open(filename, "r") as file:
        data = file.read()
else:
    data = "default config"
```

### ✅ Best Practice (Handle Exception - EAFP)
```python
filename = "config.json"
try:
    with open(filename, "r") as file:
        data = file.read()
except FileNotFoundError:
    data = "default config"
```

---

## 4. Model Structured Data with Dataclasses

Instead of using plain dictionaries, tuples, or writing verbose boilerplate for custom classes, use Python's built-in `dataclasses` module to model structured data. It automatically generates standard methods (`__init__`, `__repr__`, `__eq__`) and enforces schema clarity.

### 🚫 Bad Practice (Dictionaries or Verbose Boilerplate)
```python
# Unstructured/untyped dictionary
user_dict = {"name": "Alice", "id": 42, "role": "admin"}

# Or verbose custom class
class User:
    def __init__(self, name: str, id: int, role: str):
        self.name = name
        self.id = id
        self.role = role
```

### ✅ Best Practice (Using `@dataclass`)
```python
from dataclasses import dataclass

@dataclass(frozen=True)  # frozen=True makes the instances immutable
class User:
    name: str
    user_id: int
    role: str

user = User(name="Alice", user_id=42, role="admin")
```

---

## 5. Centralize File Paths and Constants

Avoid hardcoding file paths as raw strings scattered across modules. Instead, use Python's modern `pathlib` module and group your configuration, constants, and paths at the top of the file or in a dedicated configuration module.

### 🚫 Bad Practice (Hardcoded Strings Scattered)
```python
# Hardcoded string paths
with open("data/raw/users.csv", "r") as f:
    ...

with open("data/processed/output.json", "w") as f:
    ...
```

### ✅ Best Practice (Using `pathlib.Path` & Centralized Config)
```python
from pathlib import Path

# Centralize base paths and constants at the module level
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
USER_INPUT_PATH = DATA_DIR / "raw" / "users.csv"
OUTPUT_PATH = DATA_DIR / "processed" / "output.json"

MAX_RETRIES = 3

# Usage
with open(USER_INPUT_PATH, "r") as f:
    ...
```

---

## 6. Rely on Python's Core Strengths (Built-ins and Idioms)

Leverage built-in functions, list comprehensions, and Python's collection structures to write expressive, performance-efficient, and concise code.

### 🚫 Bad Practice (Manual loops for transformations)
```python
# Squaring even numbers using manual loops
evens = []
for x in range(10):
    if x % 2 == 0:
        evens.append(x * x)
```

### ✅ Best Practice (List Comprehensions and Built-ins)
```python
# Expressive list comprehension
evens = [x * x for x in range(10) if x % 2 == 0]

# Rely on helper functions like zip() and enumerate()
names = ["Alice", "Bob"]
for idx, name in enumerate(names):
    print(f"{idx}: {name}")
```

---

## 7. Use `logging` Instead of `print`

For outputting status messages, errors, or debugging information, use the standard library `logging` module rather than `print` statements. Logging allows you to configure log levels (DEBUG, INFO, WARNING, ERROR), format outputs, and direct logs to different destinations (console, files, monitoring tools) dynamically.

### 🚫 Bad Practice (Using print)
```python
print("App started...")
print(f"Error: {error_msg}")  # No severity level or timestamp
```

### ✅ Best Practice (Using logging)
```python
import logging

# Configure logging at the entry point of the application
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logging.info("App started successfully.")
logging.error("Failed to connect to database: %s", error_msg)
```

---

## 8. Add a `main` Function Guard

Structure scripts so that they can be either imported as modules or executed as standalone scripts. Place executable logic inside a `main()` function and call it under the `if __name__ == "__main__":` guard.

### 🚫 Bad Practice (Global Executable Code)
```python
import sys

# This executes immediately when imported, preventing safe reuse or testing
data = sys.argv[1]
print(f"Processing data: {data}")
```

### ✅ Best Practice (Using a main Entry Point)
```python
import sys
import logging

def main() -> None:
    logging.basicConfig(level=logging.INFO)
    
    if len(sys.argv) < 2:
        logging.error("Missing required arguments.")
        sys.exit(1)
        
    data = sys.argv[1]
    logging.info("Processing data: %s", data)

if __name__ == "__main__":
    main()

---

## 9. Resource Management: Context Managers & Try-Finally Pitfalls

Properly releasing resources (files, sockets, locks) is crucial, even when exceptions occur. While the `with` statement is the most elegant way to handle cleanup, there are advanced patterns and critical pitfalls to keep in mind.

### A. Custom Context Managers
You can implement custom context managers in two ways:
1. **Class-based**: Define `__enter__` and `__exit__` methods.
2. **Generator-based**: Use the `@contextmanager` decorator from `contextlib`.

```python
from contextlib import contextmanager

@contextmanager
def temp_resource():
    resource = acquire_resource()
    try:
        yield resource
    finally:
        release_resource(resource)
```

### B. Suppressing Exceptions in `__exit__`
Most context managers propagate exceptions. However, you can suppress exceptions by returning `True` (or a truthy value) from `__exit__`.

```python
class SuppressValueError:
    def __enter__(self):
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        # Return True to suppress ValueError; other exceptions will propagate
        return exc_type is ValueError
```

### C. Context Managers for Temporary State
Beyond cleanup, context managers are excellent for managing temporary states (e.g., database transactions or local thread contexts). For instance, the `decimal` module uses `localcontext` for high-precision calculations:

```python
import decimal

with decimal.localcontext() as ctx:
    ctx.prec = 50  # Sets high precision temporarily
    # Perform calculations...
```

### D. Critical Limitations & Pitfalls

> [!WARNING]
> **Never use `return`, `break`, or `continue` inside `finally` blocks.**
> Doing so will discard any pending exceptions that occurred inside the `try` block, potentially masking critical bugs.

```python
# 🚫 Bad Practice
def retrieve_data():
    try:
        raise ValueError("Critical error!")
    finally:
        return "Suppressed!"  # The ValueError is silently discarded!
```

* **No Cleanup Guarantees on Sudden Termination**: Context manager cleanups and `finally` blocks are not guaranteed to run if the process is terminated abruptly (e.g., via `os._exit()` or an OS-level `SIGKILL`).
* **Interrupt Race Conditions**: Although rare, asynchronous interrupts (like `KeyboardInterrupt`) can occur between operations in `try-finally` blocks. Built-in locks implemented in C generally avoid this since they handle locking atomically.

---

## 10. Testing Best Practices

Writing clear, independent, and well-asserted tests is essential for maintaining a reliable test suite. Avoid common beginner test design and assertion mistakes.

### A. Avoid Assertions That Always Pass
Always verify that your assertions actually check the correctness of the code under test, rather than comparing a variable to itself or checking trivial truths.

#### 🚫 Bad Practice
Comparing a result to itself passes even if the function returns `None` or an incorrect value.
```python
def test_pop(self):
    self.stack.push(5)
    result = self.stack.pop()
    self.assertEqual(result, result)  # 🚫 Comparing result to itself!
```

#### ✅ Best Practice
Compare the result to the expected hardcoded or predefined value.
```python
def test_pop(self):
    self.stack.push(5)
    result = self.stack.pop()
    self.assertEqual(result, 5)  # ✅ Comparing with expected value
```

### B. One Behavior Per Test (Avoid Unrelated Assertions)
Do not test multiple unrelated features or state transitions in a single test case. If an early assertion fails, subsequent assertions are not executed, making it hard to diagnose the root cause.

#### 🚫 Bad Practice
Testing pushes, sizes, pops, and empty status all in one monolithic test.
```python
def test_stack(self):
    self.stack.push(1)
    self.stack.push(2)
    self.assertEqual(self.stack.size(), 2)
    self.assertEqual(self.stack.pop(), 2)
    self.assertEqual(self.stack.size(), 1)
    self.assertEqual(self.stack.pop(), 1)
    self.assertTrue(self.stack.is_empty())
```

#### ✅ Best Practice
Write isolated, descriptive tests for each distinct behavior.
```python
def test_size_after_two_pushes(self):
    self.stack.push(1)
    self.stack.push(2)
    self.assertEqual(self.stack.size(), 2)

def test_pop_returns_correct_value(self):
    self.stack.push(1)
    self.stack.push(2)
    self.assertEqual(self.stack.pop(), 2)
```

### C. Do Not Put Test-Specific State in `setUp`
The `setUp()` method should create a clean, basic environment. Avoid pre-filling objects or initializing state that isn't required by all tests.

#### 🚫 Bad Practice
Pre-filling data in `setUp()` that only a few tests actually need.
```python
def setUp(self):
    self.stack = Stack()
    self.stack.push(99)  # 🚫 Why? Not every test needs a pre-filled stack
```

#### ✅ Best Practice
Initialize a clean object in `setUp()`, and let individual tests set up their own specific state.
```python
def setUp(self):
    self.stack = Stack()

def test_pop_after_push(self):
    self.stack.push(99)  # ✅ Set up exactly what THIS test needs
    self.assertEqual(self.stack.pop(), 99)
```

### D. Use Self-Documenting Test Names
Good test names should act as self-documenting failure messages in CI/CD logs. Follow a naming convention like `test_<method/scenario>_<condition>_<expected_result>`.

#### 🚫 Bad Practice
Vague or non-descriptive test names.
```python
def test_1(self): ...
def test_stack_works(self): ...
def test_pop(self): ...
```

#### ✅ Best Practice
Expressive names that state precisely what condition is being tested and what result is expected.
```python
def test_pop_returns_last_pushed_item(self): ...
def test_pop_on_empty_stack_raises_index_error(self): ...
def test_peek_does_not_change_size(self): ...
def test_size_is_zero_on_new_stack(self): ...

### E. Pytest and Professional Unit Testing Guidelines

For writing clean, readable, and robust test suites, adopt Pytest as the standard test runner and follow these modern unit testing practices:

* **Use Pytest over Unittest**: Prefer `pytest` due to its simpler syntax (using plain `assert` statements instead of verbose camelCase helper methods) and its powerful extension ecosystem.
* **Isolated and Predictable Validation**: Keep unit tests highly focused on isolated pieces of code (a single function or method). Avoid database or network calls; tests must be deterministic and extremely fast to provide a continuous feedback loop.
* **Mocking and Monkey Patching**: Swap external dependencies (such as HTTP requests, third-party APIs, or filesystem operations) with mocks. Leverage `unittest.mock.MagicMock` or `pytest`'s `monkeypatch` fixture to simulate responses and inspect call histories.
* **Use Fixtures for Setup/Teardown**: Replace old-style `setUp` and `tearDown` methods with Pytest fixtures. Fixtures are modular, reusable, and cleanly inject test dependencies.
* **Parameterization**: Avoid writing separate test functions for verifying the same logic with different inputs. Use `@pytest.mark.parametrize` to run a single test logic against multiple datasets.

```python
import pytest
from unittest.mock import MagicMock

# Using pytest fixture for shared state/setup
@pytest.fixture
def api_client():
    client = MagicMock()
    client.get.return_value = {"status": "success", "data": 42}
    return client

# Parameterizing tests to reduce code duplication
@pytest.mark.parametrize("input_val, expected", [
    (2, 4),
    (3, 9),
    (4, 16)
])
def test_squares(input_val, expected):
    assert input_val ** 2 == expected

def test_api_call(api_client):
    response = api_client.get("/endpoint")
    assert response["status"] == "success"
    api_client.get.assert_called_once_with("/endpoint")
```

* **Single Responsibility Assertions**: Keep assertions per test to a minimum (ideally a single logical assertion) so that failures pinpoint the exact broken behavior immediately.
* **Environment Configuration**: Always define the pythonpath in configuration files (like `pytest.ini` or `pyproject.toml`) so the test runner can locate the application's source modules reliably.

```ini
# pytest.ini
[pytest]
pythonpath = .
testpaths = tests
```

---


## 11. Registry Pattern for Extensible Architectures

The **Registry Pattern** replaces complex `if-elif` chains with a central dictionary or list mapping keys (like strings, enums, or types) to specific functions, classes, or handlers. This promotes a decoupled, highly extensible, and plugin-friendly architecture.

By using Python decorators, you can automate this registration process, allowing new handlers to register themselves dynamically.

### 🚫 Bad Practice (Verbose `if-elif` chains)
Adding a new handler requires modifying the core decision logic, violating the Open-Closed Principle.
```python
def process_data(data: str, format_type: str) -> str:
    if format_type == "json":
        return format_json(data)
    elif format_type == "xml":
        return format_xml(data)
    elif format_type == "yaml":
        return format_yaml(data)
    else:
        raise ValueError(f"Unsupported format: {format_type}")
```

### ✅ Best Practice (Centralized Registry with Decorators)
Use a registry decorator to register handlers automatically, keeping the core processing logic decoupled.

```python
from typing import Callable, Dict

# 1. Central registry
FORMAT_REGISTRY: Dict[str, Callable[[str], str]] = {}

# 2. Registration decorator
def register_format(name: str) -> Callable[[Callable[[str], str]], Callable[[str], str]]:
    def decorator(func: Callable[[str], str]) -> Callable[[str], str]:
        FORMAT_REGISTRY[name] = func
        return func
    return decorator

# 3. Dynamic self-registration
@register_format("json")
def format_json(data: str) -> str:
    return f"{{\"data\": \"{data}\"}}"

@register_format("xml")
def format_xml(data: str) -> str:
    return f"<data>{data}</data>"

# 4. Clean, extensible execution
def process_data(data: str, format_type: str) -> str:
    if handler := FORMAT_REGISTRY.get(format_type):
        return handler(data)
    raise ValueError(f"Unsupported format: {format_type}")
```

### ⚠️ Pitfalls to Keep in Mind
* **Hidden/Implicit Logic**: Automated registration can make code harder to debug and trace because handlers register themselves as a side effect of importing the module.
* **Import Order Dependency**: Decorators only execute when the module containing them is imported. If registration occurs dynamically (e.g., plugins folder), you must ensure your application explicitly imports/loads all plugin modules (e.g., using `importlib` or package discovery) at startup.

---

## 12. Best Practices for Production-Ready Code

When building and deploying applications to production, follow these key architectural and operational guidelines to ensure reliability, security, scalability, and maintainability:

### A. Use Appropriate Types
Avoid using floating-point types (`float`) for currency, financial data, or any calculation where rounding errors are unacceptable due to precision issues. Instead, use Python's built-in `decimal.Decimal` class to ensure exact decimal representation.

```python
from decimal import Decimal

# 🚫 Bad: Float precision issues
price = 0.1 + 0.2  # 0.30000000000000004

# ✅ Good: Exact precision with Decimal
price = Decimal('0.1') + Decimal('0.2')  # Decimal('0.3')
```

### B. Validate Input
Do not trust client input. Leverage modern validation libraries like Pydantic and web framework tools (e.g., FastAPI query parameters) to enforce strict constraints (e.g., minimum/maximum string lengths, positive numbers, and correct formats) at the boundary of your application to prevent malformed data from propagating.

```python
from pydantic import BaseModel, Field

# ✅ Validate incoming requests automatically
class CreateUserRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    age: int = Field(..., gt=0, lt=150)
```

### C. Decouple Business Logic
Extract core business rules and logic from API routers or controller endpoints into dedicated Service classes or utility layers. This keeps the API transport layer thin, clean, and focused on HTTP concerns (routing, status codes, serialization), while making business logic independently unit-testable.

### D. Implement Persistence
Never store persistent state in-memory or hardcode data. Use a robust Database Management System (DBMS) alongside an Object-Relational Mapper (ORM) like SQLAlchemy or SQLModel. Always couple this setup with database migrations (e.g., using Alembic) to manage schema evolution safely over time.

### E. Add Health Checks
Expose a dedicated `/health` (or `/healthz`) endpoint that returns the status of the service and its key dependencies (like database, cache, or message queue connectivity). This allows infrastructure control planes (e.g., Kubernetes, AWS ECS, or Load Balancers) to perform automated liveness and readiness checks.

### F. Defensive Programming & Error Handling
Avoid returning generic `500 Internal Server Error` responses. Program defensively by intercepting expected failures and raising specific HTTP exceptions (e.g., `404 Not Found` for missing resources, `409 Conflict` for duplicate entries, or `400 Bad Request` for invalid states) to provide meaningful feedback to clients.

```python
from fastapi import HTTPException, status

def get_item(item_id: int):
    item = db.query(Item).get(item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with ID {item_id} not found"
        )
    return item
```

### G. Configuration Management
Do not hardcode database URLs, API keys, or environment settings in your codebase. Manage configurations dynamically using environment variables or a configuration framework like Pydantic Settings. This enables clean separation of code and config across development, staging, and production environments.

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    api_key: str

    class Config:
        env_file = ".env"

settings = Settings()
```

### H. Add Rate Limiting
Protect your APIs from denial-of-service (DoS) attacks, brute-force attempts, and general abuse. Implement rate limiting on public or sensitive endpoints using libraries like `slowapi` or middleware at the gateway level to control the volume of requests a user can make in a given timeframe.

### I. Write Comprehensive Tests
Ensure reliability by automating test coverage for both success paths and failure edge cases. Set up a separate testing environment (such as using an in-memory SQLite database or Dockerized test containers) to run tests in isolation without mutating production or development data.

### J. Monitoring & Logging
Never use `print()` statements for diagnostic output in production environments. Use Python's standard `logging` library or structured logging (e.g., `structlog`) to emit logs with appropriate levels (`INFO`, `WARNING`, `ERROR`, `DEBUG`) and trace IDs, allowing centralized log management tools to parse and query them efficiently.

### K. Automated Deployment
Standardize the application environment using Docker to bundle code, dependencies, and system configurations into portable, reproducible container images. Automate build, test, and deployment workflows using Continuous Integration/Continuous Deployment (CI/CD) pipelines like GitHub Actions to ensure consistent and reliable releases.

---

## 13. Scalable FastAPI Project Structure and Configuration

For building scalable, production-ready FastAPI applications, maintain clear boundaries between the API layer, business logic, data persistence, and configurations.

### A. Balanced Folder Structure

Keep application source code (`app/`) separated from tests (`tests/`) at the root level. Mirror the application structure within your test directory to keep tests organized and easily discoverable.

```text
├── app/
│   ├── api/
│   │   └── v1/          # Thin API routes/endpoints handling HTTP requests & responses
│   ├── core/            # Cross-cutting configurations (Settings, logging, security)
│   ├── database/        # Database sessions, engines, and migrations setup
│   ├── models/          # Pydantic validation schemas (request/response models)
│   ├── services/        # Service layer containing core business logic
│   └── main.py          # Application entry point where routes/middlewares are registered
├── tests/               # Mirrors the app/ folder structure for test files
│   ├── api/
│   ├── services/
│   └── conftest.py      # pytest fixtures, database overrides, test configurations
├── .env                 # Environment variables (local-only, not committed)
├── .python-version      # Target python interpreter version
├── pyproject.toml       # Centralized dependencies and tool configurations
├── Dockerfile           # Standardized container environment
└── docker-compose.yml   # Multi-container local development orchestrations
```

### B. Centralized Configuration Management
Leverage `pydantic-settings` to load configurations dynamically from environment variables or a `.env` file. This prevents sensitive credentials from leaking into source control and ensures clean configuration validation at startup.

### C. Thin API Layer (Decoupling)
Keep FastAPI routes lightweight. The API layer should only concern itself with HTTP request translation, dependency resolution (e.g., getting DB sessions), calling the appropriate business logic service, and returning the structured response. Moving all business logic into service classes (`services/`) ensures a clean separation of concerns and easier testing.

### D. Dependency Injection and Testing
Utilize FastAPI's dependency injection (`Depends`) to inject services or database sessions. During testing, leverage dependency overrides (`app.dependency_overrides`) to swap real databases with an isolated, in-memory database or real services with mock implementations.

```python
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

app = FastAPI()

# Core implementation using dependency injection
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/items/")
def read_items(db: Session = Depends(get_db)):
    return item_service.get_all(db)

# Overriding dependencies in test setup
def get_test_db():
    # Return mock or in-memory database session
    ...

app.dependency_overrides[get_db] = get_test_db
```

### E. Consistent Environments
Always use standard build and orchestration tooling (`Docker`, `Docker Compose`, and dependency manifests like `pyproject.toml`) to ensure local development environments mirror the production deployment environments exactly.


