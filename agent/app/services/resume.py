"""Resume parsing service.

The function defined here reads a Word document (`.docx`) and returns the
paragraphs as plain text. In a real system this module would include
sophisticated extraction logic and persist data into MongoDB. The current
implementation is intentionally light-weight but heavily documented for
clarity and future extension.
"""

from __future__ import annotations

from pathlib import Path
from typing import List

import docx
from pydantic import BaseModel

from ..models import ResumeParseResponse


class ParsedResume(BaseModel):
    """Pydantic model representing the parsed resume."""

    paragraphs: List[str]


async def parse_and_store(path: Path) -> ResumeParseResponse:
    """Parse the resume file and return its content.

    Parameters
    ----------
    path:
        Location of the `.docx` resume file.

    Returns
    -------
    ResumeParseResponse
        Pydantic model containing paragraph text.
    """

    document = docx.Document(path)
    paragraphs = [p.text for p in document.paragraphs if p.text]
    # TODO: persist to MongoDB with versioning
    return ResumeParseResponse(paragraphs=paragraphs)
