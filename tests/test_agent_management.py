import io
import subprocess
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

import agents


class ExistingAgentFlowTests(unittest.TestCase):
    def test_list_models_returns_sorted_model_names(self):
        with patch.object(
            agents,
            "api_get",
            return_value={"models": [{"name": "zeta:latest"}, {"name": "alpha:latest"}]},
        ):
            self.assertEqual(
                agents.list_models(),
                ["alpha:latest", "zeta:latest"],
            )

    def test_choose_agent_keeps_number_and_exact_name_selection(self):
        with patch("builtins.input", side_effect=["2"]):
            self.assertEqual(
                agents.choose_agent(["alpha:latest", "beta:latest"]),
                "beta:latest",
            )

        with patch("builtins.input", side_effect=["alpha:latest"]):
            self.assertEqual(
                agents.choose_agent(["alpha:latest", "beta:latest"]),
                "alpha:latest",
            )

    def test_choose_agent_retries_invalid_input(self):
        output = io.StringIO()
        with patch("builtins.input", side_effect=["invalid", "1"]):
            with redirect_stdout(output):
                selected = agents.choose_agent(["alpha:latest"])

        self.assertEqual(selected, "alpha:latest")
        self.assertIn("Opção inválida.", output.getvalue())


class OllamaCommandTests(unittest.TestCase):
    def test_run_ollama_command_preserves_arguments_without_shell(self):
        expected = subprocess.CompletedProcess(
            args=["ollama", "create", "custom agent", "-f", "C:\\models\\My Modelfile"],
            returncode=0,
            stdout="success",
            stderr="",
        )
        command = ["ollama", "create", "custom agent", "-f", "C:\\models\\My Modelfile"]
        with patch("agents.subprocess.run", return_value=expected) as run:
            result = agents.run_ollama_command(command)

        self.assertIs(result, expected)
        run.assert_called_once_with(
            command,
            shell=False,
            capture_output=True,
            text=True,
            check=False,
        )

    def test_run_ollama_command_exposes_missing_executable(self):
        with patch(
            "agents.subprocess.run",
            side_effect=FileNotFoundError("ollama was not found"),
        ):
            with self.assertRaises(FileNotFoundError):
                agents.run_ollama_command(["ollama", "rm", "custom"])

    def test_nonzero_exit_status_is_preserved_for_caller(self):
        failed = subprocess.CompletedProcess(
            args=["ollama", "rm", "custom"],
            returncode=1,
            stdout="",
            stderr="model is in use",
        )
        with patch("agents.subprocess.run", return_value=failed):
            result = agents.run_ollama_command(["ollama", "rm", "custom"])

        self.assertEqual(result.returncode, 1)
        self.assertEqual(result.stderr, "model is in use")


class CreateAgentTests(unittest.TestCase):
    def test_create_agent_runs_ollama_and_reports_success(self):
        with tempfile.TemporaryDirectory() as directory:
            modelfile = Path(directory) / "My Modelfile"
            modelfile.write_text("FROM llama3.2\n", encoding="utf-8")
            command_result = subprocess.CompletedProcess(
                args=[], returncode=0, stdout="created", stderr=""
            )
            output = io.StringIO()
            with (
                patch("builtins.input", side_effect=["custom:latest", str(modelfile), "s"]),
                patch.object(agents, "list_models", return_value=["base:latest"]),
                patch.object(agents, "run_ollama_command", return_value=command_result) as run,
                redirect_stdout(output),
            ):
                agents.create_agent()

        run.assert_called_once_with(
            ["ollama", "create", "custom:latest", "-f", str(modelfile.resolve())]
        )
        self.assertIn("criado", output.getvalue().lower())

    def test_create_agent_rejects_existing_name_without_running_ollama(self):
        output = io.StringIO()
        with (
            patch("builtins.input", side_effect=["base:latest"]),
            patch.object(agents, "list_models", return_value=["base:latest"]),
            patch.object(agents, "run_ollama_command") as run,
            redirect_stdout(output),
        ):
            agents.create_agent()

        run.assert_not_called()
        self.assertIn("já existe", output.getvalue())

    def test_create_agent_rejects_empty_name(self):
        output = io.StringIO()
        with (
            patch("builtins.input", return_value="  "),
            patch.object(agents, "list_models") as list_models,
            patch.object(agents, "run_ollama_command") as run,
            redirect_stdout(output),
        ):
            agents.create_agent()

        list_models.assert_not_called()
        run.assert_not_called()
        self.assertIn("não pode ficar vazio", output.getvalue())

    def test_create_agent_rejects_missing_modelfile(self):
        with tempfile.TemporaryDirectory() as directory:
            missing = Path(directory) / "missing.Modelfile"
            output = io.StringIO()
            with (
                patch("builtins.input", side_effect=["custom:latest", str(missing)]),
                patch.object(agents, "list_models", return_value=[]),
                patch.object(agents, "run_ollama_command") as run,
                redirect_stdout(output),
            ):
                agents.create_agent()

        run.assert_not_called()
        self.assertIn("Modelfile", output.getvalue())

    def test_create_agent_cancellation_does_not_run_ollama(self):
        with tempfile.TemporaryDirectory() as directory:
            modelfile = Path(directory) / "Modelfile"
            modelfile.write_text("FROM llama3.2\n", encoding="utf-8")
            output = io.StringIO()
            with (
                patch(
                    "builtins.input",
                    side_effect=["custom:latest", str(modelfile), "n"],
                ),
                patch.object(agents, "list_models", return_value=[]),
                patch.object(agents, "run_ollama_command") as run,
                redirect_stdout(output),
            ):
                agents.create_agent()

        run.assert_not_called()
        self.assertIn("cancel", output.getvalue().lower())

    def test_create_agent_reports_cli_failure(self):
        with tempfile.TemporaryDirectory() as directory:
            modelfile = Path(directory) / "Modelfile"
            modelfile.write_text("FROM llama3.2\n", encoding="utf-8")
            failed = subprocess.CompletedProcess(
                args=[], returncode=1, stdout="", stderr="invalid Modelfile"
            )
            output = io.StringIO()
            with (
                patch(
                    "builtins.input",
                    side_effect=["custom:latest", str(modelfile), "s"],
                ),
                patch.object(agents, "list_models", return_value=[]),
                patch.object(agents, "run_ollama_command", return_value=failed),
                redirect_stdout(output),
            ):
                agents.create_agent()

        self.assertIn("invalid Modelfile", output.getvalue())
        self.assertNotIn("agente criado", output.getvalue().lower())

    def test_main_menu_offers_create_with_no_installed_models(self):
        output = io.StringIO()
        with (
            patch("builtins.input", side_effect=["c"]),
            redirect_stdout(output),
        ):
            self.assertEqual(agents.choose_menu_action([]), "__create__")

        self.assertIn("Criar agente", output.getvalue())

    def test_main_refreshes_models_after_create_action(self):
        with (
            patch.object(agents.sys, "argv", ["agents.py"]),
            patch.object(agents, "list_models", side_effect=[[], ["new:latest"]]) as list_models,
            patch.object(
                agents, "choose_menu_action", side_effect=["__create__", None]
            ),
            patch.object(agents, "create_agent") as create,
            patch.object(agents, "chat") as chat,
            redirect_stdout(io.StringIO()),
        ):
            agents.main()

        self.assertEqual(list_models.call_count, 2)
        create.assert_called_once_with()
        chat.assert_not_called()


class DeleteAgentTests(unittest.TestCase):
    def test_delete_agent_runs_ollama_for_number_selection(self):
        success = subprocess.CompletedProcess(
            args=[], returncode=0, stdout="", stderr=""
        )
        output = io.StringIO()
        with (
            patch("builtins.input", side_effect=["2", "s"]),
            patch.object(agents, "list_models", return_value=["alpha:latest", "beta:latest"]),
            patch.object(agents, "run_ollama_command", return_value=success) as run,
            redirect_stdout(output),
        ):
            agents.delete_agent(["alpha:latest", "beta:latest"])

        run.assert_called_once_with(["ollama", "rm", "beta:latest"])
        self.assertIn("removido com sucesso", output.getvalue())

    def test_delete_agent_supports_exact_name_selection(self):
        success = subprocess.CompletedProcess(
            args=[], returncode=0, stdout="", stderr=""
        )
        with (
            patch("builtins.input", side_effect=["alpha:latest", "s"]),
            patch.object(agents, "list_models", return_value=["alpha:latest"]),
            patch.object(agents, "run_ollama_command", return_value=success) as run,
            redirect_stdout(io.StringIO()),
        ):
            agents.delete_agent(["alpha:latest"])

        run.assert_called_once_with(["ollama", "rm", "alpha:latest"])

    def test_delete_agent_cancellation_does_not_run_ollama(self):
        output = io.StringIO()
        with (
            patch("builtins.input", side_effect=["alpha:latest", "n"]),
            patch.object(agents, "list_models") as list_models,
            patch.object(agents, "run_ollama_command") as run,
            redirect_stdout(output),
        ):
            agents.delete_agent(["alpha:latest"])

        list_models.assert_not_called()
        run.assert_not_called()
        self.assertIn("cancelada", output.getvalue())

    def test_delete_agent_handles_empty_model_list(self):
        output = io.StringIO()
        with (
            patch("builtins.input") as user_input,
            patch.object(agents, "run_ollama_command") as run,
            redirect_stdout(output),
        ):
            agents.delete_agent([])

        user_input.assert_not_called()
        run.assert_not_called()
        self.assertIn("Não há agentes instalados", output.getvalue())

    def test_delete_agent_does_not_run_if_model_disappeared(self):
        output = io.StringIO()
        with (
            patch("builtins.input", side_effect=["alpha:latest", "s"]),
            patch.object(agents, "list_models", return_value=[]),
            patch.object(agents, "run_ollama_command") as run,
            redirect_stdout(output),
        ):
            agents.delete_agent(["alpha:latest"])

        run.assert_not_called()
        self.assertIn("não está mais instalado", output.getvalue())

    def test_delete_agent_reports_cli_failure(self):
        failed = subprocess.CompletedProcess(
            args=[], returncode=1, stdout="", stderr="model is in use"
        )
        output = io.StringIO()
        with (
            patch("builtins.input", side_effect=["alpha:latest", "s"]),
            patch.object(agents, "list_models", return_value=["alpha:latest"]),
            patch.object(agents, "run_ollama_command", return_value=failed),
            redirect_stdout(output),
        ):
            agents.delete_agent(["alpha:latest"])

        self.assertIn("model is in use", output.getvalue())
        self.assertNotIn("removido com sucesso", output.getvalue())

    def test_main_refreshes_models_after_delete_action(self):
        with (
            patch.object(agents.sys, "argv", ["agents.py"]),
            patch.object(
                agents,
                "list_models",
                side_effect=[["old:latest"], []],
            ) as list_models,
            patch.object(
                agents, "choose_menu_action", side_effect=["__delete__", None]
            ),
            patch.object(agents, "delete_agent") as delete,
            patch.object(agents, "chat") as chat,
            redirect_stdout(io.StringIO()),
        ):
            agents.main()

        self.assertEqual(list_models.call_count, 2)
        delete.assert_called_once_with(["old:latest"])
        chat.assert_not_called()


if __name__ == "__main__":
    unittest.main()
