package main

import (
	"bytes"
	"encoding/json"
	"errors"
	"log"
	"net/http"
	"net/http/httptest"
	"strings"
	"testing"
)

func TestPingHandler(t *testing.T) {
	tests := []struct {
		name           string
		method         string
		expectedStatus int
		expectedHeader string
	}{
		{
			name:           "Valid GET Request",
			method:         http.MethodGet,
			expectedStatus: http.StatusOK,
		},
		{
			name:           "Invalid POST Request",
			method:         http.MethodPost,
			expectedStatus: http.StatusMethodNotAllowed,
			expectedHeader: http.MethodGet,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			req := httptest.NewRequest(tt.method, "/ping", nil)
			rr := httptest.NewRecorder()

			pingHandler(rr, req)

			if rr.Code != tt.expectedStatus {
				t.Errorf("got status %d, want %d", rr.Code, tt.expectedStatus)
			}

			contentType := rr.Header().Get("Content-Type")
			if contentType != "application/json" {
				t.Errorf("got Content-Type %s, want application/json", contentType)
			}

			if tt.expectedHeader != "" {
				allow := rr.Header().Get("Allow")
				if allow != tt.expectedHeader {
					t.Errorf("got Allow header %s, want %s", allow, tt.expectedHeader)
				}
			}

			if tt.expectedStatus == http.StatusOK {
				var resp map[string]string
				if err := json.NewDecoder(rr.Body).Decode(&resp); err != nil {
					t.Fatalf("failed to decode response: %v", err)
				}
				if resp["message"] != "pong" {
					t.Errorf("got message %s, want pong", resp["message"])
				}
			}
		})
	}
}

func TestEchoHandler(t *testing.T) {
	tests := []struct {
		name           string
		method         string
		body           string
		expectedStatus int
		checkBody      func(t *testing.T, body string)
	}{
		{
			name:           "Valid JSON POST",
			method:         http.MethodPost,
			body:           `{"foo":"bar","num":42}`,
			expectedStatus: http.StatusOK,
			checkBody: func(t *testing.T, body string) {
				var data map[string]any
				if err := json.Unmarshal([]byte(body), &data); err != nil {
					t.Fatalf("invalid json response: %v", err)
				}
				if data["foo"] != "bar" || data["num"] != float64(42) {
					t.Errorf("unexpected body content: %s", body)
				}
			},
		},
		{
			name:           "Method Not Allowed GET",
			method:         http.MethodGet,
			body:           "",
			expectedStatus: http.StatusMethodNotAllowed,
			checkBody: func(t *testing.T, body string) {
				var errResp ErrorResponse
				if err := json.Unmarshal([]byte(body), &errResp); err != nil {
					t.Fatalf("invalid error json: %v", err)
				}
				if errResp.Code != http.StatusMethodNotAllowed {
					t.Errorf("got code %d, want %d", errResp.Code, http.StatusMethodNotAllowed)
				}
			},
		},
		{
			name:           "Malformed Syntax JSON",
			method:         http.MethodPost,
			body:           `{"foo":}`,
			expectedStatus: http.StatusBadRequest,
			checkBody: func(t *testing.T, body string) {
				var errResp ErrorResponse
				if err := json.Unmarshal([]byte(body), &errResp); err != nil {
					t.Fatalf("invalid error json: %v", err)
				}
				if errResp.Error != "Invalid JSON" {
					t.Errorf("got error %s, want Invalid JSON", errResp.Error)
				}
			},
		},
		{
			name:           "Empty Request Body",
			method:         http.MethodPost,
			body:           "",
			expectedStatus: http.StatusBadRequest,
			checkBody: func(t *testing.T, body string) {
				var errResp ErrorResponse
				if err := json.Unmarshal([]byte(body), &errResp); err != nil {
					t.Fatalf("invalid error json: %v", err)
				}
				if errResp.Error != "Bad Request" {
					t.Errorf("got error %s, want Bad Request", errResp.Error)
				}
			},
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			req := httptest.NewRequest(tt.method, "/echo", strings.NewReader(tt.body))
			rr := httptest.NewRecorder()

			echoHandler(rr, req)

			if rr.Code != tt.expectedStatus {
				t.Errorf("got status %d, want %d", rr.Code, tt.expectedStatus)
			}

			if tt.checkBody != nil {
				tt.checkBody(t, rr.Body.String())
			}
		})
	}
}

func TestUsersHandler(t *testing.T) {
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
			body:           `{"username":"gopher","email":"gopher@go.dev","age":25,"roles":["admin"]}`,
			expectedStatus: http.StatusCreated,
			checkResponse: func(t *testing.T, body string) {
				var resp UserResponse
				if err := json.Unmarshal([]byte(body), &resp); err != nil {
					t.Fatalf("failed to unmarshal UserResponse: %v", err)
				}
				if resp.Username != "gopher" || resp.Email != "gopher@go.dev" {
					t.Errorf("unexpected user data: %+v", resp)
				}
				if !resp.IsAdult {
					t.Errorf("expected IsAdult to be true")
				}
				if len(resp.Roles) != 1 || resp.Roles[0] != "admin" {
					t.Errorf("unexpected roles: %v", resp.Roles)
				}
				if resp.Status != "active" {
					t.Errorf("got status %s, want active", resp.Status)
				}
			},
		},
		{
			name:           "Missing Username Validation Failure",
			method:         http.MethodPost,
			body:           `{"email":"gopher@go.dev","age":20}`,
			expectedStatus: http.StatusBadRequest,
			checkResponse: func(t *testing.T, body string) {
				var errResp ErrorResponse
				if err := json.Unmarshal([]byte(body), &errResp); err != nil {
					t.Fatalf("failed to unmarshal ErrorResponse: %v", err)
				}
				if errResp.Error != "Validation Error" {
					t.Errorf("got error %s, want Validation Error", errResp.Error)
				}
			},
		},
		{
			name:           "Missing Email Validation Failure",
			method:         http.MethodPost,
			body:           `{"username":"gopher","age":20}`,
			expectedStatus: http.StatusBadRequest,
			checkResponse: func(t *testing.T, body string) {
				var errResp ErrorResponse
				if err := json.Unmarshal([]byte(body), &errResp); err != nil {
					t.Fatalf("failed to unmarshal ErrorResponse: %v", err)
				}
				if errResp.Error != "Validation Error" {
					t.Errorf("got error %s, want Validation Error", errResp.Error)
				}
			},
		},
		{
			name:           "Negative Age Validation Failure",
			method:         http.MethodPost,
			body:           `{"username":"gopher","email":"gopher@go.dev","age":-5}`,
			expectedStatus: http.StatusBadRequest,
			checkResponse: func(t *testing.T, body string) {
				var errResp ErrorResponse
				if err := json.Unmarshal([]byte(body), &errResp); err != nil {
					t.Fatalf("failed to unmarshal ErrorResponse: %v", err)
				}
				if errResp.Details != "age cannot be negative" {
					t.Errorf("unexpected error details: %s", errResp.Details)
				}
			},
		},
		{
			name:           "Method Not Allowed GET",
			method:         http.MethodGet,
			body:           "",
			expectedStatus: http.StatusMethodNotAllowed,
			checkResponse: func(t *testing.T, body string) {
				var errResp ErrorResponse
				if err := json.Unmarshal([]byte(body), &errResp); err != nil {
					t.Fatalf("failed to unmarshal ErrorResponse: %v", err)
				}
				if errResp.Code != http.StatusMethodNotAllowed {
					t.Errorf("got code %d, want 405", errResp.Code)
				}
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

func TestParseJSONBody_ErrorWrapping(t *testing.T) {
	t.Run("Empty Body Error Unwrapping", func(t *testing.T) {
		req := httptest.NewRequest(http.MethodPost, "/test", strings.NewReader(""))
		var val map[string]any
		err := parseJSONBody(req, &val)

		if !errors.Is(err, ErrEmptyBody) {
			t.Errorf("expected errors.Is(err, ErrEmptyBody) to be true, got %v", err)
		}
	})

	t.Run("Syntax Error Unwrapping", func(t *testing.T) {
		req := httptest.NewRequest(http.MethodPost, "/test", strings.NewReader("{bad}"))
		var val map[string]any
		err := parseJSONBody(req, &val)

		if !errors.Is(err, ErrInvalidJSON) {
			t.Errorf("expected errors.Is(err, ErrInvalidJSON) to be true, got %v", err)
		}
	})

	t.Run("Type Error Unwrapping", func(t *testing.T) {
		type Target struct {
			Age int `json:"age"`
		}
		req := httptest.NewRequest(
			http.MethodPost,
			"/test",
			strings.NewReader(`{"age":"not-a-number"}`),
		)
		var val Target
		err := parseJSONBody(req, &val)

		if !errors.Is(err, ErrInvalidJSON) {
			t.Errorf("expected errors.Is(err, ErrInvalidJSON) to be true, got %v", err)
		}
	})
}

func TestRespondWithError(t *testing.T) {
	rr := httptest.NewRecorder()
	respondWithError(rr, http.StatusBadRequest, "Bad Request", "test detail")

	if rr.Code != http.StatusBadRequest {
		t.Errorf("got status %d, want %d", rr.Code, http.StatusBadRequest)
	}

	var resp ErrorResponse
	if err := json.NewDecoder(rr.Body).Decode(&resp); err != nil {
		t.Fatalf("failed to decode response: %v", err)
	}

	if resp.Error != "Bad Request" || resp.Code != http.StatusBadRequest || resp.Details != "test detail" {
		t.Errorf("unexpected error response structure: %+v", resp)
	}
}

func TestLoggingMiddleware(t *testing.T) {
	var buf bytes.Buffer
	originalWriter := log.Writer()
	log.SetOutput(&buf)
	defer log.SetOutput(originalWriter)

	nextHandler := http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusOK)
	})

	middleware := loggingMiddleware(nextHandler)
	req := httptest.NewRequest(http.MethodGet, "/test-path", nil)
	rr := httptest.NewRecorder()

	middleware.ServeHTTP(rr, req)

	if rr.Code != http.StatusOK {
		t.Errorf("got status %d, want 200", rr.Code)
	}

	logOutput := buf.String()
	if !strings.Contains(logOutput, "GET") || !strings.Contains(logOutput, "/test-path") {
		t.Errorf("log output missing details: %s", logOutput)
	}
}
