# Personal Agent Design

This document outlines the high-level architecture of the personal agent
system. The repository contains three microservices:

- **Python Agent** (`agent/`): FastAPI application responsible for parsing the
  resume, synchronising LinkedIn data and answering chat questions. It exposes
  HTTP endpoints and interacts with an Ollama LLM through LangChain (stubbed in
  this prototype).
- **Go Backend** (`backend/`): Provides REST endpoints for the web UI and
  proxies requests to the Python agent. LittleHorse workflow orchestration is
  planned for future integration.
- **Web UI** (`web/`): Vue single page application that allows anyone to ask
  questions about the profile.

All services expose Prometheus metrics, emit JSON structured logs and can be
instrumented with OpenTelemetry traces. Configuration is supplied via
environment variables; no secrets are checked into source control.
