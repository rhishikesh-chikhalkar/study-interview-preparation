# Idiomatic Go REST API & JSON Struct Marshaling

This directory contains a production-ready REST API built using standard Go (`net/http`, `encoding/json`).

---

## 🚀 Key Features Demonstrated

- **Go Struct Design & Visibility**: Exported vs unexported fields and struct field tags.
- **JSON Marshaling & Unmarshaling**: Decoding request streams into structs and encoding structured JSON responses.
- **Idiomatic Go Error Handling**: Sentinel errors, error wrapping (`fmt.Errorf("%w")`), and inspection (`errors.Is`, `errors.As`).
- **REST Protocol Standards**: Appropriate HTTP status codes (`200`, `201`, `400`, `405`) and response headers (`Content-Type`, `Allow`).
- **Table-Driven HTTP Testing**: Unit testing handlers with `net/http/httptest`.

---

## 📌 Important Notes & Interview Study Guide

### 1. Go Structs & Field Visibility
- **Exported Fields (Capitalized)**: Only fields starting with an uppercase letter (e.g. `Username`) are visible outside the package and can be encoded/decoded by `encoding/json`.
- **Unexported Fields (Lowercase)**: Fields starting with a lowercase letter (e.g. `password`) are ignored by `encoding/json`.

### 2. JSON Struct Tag Options
- `json:"name"`: Customizes the JSON key name.
- `json:",omitempty"`: Omits the field from output JSON if its value is the Go zero value (`0`, `""`, `false`, `nil`).
- **Gotcha with `omitempty`**: If `0` or `false` is a valid distinct value (e.g. `Age = 0` for an infant), using `omitempty` with primitive types will omit `0`. Use pointer types (e.g. `*int`) to distinguish missing fields (`nil`) from zero values (`0`).
- `json:"-"`: Instructs `encoding/json` to completely ignore this struct field (useful for sensitive internal state or unmarshaled tokens).

### 3. Go Error Handling Best Practices
- **Sentinel Errors**: Pre-declared package variables (e.g. `var ErrEmptyBody = errors.New(...)`) allow direct comparison.
- **Error Wrapping (`fmt.Errorf("%w", err)`)**: Preserves the cause chain so callers can inspect nested errors.
- **`errors.Is(err, target)`**: Always use `errors.Is` instead of `err == target` when errors might be wrapped.
- **`errors.As(err, &target)`**: Unwraps and extracts concrete error types (e.g. `*json.SyntaxError` or `*json.UnmarshalTypeError`).

### 4. `json.NewDecoder` vs `json.Unmarshal`
- **`json.NewDecoder(r.Body)`**: Streams data directly from an `io.Reader` without buffering the entire payload into RAM first. Ideal for HTTP request bodies.
- **`DisallowUnknownFields()`**: Configures the decoder to reject request payloads containing unexpected JSON keys, enforcing strict API schemas.
- **`json.Unmarshal([]byte)`**: Best suited when the entire byte slice is already loaded in memory.

### 5. HTTP Status Codes & REST Conventions
- **`200 OK`**: Standard response for successful GET/POST requests.
- **`201 Created`**: Standard response when a new resource (e.g. User) is successfully created.
- **`400 Bad Request`**: Indicates client-side payload syntax or validation errors.
- **`405 Method Not Allowed`**: Returned when an HTTP method is unsupported. Per RFC 9110, HTTP 405 responses MUST include an `Allow` header listing supported methods (e.g. `Allow: POST`).

### 6. HTTP Unit Testing with `httptest`
- **`httptest.NewRecorder()`**: A mock response writer implementing `http.ResponseWriter` that captures status codes, headers, and body bytes without opening a network socket.
- **`httptest.NewRequest()`**: Creates synthetic `*http.Request` objects for table-driven testing.

---

## 🧩 Struct Tag Syntax Example

```go
type UserRequest struct {
    Username string   `json:"username"`        // Key "username"
    Email    string   `json:"email"`           // Key "email"
    Age      int      `json:"age,omitempty"`   // Omits if 0
    Roles    []string `json:"roles,omitempty"` // Omits if empty
    Secret   string   `json:"-"`               // Ignored in JSON
}
```

---

## 🚀 API Endpoints

### 1. `POST /users` (Structured Creation & Validation)
- **Method Allowed**: `POST`
- **Request Body**:
  ```json
  {
    "username": "gopher",
    "email": "gopher@go.dev",
    "age": 25,
    "roles": ["admin"]
  }
  ```
- **Response (`201 Created`)**:
  ```json
  {
    "id": "usr_101",
    "username": "gopher",
    "email": "gopher@go.dev",
    "is_adult": true,
    "roles": ["admin"],
    "created_at": "2026-08-04T13:10:00Z",
    "status": "active"
  }
  ```
- **Validation Error (`400 Bad Request`)**:
  ```json
  {
    "error": "Validation Error",
    "code": 400,
    "details": "username is required"
  }
  ```

### 2. `GET /ping`
- **Method Allowed**: `GET`
- **Response (`200 OK`)**: `{"message": "pong"}`

### 3. `POST /echo`
- **Method Allowed**: `POST`
- **Response (`200 OK`)**: Echoes validated raw JSON body.

---

## 🧪 Testing & Execution

### Run Server
```bash
go run main.go
```

### Run Tests & Static Analysis
```bash
go test -v ./...
go vet ./...
```

### Sample `curl` Command
```bash
curl -i -X POST http://localhost:8080/users \
  -H "Content-Type: application/json" \
  -d '{"username":"gopher","email":"gopher@go.dev","age":25}'
```
