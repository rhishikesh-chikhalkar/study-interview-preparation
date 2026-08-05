# Go HTTP Middleware Chaining Guide

A comprehensive technical note and interview preparation reference covering HTTP middleware architecture, pattern design, custom response wrapping, context propagation, API key authentication, request logging, and middleware chain composition in Go.

---

## 🎯 1. Fundamental Middleware Architecture in Go

### The `http.Handler` Interface & `http.HandlerFunc`

In Go's standard `net/http` package, HTTP request processing centers on the `http.Handler` interface:

```go
type Handler interface {
    ServeHTTP(ResponseWriter, *Request)
}
```

The `http.HandlerFunc` type adapter allows ordinary functions with the signature `func(http.HandlerFunc)` to act as `http.Handler`s:

```go
type HandlerFunc func(ResponseWriter, *Request)

func (f HandlerFunc) ServeHTTP(w ResponseWriter, r *Request) {
    f(w, r)
}
```

### Middleware Constructor Pattern

A Go middleware is a higher-order function that accepts an `http.Handler` and returns a new `http.Handler`:

```go
type Middleware func(http.Handler) http.Handler

// Example idiomatic middleware constructor
func CustomMiddleware(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        // 1. Pre-processing (before target handler runs)
        
        // 2. Delegate execution to next handler in chain
        next.ServeHTTP(w, r)
        
        // 3. Post-processing (after target handler returns)
    })
}
```

---

## 🛠️ 2. Key Middleware Implementation Patterns

### A. Response Capturing Wrapper (`responseWriter`)

The standard `http.ResponseWriter` does not expose the HTTP status code or written byte count once `WriteHeader` or `Write` is invoked. To record status codes and response metrics (e.g. for logging or analytics), wrap `http.ResponseWriter`:

```go
type responseWriter struct {
    http.ResponseWriter
    statusCode int
    bytesWritten int64
    wroteHeader bool
}

func newResponseWriter(w http.ResponseWriter) *responseWriter {
    return &responseWriter{
        ResponseWriter: w,
        statusCode:     http.StatusOK, // Default to 200 OK
    }
}

func (rw *responseWriter) WriteHeader(code int) {
    if !rw.wroteHeader {
        rw.statusCode = code
        rw.wroteHeader = true
        rw.ResponseWriter.WriteHeader(code)
    }
}

func (rw *responseWriter) Write(b []byte) (int, error) {
    if !rw.wroteHeader {
        rw.WriteHeader(http.StatusOK)
    }
    n, err := rw.ResponseWriter.Write(b)
    rw.bytesWritten += int64(n)
    return n, err
}
```

### B. Context Propagation (`context.Context`)

Middleware often extracts request metadata (such as authenticated User IDs or Client Tenants) and passes it downstream safely using request context (`r.Context()`):

```go
type contextKey string

const (
    ClientIDKey contextKey = "clientID"
    UserRoleKey contextKey = "userRole"
)

// In Auth Middleware:
ctx := context.WithValue(r.Context(), ClientIDKey, clientID)
r = r.WithContext(ctx)
next.ServeHTTP(w, r)

// In Downstream Handler:
clientID, ok := r.Context().Value(ClientIDKey).(string)
if !ok {
    // Handle unauthenticated or missing context
}
```

> ⚠️ **Key Safety Rule**: Always define unexported custom type key aliases (e.g. `type contextKey string`) instead of plain strings (`"clientID"`) to avoid key collision across third-party packages.

### C. Logging Middleware

Logs HTTP method, URI path, client remote IP, response status code, latency, and response byte length:

```go
func LoggingMiddleware(logger *log.Logger) func(http.Handler) http.Handler {
    return func(next http.Handler) http.Handler {
        return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
            start := time.Now()
            rw := newResponseWriter(w)

            next.ServeHTTP(rw, r)

            duration := time.Since(start)
            logger.Printf(
                "[%s] %s %s %d %dB %v - Remote: %s",
                r.Method,
                r.URL.Path,
                r.Proto,
                rw.statusCode,
                rw.bytesWritten,
                duration,
                r.RemoteAddr,
            )
        })
    }
}
```

### D. Basic API Key Authentication Middleware

Validates an API key passed in the `X-API-Key` or `Authorization: Bearer` header. Short-circuits execution with `401 Unauthorized` if invalid:

```go
func APIKeyAuthMiddleware(validKeys map[string]string) func(http.Handler) http.Handler {
    return func(next http.Handler) http.Handler {
        return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
            apiKey := r.Header.Get("X-API-Key")
            if apiKey == "" {
                // Support Authorization: Bearer <key> fallback
                authHeader := r.Header.Get("Authorization")
                if strings.HasPrefix(authHeader, "Bearer ") {
                    apiKey = strings.TrimPrefix(authHeader, "Bearer ")
                }
            }

            clientName, exists := validKeys[apiKey]
            if apiKey == "" || !exists {
                w.Header().Set("Content-Type", "application/json")
                w.WriteHeader(http.StatusUnauthorized)
                json.NewEncoder(w).Encode(map[string]any{
                    "error": "Unauthorized",
                    "code":  http.StatusUnauthorized,
                    "details": "Invalid or missing API key",
                })
                return // Short-circuit: target handler will NOT be executed
            }

            // Pass identity downstream
            ctx := context.WithValue(r.Context(), ClientIDKey, clientName)
            next.ServeHTTP(w, r.WithContext(ctx))
        })
    }
}
```

---

## 🔗 3. Middleware Chaining Mechanics

### Manual Nesting vs. Variadic Composition

Manual middleware nesting becomes unreadable quickly:
```go
// Manual nesting (Hard to read and maintain)
handler := LoggingMiddleware(logger)(APIKeyAuthMiddleware(keys)(RecoveryMiddleware(targetHandler)))
```

### Variadic `Chain` Function

To compose middlewares in clean, left-to-right readable order (outermost to innermost):

```go
type Middleware func(http.Handler) http.Handler

// Chain applies middlewares in outermost-first execution order.
// Chain(h, m1, m2) yields: m1(m2(h))
func Chain(h http.Handler, middlewares ...Middleware) http.Handler {
    // Iterate backwards so that the first listed middleware becomes the outermost wrapper
    for i := len(middlewares) - 1; i >= 0; i-- {
        h = middlewares[i](h)
    }
    return h
}
```

### Execution Flow Diagram

```
[ Incoming Request ]
         │
         ▼
 ┌──────────────────────┐  (Pre-processing)
 │ LoggingMiddleware    │ ───► Starts timer, wraps ResponseWriter
 └──────────┬───────────┘
            │
            ▼
 ┌──────────────────────┐  (Pre-processing)
 │ APIKeyAuthMiddleware │ ───► Validates key; short-circuits if 401
 └──────────┬───────────┘
            │
            ▼
 ┌──────────────────────┐
 │ Target Handler       │ ───► Executes core domain business logic
 └──────────┬───────────┘
            │
            ▼
 ┌──────────────────────┐  (Post-processing)
 │ APIKeyAuthMiddleware │ ───► Returns back up stack
 └──────────┬───────────┘
            │
            ▼
 ┌──────────────────────┐  (Post-processing)
 │ LoggingMiddleware    │ ───► Calculates total latency & logs entry
 └──────────┬───────────┘
            │
            ▼
[ HTTP Response Sent ]
```

---

## ⚡ 4. Advanced Considerations & Production Best Practices

1. **Panic Recovery Middleware**: Always place a `RecoveryMiddleware` near the top of the chain to catch unexpected runtime panics and return a controlled `500 Internal Server Error` without crashing the HTTP server process.
2. **Sub-Router Middleware Scope**: Public routes (e.g. `/health`, `/metrics`, `/login`) should bypass auth middleware. Apply auth middleware selectively to protected sub-routers or specific handler chains rather than globally on `http.ServeMux`.
3. **Context Timeout Injection**: Use `context.WithTimeout` middleware for high-load APIs to enforce request deadlines and mitigate thread starvation from slow downstream dependencies.

---

## ❓ 5. Senior-Level Interview Questions & Detailed Answers

### 1. Conceptual / Theoretical

#### Q1: Explain how Go's `http.Handler` and `http.HandlerFunc` enable middleware chaining without external frameworks.
**Answer:**
Go achieves middleware chaining using higher-order functions leveraging the single-method `http.Handler` interface (`ServeHTTP(ResponseWriter, *Request)`). `http.HandlerFunc` acts as an adapter function type converting a plain function with signature `func(http.ResponseWriter, *Request)` into an `http.Handler`.

By defining a middleware as `func(http.Handler) http.Handler`, each middleware receives the next handler in the chain and returns a new `http.HandlerFunc`. When `ServeHTTP` is invoked on the outermost handler, control flows inward through pre-processing logic, enters the target handler, and unwinds back outward through post-processing logic. Because every middleware abides strictly by `http.Handler`, native standard library `net/http` handlers, third-party routers, and custom functions can be chained seamlessly without third-party dependencies.

**Follow-up Question:** What happens to heap allocations when chaining 10+ middlewares for every incoming HTTP request?
**Follow-up Answer:** If middleware functions construct new closure instances inside the request handler body, allocations occur per request. However, idiomatic Go middleware constructors initialize closures *once* during application initialization / router construction. During request execution, only minimal context and response wrapper structs are allocated on the stack/heap, keeping overhead negligible.

---

### 2. Practical / Scenario-Based

#### Q2: You need to log HTTP response status codes and byte sizes, but `http.ResponseWriter` doesn't provide getter methods for these fields. How do you implement this in Go middleware?
**Answer:**
We implement the Decorator design pattern by creating a custom struct (e.g., `responseWriter`) that embeds `http.ResponseWriter` and maintains internal fields for `statusCode` and `bytesWritten`. 

Because standard Go struct embedding forwards all un-implemented method calls to the inner `http.ResponseWriter`, we only need to intercept `WriteHeader(code int)` and `Write(b []byte) (int, error)`. In `WriteHeader`, we save the status code. In `Write`, we track accumulated byte lengths and ensure a default status code of `http.StatusOK` if `WriteHeader` was not explicitly called.

**Follow-up Question:** What issue occurs if the underlying `http.ResponseWriter` also implements `http.Flusher` or `http.Hijacker` when wrapped by your struct?
**Follow-up Answer:** Struct embedding hides optional interfaces like `http.Flusher`, `http.Pusher`, or `http.Hijacker`. If a downstream handler uses type assertion (`w.(http.Flusher)`), it will fail unless the wrapper explicitly implements those interfaces or type asserts the underlying `ResponseWriter` before delegating.

---

### 3. Coding / Implementation

#### Q3: Write a thread-safe `APIKeyAuthMiddleware` that authenticates requests via the `X-API-Key` header, injects the authenticated client name into `r.Context()`, and short-circuits with `401 Unauthorized` if invalid.

```go
package middleware

import (
	"context"
	"encoding/json"
	"net/http"
)

type contextKey string
const ClientKey contextKey = "authenticatedClient"

func APIKeyAuth(validKeys map[string]string) func(http.Handler) http.Handler {
	return func(next http.Handler) http.Handler {
		return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
			key := r.Header.Get("X-API-Key")
			clientName, valid := validKeys[key]
			if key == "" || !valid {
				w.Header().Set("Content-Type", "application/json")
				w.WriteHeader(http.StatusUnauthorized)
				json.NewEncoder(w).Encode(map[string]string{
					"error": "Unauthorized: invalid or missing X-API-Key header",
				})
				return // Short-circuit: do not call next.ServeHTTP
			}

			ctx := context.WithValue(r.Context(), ClientKey, clientName)
			next.ServeHTTP(w, r.WithContext(ctx))
		})
	}
}
```

**Follow-up Question:** Why do we use `r.WithContext(ctx)` instead of mutating the existing request context directly?
**Follow-up Answer:** Requests in Go (`*http.Request`) are immutable values regarding their context reference. `r.WithContext(ctx)` returns a shallow copy of `*http.Request` with the updated context pointer, maintaining concurrent safety and preventing side effects across asynchronous goroutines.

---

### 4. System Design & Architecture

#### Q4: How would you structure middleware layering in a microservice framework handling both public endpoints (health checks, login) and restricted tenant endpoints?

**Answer:**
In a production microservice, middleware should be layered hierarchically using sub-routers or middleware pipelines:

1. **Global Middleware Layer (Applied to ALL endpoints)**:
   - `PanicRecovery`: Prevents process crashes.
   - `RequestID`: Generates/propagates `X-Request-ID` tracing header.
   - `Logging & Metrics`: Captures total request throughput, latency, and status codes.
   - `CORS`: Standard browser cross-origin policy enforcement.

2. **Protected Sub-Router Layer (Applied ONLY to authenticated endpoints)**:
   - `APIKeyAuth` / `JWTAuth`: Validates credentials, extracts claims, injects tenant context.
   - `RateLimiter`: Per-tenant token bucket rate limiting based on authenticated tenant ID.
   - `RBAC / Authorization`: Checks user role permissions for specific endpoints.

```go
mainMux := http.NewServeMux()

// Public handlers wrapped only in global middlewares
publicChain := Chain(publicMux, RecoveryMiddleware, RequestIDMiddleware, LoggingMiddleware)

// Protected handlers wrapped in global + auth + rate limiter
protectedChain := Chain(protectedMux, RecoveryMiddleware, RequestIDMiddleware, LoggingMiddleware, AuthMiddleware, RateLimitMiddleware)
```

**Follow-up Question:** How do you handle distributed tracing across middleware chains in microservices?
**Follow-up Answer:** Tracing middleware (e.g. OpenTelemetry) extracts trace context headers (`traceparent`, `tracestate`) from incoming request headers, starts a span, attaches the span to `r.Context()`, updates response headers with trace IDs, and records status/errors before completing the span when the response unwinds.
