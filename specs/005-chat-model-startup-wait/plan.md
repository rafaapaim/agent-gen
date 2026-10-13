# Implementation Plan: Wait for Chat Model Startup

**Branch**: `005-chat-model-startup-wait` | **Date**: 2026-10-12 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/005-chat-model-startup-wait/spec.md`

## Summary

The supplied logs show Ollama's model startup was aborted because its chat client closed the connection after approximately 10 seconds. The backend currently uses `urllib.request.urlopen(..., timeout=10)` for every request, including chat. Keep short timeouts for health and agent listing, but give chat a bounded 300-second upstream timeout to accommodate cold-start loading and response generation. During this wait, the browser will indicate progress, prevent duplicate submissions and agent switches, preserve the pending exchange, and present a distinct actionable timeout if the bounded wait expires.

## Technical Context

**Language/Version**: Python 3.11+; browser-native JavaScript (ES modules)

**Primary Dependencies**: Python standard library `urllib`; existing FastAPI and Uvicorn backend; browser `fetch`

**Storage**: No new persistence; conversation remains in browser memory

**Testing**: pytest with mocked `urlopen` and FastAPI `TestClient`; JavaScript syntax check; live Ollama/browser smoke test when available

**Target Platform**: Local Windows, macOS, or Linux environment with a browser, the backend, and local Ollama

**Project Type**: Local web application

**Performance Goals**: Permit up to 300 seconds for a chat request to cover model cold start and generation; do not increase timeouts for health checks or agent listing

**Constraints**: Keep the existing chat request and successful response shapes; maintain a finite upstream wait; report request timeout distinctly from service unavailability; prevent duplicate submissions and responses associated with a different selected agent

**Scale/Scope**: Chat request timeout behavior in the Ollama adapter, user-visible in-progress/recovery state in the browser, and focused tests

## Constitution Check

The repository constitution is an unfilled template and supplies no enforceable project-specific gates. The project-wide constraint that documentation and code remain in English is followed. The plan uses existing dependencies and the current backend/frontend boundary.

**Gate**: PASS — no applicable governance violations identified.

## Project Structure

### Documentation (this feature)

```text
specs/005-chat-model-startup-wait/
├── spec.md
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   └── chat-wait-contract.md
├── checklists/
│   └── requirements.md
└── tasks.md  # generated later by /speckit.tasks
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── api/
│   │   └── chat_routes.py
│   └── services/
│       └── ollama_service.py
└── tests/
    └── test_api.py

frontend/
└── src/
    ├── app.js
    ├── api.js
    └── styles/app.css
```

**Structure Decision**: Keep the change inside the existing Ollama adapter and static frontend chat flow. Reuse the current API error envelope and tests; do not add asynchronous job storage, polling endpoints, or new dependencies.

## Constitution Check (Post-Design)

- Existing request and response contract is preserved: PASS.
- Chat request duration remains bounded and other Ollama operations keep their current timeout: PASS.
- In-progress, duplicate-submit, timeout, and conversation recovery behavior are covered by design: PASS.
- No new persistence, dependency, or constitution exception is required.
