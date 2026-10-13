"""System endpoints for frontend status and dependency checks."""

from __future__ import annotations

from fastapi import APIRouter

from backend.src.services.ollama_service import OllamaService

router = APIRouter(prefix="/api")
service = OllamaService()


@router.get("/health")
def health() -> dict[str, object]:
    return service.health()
