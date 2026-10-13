"""Connectivity and model management helpers for the public API."""

from __future__ import annotations

import http.client
import json
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

from backend.src.models.agent import Agent

OLLAMA_URL = "http://localhost:11434"


class ChatAgentUnavailable(Exception):
    """Raised when Ollama does not recognize the requested agent."""


class ChatServiceUnavailable(Exception):
    """Raised when the local Ollama service cannot be reached."""


class ChatRequestTimeout(Exception):
    """Raised when the bounded wait for a chat response expires."""


class ChatUpstreamError(Exception):
    """Raised when Ollama returns an unusable or unsuccessful response."""


class OllamaService:
    """Thin adapter for the local Ollama runtime."""

    def __init__(self, base_url: str = OLLAMA_URL) -> None:
        self.base_url = base_url.rstrip("/")

    def _request(
        self,
        path: str,
        *,
        method: str = "GET",
        payload: dict[str, Any] | None = None,
        timeout: float = 10,
    ) -> Any:
        body = None
        headers = {"Content-Type": "application/json"}
        if payload is not None:
            body = json.dumps(payload).encode("utf-8")

        request = urllib.request.Request(
            f"{self.base_url}{path}",
            data=body,
            headers=headers,
            method=method,
        )
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return json.load(response)

    def health(self) -> dict[str, Any]:
        try:
            data = self._request("/api/tags")
        except (urllib.error.URLError, TimeoutError, ConnectionError, OSError):
            return {"connected": False, "message": "Ollama is not available on localhost:11434"}

        if data is None:
            return {"connected": False, "message": "Ollama responded with empty data"}
        return {"connected": True, "message": "Ollama is available"}

    def list_models(self) -> list[Agent]:
        data = self._request("/api/tags")
        return [Agent(name=item["name"], status="available") for item in data.get("models", [])]

    def create_agent(self, name: str, modelfile_path: str) -> Agent:
        modelfile = Path(modelfile_path).expanduser().resolve(strict=True)
        if not modelfile.is_file():
            raise FileNotFoundError(f"Modelfile not found: {modelfile}")

        normalized_name = name.strip()
        if not normalized_name:
            raise ValueError("Agent name cannot be empty")

        if self._agent_exists(normalized_name):
            raise ValueError(f"Agent '{normalized_name}' already exists")

        command = ["ollama", "create", normalized_name, "-f", str(modelfile)]
        import subprocess

        result = subprocess.run(command, shell=False, capture_output=True, text=True, check=False)
        if result.returncode != 0:
            detail = (result.stderr or result.stdout).strip() or "Unknown creation error"
            raise ValueError(detail)
        return Agent(name=normalized_name, status="available")

    def delete_agent(self, agent_name: str) -> str:
        if not agent_name:
            raise ValueError("Agent name cannot be empty")
        if not self._agent_exists(agent_name):
            raise ValueError(f"Agent '{agent_name}' is not installed")

        result = subprocess.run(["ollama", "rm", agent_name], shell=False, capture_output=True, text=True, check=False)
        if result.returncode != 0:
            detail = (result.stderr or result.stdout).strip() or "Unknown removal error"
            raise ValueError(detail)
        return agent_name

    def chat(self, agent_name: str, message: str) -> dict[str, str]:
        payload = {
            "model": agent_name,
            "messages": [{"role": "user", "content": message}],
            "stream": False,
        }
        try:
            response = self._request("/api/chat", method="POST", payload=payload, timeout=300)
        except urllib.error.HTTPError as exc:
            if exc.code == 404:
                raise ChatAgentUnavailable(
                    "The selected agent is unavailable. Select an installed agent or install it, then try again."
                ) from exc
            raise ChatUpstreamError(
                "The local model service could not complete the request. Check the selected agent and try again."
            ) from exc
        except TimeoutError as exc:
            raise ChatRequestTimeout(
                "The agent is taking too long to start or respond. Check Ollama and try again."
            ) from exc
        except urllib.error.URLError as exc:
            if isinstance(exc.reason, TimeoutError):
                raise ChatRequestTimeout(
                    "The agent is taking too long to start or respond. Check Ollama and try again."
                ) from exc
            raise ChatServiceUnavailable(
                "The local Ollama service is unavailable. Start or check Ollama, then try again."
            ) from exc
        except (ConnectionError, OSError) as exc:
            raise ChatServiceUnavailable(
                "The local Ollama service is unavailable. Start or check Ollama, then try again."
            ) from exc
        except (http.client.HTTPException, ValueError, TypeError) as exc:
            raise ChatUpstreamError(
                "The local model service returned an unusable response. Check the selected agent and try again."
            ) from exc

        if not isinstance(response, dict):
            raise ChatUpstreamError(
                "The local model service returned an unusable response. Check the selected agent and try again."
            )
        msg = response.get("message")
        if not isinstance(msg, dict):
            raise ChatUpstreamError(
                "The local model service returned an unusable response. Check the selected agent and try again."
            )
        content = msg.get("content")
        if not isinstance(content, str) or not content.strip():
            raise ChatUpstreamError(
                "The local model service returned an unusable response. Check the selected agent and try again."
            )
        return {
            "role": "assistant",
            "content": content,
        }

    def _agent_exists(self, name: str) -> bool:
        try:
            models = self.list_models()
        except Exception:
            return False
        return any(agent.name == name for agent in models)
