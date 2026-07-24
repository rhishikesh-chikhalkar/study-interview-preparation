package main

import (
	"bytes"
	"log"
	"net/http"
	"net/http/httptest"
	"strings"
	"testing"
)

func TestPingHandler(t *testing.T) {
	req, err := http.NewRequest("GET", "/ping", nil)
	if err != nil {
		t.Fatal(err)
	}

	rr := httptest.NewRecorder()
	handler := http.HandlerFunc(pingHandler)
	handler.ServeHTTP(rr, req)

	if status := rr.Code; status != http.StatusOK {
		t.Errorf("handler returned wrong status code: got %v want %v", status, http.StatusOK)
	}

	expected := `{"message": "pong"}`
	if rr.Body.String() != expected {
		t.Errorf("handler returned unexpected body: got %v want %v", rr.Body.String(), expected)
	}

	contentType := rr.Header().Get("Content-Type")
	if contentType != "application/json" {
		t.Errorf("handler returned wrong content type: got %v want %v", contentType, "application/json")
	}
}

func TestEchoHandler_ValidJSON(t *testing.T) {
	jsonStr := []byte(`{"foo":"bar","baz":123}`)
	req, err := http.NewRequest("POST", "/echo", bytes.NewBuffer(jsonStr))
	if err != nil {
		t.Fatal(err)
	}
	req.Header.Set("Content-Type", "application/json")

	rr := httptest.NewRecorder()
	handler := http.HandlerFunc(echoHandler)
	handler.ServeHTTP(rr, req)

	if status := rr.Code; status != http.StatusOK {
		t.Errorf("handler returned wrong status code: got %v want %v", status, http.StatusOK)
	}

	if rr.Body.String() != string(jsonStr) {
		t.Errorf("handler returned unexpected body: got %v want %v", rr.Body.String(), string(jsonStr))
	}
}

func TestEchoHandler_InvalidJSON(t *testing.T) {
	jsonStr := []byte(`invalid json`)
	req, err := http.NewRequest("POST", "/echo", bytes.NewBuffer(jsonStr))
	if err != nil {
		t.Fatal(err)
	}

	rr := httptest.NewRecorder()
	handler := http.HandlerFunc(echoHandler)
	handler.ServeHTTP(rr, req)

	if status := rr.Code; status != http.StatusBadRequest {
		t.Errorf("handler returned wrong status code: got %v want %v", status, http.StatusBadRequest)
	}
}

func TestLoggingMiddleware(t *testing.T) {
	// Capture log output
	var buf bytes.Buffer
	originalWriter := log.Writer()
	log.SetOutput(&buf)
	defer log.SetOutput(originalWriter)

	// Create a dummy next handler
	nextHandler := http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusOK)
		w.Write([]byte("ok"))
	})

	middleware := loggingMiddleware(nextHandler)

	req, err := http.NewRequest("GET", "/test-path", nil)
	if err != nil {
		t.Fatal(err)
	}

	rr := httptest.NewRecorder()
	middleware.ServeHTTP(rr, req)

	if rr.Code != http.StatusOK {
		t.Errorf("expected status 200, got %d", rr.Code)
	}

	logOutput := buf.String()
	if !strings.Contains(logOutput, "GET") {
		t.Errorf("expected log output to contain GET, got %s", logOutput)
	}
	if !strings.Contains(logOutput, "/test-path") {
		t.Errorf("expected log output to contain /test-path, got %s", logOutput)
	}
}

