from typing import Literal

from pydantic import BaseModel, Field, field_validator, model_validator


class AssistRequest(BaseModel):
    mode: Literal["challenge", "options", "pre-mortem"] = "challenge"
    objective: str = Field(min_length=10, max_length=1500)
    context: str = Field(default="", max_length=2500)
    confirmed_safe_input: bool = False

    @field_validator("objective", "context")
    @classmethod
    def normalize_text(cls, value: str) -> str:
        return value.strip()

    @model_validator(mode="after")
    def require_safety_confirmation(self) -> "AssistRequest":
        if not self.confirmed_safe_input:
            raise ValueError("Confirm that the input contains no secrets or personal data.")
        return self


class AssistResponse(BaseModel):
    advice: str
    model: str
    redactions_applied: int
    requires_human_review: Literal[True] = True
    request_id: str


class HealthResponse(BaseModel):
    status: Literal["ok"] = "ok"
    ai_configured: bool
    environment: str
