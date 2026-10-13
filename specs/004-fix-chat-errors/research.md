# Research: Fix Chat Request Failures

## Current Behavior

- The chat route in `backend/src/api/chat_routes.py` validates missing agent names and messages as HTTP 400.
- The route catches `ValueError` from `OllamaService.chat()` and returns HTTP 503 with an `error` field for every caught failure.
- `OllamaService.chat()` catches `urllib.error.URLError`, `TimeoutError`, `ConnectionError`, `OSError`, and `ValueError`, then wraps each in `ValueError`.
- `urllib.error.HTTPError` is a subclass of `URLError`. As a result, upstream HTTP failures such as an unknown model response can be converted into the same `ValueError` as a connection failure and surfaced as HTTP 503.
- The supplied logs do not include the body of the 503 response or Ollama's upstream response. The exact cause of that particular request therefore cannot be established from the logs alone.
- The browser API client reads `payload.error` for non-success responses. The chat handler preserves the submitted user message in browser state when a request fails and displays the returned message in its error banner.

## Decisions

### Decision: Preserve error categories from the Ollama service through the API boundary

**Rationale**: Mapping every failure to `ValueError` erases the distinction between network outages, upstream rejections, missing agents, and malformed responses. Preserve or expose sufficient structured failure information so the route can map known conditions to the contract's status and safe message.

**Alternatives considered**:
- Continue raising generic `ValueError` and infer the cause from its message: rejected because message text is not a reliable classification contract.
- Return HTTP 503 for all upstream failures: rejected because invalid agent names and invalid upstream responses are not service outages.

### Decision: Use HTTP status codes by cause and keep the JSON error envelope

**Rationale**: The existing frontend consumes `{ "error": "..." }`. Preserve this body shape while choosing 400 for invalid client input, 404 for an agent not found by the upstream service, 503 for a connectivity/timeout outage, and 502 for other upstream failures or unusable responses.

**Alternatives considered**:
- Add a new error schema or status field: rejected for this bounded bug fix because the current frontend already understands the `error` field and HTTP status.
- Return a generic 500 for every non-validation error: rejected because it would continue obscuring whether users can recover by starting Ollama or selecting another agent.

### Decision: Keep user-facing diagnostics actionable and safe

**Rationale**: Users need to know whether to check Ollama, choose an installed agent, or retry. Raw exception text, upstream payloads, and local paths may include implementation details and are not required for those actions.

**Alternatives considered**:
- Expose raw upstream error text: rejected as inconsistent and potentially revealing local details.
- Hide all cause information behind a generic message: rejected because it prevents user recovery.

### Decision: Preserve the current frontend conversation behavior on failure

**Rationale**: The browser currently retains the submitted user message and prior messages when chat fails. Preserve this behavior and ensure the error banner and status remain useful; do not clear the conversation or silently discard the failed message.

**Alternatives considered**:
- Remove the submitted user message on failure: rejected because it loses context and makes retry difficult.
- Automatically retry: rejected because a retry may repeat a costly model operation and the user can already retry explicitly.

## Validation Strategy

- Mock the service to verify successful chat responses and each error category at the API boundary.
- Test invalid or missing request fields without invoking the Ollama adapter.
- Test Ollama upstream HTTP errors, connectivity errors, and empty/malformed responses with deterministic mocks.
- Verify the frontend displays the API error text and does not lose the conversation after a rejected request.
- Perform a real Ollama/browser smoke test only when a local Ollama instance and an installed model are available; the provided log alone is insufficient to establish that runtime dependency state.
