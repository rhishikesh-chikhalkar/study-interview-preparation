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

