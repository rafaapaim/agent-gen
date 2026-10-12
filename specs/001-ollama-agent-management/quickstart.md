# Quickstart: Ollama Agent Management

## Prerequisites

- Python 3.10 or newer.
- Ollama installed and running locally.
- The `ollama` executable available on `PATH`.
- A valid Modelfile for the model to create.

## Automated validation

From the workspace root, run:

```powershell
py -m unittest discover -s tests -v
```

The unit tests should mock Ollama calls and verify creation, deletion, confirmation cancellation, invalid inputs, command failures, and preservation of existing model-selection behavior. They must not require a running Ollama service or alter installed models.

## Manual end-to-end validation

1. Start Ollama and confirm that `ollama list` works.
2. Start the application with `py agents.py`.
3. At the main menu, enter `c` to create an agent, enter a new model name and the path to a valid Modelfile, review the details, and confirm with `s`.
4. Verify the success message, confirm the model appears in the refreshed menu, and select it to start a chat.
5. At the main menu, enter `r` to remove an agent, select that model by number or name, and decline confirmation. Verify it remains in the list.
6. Repeat deletion, confirm with `s`, and verify the success message and that the model is absent from the refreshed list.
7. Test a missing Modelfile path and a model name already in use; verify both are reported and no existing model is changed.
8. Test an invalid Ollama command/environment where practical; verify that the application reports failure and does not claim success.

See [the terminal interface contract](./contracts/terminal-interface.md) and [the transient data model](./data-model.md) for expected behavior and validation.
