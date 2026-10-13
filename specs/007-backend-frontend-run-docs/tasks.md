# Tasks: Backend and Frontend Run Documentation

**Input**: Design documents from `specs/007-backend-frontend-run-docs/`

**Prerequisites**: `plan.md`, `spec.md`, `research.md`, `data-model.md`, `contracts/`, `quickstart.md`

**Tests**: Documentation-only change. Validate documented commands and URLs against the application configuration and check that the README and quickstart agree.

## Phase 1: Setup

**Purpose**: Project setup

No setup tasks are required. This feature updates existing documentation only.

## Phase 2: Foundational

**Purpose**: Shared prerequisites blocking the user story

No foundational tasks are required. The startup sequence and service addresses are documented in the design contract and do not require shared code or infrastructure changes.

## Phase 3: User Story 1 - Start the local web application from the documentation (Priority: P1) 🎯 MVP

**Goal**: Provide a complete, consistent startup guide for the local backend API and static frontend, including prerequisites and basic recovery guidance.

**Independent Test**: Starting from the repository root, follow the README or quickstart instructions to install backend requirements, start the backend and frontend in separate terminals, and open `http://localhost:5173/public/`. Confirm the backend uses `127.0.0.1:8000`, the frontend calls the matching API, and Ollama availability is explained.

### Documentation

- [X] T001 [P] [US1] Update the web application startup section in `README.md` with prerequisites, backend dependency installation, separate backend/frontend terminal commands, browser URL, and port/Ollama troubleshooting matching `specs/007-backend-frontend-run-docs/contracts/web-app-startup.md`.
- [X] T002 [P] [US1] Add a consistent web application startup section to `quickstart.md` with prerequisites, both terminal commands, browser URL, health endpoint, and recovery guidance matching `specs/007-backend-frontend-run-docs/contracts/web-app-startup.md`.
- [X] T003 [US1] Verify the commands and addresses in `README.md` and `quickstart.md` against `backend/requirements.txt`, `backend/src/main.py`, `frontend/src/api.js`, and `frontend/public/index.html`; confirm both guides describe the same startup sequence.

**Checkpoint**: A user can start and open the local web application using either documentation guide without needing an undocumented command.

## Phase 4: Polish & Cross-Cutting Concerns

**Purpose**: Validate documentation quality and consistency.

- [X] T004 Run `git diff --check -- README.md quickstart.md` and review both files for Markdown rendering, consistent service URLs, and preservation of existing CLI instructions.

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No tasks required.
- **Foundational (Phase 2)**: No tasks required.
- **User Story 1 (Phase 3)**: Can start immediately. T001 and T002 edit different files and may run in parallel; T003 depends on both documentation updates.
- **Polish (Phase 4)**: T004 runs after the story documentation and validation are complete.

### User Story Dependencies

- **User Story 1 (P1)**: No dependencies on other stories; it is the complete MVP.

### Parallel Opportunities

- T001 can update `README.md` in parallel with T002 updating `quickstart.md`.

## Parallel Example: User Story 1

```text
Task: "Update backend and frontend startup instructions in README.md."
Task: "Add backend and frontend startup instructions in quickstart.md."
```

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Update the README and quickstart in parallel.
2. Verify the commands against the backend and frontend configuration.
3. Run the documentation diff check and confirm the existing CLI guidance remains intact.

### Incremental Delivery

This feature contains one user story. Deliver the two aligned guides together as a single MVP increment.
