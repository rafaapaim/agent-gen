# Chat API Contract

## Endpoint

`POST /api/chat`

## Request

```json
{
  "agentName": "llama3.2",
  "message": "Summarize this repository."
}
```

Both fields are required strings and must contain non-whitespace text.

## Success

**Status**: `200 OK`

```json
{
  "role": "assistant",
  "content": "This project is a local agent manager..."
}
```

The response content must be non-empty and usable by the conversation UI.

## Errors

All errors use the existing JSON shape:

```json
{
  "error": "Select an available agent and try again."
}
```

| Status | Meaning | Expected user action |
|---:|---|---|
| `400 Bad Request` | Agent name or message is missing/blank | Select an agent and enter a message |
| `404 Not Found` | Requested agent is unavailable or unknown | Select an installed agent or install the requested one |
| `502 Bad Gateway` | Upstream service rejected the request for another reason or returned an unusable response | Check the selected agent and model service, then retry |
| `503 Service Unavailable` | Local model service cannot be reached or timed out | Start/check the local model service, then retry |

Errors must not include stack traces, local filesystem paths, or raw upstream diagnostics unless separately deemed safe. Existing request and success payload shapes remain unchanged.
