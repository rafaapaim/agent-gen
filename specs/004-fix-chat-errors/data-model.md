# Data Model: Fix Chat Request Failures

This change adds no persisted data. It clarifies the transient request, result, and failure information passed between the browser, backend, and local model service.

## Chat Request

Represents one user attempt to contact an agent.

| Field | Type | Required | Validation |
|---|---|---:|---|
| `agentName` | string | Yes | Must contain non-whitespace text and identify the selected agent |
| `message` | string | Yes | Must contain non-whitespace text |

## Chat Result

Represents a successful response shown in the conversation.

| Field | Type | Required | Validation |
|---|---|---:|---|
| `role` | string | Yes | `assistant` |
| `content` | string | Yes | Must be a usable, non-empty response |

The browser also retains the submitted user message in its in-memory conversation state. A failed response does not erase that message or earlier exchanges.

## Chat Failure

Represents an unsuccessful request. It is returned using the existing JSON envelope.

| Field | Type | Required | Meaning |
|---|---|---:|---|
| `error` | string | Yes | Safe, user-understandable message with a relevant recovery action |
| HTTP status | integer | Yes | Classifies the failure for the API client |

### Failure categories and transitions

| Cause | HTTP status | User guidance |
|---|---:|---|
| Missing/blank agent or message | 400 | Select an agent and enter a message |
| Agent is not installed or not recognized | 404 | Select an available agent or install the requested one |
| Model service cannot be reached or times out | 503 | Start/check the local Ollama service, then retry |
| Other upstream rejection or unusable response | 502 | Retry; if it continues, check the model service and selected agent |

Request lifecycle: `submitted -> succeeded` or `submitted -> failed`. A failed request remains visible in the conversation and can be retried or followed by a request to a different agent.
