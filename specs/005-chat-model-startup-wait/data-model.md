# Data Model: Wait for Chat Model Startup

This feature introduces no persisted data. It describes transient state for a chat request while the local agent starts and generates a response.

## Chat Request

| Field | Type | Required | Meaning |
|---|---|---:|---|
| `agentName` | string | Yes | The agent selected when the request was submitted |
| `message` | string | Yes | The submitted user message |
| `status` | enum | Yes | `pending`, `completed`, `timed_out`, or `failed` |

The agent name is captured for the lifetime of the request. The active agent cannot be changed in the interface while the request is pending.

## Wait Limit

| Field | Type | Value | Meaning |
|---|---|---:|---|
| `timeoutSeconds` | positive integer | 300 | Maximum socket wait for one chat request |

This bound applies to chat only. Existing shorter timeouts for health and agent-list operations remain unchanged.

## Conversation Exchange

| Field | Type | Required | Meaning |
|---|---|---:|---|
| `role` | string | Yes | `user` or `assistant` |
| `content` | string | Yes | Submitted message or returned response |

On submit, exactly one user entry is added. On success, exactly one assistant entry follows it. On timeout or failure, no assistant entry is fabricated, and the user entry remains available for retry.

## State Transitions

```text
pending -> completed
pending -> timed_out
pending -> failed
```

- A request remains pending while the upstream chat call has not returned and the wait limit has not expired.
- `completed` adds the assistant response to the exchange.
- `timed_out` reports a retryable wait-limit message and retains the user message.
- `failed` reports the recognized service/upstream failure and retains the user message.
- A response may update the conversation only if it belongs to the still-active request and its captured agent selection.
