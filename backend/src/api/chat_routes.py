"""API routes for conversation management."""

from __future__ import annotations

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from backend.src.services.ollama_service import (
    ChatAgentUnavailable,
    ChatRequestTimeout,
    ChatServiceUnavailable,
    ChatUpstreamError,
    OllamaService,
)

router = APIRouter(prefix="/api")
service = OllamaService()


@router.post("/chat", response_model=None)
def chat(payload: dict[str, str]) -> dict[str, str] | JSONResponse:
    agent_name = (payload.get("agentName") or "").strip()
    message = (payload.get("message") or "").strip()

    if not agent_name or not message:
        return JSONResponse(status_code=400, content={"error": "Agent name and message are required."})

    try:
        response = service.chat(agent_name, message)
    except ChatAgentUnavailable as exc:
        return JSONResponse(status_code=404, content={"error": str(exc)})
    except ChatRequestTimeout as exc:
        return JSONResponse(status_code=504, content={"error": str(exc)})
    except ChatServiceUnavailable as exc:
        return JSONResponse(status_code=503, content={"error": str(exc)})
    except ChatUpstreamError as exc:
        return JSONResponse(status_code=502, content={"error": str(exc)})
    return response
