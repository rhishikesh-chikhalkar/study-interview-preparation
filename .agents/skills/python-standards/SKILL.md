---
name: python-standards
description: Use when writing, reviewing, or debugging Python code. Covers docstrings, imports, logging, exception handling, async patterns, and ruff/pytest validation for production-grade Python development.
---

# Python Coding Standards

Production-grade Python standards for all projects.

---

## 1. Documentation & Readability

- **Mandatory Docstrings**: Every module, class, and public function/method must have a **single-line docstring** using `"""Triple double quotes"""`. Modules and classes must never be left undocumented.
- **Formatting**: Add exactly one empty line immediately following any docstring. Keep lines strictly under 100 characters. Use Black-style formatting: multi-line function calls/definitions should have one argument per line with a trailing comma. No trailing whitespace allowed.
- **No Inline Comments**: Do NOT use inline comments (comments on the same line as code). Place explanations on the line *before* the code. Prefer self-documenting code over comments.
- **Indentation**: Never put multiple statements on a single line (avoid `if x: return y`). Use parentheses for multi-line expressions.

---

## 2. Imports & Best Practices

- **Ordering**: 1. Standard Library, 2. Third-party, 3. Local (separated by single newlines).
- **Security**: Specify `encoding="utf-8"` in all text-based `open()` calls.
- **Exception Chaining**: Always use `raise ... from e` when re-raising exceptions to preserve the original traceback.
- **Empty Checks**: Use Pythonic truthiness (`if not my_list:`) instead of `len() == 0`.
- **SQLAlchemy**: When subclassing `TypeDecorator`, override `process_literal_param` and `python_type`.
- **Closure Safety**: Fix "cell variable defined in loop" by passing loop variables as default arguments.
- **No Shadowing**: Never redefine Python built-in names (`set`, `list`, `id`, `type`, `map`, `input`, `str`).
- **No Dead Code**: Remove unused variables, arguments, and imports immediately. Unused imports in `__init__.py` should use `__all__` or `# noqa: F401`. This includes unused mocks in tests.

---

## 3. Production-Grade Logging

- **Logger Init**: `logger = logging.getLogger(__name__)` at the top of every module.
- **Exception Logging**: Inside `except` blocks, ALWAYS use `logger.exception("Descriptive message")`. Never use `logger.error` for exceptions unless you want to suppress the traceback.
- **Log Levels**:
    - `INFO`: Significant business milestones.
    - `WARNING`: Non-fatal issues or recoverable errors.
    - `ERROR`: Operations that failed but did not crash the app.
    - `DEBUG`: Detailed diagnostic data; must not leak into production logs.
- **Contextual Metadata**: Include identifiers (`user_id`, `provider`, `file_id`) in log messages.
- **Milestone Logging**: Log entry and exit of complex/long-running operations.
- **PII Sanitization**: NEVER log raw passwords, tokens, or PII. Mask emails, truncate tokens.
- **No Generic Logs**: Use specific, actionable messages instead of "Error occurred".

---

## 4. Performance & Async

- **Asynchronous I/O**: Use `asyncio` for I/O bound tasks wherever applicable.
- **String Building**: Use list accumulation (not `+=` in loops).
- **Caching**: Cache env vars at init; prefer iterative over recursive when stack depth matters.

---

## 5. Validation Commands

Run checks in this order:

```bash
uv run ruff format
uv run ruff check
uv run ty check
uv run pytest
```
