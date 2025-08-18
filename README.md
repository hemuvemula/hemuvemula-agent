# hemuvemula-agent

A minimal multi-service stack demonstrating a personal agent capable of
answering questions about a resume and LinkedIn profile. The project uses a Go
backend, a Python FastAPI agent and a Vue web front‑end. This repository is a
starting point and not a complete production deployment.

## Services

- **agent/** – FastAPI application with endpoints for parsing a local resume,
  proxying chat to an Ollama model and (stubbed) LinkedIn synchronisation.
- **backend/** – Go service using the chi router. Acts as an API gateway and
  proxy to the Python agent. Workflow orchestration via LittleHorse can be
  integrated here.
- **web/** – Placeholder Vue application.
- **deploy/** – Docker Compose configuration for running the stack locally.

## Running Tests

Python tests:

```bash
pip install -r agent/requirements.txt
pytest agent/tests
```

Go tests:

```bash
(cd backend && go test ./...)
```

The Docker Compose file in `deploy/` can be used for local development:

```bash
cd deploy
podman compose up --build
```
