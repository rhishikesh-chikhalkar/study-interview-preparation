package handler_test

import (
	"bytes"
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"testing"

	"render-go-service/internal/handler"
	"render-go-service/internal/model"
	"render-go-service/internal/service"
)

func setupTestRouter() http.Handler {
	svc := service.NewMemoryTaskService()
	healthH := handler.NewHealthHandler()
	taskH := handler.NewTaskHandler(svc)

	mux := http.NewServeMux()
	mux.HandleFunc("/healthz", healthH.Liveness)
	mux.HandleFunc("/readyz", healthH.Readiness)
	mux.HandleFunc("/api/v1/tasks", taskH.HandleTasks)
	mux.HandleFunc("/api/v1/tasks/", taskH.HandleTaskByID)

	return mux
}

func TestHealthEndpoints(t *testing.T) {
	router := setupTestRouter()

	t.Run("GET /healthz returns 200 OK", func(t *testing.T) {
		req := httptest.NewRequest(http.MethodGet, "/healthz", nil)
		rr := httptest.NewRecorder()

		router.ServeHTTP(rr, req)

		if rr.Code != http.StatusOK {
			t.Fatalf("expected status 200, got %d", rr.Code)
		}

		var body map[string]interface{}
		if err := json.NewDecoder(rr.Body).Decode(&body); err != nil {
			t.Fatalf("failed to decode response: %v", err)
		}
		if body["status"] != "healthy" {
			t.Errorf("expected status 'healthy', got '%v'", body["status"])
		}
	})

	t.Run("GET /readyz returns 200 OK", func(t *testing.T) {
		req := httptest.NewRequest(http.MethodGet, "/readyz", nil)
		rr := httptest.NewRecorder()

		router.ServeHTTP(rr, req)

		if rr.Code != http.StatusOK {
			t.Fatalf("expected status 200, got %d", rr.Code)
		}

		var body map[string]interface{}
		if err := json.NewDecoder(rr.Body).Decode(&body); err != nil {
			t.Fatalf("failed to decode response: %v", err)
		}
		if body["status"] != "ready" {
			t.Errorf("expected status 'ready', got '%v'", body["status"])
		}
	})
}

func TestTaskCRUD(t *testing.T) {
	router := setupTestRouter()

	t.Run("GET /api/v1/tasks returns initial pre-seeded tasks", func(t *testing.T) {
		req := httptest.NewRequest(http.MethodGet, "/api/v1/tasks", nil)
		rr := httptest.NewRecorder()

		router.ServeHTTP(rr, req)

		if rr.Code != http.StatusOK {
			t.Fatalf("expected status 200, got %d", rr.Code)
		}

		var tasks []model.Task
		if err := json.NewDecoder(rr.Body).Decode(&tasks); err != nil {
			t.Fatalf("failed to decode task list: %v", err)
		}
		if len(tasks) == 0 {
			t.Errorf("expected pre-seeded task, got empty list")
		}
	})

	t.Run("POST /api/v1/tasks creates a new task", func(t *testing.T) {
		payload := map[string]string{
			"title":       "Write unit tests",
			"description": "Cover all HTTP endpoints with httptest",
		}
		jsonBytes, _ := json.Marshal(payload)

		req := httptest.NewRequest(http.MethodPost, "/api/v1/tasks", bytes.NewReader(jsonBytes))
		req.Header.Set("Content-Type", "application/json")
		rr := httptest.NewRecorder()

		router.ServeHTTP(rr, req)

		if rr.Code != http.StatusCreated {
			t.Fatalf("expected status 201 Created, got %d", rr.Code)
		}

		var created model.Task
		if err := json.NewDecoder(rr.Body).Decode(&created); err != nil {
			t.Fatalf("failed to decode created task: %v", err)
		}
		if created.Title != payload["title"] {
			t.Errorf("expected title '%s', got '%s'", payload["title"], created.Title)
		}
	})

	t.Run("POST /api/v1/tasks returns 400 Bad Request on empty title", func(t *testing.T) {
		payload := map[string]string{
			"title": "",
		}
		jsonBytes, _ := json.Marshal(payload)

		req := httptest.NewRequest(http.MethodPost, "/api/v1/tasks", bytes.NewReader(jsonBytes))
		req.Header.Set("Content-Type", "application/json")
		rr := httptest.NewRecorder()

		router.ServeHTTP(rr, req)

		if rr.Code != http.StatusBadRequest {
			t.Fatalf("expected status 400 Bad Request, got %d", rr.Code)
		}
	})
}
