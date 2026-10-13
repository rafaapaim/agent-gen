# Tasks: Fix Chat Request Failures

**Input**: Design documents in `specs/004-fix-chat-errors/`
**Prerequisites**: `plan.md`, `spec.md`, `research.md`, `data-model.md`, `contracts/chat-contract.md`, `quickstart.md`

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Setup)**: No code changes are needed; confirms the existing validation baseline.
- **Phase 2 (Foundational)**: Establishes shared upstream error classification. Must complete before both user stories.
- **Phase 3 (US1)**: Successful chat response behavior. Depends on Phase 2.
- **Phase 4 (US2)**: Accurate errors and recovery. Depends on Phase 2. May proceed in parallel with US1 after Phase 2, except any tasks editing the same files must be serialized.
- **Phase 5 (Polish)**: Final targeted validation and documentation alignment after user stories.

### User Story Completion Order

`US1` and `US2` are both P1 and independently testable after the shared error classification foundation. They can be implemented in either order. Avoid concurrent edits to `backend/src/services/ollama_service.py`, `backend/src/api/chat_routes.py`, `backend/tests/test_api.py`, or `frontend/src/app.js`.

## Phase 1: Setup

**Purpose**: Confirm the existing chat tests and dependencies are available before modifying behavior.

- [X] T001 Run the current focused API baseline with `.\.venv\Scripts\python.exe -m pytest backend/tests/test_api.py -q` and record the result in the task execution report

## Phase 2: Foundational

**Purpose**: Create a stable failure classification from Ollama service through the chat endpoint; both stories depend on this.

- [X] T002 Define explicit internal chat failure categories and safe public messages in `backend/src/services/ollama_service.py`
- [X] T003 Preserve upstream HTTP status/body classification separately from connection and timeout failures in `backend/src/services/ollama_service.py`

## Phase 3: User Story 1 - Send a message to an available agent (Priority: P1)

**Goal**: A valid chat request to an available agent returns the actual usable assistant response and remains compatible with the browser.

**Independent Test**: Mock a successful Ollama chat response and verify `POST /api/chat` returns HTTP 200 with `role: assistant` and the expected non-empty content; verify sequential chat requests each return their corresponding response.

- [X] T004 [US1] Validate successful upstream chat payloads and return the existing assistant response shape in `backend/src/services/ollama_service.py`
- [X] T005 [US1] Add API tests for successful and sequential chat responses in `backend/tests/test_api.py`
- [X] T006 [US1] Verify the browser appends successful assistant responses after the submitted message without clearing earlier messages in `frontend/src/app.js`

## Phase 4: User Story 2 - Understand and recover from chat failures (Priority: P1)

**Goal**: Classify chat failures accurately, present actionable errors, and preserve the conversation so users can retry or switch agents.

**Independent Test**: Mock invalid input, unknown agent, unreachable service, other upstream HTTP errors, and unusable responses; verify each produces the contract status and safe `error` message, and that the browser retains the conversation after a failure.

- [X] T007 [US2] Map invalid input, missing agent, upstream rejection, connectivity, and unusable response categories to the documented status codes and safe JSON error envelope in `backend/src/api/chat_routes.py`
- [X] T008 [P] [US2] Add API tests for invalid input, unknown agent, connection failure, upstream rejection, timeout, and malformed or empty response in `backend/tests/test_api.py`
- [X] T009 [US2] Keep failed user messages and prior conversation visible, display actionable error feedback, and allow explicit retry or agent change in `frontend/src/app.js`

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: Verify contract consistency and end-to-end recovery scenarios.

- [X] T010 [P] Align the chat endpoint documentation with the implemented statuses and safe error messages in `specs/004-fix-chat-errors/contracts/chat-contract.md`
- [X] T011 Run the focused API suite and complete the available success, unknown-agent, service-unavailable, and retry scenarios documented in `specs/004-fix-chat-errors/quickstart.md`
- [X] T012 Review user-facing chat error messages for unnecessary stack traces, local paths, or raw upstream diagnostic details in `backend/src/services/ollama_service.py` and `frontend/src/app.js`

## Parallel Execution Examples

### After Phase 2

- US1 response validation and API tests can be developed as a slice, but T004 precedes meaningful T005 validation.
- US2 documentation/error mapping and success-flow work may proceed separately only when edits do not overlap.
- T008 can be prepared in parallel with frontend recovery work T009 because they target different files.
- T011 is parallelizable with implementation after the behavior is agreed, but must be reconciled against the final implementation before completion.

### Suggested parallel batch for US2

```text
Task A: T008 - Add service/API failure tests in backend/tests/test_api.py
Task B: T009 - Preserve browser conversation and improve recoverable error feedback in frontend/src/app.js
```

## Implementation Strategy

1. Establish explicit failure types and classification in the Ollama adapter.
2. Deliver the minimum successful-chat increment (US1) and prove the response shape through API tests.
3. Deliver error classification and recovery (US2), keeping error responses compatible with the frontend's `error` field.
4. Run focused automated tests, then perform the local Ollama/browser smoke test when the dependency and an installed model are available.

**Suggested MVP**: Complete Phase 2 and User Story 1. This verifies that a valid request produces the assistant reply; User Story 2 then makes failures classifiable and recoverable.

## Format Validation

All task entries use the required checkbox, sequential task ID, applicable parallel/story labels, and a concrete file path or runnable repository-relative command.
