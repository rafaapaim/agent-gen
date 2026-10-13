# Feature Specification: Backend and Frontend Run Documentation

**Feature Branch**: `007-backend-frontend-run-docs`

**Created**: 2026-10-13

**Status**: Draft

**Input**: User description: "Melhore a documentação acrescentando como executar o backend e o frontend."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Start the local web application from the documentation (Priority: P1)

As a developer or local user, I want clear instructions for starting the backend and frontend, so I can open the web interface and use the application without guessing commands or setup steps.

**Why this priority**: The web application requires both a backend API and a frontend page, but the current documentation does not explain the complete startup sequence and browser address clearly.

**Independent Test**: Follow the documentation from the repository root on a machine with Python installed, start the documented services in separate terminals, and open the documented frontend address.

**Acceptance Scenarios**:

1. **Given** the user has opened the project root and has not installed backend dependencies, **When** they follow the setup instructions, **Then** they can install the required dependencies before starting the backend.
2. **Given** the backend dependencies are installed, **When** the user follows the backend startup instructions, **Then** the API starts at the documented local address and port.
3. **Given** the backend is running, **When** the user follows the frontend startup instructions in a separate terminal, **Then** the static frontend is served at a documented address that can be opened in the browser.
4. **Given** the user has started both services and Ollama, **When** they open the frontend address, **Then** the page can reach the backend and show available agents or a clear empty state.

### Edge Cases

- The user attempts to open the frontend file directly instead of serving it over HTTP.
- The backend or frontend port is already in use.
- Ollama is not running while the web application is opened.
- The commands are launched from a directory other than the repository root.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The project documentation MUST provide the prerequisites for running the local web application, including Python, Ollama, and required backend packages.
- **FR-002**: The project documentation MUST provide an explicit backend dependency installation command that works from the repository root.
- **FR-003**: The project documentation MUST provide an explicit backend startup command and identify the local address and port where the API is available.
- **FR-004**: The project documentation MUST provide an explicit frontend startup command, identify that it runs in a separate terminal, and state the browser URL to open.
- **FR-005**: The project documentation MUST explain that Ollama must be running locally for agent listing and chat to work.
- **FR-006**: Startup instructions in the README and quickstart guide MUST be consistent with each other and with the current project structure.
- **FR-007**: The documentation MUST include basic recovery guidance for service startup failures, including an occupied port or unreachable Ollama service.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A user starting from the repository root can identify the complete backend and frontend startup sequence, including the need for two terminals, in under 2 minutes.
- **SC-002**: A user following the documentation can start both local services and reach the frontend without needing an undocumented command.
- **SC-003**: 100% of documented commands, service addresses, and ports match the repository's current backend and frontend configuration.
- **SC-004**: The README and quickstart provide consistent prerequisites, startup steps, browser address, and Ollama dependency guidance.

## Assumptions

- The documentation should cover the browser-based local web application, not change how the CLI is launched.
- Python and Ollama are installed on the user's local machine.
- The user starts commands from the repository root and runs the backend and static frontend server in separate terminals.
- The existing backend and frontend ports remain the documented defaults unless the project configuration changes.
