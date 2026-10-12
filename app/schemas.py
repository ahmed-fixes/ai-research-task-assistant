from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field

from app.services.llm_service import ask_llm

class AgentRunRequest(BaseModel):

    message: str = Field(
        min_length=1,
        max_length=5000,
        description="User's request."
    )


class AgentChatRequest(BaseModel):

    session_id: str = Field(
        min_length=1,
        max_length=100,
        description="Existing session identifier."
    )

    message: str = Field(
        min_length=1,
        max_length=5000,
        description="User's request."
    )


class AgentResponse(BaseModel):

    answer: str

    actions: list[str] = Field(
        default_factory=list
    )

    sources: list[dict[str, Any]] = Field(
        default_factory=list
    )

    session_id: str

    step_count: int

    error: str | None = None


class SessionResponse(BaseModel):

    session_id: str

    messages: list[dict[str, str]] = Field(
        default_factory=list
    )

    step_count: int

    route: str = ""

    actions: list[str] = Field(
        default_factory=list
    )


# -------------------------
# Document Schemas
# -------------------------

class DocumentCreate(BaseModel):

    filename: str = Field(
        min_length=1,
        max_length=255
    )

    content: str = Field(
        min_length=1
    )


class DocumentResponse(BaseModel):

    id: str

    filename: str

    content: str

    created_at: datetime