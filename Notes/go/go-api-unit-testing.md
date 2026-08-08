# Unit Testing Go REST APIs with Standard Library (`testing` & `net/http/httptest`)

A comprehensive guide and interview reference for unit testing Go HTTP web APIs using Go's
built-in `testing` and `net/http/httptest` packages.

---

## 1. Core Architecture & Testing Primitives

Go standard library provides all essential utilities required to test HTTP services without
relying on external third-party testing frameworks or mock libraries.

### Key Packages
- `testing`: Standard testing library providing test runner `t *testing.T`, subtests
  (`t.Run`), assertions, and benchmarking (`testing.B`).
- `net/http/httptest`: Utilities specifically designed for HTTP server and client testing.
  - `httptest.NewRecorder()`: Implements `http.ResponseWriter` to record status codes,
    headers, and body outputs in memory.
  - `httptest.NewRequest(method, target, body)`: Generates an `*http.Request` initialized for
    testing.
  - `httptest.NewServer(handler)`: Spawns an ephemeral local HTTP server on a random port for
    end-to-end handler or client testing.

---

## 2. Testing HTTP Handlers with `httptest.ResponseRecorder`

Instead of spinning up a live network port, unit testing HTTP handler functions directly
invokes the `http.Handler` or `http.HandlerFunc` with a synthetic request and response
recorder.

### Basic Handler Test Execution Flow

```go
func TestPingHandler_Basic(t *testing.T) {
	// 1. Create synthetic HTTP GET request
	req := httptest.NewRequest(http.MethodGet, "/ping", nil)

	// 2. Create ResponseRecorder to capture response data
	rr := httptest.NewRecorder()

	// 3. Call handler directly
	pingHandler(rr, req)

	// 4. Assert HTTP status code
	if rr.Code != http.StatusOK {
		t.Errorf("got status %d, want %d", rr.Code, http.StatusOK)
	}

	// 5. Assert Response Headers
	contentType := rr.Header().Get("Content-Type")
	if contentType != "application/json" {
		t.Errorf("got Content-Type %s, want application/json", contentType)
	}
}
```

---

## 3. Table-Driven Testing Pattern for Go HTTP APIs

Table-driven testing is the idiomatic Go pattern for testing multiple inputs, HTTP methods,
edge cases, and error conditions against a single endpoint handler.

### Table-Driven Test Structure for Multi-Route API

```go
func TestUsersHandler_TableDriven(t *testing.T) {
	tests := []struct {
		name           string
		method         string
		body           string
		expectedStatus int
		checkResponse  func(t *testing.T, body string)
	}{
		{
			name:           "Valid Adult User Creation",
			method:         http.MethodPost,
			body:           `{"username":"gopher","email":"gopher@go.dev","age":25}`,
			expectedStatus: http.StatusCreated,
			checkResponse: func(t *testing.T, body string) {
				var resp UserResponse
				if err := json.Unmarshal([]byte(body), &resp); err != nil {
					t.Fatalf("failed to decode JSON response: %v", err)
				}
				if !resp.IsAdult {
					t.Errorf("expected IsAdult to be true for age 25")
				}
			},
		},
		{
			name:           "Missing Required Username",
			method:         http.MethodPost,
			body:           `{"email":"gopher@go.dev","age":25}`,
			expectedStatus: http.StatusBadRequest,
			checkResponse: func(t *testing.T, body string) {
				var errResp ErrorResponse
				if err := json.Unmarshal([]byte(body), &errResp); err != nil {
					t.Fatalf("failed to decode error JSON: %v", err)
				}
				if errResp.Error != "Validation Error" {
					t.Errorf("got error %s, want Validation Error", errResp.Error)
				}
			},
		},
		{
			name:           "Method Not Allowed (GET)",
			method:         http.MethodGet,
			body:           "",
			expectedStatus: http.StatusMethodNotAllowed,
			checkResponse: func(t *testing.T, body string) {
				// Assert RFC compliance (Allow header MUST be set for 405 status)
			},
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			req := httptest.NewRequest(tt.method, "/users", strings.NewReader(tt.body))
			rr := httptest.NewRecorder()

			usersHandler(rr, req)

			if rr.Code != tt.expectedStatus {
				t.Errorf("got status %d, want %d", rr.Code, tt.expectedStatus)
			}

			if tt.checkResponse != nil {
				tt.checkResponse(t, rr.Body.String())
			}
		})
	}
}
```

---

## 4. Best Practices & Common Pitfalls

1. **Test Full Middleware & Routing Chains**:
   - Testing handler functions in isolation tests logic but bypasses routing rules, context
     injection, and logging middleware.
   - Solution: Pass `httptest.NewRequest` to your configured `http.ServeMux` or router
     (`mux.ServeHTTP(rr, req)`).

2. **Verify Headers & RFC Compliance**:
   - Check `Content-Type: application/json`.
   - Verify `Allow` header presence on HTTP 405 Method Not Allowed responses.

3. **In-Memory Body Cleanup**:
   - `httptest.NewRequest` automatically provides a readable `io.Reader` for `r.Body`.
     In handlers under test, ensure `r.Body.Close()` is called to prevent resource leaks in
     production.

4. **Isolate External Dependencies via Interfaces**:
   - Inject repository or service interfaces into handler structs to substitute mock
     implementations during unit testing without real database access.

---

## 5. Interview Questions & Answers (5 YOE IT Professional Level)

### Question 1 (Conceptual)
Why use `httptest.NewRecorder()` instead of starting a live server with `http.ListenAndServe`
during unit tests?

**Answer**:
`httptest.NewRecorder()` operates entirely in-memory without allocating network sockets or
ports. This provides three major advantages:
1. **Speed**: Eliminates network TCP handshake overhead and socket creation latency, allowing
   thousands of unit tests to execute in milliseconds.
2. **Determinism & Parallelism**: Avoids port collision issues when running tests
   concurrently (`go test -parallel`).
3. **Isolation**: Tests focus directly on HTTP handler business logic, status codes, and header
   generation without external network noise.

*Follow-up Question*: When *should* you use `httptest.NewServer()` instead of
`httptest.NewRecorder()`?

*Follow-up Answer*: Use `httptest.NewServer()` when testing HTTP client code (e.g. custom SDKs or
external REST client integrations), or when testing complex middleware that relies on full HTTP
protocol transport behavior (such as HTTP/2 framing, connection hijacking, or chunked transfer
encoding).

---

### Question 2 (Practical / Scenario)
How do you unit test an HTTP endpoint that relies on a database service without hitting a real
database?

**Answer**:
Decouple handler implementation from database concrete types by introducing a Go interface:

```go
type UserService interface {
	GetUser(ctx context.Context, id string) (*User, error)
}

type UserHandler struct {
	Service UserService
}

func (h *UserHandler) ServeHTTP(w http.ResponseWriter, r *http.Request) {
	// Uses h.Service.GetUser(...)
}
```

In unit tests, implement a mock struct satisfying `UserService`:

```go
type MockUserService struct {
	GetUserFn func(ctx context.Context, id string) (*User, error)
}

func (m *MockUserService) GetUser(ctx context.Context, id string) (*User, error) {
	return m.GetUserFn(ctx, id)
}
```

This allows defining dynamic return values or error conditions per subtest without requiring
external database containers or network calls.

*Follow-up Question*: How do you test context cancellation or request timeouts in handlers?

*Follow-up Answer*: Pass a context with deadline or cancellation (`context.WithTimeout`) to
`httptest.NewRequest(method, target, body).WithContext(ctx)` and verify that the handler responds
with `http.StatusGatewayTimeout` or `499 Client Closed Request`.

---

### Question 3 (Coding / Implementation)
Write a test checking that a POST route correctly returns `400 Bad Request` when sent invalid JSON
and `405 Method Not Allowed` when called via GET.

**Answer**:

```go
func TestEchoHandler_ValidationAndMethodNotAllowed(t *testing.T) {
	t.Run("Invalid JSON Payload", func(t *testing.T) {
		req := httptest.NewRequest(http.MethodPost, "/echo", strings.NewReader("{malformed}"))
		rr := httptest.NewRecorder()

		echoHandler(rr, req)

		if rr.Code != http.StatusBadRequest {
			t.Errorf("got status %d, want %d", rr.Code, http.StatusBadRequest)
		}
	})

	t.Run("Method Not Allowed", func(t *testing.T) {
		req := httptest.NewRequest(http.MethodGet, "/echo", nil)
		rr := httptest.NewRecorder()

		echoHandler(rr, req)

		if rr.Code != http.StatusMethodNotAllowed {
			t.Errorf("got status %d, want %d", rr.Code, http.StatusMethodNotAllowed)
		}
		if allow := rr.Header().Get("Allow"); allow != http.MethodPost {
			t.Errorf("got Allow header %s, want POST", allow)
		}
	})
}
```

*Follow-up Question*: How do you inspect and validate structured JSON error response bodies
returned by `rr.Body`?

*Follow-up Answer*: Unmarshal `rr.Body.Bytes()` into a response struct (e.g. `ErrorResponse`)
or `map[string]any` and perform assertions on the error code, error message, and detail fields.

---

### Question 4 (System Design / Architecture)
How do you structure unit, integration, and end-to-end (E2E) testing strategy for a microservice
architecture in Go?

**Answer**:
A robust Go microservice testing strategy follows the testing pyramid:
1. **Unit Tests (`main_test.go`, `*_test.go`)**:
   - Focus on isolated domain logic, handlers (`httptest.ResponseRecorder`), and utilities.
   - Use table-driven tests and interfaces/mocks. Fast execution (<1s).
2. **Integration Tests (`go test -tags=integration ./...`)**:
   - Use Go build tags (`//go:build integration`).
   - Run real dependencies in Docker containers (e.g. Testcontainers-go or Postgres/Redis).
   - Test full router setups (`mux.ServeHTTP`), middleware chains, database queries, and cache
     behavior.
3. **End-to-End Smoke Tests (`httptest.NewServer` or Staging Deployment)**:
   - Verify external API contracts, auth workflows, and multi-service event streaming pipelines.

*Follow-up Question*: How do you prevent integration tests from running during quick unit passes?

*Follow-up Answer*: Use Go build tags like `//go:build integration` at the top of test files and
execute unit tests using standard `go test ./...`. Integration tests are triggered explicitly via
`go test -tags=integration ./...`.

---

## 6. Official References & Documentation
- [Go `testing` Package Documentation](https://pkg.go.dev/testing)
- [Go `net/http/httptest` Package Documentation](https://pkg.go.dev/net/http/httptest)
- [Go Wiki: TableDrivenTests](https://github.com/golang/go/wiki/TableDrivenTests)
