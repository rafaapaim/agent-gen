# Chat Wait Contract

## Request

The existing endpoint and payload remain unchanged:

`POST /api/chat`

```json
{
  "agentName": "large-local-agent",
  "message": "Hello"
}
```

The client keeps the request active while the server waits for the agent, for up to 300 seconds. Health and agent-list requests retain their existing 10-second timeout.

## Successful response

**Status**: `200 OK`

```json
{
  "role": "assistant",
  "content": "Hello. How can I help?"
}
```

The browser adds the assistant response once after the corresponding user message.

## Error responses

All errors keep the existing JSON envelope:

```json
{
  "error": "The agent is taking too long to start. Wait a little and try again."
}
```

| Status | Meaning | UI behavior |
|---:|---|---|
| `504 Gateway Timeout` | The 300-second bounded wait for the local agent's response expired | Explain that startup/response exceeded the wait, preserve the user message, allow retry |
| `503 Service Unavailable` | The local model service could not be reached | Explain service connectivity failure and suggest starting/checking Ollama |
| `502 Bad Gateway` | The upstream response was unsuccessful or unusable for another reason | Show the existing safe actionable upstream error |

## Pending UI behavior

- Show “Waiting for the agent to start and respond...” while waiting for a response.
- Disable the message input, send control, and agent selection until the active request resolves.
- On success, timeout, or failure, restore the controls.
- Keep the pending user message and earlier conversation visible.
- Retrying the same submitted message for the same agent reuses the existing user entry rather than adding a duplicate.
- Never append a response to an agent context different from the one captured when submitting.
