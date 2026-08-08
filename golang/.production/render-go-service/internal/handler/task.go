package handler

import (
	"encoding/json"
	"errors"
	"net/http"
	"strings"

	"render-go-service/internal/model"
	"render-go-service/internal/service"
)

// TaskHandler manages HTTP routes for task resources.
type TaskHandler struct {
	svc service.TaskService
}

// NewTaskHandler constructs a TaskHandler with service dependencies.
func NewTaskHandler(svc service.TaskService) *TaskHandler {
	return &TaskHandler{svc: svc}
}

// HandleTasks routes GET /api/v1/tasks and POST /api/v1/tasks.
func (h *TaskHandler) HandleTasks(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")

	switch r.Method {
	case http.MethodGet:
		tasks := h.svc.ListTasks()
		_ = json.NewEncoder(w).Encode(tasks)

	case http.MethodPost:
		var req model.CreateTaskRequest
		if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
			w.WriteHeader(http.StatusBadRequest)
			_ = json.NewEncoder(w).Encode(map[string]string{
				"error": "invalid JSON body",
			})
			return
		}

		task, err := h.svc.CreateTask(req)
		if err != nil {
			w.WriteHeader(http.StatusBadRequest)
			_ = json.NewEncoder(w).Encode(map[string]string{
				"error": err.Error(),
			})
			return
		}

		w.WriteHeader(http.StatusCreated)
		_ = json.NewEncoder(w).Encode(task)

	default:
		w.WriteHeader(http.StatusMethodNotAllowed)
		_ = json.NewEncoder(w).Encode(map[string]string{
			"error": "method not allowed",
		})
	}
}

// HandleTaskByID routes GET, PUT, DELETE for /api/v1/tasks/{id}.
func (h *TaskHandler) HandleTaskByID(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")

	id := strings.TrimPrefix(r.URL.Path, "/api/v1/tasks/")
	if id == "" || strings.Contains(id, "/") {
		w.WriteHeader(http.StatusBadRequest)
		_ = json.NewEncoder(w).Encode(map[string]string{
			"error": "invalid task ID in URL path",
		})
		return
	}

	switch r.Method {
	case http.MethodGet:
		task, err := h.svc.GetTaskByID(id)
		if err != nil {
			if errors.Is(err, model.ErrTaskNotFound) {
				w.WriteHeader(http.StatusNotFound)
				_ = json.NewEncoder(w).Encode(map[string]string{
					"error": "task not found",
				})
				return
			}
			w.WriteHeader(http.StatusInternalServerError)
			_ = json.NewEncoder(w).Encode(map[string]string{
				"error": "internal server error",
			})
			return
		}
		_ = json.NewEncoder(w).Encode(task)

	case http.MethodPut:
		var req model.UpdateTaskRequest
		if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
			w.WriteHeader(http.StatusBadRequest)
			_ = json.NewEncoder(w).Encode(map[string]string{
				"error": "invalid JSON body",
			})
			return
		}

		task, err := h.svc.UpdateTask(id, req)
		if err != nil {
			if errors.Is(err, model.ErrTaskNotFound) {
				w.WriteHeader(http.StatusNotFound)
				_ = json.NewEncoder(w).Encode(map[string]string{
					"error": "task not found",
				})
				return
			}
			w.WriteHeader(http.StatusInternalServerError)
			_ = json.NewEncoder(w).Encode(map[string]string{
				"error": "internal server error",
			})
			return
		}
		_ = json.NewEncoder(w).Encode(task)

	case http.MethodDelete:
		err := h.svc.DeleteTask(id)
		if err != nil {
			if errors.Is(err, model.ErrTaskNotFound) {
				w.WriteHeader(http.StatusNotFound)
				_ = json.NewEncoder(w).Encode(map[string]string{
					"error": "task not found",
				})
				return
			}
			w.WriteHeader(http.StatusInternalServerError)
			_ = json.NewEncoder(w).Encode(map[string]string{
				"error": "internal server error",
			})
			return
		}
		w.WriteHeader(http.StatusNoContent)

	default:
		w.WriteHeader(http.StatusMethodNotAllowed)
		_ = json.NewEncoder(w).Encode(map[string]string{
			"error": "method not allowed",
		})
	}
}
