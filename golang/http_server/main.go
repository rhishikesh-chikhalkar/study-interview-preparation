package main

import (
	"fmt"
	"log"
	"net/http"
	"time"
)

// getAboutInfo demonstrates a function returning multiple values: a description and a version string.
func getAboutInfo() (string, string) {
	return "This is a simple Go HTTP server demonstrating multiple routes.", "v1.0"
}

func helloHandler(w http.ResponseWriter, r *http.Request) {
	fmt.Fprint(w, "Hello from Go")
}

func aboutHandler(w http.ResponseWriter, r *http.Request) {
	description, version := getAboutInfo()
	fmt.Fprintf(w, "About: %s\nVersion: %s", description, version)
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
	mux.HandleFunc("/", helloHandler)
	mux.HandleFunc("/about", aboutHandler)

	wrappedMux := loggingMiddleware(mux)

	fmt.Println("Server is starting on port 8080...")
	if err := http.ListenAndServe(":8080", wrappedMux); err != nil {
		fmt.Printf("Error starting server: %s\n", err)
	}
}

