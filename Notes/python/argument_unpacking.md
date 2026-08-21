# Python Argument Packing and Unpacking (`*args` and `**kwargs`)

This note covers Python's iterable and dictionary unpacking mechanisms
(`*` and `**`), parameter enforcement rules, design patterns, anti-patterns,
and enterprise interview questions tailored for a 5 YOE software engineer.

---

## 1. Structured Notes

### 1.1 Core Concepts: Packing vs. Unpacking

Python uses `*` (single asterisk) and `**` (double asterisk) for two
distinct operations depending on context: **Packing** (in function
definitions) and **Unpacking** (at call sites or expression contexts).

| Context | Syntax | Description |
| :--- | :--- | :--- |
| **Packing** | `def fn(*args, **kwargs)` | Collects positional/keyword args into `tuple`/`dict`. |
| **Unpacking** | `fn(*seq, **mapping)` | Expands elements of iterable/dict into arguments. |
| **Expression** | `{**d1, **d2}` | Destructures collections or merges dicts inline. |

---

### 1.2 Unpacking at Function Call Sites

When `**` is prefixed to a dictionary at a function call site, Python
unpacks the dictionary key-value pairs into explicit **keyword arguments**.

```python
def create_user(email: str, password: str, name: str) -> dict:
    return {"email": email, "password": password, "name": name}


user_details = {
    "email": "dev@example.com",
    "password": "secure_password_123",
    "name": "Alex Smith",
}

# Unpacking dictionary as keyword arguments
user = create_user(**user_details)

# Equivalent explicit call:
# user = create_user(
#     email="dev@example.com",
#     password="secure_password_123",
#     name="Alex Smith"
# )
```

#### Rules for Call-Site Unpacking:
1. Dictionary keys **must be strings** matching valid identifier names.
2. If dictionary keys do not match function parameters (and function
   does not take `**kwargs`), Python raises a `TypeError`.
3. Passing an explicit keyword argument alongside a dictionary with the
   same key raises `TypeError: got multiple values for keyword argument`.

---

### 1.3 Packing in Function Definitions

In function definitions, `**kwargs` collects all remaining keyword arguments
not explicitly matched by preceding parameters into a standard `dict`.

```python
def log_event(event_name: str, **metadata: str) -> None:
    print(f"Event: {event_name}")
    print(f"Metadata type: {type(metadata)}")  # <class 'dict'>
    for key, value in metadata.items():
        print(f"  {key}: {value}")


log_event("USER_LOGIN", user_id="u123", ip_address="192.168.1.1")
```

---

### 1.4 Advanced Parameter Enforcement

Python 3.8+ introduced positional-only parameters (`/`), while keyword-only
parameters (`*`) enable strict API contract enforcement.

```python
# Signature breakdown:
# - 'a', 'b': Positional-only
# - 'c': Positional or keyword
# - 'd': Keyword-only
# - 'kwargs': Remaining keyword arguments
def complex_sig(a: int, b: int, /, c: int, *, d: int, **kwargs: str) -> None:
    pass


# Valid calls:
complex_sig(1, 2, c=3, d=4, custom_flag="enabled")
complex_sig(1, 2, 3, d=4)
```

---

### 1.5 Dictionary Merging and Updating (Python 3.9+)

Python 3.9+ introduced union operators (`|` and `|=`) alongside `**`
unpacking for dictionary combination.

```python
default_config = {"host": "localhost", "port": 5432, "timeout": 30}
user_config = {"port": 5433, "debug": True}

# Method 1: Double asterisk unpacking
merged_unpacking = {**default_config, **user_config}

# Method 2: Python 3.9+ union operator (preferred for readability)
merged_union = default_config | user_config
```

---

### 1.6 Common Pitfalls & Anti-Patterns

1. **The "God kwargs" Anti-Pattern**:
   - Overusing `**kwargs` across multiple function layers destroys static
     typing (`mypy`), hides parameters from IDE autocompletion, and causes
     silent parameter drops if intermediate functions forget to forward.
   - *Fix*: Use explicit parameters, `TypedDict`, or Pydantic models.

2. **Unchecked `KeyError`**:
   - Accessing `kwargs["key"]` directly raises `KeyError` if omitted by
     callers. Use `kwargs.get("key", default)` or explicit parameters.

3. **Performance Overhead**:
   - `**kwargs` allocates a new `dict` object on every function call.
     In high-frequency loops, explicit parameters eliminate dictionary
     instantiation costs.

---

## 2. Interview Questions & Answers (5 YOE Level)

### Q1 (Conceptual): Unpacking vs. Packing Mechanics

**Question:**
Explain the internal mechanics of dictionary unpacking (`**`) in Python.
How does the interpreter handle call-site unpacking versus definition-side
packing?

**Answer:**
At the bytecode level, Python handles unpacking and packing differently:

1. **Call-Site Unpacking (`fn(**data)`)**:
   - Executed via `CALL_FUNCTION_EX` with a mapping expansion flag.
   - The interpreter verifies `data` is a mapping (`PyMapping_Check`).
   - Keys are validated to ensure they are string objects (`PyUnicode`).
   - Key-value pairs are bound to code object parameters (`co_varnames`).
     Duplicate bindings raise a `TypeError` during frame creation.

2. **Definition-Side Packing (`def fn(**kwargs)`)**:
   - The interpreter builds a new Python `dict` containing keyword
     arguments that do not map to named parameters in `co_varnames`.
   - The `kwargs` variable receives this dictionary inside the new frame.

---

### Q2 (Practical/Scenario): Refactoring `**kwargs` in Microservices

**Question:**
In a microservice codebase, `process_order(**kwargs)` passes data through
4 helper layers, leading to runtime bugs. How do you refactor this safely?

**Answer:**
1. **Define a `TypedDict` or Pydantic Model** for the schema contract:
   ```python
   from typing import TypedDict


   class OrderPayload(TypedDict, total=False):
       order_id: str
       user_id: str
       amount: float
       currency: str
   ```

2. **Refactor Function Signature with Unpack Hints**:
   ```python
   from typing import Unpack


   def process_order(**kwargs: Unpack[OrderPayload]) -> None:
       order_id = kwargs.get("order_id")
       if not order_id:
           raise ValueError("Missing required key: order_id")
       # Business logic...
   ```

3. **Migrate Callers** to pass structured objects or validated Pydantic
   instances instead of raw untyped dictionaries.

---

### Q3 (Coding/Implementation): Kwargs Sanitizer & Forwarder Decorator

**Question:**
Write a decorator `intercept_and_forward` that intercepts calls to any
function, injects a standard `request_id` into `kwargs` if missing, removes
`_private` keys, and forwards clean arguments.

**Answer:**

```python
import functools
from typing import Any, Callable, TypeVar

F = TypeVar("F", bound=Callable[..., Any])


def intercept_and_forward(func: F) -> F:
    """Decorator that sanitizes kwargs and injects request_id."""

    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        sanitized = {k: v for k, v in kwargs.items() if not k.startswith("_")}
        sanitized.setdefault("request_id", "req-default-0000")
        return func(*args, **sanitized)

    return wrapper  # type: ignore[return-value]


@intercept_and_forward
def submit_job(job_name: str, request_id: str, priority: int = 1) -> str:
    return f"Job: {job_name} | RequestID: {request_id} | Priority: {priority}"


res = submit_job("etl_sync", _internal_token="secret", priority=5)
print(res)
# Output: Job: etl_sync | RequestID: req-default-0000 | Priority: 5
```

---

### Q4 (System Design / Architecture): `**kwargs` in Test Suites & Factories

**Question:**
In frameworks like Django and pytest fixture suites, dictionary unpacking
(`**payload`) is used for factory methods (e.g., `create_user(**user_details)`).
What are the design trade-offs?

**Answer:**

**Advantages:**
- **DRY Fixtures**: Enables test helpers to supply default attributes
  while allowing individual tests to override specific fields.
- **Schema Resilience**: Adding non-mandatory model fields does not break
  existing test calls across hundreds of test files.

**Disadvantages & Trade-offs:**
- **Silent Failures / Invalid Fields**: Unpacking invalid keys into
  Django models raises runtime `TypeError` rather than failing type checks.
- **Hidden Dependencies**: Overshadowing required fields relies on
  runtime validation instead of compile-time contract enforcement.

**Best Practice Mitigation:**
Use Factory Boy (`factory.django.DjangoModelFactory`) or explicit builder
patterns with typed default dictionaries for enterprise test suites.

---

## References

- [Python Docs - Defining Functions](https://docs.python.org/3/tutorial/controlflow.html)
- [PEP 448 - Additional Unpacking](https://peps.python.org/pep-0448/)
- [PEP 570 - Positional-Only Parameters](https://peps.python.org/pep-0570/)
- [PEP 692 - Unpack for Typed kwargs](https://peps.python.org/pep-0692/)
