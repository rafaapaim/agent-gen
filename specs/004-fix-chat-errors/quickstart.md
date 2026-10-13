# Chat Failure Fix: Validation Quickstart

## Prerequisites

- Python 3.11 or newer
- Project dependencies installed from `backend/requirements.txt`
- A local Ollama installation
- At least one installed Ollama model for the successful chat scenario

## Start the services

From the repository root, start Ollama if it is not already running:

```powershell
ollama serve
```

In another terminal, start the backend:

```powershell
.\.venv\Scripts\python.exe -m uvicorn backend.src.main:app --reload --host 127.0.0.1 --port 8000
```

Serve the static browser UI from a separate terminal:

```powershell
.\.venv\Scripts\python.exe -m http.server 5500
```

Open `http://127.0.0.1:5500/frontend/public/index.html` and select an installed agent.

## Automated validation

Run the focused API tests from the repository root:

```powershell
.\.venv\Scripts\python.exe -m pytest backend/tests/test_api.py -q
```

Expected outcome: tests pass for successful chat, invalid request fields, unknown agent, service connectivity failure, and unusable upstream response.

## Manual scenarios

1. **Successful chat**: Choose an installed agent and send a short message. The assistant response appears after the user message.
2. **Unknown agent**: Submit a request for an agent that is not installed. The API/UI identifies the missing agent and suggests selecting or installing one; the conversation remains visible.
3. **Unavailable model service**: Stop Ollama and send a message. The UI explains that the local service is unavailable and suggests starting/checking it.
4. **Retry and recover**: Restart Ollama or select an available agent and send another message. The previous conversation and failed user message remain available.

Refer to [chat-contract.md](./contracts/chat-contract.md) for exact response statuses and shapes and [data-model.md](./data-model.md) for request and failure semantics.
