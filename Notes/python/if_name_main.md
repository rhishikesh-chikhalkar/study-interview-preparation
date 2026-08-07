# Python `__name__` and `__main__` Execution Guard

Understanding `__name__` and `__main__` is fundamental to mastering Python module execution,
script architecture, namespace management, and process creation.

---

## 1. Structured Notes

### Core Concepts

When the Python interpreter reads a source file, it automatically defines several special
variables (dunder variables). One of the most important is `__name__`.

- **`__name__`**: A built-in string variable managed by Python that identifies the execution
  context of the current module.
- **`"__main__"`**: A standard string literal assigned to `__name__` when a Python script is
  executed as the top-level entry point of a program.

### Execution Contexts & Behavior Matrix

| Execution Context | `__name__` Value | Explanation |
| :--- | :--- | :--- |
| Direct invocation (`python script.py`) | `"__main__"` | Executed as top-level program. |
| Module execution (`python -m pkg.script`) | `"__main__"` | Executed as top-level module script. |
| Interactive REPL / `python -c` | `"__main__"` | Top-level interactive environment. |
| Imported module (`import script`) | `"script"` | Set to module's name relative to import path. |
| Sub-package import (`import pkg.mod`) | `"pkg.mod"` | Fully qualified module path name. |

### Mechanics: How Python Sets `__name__`

1. **Top-Level Execution**:
   - Python creates a top-level module scope called `__main__`.
   - The interpreter executes code in that file sequentially within `sys.modules['__main__']`.

2. **Module Import**:
   - Python checks `sys.modules` to see if the module has already been loaded.
   - If not, Python creates a new module object, sets `__name__ = "module_basename"`, and
     executes the file top-to-bottom to populate the module's dictionary.

### The Purpose of `if __name__ == "__main__":`

The guard statement isolates execution logic from definition logic.

```python
def calculate_metrics(data: list[float]) -> dict[str, float]:
    """Calculate summary statistics for input data."""
    return {"mean": sum(data) / len(data) if data else 0.0}


def main() -> None:
    """Entry point logic executed only when run directly."""
    sample_data = [10.5, 20.0, 30.5]
    results = calculate_metrics(sample_data)
    print(f"Results: {results}")


if __name__ == "__main__":
    main()
```

#### Key Benefits of the Guard Pattern
1. **Import Safety**: Other scripts or test suites can safely import functions, classes, and
   constants without triggering side effects (e.g., database connections, CLI prompts).
2. **Global Scope Protection**: Wrapping execution logic inside `def main():` prevents
   temporary variables from leaking into global module scope, aiding garbage collection.
3. **Testability**: Unit tests can target internal functions directly without invoking CLI code.

---

### Advanced Production Scenarios

#### 1. Package Entry Points with `__main__.py`
When executing a package directory or zip file using `python -m mypackage`, Python looks for
a file named `__main__.py` inside the package directory and executes it with
`__name__ = "__main__"`.

```
mypackage/
├── __init__.py
├── __main__.py
└── core.py
```

Inside `mypackage/__main__.py`:
```python
import sys
from mypackage.core import run_cli

if __name__ == "__main__":
    sys.exit(run_cli())
```

#### 2. Multiprocessing Safeguards (`spawn` vs `fork`)
On Windows and macOS (Python 3.8+ default), `multiprocessing` uses the `spawn` start method
instead of `fork`. Spawning creates a fresh Python interpreter process and imports the main
script to reconstruct the environment.

- **Without Guard**: Importing the script spawns a new process, which re-imports the script,
  creating another process in an infinite recursive loop resulting in `RuntimeError`.
- **With Guard**: The guard prevents child processes from re-executing process creation logic.

```python
import multiprocessing as mp


def worker_task(task_id: int) -> None:
    print(f"Worker {task_id} processing")


def main() -> None:
    processes = []
    for i in range(4):
        p = mp.Process(target=worker_task, args=(i,))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()


# Mandatory guard for cross-platform multiprocessing safety
if __name__ == "__main__":
    main()
```

#### 3. Standard Library Entry Points (`runpy`)
Python's standard library provides `runpy.run_module()` and `runpy.run_path()`, which manipulate
`__name__` programmatically to execute scripts inside specified module contexts.

---

## 2. Interview Questions & Answers (5 YOE Level)

### Q1: Conceptual / Deep Dive
**Question**: Explain how Python handles `__name__` in `sys.modules` during execution, and
describe what happens when a script imports itself directly or indirectly.

**Answer**:
When Python executes a script directly (e.g., `python app.py`), it creates a module object
bound to `sys.modules['__main__']` with `__name__ = "__main__"`.

If `app.py` contains `import app`, Python checks `sys.modules['app']`. Since `app` is not yet in
`sys.modules` (only `'__main__'` exists), Python loads and executes `app.py` a SECOND time,
this time setting `__name__ = "app"` in `sys.modules['app']`.

This results in duplicate module execution, two distinct sets of global variables, and broken
class identity checks (`isinstance(obj, Class)` fails if created across the two imports).

---

### Q2: Scenario / Troubleshooting
**Question**: A production batch job using Python `multiprocessing` runs smoothly on Linux
servers but crashes immediately with `RuntimeError: An attempt has been made...` when executed on
macOS or Windows. What is the root cause and resolution?

**Answer**:
- **Root Cause**: Linux defaults to the `fork` start method, where the child process inherits
  the parent's memory space without re-executing the script. Windows and macOS default to `spawn`,
  which launches a new Python process and imports the entry-point script to rebuild context.
- Without `if __name__ == "__main__":`, spawned child processes re-execute process creation
  logic at top level, entering an infinite loop until `RuntimeError` is raised.
- **Resolution**: Wrap process instantiation and execution logic inside `def main():` guarded
  by `if __name__ == "__main__":`.

---

### Q3: Coding / Best Practice
**Question**: Write a production-ready Python CLI entry point script utilizing `argparse`, clean
error handling, appropriate exit codes (`sys.exit`), and isolated `main()` function.

**Answer**:
```python
import argparse
import sys
from typing import Sequence


def parse_args(args: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Production data processor CLI")
    parser.add_argument(
        "--input",
        required=True,
        help="Path to input dataset file",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose output logging",
    )
    return parser.parse_args(args)


def run_pipeline(input_path: str, verbose: bool) -> int:
    """Execute main processing pipeline. Returns status exit code."""
    try:
        if verbose:
            print(f"Processing input file: {input_path}")
        # Core logic executed here
        return 0
    except FileNotFoundError as err:
        print(f"Error: Input file not found - {err}", file=sys.stderr)
        return 1
    except Exception as err:
        print(f"Unexpected processing failure: {err}", file=sys.stderr)
        return 2


def main(args: Sequence[str] | None = None) -> None:
    parsed_args = parse_args(args)
    exit_code = run_pipeline(parsed_args.input, parsed_args.verbose)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
```

---

### Q4: System Design / Package Architecture
**Question**: How would you structure a Python package intended to be run both as a CLI tool
via `python -m pkgname` and as an installable binary via `pip install`, while maintaining clean
layer separation?

**Answer**:
1. **Package Layout**:
   ```
   src/mypackage/
   ├── __init__.py
   ├── __main__.py      # CLI invocation entry for `python -m mypackage`
   ├── cli.py           # Argparse / Click / Typer interface parser
   └── core/            # Business & domain logic (decoupled from CLI)
   ```
2. **`pyproject.toml` configuration**:
   ```toml
   [project.scripts]
   mypackage = "mypackage.cli:main"
   ```
3. **`__main__.py` pattern**:
   ```python
   import sys
   from mypackage.cli import main

   if __name__ == "__main__":
       sys.exit(main())
   ```
4. **Benefits**:
   - `core/` remains pure Python, independent of CLI frameworks.
   - `cli.py` handles input parsing and converts CLI options to core domain arguments.
   - `__main__.py` ensures seamless `python -m mypackage` execution.
   - Setuptools/flit creates executable entry points for shell environments during installation.
