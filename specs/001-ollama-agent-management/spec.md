# Feature Specification: Ollama Agent Management

**Feature Branch**: `001-ollama-agent-management`

**Created**: 2026-10-12

**Status**: Draft

**Input**: User description: "Precisamos das seguintes novas features: adicionar um modo de criar novos agentes alterando o arquivo Modelfile para a criação do novo agente; adicionar um modo de deletar um agente criado usando o comando `ollama rm <nome_do_modelo>`."

## User Scenarios & Testing

### User Story 1 - Create an agent (Priority: P1)

As a user, I want to create an agent from a Modelfile so that I can add a customized model to the agents available in the application.

**Why this priority**: Creating agents is the primary requested capability and makes customized agents available for use.

**Independent Test**: Start the creation flow, provide a valid Modelfile and a model name, complete creation, and verify that the new agent appears in the available-agents list and can be selected.

**Acceptance Scenarios**:

1. **Given** the application can reach Ollama and the user has a valid Modelfile, **When** the user starts agent creation, provides the Modelfile and a model name, and confirms, **Then** the agent is created and becomes available in the agent list.
2. **Given** the user is in the creation flow, **When** the user cancels before confirming, **Then** no agent is created and no existing agent is changed.
3. **Given** the provided Modelfile or model name cannot be used, **When** creation is attempted, **Then** the user receives an actionable error and can correct the input or cancel.

### User Story 2 - Delete an agent (Priority: P2)

As a user, I want to remove an agent I no longer need so that it no longer appears among the agents available in the application.

**Why this priority**: Removing agents is the second requested capability and lets users manage models they have created.

**Independent Test**: Select an installed agent for removal, confirm the action, and verify that the agent is removed from the available-agents list.

**Acceptance Scenarios**:

1. **Given** at least one installed agent is available, **When** the user selects an agent for deletion and confirms, **Then** the application removes that model using `ollama rm <nome_do_modelo>` and refreshes the available-agents list.
2. **Given** the user is asked to confirm deletion, **When** the user cancels, **Then** the model remains installed and available.
3. **Given** the selected model cannot be removed, **When** deletion is attempted, **Then** the user receives an error and the application does not report successful deletion.

### Edge Cases

- Ollama is unavailable when the user starts creation or deletion.
- The Modelfile path does not exist, cannot be read, or does not describe a model that Ollama can create.
- The user enters an empty or invalid model name, or a name that conflicts with an existing model.
- There are no installed agents to delete.
- A model disappears between the time it is listed and the time the user confirms deletion.
- The user cancels either operation; cancellation must leave installed models unchanged.
- A create or delete operation fails after it has started; the application must report the failure and refresh its displayed agent list when possible.

## Requirements

### Functional Requirements

- **FR-001**: The application MUST provide an agent-creation option in addition to the existing agent selection and chat flows.
- **FR-002**: The creation flow MUST let the user provide a Modelfile and the name for the new agent.
- **FR-003**: Before creation, the application MUST allow the user to review and confirm the requested operation or cancel it without creating an agent.
- **FR-004**: The application MUST create the requested agent from the provided Modelfile and report whether creation succeeded.
- **FR-005**: After successful creation, the application MUST refresh the available-agent list so the new agent can be selected.
- **FR-006**: The application MUST provide a deletion option for installed agents.
- **FR-007**: Before deletion, the application MUST identify the selected agent and require explicit confirmation; cancellation MUST leave that agent installed.
- **FR-008**: On confirmation, the application MUST remove the selected model using the requested `ollama rm <nome_do_modelo>` operation.
- **FR-009**: After successful deletion, the application MUST refresh the available-agent list and no longer offer the deleted model.
- **FR-010**: The application MUST clearly report connection, validation, creation, and deletion failures and MUST NOT report an operation as successful when it failed.
- **FR-011**: The existing ability to list, select, and chat with installed agents MUST continue to work.

### Key Entities

- **Agent**: An Ollama model available for selection in the application, identified by its model name.
- **Modelfile**: The user-provided description used to create an agent.
- **Agent operation**: A creation or deletion request, including the selected inputs, confirmation or cancellation, and final outcome.

## Success Criteria

### Measurable Outcomes

- **SC-001**: In testing with a valid Modelfile and a reachable Ollama service, users can complete agent creation and select the new agent in 100% of attempts.
- **SC-002**: In testing with an installed model, confirmed deletion removes that model from the available-agent list in 100% of successful attempts.
- **SC-003**: In testing, cancelling either operation leaves the relevant installed-model list unchanged in 100% of attempts.
- **SC-004**: In testing, every simulated connection, validation, creation, or deletion failure is reported as a failure and never as a success.
- **SC-005**: Existing agent selection and chat scenarios continue to pass after the management options are added.

## Assumptions

- The application continues to use the local Ollama service and terminal interaction already used for agent selection and chat.
- Users provide or edit a Modelfile suitable for Ollama and choose the model name for the resulting agent.
- The agent list reflects models available from Ollama; deleting a model removes it from that local Ollama installation.
- Deletion is intentionally destructive, so a confirmation step is required before the requested model-removal operation runs.
- The feature is limited to creating and deleting agents; changing chat behavior, conversation history, or existing models during creation is out of scope.
