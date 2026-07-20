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
