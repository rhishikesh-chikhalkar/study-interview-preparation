# Python Decorators - Complete Notes

# DAY 1: Python Decorators — Part 1
**Date:** 11 May 2026 (Mon) | **Duration:** 3-4 hrs

---

## THEORY — What to Learn

### What is a Decorator?

A decorator is a function that wraps another function to extend or change its behaviour WITHOUT modifying the original code. Think of it like adding a phone case to your iPhone — same phone, but now protected.

**Real-World Framework Examples:**
- Flask: `@app.route('/home')`
- FastAPI: `@app.get('/users')`
- Django: `@login_required`
- pytest: `@pytest.fixture`
- Celery: `@app.task`

Understanding decorators deeply = understanding how frameworks work.

### What is a Higher-Order Function?

Functions that take other functions as arguments OR return functions as output. Decorators are built on this concept.

```python
# Function takes another function as argument
def higher_order_func(func):
    def wrapper():
        print("Before")
        func()
        print("After")
    return wrapper

# Function returns another function
def make_multiplier(n):
    def multiplier(x):
        return x * n
    return multiplier

times3 = make_multiplier(3)
print(times3(10))  # 30
```

### Basic Decorator Syntax

```python
# Both are EXACTLY the same:

# Method 1: Using @ syntax (Pythonic)
@my_decorator
def greet():
    print('Hello!')

# Method 2: Manual application (what @ syntax does)
def greet():
    print('Hello!')
greet = my_decorator(greet)
```

The `@` symbol is just syntactic sugar for function reassignment.

### Wrapper Functions

The inner function that wraps the original function.

**Key Rules:**
- Must accept `*args, **kwargs` to handle any function signature
- Must call the original function: `result = func(*args, **kwargs)`
- Must return the result from the original function
- Can add code before and after the function call

```python
def my_decorator(func):
    def wrapper(*args, **kwargs):  # Generic signature
        print('Before')
        result = func(*args, **kwargs)  # Call original
        print('After')
        return result  # Return the result
    return wrapper
```

### Decorator Execution Order

**IMPORTANT:** Decorators run at **import/definition time**, NOT at call time. This is a very common interview trap!

```python
def my_decorator(func):
    print("Decorator is running!")  # Runs when function is DEFINED
    def wrapper():
        print("Wrapper is running!")  # Runs when function is CALLED
        func()
    return wrapper

@my_decorator
def greet():
    print("Hello!")

# Output so far: "Decorator is running!"

greet()
# Output now: "Wrapper is running!" then "Hello!"
```

### Stacking Decorators

When multiple decorators are applied, they execute from **bottom to top** (inside-out).

```python
@decorator1
@decorator2
@decorator3
def func():
    pass

# Equivalent to:
func = decorator1(decorator2(decorator3(func)))
```

---

## CODE — What to Write

### 1. Basic Decorator WITHOUT @ Syntax First

```python
def my_decorator(func):
    """Simple decorator that prints before and after execution"""
    def wrapper(*args, **kwargs):
        print('Before function call')
        result = func(*args, **kwargs)
        print('After function call')
        return result
    return wrapper

# Manual application (no @ syntax)
def greet(name):
    print(f'Hello {name}!')
    return f'Greeted {name}'

greet = my_decorator(greet)
print(greet('Alice'))

# Output:
# Before function call
# Hello Alice!
# After function call
# Greeted Alice
```

### 2. Same Thing With @ Syntax

```python
def my_decorator(func):
    def wrapper(*args, **kwargs):
        print('Before function call')
        result = func(*args, **kwargs)
        print('After function call')
        return result
    return wrapper

@my_decorator
def greet(name):
    print(f'Hello {name}!')
    return f'Greeted {name}'

print(greet('Alice'))

# Output:
# Before function call
# Hello Alice!
# After function call
# Greeted Alice
```

### 3. Timer Decorator — Build This

```python
import time

def timer(func):
    """Decorator that measures function execution time"""
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f'[TIMER] {func.__name__} took {end-start:.4f}s')
        return result
    return wrapper

@timer
def slow_function():
    """Simulates slow operation"""
    time.sleep(1)
    return "Done"

slow_function()
# Output: [TIMER] slow_function took 1.0012s

@timer
def add(a, b):
    """Quick math operation"""
    return a + b

result = add(5, 3)
print(f"Result: {result}")
# Output:
# [TIMER] add took 0.0001s
# Result: 8
```

### 4. Logger Decorator

```python
def logger(func):
    """Decorator that logs function calls with arguments and return value"""
    def wrapper(*args, **kwargs):
        print(f'[LOG] Calling {func.__name__}')
        print(f'[LOG] Arguments: args={args}, kwargs={kwargs}')
        result = func(*args, **kwargs)
        print(f'[LOG] {func.__name__} returned: {result}')
        return result
    return wrapper

@logger
def calculate(x, y, operation='add'):
    if operation == 'add':
        return x + y
    elif operation == 'multiply':
        return x * y

calculate(5, 3)
# Output:
# [LOG] Calling calculate
# [LOG] Arguments: args=(5, 3), kwargs={}
# [LOG] calculate returned: 8

calculate(5, 3, operation='multiply')
# Output:
# [LOG] Calling calculate
# [LOG] Arguments: args=(5, 3), kwargs={'operation': 'multiply'}
# [LOG] calculate returned: 15
```

### 5. Retry Decorator

```python
def retry(max_attempts=3):
    """Decorator that retries function up to max_attempts times on exception"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    attempts += 1
                    print(f'[RETRY] Attempt {attempts}/{max_attempts}')
                    result = func(*args, **kwargs)
                    print(f'[RETRY] Success!')
                    return result
                except Exception as e:
                    print(f'[RETRY] Failed: {e}')
                    if attempts >= max_attempts:
                        print(f'[RETRY] Max attempts ({max_attempts}) reached. Giving up.')
                        raise
        return wrapper
    return decorator

@retry(max_attempts=3)
def unstable_api_call():
    """Simulates an unstable API that fails first 2 times"""
    import random
    if random.random() < 0.7:
        raise ConnectionError("API unavailable")
    return "Success!"

unstable_api_call()
```

### 6. Using functools.wraps (IMPORTANT!)

Without `functools.wraps`, the decorated function loses its metadata:

```python
def bad_decorator(func):
    def wrapper(*args, **kwargs):
        print("Before")
        return func(*args, **kwargs)
    return wrapper

@bad_decorator
def my_func():
    """My docstring"""
    pass

print(my_func.__name__)   # Output: wrapper (WRONG!)
print(my_func.__doc__)    # Output: None (WRONG!)
```

**FIX: Use functools.wraps**

```python
from functools import wraps

def good_decorator(func):
    @wraps(func)  # Preserves metadata
    def wrapper(*args, **kwargs):
        print("Before")
        return func(*args, **kwargs)
    return wrapper

@good_decorator
def my_func():
    """My docstring"""
    pass

print(my_func.__name__)   # Output: my_func (CORRECT!)
print(my_func.__doc__)    # Output: My docstring (CORRECT!)
```

### 7. Stacking Multiple Decorators

```python
import time
from functools import wraps

def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f'⏱️  {func.__name__} took {end-start:.4f}s')
        return result
    return wrapper

def logger(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f'📝 Calling {func.__name__} with args={args}, kwargs={kwargs}')
        result = func(*args, **kwargs)
        print(f'📝 {func.__name__} returned: {result}')
        return result
    return wrapper

def validate_positive(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        for arg in args:
            if isinstance(arg, (int, float)) and arg < 0:
                raise ValueError("Arguments must be positive!")
        return func(*args, **kwargs)
    return wrapper

# Stack all 3 decorators
@timer
@logger
@validate_positive
def square(x):
    """Returns square of x"""
    import time
    time.sleep(0.1)
    return x ** 2

print(square(5))

# Output:
# 📝 Calling square with args=(5,), kwargs={}
# ⏱️  square took 0.1005s
# 📝 square returned: 25
# 25
```

---

## EXERCISES — Hands-on Practice

### Exercise 1: Write a decorator WITHOUT @ syntax first — then convert to @

```python
# TODO: Create a decorator called add_prefix that adds "PREFIX: " to function output
# First: Test it without @ syntax
# Then: Rewrite using @ syntax

# Expected output:
# Without @: "PREFIX: Hello World"
# With @: "PREFIX: Hello World"
```

**Solution:**

```python
def add_prefix(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return f"PREFIX: {result}"
    return wrapper

# Without @ syntax
def greet():
    return "Hello World"

greet = add_prefix(greet)
print(greet())  # PREFIX: Hello World

# With @ syntax
@add_prefix
def greet2():
    return "Hello World"

print(greet2())  # PREFIX: Hello World
```

### Exercise 2: Build a timer decorator that prints function name + time taken

```python
# TODO: Create a timer decorator
# Should print: [TIMER] function_name took X.XXXXs
# Test with: slow_function(1), another_function(0.5)

import time

def timer(func):
    # YOUR CODE HERE
    pass

@timer
def slow_function(duration):
    time.sleep(duration)
    return f"Slept for {duration}s"

@timer
def another_function(duration):
    time.sleep(duration)
    return "Done"

slow_function(1)
another_function(0.5)
```

**Solution:**

```python
import time
from functools import wraps

def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f'[TIMER] {func.__name__} took {end-start:.4f}s')
        return result
    return wrapper
```

### Exercise 3: Build a logger decorator that prints arguments + return value

```python
# TODO: Create a logger decorator
# Should print:
# [LOG] Calling function_name with args=(...), kwargs={...}
# [LOG] function_name returned: ...

def logger(func):
    # YOUR CODE HERE
    pass

@logger
def add(a, b):
    return a + b

@logger
def greet(name, greeting="Hello"):
    return f"{greeting}, {name}!"

add(5, 3)
greet("Alice")
greet("Bob", greeting="Hi")
```

**Solution:**

```python
from functools import wraps

def logger(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f'[LOG] Calling {func.__name__} with args={args}, kwargs={kwargs}')
        result = func(*args, **kwargs)
        print(f'[LOG] {func.__name__} returned: {result}')
        return result
    return wrapper
```

### Exercise 4: Build a retry decorator (retries function up to 3 times on exception)

```python
# TODO: Create a retry decorator with max_attempts parameter
# Should retry on any exception
# Print: [RETRY] Attempt X/3, [RETRY] Success!, [RETRY] Failed: ...

def retry(max_attempts=3):
    # YOUR CODE HERE
    pass

@retry(max_attempts=3)
def flaky_function():
    import random
    if random.random() < 0.7:
        raise ConnectionError("API down")
    return "Success!"

flaky_function()
```

**Solution:**

```python
from functools import wraps

def retry(max_attempts=3):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try:
                    print(f'[RETRY] Attempt {attempt}/{max_attempts}')
                    result = func(*args, **kwargs)
                    print(f'[RETRY] Success!')
                    return result
                except Exception as e:
                    print(f'[RETRY] Failed: {e}')
                    if attempt == max_attempts:
                        print(f'[RETRY] Max attempts reached')
                        raise
        return wrapper
    return decorator
```

### Exercise 5: Stack all 3 decorators on one function and observe output

```python
# TODO: Combine timer, logger, and retry decorators on single function
# Observe execution order (bottom-to-top)

import time
from functools import wraps

# Your decorator definitions here...

@timer
@logger
@retry(max_attempts=2)
def complex_function(x):
    time.sleep(0.1)
    if x < 0:
        raise ValueError("x must be positive")
    return x ** 2

complex_function(5)
```

**Solution - See stacking section above**

---

## REAL-WORLD USE CASES

### Flask Web Framework

```python
from flask import Flask

app = Flask(__name__)

@app.route('/home')
def home():
    return "Welcome home!"

@app.route('/users/<int:user_id>')
def get_user(user_id):
    return f"User {user_id}"

# @app.route is a decorator that registers URL handlers
```

### Django Authentication

```python
from django.contrib.auth.decorators import login_required

@login_required
def protected_view(request):
    return "Only logged-in users can see this"
```

### FastAPI API Endpoints

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}
```

### Pytest Testing

```python
import pytest

@pytest.fixture
def sample_data():
    return [1, 2, 3, 4, 5]

def test_something(sample_data):
    assert len(sample_data) == 5
```

### Celery Async Tasks

```python
from celery import Celery

app = Celery('tasks')

@app.task
def add(x, y):
    return x + y

# Enables async execution
result = add.delay(4, 6)
```

---

## Common Mistakes

### ❌ Mistake 1: Forgetting to return result from wrapper

```python
def bad_decorator(func):
    def wrapper(*args, **kwargs):
        print("Before")
        func(*args, **kwargs)  # MISSING: result =
        # MISSING: return result
    return wrapper

@bad_decorator
def get_value():
    return 42

print(get_value())  # Output: None (WRONG!)
```

**✅ Fix:**

```python
def good_decorator(func):
    def wrapper(*args, **kwargs):
        print("Before")
        result = func(*args, **kwargs)  # Capture result
        return result  # Return it
    return wrapper
```

### ❌ Mistake 2: Not using *args/**kwargs

```python
def bad_decorator(func):
    def wrapper():  # WRONG: No arguments!
        print("Before")
        return func()  # Only works for zero-arg functions
    return wrapper

@bad_decorator
def add(a, b):
    return a + b

add(5, 3)  # TypeError: wrapper() takes 0 positional arguments but 2 were given
```

**✅ Fix:**

```python
def good_decorator(func):
    def wrapper(*args, **kwargs):  # Accepts any arguments
        print("Before")
        return func(*args, **kwargs)  # Pass them through
    return wrapper
```

### ❌ Mistake 3: Thinking decorator runs at call time

```python
def my_decorator(func):
    print("DECORATOR RUNNING")  # When does this print?
    def wrapper():
        print("WRAPPER RUNNING")
        func()
    return wrapper

@my_decorator
def greet():
    print("GREET RUNNING")

# Output so far: "DECORATOR RUNNING"
# (Decorator already ran at definition time!)

greet()
# Output now: "WRAPPER RUNNING" then "GREET RUNNING"
```

### ❌ Mistake 4: Forgetting to return the wrapper function from decorator

```python
def bad_decorator(func):
    def wrapper(*args, **kwargs):
        print("Before")
        return func(*args, **kwargs)
    # MISSING: return wrapper

@bad_decorator
def greet():
    print("Hello")

greet()  # TypeError: 'NoneType' object is not callable
```

**✅ Fix:**

```python
def good_decorator(func):
    def wrapper(*args, **kwargs):
        print("Before")
        return func(*args, **kwargs)
    return wrapper  # Must return the wrapper!
```

---

## Best Practices

### ✅ Practice 1: Always use *args, **kwargs in wrapper

Makes your decorator work with ANY function signature.

```python
from functools import wraps

def my_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):  # Generic signature
        print(f"Calling {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

# Works with any function!
@my_decorator
def no_args():
    pass

@my_decorator
def one_arg(x):
    pass

@my_decorator
def many_args(x, y, z, name="default"):
    pass
```

### ✅ Practice 2: Always return result from wrapper

Otherwise your function returns None.

```python
from functools import wraps

def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        import time
        start = time.time()
        result = func(*args, **kwargs)  # Capture it
        end = time.time()
        print(f"Took {end-start:.4f}s")
        return result  # Return it
    return wrapper
```

### ✅ Practice 3: Always use functools.wraps

Preserves original function's metadata (__name__, __doc__, etc).

```python
from functools import wraps

def my_decorator(func):
    @wraps(func)  # ALWAYS include this!
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@my_decorator
def documented_function():
    """This is my function"""
    pass

print(documented_function.__name__)   # "documented_function" ✅
print(documented_function.__doc__)    # "This is my function" ✅
```

### ✅ Practice 4: Test decorator with multiple function signatures

Test with:
- No arguments
- Positional arguments
- Keyword arguments
- Return values
- Exceptions

```python
from functools import wraps

def my_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}")
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            print(f"Exception: {e}")
            raise
    return wrapper

# Test it thoroughly!
@my_decorator
def func_no_args():
    return "No args"

@my_decorator
def func_with_args(x, y):
    return x + y

@my_decorator
def func_with_kwargs(name, greeting="Hello"):
    return f"{greeting}, {name}"

@my_decorator
def func_with_exception():
    raise ValueError("Intentional error")

# Run tests
print(func_no_args())
print(func_with_args(5, 3))
print(func_with_kwargs("Alice"))
print(func_with_kwargs("Bob", greeting="Hi"))
try:
    func_with_exception()
except ValueError:
    print("Exception caught correctly")
```

---

## INTERVIEW QUESTIONS

### Q1: What is a decorator in Python? Explain without using the word 'decorator'.

**Answer:**
A decorator is a function that takes another function as input, adds extra functionality to it, and returns a modified version. It follows the higher-order function pattern where a function can accept and/or return other functions. The main purpose is to extend or modify behavior without changing the original function's code.

### Q2: What is the difference between @decorator and decorator(func)?

**Answer:**
They are identical in functionality. The `@decorator` syntax is syntactic sugar for `decorator(func)`. Both achieve the same result:

```python
# These two are exactly the same:

@decorator
def func():
    pass

# is equivalent to:
def func():
    pass
func = decorator(func)
```

The `@` syntax is just a cleaner, more Pythonic way to apply decorators at definition time.

**Comparison:**

| Aspect | @decorator | decorator(func) |
|--------|-----------|-----------------|
| **Usage** | At function definition | After function definition |
| **Readability** | Cleaner, more Pythonic | More verbose |
| **Timing** | Decorator at import time | Can be applied conditionally |
| **Multiple** | @dec1 @dec2 def f(): | func = dec1(dec2(func)) |

### Q3: When does a decorator execute — at definition or at call time?

**Answer:**
Decorators execute at **definition time** (when the function is defined), NOT at call time (when the function is called).

```python
def my_decorator(func):
    print("🔴 DECORATOR EXECUTING (definition time)")
    def wrapper():
        print("🟢 WRAPPER EXECUTING (call time)")
        func()
    return wrapper

print("BEFORE DEFINITION")
@my_decorator
def greet():
    print("GREET EXECUTING")
print("AFTER DEFINITION")

print("\nNOW CALLING:")
greet()

# Output:
# BEFORE DEFINITION
# 🔴 DECORATOR EXECUTING (definition time)
# AFTER DEFINITION
# 
# NOW CALLING:
# 🟢 WRAPPER EXECUTING (call time)
# GREET EXECUTING
```

### Q4: Why do we use *args and **kwargs inside the wrapper function?

**Answer:**
`*args` and `**kwargs` make the decorator generic so it works with ANY function signature:

- `*args` captures positional arguments as a tuple
- `**kwargs` captures keyword arguments as a dictionary

Without them, the decorator only works with functions matching the wrapper's signature.

```python
# ❌ BAD: Only works for functions with exactly 2 arguments
def bad_decorator(func):
    def wrapper(a, b):
        return func(a, b)
    return wrapper

# ✅ GOOD: Works with any number of arguments
def good_decorator(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

# With good_decorator, we can use:
@good_decorator
def add(a, b):
    return a + b

@good_decorator
def greet(name, greeting="Hello"):
    return f"{greeting}, {name}"

@good_decorator
def multiply(a, b, c):
    return a * b * c
```

### Q5: What happens if you forget to return result from wrapper?

**Answer:**
The decorated function returns `None` instead of its actual return value.

```python
# ❌ WRONG: Missing return
def bad_decorator(func):
    def wrapper(*args, **kwargs):
        print("Before")
        func(*args, **kwargs)  # Not capturing or returning
    return wrapper

@bad_decorator
def add(a, b):
    return a + b

result = add(5, 3)
print(result)  # Output: None (WRONG! Should be 8)

# ✅ CORRECT: Capture and return
def good_decorator(func):
    def wrapper(*args, **kwargs):
        print("Before")
        result = func(*args, **kwargs)  # Capture
        return result  # Return
    return wrapper

@good_decorator
def add(a, b):
    return a + b

result = add(5, 3)
print(result)  # Output: 8 (CORRECT!)
```

### Q6: What does functools.wraps do and why is it important?

**Answer:**
`functools.wraps` preserves the original function's metadata (__name__, __doc__, __module__, etc.) when creating a wrapper function. Without it, the decorated function's name and docstring are lost.

```python
# ❌ WITHOUT functools.wraps
def bad_decorator(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@bad_decorator
def my_function():
    """My docstring"""
    pass

print(my_function.__name__)   # Output: "wrapper" (WRONG!)
print(my_function.__doc__)    # Output: None (WRONG!)

# ✅ WITH functools.wraps
from functools import wraps

def good_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@good_decorator
def my_function():
    """My docstring"""
    pass

print(my_function.__name__)   # Output: "my_function" (CORRECT!)
print(my_function.__doc__)    # Output: "My docstring" (CORRECT!)
```

### Q7: How does stacking multiple decorators work? What is the execution order?

**Answer:**
When multiple decorators are stacked, they are applied from **bottom to top** (inside-out). The innermost decorator is applied first.

```python
@decorator1
@decorator2
@decorator3
def func():
    pass

# Is equivalent to:
func = decorator1(decorator2(decorator3(func)))

# Execution order:
# 1. decorator3 is applied to func
# 2. decorator2 is applied to the result
# 3. decorator1 is applied to the result
# 4. When func() is called, decorators execute INSIDE-OUT
```

**Example:**

```python
def logger(func):
    print("LOGGER decorator applied")
    def wrapper(*args, **kwargs):
        print("→ LOGGER wrapper")
        return func(*args, **kwargs)
    return wrapper

def timer(func):
    print("TIMER decorator applied")
    def wrapper(*args, **kwargs):
        print("→ TIMER wrapper")
        return func(*args, **kwargs)
    return wrapper

print("=== DEFINITION ===")
@logger
@timer
def greet():
    print("→ GREET function")

print("\n=== CALLING ===")
greet()

# Output:
# === DEFINITION ===
# TIMER decorator applied
# LOGGER decorator applied
# 
# === CALLING ===
# → LOGGER wrapper
# → TIMER wrapper
# → GREET function
```

### Q8: Can decorators take arguments? Give an example.

**Answer:**
Yes! To make a decorator take arguments, wrap it in another function. This creates a decorator factory.

```python
def repeat(times):
    """Decorator factory that takes arguments"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            results = []
            for _ in range(times):
                results.append(func(*args, **kwargs))
            return results
        return wrapper
    return decorator

@repeat(times=3)
def greet(name):
    return f"Hello {name}!"

print(greet("Alice"))
# Output: ['Hello Alice!', 'Hello Alice!', 'Hello Alice!']
```

### Q9: What is the difference between decorating a function vs a class?

**Answer:**
Function decorators wrap function behavior. Class decorators wrap class behavior.

```python
# Function decorator
def uppercase(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return result.upper() if isinstance(result, str) else result
    return wrapper

@uppercase
def greet():
    return "hello"

print(greet())  # "HELLO"

# Class decorator
def add_method(cls):
    def new_method(self):
        return "Added by decorator"
    cls.new_method = new_method
    return cls

@add_method
class MyClass:
    pass

obj = MyClass()
print(obj.new_method())  # "Added by decorator"
```

---

## GITHUB TASK

### Setup Repository

```bash
# Create repository
mkdir python-advanced-learning
cd python-advanced-learning

# Initialize git
git init
git config user.name "Your Name"
git config user.email "your.email@example.com"

# Create week1 directory
mkdir -p week1/notes

# Create day1_decorators.py file
touch week1/day1_decorators.py
```

### File: week1/day1_decorators.py

```python
"""
DAY 1: Python Decorators Basics
- Timer decorator
- Logger decorator
- Retry decorator
"""

import time
from functools import wraps

# ==================== DECORATORS ====================

def timer(func):
    """Measures function execution time"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f'⏱️  {func.__name__} took {end-start:.4f}s')
        return result
    return wrapper


def logger(func):
    """Logs function calls with arguments and return value"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f'📝 Calling {func.__name__}')
        print(f'   args={args}, kwargs={kwargs}')
        result = func(*args, **kwargs)
        print(f'   returned: {result}')
        return result
    return wrapper


def retry(max_attempts=3):
    """Retries function on exception up to max_attempts times"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try:
                    print(f'🔄 Attempt {attempt}/{max_attempts}')
                    result = func(*args, **kwargs)
                    print(f'✅ Success!')
                    return result
                except Exception as e:
                    print(f'❌ Failed: {e}')
                    if attempt >= max_attempts:
                        print(f'🛑 Max attempts ({max_attempts}) reached')
                        raise
        return wrapper
    return decorator


# ==================== TESTS ====================

@timer
def test_timer():
    """Test timer decorator"""
    time.sleep(0.5)
    return "Timer test done"


@logger
def test_logger(a, b, operation="add"):
    """Test logger decorator"""
    if operation == "add":
        return a + b
    elif operation == "multiply":
        return a * b


@retry(max_attempts=3)
def test_retry_success():
    """Test retry decorator - succeeds immediately"""
    return "Retry test passed"


call_count = 0

@retry(max_attempts=3)
def test_retry_fail():
    """Test retry decorator - fails then succeeds"""
    global call_count
    call_count += 1
    if call_count < 2:
        raise ConnectionError("Simulated failure")
    return "Retry eventually succeeded"


@timer
@logger
@retry(max_attempts=2)
def test_stacked_decorators(x):
    """Test all decorators stacked together"""
    time.sleep(0.1)
    if x < 0:
        raise ValueError("x must be positive")
    return x ** 2


# ==================== RUN TESTS ====================

if __name__ == "__main__":
    print("=" * 60)
    print("TEST 1: Timer Decorator")
    print("=" * 60)
    result = test_timer()
    print(f"Result: {result}\n")

    print("=" * 60)
    print("TEST 2: Logger Decorator")
    print("=" * 60)
    result = test_logger(5, 3)
    print(f"Result: {result}\n")
    
    result = test_logger(5, 3, operation="multiply")
    print(f"Result: {result}\n")

    print("=" * 60)
    print("TEST 3: Retry Decorator - Success")
    print("=" * 60)
    result = test_retry_success()
    print(f"Result: {result}\n")

    print("=" * 60)
    print("TEST 4: Retry Decorator - Fail Then Succeed")
    print("=" * 60)
    call_count = 0
    result = test_retry_fail()
    print(f"Result: {result}\n")

    print("=" * 60)
    print("TEST 5: Stacked Decorators")
    print("=" * 60)
    result = test_stacked_decorators(5)
    print(f"Result: {result}\n")

    print("=" * 60)
    print("All tests completed successfully! ✅")
    print("=" * 60)
```

### Git Commit

```bash
# Stage all files
git add .

# Create initial commit
git commit -m "Day 1: Python Decorators - Timer, Logger, Retry decorators with tests"

# View commit history
git log --oneline
```

---

## TODAY'S DELIVERABLES

✅ **File created:** week1/day1_decorators.py
- Timer decorator working with multiple function types
- Logger decorator capturing arguments and return values
- Retry decorator with configurable attempts
- All decorated functions tested

✅ **3 decorators working:**
- `@timer` - measures execution time
- `@logger` - logs calls and returns
- `@retry(max_attempts=3)` - retries on exception

✅ **All decorators tested with different function types:**
- No-argument functions
- Functions with positional arguments
- Functions with keyword arguments
- Functions that raise exceptions
- Stacked decorators

✅ **Pushed to GitHub with descriptive commit message:**
```
git commit -m "Day 1: Python Decorators - Timer, Logger, Retry decorators with tests"
```

✅ **Notes file created:** notes/week1/decorators_basics.md
- Complete explanation of what, why, and how
- Code examples for each concept
- @decorator vs decorator(func) comparison table
- Real-world use cases
- Common mistakes and best practices
- Interview questions and answers

---

## SUMMARY

**Key Concepts Learned:**
1. Decorators wrap functions to extend behavior without modifying source
2. Built on higher-order function pattern
3. Execute at definition time, not call time
4. @ syntax is syntactic sugar for function reassignment
5. Must use *args, **kwargs, return result, and functools.wraps
6. Can be stacked for multiple transformations
7. Used everywhere in modern Python frameworks

**Code Written:**
- 3 fully functional decorators (timer, logger, retry)
- Comprehensive test suite
- Production-ready with proper error handling

**Next Steps:** Understanding decorator internals will prepare you for learning class decorators, decorator factories, and decorators with arguments.


---

# Python Decorators Basics

## What are Decorators?

Decorators are functions that modify or enhance other functions or classes without permanently changing their source code. They "wrap" a function with another function to extend its behavior.

## Why Use Decorators?

- **Code Reusability**: Apply the same logic to multiple functions
- **Separation of Concerns**: Keep business logic separate from cross-cutting concerns
- **Clean Code**: Reduce code duplication and improve readability
- **Metadata Management**: Add functionality like logging, timing, validation, authentication
- **Aspect-Oriented Programming**: Handle concerns like caching, rate limiting, error handling

## How Decorators Work

Decorators are based on Python's higher-order functions (functions that take or return other functions).

### Basic Concept

```python
def my_decorator(func):
    def wrapper():
        print("Something before the function")
        func()
        print("Something after the function")
    return wrapper

@my_decorator
def say_hello():
    print("Hello!")

# Equivalent to: say_hello = my_decorator(say_hello)

say_hello()
```

Output:
```
Something before the function
Hello!
Something after the function
```

## Examples

### Example 1: Timing Decorator

```python
import time

def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end - start:.4f} seconds")
        return result
    return wrapper

@timer
def slow_function():
    time.sleep(1)
    return "Done"

slow_function()
```

### Example 2: Logging Decorator

```python
def log_calls(func):
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__} with args={args}, kwargs={kwargs}")
        result = func(*args, **kwargs)
        print(f"{func.__name__} returned {result}")
        return result
    return wrapper

@log_calls
def add(a, b):
    return a + b

add(3, 5)
```

Output:
```
Calling add with args=(3, 5), kwargs={}
add returned 8
```

### Example 3: Validation Decorator

```python
def validate_positive(func):
    def wrapper(*args, **kwargs):
        for arg in args:
            if isinstance(arg, (int, float)) and arg < 0:
                raise ValueError("Arguments must be positive")
        return func(*args, **kwargs)
    return wrapper

@validate_positive
def square(x):
    return x ** 2

print(square(5))      # 25
print(square(-5))     # ValueError: Arguments must be positive
```

### Example 4: Caching/Memoization Decorator

```python
def memoize(func):
    cache = {}
    def wrapper(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]
    return wrapper

@memoize
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

print(fibonacci(10))  # Computed with caching
```

### Example 5: Stacking Multiple Decorators

```python
def uppercase(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return result.upper()
    return wrapper

def add_prefix(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return f"PREFIX: {result}"
    return wrapper

@uppercase
@add_prefix
def greet(name):
    return f"hello {name}"

print(greet("Alice"))  # PREFIX: HELLO ALICE
```

Note: Decorators are applied bottom-to-top (right-to-left)

## Preserving Function Metadata

Without `functools.wraps`, the decorated function loses its original metadata:

```python
from functools import wraps

def my_decorator(func):
    @wraps(func)  # Preserves __name__, __doc__, etc.
    def wrapper(*args, **kwargs):
        """Wrapper docstring"""
        return func(*args, **kwargs)
    return wrapper

@my_decorator
def my_function():
    """Original docstring"""
    pass

print(my_function.__name__)   # my_function (not wrapper)
print(my_function.__doc__)    # Original docstring
```

## @decorator vs decorator(func) Comparison

| Feature | @decorator Syntax | decorator(func) Syntax |
|---------|------------------|----------------------|
| **Usage** | `@my_decorator` above function definition | `func = my_decorator(func)` |
| **Readability** | More clean and Pythonic | More verbose |
| **Placement** | Above function/class | Below or separate line |
| **Application** | Applied at definition time | Applied at any time |
| **Multiple Decorators** | Stack multiple easily with multiple `@` | Requires nested calls |
| **Dynamic Application** | Not ideal for conditional decoration | Better for conditional/dynamic use |
| **Example** | `@timer def foo(): pass` | `foo = timer(foo)` |
| **Multiple Example** | `@timer` `@log_calls` `def foo(): pass` | `foo = log_calls(timer(foo))` |
| **When to Use** | 95% of cases - standard practice | Only when decorating dynamically |
| **Performance** | Same | Same |

### Syntax Examples

```python
# @decorator Syntax (Recommended)
@timer
@log_calls
def process_data(x):
    return x * 2

# Equivalent to:
def process_data(x):
    return x * 2
process_data = timer(log_calls(process_data))
```

```python
# decorator(func) Syntax
def process_data(x):
    return x * 2

process_data = log_calls(process_data)
process_data = timer(process_data)
```

## Decorators with Arguments

```python
def repeat(times):
    def decorator(func):
        def wrapper(*args, **kwargs):
            results = []
            for _ in range(times):
                results.append(func(*args, **kwargs))
            return results
        return wrapper
    return decorator

@repeat(times=3)
def greet(name):
    return f"Hello {name}"

print(greet("Bob"))  # ['Hello Bob', 'Hello Bob', 'Hello Bob']
```

## Class Decorators

```python
def add_method(cls):
    def new_method(self):
        return "Added by decorator"
    cls.new_method = new_method
    return cls

@add_method
class MyClass:
    pass

obj = MyClass()
print(obj.new_method())  # Added by decorator
```

## Built-in Decorators

Python provides some built-in decorators:

```python
class Example:
    @property
    def value(self):
        return self._value
    
    @staticmethod
    def static_method():
        return "Static"
    
    @classmethod
    def class_method(cls):
        return f"Called on {cls.__name__}"
```

## Key Takeaways

✓ Decorators modify function behavior without changing source code  
✓ They are implemented using higher-order functions  
✓ Use `@decorator` syntax for clarity and Pythonic code  
✓ Always use `functools.wraps` to preserve metadata  
✓ Stack decorators to apply multiple modifications  
✓ Common use cases: logging, timing, validation, caching, authentication

---

# QUICK REFERENCE — Python Decorators
**Day 1 Summary | Cheat Sheet | Key Concepts**

---

## WHAT IS A DECORATOR?

A function that wraps another function to extend or modify its behavior without changing the original code.

```python
def my_decorator(func):
    def wrapper(*args, **kwargs):
        print("Before")
        result = func(*args, **kwargs)
        print("After")
        return result
    return wrapper

@my_decorator
def greet():
    print("Hello!")
```

---

## BASIC STRUCTURE

```
Decorator
├── Takes a function as argument: func
│
├── Defines wrapper function
│   ├── Accepts *args, **kwargs
│   ├── Calls original function: func(*args, **kwargs)
│   ├── Optionally modifies behavior
│   └── Returns the result
│
└── Returns wrapper function
```

---

## SYNTAX COMPARISON

| Feature | @decorator | decorator(func) |
|---------|-----------|-----------------|
| **Syntax** | `@my_decorator` | `func = my_decorator(func)` |
| **Placement** | Above function | Below function |
| **Readability** | Clean, Pythonic | Verbose |
| **Timing** | At definition | Any time |
| **Usage** | 99% of cases | Dynamic decoration |

---

## KEY RULES

### Rule 1: Always use *args, **kwargs

```python
# ❌ WRONG: Limited to specific signature
def bad(func):
    def wrapper(a, b):
        return func(a, b)
    return wrapper

# ✅ CORRECT: Works with any signature
def good(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper
```

### Rule 2: Always return the result

```python
# ❌ WRONG: Returns None
def bad(func):
    def wrapper(*args, **kwargs):
        func(*args, **kwargs)
    return wrapper

# ✅ CORRECT: Returns actual result
def good(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return result
    return wrapper
```

### Rule 3: Always use functools.wraps

```python
# ❌ WRONG: Loses metadata
def bad(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

# ✅ CORRECT: Preserves metadata
from functools import wraps

def good(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper
```

---

## EXECUTION TIMING

```python
def my_decorator(func):
    print("DECORATOR RUNS HERE")  # Runs at definition time
    
    def wrapper():
        print("WRAPPER RUNS HERE")  # Runs at call time
        func()
    
    return wrapper

@my_decorator  # ← DECORATOR RUNS HERE
def greet():
    print("GREET RUNS HERE")

greet()  # ← WRAPPER & GREET RUN HERE
```

**Output:**
```
DECORATOR RUNS HERE
WRAPPER RUNS HERE
GREET RUNS HERE
```

---

## DECORATOR PATTERNS

### Pattern 1: Simple Decorator (No Arguments)

```python
from functools import wraps

def my_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Before
        result = func(*args, **kwargs)
        # After
        return result
    return wrapper

@my_decorator
def my_func():
    pass
```

### Pattern 2: Decorator with Arguments

```python
from functools import wraps

def my_decorator(arg1, arg2):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Use arg1, arg2
            result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

@my_decorator(arg1=10, arg2=20)
def my_func():
    pass
```

### Pattern 3: Stacked Decorators

```python
@decorator1
@decorator2
@decorator3
def func():
    pass

# Equivalent to:
func = decorator1(decorator2(decorator3(func)))

# Execution order: decorator3 → decorator2 → decorator1
```

### Pattern 4: Class Decorator

```python
def my_decorator(cls):
    # Modify class
    cls.new_method = lambda self: "Added by decorator"
    return cls

@my_decorator
class MyClass:
    pass
```

---

## COMMON DECORATORS

### Timer Decorator

```python
import time
from functools import wraps

def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f'{func.__name__} took {end-start:.4f}s')
        return result
    return wrapper
```

### Logger Decorator

```python
from functools import wraps

def logger(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f'Calling {func.__name__} with args={args}, kwargs={kwargs}')
        result = func(*args, **kwargs)
        print(f'{func.__name__} returned {result}')
        return result
    return wrapper
```

### Retry Decorator

```python
from functools import wraps

def retry(max_attempts=3):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt >= max_attempts:
                        raise
        return wrapper
    return decorator
```

### Caching/Memoization Decorator

```python
from functools import wraps

def cache(func):
    cached = {}
    
    @wraps(func)
    def wrapper(*args):
        if args not in cached:
            cached[args] = func(*args)
        return cached[args]
    
    return wrapper
```

---

## COMMON MISTAKES

| Mistake | Problem | Fix |
|---------|---------|-----|
| Forget to return result | Function returns None | `return func(*args, **kwargs)` |
| No *args/**kwargs | Only works with specific signature | `def wrapper(*args, **kwargs)` |
| Forget functools.wraps | Lose function metadata | `@wraps(func)` |
| Forget return wrapper | Decorator doesn't work | `return wrapper` |
| Think decorator runs at call time | Initialization at wrong time | Understand it runs at definition |
| Don't capture result | Can't modify/return value | `result = func(*args, **kwargs)` |

---

## INTERVIEW CHECKLIST

- [ ] Can explain what a decorator is
- [ ] Understand @ is syntactic sugar
- [ ] Know decorators run at definition time
- [ ] Can implement timer decorator
- [ ] Can implement logger decorator
- [ ] Can implement retry decorator
- [ ] Understand *args/**kwargs necessity
- [ ] Know functools.wraps importance
- [ ] Can stack decorators
- [ ] Know when to use decorator(func) syntax

---

## FRAMEWORK USAGE

### Flask

```python
from flask import Flask
app = Flask(__name__)

@app.route('/home')
def home():
    return "Home"

@app.route('/user/<int:id>')
def get_user(id):
    return f"User {id}"
```

### Django

```python
from django.contrib.auth.decorators import login_required

@login_required
def protected_view(request):
    return HttpResponse("Only for logged-in users")
```

### FastAPI

```python
from fastapi import FastAPI
app = FastAPI()

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}
```

### pytest

```python
import pytest

@pytest.fixture
def sample_data():
    return [1, 2, 3, 4, 5]

def test_len(sample_data):
    assert len(sample_data) == 5
```

---

## REAL-WORLD EXAMPLES

### Authentication Decorator

```python
def require_auth(func):
    @wraps(func)
    def wrapper(*args, request, **kwargs):
        if not request.user.is_authenticated:
            raise PermissionError("Not authenticated")
        return func(*args, request, **kwargs)
    return wrapper

@require_auth
def get_user_profile(request):
    return request.user.profile
```

### Rate Limiting Decorator

```python
import time

def rate_limit(calls=10, period=60):
    def decorator(func):
        last_called = [0.0]
        calls_made = [0]
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            now = time.time()
            if now - last_called[0] > period:
                calls_made[0] = 0
                last_called[0] = now
            
            if calls_made[0] >= calls:
                raise Exception(f"Rate limit exceeded: {calls}/{period}s")
            
            calls_made[0] += 1
            return func(*args, **kwargs)
        
        return wrapper
    return decorator

@rate_limit(calls=10, period=60)
def api_call():
    return requests.get("https://api.example.com")
```

### Validation Decorator

```python
def validate(**types):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for name, expected_type in types.items():
                if name in kwargs and not isinstance(kwargs[name], expected_type):
                    raise TypeError(f"{name} must be {expected_type}")
            return func(*args, **kwargs)
        return wrapper
    return decorator

@validate(name=str, age=int)
def create_user(name, age):
    return f"{name} is {age}"
```

---

## HOW TO DEBUG DECORATORS

```python
# Add print statements to see execution order
def debug_decorator(func):
    print(f"1. Decorator called for {func.__name__}")
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"2. Wrapper called with args={args}, kwargs={kwargs}")
        result = func(*args, **kwargs)
        print(f"3. Result: {result}")
        return result
    
    print(f"4. Returning wrapper for {func.__name__}")
    return wrapper

@debug_decorator
def my_func(x):
    print(f"5. Inside my_func with x={x}")
    return x * 2

my_func(5)
```

**Output shows execution order clearly**

---

## TESTING DECORATORS

```python
def test_decorator():
    @my_decorator
    def add(a, b):
        return a + b
    
    # Test with different signatures
    assert add(5, 3) == 8  # Basic
    
    @my_decorator
    def no_args():
        return "test"
    
    assert no_args() == "test"
    
    @my_decorator
    def with_kwargs(a, b=10):
        return a + b
    
    assert with_kwargs(5) == 15
    assert with_kwargs(5, b=20) == 25
```

---

## KEY CONCEPTS TO REMEMBER

1. **Higher-order functions:** Functions that take/return functions
2. **Definition time:** Decorators execute when function is defined
3. **Call time:** Wrapper function executes when decorated function is called
4. **Generic signature:** *args/**kwargs makes decorator work with any function
5. **Metadata preservation:** functools.wraps keeps original function info
6. **Bottom-to-top:** Stacked decorators applied from innermost to outermost
7. **Inside-out execution:** Decorators execute from outermost to innermost

---

## QUICK PROBLEMS & SOLUTIONS

**Problem: Decorator works but function name is wrong**
```python
# Solution: Add @wraps(func)
from functools import wraps

@wraps(func)
def wrapper(*args, **kwargs):
    return func(*args, **kwargs)
```

**Problem: Decorator only works with specific argument types**
```python
# Solution: Use *args, **kwargs
def wrapper(*args, **kwargs):  # Instead of wrapper(a, b, c)
    return func(*args, **kwargs)
```

**Problem: Decorated function returns None**
```python
# Solution: Return the result
result = func(*args, **kwargs)
return result  # Don't forget!
```

**Problem: Multiple decorators not working**
```python
# Solution: Check execution order (bottom-to-top at definition)
@outer
@middle
@inner
def func():
    pass
# Equivalent to: outer(middle(inner(func)))
```

---

## TODAY'S GOALS CHECKLIST

- [ ] Understand what decorators are
- [ ] Know when they execute (definition time)
- [ ] Can write basic decorators
- [ ] Always use *args/**kwargs
- [ ] Always return result
- [ ] Always use functools.wraps
- [ ] Can implement timer, logger, retry decorators
- [ ] Can stack decorators
- [ ] Know decorator(func) vs @decorator
- [ ] Understand real-world framework usage

---

## NEXT STEPS

1. **Practice:** Write decorators from scratch
2. **Test:** Test with different function signatures
3. **Read:** Study Flask/Django decorator usage
4. **Build:** Add decorators to your projects
5. **Interview:** Practice explaining decorators

---

**Congratulations! You've mastered Python Decorators! 🎉**

Now move on to:
- Day 2: Advanced Decorators (with arguments, async, composition)
- Day 3: Metaclasses (class decorators)
- Week 2: Understanding Frameworks (how Flask/Django use decorators)


---

# EXERCISES — Day 1 Python Decorators
**Hands-on Practice | 3-4 hours**

---

## Exercise 1: Write a decorator WITHOUT @ syntax first — then convert to @

### Task

Create a decorator called `add_prefix` that adds "PREFIX: " to the beginning of any function's output.

**Constraints:**
- First implement WITHOUT @ syntax (manual application)
- Then rewrite using @ syntax
- Test with multiple functions
- Ensure return value is preserved

### Starter Code

```python
# TODO: Create the add_prefix decorator

def add_prefix(func):
    # YOUR CODE HERE
    pass

# Test WITHOUT @ syntax
def greet():
    return "Hello World"

# YOUR CODE: greet = add_prefix(greet)
# YOUR CODE: print(greet())  # Should print: PREFIX: Hello World

# Test WITH @ syntax
@add_prefix
def greet_v2():
    return "Hello World"

# YOUR CODE: print(greet_v2())  # Should print: PREFIX: Hello World
```

### Expected Output

```
PREFIX: Hello World
PREFIX: Hello World
```

### Solution

```python
from functools import wraps

def add_prefix(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return f"PREFIX: {result}"
    return wrapper

# Without @ syntax
def greet():
    return "Hello World"

greet = add_prefix(greet)
print(greet())  # PREFIX: Hello World

# With @ syntax
@add_prefix
def greet_v2():
    return "Hello World"

print(greet_v2())  # PREFIX: Hello World

# Bonus: Test with arguments
@add_prefix
def greet_person(name):
    return f"Hello {name}"

print(greet_person("Alice"))  # PREFIX: Hello Alice
```

---

## Exercise 2: Build a timer decorator that prints function name + time taken

### Task

Create a `timer` decorator that:
- Measures how long a function takes to execute
- Prints: `[TIMER] function_name took X.XXXXs`
- Works with functions that take arguments
- Returns the original result

**Constraints:**
- Must use `time.time()` for measurement
- Must print function.__name__
- Must preserve the return value
- Must use *args, **kwargs
- Use functools.wraps

### Starter Code

```python
import time
from functools import wraps

def timer(func):
    # YOUR CODE HERE
    pass

@timer
def slow_function(duration):
    """Simulates slow operation"""
    time.sleep(duration)
    return f"Slept for {duration}s"

@timer
def quick_function():
    """Quick operation"""
    return "Done"

@timer
def add(a, b):
    """Addition operation"""
    return a + b

# Test the decorator
result = slow_function(1)
print(f"Return value: {result}\n")

result = quick_function()
print(f"Return value: {result}\n")

result = add(5, 3)
print(f"Return value: {result}\n")
```

### Expected Output

```
[TIMER] slow_function took 1.0XXXs
Return value: Slept for 1s

[TIMER] quick_function took 0.0XXXs
Return value: Done

[TIMER] add took 0.0XXXs
Return value: 8
```

### Solution

```python
import time
from functools import wraps

def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        elapsed = end - start
        print(f'[TIMER] {func.__name__} took {elapsed:.4f}s')
        return result
    return wrapper
```

---

## Exercise 3: Build a logger decorator that prints arguments + return value

### Task

Create a `logger` decorator that:
- Prints when function is called (with arguments)
- Prints the return value
- Works with positional and keyword arguments
- Format: `[LOG] Calling function_name with args=(...), kwargs={...}`
- Format: `[LOG] function_name returned: ...`

**Constraints:**
- Must capture both args and kwargs
- Must preserve return value
- Must print before and after execution
- Use functools.wraps

### Starter Code

```python
from functools import wraps

def logger(func):
    # YOUR CODE HERE
    pass

@logger
def add(a, b):
    """Add two numbers"""
    return a + b

@logger
def greet(name, greeting="Hello"):
    """Greet someone"""
    return f"{greeting}, {name}!"

@logger
def process(x, y, z):
    """Process three values"""
    return x + y + z

# Test the decorator
print("Test 1: add(5, 3)")
result = add(5, 3)
print(f"Got: {result}\n")

print("Test 2: greet('Alice')")
result = greet("Alice")
print(f"Got: {result}\n")

print("Test 3: greet('Bob', greeting='Hi')")
result = greet("Bob", greeting="Hi")
print(f"Got: {result}\n")

print("Test 4: process(1, 2, 3)")
result = process(1, 2, 3)
print(f"Got: {result}\n")
```

### Expected Output

```
Test 1: add(5, 3)
[LOG] Calling add with args=(5, 3), kwargs={}
[LOG] add returned: 8
Got: 8

Test 2: greet('Alice')
[LOG] Calling greet with args=('Alice',), kwargs={}
[LOG] greet returned: Hello, Alice!
Got: Hello, Alice!

Test 3: greet('Bob', greeting='Hi')
[LOG] Calling greet with args=('Bob',), kwargs={'greeting': 'Hi'}
[LOG] greet returned: Hi, Bob!
Got: Hi, Bob!

Test 4: process(1, 2, 3)
[LOG] Calling process with args=(1, 2, 3), kwargs={}
[LOG] process returned: 6
Got: 6
```

### Solution

```python
from functools import wraps

def logger(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f'[LOG] Calling {func.__name__} with args={args}, kwargs={kwargs}')
        result = func(*args, **kwargs)
        print(f'[LOG] {func.__name__} returned: {result}')
        return result
    return wrapper
```

---

## Exercise 4: Build a retry decorator (retries function up to 3 times on exception)

### Task

Create a `retry` decorator that:
- Takes a `max_attempts` parameter (default=3)
- Retries the function if it raises an exception
- Prints attempt number on each try
- Prints "Success!" when it finally succeeds
- Prints "Max attempts reached" when giving up
- Re-raises the exception if all attempts fail

**Constraints:**
- Must be a decorator factory (takes arguments)
- Must handle any exception type
- Must be used as `@retry(max_attempts=3)`
- Use functools.wraps
- Print attempt count: `[RETRY] Attempt X/3`

### Starter Code

```python
from functools import wraps

def retry(max_attempts=3):
    # YOUR CODE HERE
    pass

# Test 1: Function that succeeds immediately
@retry(max_attempts=3)
def successful_function():
    """Succeeds on first try"""
    return "Success!"

# Test 2: Function that fails then succeeds
call_count = 0

@retry(max_attempts=3)
def flaky_function():
    """Fails first time, succeeds second time"""
    global call_count
    call_count += 1
    if call_count == 1:
        raise ConnectionError("API unavailable")
    return "Connected!"

# Test 3: Function that always fails
@retry(max_attempts=3)
def always_fails():
    """Always raises an exception"""
    raise ValueError("This always fails")

# Test the decorators
print("=" * 50)
print("Test 1: Function that succeeds immediately")
print("=" * 50)
result = successful_function()
print(f"Result: {result}\n")

print("=" * 50)
print("Test 2: Function that fails then succeeds")
print("=" * 50)
call_count = 0
result = flaky_function()
print(f"Result: {result}\n")

print("=" * 50)
print("Test 3: Function that always fails")
print("=" * 50)
try:
    result = always_fails()
except ValueError as e:
    print(f"Exception raised after max attempts: {e}\n")
```

### Expected Output

```
==================================================
Test 1: Function that succeeds immediately
==================================================
[RETRY] Attempt 1/3
[RETRY] Success!
Result: Success!

==================================================
Test 2: Function that fails then succeeds
==================================================
[RETRY] Attempt 1/3
[RETRY] Failed: API unavailable
[RETRY] Attempt 2/3
[RETRY] Success!
Result: Connected!

==================================================
Test 3: Function that always fails
==================================================
[RETRY] Attempt 1/3
[RETRY] Failed: This always fails
[RETRY] Attempt 2/3
[RETRY] Failed: This always fails
[RETRY] Attempt 3/3
[RETRY] Failed: This always fails
[RETRY] Max attempts reached
Exception raised after max attempts: This always fails
```

### Solution

```python
from functools import wraps

def retry(max_attempts=3):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            
            for attempt in range(1, max_attempts + 1):
                try:
                    print(f'[RETRY] Attempt {attempt}/{max_attempts}')
                    result = func(*args, **kwargs)
                    print(f'[RETRY] Success!')
                    return result
                except Exception as e:
                    last_exception = e
                    print(f'[RETRY] Failed: {e}')
                    
                    if attempt >= max_attempts:
                        print(f'[RETRY] Max attempts reached')
            
            raise last_exception
        return wrapper
    return decorator
```

---

## Exercise 5: Stack all 3 decorators on one function and observe output

### Task

Create a function decorated with all three decorators (timer, logger, retry) and observe:
1. The order in which decorators are applied (bottom-to-top)
2. The order in which wrappers execute (inside-out)
3. How exceptions flow through the decorator stack

**Constraints:**
- Use all three decorators: @timer, @logger, @retry
- Function should succeed on first try
- Function should sleep for 0.2 seconds
- Create a version that fails, then succeeds

### Starter Code

```python
import time
from functools import wraps

# Your decorator definitions here...

def timer(func):
    # YOUR CODE
    pass

def logger(func):
    # YOUR CODE
    pass

def retry(max_attempts=3):
    # YOUR CODE
    pass

print("=" * 60)
print("DEFINING FUNCTION WITH STACKED DECORATORS")
print("=" * 60)

@timer
@logger
@retry(max_attempts=2)
def stacked_success(x):
    """Function that succeeds on first try"""
    time.sleep(0.2)
    if x < 0:
        raise ValueError("x must be positive")
    return x ** 2

print("\n" + "=" * 60)
print("CALLING STACKED DECORATORS - SUCCESS CASE")
print("=" * 60)
result = stacked_success(5)
print(f"Final result: {result}\n")

# Bonus: Try with exception
attempt_count = 0

@timer
@logger
@retry(max_attempts=2)
def stacked_with_retry(x):
    """Function that fails first time, succeeds second"""
    global attempt_count
    attempt_count += 1
    time.sleep(0.1)
    
    if attempt_count == 1:
        raise ConnectionError("Simulated failure")
    
    return x * 2

print("=" * 60)
print("CALLING STACKED DECORATORS - RETRY CASE")
print("=" * 60)
attempt_count = 0
result = stacked_with_retry(10)
print(f"Final result: {result}\n")
```

### Expected Output

```
============================================================
DEFINING FUNCTION WITH STACKED DECORATORS
============================================================
[RETRY] decorator applied
[LOG] decorator applied
[TIMER] decorator applied

============================================================
CALLING STACKED DECORATORS - SUCCESS CASE
============================================================
[RETRY] Attempt 1/2
[LOG] Calling stacked_success with args=(5,), kwargs={}
[TIMER] Starting timer for stacked_success
[TIMER] stacked_success took 0.2005s
[LOG] stacked_success returned: 25
[RETRY] Success!
Final result: 25

============================================================
CALLING STACKED DECORATORS - RETRY CASE
============================================================
[RETRY] Attempt 1/2
[LOG] Calling stacked_with_retry with args=(10,), kwargs={}
[LOG] stacked_with_retry raised: Simulated failure
[RETRY] Failed: Simulated failure
[RETRY] Attempt 2/2
[LOG] Calling stacked_with_retry with args=(10,), kwargs={}
[TIMER] stacked_with_retry took 0.1003s
[LOG] stacked_with_retry returned: 20
[RETRY] Success!
Final result: 20
```

### Solution

```python
import time
from functools import wraps

def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f'[TIMER] {func.__name__} took {end-start:.4f}s')
        return result
    return wrapper

def logger(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f'[LOG] Calling {func.__name__} with args={args}, kwargs={kwargs}')
        try:
            result = func(*args, **kwargs)
            print(f'[LOG] {func.__name__} returned: {result}')
            return result
        except Exception as e:
            print(f'[LOG] {func.__name__} raised: {e}')
            raise
    return wrapper

def retry(max_attempts=3):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try:
                    print(f'[RETRY] Attempt {attempt}/{max_attempts}')
                    result = func(*args, **kwargs)
                    print(f'[RETRY] Success!')
                    return result
                except Exception as e:
                    print(f'[RETRY] Failed: {e}')
                    if attempt >= max_attempts:
                        print(f'[RETRY] Max attempts reached')
                        raise
        return wrapper
    return decorator

# Test
@timer
@logger
@retry(max_attempts=2)
def stacked_success(x):
    time.sleep(0.2)
    return x ** 2

result = stacked_success(5)
print(f"Result: {result}")
```

---

## BONUS EXERCISES

### Bonus 1: Counting Decorator

Create a decorator that counts how many times a function has been called.

```python
def count_calls(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        wrapper.call_count += 1
        print(f'[COUNT] {func.__name__} has been called {wrapper.call_count} times')
        return func(*args, **kwargs)
    wrapper.call_count = 0
    return wrapper

@count_calls
def greet(name):
    return f"Hello {name}"

greet("Alice")  # Called 1 times
greet("Bob")    # Called 2 times
greet("Charlie") # Called 3 times
```

### Bonus 2: Validation Decorator

Create a decorator that validates function arguments.

```python
def validate_positive(*arg_names):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Check positional arguments
            for i, val in enumerate(args):
                if isinstance(val, (int, float)) and val < 0:
                    raise ValueError(f"Argument {i} must be positive, got {val}")
            
            # Check keyword arguments
            for name, val in kwargs.items():
                if isinstance(val, (int, float)) and val < 0:
                    raise ValueError(f"Argument '{name}' must be positive, got {val}")
            
            return func(*args, **kwargs)
        return wrapper
    return decorator

@validate_positive()
def square(x):
    return x ** 2

print(square(5))    # 25
print(square(-5))   # ValueError: Argument 0 must be positive, got -5
```

### Bonus 3: Caching Decorator

Create a decorator that caches function results.

```python
def cache(func):
    cached_results = {}
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Create cache key from args and kwargs
        key = (args, tuple(sorted(kwargs.items())))
        
        if key in cached_results:
            print(f'[CACHE] Returning cached result for {func.__name__}')
            return cached_results[key]
        
        print(f'[CACHE] Computing result for {func.__name__}')
        result = func(*args, **kwargs)
        cached_results[key] = result
        return result
    
    return wrapper

@cache
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

print(fibonacci(5))  # Computed with heavy caching
```

### Bonus 4: Type Checking Decorator

Create a decorator that checks argument types.

```python
def type_check(**type_rules):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Check kwargs types
            for arg_name, expected_type in type_rules.items():
                if arg_name in kwargs:
                    value = kwargs[arg_name]
                    if not isinstance(value, expected_type):
                        raise TypeError(
                            f"Argument '{arg_name}' must be {expected_type}, "
                            f"got {type(value)}"
                        )
            
            return func(*args, **kwargs)
        return wrapper
    return decorator

@type_check(name=str, age=int)
def create_person(name, age):
    return f"{name} is {age} years old"

print(create_person(name="Alice", age=30))  # OK
print(create_person(name="Bob", age="thirty"))  # TypeError
```

---

## COMPLETION CHECKLIST

- [ ] Exercise 1: add_prefix decorator (both syntaxes)
- [ ] Exercise 2: timer decorator (multiple function types)
- [ ] Exercise 3: logger decorator (args and kwargs)
- [ ] Exercise 4: retry decorator with max_attempts
- [ ] Exercise 5: stacked decorators (observed execution order)
- [ ] All exercises have working code
- [ ] All exercises produce expected output
- [ ] Bonus exercises attempted (at least one)

---

## TESTING GUIDE

Run your decorators with edge cases:

```python
# Test with no arguments
@my_decorator
def no_args():
    pass

# Test with positional arguments
@my_decorator
def with_args(a, b, c):
    pass

# Test with keyword arguments
@my_decorator
def with_kwargs(name, greeting="Hello"):
    pass

# Test with return value
@my_decorator
def returns_value():
    return 42

# Test with exception
@my_decorator
def raises_exception():
    raise ValueError("Error!")

# Test with multiple decorators
@decorator1
@decorator2
@decorator3
def multi_decorated():
    pass
```

Ensure your decorators handle all these cases correctly!


---

# INTERVIEW QUESTIONS — Python Decorators
**Day 1 Python Decorators | Full Preparation Guide**

---

## Q1: What is a decorator in Python? Explain without using the word 'decorator'.

### Asked By
Meta, Google, Amazon, Apple

### Key Points to Cover
- Function that wraps another function
- Extends/modifies behavior without changing original code
- Based on higher-order functions
- Used extensively in frameworks (Flask, Django, FastAPI)

### Sample Answer

A decorator is a function that takes another function as input and returns a modified version of that function. It follows the higher-order function pattern where a function can accept other functions as arguments.

The main purpose is to add extra functionality or modify behavior without changing the original function's code. For example:

```python
def timer(func):
    def wrapper(*args, **kwargs):
        import time
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"Took {end-start:.4f}s")
        return result
    return wrapper

@timer  # This is a decorator
def slow_function():
    import time
    time.sleep(1)

# slow_function = timer(slow_function)  # This is what @ does
```

### Follow-up Questions to Prepare For
- Can you give a real-world example?
- What frameworks use decorators?
- What's the difference between @ syntax and manual application?

---

## Q2: What is the difference between @decorator and decorator(func)?

### Asked By
Amazon, Microsoft, Google

### Key Points to Cover
- They are identical in functionality
- @ is syntactic sugar
- Same result, different presentation
- When to use each

### Sample Answer

Both `@decorator` and `decorator(func)` do exactly the same thing. The `@` syntax is just syntactic sugar that makes the code more readable and Pythonic.

**They are equivalent:**

```python
# These two are identical:

# Method 1: Using @ syntax (Pythonic, recommended)
@my_decorator
def func():
    pass

# Method 2: Manual application
def func():
    pass
func = my_decorator(func)
```

**Comparison Table:**

| Aspect | @decorator | decorator(func) |
|--------|-----------|-----------------|
| **Syntax** | `@decorator` above definition | `func = decorator(func)` |
| **Readability** | More clean, Pythonic | More verbose |
| **Use Case** | 99% of the time | Dynamic/conditional decoration |
| **Multiple** | Easy: @dec1 @dec2 def f(): | Nested: f = dec1(dec2(f)) |
| **Timing** | At definition | Any time |

**When to use each:**

```python
# Use @ syntax (99% of cases)
@my_decorator
def regular_function():
    pass

# Use manual syntax when decorating conditionally
def my_function():
    pass

if some_condition:
    my_function = decorator1(my_function)
else:
    my_function = decorator2(my_function)
```

---

## Q3: When does a decorator execute — at definition or at call time?

### Asked By
Google, Facebook (Meta), Apple, Microsoft, Amazon

### Key Points to Cover
- Decorators execute at **definition time** (very important!)
- Common interview trap
- Show with clear example
- Explain why this matters

### Sample Answer

**Decorators execute at DEFINITION TIME, not call time.**

This is a very common interview trick question. Here's proof:

```python
def my_decorator(func):
    print("🔴 DECORATOR IS RUNNING (definition time)")
    
    def wrapper():
        print("🟢 WRAPPER IS RUNNING (call time)")
        func()
    
    return wrapper

print("BEFORE DEFINITION")

@my_decorator
def greet():
    print("GREET IS RUNNING")

print("AFTER DEFINITION")
print("\nNOW CALLING THE FUNCTION:")

greet()

# OUTPUT:
# BEFORE DEFINITION
# 🔴 DECORATOR IS RUNNING (definition time)
# AFTER DEFINITION
# 
# NOW CALLING THE FUNCTION:
# 🟢 WRAPPER IS RUNNING (call time)
# GREET IS RUNNING
```

**Why does this matter?**

1. **Side effects happen early:** If your decorator has side effects, they happen when the module is imported, not when the function is called.

2. **Setup/teardown:** You might want to do initialization when function is defined.

```python
import database

def use_db_connection(func):
    print("Setting up database connection")  # Happens at import time
    
    def wrapper(*args, **kwargs):
        db = database.connect()  # Happens at call time
        result = func(*args, **kwargs)
        db.close()
        return result
    
    return wrapper

@use_db_connection  # Database setup happens HERE
def query_users():  # Not here
    pass

query_users()  # Database connection made HERE
```

---

## Q4: Why do we use *args and **kwargs inside the wrapper function?

### Asked By
Amazon, Google, Facebook (Meta), Apple

### Key Points to Cover
- Makes decorator generic
- Works with any function signature
- Without them, decorator is limited
- Show what breaks without them

### Sample Answer

`*args` and `**kwargs` make the wrapper function accept **any number and type of arguments**, making your decorator work with ANY function signature.

**Without them (BROKEN):**

```python
def bad_decorator(func):
    def wrapper(a, b):  # ONLY works for 2 arguments!
        print("Before")
        return func(a, b)
    return wrapper

@bad_decorator
def add(a, b):
    return a + b

print(add(5, 3))  # Works ✓

@bad_decorator
def greet(name):  # Only 1 argument!
    return f"Hello {name}"

print(greet("Alice"))  # TypeError: wrapper() takes 2 positional arguments but 1 was given ✗
```

**With them (FIXED):**

```python
def good_decorator(func):
    def wrapper(*args, **kwargs):  # Accept ANY arguments!
        print("Before")
        return func(*args, **kwargs)
    return wrapper

@good_decorator
def add(a, b):
    return a + b

@good_decorator
def greet(name):
    return f"Hello {name}"

@good_decorator
def process(x, y, z, operation="add"):
    if operation == "add":
        return x + y + z
    return x * y * z

print(add(5, 3))  # Works ✓
print(greet("Alice"))  # Works ✓
print(process(1, 2, 3))  # Works ✓
print(process(1, 2, 3, operation="multiply"))  # Works ✓
```

**How *args and **kwargs work:**

```python
def example(*args, **kwargs):
    print(f"args: {args}")  # Tuple of positional arguments
    print(f"kwargs: {kwargs}")  # Dict of keyword arguments

example(1, 2, 3)
# args: (1, 2, 3)
# kwargs: {}

example(1, 2, name="Alice", age=30)
# args: (1, 2)
# kwargs: {'name': 'Alice', 'age': 30}

# When calling with *, they unpack:
args = (5, 3)
kwargs = {'operation': 'add'}
result = some_function(*args, **kwargs)
# Equivalent to: some_function(5, 3, operation='add')
```

---

## Q5: What happens if you forget to return result from wrapper?

### Asked By
Amazon, Google, Facebook (Meta), Bloomberg

### Key Points to Cover
- Function returns None instead of actual value
- Very common mistake
- Show the difference
- Why it matters

### Sample Answer

If you forget to capture and return the original function's result, the decorated function returns `None` instead of its actual return value.

**WRONG (Missing return):**

```python
def bad_decorator(func):
    def wrapper(*args, **kwargs):
        print("Before")
        func(*args, **kwargs)  # Called but result is ignored!
        # Missing: result = ...
        # Missing: return result
    return wrapper

@bad_decorator
def add(a, b):
    return a + b

result = add(5, 3)
print(result)  # Output: None (WRONG! Should be 8)

user = get_user(1)
print(user)  # Output: None (WRONG! Should be user object)
```

**CORRECT (With return):**

```python
def good_decorator(func):
    def wrapper(*args, **kwargs):
        print("Before")
        result = func(*args, **kwargs)  # Capture the result
        print("After")
        return result  # Return the result!
    return wrapper

@good_decorator
def add(a, b):
    return a + b

result = add(5, 3)
print(result)  # Output: 8 (CORRECT!)

user = get_user(1)
print(user)  # Output: <User object> (CORRECT!)
```

**Why this matters:**

1. **Breaks function contracts:** Users expect the function to return its value
2. **Silent failures:** Code might work but produce wrong data
3. **Debugging nightmare:** All calls return None, hard to find the issue

**Real-world example:**

```python
# This broken decorator is in production...
@broken_cache
def fetch_user(user_id):
    return database.query(f"SELECT * FROM users WHERE id = {user_id}")

# Code trying to use it:
user = fetch_user(123)
if user:  # Always False because user is None!
    print(user.name)
else:
    print("User not found")  # Always prints this (BUG!)
```

---

## Q6: What does functools.wraps do and why is it important?

### Asked By
Google, Facebook (Meta), Stripe, Microsoft

### Key Points to Cover
- Preserves function metadata
- What metadata is lost without it
- Why it matters
- Show the difference

### Sample Answer

`functools.wraps` is a decorator that preserves the original function's metadata when creating a wrapper function. Without it, the wrapper function's metadata is used instead.

**WITHOUT functools.wraps (WRONG):**

```python
def bad_decorator(func):
    def wrapper(*args, **kwargs):
        print("Before")
        return func(*args, **kwargs)
    return wrapper

@bad_decorator
def my_function():
    """This function calculates the sum of two numbers"""
    pass

# Metadata is lost!
print(my_function.__name__)   # Output: "wrapper" (WRONG! Should be "my_function")
print(my_function.__doc__)    # Output: None (WRONG! Should be docstring)
print(my_function.__module__) # Output: "decorator" (WRONG!)
```

**WITH functools.wraps (CORRECT):**

```python
from functools import wraps

def good_decorator(func):
    @wraps(func)  # This decorator preserves metadata!
    def wrapper(*args, **kwargs):
        print("Before")
        return func(*args, **kwargs)
    return wrapper

@good_decorator
def my_function():
    """This function calculates the sum of two numbers"""
    pass

# Metadata is preserved!
print(my_function.__name__)   # Output: "my_function" (CORRECT!)
print(my_function.__doc__)    # Output: "This function..." (CORRECT!)
print(my_function.__module__) # Output: "__main__" (CORRECT!)
```

**What metadata does wraps preserve?**

```python
# functools.wraps copies these attributes:
__name__        # Function name
__doc__         # Docstring
__module__      # Module name
__qualname__    # Qualified name
__annotations__ # Type hints
__dict__        # Function's namespace
```

**Why does this matter?**

1. **Documentation tools:** Tools like `help()`, Sphinx, and IDE auto-complete rely on `__doc__` and `__name__`
2. **Debugging:** Stack traces show the wrong function name without it
3. **Testing:** Test frameworks use function names in reports
4. **Introspection:** Code that inspects functions breaks

```python
# Example: help() without wraps
@bad_decorator
def process_data(x, y):
    """Process two data points"""
    return x + y

help(process_data)
# Output shows "wrapper" with no docstring (CONFUSING!)

# Example: help() with wraps
@good_decorator
def process_data(x, y):
    """Process two data points"""
    return x + y

help(process_data)
# Output shows "process_data" with correct docstring (CORRECT!)
```

---

## Q7: How does stacking multiple decorators work? What is the execution order?

### Asked By
Google, Facebook (Meta), Amazon, Microsoft

### Key Points to Cover
- Decorators applied bottom-to-top at definition
- Executed inside-out at call time
- Show with clear example
- Draw diagram if possible

### Sample Answer

When multiple decorators are stacked, they are applied from **bottom-to-top** at definition time, and executed from **inside-out** at call time.

**Order of application (definition time):**

```python
@decorator1
@decorator2
@decorator3
def func():
    pass

# Is equivalent to:
func = decorator1(decorator2(decorator3(func)))

# Application order:
# 1. decorator3(func)     - Applied first
# 2. decorator2(result)   - Applied to result
# 3. decorator1(result)   - Applied last
```

**Example with clear output:**

```python
def decorator1(func):
    print("DECORATOR1 applied")
    def wrapper(*args, **kwargs):
        print("→ DECORATOR1 wrapper")
        return func(*args, **kwargs)
    return wrapper

def decorator2(func):
    print("DECORATOR2 applied")
    def wrapper(*args, **kwargs):
        print("→ DECORATOR2 wrapper")
        return func(*args, **kwargs)
    return wrapper

def decorator3(func):
    print("DECORATOR3 applied")
    def wrapper(*args, **kwargs):
        print("→ DECORATOR3 wrapper")
        return func(*args, **kwargs)
    return wrapper

print("=== DEFINITION TIME ===")
@decorator1
@decorator2
@decorator3
def greet():
    print("→ GREET function")

print("\n=== CALL TIME ===")
greet()

# OUTPUT:
# === DEFINITION TIME ===
# DECORATOR3 applied
# DECORATOR2 applied
# DECORATOR1 applied
# 
# === CALL TIME ===
# → DECORATOR1 wrapper
# → DECORATOR2 wrapper
# → DECORATOR3 wrapper
# → GREET function
```

**Practical example with real decorators:**

```python
import time
from functools import wraps

def logger(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"[LOG] Calling {func.__name__}")
        result = func(*args, **kwargs)
        print(f"[LOG] {func.__name__} returned {result}")
        return result
    return wrapper

def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"[TIMER] Took {end-start:.4f}s")
        return result
    return wrapper

@logger
@timer
def slow_function():
    time.sleep(0.1)
    return "Done"

slow_function()

# OUTPUT:
# [LOG] Calling slow_function
# [TIMER] Took 0.1005s
# [LOG] slow_function returned Done
```

---

## Q8: Can decorators take arguments? Give an example.

### Asked By
Facebook (Meta), Google, Amazon, Stripe

### Key Points to Cover
- Decorators can take arguments
- Need extra level of nesting (decorator factory)
- Usage pattern
- Show real-world example

### Sample Answer

Yes! To make a decorator take arguments, you need to wrap it in another function. This is called a **decorator factory**.

**Basic example:**

```python
def repeat(times):  # ← Takes argument
    def decorator(func):  # ← Decorator
        def wrapper(*args, **kwargs):  # ← Wrapper
            results = []
            for _ in range(times):
                results.append(func(*args, **kwargs))
            return results
        return wrapper
    return decorator

@repeat(times=3)  # ← Note the parentheses!
def greet(name):
    return f"Hello {name}!"

print(greet("Alice"))
# Output: ['Hello Alice!', 'Hello Alice!', 'Hello Alice!']
```

**Structure explanation:**

```python
@repeat(times=3)
def func():
    pass

# Equivalent to:
func = repeat(times=3)(func)

# Step by step:
# 1. repeat(times=3) is called → returns decorator function
# 2. decorator(func) is called → returns wrapper function
# 3. func is now the wrapper function
```

**Real-world examples:**

Flask route decorator:
```python
from flask import Flask

app = Flask(__name__)

@app.route('/home', methods=['GET', 'POST'])  # Takes arguments!
def home():
    return "Home page"

@app.route('/user/<int:user_id>')
def get_user(user_id):
    return f"User {user_id}"
```

Rate limiting decorator:
```python
def rate_limit(calls_per_second=1):
    def decorator(func):
        last_called = [0.0]
        min_interval = 1.0 / calls_per_second
        
        def wrapper(*args, **kwargs):
            elapsed = time.time() - last_called[0]
            if elapsed < min_interval:
                time.sleep(min_interval - elapsed)
            result = func(*args, **kwargs)
            last_called[0] = time.time()
            return result
        return wrapper
    return decorator

@rate_limit(calls_per_second=2)
def api_call():
    return requests.get("https://api.example.com")
```

---

## Q9: What is the difference between decorating a function vs a class?

### Asked By
Google, Facebook (Meta), Amazon

### Key Points to Cover
- Function decorators wrap function behavior
- Class decorators wrap class behavior
- Different use cases
- Show examples

### Sample Answer

**Function decorators** modify how a function works. **Class decorators** modify how a class works (add methods, change attributes, etc.).

**Function decorator:**

```python
def uppercase(func):
    """Function decorator - transforms output"""
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return result.upper() if isinstance(result, str) else result
    return wrapper

@uppercase
def greet(name):
    return f"hello {name}"

print(greet("Alice"))  # "HELLO ALICE"
```

**Class decorator:**

```python
def add_repr(cls):
    """Class decorator - adds/modifies class behavior"""
    def __repr__(self):
        attrs = ", ".join(f"{k}={v}" for k, v in self.__dict__.items())
        return f"{cls.__name__}({attrs})"
    cls.__repr__ = __repr__
    return cls

@add_repr
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

p = Person("Alice", 30)
print(p)  # Person(name=Alice, age=30)
```

**Modify class attributes:**

```python
def add_id(cls):
    """Add ID to every instance"""
    cls.id_counter = 0
    original_init = cls.__init__
    
    def new_init(self, *args, **kwargs):
        cls.id_counter += 1
        self.id = cls.id_counter
        original_init(self, *args, **kwargs)
    
    cls.__init__ = new_init
    return cls

@add_id
class User:
    def __init__(self, name):
        self.name = name

u1 = User("Alice")
u2 = User("Bob")
print(u1.id, u1.name)  # 1 Alice
print(u2.id, u2.name)  # 2 Bob
```

---

## Q10: Name a common mistake people make with decorators

### Asked By
Amazon, Google, Microsoft, Apple

### Key Points to Cover
- Forgetting to return result
- Not using *args/**kwargs
- Thinking decorator runs at call time
- Not using functools.wraps

### Sample Answer

There are several common mistakes:

**Mistake 1: Forgetting to return result**

```python
# ❌ WRONG
def bad_decorator(func):
    def wrapper(*args, **kwargs):
        print("Before")
        func(*args, **kwargs)  # Result thrown away!
    return wrapper

@bad_decorator
def add(a, b):
    return a + b

result = add(5, 3)
print(result)  # None (WRONG!)

# ✅ CORRECT
def good_decorator(func):
    def wrapper(*args, **kwargs):
        print("Before")
        result = func(*args, **kwargs)
        return result  # Return the result
    return wrapper
```

**Mistake 2: Not using *args/**kwargs**

```python
# ❌ WRONG
def bad_decorator(func):
    def wrapper():  # No parameters!
        return func()  # Doesn't work with arguments
    return wrapper

@bad_decorator
def add(a, b):
    return a + b

add(5, 3)  # TypeError!

# ✅ CORRECT
def good_decorator(func):
    def wrapper(*args, **kwargs):  # Accept any arguments
        return func(*args, **kwargs)
    return wrapper
```

**Mistake 3: Forgetting functools.wraps**

```python
# ❌ WRONG
def bad_decorator(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@bad_decorator
def documented_func():
    """My docstring"""
    pass

print(documented_func.__name__)  # "wrapper" (WRONG!)
print(documented_func.__doc__)   # None (WRONG!)

# ✅ CORRECT
from functools import wraps

def good_decorator(func):
    @wraps(func)  # Preserve metadata
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@good_decorator
def documented_func():
    """My docstring"""
    pass

print(documented_func.__name__)  # "documented_func" (CORRECT!)
print(documented_func.__doc__)   # "My docstring" (CORRECT!)
```

---

## BONUS QUESTIONS

### Q11: How would you implement a decorator that validates function arguments?

```python
def validate_types(**type_rules):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for name, expected_type in type_rules.items():
                if name in kwargs:
                    if not isinstance(kwargs[name], expected_type):
                        raise TypeError(f"{name} must be {expected_type}")
            return func(*args, **kwargs)
        return wrapper
    return decorator

@validate_types(name=str, age=int)
def create_user(name, age):
    return f"{name} is {age}"

create_user(name="Alice", age=30)  # ✓ Works
create_user(name="Bob", age="thirty")  # ✗ TypeError
```

### Q12: How would you implement a memoization decorator?

```python
def memoize(func):
    cache = {}
    
    @wraps(func)
    def wrapper(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]
    
    return wrapper

@memoize
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

print(fibonacci(10))  # Much faster due to caching
```

### Q13: Can you use a class as a decorator?

```python
class MyDecorator:
    def __init__(self, func):
        self.func = func
    
    def __call__(self, *args, **kwargs):
        print("Before")
        result = self.func(*args, **kwargs)
        print("After")
        return result

@MyDecorator
def greet(name):
    return f"Hello {name}"

print(greet("Alice"))
# Output:
# Before
# Hello Alice
# After
```

---

## PRACTICE TIPS

1. **Implement from scratch:** Write decorators without looking at examples
2. **Test thoroughly:** Test with different function signatures
3. **Use real projects:** Add decorators to your own code
4. **Understand deeply:** Know why each part is needed
5. **Practice stacking:** Combine multiple decorators frequently

---

## FINAL INTERVIEW STRATEGY

1. **Start simple:** Begin with basic decorator definition
2. **Show examples:** Provide working code, not just theory
3. **Explain why:** Understand the purpose of each line
4. **Avoid mistakes:** Always use *args, **kwargs, functools.wraps
5. **Show your knowledge:** Mention framework usage (Flask, Django)
6. **Ask clarifying questions:** "Should this work with async functions?" etc.

Good luck! 🚀


---

