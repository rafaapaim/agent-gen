# Research: Wait for Chat Model Startup

## Current Behavior

- `OllamaService._request()` in `backend/src/services/ollama_service.py` passes `timeout=10` to `urllib.request.urlopen()` for all Ollama calls.
- `OllamaService.chat()` uses that shared helper to make the synchronous `/api/chat` request.
- The new logs report the Ollama client connection closing after about 10.65 seconds while a large model was still starting. Ollama then cancels its load with `context canceled` and records HTTP 499.
- The observed elapsed time closely matches the backend's ten-second socket timeout. This points to the backend closing the upstream request, rather than a model load failure.
- The browser `fetch()` call in `frontend/src/api.js` does not set an explicit timeout, so the observed short deadline is in the backend's Ollama HTTP request.
- The chat UI currently gives no in-progress feedback and does not disable repeated submission or agent selection while a request is pending.

## Decisions

### Decision: Apply a 300-second socket timeout to chat only

**Rationale**: A 10-second deadline is too short for first-use loading of a multi-gigabyte local model. Five minutes is a finite, conservative bound for local cold starts and initial generation without changing the responsiveness of health and agent-list requests. The existing `urllib` timeout applies to socket operations and bounds a request that is waiting without a response.

**Alternatives considered**:
- Increase the global timeout: rejected because status and list operations should remain quick and fail promptly if Ollama is unavailable.
- Remove the timeout: rejected because a stuck model service could leave requests pending indefinitely.
- Add a configurable environment variable: rejected for the initial fix because one explicit bound is enough to correct the observed behavior without expanding configuration surface.

### Decision: Return a distinct gateway timeout for chat deadline expiry

**Rationale**: A request that exceeded its wait limit is not proof that Ollama is unreachable. Reporting a distinct timeout (HTTP 504) lets the UI tell users the agent may still be starting and to retry, while reserving 503 for service connectivity failure.

**Alternatives considered**:
- Continue mapping socket timeouts to HTTP 503: rejected because it incorrectly reports a confirmed outage.
- Return HTTP 200 with an error-shaped payload: rejected because it would make a failed request appear successful to clients.

### Decision: Keep the current synchronous request/response contract

**Rationale**: The existing browser can keep a fetch pending while the backend waits. This directly addresses the connection close shown in the logs without introducing polling, background jobs, or persistence.

**Alternatives considered**:
- Add asynchronous job creation and polling: rejected as disproportionate to a single local request timeout and as additional state the application does not need.
- Stream startup progress: deferred because Ollama's existing non-streaming response does not provide model-loading progress through the current integration.

### Decision: Show pending state and prevent duplicate or misrouted UI actions

**Rationale**: A long first response needs visible progress. Disabling the send action and agent switching while the request is pending prevents accidental duplicate requests and ensures a late response cannot be appended to another agent's conversation.

**Alternatives considered**:
- Keep controls enabled and rely on users not to click again: rejected because long waits make duplicate submissions likely.
- Permit changing agents and attempt to reconcile global message history later: rejected because the current UI holds a single conversation state and does not associate history per agent.

## Validation Strategy

- Verify the chat path passes the explicit 300-second timeout to the HTTP client while health and list calls retain the existing ten-second timeout.
- Mock a delayed response that completes before the chat deadline and verify a normal HTTP 200 response.
- Mock a socket timeout and verify HTTP 504 with an actionable startup/retry message; verify connection-refused failures remain HTTP 503.
- Verify malformed upstream responses continue to use the existing bad-gateway handling.
- Exercise the UI's pending state, duplicate-submit prevention, preserved message, timeout recovery, and selected-agent consistency.
- Run the full pytest suite and JavaScript syntax validation. Perform a real cold-start test only when Ollama and a model are available.
