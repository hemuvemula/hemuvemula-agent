"""Unit tests for FastAPI app."""

from pathlib import Path
import os, sys
sys.path.append(os.path.abspath("."))

import pytest
from fastapi.testclient import TestClient

from agent.app.main import app, RESUME_PATH

client = TestClient(app)


def setup_module(module):  # noqa: D401 - pytest hook
    """Ensure sample resume exists before tests run."""
    RESUME_PATH.parent.mkdir(parents=True, exist_ok=True)
    if not RESUME_PATH.exists():
        # Create a minimal Word document for parsing tests.
        import docx

        doc = docx.Document()
        doc.add_paragraph("This is a test resume.")
        doc.save(RESUME_PATH)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_parse_resume():
    response = client.post("/parse-resume")
    assert response.status_code == 200
    assert response.json()["paragraphs"]


def test_chat_echo():
    payload = {"session_id": "abc", "question": "Hello"}
    response = client.post("/chat", json=payload)
    assert response.status_code == 200
    assert response.json()["answer"] == "You said: Hello"
