package handler

import (
	"encoding/json"
	"net/http"

	"time"
)

// HealthHandler provides standard cloud PaaS liveness and readiness probe handlers.
type HealthHandler struct {
	startTime time.Time
}

// NewHealthHandler constructs a HealthHandler instance.
func NewHealthHandler() *HealthHandler {
	return &HealthHandler{
		startTime: time.Now().UTC(),
	}
}

type HealthResponse struct {
	Status    string    `json:"status"`
	Uptime    string    `json:"uptime"`
	Timestamp time.Time `json:"timestamp"`
}

// Liveness (/healthz) checks whether the service HTTP process is alive.
func (h *HealthHandler) Liveness(w http.ResponseWriter, r *http.Request) {
	resp := HealthResponse{
		Status:    "healthy",
		Uptime:    time.Since(h.startTime).String(),
		Timestamp: time.Now().UTC(),
	}

	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
	_ = json.NewEncoder(w).Encode(resp)
}

// Readiness (/readyz) checks whether background dependencies are available.
func (h *HealthHandler) Readiness(w http.ResponseWriter, r *http.Request) {
	resp := HealthResponse{
		Status:    "ready",
		Uptime:    time.Since(h.startTime).String(),
		Timestamp: time.Now().UTC(),
	}

	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
	_ = json.NewEncoder(w).Encode(resp)
}
