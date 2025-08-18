"""Chat service implementation.

This module keeps an in-memory history per session and returns a simple
response. In production it would connect to an Ollama model through
LangChain and enforce the 20-turn limit described in the requirements.
"""

from __future__ import annotations

from collections import deque
from typing import Deque, Dict, Tuple

from ..models import ChatRequest, ChatResponse

# In-memory history mapping session id to deque of (question, answer) tuples.
_HISTORY: Dict[str, Deque[Tuple[str, str]]] = {}
_MAX_TURNS = 20


def _get_history(session_id: str) -> Deque[Tuple[str, str]]:
    """Retrieve the conversation history for *session_id*.

    A new deque is created automatically when the session is first used.
    """

    return _HISTORY.setdefault(session_id, deque(maxlen=_MAX_TURNS))


async def chat(request: ChatRequest) -> ChatResponse:
    """Generate a chat response.

    This stub implementation simply echoes the user's question. Real logic
    would call the configured LLM and incorporate resume/LinkedIn data.
    """

    history = _get_history(request.session_id)
    answer = f"You said: {request.question}"
    history.append((request.question, answer))
    return ChatResponse(answer=answer)
