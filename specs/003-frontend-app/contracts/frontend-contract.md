# Front-end API Contract

## Overview

This contract defines the backend-facing endpoints needed for the front-end user experience. It is designed to mirror the existing agent-management behavior while exposing a cleaner interface to the browser.

## Endpoints

### GET /api/health

Returns the current health of the local dependency layer.

**Response**

```json
{
  "connected": true,
  "message": "Ollama is available"
}
```

### GET /api/agents

Returns all locally available agents.

**Response**

```json
[
  {
    "name": "llama3.2",
    "status": "available",
    "source": "installed",
    "createdAt": "2026-10-12T12:00:00Z"
  }
]
```

### POST /api/agents

Creates a new agent from a valid Modelfile.

**Request**

```json
{
  "name": "custom-agent",
  "modelfilePath": "/path/to/Modelfile"
}
```

**Success response**

```json
{
  "name": "custom-agent",
  "status": "available"
}
```

**Error response**

```json
{
  "error": "Agent name already exists or Modelfile is invalid."
}
```

### DELETE /api/agents/{agentName}

Deletes an existing agent after confirmation.

**Success response**

```json
{
  "deleted": true,
  "agentName": "custom-agent"
}
```

### POST /api/chat

Sends a user prompt to the selected agent and returns a response.

**Request**

```json
{
  "agentName": "llama3.2",
  "message": "Summarize this repository."
}
```

**Success response**

```json
{
  "role": "assistant",
  "content": "This project is a local agent manager for Ollama...",
  "timestamp": "2026-10-12T12:03:00Z"
}
```

### GET /api/conversations/{agentName}

Returns the current conversation history for an agent.

**Response**

```json
{
  "id": "conversation-001",
  "agentName": "llama3.2",
  "messages": [
    {
      "role": "user",
      "content": "Hello",
      "timestamp": "2026-10-12T12:00:00Z"
    }
  ]
}
```

## Error Handling

The API must return structured error messages for invalid input, service unavailability, duplicates, and unsupported operations. All front-end states should map these errors to actionable UI feedback rather than displaying raw backend exceptions.
