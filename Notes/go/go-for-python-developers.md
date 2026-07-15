# Go for Python Developers

A quick reference guide comparing Go concepts to Python concepts, tailored for developers transitioning from Python to Go.

---

## 1. Project Organization & Scope

In Python, every `.py` file is a self-contained module. In Go, compilation works on a **directory-level** package system.

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

In Go, having two files in the same directory with their own `func main()` will cause a compiler error (`main redeclared in this block`). Instead, structure them in subdirectories:
```
my_project/
├── hello/
│   └── hello.go  // package main, contains func main()
└── add_two_numbers/
    └── add_two_numbers.go  // package main, contains func main()
```

---

## 2. Loop Syntax

Go only has one looping keyword: `for`. It is used for all types of loops (ranges, condition-based, infinite, and collection iteration).

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
