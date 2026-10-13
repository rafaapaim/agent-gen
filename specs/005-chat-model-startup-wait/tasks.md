# Tasks: Wait for Chat Model Startup

**Input**: Design documents in `specs/005-chat-model-startup-wait/`
**Prerequisites**: `plan.md`, `spec.md`, `research.md`, `data-model.md`, `contracts/chat-wait-contract.md`, `quickstart.md`

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Setup)**: Run baseline tests before changes.
- **Phase 2 (Foundational)**: Add a per-request timeout option while retaining the existing default. Both user stories depend on this.
- **Phase 3 (US1)**: Use the longer bound for chat and provide pending UI state. Depends on Phase 2.
- **Phase 4 (US2)**: Classify and recover from timeout while preserving the conversation. Depends on Phase 2; can proceed after US1 or in parallel where files do not overlap.
- **Phase 5 (Polish)**: Align documentation and perform final validation after both stories.

### User Story Completion Order

US1 and US2 are both P1. They share the HTTP timeout foundation, then are independently testable. Serialize changes to files touched by more than one story, especially `backend/src/services/ollama_service.py`, `backend/src/api/chat_routes.py`, `backend/tests/test_api.py`, and `frontend/src/app.js`.

## Phase 1: Setup

**Purpose**: Confirm the current test baseline before changing request behavior.

- [X] T001 Run `.\.venv\Scripts\python.exe -m pytest backend/tests/test_api.py -q` from the repository root and record the baseline result (9 passed)

## Phase 2: Foundational

**Purpose**: Support a bounded timeout per Ollama request without slowing health or agent-list requests.

- [X] T002 [P] Add a timeout parameter with the existing 10-second default to `OllamaService._request()` in `backend/src/services/ollama_service.py`
- [X] T003 [P] Add a unit/API test verifying requests that omit the timeout keep the 10-second default and explicit timeouts are passed to `urlopen()` in `backend/tests/test_api.py`

## Phase 3: User Story 1 - Receive a response while an agent is starting (Priority: P1)

**Goal**: Chat may wait up to 300 seconds for cold model startup and presents visible progress without allowing accidental duplicate submissions.

**Independent Test**: Verify chat calls use a 300-second bound while health/list operations retain 10 seconds; simulate a response that arrives before the bound and verify it returns normally. In the browser, verify pending feedback and disabled submit/agent-selection controls until completion.

- [X] T004 [P] [US1] Call `_request()` with a 300-second timeout from `OllamaService.chat()` in `backend/src/services/ollama_service.py`
- [X] T005 [P] [US1] Add a test proving the chat call uses the 300-second timeout and a mocked delayed successful response still returns HTTP 200 in `backend/tests/test_api.py`
- [X] T006 [P] [US1] Add a pending-chat state, in-progress status, and disabled send and agent-selection controls while a request is active in `frontend/src/app.js`
- [X] T007 [P] [US1] Style the in-progress chat status and disabled controls for clear feedback in `frontend/src/styles/app.css`

## Phase 4: User Story 2 - Recover when startup takes too long (Priority: P1)

**Goal**: A chat that exceeds its bounded wait is reported as a retryable timeout, retains the user's message, and restores interaction controls.

**Independent Test**: Simulate a socket timeout and verify HTTP 504 with an actionable message; verify connection errors remain HTTP 503. Confirm the browser retains the message, unlocks controls, permits retry, and does not duplicate the message or append a late response to another agent's conversation.

- [X] T008 [P] [US2] Map chat socket timeouts to a distinct timeout failure while keeping connection-refused errors classified as service unavailable in `backend/src/services/ollama_service.py`
- [X] T009 [P] [US2] Add API tests for socket timeout to HTTP 504 and connection failure to HTTP 503 in `backend/tests/test_api.py`
- [X] T010 [P] [US2] Return HTTP 504 with a safe, actionable timeout message for the chat wait limit in `backend/src/api/chat_routes.py`
- [X] T011 [US2] Preserve the submitted user message after timeout, restore controls, retain same-message retry behavior without duplicating the user entry, and prevent stale responses from updating a different agent context in `frontend/src/app.js`

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: Keep the contract and run instructions aligned with the implemented behavior; validate the feature.

- [X] T012 [P] Update the timeout, status mapping, and pending UI behavior in `specs/005-chat-model-startup-wait/contracts/chat-wait-contract.md`
- [X] T013 [P] Update expected behavior and manual cold-start validation steps in `specs/005-chat-model-startup-wait/quickstart.md`
- [X] T014 Run the full Python test suite with `.\.venv\Scripts\python.exe -m pytest -q` and verify frontend syntax with `node --check frontend\src\app.js` from the repository root (34 passed; syntax check passed)
- [X] T015 Perform the local-model and browser smoke validation from `specs/005-chat-model-startup-wait/quickstart.md` when Ollama and a model are available, recording elapsed time. Cold-start state was not forced.

## Recorded Validation

- The full Python suite passed: 34 tests.
- The live backend chat endpoint returned HTTP 200 after 95.22 seconds for the first tested local-model request. The model was not explicitly unloaded beforehand, so this does not prove a cold start.
- In the browser, the pending status appeared and send, agent selection, refresh, create, and delete controls were disabled. The response appeared once and the controls were restored.
- The browser console also reported a missing `favicon.ico` (404), unrelated to chat behavior.

## Parallel Execution Examples

### After Phase 2

```text
Task A: T004 and T005 - Apply the chat-specific wait bound and add its backend test in separate service and test files
Task B: T006 and T007 - Implement pending state and its styling in separate frontend files
```

T004 and T005 can be authored in parallel because they target separate files; the new test should fail until the implementation lands. T006 and T007 target different frontend files and can also proceed in parallel.

### User Story 2

```text
Task A: T008 and T009 - Implement timeout classification and its API tests in separate service and test files
Task B: T011 - Implement timeout recovery and stale-response protection in frontend/src/app.js
```

T008 and T009 can be authored in parallel because they target separate files; the tests should fail until the classification is implemented. T010 also targets a separate route file and can be developed in parallel. T009 should be completed before final validation T014.

### Polish

T012 and T013 update separate documentation files and can proceed in parallel; reconcile both with the final implementation before T014.

## Implementation Strategy

1. Establish per-call timeout support without changing the default for non-chat requests.
2. Deliver US1 by applying the bounded 300-second timeout to chat and making the pending state visible.
3. Deliver US2 by distinguishing timeout from connectivity failures and retaining a retryable conversation state.
4. Run all tests and frontend syntax validation; do a real cold-start test only when the local Ollama service and model are available.

**Suggested MVP**: Complete Phase 2 and US1 first. This directly prevents the reported 10-second client abort while keeping the wait finite. US2 adds explicit timeout classification and recovery.

## Format Validation

All task entries use `- [ ]`, sequential task IDs, story labels for user-story phases, `[P]` only where tasks can be performed independently, and concrete repository-relative file paths or commands.
