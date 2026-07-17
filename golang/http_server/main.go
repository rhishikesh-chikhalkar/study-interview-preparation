package main

import (
	"fmt"
	"net/http"
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

func main() {
	http.HandleFunc("/", helloHandler)
	http.HandleFunc("/about", aboutHandler)
	fmt.Println("Server is starting on port 8080...")
	if err := http.ListenAndServe(":8080", nil); err != nil {
		fmt.Printf("Error starting server: %s\n", err)
	}
}
