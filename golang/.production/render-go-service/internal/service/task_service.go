package service

import (
	"fmt"
	"sync"
	"time"

	"render-go-service/internal/model"
)

// TaskService defines operational capabilities for task business logic.
type TaskService interface {
	CreateTask(req model.CreateTaskRequest) (model.Task, error)
	GetTaskByID(id string) (model.Task, error)
	ListTasks() []model.Task
	UpdateTask(id string, req model.UpdateTaskRequest) (model.Task, error)
	DeleteTask(id string) error
}

type memoryTaskService struct {
	mu     sync.RWMutex
	tasks  map[string]model.Task
	nextID int
}

// NewMemoryTaskService initializes an thread-safe in-memory task repository.
func NewMemoryTaskService() TaskService {
	s := &memoryTaskService{
		tasks:  make(map[string]model.Task),
		nextID: 1,
	}

	// Pre-seed sample task for immediate demo testing
	_, _ = s.CreateTask(model.CreateTaskRequest{
		Title:       "Deploy Go service to Render",
		Description: "Verify live web service endpoint on Render PaaS platform",
	})

	return s
}

func (s *memoryTaskService) CreateTask(req model.CreateTaskRequest) (model.Task, error) {
	if err := req.Validate(); err != nil {
		return model.Task{}, err
	}

	s.mu.Lock()
	defer s.mu.Unlock()

	id := fmt.Sprintf("task-%d", s.nextID)
	s.nextID++

	now := time.Now().UTC()
	task := model.Task{
		ID:          id,
		Title:       req.Title,
		Description: req.Description,
		Completed:   false,
		CreatedAt:   now,
		UpdatedAt:   now,
	}

	s.tasks[id] = task
	return task, nil
}

func (s *memoryTaskService) GetTaskByID(id string) (model.Task, error) {
	s.mu.RLock()
	defer s.mu.RUnlock()

	task, exists := s.tasks[id]
	if !exists {
		return model.Task{}, model.ErrTaskNotFound
	}
	return task, nil
}

func (s *memoryTaskService) ListTasks() []model.Task {
	s.mu.RLock()
	defer s.mu.RUnlock()

	list := make([]model.Task, 0, len(s.tasks))
	for _, task := range s.tasks {
		list = append(list, task)
	}
	return list
}

func (s *memoryTaskService) UpdateTask(
	id string,
	req model.UpdateTaskRequest,
) (model.Task, error) {
	s.mu.Lock()
	defer s.mu.Unlock()

	task, exists := s.tasks[id]
	if !exists {
		return model.Task{}, model.ErrTaskNotFound
	}

	if req.Title != nil {
		task.Title = *req.Title
	}
	if req.Description != nil {
		task.Description = *req.Description
	}
	if req.Completed != nil {
		task.Completed = *req.Completed
	}
	task.UpdatedAt = time.Now().UTC()

	s.tasks[id] = task
	return task, nil
}

func (s *memoryTaskService) DeleteTask(id string) error {
	s.mu.Lock()
	defer s.mu.Unlock()

	if _, exists := s.tasks[id]; !exists {
		return model.ErrTaskNotFound
	}

	delete(s.tasks, id)
	return nil
}
