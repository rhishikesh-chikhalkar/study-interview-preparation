package handler

import (
	"bytes"
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"testing"
)

func TestHandleAnalyze(t *testing.T) {
	h := NewAnalyzeHandler()

	t.Run("valid text analysis", func(t *testing.T) {
		body := []byte(`{"text": "Hello world from Go microservice!\nLine two."}`)
		req := httptest.NewRequest(http.MethodPost, "/api/v1/analyze", bytes.NewBuffer(body))
		req.Header.Set("Content-Type", "application/json")
		rr := httptest.NewRecorder()

		h.HandleAnalyze(rr, req)

		if rr.Code != http.StatusOK {
			t.Fatalf("expected status %d, got %d", http.StatusOK, rr.Code)
		}

		var resp AnalyzeResponse
		if err := json.NewDecoder(rr.Body).Decode(&resp); err != nil {
			t.Fatalf("failed to decode response: %v", err)
		}

		if resp.WordCount != 7 {
			t.Errorf("expected word count 7, got %d", resp.WordCount)
		}
		if resp.LineCount != 2 {
			t.Errorf("expected line count 2, got %d", resp.LineCount)
		}
		if resp.Service != "Go High-Performance Microservice" {
			t.Errorf("unexpected service string: %s", resp.Service)
		}
	})

	t.Run("method not allowed", func(t *testing.T) {
		req := httptest.NewRequest(http.MethodGet, "/api/v1/analyze", nil)
		rr := httptest.NewRecorder()

		h.HandleAnalyze(rr, req)

		if rr.Code != http.StatusMethodNotAllowed {
			t.Fatalf("expected status %d, got %d", http.StatusMethodNotAllowed, rr.Code)
		}
	})
}
