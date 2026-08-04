# Go Error Handling, Structs, and JSON REST API Guide

A comprehensive study note and interview reference covering idiomatic Go error handling, struct field
visibility, JSON tags, HTTP REST protocols, and handler unit testing.

---

## 🎯 1. Go Error Handling Architecture

Go does not use exception handling (`try/catch`). Functions return errors explicitly as return values:
```go
val, err := parseJSONBody(r, &req)
if err != nil {
    // Handle error explicitly
}
```

### Key Principles

1. **Sentinel Errors**: Declared at the package level for constant comparison.
   ```go
   var ErrInvalidJSON = errors.New("malformed or invalid JSON payload")
   ```
2. **Error Wrapping (`fmt.Errorf("%w")`)**: Wraps an underlying error while retaining its cause.
   ```go
   return fmt.Errorf("%w: syntax error at byte offset %d", ErrInvalidJSON, syntaxErr.Offset)
   ```
3. **`errors.Is(err, target)`**: Checks if `target` exists anywhere in the error chain.
   ```go
   if errors.Is(err, ErrInvalidJSON) {
       respondWithError(w, http.StatusBadRequest, "Invalid JSON", err.Error())
   }
   ```
4. **`errors.As(err, &target)`**: Unwraps and extracts concrete error types.
   ```go
   var syntaxErr *json.SyntaxError
   if errors.As(err, &syntaxErr) {
       log.Printf("Syntax error offset: %d", syntaxErr.Offset)
   }
   ```

---

## 🧩 2. Structs & JSON Field Tags

### Field Capitalization (Visibility)
- **Exported (Capitalized)**: `Username string` -> Visible to `encoding/json`.
- **Unexported (Lowercase)**: `password string` -> Ignored by `encoding/json`.

### Tag Options Syntax
```go
type UserRequest struct {
    Username string   `json:"username"`        // Custom JSON key name
    Email    string   `json:"email"`           // Custom JSON key name
    Age      int      `json:"age,omitempty"`   // Omit if zero value (0)
    Roles    []string `json:"roles,omitempty"` // Omit if nil/empty slice
    Password string   `json:"-"`               // Completely exclude from JSON
}
```

> ⚠️ **`omitempty` Pitfall**: Primitive zero values (`0`, `false`, `""`) are omitted when `omitempty` is
> set. Use pointer types (e.g. `*int`, `*bool`) to differentiate between missing fields (`nil`) and
> valid zero values (`0`).

---

## 🌐 3. REST API Protocols & Status Codes

- **`200 OK`**: Standard success response for queries/updates.
- **`201 Created`**: Standard response when a new entity (e.g. User) is created.
- **`400 Bad Request`**: Client input validation or malformed syntax failure.
- **`405 Method Not Allowed`**: Per RFC 9110, HTTP 405 MUST include an `Allow` header listing allowed
  HTTP methods (e.g., `w.Header().Set("Allow", "POST")`).

---

## ⚡ 4. JSON Decoder vs Unmarshal

- **`json.NewDecoder(r.Body)`**: Streams data directly from an `io.Reader`. Memory efficient.
- **`DisallowUnknownFields()`**: Configures decoder to reject unexpected JSON fields.
- **`json.Unmarshal([]byte)`**: Best when payload bytes are already loaded in memory.

---

## 🧪 5. Unit Testing HTTP Handlers (`net/http/httptest`)

- **`httptest.NewRecorder()`**: Implements `http.ResponseWriter` to record status, headers, and body.
- **`httptest.NewRequest()`**: Creates synthetic `*http.Request` instances for testing.
```go
req := httptest.NewRequest("POST", "/users", strings.NewReader(`{"username":"gopher"}`))
rr := httptest.NewRecorder()
usersHandler(rr, req)
```
