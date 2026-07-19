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
```
