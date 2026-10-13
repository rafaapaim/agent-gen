# Quickstart: Front-end Validation Guide

## Purpose

This guide explains how to validate the front-end feature end to end once the implementation is in place. It focuses on the primary user flows: loading the interface, listing agents, creating and deleting them, and chatting with a selected model.

## Prerequisites

- Python 3.11+
- Ollama installed and running locally at `http://localhost:11434`
- A browser available on the same machine or accessible via localhost
- Access to the repository and the backend/frontend implementation files

## Setup

1. Create and activate a Python virtual environment.
2. Install the backend dependencies required by the project, including the API framework and any supporting libraries.
3. Start the backend server on a local port such as `8000`.
4. Open the front-end in a browser at the served local URL.

## Validation Scenarios

### 1. Empty state

Expected result:
- The home screen loads correctly.
- The interface shows that no agents are currently available.
- The user sees a clear action to create a new one.

### 2. Agent list and selection

Expected result:
- The page loads the available local agents from the backend.
- Each agent appears with a readable status label.
- A user can select an agent without shell commands.

### 3. Create agent flow

Expected result:
- The user can submit a valid agent name and Modelfile path.
- The backend validates the input and rejects duplicates or invalid files.
- The list refreshes and shows the newly created agent.

### 4. Delete agent flow

Expected result:
- Selecting an existing agent and choosing delete triggers a confirmation step.
- A cancellation keeps the agent list unchanged.
- Confirmed deletion removes the agent and refreshes the list.

### 5. Chat flow

Expected result:
- A user selects an agent and enters a prompt.
- The interface displays the user message and the assistant response in sequence.
- Later messages continue the same conversation context.

### 6. Error and recovery flow

Expected result:
- When Ollama is offline, the UI surfaces a visible error message and recovery guidance.
- The interface remains usable and tells the user how to recover.

## Expected Outcome

The implementation should allow a user to complete the core flow—select an agent, create or remove one when needed, and chat with it—without relying on the command line or shell access.

This is the acceptance-level validation for the front-end feature.
