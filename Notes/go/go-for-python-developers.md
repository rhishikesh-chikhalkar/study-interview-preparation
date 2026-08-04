# Go for Python Developers

A quick reference guide comparing Go concepts to Python concepts, tailored for developers
transitioning from Python to Go.

---

## 1. Project Organization & Scope

In Python, every `.py` file is a self-contained module. In Go, compilation works on a
**directory-level** package system.

| Concept | Python | Go |
| :--- | :--- | :--- |
| **Code isolation** | Each `.py` file is isolated. | Each **directory** (package) is isolated. All files in a folder share scope. |
| **Entry Point** | `if __name__ == '__main__':` | `func main()` inside `package main` |
| **Organizing multiple scripts** | Just put multiple `.py` files in one folder. | Put each separate program into its own **subdirectory** (each with its own `func main()`). |

### Example Structure Comparison

To run two independent scripts in Python, you can put them in the same directory:
```
my_project/
├── hello.py
└── add_two_numbers.py
```

In Go, having two files in the same directory with their own `func main()` will cause a compiler
error (`main redeclared in this block`). Instead, structure them in subdirectories:
```
my_project/
├── hello/
│   └── hello.go  // package main, contains func main()
└── add_two_numbers/
    └── add_two_numbers.go  // package main, contains func main()
```

---

## 2. Loop Syntax

Go only has one looping keyword: `for`. It is used for all types of loops (ranges, condition-based,
infinite, and collection iteration).

### A. Counter/Range Loop

* **Python:**
  ```python
  for i in range(10):
      print(i)
  ```
* **Go:**
  ```go
  for i := 0; i < 10; i++ {
      fmt.Println(i)
  }
  ```
  * `i := 0`: Initialize a counter (uses short variable declaration `:=`).
  * `i < 10`: The condition under which the loop continues.
  * `i++`: Increment step executed after each iteration.

### B. Conditional Loop (While Loop)

* **Python:**
  ```python
  while x < 5:
      # Do something
  ```
* **Go:**
  ```go
  for x < 5 {
      // Do something
  }
  ```

### C. Infinite Loop

* **Python:**
  ```python
  while True:
      # Loop forever
  ```
* **Go:**
  ```go
  for {
      // Loop forever
  }
  ```

### D. Iterating Over Collections

* **Python (using `enumerate`):**
  ```python
  names = ["Alice", "Bob"]
  for index, name in enumerate(names):
      print(index, name)
  ```
* **Go (using `range`):**
  ```go
  names := []string{"Alice", "Bob"}
  for index, name := range names {
      fmt.Println(index, name)
  }
  ```

---

## 3. Functions & Static Typing

Unlike Python's dynamic typing, Go is strictly and statically typed. Parameter and return types
must be declared.

* **Python:**
  ```python
  def greeting(name: str) -> str:
      return "Hi " + name
  ```
* **Go:**
  ```go
  func greeting(name string) string {
      return "Hi " + name
  }
  ```
  * Parameter format: `[parameter_name] [type]`.
  * Return type is placed **after** the parameters list.

---

## 4. Variable Declaration (`:=` vs `=`)

* **Python:**
  ```python
  # Dynamic declaration and assignment
  message = "Hello"
  ```
* **Go:**
  Go has two ways to declare variables:
  1. **Short Assignment (`:=`):** Declares and initializes a variable, inferring the type
     automatically. Only works inside functions.
     ```go
     message := "Hello" // Declared as string
     ```
  2. **Standard Declaration (`var`):** Used if you want to declare a variable without initializing
     it immediately, or for package-level scope.
     ```go
     var message string
     message = "Hello"
     ```

---

## 5. String Formatting & Printing

* **Python (f-strings):**
  ```python
  message = f"Hi {name}, Welcome!"
  print(message)
  ```
* **Go (`fmt` package):**
  ```go
  // Formats and returns a string without printing
  message := fmt.Sprintf("Hi %v, Welcome!", name)

  // Prints directly to console (adds a newline at the end)
  fmt.Println(message)
  ```
  * `%v` is the "default value" placeholder in Go format strings. It formats any basic type
    automatically.

---

## 6. Reserved Keywords Caution

In Go, certain words are strictly reserved and **cannot** be used as identifiers (such as package
names or variable names).

* For example, **`go`** is a reserved keyword (used to launch goroutines). Writing `package go`
  at the top of a file will fail compilation with `expected 'IDENT', found 'go'`. Use `package main`
  for executable scripts instead.

---

## 7. Building a Web Server (`net/http`)

For web servers, Go's standard library `net/http` replaces the need for a micro-framework like
Flask or FastAPI for basic applications.

### A. Code Comparison: Go vs. Python (Flask)

| Go (`net/http`) | Python (`Flask`) | Notes |
| :--- | :--- | :--- |
| `func hello(w http.ResponseWriter, r *http.Request)` | `def hello(): return "Hello"` | Go passes response and request objects directly into the handler function. |
| `fmt.Fprint(w, "Hello")` | `return "Hello"` | In Go, you write directly to the connection writer stream `w`. |
| `http.HandleFunc("/route", hello)` | `@app.route("/route")` | Map paths to handlers. |
| `http.ListenAndServe(":8080", nil)` | `app.run(port=8080)` | Starts the HTTP server on port 8080. |

### B. Standard Go Conventions

1. **Short Variable Names (`w` and `r`)**:
   Unlike Python's preference for descriptive names (e.g., `request`, `response`), Go developers
   idiomatically use `w` for `http.ResponseWriter` and `r` for `*http.Request` in handler functions.
2. **Wildcard Routing**:
   A path like `"/"` acts as a subtree wildcard in Go. It catches any route that doesn't match a
   more specific pattern (e.g., hitting `/foo` will run the `/` handler).

### C. Advanced Concepts for Production

1. **Concurrency and State Safety**:
   * **Go**: Handles every incoming HTTP request on its own lightweight thread (**goroutine**).
   * **Python**: Typically relies on a single-threaded GIL and uses async or worker processes.
   * **Warning**: Because Go handlers run concurrently, reading/writing to shared state (like a
     standard Python `dict` / Go `map`) at the same time will cause a fatal runtime crash.
     Guard shared variables using synchronizers like `sync.Mutex`.

2. **Server Timeouts**:
   The default helper `http.ListenAndServe()` does not set timeouts. Always configure a custom
   `http.Server` with `ReadTimeout` and `WriteTimeout`.

---

## 8. Error Handling (Exceptions vs Explicit Return Values)

Python uses exception handling (`try...except`), while Go treats errors as first-class explicit return
values (`val, err := fn()`).

| Concept | Python | Go |
| :--- | :--- | :--- |
| **Control Flow** | `try...except Exception as e:` | `if err != nil { return err }` |
| **Sentinel Errors** | `raise ValueError("custom")` | `var ErrNotFound = errors.New("not found")` |
| **Error Wrapping** | `raise NewError() from e` | `fmt.Errorf("%w: failed", err)` |
| **Error Checking** | `isinstance(e, ValueError)` | `errors.Is(err, ErrNotFound)` |
| **Type Inspection** | `except CustomError as e:` | `var target *CustomError; errors.As(err, &target)` |

---

## 9. Structs & JSON Marshaling (Pydantic / Dicts vs Go Struct Tags)

In Python, JSON serialization uses `json.loads()` / `json.dumps()` or Pydantic models. Go uses
strongly-typed `struct` definitions with struct field tags.

### Struct Visibility & Tags

* **Exported Fields (Capitalized)**: Must start with a capital letter (e.g. `Username`) to be
  accessible by `encoding/json`.
* **Unexported Fields (Lowercase)**: Fields starting with lowercase (e.g. `password`) are omitted.
* **Struct Tags Syntax**:
  ```go
  type UserRequest struct {
      Username string   `json:"username"`        // Custom JSON key name
      Age      int      `json:"age,omitempty"`   // Omit if zero value (0)
      Password string   `json:"-"`               // Completely ignore in JSON
  }
  ```

---

## 10. HTTP REST API Error Responses & Protocols

* **Structured Error Output**: Return a standardized JSON model (`ErrorResponse`) with `error`,
  `code`, and optional `details`.
* **HTTP 405 Method Not Allowed**: Per RFC 9110, HTTP 405 responses MUST include an `Allow` header
  listing supported methods (e.g. `Allow: POST`).
* **`json.NewDecoder` Streaming**: Streaming request bytes directly via `json.NewDecoder(r.Body)`
  is more memory-efficient than reading full payloads into memory with `json.Unmarshal`.
