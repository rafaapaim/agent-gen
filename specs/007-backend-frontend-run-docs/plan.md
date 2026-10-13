# Implementation Plan: Backend and Frontend Run Documentation

**Branch**: `main` | **Date**: 2026-10-13 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `specs/007-backend-frontend-run-docs/spec.md`

## Summary

Update the Portuguese README and the English quickstart so a user can install backend requirements and launch the local web app without guessing. Both guides will describe the same sequence: run Ollama, install `backend/requirements.txt`, start the API at `127.0.0.1:8000`, serve the frontend from `frontend/` in a second terminal, and open `http://localhost:5173/public/`. Include basic checks and troubleshooting for occupied ports and unavailable Ollama. No application code or runtime behavior changes are in scope.

## Technical Context

**Language/Version**: Documentation in Portuguese (README) and English (quickstart); Python 3.11+ commands

**Primary Dependencies**: Existing FastAPI and Uvicorn requirements listed in `backend/requirements.txt`; Python standard-library static HTTP server

**Storage**: N/A

**Testing**: Validate command and URL consistency against `backend/src/main.py`, `frontend/src/api.js`, `frontend/public/index.html`, and `backend/requirements.txt`; run the documented services and verify the frontend and health endpoint locally

**Target Platform**: Local development on Windows, macOS, or Linux with Python and Ollama

**Project Type**: Documentation-only update for a local web application

**Performance Goals**: A reader can find the full two-terminal startup sequence in under 2 minutes

**Constraints**: Use repository-root-relative commands; preserve existing CLI documentation; document default ports and frontend URL accurately; port changes may require matching changes to the frontend API base URL

**Scale/Scope**: Two existing documentation files: `README.md` and `quickstart.md`

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

The constitution contains only unfilled template placeholders and no active rules. This documentation-only change introduces no dependencies, code paths, data, or runtime behavior. It preserves current CLI instructions and documents commands based on existing configuration. No violations or exceptions are identified.

## Project Structure

### Documentation (this feature)

```text
specs/007-backend-frontend-run-docs/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
└── contracts/
    └── web-app-startup.md
```

### Source Code (repository root)

```text
README.md
quickstart.md
backend/
├── requirements.txt
└── src/main.py
frontend/
├── public/index.html
└── src/api.js
```

**Structure Decision**: Update only `README.md` and `quickstart.md`. No application source, tests, dependency manifests, or runtime configuration need to change.

## Complexity Tracking

No constitution violations require justification. The work is limited to correcting and aligning the existing user-facing run instructions.
