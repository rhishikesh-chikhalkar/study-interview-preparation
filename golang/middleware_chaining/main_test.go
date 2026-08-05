package main

import (
	"bytes"
	"encoding/json"
	"io"
	"log"
	"net/http"
	"net/http/httptest"
	"strings"
	"testing"
)

func TestHealthEndpoint(t *testing.T) {
	var buf bytes.Buffer
	logger := log.New(&buf, "[TEST] ", 0)
	validKeys := map[string]string{"key1": "Client1"}

	handler := setupRoutes(logger, validKeys)

	req := httptest.NewRequest(http.MethodGet, "/health", nil)
	rr := httptest.NewRecorder()

	handler.ServeHTTP(rr, req)

	if rr.Code != http.StatusOK {
		t.Errorf("got status %d, want %d", rr.Code, http.StatusOK)
	}

	var resp map[string]string
	if err := json.NewDecoder(rr.Body).Decode(&resp); err != nil {
		t.Fatalf("failed to decode response JSON: %v", err)
	}

	if resp["status"] != "healthy" {
		t.Errorf("got status %s, want healthy", resp["status"])
	}

	logOutput := buf.String()
	if !strings.Contains(logOutput, "/health") || !strings.Contains(logOutput, "GET") {
		t.Errorf("expected log to contain GET and /health, got: %s", logOutput)
	}
}

func TestAPIKeyAuth_Success_Header(t *testing.T) {
	var buf bytes.Buffer
	logger := log.New(&buf, "[TEST] ", 0)
	validKeys := map[string]string{"secret-key-123": "AcmeCorp"}

	handler := setupRoutes(logger, validKeys)

	req := httptest.NewRequest(http.MethodGet, "/api/v1/data", nil)
	req.Header.Set("X-API-Key", "secret-key-123")
	rr := httptest.NewRecorder()

	handler.ServeHTTP(rr, req)

	if rr.Code != http.StatusOK {
		t.Errorf("got status %d, want %d", rr.Code, http.StatusOK)
	}

	var resp map[string]any
	if err := json.NewDecoder(rr.Body).Decode(&resp); err != nil {
		t.Fatalf("failed to decode response: %v", err)
	}

	msg, ok := resp["message"].(string)
	if !ok || !strings.Contains(msg, "AcmeCorp") {
		t.Errorf("expected message to contain AcmeCorp, got %v", resp["message"])
	}
}

func TestAPIKeyAuth_Success_Bearer(t *testing.T) {
	var buf bytes.Buffer
	logger := log.New(&buf, "[TEST] ", 0)
	validKeys := map[string]string{"secret-key-456": "BetaInc"}

	handler := setupRoutes(logger, validKeys)

	req := httptest.NewRequest(http.MethodGet, "/api/v1/data", nil)
	req.Header.Set("Authorization", "Bearer secret-key-456")
	rr := httptest.NewRecorder()

	handler.ServeHTTP(rr, req)

	if rr.Code != http.StatusOK {
		t.Errorf("got status %d, want %d", rr.Code, http.StatusOK)
	}

	var resp map[string]any
	if err := json.NewDecoder(rr.Body).Decode(&resp); err != nil {
		t.Fatalf("failed to decode response: %v", err)
	}

	msg, ok := resp["message"].(string)
	if !ok || !strings.Contains(msg, "BetaInc") {
		t.Errorf("expected message to contain BetaInc, got %v", resp["message"])
	}
}

func TestAPIKeyAuth_MissingKey(t *testing.T) {
	var buf bytes.Buffer
	logger := log.New(&buf, "[TEST] ", 0)
	validKeys := map[string]string{"secret-key-123": "AcmeCorp"}

	handler := setupRoutes(logger, validKeys)

	req := httptest.NewRequest(http.MethodGet, "/api/v1/data", nil)
	rr := httptest.NewRecorder()

	handler.ServeHTTP(rr, req)

	if rr.Code != http.StatusUnauthorized {
		t.Errorf("got status %d, want %d", rr.Code, http.StatusUnauthorized)
	}

	var resp map[string]any
	if err := json.NewDecoder(rr.Body).Decode(&resp); err != nil {
		t.Fatalf("failed to decode error JSON: %v", err)
	}

	if resp["error"] != "Unauthorized" {
		t.Errorf("got error message %v, want Unauthorized", resp["error"])
	}
}

func TestAPIKeyAuth_InvalidKey(t *testing.T) {
	var buf bytes.Buffer
	logger := log.New(&buf, "[TEST] ", 0)
	validKeys := map[string]string{"secret-key-123": "AcmeCorp"}

	handler := setupRoutes(logger, validKeys)

	req := httptest.NewRequest(http.MethodGet, "/api/v1/data", nil)
	req.Header.Set("X-API-Key", "wrong-key")
	rr := httptest.NewRecorder()

	handler.ServeHTTP(rr, req)

	if rr.Code != http.StatusUnauthorized {
		t.Errorf("got status %d, want %d", rr.Code, http.StatusUnauthorized)
	}
}

func TestMiddlewareChainingOrder(t *testing.T) {
	executionLog := []string{}

	m1 := func(next http.Handler) http.Handler {
		return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
			executionLog = append(executionLog, "m1_start")
			next.ServeHTTP(w, r)
			executionLog = append(executionLog, "m1_end")
		})
	}

	m2 := func(next http.Handler) http.Handler {
		return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
			executionLog = append(executionLog, "m2_start")
			next.ServeHTTP(w, r)
			executionLog = append(executionLog, "m2_end")
		})
	}

	target := http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		executionLog = append(executionLog, "target")
		w.WriteHeader(http.StatusOK)
	})

	chained := Chain(target, m1, m2)

	req := httptest.NewRequest(http.MethodGet, "/", nil)
	rr := httptest.NewRecorder()

	chained.ServeHTTP(rr, req)

	expectedOrder := []string{
		"m1_start",
		"m2_start",
		"target",
		"m2_end",
		"m1_end",
	}

	if len(executionLog) != len(expectedOrder) {
		t.Fatalf("got log length %d, want %d", len(executionLog), len(expectedOrder))
	}

	for i, v := range expectedOrder {
		if executionLog[i] != v {
			t.Errorf("step %d: got %s, want %s", i, executionLog[i], v)
		}
	}
}

func TestMiddlewareChaining_ShortCircuit(t *testing.T) {
	targetCalled := false

	validKeys := map[string]string{"valid_key": "user"}
	authMw := APIKeyAuthMiddleware(validKeys)

	target := http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		targetCalled = true
		w.WriteHeader(http.StatusOK)
	})

	chained := Chain(target, authMw)

	req := httptest.NewRequest(http.MethodGet, "/", nil)
	req.Header.Set("X-API-Key", "invalid_key")
	rr := httptest.NewRecorder()

	chained.ServeHTTP(rr, req)

	if rr.Code != http.StatusUnauthorized {
		t.Errorf("got status %d, want %d", rr.Code, http.StatusUnauthorized)
	}

	if targetCalled {
		t.Errorf("target handler was executed despite auth failure")
	}
}

func TestRecoveryMiddleware(t *testing.T) {
	var buf bytes.Buffer
	logger := log.New(&buf, "[TEST] ", 0)
	validKeys := map[string]string{"secret-key-123": "AcmeCorp"}

	handler := setupRoutes(logger, validKeys)

	req := httptest.NewRequest(http.MethodGet, "/api/v1/panic", nil)
	req.Header.Set("X-API-Key", "secret-key-123")
	rr := httptest.NewRecorder()

	handler.ServeHTTP(rr, req)

	if rr.Code != http.StatusInternalServerError {
		t.Errorf("got status %d, want %d", rr.Code, http.StatusInternalServerError)
	}

	var resp map[string]any
	if err := json.NewDecoder(rr.Body).Decode(&resp); err != nil {
		t.Fatalf("failed to decode response: %v", err)
	}

	if resp["error"] != "Internal Server Error" {
		t.Errorf("got error %v, want Internal Server Error", resp["error"])
	}

	logOutput := buf.String()
	if !strings.Contains(logOutput, "PANIC RECOVERED") {
		t.Errorf("expected log to contain 'PANIC RECOVERED', got: %s", logOutput)
	}
}

func TestResponseWriter_CaptureStatusAndBytes(t *testing.T) {
	rec := httptest.NewRecorder()
	rw := newResponseWriter(rec)

	bodyText := "Hello, World!"
	rw.WriteHeader(http.StatusCreated)
	rw.Write([]byte(bodyText))

	if rw.statusCode != http.StatusCreated {
		t.Errorf("got status %d, want %d", rw.statusCode, http.StatusCreated)
	}

	if rw.bytesWritten != int64(len(bodyText)) {
		t.Errorf("got bytesWritten %d, want %d", rw.bytesWritten, len(bodyText))
	}

	res := rec.Result()
	defer res.Body.Close()
	resBody, _ := io.ReadAll(res.Body)

	if string(resBody) != bodyText {
		t.Errorf("got body %s, want %s", string(resBody), bodyText)
	}
}
