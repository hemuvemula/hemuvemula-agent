"""Pydantic request and response models used by the agent service."""
from __future__ import annotations

from pydantic import BaseModel, Field
from typing import List


class ChatRequest(BaseModel):
    """Input schema for :func:`chat`.

    Attributes
    ----------
    session_id: str
        Identifier for the client session. Used to maintain conversation
        history across requests.
    question: str
        Natural language prompt from the user.
    """

    session_id: str = Field(..., description="Conversation session identifier")
    question: str = Field(..., description="Question posed by the user")


class ChatResponse(BaseModel):
    """Response schema for :func:`chat`."""

    answer: str


class ResumeParseResponse(BaseModel):
    """Model describing the result of resume parsing."""

    paragraphs: List[str]
