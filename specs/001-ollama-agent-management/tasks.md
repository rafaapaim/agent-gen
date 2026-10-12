# Tasks: Ollama Agent Management

**Input**: Design documents from `specs/001-ollama-agent-management/`

**Prerequisites**: `plan.md`, `spec.md`, `research.md`, `data-model.md`, `contracts/terminal-interface.md`, `quickstart.md`

**Tests**: The implementation plan calls for standard-library `unittest` coverage using mocks. Tests below run without Ollama and must not change installed models.

**Organization**: Tasks are grouped by user story. The existing application and focused test suite are single files, so work that edits either file is intentionally sequenced to avoid conflicts.

## Format: `[ID] [P?] [Story] Description`

- `[P]` marks work that can proceed in parallel without editing another task's files or depending on incomplete work.
- `[US1]` maps a task to agent creation; `[US2]` maps a task to agent deletion.
- Every task names the file or files to change or validate.

## Phase 1: Setup

**Purpose**: Establish automated regression coverage for the existing terminal application before changing it.

- [X] T001 Create `unittest` scaffolding in `tests/test_agent_management.py` with mocked model-list responses and passing regression tests for existing model listing and agent selection.

## Phase 2: Foundational

**Purpose**: Add and validate the shared, safe Ollama CLI boundary used by both management flows.

- [X] T002 Add failing unit tests in `tests/test_agent_management.py` for a shared `run_ollama_command(args)` helper, covering argument preservation, `shell=False`, nonzero exit status, and a missing Ollama executable.
- [X] T003 Implement `run_ollama_command(args)` in `agents.py` using an argument list without a shell, captured output, and explicit success/failure results; surface CLI launch errors.

**Checkpoint**: Shared CLI execution is tested and both user-story flows can build on it.

## Phase 3: User Story 1 - Create an agent (Priority: P1) 🎯 MVP

**Goal**: Create an Ollama agent from a user-provided Modelfile and make it selectable.

**Independent Test**: With mocked Ollama CLI and model listing, confirm a valid Modelfile and new name; verify the expected create arguments, success result, and refreshed list. Also verify cancellation and invalid inputs do not invoke creation.

### Tests for User Story 1

- [X] T004 Add failing creation-flow tests in `tests/test_agent_management.py` for a valid Modelfile, name collision, missing/unreadable Modelfile, cancellation, CLI failure, and model-list refresh after success.

### Implementation for User Story 1

- [X] T005 Implement the create-agent prompts and flow in `agents.py`: validate a non-empty non-existing model name and readable Modelfile path, confirm before action, run `ollama create <model_name> -f <path>` through `run_ollama_command`, report the actual result, and refresh models after success.
- [X] T006 Add the create-agent action to the main menu in `agents.py`, including when no models are installed, while preserving existing numbered and exact-name model selection.

**Checkpoint**: Creation works independently; a successfully created agent appears in the refreshed list and remains selectable for chat.

## Phase 4: User Story 2 - Delete an agent (Priority: P2)

**Goal**: Remove a selected installed agent only after explicit user confirmation.

**Independent Test**: With mocked model listing and CLI execution, select an installed model and confirm deletion; verify `ollama rm <model_name>` is invoked and the list is refreshed. Verify cancellation and command failure do not report deletion success.

### Tests for User Story 2

- [X] T007 Add failing deletion-flow tests in `tests/test_agent_management.py` for selecting by number/name, confirmation cancellation, no installed agents, a model that disappears before deletion, CLI failure, and list refresh after success.

### Implementation for User Story 2

- [X] T008 Implement the delete-agent flow and menu action in `agents.py`: refresh and select from installed models, handle an empty list, confirm the exact model name, invoke `ollama rm <model_name>` through `run_ollama_command`, report failures accurately, and refresh after success.

**Checkpoint**: Deletion works independently; cancellation leaves the model installed, and successful deletion removes it from the refreshed menu.

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: Verify all requirements and preserve documented operation guidance.

- [X] T009 Update `specs/001-ollama-agent-management/quickstart.md` if needed so its menu labels and manual steps match the implemented flows, then run `py -m unittest discover -s tests -v` and `py -m py_compile agents.py tests/test_agent_management.py` from the workspace root.

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies; provides baseline tests for current model listing and selection.
- **Foundational (Phase 2)**: Depends on T001 and blocks the user-story implementation by providing the tested CLI boundary.
- **User Story 1 (Phase 3)**: Depends on T003; delivers the MVP creation flow.
- **User Story 2 (Phase 4)**: Depends on T006 and T003; sequenced after creation because both stories edit `agents.py` and the same test module.
- **Polish (Phase 5)**: Depends on T005, T006, T007, and T008.

### User Story Dependencies

- **US1 (P1)**: Starts after the foundational CLI helper; independent acceptance criteria and the recommended MVP.
- **US2 (P2)**: Uses the same foundational CLI helper, but is scheduled after US1 to avoid concurrent edits to `agents.py` and `tests/test_agent_management.py`.

### Parallel Opportunities

- No `[P]` tasks are marked: every implementation and test task currently targets one of the same two files, so concurrent editing would conflict.
- After T003 is complete, a separate contributor could review `specs/001-ollama-agent-management/contracts/terminal-interface.md` against the implementation without editing these task files; this review is optional and is not a prerequisite.

## Parallel Example: User Story 1

No safe parallel task pair is identified for US1 because its test and implementation tasks both edit `tests/test_agent_management.py` or `agents.py`. Execute T004 before T005 and T006.

## Parallel Example: User Story 2

No safe parallel task pair is identified for US2 because its tests and implementation both edit `tests/test_agent_management.py` or `agents.py`. Execute T007 before T008.

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete T001-T003 to establish regression tests and the shared CLI boundary.
2. Complete T004-T006 to implement and independently validate agent creation.
3. Stop at the US1 checkpoint to verify that creation succeeds, cancellation is safe, and the created agent can be selected.
4. Deliver the creation flow as the initial usable increment if deletion is deferred.

### Incremental Delivery

1. Complete Setup and Foundational phases.
2. Deliver US1: create an agent from a Modelfile and verify that it appears in the list.
3. Deliver US2: confirm and remove an installed agent.
4. Complete the quickstart and full automated validation.

## Notes

- Tests are included because the implementation plan explicitly calls for `unittest` coverage with mocked subprocess calls and model-list responses.
- No manual test should delete a user's existing model; use a disposable model for the Ollama-backed deletion smoke test.
- User-provided model names and paths must stay separate process arguments; never interpolate them into a shell command.
