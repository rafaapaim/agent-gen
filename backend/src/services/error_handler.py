"""Structured error handling for the web backend."""

from __future__ import annotations

from typing import Any


class AppError(Exception):
    """Domain-level error returned to the API layer."""

    def __init__(self, message: str, status_code: int = 400, *, details: Any | None = None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.details = details


def error_response(message: str, status_code: int = 400, *, details: Any | None = None) -> dict[str, Any]:
    payload: dict[str, Any] = {"error": message}
    if details is not None:
        payload["details"] = details
    return payload
