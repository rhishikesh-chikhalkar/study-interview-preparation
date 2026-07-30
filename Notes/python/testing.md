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

---

## Subtests and Parametrization (Looping Test Cases)

When you need to run a series of similar test cases (e.g., testing multiple inputs against the same logic), stopping execution on the first failure is undesirable. Both `unittest` and `pytest` offer ways to continue executing remaining inputs even if one fails.

### 1. `unittest`: `self.subTest()`
`self.subTest()` is a context manager. If an assertion fails inside the block, `unittest` records the failure but continues executing the remaining iterations of the loop.

```python
import unittest

class TestNumbers(unittest.TestCase):
    def test_even_numbers(self):
        for i in [2, 4, 5, 6, 8]:
            with self.subTest(i=i):
                self.assertEqual(i % 2, 0)
```

### 2. `pytest`: Parametrization (Idiomatic Way)
Instead of loop-based subtests, `pytest` natively encourages the `@pytest.mark.parametrize` decorator. This generates separate, fully independent test cases at collect-time.

```python
import pytest

@pytest.mark.parametrize("i", [2, 4, 5, 6, 8])
def test_even_numbers(i):
    assert i % 2 == 0
```

### 3. `pytest`: `pytest-subtests` Plugin (Direct Equivalent)
If parameters are dynamic (determined at runtime inside a test rather than at collect-time), you can use the official `pytest-subtests` plugin.

Install the plugin:
```bash
uv pip install pytest-subtests
```

Use the `subtests` fixture in your test function:
```python
def test_even_numbers(subtests):
    for i in [2, 4, 5, 6, 8]:
        with subtests.test(i=i):
            assert i % 2 == 0

---

## Monkey Patching vs. Mocking

When writing unit tests, you frequently need to isolate the system under test from external dependencies (such as databases, file systems, or network requests). Both **monkey patching** and **mocking** are techniques used to achieve this isolation, but they operate differently.

### 1. Monkey Patching

**Monkey patching** is the mechanism of dynamically replacing a function, class, method, or attribute at runtime (execution time) with a fake or modified version.

* **Purpose:** It temporarily overrides existing behavior, typically to prevent side-effects (such as making actual HTTP calls to external APIs).
* **Usage:** Pytest provides a built-in `monkeypatch` fixture to safely modify attributes, dictionary items, or environment variables, automatically reverting the changes after the test completes.

#### Example (Monkey Patching `httpx.get`):
```python
import httpx

def test_fetch_data(monkeypatch):
    # Dynamic runtime replacement function
    def mock_get(url):
        class FakeResponse:
            def json(self):
                return {"data": "mocked_response"}
        return FakeResponse()

    # Monkey patching the target dependency at runtime
    monkeypatch.setattr(httpx, "get", mock_get)

    response = httpx.get("https://api.example.com")
    assert response.json() == {"data": "mocked_response"}
```

---

### 2. Mocking

**Mocking** uses specialized test-double objects—most notably `unittest.mock.MagicMock` or `Mock` in Python—to simulate complex dependencies.

* **Purpose:** Mocks are designed specifically for testing. In addition to acting as placeholder objects, they record every interaction (calls, parameters, counts) and expose built-in assertion methods to verify usage.
* **Usage:** Mocks allow you to check if a method was called correctly (e.g., `assert_called_once_with`) without writing boilerplate logic to track call states.

#### Example (Mocking with `MagicMock`):
```python
from unittest.mock import MagicMock

def test_user_service():
    # Instantiate a mock repository object
    mock_repo = MagicMock()
    # Configure return value
    mock_repo.get_user.return_value = {"id": 1, "name": "Alice"}

    # Execute system under test
    user = mock_repo.get_user(1)

    # Built-in assertions to verify interaction
    assert user["name"] == "Alice"
    mock_repo.get_user.assert_called_once_with(1)
```

---

### 3. Comparison Summary

| Feature | Monkey Patching | Mocking |
| :--- | :--- | :--- |
| **Definition** | The broad mechanism of dynamically replacing code/attributes at runtime. | The practice of using mock objects (`MagicMock`) to simulate dependencies. |
| **Approach** | Typically replaces a reference with a standard Python function or basic fake. | Replaces a reference with a sophisticated mock object that tracks calls. |
| **Built-in Assertions** | No. Tracking calls requires manual helper variables or counters. | Yes. Provides helper methods (`assert_called_once`, `assert_called_with`). |
| **Brittleness** | Higher. Manually managing dynamic attributes can easily leak state or mask typos. | Lower. Mocks can be configured strictly (e.g., `spec=True`) to match class APIs. |

```

