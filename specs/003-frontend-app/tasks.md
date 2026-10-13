# Tasks: Front-end for the Application

**Input**: Design documents from `/specs/003-frontend-app/`

**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, quickstart.md, contracts/

**Tests**: Tests are optional for this feature and are not required unless future validation adds them.

**Organization**: Tasks are grouped by user story to enable independent implementation and verification.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Create the project structure and define the local web app boundary before building the UI and service layers.

- [ ] T001 Create the backend service structure in `backend/src/api/`, `backend/src/services/`, and `backend/src/models/` to match the implementation plan
- [ ] T002 Create the browser application scaffold in `frontend/src/`, `frontend/public/`, and `frontend/src/styles/` for the initial UI shell
- [ ] T003 [P] Add the backend package manifest and runtime setup in `backend/requirements.txt` for the local API server and Ollama integration
- [ ] T004 [P] Add the frontend entry point and initial HTML shell in `frontend/public/index.html` and `frontend/src/app.js`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Establish the core local service contracts and shared state needed before any user story can be implemented.

- [ ] T005 Define the backend agent and conversation data contracts in `backend/src/models/agent.py` and `backend/src/models/conversation.py`
- [ ] T006 Implement the Ollama connectivity and health-check service in `backend/src/services/ollama_service.py`
- [ ] T007 [P] Build the shared frontend state model and API client in `frontend/src/state.js` and `frontend/src/api.js`
- [ ] T008 Create the backend application bootstrap and route registration in `backend/src/main.py`
- [ ] T009 Implement structured error handling and user-facing service messages in `backend/src/services/error_handler.py`

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel.

---

## Phase 3: User Story 1 - View and manage available agents (Priority: P1) 🎯 MVP

**Goal**: Expose the installed agents and their current state in a readable, usable interface.

**Independent Test**: A user can open the application and see the available agents and status without any terminal commands.

### Implementation for User Story 1

- [ ] T010 [US1] Build the agent list view and empty-state layout in `frontend/src/components/agent_list.js`
- [ ] T011 [US1] Add agent status rendering and refresh behavior in `frontend/src/components/agent_card.js`
- [ ] T012 [US1] Implement the `GET /api/agents` backend route in `backend/src/api/agent_routes.py` and return structured agent data
- [ ] T013 [US1] Hook the UI list to the backend data flow and render the selected agent state in `frontend/src/app.js`

**Checkpoint**: User Story 1 is ready to be used as the minimum viable experience for agent discovery.

---

## Phase 4: User Story 2 - Create and remove agents from a browser interface (Priority: P1)

**Goal**: Allow users to create and delete agents without shell access or terminal commands.

**Independent Test**: A user can create a valid agent, see it appear in the list, and delete it only after confirmation.

### Implementation for User Story 2

- [ ] T014 [US2] Build the agent creation form and validation flow in `frontend/src/components/create_agent_form.js`
- [ ] T015 [US2] Add delete confirmation and cancel behavior in `frontend/src/components/delete_agent_modal.js`
- [ ] T016 [US2] Implement create-agent validation and duplicate detection in `backend/src/services/agent_service.py`
- [ ] T017 [US2] Implement the `POST /api/agents` and `DELETE /api/agents/{agentName}` endpoints in `backend/src/api/agent_routes.py`
- [ ] T018 [US2] Wire the create and delete actions into the app state and refresh the agent list after each operation in `frontend/src/app.js`

**Checkpoint**: User Story 2 is independently testable through the management workflow.

---

## Phase 5: User Story 3 - Chat with an agent in a simple conversational interface (Priority: P1)

**Goal**: Allow users to select an agent and exchange messages in a clear chat flow.

**Independent Test**: A user can select an agent, send a message, and see the assistant response in the browser interface.

### Implementation for User Story 3

- [ ] T019 [US3] Build the conversation pane and message rendering in `frontend/src/components/chat_panel.js`
- [ ] T020 [US3] Add the input form and send-state handling in `frontend/src/components/message_input.js`
- [ ] T021 [US3] Implement the `POST /api/chat` backend route in `backend/src/api/chat_routes.py` and preserve conversation context with the selected agent
- [ ] T022 [US3] Add conversation retrieval and message history support in `backend/src/api/chat_routes.py` and `backend/src/services/chat_service.py`
- [ ] T023 [US3] Connect the frontend chat flow to the selected-agent state and render chronological messages in `frontend/src/app.js`

**Checkpoint**: User Story 3 is complete and can be used as the core conversation experience.

---

## Phase 6: User Story 4 - Understand state, recover from errors, and keep work organized (Priority: P2)

**Goal**: Ensure the interface clearly communicates progress, empty states, and service failures.

**Independent Test**: A user can understand the current app state, recover from service or validation issues, and continue using the interface without technical assistance.

### Implementation for User Story 4

- [ ] T024 [US4] Add empty-state, loading, and failure banners in `frontend/src/components/status_banner.js`
- [ ] T025 [US4] Implement health-check and offline guidance in `backend/src/api/system_routes.py` and `backend/src/services/ollama_service.py`
- [ ] T026 [US4] Add conversation and agent refresh handling so the UI remains consistent after errors or missing data in `frontend/src/state.js`
- [ ] T027 [US4] Improve the user flow for invalid inputs, duplicate names, and missing resources with explanatory messages in `frontend/src/app.js` and `backend/src/services/error_handler.py`

**Checkpoint**: User Story 4 is complete and supports usability across failure states.

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Final quality pass across the frontend and backend to ensure the experience is clear, stable, and release-ready.

- [ ] T028 [P] Validate the browser layout against the empty-state, loading, and chat flows in `frontend/public/index.html` and `frontend/src/styles/`
- [ ] T029 [P] Review the API response contracts against `specs/003-frontend-app/contracts/frontend-contract.md` and confirm the frontend renders all required states correctly
- [ ] T030 [P] Run the quickstart validation scenarios from `specs/003-frontend-app/quickstart.md` and confirm the key user journeys work end-to-end

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies; can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion; blocks all user stories
- **User Story phases (Phases 3-6)**: All depend on the shared foundation and can proceed in priority order
- **Polish (Phase 7)**: Depends on all user story work being complete

### User Story Dependencies

- **User Story 1 (US1)**: Can start after foundation; delivers the agent list and status view
- **User Story 2 (US2)**: Can start after foundation; depends on the same agent domain model and API surface
- **User Story 3 (US3)**: Can start after foundation; depends on the selected agent and conversation state
- **User Story 4 (US4)**: Can start after foundation; improves recovery and usability across all flows

### Parallel Opportunities

- T003 and T004 can run in parallel during Setup
- T007 and T008 can run in parallel during the Foundational phase
- US1, US2, and US3 can run in parallel once the foundation is complete if multiple contributors are available
- T028, T029, and T030 can all run in parallel during the final polish phase

---

## Parallel Example: Post-Foundation Execution

```bash
# Example parallel work after Phase 2 completes
Task: "Build the agent list view and empty-state layout in frontend/src/components/agent_list.js"
Task: "Implement create and delete flows in backend/src/api/agent_routes.py"
Task: "Build the conversation pane and message rendering in frontend/src/components/chat_panel.js"
Task: "Add health-check and offline guidance in backend/src/api/system_routes.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational
3. Complete Phase 3: User Story 1
4. Validate that the interface reliably displays the available agents and their status
5. Stop and review before expanding into agent management and chat flows

### Incremental Delivery

1. Add the core agent overview and status view
2. Add create and delete management actions
3. Add the conversation and message experience
4. Add recovery states, failure guidance, and polished empty states
5. Finish with release-quality validation and contract checks

## Validation Summary

- Total task count: 30
- Task count by user story: US1 = 4, US2 = 5, US3 = 5, US4 = 4
- Parallel opportunities identified: Setup, Foundation, and final polish phases
- Suggested MVP scope: User Story 1 only, followed by User Story 2 and User Story 3
- Format validation: All tasks follow the required checklist format with a checkbox, task ID, optional [P] marker, optional [USx] story label, and exact file paths in the description
