"""Main entrypoint for Python agent service.

This FastAPI application exposes endpoints for resume parsing, LinkedIn
synchronisation and conversational chat. It keeps the implementation
intentionally simple yet provides extensive comments to serve as a
production‑grade starting point.
"""

from __future__ import annotations

from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

from .models import ChatRequest, ChatResponse, ResumeParseResponse
from .services import chat as chat_service
from .services import resume as resume_service

app = FastAPI(title="Personal Agent", version="0.1.0")

RESUME_PATH = Path("resources/resume/resume.docx")


@app.on_event("startup")
async def startup_event() -> None:
    """Application start‑up hook.

    The resume is parsed when the service starts so that the information is
    readily available for subsequent chat requests.
    """
    if RESUME_PATH.exists():
        await resume_service.parse_and_store(RESUME_PATH)
    else:
        app.logger.warning("Resume file not found: %s", RESUME_PATH)


@app.get("/health", summary="Health check")
async def health() -> JSONResponse:
    """Simple health end‑point used by container orchestrators."""
    return JSONResponse({"status": "ok"})


@app.post("/parse-resume", response_model=ResumeParseResponse)
async def parse_resume() -> ResumeParseResponse:
    """Trigger resume parsing on demand.

    Returns the parsed structure or raises a 404 if the resume file is
    missing.
    """
    if not RESUME_PATH.exists():
        raise HTTPException(status_code=404, detail="Resume file missing")
    return await resume_service.parse_and_store(RESUME_PATH)


@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest) -> ChatResponse:
    """Main chat endpoint.

    Delegates to :mod:`services.chat` which maintains conversation history and
    interacts with the configured LLM (Ollama by default).
    """
    return await chat_service.chat(req)


@app.post("/sync-linkedin")
async def sync_linkedin() -> JSONResponse:
    """Placeholder endpoint for LinkedIn synchronisation.

    The real implementation would fetch profile data using LinkedIn's API and
    persist a new version in MongoDB. Here we simply return a stub response.
    """
    # TODO: Implement LinkedIn API integration.
    return JSONResponse({"status": "not-implemented"})
