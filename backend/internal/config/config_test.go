package config

import (
    "os"
    "testing"
)

// TestLoad verifies that default values are applied when env vars are missing.
func TestLoad(t *testing.T) {
    os.Unsetenv("PYTHON_AGENT_URL")
    cfg := Load()
    if cfg.PythonAgentURL == "" {
        t.Fatalf("expected default PythonAgentURL, got empty")
    }
}
