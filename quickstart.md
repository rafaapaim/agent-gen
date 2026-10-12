# Quickstart

This guide explains how to verify that the application is installed correctly and ready to use.

## Prerequisites

Before running the CLI, ensure that:

- Python 3.11+ is installed
- Ollama is installed locally
- Ollama is running on `http://localhost:11434`
- you have a terminal open in the project root

## Verify the environment

Run:

```bash
python --version
ollama list
```

If `ollama list` fails, start Ollama first:

```bash
ollama serve
```

## Start the application

From the repository root:

```bash
python agents.py
```

The menu will show the available installed agents and options to create or remove them.

## Use an existing agent

Choose one of the listed agents or type its name directly when prompted.

You can also skip the menu and open a chat directly:

```bash
python agents.py llama3.2
```

## Create a new agent

From the main menu, choose the create option and provide:

- a unique agent name,
- the path to an existing Modelfile,
- confirmation to proceed.

Example:

```bash
python agents.py
```

Then select the create action and provide the Modelfile path.

## Delete an agent

From the main menu, choose the delete option, confirm the model name, and confirm the removal.

## Chat commands

Once inside a chat session, use the built-in commands:

- `/ajuda` to display help
- `/agente` to switch agents
- `/limpar` to clear the conversation history
- `/salvar` to save the conversation as Markdown
- `/multi` to send multi-line text
- `/arquivo` to include file content in the prompt
- `/pensar` to show or hide reasoning output
- `/sair` to end the session

## Validation checklist

Use this short checklist after setup:

- [ ] Python runs successfully
- [ ] Ollama is running locally
- [ ] `ollama list` returns available models
- [ ] `python agents.py` starts the menu without errors
- [ ] A model can be selected and a chat session opens
- [ ] A custom agent can be created from a valid Modelfile
- [ ] A deletion action can be confirmed and completed

## Troubleshooting

If the application cannot connect to Ollama:

1. confirm the Ollama service is running,
2. confirm the URL is `http://localhost:11434`,
3. check whether the local installation is healthy with `ollama list`,
4. retry after restarting Ollama if needed.

If a model is not available:

1. pull or create it,
2. verify the name exactly matches the installed model,
3. rerun the CLI.

If a Modelfile fails during creation:

1. verify the file exists,
2. check the path format,
3. ensure it is readable,
4. confirm it is a valid Modelfile for the Ollama toolchain.
