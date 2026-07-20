# Testing in Python

## `assertEqual` vs `assertEquals`

### Comparison

| Method             | Status                   | Python Compatibility               | Behavior                                                                |
| :----------------- | :----------------------- | :--------------------------------- | :---------------------------------------------------------------------- |
| **`assertEqual`**  | **Active (Recommended)** | All versions                       | Checks if two values are equal.                                         |
| **`assertEquals`** | **Deprecated / Removed** | Deprecated in 3.2, Removed in 3.12 | Legacy alias of `assertEqual`. Throws `AttributeError` in Python 3.12+. |

### Example

```python
import unittest

class TestExample(unittest.TestCase):
    def test_values(self):
        # Correct approach
        self.assertEqual(1 + 1, 2)

        # Avoid (Raises AttributeError in Python 3.12+)
        # self.assertEquals(1 + 1, 2)
```

### Why it was removed

Python standard library cleaned up legacy aliases to keep the API surface minimal, consistent, and PEP 8 compliant.

## Executable Test Files: `__name__ == "__main__"` & `unittest.main()`

### `__name__ == "__main__"` (Execution Context)

- **When run directly:** (e.g., `python test_stack.py`), Python assigns `__name__ = "__main__"`.
- **When imported:** (e.g., `import test_stack`), Python sets `__name__` to the module name/path (`"test_stack"`).
- **Purpose:** Acts as a guard clause to separate executable script logic from reusable module exports, preventing tests from auto-running on imports.

### `unittest.main()` (Test Runner Entrypoint)

- **What it does:** Scans the current module for subclasses of `unittest.TestCase`, discovers all methods prefixed with `test_`, executes them (along with `setUp` and `tearDown`), and reports results.
- **Modern Context:** Modern test runners like `pytest` discover and run test files directly, making the `unittest.main()` invocation optional but still convenient for standalone execution.

---

## Pytest

`pytest` is a modern, clean, and feature-rich testing framework in Python. Unlike `unittest`, it does not require class inheritance or custom assertion methods.

### 1. Plain `assert` Statements
`pytest` uses standard Python `assert` statements. When a test fails, `pytest` performs AST-rewriting to output extremely descriptive diffs.

```python
# Unittest
self.assertEqual(stack.size(), 1)

# Pytest
assert stack.size() == 1
```

### 2. Fixtures (`@pytest.fixture`)
Instead of class-based `setUp()` and `tearDown()` methods, `pytest` uses fixtures to inject dependencies or fresh state. A fixture function returns a value and is passed into test functions by matching its argument name.

```python
import pytest

@pytest.fixture
def stack():
    return Stack()

def test_stack_is_empty(stack):
    assert stack.is_empty()
```

### 2.1 Fixture Lifecycles (Scope & Teardowns)
`pytest` fixtures allow you to specify their **scope** (how long they live) and run teardown code using the `yield` statement instead of `return`.

#### Scopes:
*   **`scope="function"` (Default)**: Setup runs before each test; teardown runs after each test. Similar to `setUp()` / `tearDown()` in `unittest`.
*   **`scope="module"`**: Setup runs once per test file; teardown runs after all tests in the file complete. Similar to `setUpClass()` / `tearDownClass()`.
*   **`scope="session"`**: Setup runs once for the entire test runner invocation.

#### Example (Database connection testing):
```python
import pytest

@pytest.fixture(scope="module")
def db_connection():
    # Setup: runs ONCE for the entire file
    connection = create_db_connection()
    yield connection
    # Teardown: runs after all tests in this file finish
    connection.close()

@pytest.fixture(scope="function")
def db_cursor(db_connection):
    # Setup: runs before EACH test method
    cursor = db_connection.cursor()
    yield cursor
    # Teardown: runs after EACH test method
    cursor.close()

def test_insert(db_cursor):
    assert db_cursor.execute("INSERT INTO users VALUES (1, 'Alice')")
```

### 3. Asserting Exceptions (`pytest.raises`)

Use `pytest.raises` as a context manager to assert that an operation raises a specific exception.

```python
with pytest.raises(IndexError):
    stack.pop()
```

### 4. Running Pytest with `uv`
To run your test suite:

- **Run all tests in current directory:**
  ```bash
  uv run pytest .
  ```
- **Run a specific file:**
  ```bash
  uv run pytest tests/test_stack_using_pytest.py
  ```
- **Run a specific test case by pattern:**
  ```bash
  uv run pytest tests/test_stack_using_pytest.py -k test_new_stack_is_empty
  ```

