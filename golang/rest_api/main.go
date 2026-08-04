package main

import (
	"encoding/json"
	"errors"
	"fmt"
	"io"
	"log"
	"net/http"
	"time"
)

// Sentinel errors representing common API failure cases.
var (
	ErrMethodNotAllowed = errors.New("method not allowed")
	ErrEmptyBody        = errors.New("request body cannot be empty")
	ErrInvalidJSON      = errors.New("malformed or invalid JSON payload")
)

// ErrorResponse represents a standardized JSON error response structure.
type ErrorResponse struct {
	Error   string `json:"error"`
	Code    int    `json:"code"`
	Details string `json:"details,omitempty"`
}

// respondJSON writes a structured JSON payload with the given HTTP status code.
func respondJSON(w http.ResponseWriter, status int, payload any) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(status)
	if err := json.NewEncoder(w).Encode(payload); err != nil {
		log.Printf("error encoding JSON response: %v", err)
	}
}

// respondWithError writes a standardized JSON error response.
func respondWithError(w http.ResponseWriter, status int, message string, details string) {
	resp := ErrorResponse{
		Error:   message,
		Code:    status,
		Details: details,
	}
	respondJSON(w, status, resp)
}

// parseJSONBody parses and validates a JSON request body into target struct/raw message.
// Demonstrates Go error wrapping and errors.As / errors.Is usage.
func parseJSONBody(r *http.Request, v any) error {
	if r.Body == nil {
		return ErrEmptyBody
	}
	defer r.Body.Close()

	decoder := json.NewDecoder(r.Body)
	decoder.DisallowUnknownFields()

	if err := decoder.Decode(v); err != nil {
		var syntaxErr *json.SyntaxError
		var unmarshalErr *json.UnmarshalTypeError
		switch {
		case errors.Is(err, io.EOF):
			return ErrEmptyBody
		case errors.As(err, &syntaxErr):
			return fmt.Errorf(
				"%w: syntax error at byte offset %d",
				ErrInvalidJSON,
				syntaxErr.Offset,
			)
		case errors.As(err, &unmarshalErr):
			return fmt.Errorf(
				"%w: invalid type for field '%s'",
				ErrInvalidJSON,
				unmarshalErr.Field,
			)
		default:
			return fmt.Errorf("%w: %v", ErrInvalidJSON, err)
		}
	}
	return nil
}

func pingHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodGet {
		w.Header().Set("Allow", http.MethodGet)
		respondWithError(
			w,
			http.StatusMethodNotAllowed,
			http.StatusText(http.StatusMethodNotAllowed),
			fmt.Sprintf("method %s is not allowed on /ping", r.Method),
		)
		return
	}
	respondJSON(w, http.StatusOK, map[string]string{"message": "pong"})
}

func echoHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		w.Header().Set("Allow", http.MethodPost)
		respondWithError(
			w,
			http.StatusMethodNotAllowed,
			http.StatusText(http.StatusMethodNotAllowed),
			fmt.Sprintf("method %s is not allowed on /echo", r.Method),
		)
		return
	}

	var payload json.RawMessage
	if err := parseJSONBody(r, &payload); err != nil {
		if errors.Is(err, ErrEmptyBody) {
			respondWithError(
				w,
				http.StatusBadRequest,
				"Bad Request",
				err.Error(),
			)
			return
		}
		if errors.Is(err, ErrInvalidJSON) {
			respondWithError(
				w,
				http.StatusBadRequest,
				"Invalid JSON",
				err.Error(),
			)
			return
		}
		respondWithError(
			w,
			http.StatusInternalServerError,
			"Internal Server Error",
			"failed to process payload",
		)
		return
	}

	respondJSON(w, http.StatusOK, payload)
}

// loggingMiddleware logs incoming HTTP requests with method, URL, and timestamp.
func loggingMiddleware(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		log.Printf(
			"[%s] %s %s",
			time.Now().Format(time.RFC3339),
			r.Method,
			r.URL.Path,
		)
		next.ServeHTTP(w, r)
	})
}

func main() {
	mux := http.NewServeMux()
	mux.HandleFunc("/ping", pingHandler)
	mux.HandleFunc("/echo", echoHandler)

	wrappedMux := loggingMiddleware(mux)

	fmt.Println("Server starting on port 8080...")
	if err := http.ListenAndServe(":8080", wrappedMux); err != nil {
		log.Fatalf("Server failed to start: %v", err)
	}
}
