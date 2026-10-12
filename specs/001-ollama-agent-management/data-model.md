# Data Model: Ollama Agent Management

This feature adds no persistent application data. The entities below describe the values and transient states used during one terminal operation.

## Agent

An installed Ollama model that can be selected for chat or deleted.

| Field | Description | Validation |
|-------|-------------|------------|
| `name` | Ollama model identifier, including an optional tag | Must be non-empty; compare against the current installed-model list before creation and deletion |

## Modelfile Input

The file from which Ollama creates an agent.

| Field | Description | Validation |
|-------|-------------|------------|
| `path` | User-provided path to a Modelfile | Must resolve to an existing readable regular file |
| `model_name` | Name assigned to the created agent | Must be non-empty and must not exactly match an installed model |

The application does not edit or persist Modelfile contents. The user prepares the file using their preferred editor.

## Agent Management Operation

A transient request to create or delete one model; it is not stored after the menu action completes.

| Field | Description | Validation |
|-------|-------------|------------|
| `kind` | `create` or `delete` | Must identify one supported action |
| `model_name` | Model affected by the operation | Must be non-empty |
| `modelfile_path` | Source file for a create operation | Required only for creation and must pass Modelfile path validation |
| `state` | Current operation state | One of `pending`, `cancelled`, `succeeded`, or `failed` |
| `message` | User-facing outcome or error detail | Must reflect the actual confirmation and Ollama command result |

### State Transitions

```text
pending ── user declines ──> cancelled
pending ── command succeeds ──> succeeded
pending ── validation/launch/command fails ──> failed
```

Cancelled operations do not invoke Ollama. Failed operations are never reported as successful. Successful create/delete operations are followed by a model-list refresh.
