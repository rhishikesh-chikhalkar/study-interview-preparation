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
