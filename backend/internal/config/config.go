package config

// Package config handles environment variable parsing for the backend service.
// The fields are kept minimal but documented thoroughly so the code can serve
// as a template for production deployments.

import (
    "log"
    "os"
)

// Config represents application runtime configuration. Values are read from
// environment variables so secrets are never hard coded.
type Config struct {
    PythonAgentURL string // Base URL of the Python agent service
}

// Load parses environment variables into Config.
//
// Required variables:
//   * PYTHON_AGENT_URL - URL of the Python FastAPI service.
func Load() Config {
    cfg := Config{
        PythonAgentURL: os.Getenv("PYTHON_AGENT_URL"),
    }
    if cfg.PythonAgentURL == "" {
        log.Println("warning: PYTHON_AGENT_URL not set; assuming http://localhost:8000")
        cfg.PythonAgentURL = "http://localhost:8000"
    }
    return cfg
}
