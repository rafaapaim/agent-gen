# Terminal Interface Contract

The feature extends the existing interactive menu in `agents.py`. Existing numeric model selection, exact-name selection, and chat commands remain supported.

## Main Menu

- Display the currently installed models and keep the existing numeric/exact-name selection behavior.
- Add a clearly labeled create-agent action and delete-agent action.
- Keep an exit action.
- When the model list is empty, still offer create and exit; deletion must explain that no installed agent is available.
- Refresh the installed-model list after successful creation or deletion.

## Create Agent

1. Prompt for a non-empty model name.
2. Refresh the installed model names and reject a name that already exists.
3. Prompt for a Modelfile path; reject missing, non-file, or unreadable paths with an actionable message.
4. Display the model name and Modelfile path and ask for confirmation.
5. If declined or interrupted before execution, cancel without invoking Ollama.
6. If confirmed, invoke `ollama create <model_name> -f <modelfile_path>` without a shell.
7. Report success only for a zero exit status; otherwise report failure and captured diagnostic output.

## Delete Agent

1. Refresh and display installed agents; if none exist, explain that there is nothing to delete.
2. Let the user select one installed model by its displayed number or exact name.
3. Display the exact model name and require confirmation.
4. If declined or interrupted before execution, cancel without invoking Ollama.
5. If confirmed, invoke `ollama rm <model_name>` without a shell.
6. Report success only for a zero exit status; otherwise report failure and captured diagnostic output.

## Error and Output Behavior

- Missing Ollama executable, failed command, invalid path/name, and unavailable model-list service must be reported as failures with enough detail to guide recovery.
- User-provided names and paths are passed as individual process arguments; shell interpretation is not permitted.
- The menu must not claim that a model was created or deleted until the command succeeds.
- A model-list refresh after success must not hide an error if Ollama is unavailable.
