# Python `__all__` (Dunder All) & Package Re-exporting

## Overview

In Python, `__all__` is a module-level list of strings defining the explicit **public API**
of a module or package. It specifies which symbols are exported when `from module import *`
is executed, and serves as an authoritative boundary for static analysis tools, linters
(e.g., Pyright, Ruff), and IDE autocompletion.

---

## 1. Primary Core Mechanics

### A. Controlling Wildcard Imports (`from module import *`)
- **Without `__all__`**: Python imports all symbols defined in the module, except those
  starting with an underscore (`_`).
- **With `__all__`**: Python imports **only** the symbols explicitly listed in `__all__`.

```python
# utils.py
__all__ = ["public_func"]


def public_func():
    return "Public API"


def _helper_func():
    return "Private Helper"


def internal_utility():
    return "Not in __all__"
```

```python
# main.py
from utils import *

public_func()  # Works
# internal_utility() -> NameError: name 'internal_utility' is not defined
```

### B. Package Re-Exporting in `__init__.py`
`__init__.py` files convert directories into Python packages. Using `__all__` in `__init__.py`
allows submodules to be re-exported cleanly at the top-level package namespace.

```python
# src/config/__init__.py
from src.config.providers import (
    GEMINI_BASE_URL,
    PROVIDER_REGISTRY,
    ProviderMeta,
)

__all__ = ["GEMINI_BASE_URL", "PROVIDER_REGISTRY", "ProviderMeta"]
```

This allows consumers to write clean imports:
```python
from src.config import PROVIDER_REGISTRY  # Clean top-level package import
```

---

## 2. Best Practices & Static Analysis

1. **Explicit API Boundaries**: Even if wildcard imports are avoided, defining `__all__`
   serves as self-documenting code indicating which symbols are intended for external use.
2. **Linter & Type Checker Contract**: Tools like `pyright`, `mypy`, and `ruff` use `__all__`
   in `__init__.py` to mark symbols as intentionally re-exported, suppressing unused import
   (`F401`) warnings.
3. **Immutability Convention**: `__all__` should be a `list` or `tuple` of strings matching
   symbol names.
4. **Direct Import Precedence**: `__all__` does **not** prevent direct imports
   (`from module import _private`). In Python, privacy is by convention (`_`), not restriction.

---

## 3. Interview Questions & Answers (5 YOE Level)

### Q1: Conceptual
**Question**: What is `__all__` in Python, and how does it interact with `from module import *`
vs. explicit direct imports like `from module import secret_func`?

**Answer**:
- `__all__` is a module-level sequence of strings defining public exports.
- **Wildcard import (`from module import *`)**: Strictly respects `__all__`. Only symbols
  listed in `__all__` are imported into the caller's namespace.
- **Direct import (`from module import secret_func`)**: Completely ignores `__all__`. Python
  allows importing any accessible symbol regardless of whether it is in `__all__` or prefixed
  with `_`.

---

### Q2: Practical / Scenario
**Question**: In a large Python package, `__init__.py` imports submodules to provide clean
package-level access, but linters flag the imports as unused (`F401`). How does `__all__` fix this?

**Answer**:
When `__init__.py` contains `from .submodule import SubClass`, linters assume the import is
unused if it isn't referenced inside `__init__.py`.
Adding `__all__ = ["SubClass"]` informs linters and type checkers (Pyright/Mypy) that `SubClass`
is intentionally **re-exported** as part of the public package API, suppressing the `F401`
warning and enabling full autocomplete.

---

### Q3: Architecture / Package Design
**Question**: How would you design the top-level API for a multi-layered Python SDK (e.g.,
`core`, `config`, `services`) to expose a clean developer interface?

**Answer**:
1. Implement internal modular logic under `src/core/`, `src/config/`, and `src/services/`.
2. In each package's `__init__.py`, import primary public classes and declare `__all__`:
   ```python
   # src/services/__init__.py
   from src.services.evaluator import LLMEvaluator

   __all__ = ["LLMEvaluator"]
   ```
3. Expose top-level SDK entries in the root `__init__.py` to hide deep directory nesting.

---

## References

- [Python Package Imports Docs](https://docs.python.org/3/tutorial/modules.html)
- [PEP 8 Style Guide for Python Code](https://peps.python.org/pep-0008/)
