# Implementation Plan: Ollama Agent Management

**Branch**: `N/A (workspace is not a Git repository)` | **Date**: 2026-10-12 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `specs/001-ollama-agent-management/spec.md`

## Summary

Add create and delete choices to the existing terminal agent manager in `agents.py`. Create an Ollama model from a user-provided Modelfile with `ollama create <model> -f <path>`; remove a selected installed model with `ollama rm <model>` only after explicit confirmation. Keep the existing Ollama HTTP API for listing models and chatting. Invoke the Ollama CLI with argument arrays (never through a shell), report errors, and refresh the list after successful changes.

## Technical Context

**Language/Version**: Python 3.10+ (the existing code uses union type syntax; observed bytecode is CPython 3.13)

**Primary Dependencies**: Python standard library (`subprocess`, `pathlib`, existing `urllib` and `json`); Ollama CLI and local Ollama service

**Storage**: No new persistent application data; models remain managed by Ollama

**Testing**: Python standard-library `unittest`; mock subprocess execution and the model-list API for deterministic tests, with a manual Ollama-backed smoke test

**Target Platform**: Platforms supported by Python and Ollama, including the current Windows workspace

**Project Type**: Single-project terminal application

**Performance Goals**: Management actions complete when Ollama CLI completes; no additional performance target is needed for this local interactive tool

**Constraints**: Preserve the existing list/select/chat behavior; require confirmation before destructive removal; do not invoke a shell or silently report failed commands as successful; no third-party dependencies

**Scale/Scope**: One local Ollama installation and its installed model list; one management operation at a time

## Constitution Check

The current `.specify/memory/constitution.md` contains only unfilled template placeholders and defines no ratified project principles or gates.

- **Scope and simplicity**: PASS — extend the existing single-file terminal application without adding a service, framework, or persistent store.
- **Safety**: PASS — pass user values as subprocess arguments, validate the Modelfile path, and require explicit deletion confirmation.
- **Compatibility**: PASS — retain the current model-listing and chat paths and add management as separate menu actions.
- **Testability**: PASS — isolate CLI calls and user interaction sufficiently to test outcomes without requiring a running Ollama instance.

No constitution violations or complexity exceptions are identified.

## Project Structure

### Documentation (this feature)

```text
specs/001-ollama-agent-management/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   └── terminal-interface.md
└── tasks.md                 # Created by /speckit-tasks
```

### Source Code (repository root)

```text
agents.py                    # Existing terminal UI, Ollama API calls, and chat loop
tests/
└── test_agent_management.py # New unit tests for create/delete flows and regressions
```

**Structure Decision**: This workspace is a single Python application with `agents.py` at its root and no existing test suite or package layout. Keep the production change in that module and add focused standard-library tests under `tests/`.

## Complexity Tracking

No constitution violations require justification.
