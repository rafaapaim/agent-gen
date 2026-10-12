# Research: Ollama Agent Management

**Feature**: [Ollama Agent Management](./spec.md)
**Date**: 2026-10-12

## Decision 1: Keep the current terminal application and add management choices

- **Decision**: Add create and delete actions to the current agent-selection menu and keep the existing chat interaction unchanged.
- **Rationale**: `agents.py` is the only application source file; it already provides the terminal menu, model listing through Ollama's local HTTP API, and chat. A new interface or additional service would add complexity without helping the requested flows.
- **Alternatives considered**: A separate management program or a graphical interface. Both duplicate the existing entry point or expand scope unnecessarily.

## Decision 2: Create from a user-supplied Modelfile path

- **Decision**: Ask for a model name and a path to the Modelfile the user has prepared, validate that the path is a readable file, show a summary, and require confirmation before invoking Ollama.
- **Rationale**: The specification requires creation from a Modelfile but does not prescribe an editor or a project-owned Modelfile template. Using a path allows users to edit the file with their preferred editor and avoids silently overwriting or inventing file contents.
- **Alternatives considered**: Add an inline Modelfile editor or create/modify a default `Modelfile` in the project. Those choices establish editing and overwrite behavior not requested by the specification.

## Decision 3: Use the Ollama CLI for create and delete

- **Decision**: Invoke `ollama create <model> -f <Modelfile path>` and `ollama rm <model>` as argument lists with `subprocess.run(..., shell=False)`, capture output, and check the exit status.
- **Rationale**: The user explicitly requested the `ollama rm` operation. The Ollama CLI also provides the direct creation operation for a Modelfile. Argument-list execution safely handles paths with spaces and prevents model names or paths from being interpreted as shell syntax.
- **Alternatives considered**: Implement model creation/deletion through HTTP API calls. This would diverge from the requested delete operation and duplicate the CLI's existing capability.

## Decision 4: Require an explicit confirmation for both model-changing operations

- **Decision**: Show the model name and Modelfile path before creation; show the exact model name before deletion. A negative or empty response cancels without invoking a command.
- **Rationale**: Creation may target an existing name and deletion is destructive. Confirmation gives the user a chance to catch mistakes before Ollama changes local models.
- **Alternatives considered**: Run operations immediately after input. This risks unintended replacement or removal and conflicts with cancellation guarantees in the specification.

## Decision 5: Reject a name that already exists before creating

- **Decision**: Refresh the installed model list before creation and reject an exact model-name collision with a clear message rather than replacing an existing model.
- **Rationale**: The specification identifies name conflicts as an edge case and requires cancellation not to change an existing agent. Refusing collisions protects installed models and gives predictable behavior.
- **Alternatives considered**: Permit replacement after another confirmation. This would add a separate destructive workflow not included in the requested scope.

## Decision 6: Treat nonzero exit status and missing CLI as explicit failures

- **Decision**: Report command output and a clear failure when the Ollama executable cannot be started or exits unsuccessfully. After a successful operation, refresh the model list; do not display success before the command has succeeded.
- **Rationale**: A successful process launch does not prove that the model operation succeeded. Captured exit status and output provide actionable feedback without success-shaped fallbacks.
- **Alternatives considered**: Assume success when no exception is raised, or silently return to the menu. Both can leave the user with an incorrect model list or false success.

## Decision 7: Use standard-library `unittest` and mocks

- **Decision**: Add focused tests using `unittest` and mocks for subprocess calls, prompts, and model-list responses.
- **Rationale**: The repository has no dependency manifest or tests. The standard library keeps the single-file application dependency-free and allows testing destructive and failure paths without a live Ollama daemon.
- **Alternatives considered**: Add a third-party test framework or rely only on manual tests. A new dependency is disproportionate, while manual-only checks do not adequately cover cancellation and error cases.
