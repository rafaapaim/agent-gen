# Data Model: Backend and Frontend Run Documentation

## Overview

This feature changes user-facing documentation only. It introduces no application data, persistent records, API payloads, or state transitions.

## Documentation Concepts

### Backend Service

The local API process, launched from the repository root, with default address `http://127.0.0.1:8000`.

### Frontend Static Server

The local HTTP server for the browser UI, launched separately from the repository root, with default address `http://localhost:5173/public/`.

### Ollama Service

The local model runtime expected at `http://localhost:11434` for health, agent-listing, and chat operations.

## Relationships

- The browser loads the frontend from the frontend static server.
- The frontend sends API requests to the backend at `127.0.0.1:8000`.
- The backend checks and uses Ollama at `localhost:11434`.
- Backend port and frontend API base URL must agree if the backend default port is changed.

## Validation Rules

- Commands in README and quickstart must use the same dependency file, module path, host, ports, and browser address.
- Both server commands must be shown as separate processes/terminals.
- The frontend must be served over HTTP rather than described as a direct file open.
- Instructions must state the Ollama dependency and cover service/port startup failures.
