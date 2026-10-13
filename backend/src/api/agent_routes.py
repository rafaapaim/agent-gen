"""API routes for agent listing and management."""

from __future__ import annotations

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from backend.src.services.ollama_service import OllamaService

router = APIRouter(prefix="/api")
service = OllamaService()


@router.get("/agents")
def list_agents() -> list[dict[str, object]]:
    try:
        agents = service.list_models()
    except Exception as exc:  # pragma: no cover - API boundary
        return JSONResponse(status_code=503, content={"error": str(exc)})
    return [agent.to_dict() for agent in agents]


@router.post("/agents", response_model=None)
def create_agent(payload: dict[str, str]) -> dict[str, object] | JSONResponse:
    name = (payload.get("name") or "").strip()
    modelfile_path = (payload.get("modelfilePath") or "").strip()

    if not name or not modelfile_path:
        return JSONResponse(status_code=400, content={"error": "Name and Modelfile are required."})

    try:
        agent = service.create_agent(name, modelfile_path)
    except (FileNotFoundError, ValueError) as exc:
        return JSONResponse(status_code=400, content={"error": str(exc)})
    return {"name": agent.name, "status": agent.status}


@router.delete("/agents/{agent_name}", response_model=None)
def delete_agent(agent_name: str) -> dict[str, object] | JSONResponse:
    try:
        service.delete_agent(agent_name)
    except ValueError as exc:
        return JSONResponse(status_code=400, content={"error": str(exc)})
    return {"deleted": True, "agentName": agent_name}

