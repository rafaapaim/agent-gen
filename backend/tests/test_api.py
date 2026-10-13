from __future__ import annotations

import socket
import time
from io import BytesIO
from urllib.error import HTTPError, URLError
from unittest.mock import patch

from fastapi.testclient import TestClient

from backend.src.main import app
from backend.src.services.ollama_service import OllamaService

client = TestClient(app)


def test_ollama_request_uses_default_and_explicit_timeouts():
    service = OllamaService()

    with patch(
        "backend.src.services.ollama_service.urllib.request.urlopen",
        side_effect=lambda *args, **kwargs: BytesIO(b"{}"),
    ) as urlopen:
        service._request("/api/tags")
        assert urlopen.call_args.kwargs["timeout"] == 10

        service._request("/api/chat", method="POST", payload={}, timeout=300)
        assert urlopen.call_args.kwargs["timeout"] == 300


def test_health_and_agent_listing_keep_the_default_timeout():
    service = OllamaService()
    with patch(
        "backend.src.services.ollama_service.urllib.request.urlopen",
        side_effect=lambda *args, **kwargs: BytesIO(b'{"models": []}'),
    ) as urlopen:
        service.health()
        service.list_models()

    assert [call.kwargs["timeout"] for call in urlopen.call_args_list] == [10, 10]


def test_health_status_reports_dependency_state():
    with patch(
        "backend.src.services.ollama_service.OllamaService.health",
        return_value={"connected": True, "message": "Ollama is available"},
    ):
        response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json()["connected"] is True


def test_list_agents_returns_installed_models():
    payload = [
        {
            "name": "llama3.2",
            "status": "available",
            "source": "installed",
            "createdAt": "2026-10-12T00:00:00Z",
        }
    ]

    with patch("backend.src.api.agent_routes.service.list_models", return_value=[type("Agent", (), {"to_dict": lambda self: payload[0]})()]):
        response = client.get("/api/agents")

    assert response.status_code == 200
    assert response.json()[0]["name"] == "llama3.2"


def test_create_agent_validates_required_fields():
    response = client.post("/api/agents", json={"name": "", "modelfilePath": ""})

    assert response.status_code == 400
    assert "error" in response.json()


def test_chat_requires_agent_and_message():
    response = client.post("/api/chat", json={"agentName": "", "message": ""})

    assert response.status_code == 400
    assert response.json()["error"] == "Agent name and message are required."


def test_chat_returns_successful_responses_for_sequential_messages():
    responses = [
        {"message": {"content": "First answer"}},
        {"message": {"content": "Second answer"}},
    ]

    with patch("backend.src.api.chat_routes.service._request", side_effect=responses) as request:
        first = client.post("/api/chat", json={"agentName": "llama3.2", "message": "First question"})
        second = client.post("/api/chat", json={"agentName": "llama3.2", "message": "Second question"})

    assert first.status_code == 200
    assert first.json() == {"role": "assistant", "content": "First answer"}
    assert second.status_code == 200
    assert second.json() == {"role": "assistant", "content": "Second answer"}
    assert request.call_count == 2
    assert all(call.kwargs["timeout"] == 300 for call in request.call_args_list)


def test_chat_returns_success_after_a_short_startup_delay():
    def delayed_response(*args, **kwargs):
        assert kwargs["timeout"] == 300
        time.sleep(0.01)
        return {"message": {"content": "Ready"}}

    with patch("backend.src.api.chat_routes.service._request", side_effect=delayed_response):
        response = client.post("/api/chat", json={"agentName": "llama3.2", "message": "Hello"})

    assert response.status_code == 200
    assert response.json() == {"role": "assistant", "content": "Ready"}


def test_chat_maps_unknown_agent_to_not_found_without_exposing_upstream_body():
    upstream_error = HTTPError(
        url="http://localhost:11434/api/chat",
        code=404,
        msg="Not Found",
        hdrs=None,
        fp=BytesIO(b'{"error":"model secret-internal-detail not found"}'),
    )

    with patch("backend.src.api.chat_routes.service._request", side_effect=upstream_error):
        response = client.post("/api/chat", json={"agentName": "missing-agent", "message": "Hello"})

    assert response.status_code == 404
    assert "agent" in response.json()["error"].lower()
    assert "secret-internal-detail" not in response.json()["error"]


def test_chat_maps_connection_failure_to_service_unavailable():
    for failure in (URLError("connection refused"), ConnectionRefusedError("connection refused")):
        with patch("backend.src.api.chat_routes.service._request", side_effect=failure):
            response = client.post("/api/chat", json={"agentName": "llama3.2", "message": "Hello"})

        assert response.status_code == 503
        assert "ollama" in response.json()["error"].lower()
        assert "connection refused" not in response.json()["error"].lower()


def test_chat_maps_socket_timeout_to_gateway_timeout():
    for failure in (TimeoutError("upstream timeout"), socket.timeout("upstream timeout"), URLError(socket.timeout())):
        with patch("backend.src.api.chat_routes.service._request", side_effect=failure):
            response = client.post("/api/chat", json={"agentName": "llama3.2", "message": "Hello"})

        assert response.status_code == 504
        assert "try again" in response.json()["error"].lower()
        assert "timeout" not in response.json()["error"].lower()


def test_chat_maps_other_upstream_http_failures_to_bad_gateway():
    upstream_error = HTTPError(
        url="http://localhost:11434/api/chat",
        code=500,
        msg="Internal Server Error",
        hdrs=None,
        fp=BytesIO(b'{"error":"internal detail"}'),
    )

    with patch("backend.src.api.chat_routes.service._request", side_effect=upstream_error):
        response = client.post("/api/chat", json={"agentName": "llama3.2", "message": "Hello"})

    assert response.status_code == 502
    assert "try again" in response.json()["error"].lower()
    assert "internal detail" not in response.json()["error"]


def test_chat_rejects_empty_or_malformed_upstream_responses():
    for upstream_response in ({}, {"message": {"content": ""}}, {"message": None}, None):
        with patch("backend.src.api.chat_routes.service._request", return_value=upstream_response):
            response = client.post("/api/chat", json={"agentName": "llama3.2", "message": "Hello"})

        assert response.status_code == 502
        assert response.json()["error"]
