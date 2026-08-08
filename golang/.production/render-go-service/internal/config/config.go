package config

import (
	"os"
	"strconv"
	"time"
)

// Config holds all service configuration parameters parsed from environment variables.
type Config struct {
	Port            string
	Env             string
	ReadTimeout     time.Duration
	WriteTimeout    time.Duration
	ShutdownTimeout time.Duration
	APIKey          string
}

// LoadConfig reads configuration values from environment variables with sensible production defaults.
func LoadConfig() *Config {
	port := os.Getenv("PORT")
	if port == "" {
		port = "8080"
	}

	env := os.Getenv("ENV")
	if env == "" {
		env = "development"
	}

	readTimeoutSec := getEnvAsInt("READ_TIMEOUT", 15)
	writeTimeoutSec := getEnvAsInt("WRITE_TIMEOUT", 15)
	shutdownTimeoutSec := getEnvAsInt("SHUTDOWN_TIMEOUT", 10)

	apiKey := os.Getenv("API_KEY")

	return &Config{
		Port:            port,
		Env:             env,
		ReadTimeout:     time.Duration(readTimeoutSec) * time.Second,
		WriteTimeout:    time.Duration(writeTimeoutSec) * time.Second,
		ShutdownTimeout: time.Duration(shutdownTimeoutSec) * time.Second,
		APIKey:          apiKey,
	}
}

func getEnvAsInt(name string, defaultValue int) int {
	valueStr := os.Getenv(name)
	if valueStr == "" {
		return defaultValue
	}
	value, err := strconv.Atoi(valueStr)
	if err != nil {
		return defaultValue
	}
	return value
}
