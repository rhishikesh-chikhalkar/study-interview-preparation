package model

import (
	"errors"

	"strings"
	"time"
)

var (
	ErrTitleRequired = errors.New("title is required")
	ErrTaskNotFound  = errors.New("task not found")
)

// Task represents a managed work item in the system.
type Task struct {
	ID          string    `json:"id"`
	Title       string    `json:"title"`
	Description string    `json:"description,omitempty"`
	Completed   bool      `json:"completed"`
	CreatedAt   time.Time `json:"created_at"`
	UpdatedAt   time.Time `json:"updated_at"`
}

// CreateTaskRequest contains parameters required to create a new Task.
type CreateTaskRequest struct {
	Title       string `json:"title"`
	Description string `json:"description"`
}

// Validate checks request validity.
func (req *CreateTaskRequest) Validate() error {
	if strings.TrimSpace(req.Title) == "" {
		return ErrTitleRequired
	}
	return nil
}

// UpdateTaskRequest contains optional fields to update an existing Task.
type UpdateTaskRequest struct {
	Title       *string `json:"title,omitempty"`
	Description *string `json:"description,omitempty"`
	Completed   *bool   `json:"completed,omitempty"`
}
