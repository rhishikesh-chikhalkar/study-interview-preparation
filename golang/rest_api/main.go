package main

import (
	"encoding/json"
	"fmt"
	"io"
	"log"
	"net/http"
	"time"
)

func pingHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodGet {
		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(http.StatusMethodNotAllowed)
		w.Write([]byte(`{"error": "Method Not Allowed"}`))
		return
	}
	w.Header().Set("Content-Type", "application/json")
	w.Write([]byte(`{"message": "pong"}`))
}

func echoHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(http.StatusMethodNotAllowed)
		w.Write([]byte(`{"error": "Method Not Allowed"}`))
		return
	}

	body, err := io.ReadAll(r.Body)
	if err != nil {
		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(http.StatusInternalServerError)
		w.Write([]byte(`{"error": "Failed to read request body"}`))
		return
	}
	defer r.Body.Close()

	var js json.RawMessage
	if err := json.Unmarshal(body, &js); err != nil {
		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(http.StatusBadRequest)
		w.Write([]byte(`{"error": "Invalid JSON"}`))
		return
	}

	w.Header().Set("Content-Type", "application/json")
	w.Write(body)
}

// loggingMiddleware logs the timestamp, method, and URL path of incoming requests.
func loggingMiddleware(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		log.Printf("[%s] %s %s", time.Now().Format(time.RFC3339), r.Method, r.URL.Path)
		next.ServeHTTP(w, r)
	})
}

func main() {
	mux := http.NewServeMux()
	mux.HandleFunc("/ping", pingHandler)
	mux.HandleFunc("/echo", echoHandler)

	wrappedMux := loggingMiddleware(mux)

	fmt.Println("Server is starting on port 8080...")
	if err := http.ListenAndServe(":8080", wrappedMux); err != nil {
		fmt.Printf("Error starting server: %s\n", err)
	}
}

