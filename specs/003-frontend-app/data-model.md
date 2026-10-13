# Data Model: Front-end for the Application

## Overview

The front-end introduces a small client/server data model built around the existing agent-management domain. The model focuses on the information the user sees and the state the backend must manage to support the primary user flows: listing agents, creating or deleting them, and chatting with a selected model.

## Entities

### User

Represents the person interacting with the interface.

| Field | Type | Description | Validation |
|---|---|---|---|
| id | string | Local session identifier | Must be non-empty |
| name | string | Optional display name if later added | Optional |

### Agent

Represents a model or local agent currently known to Ollama.

| Field | Type | Description | Validation |
|---|---|---|---|
| name | string | Unique installed model/agent name | Must be non-empty and unique |
| status | enum | Current lifecycle state (`available`, `creating`, `deleting`, `error`, `offline`) | Must be one of the defined states |
| source | string | Model source or Modelfile reference for creation flows | Required for creation, optional for existing models |
| createdAt | datetime | When the agent became available | ISO timestamp |

### Conversation

Represents one chat session associated with an agent.

| Field | Type | Description | Validation |
|---|---|---|---|
| id | string | Conversation identifier | Must be unique |
| agentName | string | Selected agent being used | Must match an existing agent |
| messages | array | Chronological message history | Must be array of message objects |
| createdAt | datetime | When the conversation began | ISO timestamp |
| updatedAt | datetime | Last modification time | ISO timestamp |

### Message

Represents a single chat item in the conversation.

| Field | Type | Description | Validation |
|---|---|---|---|
| role | enum | `user` or `assistant` | Must be one of the defined roles |
| content | string | Message text or assistant output | Must be string; may be empty for special cases |
| timestamp | datetime | Message send/receive time | ISO timestamp |

### Model Configuration

Represents the underlying definition for a new agent.

| Field | Type | Description | Validation |
|---|---|---|---|
| name | string | Requested agent name | Must be non-empty and not duplicate existing agent |
| modelfilePath | string | Local path to the Modelfile | Must resolve to an existing file |
| mode | enum | Creation mode, currently `modelfile` | Must match supported values |

### Service Status

Represents runtime health for the Ollama dependency.

| Field | Type | Description | Validation |
|---|---|---|---|
| connected | boolean | Whether Ollama is reachable | Boolean |
| message | string | Human-readable status or recovery guidance | Optional human-readable text |

## Relationships

- A `User` can select one `Agent` at a time for chat.
- An `Agent` can have zero or more `Conversation` records associated with it.
- A `Conversation` contains many `Message` entries in chronological order.
- `Model Configuration` is used only during the create-agent flow.
- `Service Status` is global; it affects all agent operations and the chat view.

## Validation Rules

- Agent names must not be empty.
- Agent names must be unique within the current local registry.
- Modelfile paths must resolve to readable files before creation proceeds.
- Chat requests must include a selected agent and a non-empty prompt.
- If the model service is unavailable, the UI must show a clear failure state rather than silently failing.
- Delete actions require explicit confirmation before the backend removes an agent.

## State Transitions

### Agent lifecycle

- `available` -> `creating` when the user starts creation
- `creating` -> `available` after a successful create
- `creating` -> `error` when validation or Ollama creation fails
- `available` -> `deleting` when a deletion flow begins
- `deleting` -> `available` after successful deletion
- `deleting` -> `error` if deletion fails

### Conversation lifecycle

- New session created when user selects an agent and opens a conversation.
- Messages append in order as user sends prompts and assistant replies return.
- A conversation can be cleared by user action without deleting the agent itself.

## UI State Model

The front-end should maintain a state object equivalent to:

```json
{
  "agents": [],
  "selectedAgent": null,
  "conversation": {
    "id": "",
    "agentName": "",
    "messages": []
  },
  "serviceStatus": {
    "connected": true,
    "message": ""
  },
  "loading": false,
  "error": null
}
```

This state is the foundation of the empty state, loading state, and error-state UI described in the feature specification.
