# Ollama Agent CLI

A lightweight local terminal application for working with Ollama-based AI agents.

## What this project does

This project gives you a simple CLI workflow to:

- list the Ollama models or agents available on your machine,
- create a new agent from a Modelfile,
- delete an existing agent after confirmation,
- open a chat session with a selected model and keep a local conversation history.

It is designed for developers and local users who want a fast, terminal-first way to interact with local models without needing a web UI or remote platform.

## Why it exists

The tool reduces friction when working with locally-hosted LLMs. Instead of juggling multiple commands in separate tools, you can stay in one terminal session, manage agent instances, and chat with them directly.

This is especially useful when:

- you want to keep model usage local and private,
- you are testing custom Modelfiles for local agents,
- you want a minimal, scriptable workflow for agent management.

## Main features

- Agent listing and selection from the local Ollama registry
- Optional direct startup with a chosen agent name
- Creation of custom agents using `ollama create <name> -f <modelfile>`
- Removal of agents with explicit confirmation
- Terminal chat with special commands for multi-line input, file context, cleanup, and saving conversations

## How it works

The application is implemented in `agents.py` and uses the Ollama HTTP API at `http://localhost:11434` by default.

At a high level, the flow is:

1. Load available models from `GET /api/tags`.
2. Present a menu or direct-agent selection.
3. Allow the user to create, remove, or chat with a model.
4. Send chat requests through the Ollama `/api/chat` endpoint.
5. Save conversation history under a local `conversas/` folder when requested.

The main interactive commands inside the chat loop are:

- `/multi` - paste multi-line text until a line containing `FIM`
- `/arquivo` - send the content of a file as part of the prompt
- `/agente` - switch to another agent
- `/limpar` - clear the current conversation history
- `/pensar` - show or hide reasoning output from the model
- `/salvar` - save the conversation as a Markdown file
- `/ajuda` - show available commands
- `/sair` - exit the chat

## Requirements

Before running the application, make sure the following are available:

- Python 3.11 or newer
- Ollama installed locally
- Ollama service running and reachable at `http://localhost:11434`
- A terminal or shell with access to the repository

If Ollama is not running, the project cannot list or chat with local models.

## Quick start

From the project root, run:

```bash
python agents.py
```

If you already know the model you want to use:

```bash
python agents.py llama3.2
```

You may also create a new agent by selecting the create action in the menu and pointing to a valid Modelfile.

## Typical workflow

1. Start Ollama locally.
2. Run the CLI.
3. Choose an existing model or create a new one.
4. Start a chat session.
5. Use `/ajuda` to see supported interactive commands.
6. Save or clean up conversations as needed.

## Troubleshooting

### Ollama is not reachable

The app will report that it could not connect to the Ollama service. In most cases, this means Ollama is not running.

Use:

```bash
ollama serve
```

or start the Ollama desktop application, then retry the CLI.

### No models are installed

If the project reports that no agents are available, run:

```bash
ollama list
```

If that returns nothing, you need to pull or create a model before using the application.

### Modelfile path is invalid

When creating an agent, the path must point to an existing file. Verify that:

- the file exists,
- the path is correct,
- the file is readable,
- the file is a valid Modelfile.

### Conversation or agent actions fail

Check the error returned by the command output and confirm that:

- the model name is valid,
- the Ollama service is running,
- the model is installed and available,
- there are no permission problems on the local filesystem.

## Project structure

- `agents.py` - main terminal application
- `tests/test_agent_management.py` - unit tests covering agent selection and command behavior
- `specs/002-documentacao-aplicacao/` - feature planning and documentation artifacts
- `conversas/` - local directory created at runtime for saved conversation logs

## Maintenance notes

This project is intentionally small and focused. The main responsibilities live in a single script, while tests validate the main user flows such as model selection, agent creation, and command execution safety.

When updating the project, keep the documentation aligned with the actual CLI behavior. Particularly review:

- model selection flow,
- creation/deletion procedures,
- command behavior and outputs,
- local runtime dependencies like Ollama.

## License

This repository does not currently declare a project license in the root directory. If you plan to share or distribute the project more broadly, add an explicit license file before publication.
