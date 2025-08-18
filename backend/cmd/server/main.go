package main

// Command server starts the Go backend service. It wires together the
// configuration, HTTP router and proxies to the Python agent.

import (
    "log"
    "net/http"

    "github.com/example/hemuvemula-agent/backend/internal/api"
    "github.com/example/hemuvemula-agent/backend/internal/config"
)

func main() {
    cfg := config.Load()
    r := api.NewRouter(cfg)

    log.Println("starting backend on :8080")
    if err := http.ListenAndServe(":8080", r); err != nil {
        log.Fatal(err)
    }
}
