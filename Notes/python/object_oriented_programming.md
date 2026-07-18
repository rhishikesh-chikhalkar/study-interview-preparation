---

    - **Why?** These specific integers are the most heavily used in everyday programming (loop counters, list indices, boolean equivalents). By pre-allocating them, CPython avoids the overhead of calling `malloc()` every time you type `x = 1`.
    - **The Proof:** If you assign `a = 100` and `b = 100`, `a is b` evaluates to `True` because they point to the exact same memory address. But if you do `c = 300` and `d = 300`, `c is d` evaluates to `False` (usually, depending on the compiler context) because 300 falls outside the pre-allocated cache, forcing Python to create two distinct objects in memory.
  - **String Interning**
    - **The Mechanic:** CPython automatically caches (or "interns") certain string literals. If you create two strings with the same value, Python will often point them to the exact same object in memory.
    - **The Rules:** Python implicitly interns strings that look like valid identifiers (i.e., they only contain letters, numbers, and underscores). Strings with spaces or special characters are generally not automatically interned.

---

    - **Why?** This is heavily optimized for dictionary keys. Python relies on dictionaries for almost everything under the hood (module namespaces, class attributes, etc.). If strings are interned, Python can use pointer comparison (checking if memory addresses match, which is an $O(1)$ CPU instruction) rather than string comparison (checking character-by-character, which is $O(n)$) when looking up dictionary keys.

---

- **019. Unlike Java or C++, Python does not have private or protected keywords. How do you actually achieve encapsulation and data hiding in Python?**
  Python operates on a famous design philosophy: "We are all consenting adults here." This means Python trusts the developer not to mess with internal state if they are told not to, rather than strictly enforcing it at the compiler level.
  However, architecturally, you achieve encapsulation in Python using three progressive tiers:
  **1. The Closure Method (Functional Encapsulation)**
  As we saw in the `nonlocal` example, using nested functions creates true, strict encapsulation. The variables inside the outer function cannot be accessed or modified from the global scope under any circumstances.
  **2. The Naming Convention (The "Gentleman's Agreement")**
  In Object-Oriented Python, if an attribute or method is meant for internal use only, you prefix it with a single underscore (e.g., `_database_connection`).
  - **Under the hood:** This does absolutely nothing to stop another developer from accessing it. It is purely a semantic warning that says: "This is an internal implementation detail. If you touch this and your code breaks in the next update, it is your fault." (Note: It does prevent the variable from being imported when using `from module import *`).
  **3. Name Mangling (Pseudo-Privacy)**
  If you genuinely want to prevent accidental overriding of attributes (especially in class inheritance), you use a double underscore prefix (e.g., `__secret_key`).
  - **Under the hood:** This triggers a mechanism called name mangling. The Python interpreter automatically rewrites the attribute name to include the class name: `_ClassName__secret_key`. This makes it significantly harder for subclasses or external functions to accidentally overwrite or access the data, though a determined developer can still access it if they know the mangled name.
  **4. The Pythonic Way: `@property` Decorators**
  If you need to control how an attribute is set (e.g., adding validation logic) without breaking the public API, Python uses the `@property` decorator instead of traditional Java-style `get_value()` and `set_value()` methods.
  ### The Code Example
  Here is a class that demonstrates Python's three Object-Oriented encapsulation techniques in action.
  ```python
  class BankAccount:
      def __init__(self, owner, balance):
          self.owner = owner               # Public attribute
          self._routing_number = "12345"   # Protected (by convention only)
          self.__balance = balance         # Private (via name mangling)

      # -----------------------------------------
      # ENCAPSULATION VIA @property (Getters & Setters)
      # -----------------------------------------

      @property
      def balance(self):
          """The getter: Allows read-only access to the mangled variable."""
          return self.__balance

      @balance.setter
      def balance(self, new_amount):
          """The setter: Allows controlled modification with validation."""
          if new_amount < 0:
              raise ValueError("Balance cannot be negative.")
          self.__balance = new_amount

  # Execution
  account = BankAccount("Alice", 1000)

  # 1. Accessing Public Data
  print(account.owner)
  # Output: Alice

  # 2. Accessing "Protected" Data (Python allows this, but it's bad practice)
  print(account._routing_number)
  # Output: 12345

  # 3. Accessing "Private" Data (Fails due to name mangling)
  # print(account.__balance)
  # AttributeError: 'BankAccount' object has no attribute '__balance'

  # 4. Accessing the Mangled Name directly (The "escape hatch")
  print(account._BankAccount__balance)
  # Output: 1000 (Proving it's not strictly private, just hidden!)

  # 5. Using the @property interface (The safe, Pythonic way)
  print(account.balance) # Calls the getter
  account.balance = 1500 # Calls the setter safely

  # account.balance = -50
  # ValueError: Balance cannot be negative.
  ```
  **Why this matters for a Senior Engineer:**
  A senior engineer knows that `@property` is powerful because it allows you to start with simple public attributes (`self.balance`) and, if requirements change later (e.g., adding validation), you can swap it to a `@property` without breaking any external code that uses `account.balance`. It allows for graceful architectural evolution.

---

---

  - **Why? The Parsing Engine.** As we discussed earlier, Python's C-parser relies heavily on indentation (suites) to understand where blocks of code begin and end. Because lambdas are designed to be written entirely on a single line, allowing multi-line statements (like a `try/except` block or a `for` loop) inside a one-line lambda would completely break Python's indentation-based grammar. To keep the parser fast and unambiguous, the creators locked lambdas to single expressions.
  **3. When to use them (The Sweet Spot)**
  Senior engineers use lambdas almost exclusively as **throwaway functional arguments**.
  - If you are using functions like `sorted()`, `max()`, `map()`, or `filter()`, and you need to pass in a tiny piece of custom logic that you will _never_ use anywhere else in the codebase, a lambda is perfect. It keeps the logic close to where it is actually used.
  **4. When they become an Anti-Pattern (PEP 8 Violation)**
  The biggest junior mistake is assigning a lambda to a variable (e.g., `calculate = lambda x: x * 2`).
  - **The Problem:** The official Python style guide (PEP 8) strictly forbids this. The entire point of a lambda is to be _anonymous_. If you are assigning it to a name, you should just use a `def` statement. `def` provides much better traceback errors for debugging, supports docstrings, and allows for proper type hinting.
  ***
  ### **The Code Example**
  Here is how you demonstrate the right and wrong ways to use lambdas in a professional codebase.
  ```python
  # -----------------------------------------
  # SCENARIO A: The Anti-Pattern (Bad Architecture)
  # -----------------------------------------

  # BAD: Do not assign lambdas to variables!
  # If this crashes, the stack trace just says "<lambda> failed",
  # which is incredibly frustrating to debug.
  fetch_user_id = lambda user: user.get('id', 0)

  # GOOD: Just use 'def'. It's cleaner, allows type hints, and debugs well.
  def fetch_user_id(user: dict) -> int:
      return user.get('id', 0)

  # -----------------------------------------
  # SCENARIO B: The Sweet Spot (Good Architecture)
  # -----------------------------------------

  server_logs = [
      {"status": 500, "message": "Fatal Error"},
      {"status": 200, "message": "OK"},
      {"status": 404, "message": "Not Found"}
  ]

  # We need to sort this list of dictionaries by the 'status' integer.
  # A lambda is PERFECT here. It acts as a one-time data extractor.
  sorted_logs = sorted(server_logs, key=lambda log: log["status"])

  print(sorted_logs)
  # Output: [{'status': 200...}, {'status': 404...}, {'status': 500...}]

  # -----------------------------------------
  # SCENARIO C: The Statement Constraint
  # -----------------------------------------

  # VALID: An expression (evaluates to a value, even with inline ternary operators)
  valid_lambda = lambda x: "Even" if x % 2 == 0 else "Odd"

  # INVALID: SyntaxError. You cannot use statement keywords like 'pass', 'return', or 'if' blocks.
  # invalid_lambda = lambda x: pass
  ```

---

---

- **027. What does it mean for functions to be "first-class citizens" in Python? How does this paradigm power modern web frameworks, and what are the architectural pitfalls associated with it?**
  To a junior engineer, a function is just an instruction set. To a senior engineer, a function is a data structure—specifically, an instance of the `function` class living in memory, no different from an integer, a list, or a dictionary.
  **1. The "First-Class" Paradigm**
  Saying functions are "first-class citizens" means they possess four specific capabilities:
  1. They can be created at runtime.
  2. They can be assigned to variables or stored in data structures (like a dictionary of functions).
  3. They can be passed as arguments to other functions.
  4. They can be returned as the result of other functions.
  **2. Powering Modern Frameworks (The Decorator Pattern)**
  This paradigm is the absolute backbone of almost every modern Python framework (Django, Flask, FastAPI).
  - When you write `@app.get("/users")` in FastAPI, you are using a **Decorator**.
  - Architecturally, a decorator is only possible because functions are first-class. The framework takes your entire endpoint function, passes it as an argument into the framework's internal routing function, wraps it in HTTP handling logic, and returns a modified function. Without first-class functions, web frameworks would require massive, clunky class inheritance structures (like older versions of Java) just to register a basic web route.
  **3. The Architectural Pitfall (Late Binding in Closures)**
  The biggest trap of first-class functions occurs when you create functions dynamically inside a loop (a common pattern for generating callbacks or event listeners).
  - **The Mechanic:** Python uses **late binding**. When a closure (a nested function) references a variable from its enclosing scope (like a loop counter), it does not capture the _value_ of that variable at the time it was created. It captures the _memory reference_ to the variable.
  - **The Result:** By the time you actually execute the generated functions, the loop has already finished, and all the functions will evaluate using the _final_ state of the loop variable, leading to massive bugs.
  ***
  ### **The Code Example**
  If an interviewer asks you to demonstrate the power of first-class functions and the danger of late binding, use this code:
  ```python
  # -----------------------------------------
  # SCENARIO A: The Power of First-Class Functions
  # -----------------------------------------

  def execute_payment():
      return "Payment Processed"

  def cancel_payment():
      return "Payment Cancelled"

  # We can store functions in a dictionary like any other variable!
  # This is a classic pattern to avoid massive if/elif chains.
  action_router = {
      "process": execute_payment, # Note: No parentheses. We are storing the object itself.
      "cancel": cancel_payment
  }

  user_input = "process"
  # We fetch the function object from the dict, and THEN execute it with ()
  result = action_router[user_input]()
  print(result) # Output: Payment Processed

  # -----------------------------------------
  # SCENARIO B: The Late Binding Pitfall (Senior Gotcha)
  # -----------------------------------------

  def create_multipliers():
      multipliers = []

      # We create 3 separate functions inside a loop
      for i in range(3):
          # The nested lambda references the loop variable 'i'
          multipliers.append(lambda x: x * i)

      return multipliers

  # Execution
  funcs = create_multipliers()

  # A junior expects func[0] to multiply by 0, func[1] by 1, and func[2] by 2.
  # But because of Late Binding, 'i' evaluates to its FINAL state (2) when called!
  print(funcs[0](10)) # Output: 20
  print(funcs[1](10)) # Output: 20
  print(funcs[2](10)) # Output: 20

  # THE FIX: Force early binding by making 'i' a default argument
  # multipliers.append(lambda x, i=i: x * i)
  ```
  **Why this matters for a Senior Engineer:**
  If you are building a UI with dynamic buttons, or generating async tasks in a loop, failing to understand late binding means all of your buttons or tasks will execute using the payload of the very last item in the list, completely silently, without throwing an error.

---

---

- **032. How are classes and objects created internally? What is the difference between new and init, and what is the architectural purpose of the self keyword?**
  **1. OOP and Internal Creation (The `type` Metaclass)**
  At its core, OOP is a paradigm where state (data) and behavior (methods) are bundled together.
  - **Class vs Object:** A Class is the blueprint; an Object is the allocated memory instance of that blueprint.
  - **Internal Creation:** In Python, _everything_ is an object, including the class itself. When Python compiles a class, it secretly calls the `type()` metaclass to dynamically build the class object in memory.
  **2. The Constructor (`__new__`) vs The Initializer (`__init__`)**
  The most common junior mistake is calling `__init__` the constructor. It is not.
  - **`__new__(cls)`:** This is the _actual_ constructor. It is a static-like method that is called first. Its sole job is to request a block of memory from the CPython allocator and return a fresh, empty object.
  - **`__init__(self)`:** This is the initializer. It is called immediately _after_ `__new__`. It does not create the object (notice it doesn't return anything); it simply populates the empty object with initial state.
  **3. The Purpose of `self`**
  Unlike Java or C++, where `this` is a hidden magical keyword, Python strictly adheres to the Zen of Python: _"Explicit is better than implicit."_
  - When you call `employee.print_details()`, Python translates that under the hood to `Employee.print_details(employee)`.
  - `self` is not a reserved keyword; it is just a universally agreed-upon naming convention for the first positional argument. It acts as the pointer to the specific memory block (the object instance) so the method knows whose data to modify.
  ***
  ### **The Code Example**
  To demonstrate this, I will fulfill your request to create the `Fruit` and `Employee` logic, but I will write it the way a senior engineer would explain the object lifecycle on a whiteboard.
  ```python
  # -----------------------------------------
  # SCENARIO A: The Standard Approach (Fruit)
  # -----------------------------------------
  class Fruit:
      # 1. __init__ receives the newly created object via 'self'
      def __init__(self, name: str, price: float, quantity: int):
          self.name = name
          self.price = price
          self.quantity = quantity

      def get_total_cost(self) -> float:
          return self.price * self.quantity

  apple = Fruit("Apple", 1.50, 10)
  print(f"Total cost: ${apple.get_total_cost()}") # Output: Total cost: $15.0

  # -----------------------------------------
  # SCENARIO B: Exposing the Lifecycle (Employee)
  # -----------------------------------------
  class Employee:

      # 1. The TRUE Constructor: Allocates memory and returns the object
      def __new__(cls, name: str, emp_id: int):
          print(f"[MEMORY] Allocating memory for {cls.__name__}")
          # Call the base object class to actually carve out the memory
          instance = super(Employee, cls).__new__(cls)
          return instance

      # 2. The Initializer: Receives the allocated memory as 'self'
      def __init__(self, name: str, emp_id: int):
          print(f"[STATE] Initializing state for {name}")
          self.name = name
          self.emp_id = emp_id

      # 3. The Instance Method
      def print_details(self):
          print(f"Employee Name: {self.name}, ID: {self.emp_id}")

  # Watch the exact sequence of execution:
  emp = Employee("Alice", 1042)
  # Output 1: [MEMORY] Allocating memory for Employee
  # Output 2: [STATE] Initializing state for Alice

  # Under the hood, this syntax:
  emp.print_details()
  # Is literally executed by Python as this:
  Employee.print_details(emp)
  ```
  **Why this matters for a Senior Engineer:**
  You rarely override `__new__` in day-to-day coding. However, if you are designing a **Singleton** pattern (e.g., a database connection pool where you strictly only ever want one instance to exist in memory), or if you are subclassing immutable types like `tuple` or `str`, you _must_ override `__new__` because by the time `__init__` is called, the immutable object is already locked and cannot be changed.

---

---

- **033. What is the Method Resolution Order (MRO)? Architecturally, why does Python use C3 Linearization, why is multiple inheritance incredibly risky (the Diamond Problem), and what is the safer architectural alternative?**
  To a junior engineer, inheritance is a way to reuse code. To a senior engineer, inheritance is the tightest, most dangerous form of coupling you can introduce into a system.
  **1. The Diamond Problem and The MRO**
  Python supports **Multiple Inheritance** (a class can have more than one parent). This immediately creates the famous "Diamond Problem."
  - Imagine a base class `Animal` with a method `make_sound()`.
  - You create `Dog(Animal)` and `Robot(Animal)`, both overriding `make_sound()`.
  - You then create `RoboDog(Dog, Robot)`. If `RoboDog` calls `make_sound()`, whose sound does it make? The Dog's or the Robot's?
  - **The Solution:** Python solves this using the **MRO (Method Resolution Order)**. It is a strictly ordered list of classes that Python searches, from left to right, to find the method.
  **2. Why C3 Linearization?**
  Older versions of Python (Python 2.2 and earlier) used a simple "Depth-First, Left-to-Right" algorithm. It was deeply flawed and often caused parent classes to be checked before child classes.
  In Python 2.3, they adopted **C3 Linearization**. A senior engineer knows that C3 guarantees two absolute mathematical rules:
  1. **Local Precedence:** If `class RoboDog(Dog, Robot)`, Python guarantees that `Dog` will _always_ be checked before `Robot`.
  2. **Monotonicity:** If class X precedes class Y in a parent's MRO, it will _never_ be flipped in a child's MRO.
  If you try to create an inheritance structure that breaks these two rules, C3 refuses to compile it and immediately throws a `TypeError: Cannot create a consistent method resolution order (MRO)`.
  **3. The Risk of Multiple Inheritance (Spaghetti State)**
  Architecturally, multiple inheritance is a nightmare for state management.
  - If `Dog` has an `__init__` that takes a `name`, and `Robot` has an `__init__` that takes a `battery_level`, how does `RoboDog` initialize both?
  - You have to use `super().__init__()` heavily, and rely on `*kwargs` to pass the remaining arguments down the MRO chain. If one parent forgets to call `super()`, the chain breaks, and half your object's memory is never initialized.
  **4. The Safer Alternatives**
  - **Composition ("Has-a" instead of "Is-a"):** Instead of `RoboDog` inheriting from `Robot`, give `RoboDog` a `self.battery = RobotBattery()` instance variable. Inject the behavior rather than inheriting it. This decouples the code and makes unit testing significantly easier.
  - **Mixins:** If you _must_ use multiple inheritance, restrict yourself to the Mixin pattern. A Mixin is a small class designed only to add specific behavior (like `LoggableMixin` or `JSONSerializableMixin`). The strict architectural rule for Mixins is: **They must never hold state (no `__init__` method)**.
  ***
  ### **The Code Example**
  Here is how you demonstrate the Diamond Problem, the MRO, and why C3 Linearization is a lifesaver.
  ```python
  # -----------------------------------------
  # SCENARIO A: The Diamond Problem & MRO
  # -----------------------------------------
  class Animal:
      def make_sound(self):
          return "Generic Animal Sound"

  class Dog(Animal):
      def make_sound(self):
          return "Bark!"

  class Robot(Animal):
      def make_sound(self):
          return "Beep Boop!"

  # Multiple Inheritance: Dog is declared first!
  class RoboDog(Dog, Robot):
      pass

  rd = RoboDog()

  # Python checks RoboDog -> Dog -> Robot -> Animal -> object
  print(rd.make_sound())
  # Output: Bark!

  # You can view the C3 Linearization array directly:
  print([cls.__name__ for cls in RoboDog.mro()])
  # Output: ['RoboDog', 'Dog', 'Robot', 'Animal', 'object']

  # -----------------------------------------
  # SCENARIO B: C3 Linearization Preventing Chaos
  # -----------------------------------------
  class A: pass
  class B(A): pass

  # BAD ARCHITECTURE:
  # We are telling Python: "Inherit from A first, THEN B."
  # But B is a child of A! C3 Linearization realizes this breaks Monotonicity.
  # class C(A, B):
  #     pass

  # RESULT:
  # TypeError: Cannot create a consistent method resolution order (MRO) for bases A, B

  # -----------------------------------------
  # SCENARIO C: Composition (The Senior Fix)
  # -----------------------------------------
  class BatteryModule:
      def __init__(self, capacity):
          self.capacity = capacity

      def charge(self):
          return "Charging..."

  class BetterRoboDog(Dog):
      # It "is a" Dog, but it "has a" Battery.
      def __init__(self, battery_capacity):
          self.battery = BatteryModule(battery_capacity)

  safe_dog = BetterRoboDog(100)
  print(safe_dog.make_sound())       # Output: Bark!
  print(safe_dog.battery.charge())   # Output: Charging...
  ```
  **Why this matters for a Senior Engineer:**
  If you inherit a massive legacy Django or system architecture, understanding `__mro__` is the only way you will survive tracing where a specific method is coming from. And when designing new systems, preferring Composition over Inheritance proves that you build for modularity and long-term maintainability.

---

---

- **034. What is "Duck Typing," and what is its primary architectural pitfall? How do Abstract Base Classes (ABCs) solve this, and when does abstraction actually become an anti-pattern in Python?**
  To a junior engineer, polymorphism means overriding methods from a parent class. To a senior Python engineer, polymorphism is fundamentally uncoupled from inheritance due to Python's dynamic nature.
  **1. Polymorphism & Duck Typing**
  In languages like Java, if a function expects a `Bird` object, you _must_ pass an object that explicitly inherits from the `Bird` class.
  Python does not care about ancestry. It uses **Duck Typing**: _"If it walks like a duck and quacks like a duck, it must be a duck."_
  - **The Mechanic:** If a function calls `obj.quack()`, Python simply checks if the object in memory currently possesses a method named `quack`. It does not care if the object is a `Mallard`, a `Robot`, or a `Person`. If the method exists, it executes. This makes Python incredibly flexible.
  **2. The Polymorphism Pitfall (Runtime Explosions)**
  The danger of Duck Typing is that there is no compiler to save you.
  - If you pass a `Cat` into a function expecting a `quack()` method, a compiled language catches this before the code ever runs. Python will happily start executing the function and only crash with an `AttributeError` at the exact millisecond it tries to invoke `quack()`. In a production system, if that line of code is buried inside a rare `if` condition, that bug might sit silently for months before exploding.
  **3. Abstraction & ABCs (The Strict Contract)**
  To fix this runtime danger in large architectures, senior engineers enforce **Abstraction** using Python's `abc` module (Abstract Base Classes).
  - **The Mechanic:** You define a base class that inherits from `ABC` and decorate specific methods with `@abstractmethod`.
  - **The Benefit:** This creates a strict API contract. If a junior developer creates a subclass but forgets to implement the required method, Python refuses to even instantiate the object. It shifts the crash from "deep in the runtime execution" to "the exact moment the object is created," making it instantly caught by unit tests.
  **4. When Abstraction becomes an Anti-Pattern (The "Java-fication" of Python)**
  Because ABCs introduce strictness, engineers coming from enterprise Java often over-use them, creating massive hierarchies of `AbstractInterfaces` for every single entity.
  - **The Rule:** Abstraction should be avoided if you only have one implementation of a class, or if the architecture is small enough that simple Duck Typing and unit tests provide enough safety. Over-abstracting in Python slows down execution, clutters the namespace, and violates Python's core philosophy of simplicity.
  ***
  ### **The Code Example**
  Here is how you demonstrate the danger of standard Python polymorphism, and the architectural safety net of ABCs.
  ```python
  from abc import ABC, abstractmethod

  # -----------------------------------------
  # SCENARIO A: Duck Typing & The Runtime Pitfall
  # -----------------------------------------
  class Dog:
      def speak(self): return "Bark"

  class Cat:
      def speak(self): return "Meow"

  class Car:
      def honk(self): return "Beep"

  def make_noise(entity):
      # DUCK TYPING: We just assume 'speak' exists.
      # If a Car is passed in, this crashes at RUNTIME.
      print(entity.speak())

  make_noise(Dog()) # Output: Bark
  # make_noise(Car()) # AttributeError: 'Car' object has no attribute 'speak'

  # -----------------------------------------
  # SCENARIO B: The Abstract Base Class (The Safety Net)
  # -----------------------------------------
  class AudioEntity(ABC):

      @abstractmethod
      def speak(self):
          """All subclasses MUST implement this method."""
          pass

  class Robot(AudioEntity):
      # A junior engineer forgets to implement 'speak' and writes 'make_sound' instead
      def make_sound(self):
          return "Beep Boop"

  # Because of the ABC, Python refuses to even allocate memory for this object!
  # The bug is caught instantly on line 1, not buried deep in a function later.

  # faulty_robot = Robot()
  # TypeError: Can't instantiate abstract class Robot with abstract method speak
  ```
  **Why this matters for a Senior Engineer:**
  When you are building libraries or plugins that _other_ teams will consume, you must use ABCs. It provides self-documenting code and guarantees that the consuming team adheres strictly to the interface you designed, preventing them from pushing broken implementations into your system.

---

---

- **047. What is async/await and the Event Loop? At a system level, what is the difference between blocking and non-blocking code?**
  Threading relies on the Operating System to violently swap threads. **Asyncio** completely removes the OS from the equation. It is **Cooperative Multitasking** running entirely inside a _single_ thread.
  **1. The Event Loop (The Conductor)**
  Imagine a chef in a kitchen. The chef is the single CPU thread.
  - **Threading:** The OS forces the chef to chop an onion for 1 second, then teleports them to stir a pot for 1 second, then teleports them back to the onion. It's chaotic.
  - **Asyncio:** The chef puts bread in the toaster. Instead of staring at the toaster for 2 minutes (Blocking), the chef puts a sticky note on the fridge saying "Check toast later," and walks over to chop the onion (Non-blocking).
  - The **Event Loop** is the fridge with the sticky notes. It is an infinite loop that constantly checks which tasks are ready to run, and which tasks are waiting.
  **2. `async` and `await`**
  - `async def`: This tells Python, "This function is a coroutine. It doesn't run normally; it must be managed by the Event Loop."
  - `await`: This is the sticky note. It tells the Event Loop: _"I am waiting for I/O right here. Suspend my execution frame, go run other code, and wake me up when my data arrives."_
  **3. Blocking vs. Non-Blocking Code**
  - **Blocking Code:** A standard `requests.get()` physically halts the entire thread until the data arrives. The CPU literally stops.
  - **Non-Blocking Code:** An `await aiohttp.ClientSession().get()` fires the request, immediately yields control back to the Event Loop, and allows the CPU to do other things.
  ***
  ### **The Code Example**
  ```python
  import asyncio
  import time

  # -----------------------------------------
  # SCENARIO: The Power of the Event Loop
  # -----------------------------------------
  async def fetch_data(id):
      print(f"[{id}] Firing request...")
      # 'await asyncio.sleep' is NON-BLOCKING.
      # It tells the Event Loop: "I am pausing here. Go run another task!"
      await asyncio.sleep(2)
      print(f"[{id}] Data received!")

  async def main():
      start_time = time.time()

      # asyncio.gather schedules all these coroutines on the Event Loop concurrently.
      # Because they all yield control immediately, they all wait simultaneously.
      await asyncio.gather(
          fetch_data(1),
          fetch_data(2),
          fetch_data(3)
      )

      # Total time will be ~2 seconds.
      print(f"Async Time: {time.time() - start_time:.2f} seconds")

  # This is how you actually start the Event Loop
  # asyncio.run(main())
  ```

---

---

- **100. “In Python, functions are first-class objects.” What do you infer from this?**

In Python, functions are treated as **first-class objects**, meaning they can be:

1. **Assigned to variables**
2. **Passed as arguments to other functions**
3. **Returned from functions**
4. **Stored in data structures**

### **Example:**

```python
python
CopyEdit
# Assigning a function to a variable
def greet(name):
    return f"Hello, {name}"

hello_func = greet
print(hello_func("Alice"))  # Output: Hello, Alice

```

```python
python
CopyEdit
# Passing function as an argument
def apply_function(func, value):
    return func(value)

def square(x):
    return x ** 2

print(apply_function(square, 4))  # Output: 16

```

```python
python
CopyEdit
# Returning a function from another function
def outer_function():
    def inner_function():
        return "Inner function executed"
    return inner_function

func = outer_function()
print(func())  # Output: Inner function executed

```

This makes Python highly flexible and supports functional programming concepts.

---

---

- **126. Difference between for loop and while loop in Python?**

| **For Loop**                                      | **While Loop**                                     |
| ------------------------------------------------- | -------------------------------------------------- |
| Iterates over a **sequence** (e.g., list, string) | Executes **as long as a condition is true**        |
| Runs a fixed number of times                      | Can run indefinitely if the condition remains true |
| Example:                                          | Example:                                           |

### **For Loop Example:**

```python
python
CopyEdit
for i in range(5):
    print(i)

```

### **While Loop Example:**

```python
python
CopyEdit
x = 0
while x < 5:
    print(x)
    x += 1

```

---

---

### 103. Is there an Object-Oriented Programming (OOP) concept in Python?

Yes, Python is an object-oriented programming language. This means that Python programs can be structured using classes and objects. However, Python also supports procedural and functional programming paradigms.

---

### 106. How are classes created in Python?

Classes in Python are created using the `class` keyword, followed by the class name and a colon.

```python
python
CopyEdit
class MyClass:
    def __init__(self, name):
        self.name = name

    def greet(self):
        print(f"Hello, {self.name}!")

obj = MyClass("Alice")
obj.greet()  # Output: Hello, Alice!

```

---

### 110. What is inheritance in Python?

Inheritance allows a child class to inherit attributes and methods from a parent class, enabling code reuse and modularity.

---

### 111. What are the different types of inheritance in Python?

- **Single Inheritance** – One class inherits from another.
- **Multiple Inheritance** – A class inherits from more than one parent class.
- **Multi-level Inheritance** – A class inherits from another derived class.
- **Hierarchical Inheritance** – Multiple classes inherit from a single base class.

---

### 112. Is multiple inheritance possible in Python?

Yes, Python supports multiple inheritance, meaning a class can inherit from multiple parent classes.

---

### 113. Explain polymorphism in Python.

Polymorphism allows objects of different classes to be treated as objects of a common base class. It enables methods to be overridden or redefined in child classes.

---

### 114. What is encapsulation in Python?

Encapsulation is the process of restricting direct access to certain attributes and methods of a class while still allowing controlled modification through methods.

---

### 116. Are access specifiers used in Python?

Python does not have built-in access specifiers like **private**, **protected**, or **public**. However, prefixing an attribute with `_` (single underscore) suggests it is **protected**, and `__` (double underscore) suggests it is **private**.

---

### 117. How to create an empty class in Python?

An empty class can be created using the `pass` keyword.

```python
python
CopyEdit
class EmptyClass:
    pass

```

---

### 118. What does `object()` do in Python?

The `object()` function creates a featureless base object, which is the parent of all Python classes.

---

## 20. How to Copy an Object in Python?

Python provides the `copy` module for copying objects.

- **Shallow Copy**: Copies only references, not nested objects.
- **Deep Copy**: Recursively copies all objects.

```
from copy import copy, deepcopy

list_1 = [1, 2, [3, 5], 4]
list_2 = copy(list_1)  # Shallow Copy
list_2[2].append(6)
print(list_1)  # Output: [1, 2, [3, 5, 6], 4]

list_3 = deepcopy(list_1)  # Deep Copy
list_3[2].append(7)
print(list_1)  # Output: [1, 2, [3, 5, 6], 4]
```

---

# Python OOPs Interview Questions

---

## 1. How to Check if a Class is a Child of Another Class?

Use `issubclass()` to check if a class inherits from another:

```
class Parent:
    pass

class Child(Parent):
    pass

print(issubclass(Child, Parent))  # True
print(issubclass(Parent, Child))  # False
```

To check if an object belongs to a class, use `isinstance()`:

```
obj = Child()
print(isinstance(obj, Parent))  # True
```

---

## 2. What is `__init__` Method in Python?

The `__init__` method acts as a **constructor**, initializing attributes when an object is created.

```
class Employee:
    def __init__(self, name):
        self.name = name

    def introduce(self):
        print("Hello, I am", self.name)

emp = Employee("Alice")
emp.introduce()  # Output: Hello, I am Alice
```

---

## 3. Why is `finalize()` Used?

`finalize()` helps in **freeing unmanaged resources** before garbage collection occurs, ensuring proper memory management.

---

## 4. Difference Between `new` and `override` Modifiers

- `new`: Used when a method in a child class **hides** the base class method.
- `override`: Used when a method in a child class **overrides** the base class method.

---

## 5. How to Create an Empty Class in Python?

Use the `pass` keyword to define an empty class.

```
class EmptyClass:
    pass

obj = EmptyClass()
obj.name = "Example"
print(obj.name)  # Output: Example
```

---

## 6. Can a Parent Class Be Called Without Creating an Instance?

Yes, if the parent class contains **static methods** or is instantiated by child classes.

---

---

- **188. Are Access Specifiers Used in Python?**

Unlike other languages (e.g., Java, C++), Python does not have built-in access specifiers like `public`, `private`, or `protected`. Instead, it follows a **naming convention** using underscores:

- **Public (`variable`)**: No underscores, accessible anywhere.
- **Protected (`_variable`)**: Single underscore (`_`) suggests it's for internal use but still accessible.
- **Private (`__variable`)**: Double underscore (`__`) enforces name mangling to prevent accidental access.

### **Example: Demonstrating Access Specifiers**

```python
python
CopyEdit
# Demonstrating access specifiers
class InterviewbitEmployee:

    # Protected members
    _emp_name = None
    _age = None

    # Private members
    __branch = None

    # Constructor
    def __init__(self, emp_name, age, branch):
        self._emp_name = emp_name
        self._age = age
        self.__branch = branch

    # Public method
    def display(self):
        print(self._emp_name, self._age, self.__branch)

# Creating an instance
emp = InterviewbitEmployee("Alice", 30, "Software")

# Accessing protected member (Not recommended but possible)
print(emp._emp_name)  # ✅ Allowed

# Accessing private member (Will raise an error)
# print(emp.__branch)  # ❌ AttributeError

# Correct way to access private member using name mangling
print(emp._InterviewbitEmployee__branch)  # ✅ Allowed

```

---

---

- **189. How to Access Parent Members in a Child Class?**

There are **two primary ways** to access parent class members within a child class:

---

### **1️⃣ Using Parent Class Name**

You can explicitly reference the **parent class** to access its attributes.

```python
python
CopyEdit
class Parent(object):
    # Constructor
    def __init__(self, name):
        self.name = name

class Child(Parent):
    # Constructor
    def __init__(self, name, age):
        Parent.name = name  # Accessing parent attribute
        self.age = age

    def display(self):
        print(Parent.name, self.age)

# Driver Code
obj = Child("Interviewbit", 6)
obj.display()

```

📝 **Note:** This approach directly assigns values to the `Parent` class, which may not be the best practice.

---

---

- **190. Using super()**

The `super()` function is the preferred way to call parent class methods and attributes.

```python
python
CopyEdit
class Parent(object):
    # Constructor
    def __init__(self, name):
        self.name = name

class Child(Parent):
    # Constructor
    def __init__(self, name, age):
        '''
        In Python 3.x, we can also use super().__init__(name)
        '''
        super(Child, self).__init__(name)  # Calling Parent's constructor
        self.age = age

    def display(self):
        # Using self.name instead of Parent.name
        print(self.name, self.age)

# Driver Code
obj = Child("Interviewbit", 6)
obj.display()

```

📝 **Why use `super()`?**

- Avoids hardcoding the parent class name.
- Supports multiple inheritance better.
- More maintainable and recommended in modern Python.

---

---

- **191. How Does Inheritance Work in Python?**

Inheritance allows a class to access all attributes and methods of another class.

- It promotes code reusability and helps maintain applications without redundant code.
- The class that inherits is called the **child class (derived class)**.
- The class being inherited from is the **parent class (superclass)**.

Python supports different types of inheritance:

---

---

- **192. Single Inheritance**

A child class inherits from one parent class.

```python
python
CopyEdit
# Parent class
class ParentClass:
    def par_func(self):
         print("I am parent class function")

# Child class
class ChildClass(ParentClass):
    def child_func(self):
         print("I am child class function")

# Driver code
obj1 = ChildClass()
obj1.par_func()  # Accessing parent method
obj1.child_func()  # Accessing child method

```

---

---

- **193. Multi-level Inheritance**

In this type, class B inherits from class A, and class C inherits from class B.

```python
python
CopyEdit
# Parent class
class A:
   def __init__(self, a_name):
       self.a_name = a_name

# Intermediate class
class B(A):
   def __init__(self, b_name, a_name):
       self.b_name = b_name
       A.__init__(self, a_name)  # Calling parent class constructor

# Child class
class C(B):
   def __init__(self, c_name, b_name, a_name):
       self.c_name = c_name
       B.__init__(self, b_name, a_name)  # Calling intermediate class constructor

   def display_names(self):
       print("A name:", self.a_name)
       print("B name:", self.b_name)
       print("C name:", self.c_name)

# Driver code
obj1 = C('child', 'intermediate', 'parent')
print(obj1.a_name)
obj1.display_names()

```

---

---

- **194. Multiple Inheritance**

A child class inherits from more than one parent class.

```python
python
CopyEdit
# Parent class 1
class Parent1:
   def parent1_func(self):
       print("Hi, I am first Parent")

# Parent class 2
class Parent2:
   def parent2_func(self):
       print("Hi, I am second Parent")

# Child class
class Child(Parent1, Parent2):
   def child_func(self):
       self.parent1_func()
       self.parent2_func()

# Driver code
obj1 = Child()
obj1.child_func()

```

---

---

- **195. Hierarchical Inheritance**

A single parent class is inherited by multiple child classes.

```python
python
CopyEdit
# Base class
class A:
     def a_func(self):
         print("I am from the parent class.")

# First derived class
class B(A):
     def b_func(self):
         print("I am from the first child.")

# Second derived class
class C(A):
     def c_func(self):
         print("I am from the second child.")

# Driver code
obj1 = B()
obj2 = C()
obj1.a_func()
obj1.b_func()  # Child 1 method
obj2.a_func()
obj2.c_func()  # Child 2 method

```

---
