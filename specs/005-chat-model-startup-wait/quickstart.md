# Chat Model Startup Wait: Validation Quickstart

## Prerequisites

- Python 3.11 or newer and project dependencies installed
- Ollama running locally
- A locally installed agent; use a large or cold model to exercise startup delay

## Start the application

From the repository root, start the backend:

```powershell
.\.venv\Scripts\python.exe -m uvicorn backend.src.main:app --reload --host 127.0.0.1 --port 8000
```

In another terminal, serve the browser UI:

```powershell
.\.venv\Scripts\python.exe -m http.server 5500
```

Open `http://127.0.0.1:5500/frontend/public/index.html`.

## Automated validation

Run the API tests:

```powershell
.\.venv\Scripts\python.exe -m pytest backend/tests/test_api.py -q
```

Expected results:

- A delayed chat response received before the five-minute bound returns normally.
- A chat timeout returns HTTP 504 with a retryable message.
- A connection failure remains HTTP 503.
- Chat requests use a 300-second timeout; health and agent-list requests keep their existing 10-second timeout.
- The browser shows pending feedback and disables message submission and agent selection until the request resolves.
- A timed-out message remains visible and can be retried without adding a duplicate user entry.
- Existing API tests continue to pass.

## Manual cold-start scenario

1. Restart Ollama or otherwise ensure the chosen model is not already loaded in memory.
2. Select the model in the browser and send one short message.
3. Confirm the UI indicates that the request is pending and the send and agent-selection controls cannot submit a duplicate or change the active agent.
4. Wait for the model to load. Confirm the response appears once after the user message.
5. If the wait limit is reached, confirm the UI reports a timeout, retains the submitted message, and permits retry.
6. Retry after the model is ready and confirm the response is added once without duplicating the original user message.

The exact request status and error payloads are defined in [chat-wait-contract.md](./contracts/chat-wait-contract.md); transient request lifecycle is described in [data-model.md](./data-model.md).

## Recorded Validation

- The full Python test suite passed 34 tests, and the frontend JavaScript syntax check passed.
- A live backend chat request to an installed local model returned HTTP 200 in 95.22 seconds. The model was not explicitly unloaded before the request, so the run does not establish a controlled cold start.
- In the browser, the pending status and disabled controls were visible while a chat request was active; the response appeared once and controls were restored.
