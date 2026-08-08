package main

import (
	"context"
	"errors"
	"fmt"
	"log/slog"
	"net/http"
	"os"
	"os/signal"
	"syscall"

	"render-go-service/internal/config"
	"render-go-service/internal/handler"
	"render-go-service/internal/middleware"
	"render-go-service/internal/service"
)

func main() {
	// Initialize structured JSON logging
	logger := slog.New(slog.NewJSONHandler(os.Stdout, nil))
	slog.SetDefault(logger)

	cfg := config.LoadConfig()
	slog.Info("starting_service",
		"env", cfg.Env,
		"port", cfg.Port,
	)

	// Initialize domain services and HTTP handlers
	taskSvc := service.NewMemoryTaskService()
	healthH := handler.NewHealthHandler()
	taskH := handler.NewTaskHandler(taskSvc)

	// Configure standard HTTP router
	mux := http.NewServeMux()
	mux.HandleFunc("/healthz", healthH.Liveness)
	mux.HandleFunc("/readyz", healthH.Readiness)
	mux.HandleFunc("/api/v1/tasks", taskH.HandleTasks)
	mux.HandleFunc("/api/v1/tasks/", taskH.HandleTaskByID)

	// Chain production middleware (Recovery -> CORS -> Auth -> Logging)
	handlerChain := middleware.Chain(
		mux,
		middleware.Recovery,
		middleware.CORS,
		middleware.APIKeyAuth(cfg.APIKey),
		middleware.Logging,
	)

	// Bind to 0.0.0.0:$PORT for dynamic Cloud PaaS environments like Render
	listenAddr := fmt.Sprintf("0.0.0.0:%s", cfg.Port)
	server := &http.Server{
		Addr:         listenAddr,
		Handler:      handlerChain,
		ReadTimeout:  cfg.ReadTimeout,
		WriteTimeout: cfg.WriteTimeout,
	}

	// Channel to capture termination signals from OS/Render container runtime
	shutdownErr := make(chan error, 1)
	go func() {
		quit := make(chan os.Signal, 1)
		signal.Notify(quit, os.Interrupt, syscall.SIGTERM)
		sig := <-quit

		slog.Info("shutdown_signal_received", "signal", sig.String())

		ctx, cancel := context.WithTimeout(context.Background(), cfg.ShutdownTimeout)
		defer cancel()

		shutdownErr <- server.Shutdown(ctx)
	}()

	slog.Info("server_listening", "addr", listenAddr)
	if err := server.ListenAndServe(); err != nil && !errors.Is(err, http.ErrServerClosed) {
		slog.Error("server_listen_failed", "error", err)
		os.Exit(1)
	}

	if err := <-shutdownErr; err != nil {
		slog.Error("graceful_shutdown_failed", "error", err)
		os.Exit(1)
	}

	slog.Info("server_exited_cleanly")
}
