# Tasks: Full-Viewport Web Layout

**Input**: Design documents from `specs/006-fullscreen-web-layout/`

**Prerequisites**: `plan.md`, `spec.md`, `research.md`, `data-model.md`, `contracts/`, `quickstart.md`

**Tests**: No automated frontend test harness exists and the specification does not require TDD. Validate the rendered UI manually using the viewport scenarios in `quickstart.md`; run existing CLI tests as regression coverage.

## Phase 1: Setup

**Purpose**: Project setup

No setup tasks are required. The existing frontend and static-server workflow are sufficient; this feature adds no dependencies or project configuration.

## Phase 2: Foundational

**Purpose**: Shared prerequisites blocking the user story

No foundational tasks are required. The change is isolated to the existing page root and stylesheet.

## Phase 3: User Story 1 - Use the web application across the available browser window (Priority: P1) 🎯 MVP

**Goal**: Make the existing agent sidebar and chat fill the available browser viewport, adapt to compact viewports, and preserve usable scrolling and controls.

**Independent Test**: Serve `frontend/` and open `http://localhost:5173/public/`. Confirm the application uses at least 95% of the visible area at a 1600 × 900 desktop viewport, both columns fit the page, and agent controls, messages, and message entry remain usable at narrow and short viewport sizes. See `specs/006-fullscreen-web-layout/quickstart.md`.

### Implementation

- [X] T001 [P] [US1] Remove the `app-shell` class from the outer `#app` wrapper in `frontend/public/index.html` so the rendered application has only one grid shell.
- [X] T002 [P] [US1] Update `.app-shell`, `.sidebar`, `.chat-panel`, and `.messages` viewport sizing and overflow rules in `frontend/src/styles/app.css` so the single shell fills the browser width and height, keeps the desktop columns within available width, and leaves controls reachable at compact sizes.
- [X] T003 [US1] Verify the desktop, narrow, short, and resize scenarios in `specs/006-fullscreen-web-layout/quickstart.md`; confirm agent controls and chat entry are reachable and long lists/messages remain scrollable.

**Checkpoint**: The page fills the browser viewport and the existing agent-management and chat workflows remain accessible.

## Phase 4: Polish & Cross-Cutting Concerns

**Purpose**: Confirm regression safety and contract alignment.

- [X] T004 [P] Run the existing CLI regression tests in `tests/test_agent_management.py` and confirm the presentation-only change does not alter their results.
- [X] T005 Confirm the implemented layout satisfies the viewport and workflow behavior documented in `specs/006-fullscreen-web-layout/contracts/full-viewport-layout.md`.

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No work required; the existing project setup is sufficient.
- **Foundational (Phase 2)**: No work required; the story can begin immediately.
- **User Story 1 (Phase 3)**: Independent MVP. T001 and T002 can be implemented in parallel; T003 requires both changes.
- **Polish (Phase 4)**: Run after the user story implementation. T004 can run independently of T005.

### User Story Dependencies

- **User Story 1 (P1)**: No dependencies on other stories; it is the only story and can be delivered as the MVP.

### Parallel Opportunities

- T001 (`frontend/public/index.html`) and T002 (`frontend/src/styles/app.css`) edit different files and may proceed in parallel.
- T004 (CLI regression tests) and T005 (contract review) may proceed in parallel after implementation.

## Parallel Example: User Story 1

```text
Task: "Remove the app-shell class from the outer #app wrapper in frontend/public/index.html."
Task: "Update viewport sizing and overflow rules in frontend/src/styles/app.css."
```

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Implement T001 and T002, in parallel if useful.
2. Complete T003 and verify the feature independently against the quickstart criteria.
3. Complete T004 and T005 as regression and contract checks.

### Incremental Delivery

This feature contains one user story. Complete and validate that story as a single MVP increment; do not add unrelated frontend or backend behavior.
