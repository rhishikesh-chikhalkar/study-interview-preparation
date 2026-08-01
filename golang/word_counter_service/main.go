package main

import (
	"encoding/json"
	"fmt"
	"io"
	"log"
	"net/http"
	"strings"
	"time"
)

type CountRequest struct {
	Text string `json:"text"`
}

type CountResponse struct {
	WordCount      int `json:"word_count"`
	CharacterCount int `json:"character_count"`
}

func countHandler(w http.ResponseWriter, r *http.Request) {
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

	var req CountRequest
	if err := json.Unmarshal(body, &req); err != nil {
		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(http.StatusBadRequest)
		w.Write([]byte(`{"error": "Invalid JSON"}`))
		return
	}

	// Calculate counts
	// Words are counted by splitting on whitespace
	words := strings.Fields(req.Text)
	wordCount := len(words)
	
	// Character count handles multi-byte UTF-8 runes correctly
	characterCount := len([]rune(req.Text))

	resp := CountResponse{
		WordCount:      wordCount,
		CharacterCount: characterCount,
	}

	respBytes, err := json.Marshal(resp)
	if err != nil {
		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(http.StatusInternalServerError)
		w.Write([]byte(`{"error": "Failed to marshal response"}`))
		return
	}

	w.Header().Set("Content-Type", "application/json")
	w.Write(respBytes)
}

func loggingMiddleware(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		log.Printf("[%s] %s %s", time.Now().Format(time.RFC3339), r.Method, r.URL.Path)
		next.ServeHTTP(w, r)
	})
}

func main() {
	mux := http.NewServeMux()
	mux.HandleFunc("/count", countHandler)

	wrappedMux := loggingMiddleware(mux)

	port := ":8081"
	fmt.Printf("Go Word Counter Service is starting on port %s...\n", port)
	if err := http.ListenAndServe(port, wrappedMux); err != nil {
		log.Fatalf("Error starting server: %s\n", err)
	}
}
