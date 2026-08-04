# Idiomatic Go Error Handling & REST API

This directory demonstrates production-grade, idiomatic Go error handling and standardized HTTP
responses using Go's standard library (`net/http`, `errors`, `fmt`, `encoding/json`).

---

## 💡 Key Go Error Handling Patterns

### 1. Sentinel Errors
Sentinel errors are pre-declared, package-level error variables used for constant error comparison.
```go
var (
    ErrMethodNotAllowed = errors.New("method not allowed")
    ErrEmptyBody        = errors.New("request body cannot be empty")
    ErrInvalidJSON      = errors.New("malformed or invalid JSON payload")
)
```

### 2. Error Wrapping with `%w`
Go 1.13+ allows wrapping an error inside another error using `fmt.Errorf("%w", err)`. This preserves
the underlying cause so callers can inspect error trees:
```go
return fmt.Errorf("%w: syntax error at byte offset %d", ErrInvalidJSON, syntaxErr.Offset)
```

### 3. Error Inspection (`errors.Is` and `errors.As`)
- **`errors.Is(err, target)`**: Checks if `target` exists anywhere in `err`'s wrapping chain.
```go
if errors.Is(err, ErrEmptyBody) {
    // Handle empty body error
}
```
- **`errors.As(err, &target)`**: Unwraps `err` until it matches the type of `target` and binds it.
```go
var syntaxErr *json.SyntaxError
if errors.As(err, &syntaxErr) {
    log.Printf("Syntax error at offset %d", syntaxErr.Offset)
}
```

---

## 🏗️ Standardized API Error Response

All API errors return a consistent, structured JSON payload:
```json
{
  "error": "Invalid JSON",
  "code": 400,
  "details": "malformed or invalid JSON payload: syntax error at byte offset 8"
}
```

### Response Helper Functions
- **`respondJSON(w, status, payload)`**: Encodes payload to JSON and sets `Content-Type`.
- **`respondWithError(w, status, message, details)`**: Formats an `ErrorResponse` and sends JSON.

---

## 🚀 API Endpoints

### 1. `GET /ping`
- **Method Allowed**: `GET`
- **Success (`200 OK`)**:
  ```json
  {"message": "pong"}
  ```
- **Error (`405 Method Not Allowed`)**: Sets `Allow: GET` header and returns JSON error.

### 2. `POST /echo`
- **Method Allowed**: `POST`
- **Success (`200 OK`)**: Echoes validated JSON payload.
- **Error (`400 Bad Request`)**: Returned when body is empty or malformed JSON.
- **Error (`405 Method Not Allowed`)**: Sets `Allow: POST` header and returns JSON error.

---

## 🧪 Testing & Verification

Run tests and static analysis:
```bash
go test -v ./...
go vet ./...
```

### Test Coverage Highlights
- **Table-Driven Tests**: Efficient test matrices for status codes, headers, and bodies.
- **Error Unwrapping Tests**: Verifies `errors.Is(err, ErrInvalidJSON)` for decoder failures.
