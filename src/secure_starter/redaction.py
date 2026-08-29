import re
from dataclasses import dataclass


@dataclass(frozen=True)
class RedactionResult:
    text: str
    count: int


_PATTERNS: tuple[tuple[re.Pattern[str], str], ...] = (
    (re.compile(r"\bsk-[A-Za-z0-9_-]{16,}\b"), "[REDACTED_API_KEY]"),
    (re.compile(r"(?i)\bBearer\s+[A-Za-z0-9._~+/=-]{12,}"), "Bearer [REDACTED_TOKEN]"),
    (
        re.compile(
            r"(?i)\b(api[_-]?key|token|password|secret)\b\s*[:=]\s*"
            r"[\"']?([^\s,;\"']{8,})"
        ),
        r"\1=[REDACTED_SECRET]",
    ),
    (
        re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.IGNORECASE),
        "[REDACTED_EMAIL]",
    ),
)


def redact_text(value: str) -> RedactionResult:
    """Redact a documented set of high-risk patterns before an AI request."""

    redacted = value
    total = 0
    for pattern, replacement in _PATTERNS:
        redacted, count = pattern.subn(replacement, redacted)
        total += count
    return RedactionResult(text=redacted, count=total)
