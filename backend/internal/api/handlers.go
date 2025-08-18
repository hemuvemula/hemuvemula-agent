package api

import (
    "encoding/json"
    "net/http"

    "github.com/go-chi/chi/v5"
    "github.com/go-chi/chi/v5/middleware"

    "github.com/example/hemuvemula-agent/backend/internal/config"
    "github.com/example/hemuvemula-agent/backend/internal/proxy"
)

// NewRouter constructs the HTTP routes for the backend service.
func NewRouter(cfg config.Config) http.Handler {
    r := chi.NewRouter()
    r.Use(middleware.Logger)

    client := proxy.NewClient(cfg.PythonAgentURL)

    r.Get("/api/health", func(w http.ResponseWriter, _ *http.Request) {
        w.WriteHeader(http.StatusOK)
        w.Write([]byte("ok"))
    })

    r.Post("/api/chat", func(w http.ResponseWriter, r *http.Request) {
        var payload map[string]any
        if err := json.NewDecoder(r.Body).Decode(&payload); err != nil {
            http.Error(w, err.Error(), http.StatusBadRequest)
            return
        }
        var out map[string]any
        if err := client.PostJSON(r.Context(), "/chat", payload, &out); err != nil {
            http.Error(w, err.Error(), http.StatusBadGateway)
            return
        }
        w.Header().Set("Content-Type", "application/json")
        json.NewEncoder(w).Encode(out)
    })

    r.Post("/api/resume/refresh", func(w http.ResponseWriter, r *http.Request) {
        var out map[string]any
        if err := client.PostJSON(r.Context(), "/parse-resume", nil, &out); err != nil {
            http.Error(w, err.Error(), http.StatusBadGateway)
            return
        }
        w.Header().Set("Content-Type", "application/json")
        json.NewEncoder(w).Encode(out)
    })

    return r
}
