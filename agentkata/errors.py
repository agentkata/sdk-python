"""Public error types for the AgentKata Python SDK."""

from __future__ import annotations

from typing import Any

from agentkata_generated.exceptions import ApiException
from agentkata_generated.models.error_envelope import ErrorEnvelope


class AgentKataAPIError(Exception):
    """Structured API error raised by the public SDK wrapper."""

    def __init__(
        self,
        *,
        status_code: int,
        code: str = "",
        message: str = "",
        hint: str = "",
        meta: dict[str, Any] | None = None,
        data: Any = None,
    ) -> None:
        self.status_code = status_code
        self.code = code
        self.message = message
        self.hint = hint
        self.meta = meta
        self.data = data
        super().__init__(self._build_message())

    @classmethod
    def from_generated(cls, exc: ApiException) -> AgentKataAPIError:
        envelope = exc.data if isinstance(exc.data, ErrorEnvelope) else None
        error = envelope.error if envelope is not None else None
        meta = envelope.meta.to_dict() if envelope is not None and envelope.meta is not None else None
        data = _to_plain_data(envelope.data) if envelope is not None else None

        return cls(
            status_code=int(exc.status or 0),
            code=error.code if error is not None else "",
            message=error.message if error is not None else str(exc.reason or exc),
            hint=error.hint or "" if error is not None else "",
            meta=meta,
            data=data,
        )

    def _build_message(self) -> str:
        parts = []
        if self.status_code:
            parts.append(f"HTTP {self.status_code}")
        if self.code:
            parts.append(self.code)
        if self.message:
            parts.append(self.message)
        if self.hint:
            parts.append(f"hint={self.hint}")
        return ": ".join(parts) if parts else "AgentKata API request failed"


def _to_plain_data(value: Any) -> Any:
    if value is None:
        return None
    if hasattr(value, 'to_dict') and callable(value.to_dict):
        return value.to_dict()
    if hasattr(value, 'model_dump') and callable(value.model_dump):
        return value.model_dump(mode='json')
    return value
