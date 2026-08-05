package main

import (
	"context"
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"os"
	"runtime/debug"
	"strings"
	"time"
)

// contextKey defines a custom unexported type for request context keys.
type contextKey string

const (
	// ClientNameKey is the context key for storing authenticated client name.
	ClientNameKey contextKey = "clientName"
)

// responseWriter wraps standard http.ResponseWriter to capture status and bytes.
type responseWriter struct {
	http.ResponseWriter
	statusCode   int
	bytesWritten int64
	wroteHeader  bool
}

func newResponseWriter(w http.ResponseWriter) *responseWriter {
	return &responseWriter{
		ResponseWriter: w,
		statusCode:     http.StatusOK,
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

// Middleware defines an HTTP middleware function signature.
type Middleware func(http.Handler) http.Handler

// Chain combines multiple middlewares into a single http.Handler.
// Middlewares are executed in the order provided (left-to-right / outer-to-inner).
func Chain(h http.Handler, middlewares ...Middleware) http.Handler {
	for i := len(middlewares) - 1; i >= 0; i-- {
		h = middlewares[i](h)
	}
	return h
}

// respondJSON writes a structured JSON payload with status code.
func respondJSON(w http.ResponseWriter, status int, payload any) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(status)
	if err := json.NewEncoder(w).Encode(payload); err != nil {
		log.Printf("error encoding JSON response: %v", err)
	}
}

// LoggingMiddleware logs request metadata, HTTP status code, and latency.
func LoggingMiddleware(logger *log.Logger) Middleware {
	return func(next http.Handler) http.Handler {
		return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
			start := time.Now()
			rw := newResponseWriter(w)

			next.ServeHTTP(rw, r)

			duration := time.Since(start)
			logger.Printf(
				"[%s] %s %s %d %dB %v",
				r.Method,
				r.URL.Path,
				r.Proto,
				rw.statusCode,
				rw.bytesWritten,
				duration,
			)
		})
	}
}

// APIKeyAuthMiddleware verifies API keys against validKeys map.
func APIKeyAuthMiddleware(validKeys map[string]string) Middleware {
	return func(next http.Handler) http.Handler {
		return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
			key := r.Header.Get("X-API-Key")
			if key == "" {
				authHeader := r.Header.Get("Authorization")
				if strings.HasPrefix(authHeader, "Bearer ") {
					key = strings.TrimPrefix(authHeader, "Bearer ")
				}
			}

			clientName, valid := validKeys[key]
			if key == "" || !valid {
				respondJSON(
					w,
					http.StatusUnauthorized,
					map[string]any{
						"error":   "Unauthorized",
						"code":    http.StatusUnauthorized,
						"details": "Invalid or missing API key",
					},
				)
				return
			}

			ctx := context.WithValue(r.Context(), ClientNameKey, clientName)
			next.ServeHTTP(w, r.WithContext(ctx))
		})
	}
}

// RecoveryMiddleware handles panics in HTTP handlers and returns 500.
func RecoveryMiddleware(logger *log.Logger) Middleware {
	return func(next http.Handler) http.Handler {
		return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
			defer func() {
				if err := recover(); err != nil {
					logger.Printf(
						"PANIC RECOVERED: %v\nStack: %s",
						err,
						string(debug.Stack()),
					)
					respondJSON(
						w,
						http.StatusInternalServerError,
						map[string]any{
							"error":   "Internal Server Error",
							"code":    http.StatusInternalServerError,
							"details": "An unexpected error occurred",
						},
					)
				}
			}()
			next.ServeHTTP(w, r)
		})
	}
}

// Handlers
func healthHandler(w http.ResponseWriter, r *http.Request) {
	respondJSON(w, http.StatusOK, map[string]string{
		"status": "healthy",
		"time":   time.Now().UTC().Format(time.RFC3339),
	})
}

func dataHandler(w http.ResponseWriter, r *http.Request) {
	clientName, ok := r.Context().Value(ClientNameKey).(string)
	if !ok {
		clientName = "unknown"
	}

	respondJSON(w, http.StatusOK, map[string]any{
		"message": fmt.Sprintf("Hello %s, access granted!", clientName),
		"items":   []string{"item1", "item2", "item3"},
	})
}

func panicHandler(w http.ResponseWriter, r *http.Request) {
	panic("simulated critical unexpected error")
}

func setupRoutes(logger *log.Logger, validKeys map[string]string) http.Handler {
	mux := http.NewServeMux()

	// Public routes
	healthChain := Chain(
		http.HandlerFunc(healthHandler),
		RecoveryMiddleware(logger),
		LoggingMiddleware(logger),
	)
	mux.Handle("/health", healthChain)

	// Protected data route
	dataChain := Chain(
		http.HandlerFunc(dataHandler),
		RecoveryMiddleware(logger),
		LoggingMiddleware(logger),
		APIKeyAuthMiddleware(validKeys),
	)
	mux.Handle("/api/v1/data", dataChain)

	// Protected panic route for testing recovery
	panicChain := Chain(
		http.HandlerFunc(panicHandler),
		RecoveryMiddleware(logger),
		LoggingMiddleware(logger),
		APIKeyAuthMiddleware(validKeys),
	)
	mux.Handle("/api/v1/panic", panicChain)

	return mux
}

func main() {
	logger := log.New(os.Stdout, "[SERVER] ", log.LstdFlags)
	validKeys := map[string]string{
		"secret-key-123": "AcmeCorp",
		"secret-key-456": "BetaInc",
	}

	handler := setupRoutes(logger, validKeys)

	fmt.Println("Server starting on port 8080...")
	if err := http.ListenAndServe(":8080", handler); err != nil {
		logger.Fatalf("Server failed: %v", err)
	}
}
