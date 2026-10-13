# Research: Front-end for the Application

## Research Summary

### Decision: Build a local web front-end backed by a small Python API layer

The application already depends on a local Ollama service and a Python runtime. The most consistent front-end approach is a simple local web application: a Python server exposes a JSON API for listing agents, creating and deleting them, and sending chat requests, while the browser UI renders the managed agent state and conversation history.

### Rationale

- The repository already uses Python and interacts with Ollama over HTTP, so a Python API layer aligns with existing domain knowledge and minimizes technology friction.
- A browser interface is more usable than a terminal for users who need to manage local agents visually.
- The app is intended for local, same-machine use; a localhost-only web interface is a good fit for the project’s scale and dependencies.
- A small, focused UI avoids requiring a large framework for a single-user workflow.

### Alternatives considered

1. Desktop application with Tkinter or Qt
   - Pros: delivers a native local experience without a browser.
   - Cons: higher UI complexity, more platform-specific behavior, and a less flexible deployment model for a lightweight project.
   - Rejected because the project’s current architecture and local service model fit a browser interface more naturally.

2. Direct browser calls to Ollama from JavaScript
   - Pros: very simple for a minimal prototype.
   - Cons: mixes UI logic with remote service details, bypasses a clean app boundary, and weakens validation and error handling for agent management operations.
   - Rejected because the app also needs create/delete flows, local validation, and a coherent service layer.

3. Full React + Node stack
   - Pros: strong tooling, UI ecosystem, and developer ergonomics.
   - Cons: heavier setup and dependencies for a small local utility; adds operational complexity without proportional user value.
   - Rejected because the project’s Python-first nature and small scope favor a lighter approach.

## Resolved Unknowns

### Front-end type

The interface will be a lightweight local web application served on `http://localhost:8000` or similar. The design assumes a single desktop user with direct access to the machine running the backend.

### Core architecture boundary

The backend will own all interactions with the Ollama runtime and local filesystem. The front-end will request structured data and present it, but it will not directly manage external model operations.

### State model

The app will track the current selected agent, active conversation, agent list, and status/error conditions. This will allow the UI to show empty states, loading indicators, and recovery guidance without breaking the user flow.

### User flow priority

The MVP will prioritize:
- viewing installed agents,
- creating and deleting agents,
- opening a chat session,
- handling offline or failed-service states.

## Implementation Notes

The front-end should not duplicate all terminal command logic. Instead, it should preserve the original application actions behind a robust API and present them in a clearer interface. This keeps the operational model consistent while improving usability for people who do not want to work in a shell.

The UI should provide clear states for:
- no agents installed,
- agent creation in progress,
- invalid input or duplicate name,
- chat request in progress,
- Ollama service unavailable,
- successful operation confirmations.

This approach makes the feature testable and keeps the implementation aligned with the existing CLI foundation.
