"""Main application entry point for the local web backend."""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.src.api.agent_routes import router as agent_router
from backend.src.api.chat_routes import router as chat_router
from backend.src.api.system_routes import router as system_router

app = FastAPI(title="Ollama Agent Manager UI", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(system_router)
app.include_router(agent_router)
app.include_router(chat_router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("backend.src.main:app", host="127.0.0.1", port=8000, reload=True)
