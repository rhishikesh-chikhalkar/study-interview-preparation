# Go REST API Implementation

This directory contains a production-ready, concurrent Go REST API built using only the standard library (`net/http`). 

It provides two endpoints and is fully tested with unit tests using Go's built-in `testing` and `net/http/httptest` packages.

---

## 📂 Project Structure

- [main.go](file:///Users/rhishikesh/GITHUB/study-interview-preparation/golang/rest_api/main.go): Core server setup and HTTP handler functions.
- [main_test.go](file:///Users/rhishikesh/GITHUB/study-interview-preparation/golang/rest_api/main_test.go): Comprehensive table-driven and unit tests for the handlers.
- [go.mod](file:///Users/rhishikesh/GITHUB/study-interview-preparation/golang/rest_api/go.mod): Go module declaration.

---

## 🚀 Endpoints & Implementation Details

### 1. `GET /ping`
- **Purpose**: A health-check endpoint.
- **Method Allowed**: `GET` (returns `405 Method Not Allowed` for any other method).
- **Response Format**: `application/json`
- **Payload**:
  ```json
  {
    "message": "pong"
  }
  ```

### 2. `POST /echo`
- **Purpose**: Echoes back any valid received JSON payload.
- **Method Allowed**: `POST` (returns `405 Method Not Allowed` for any other method).
- **JSON Validation**: Checks if the request body is valid JSON using `json.Unmarshal` into `json.RawMessage`. If invalid, returns a `400 Bad Request` with `{"error": "Invalid JSON"}`.
- **Response Format**: `application/json`
- **Payload**: Echoes the exact bytes of the received request body.

---

## 🛠️ How to Run

From this directory, run:
```bash
go run main.go
```
The server will start on port `8080`.

### Testing with `curl`

**1. Ping Health Check:**
```bash
curl -i http://localhost:8080/ping
```

**2. Echo JSON Payload:**
```bash
curl -i -X POST http://localhost:8080/echo \
  -H "Content-Type: application/json" \
  -d '{"name": "Gopher", "role": "Developer"}'
```

**3. Test Method Not Allowed (GET on /echo):**
```bash
curl -i http://localhost:8080/echo
```

---

## 🧪 Running Tests

Go provides robust tooling for testing HTTP handlers in the standard library. Run the suite using:
```bash
go test -v .
```

### What is covered?
- **`TestPingHandler`**: Verifies that `GET /ping` returns status `200 OK` with `{"message": "pong"}` and `Content-Type: application/json`.
- **`TestEchoHandler_ValidJSON`**: Verifies that a valid JSON payload sent via `POST` is correctly echoed back with status `200 OK`.
- **`TestEchoHandler_InvalidJSON`**: Verifies that invalid JSON payload returns status `400 Bad Request`.

### Key Go Testing Concepts Utilized
- **`httptest.NewRecorder()`**: A mock response writer that implements the `http.ResponseWriter` interface to capture response headers, status codes, and bodies without spinning up an actual network socket.
- **`http.HandlerFunc()`**: Casts the raw handler function to wrap it as a handler, exposing the `ServeHTTP(w, r)` method.
