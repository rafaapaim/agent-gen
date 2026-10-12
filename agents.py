"""Chat no terminal para escolher e conversar com agentes do Ollama.

Uso:
    python agentes.py              # mostra o menu de agentes
    python agentes.py py-dev       # abre direto um agente

Requer o Ollama rodando (http://localhost:11434). Sem dependências externas.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import urllib.error
import urllib.request
from datetime import datetime
from pathlib import Path

OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434").rstrip("/")
SAVE_DIR = Path(__file__).parent / "conversas"

HELP = """Comandos:
  /multi     colar texto com várias linhas (termine com uma linha só com FIM)
  /arquivo   enviar o conteúdo de um arquivo: /arquivo C:\\caminho\\codigo.py
  /agente    trocar de agente
  /limpar    apagar o histórico da conversa atual
  /pensar    mostrar/ocultar o raciocínio <think> do modelo
  /salvar    salvar a conversa em um arquivo .md
  /ajuda     mostrar esta ajuda
  /sair      encerrar
"""


class ThinkFilter:
    """Remove blocos <think>...</think> de um texto recebido em pedaços."""

    OPEN, CLOSE = "<think>", "</think>"

    def __init__(self) -> None:
        self.buf = ""
        self.in_think = False

    def feed(self, text: str) -> str:
        """Recebe um pedaço de texto e devolve o que pode ser exibido."""
        self.buf += text
        out: list[str] = []
        while True:
            tag = self.CLOSE if self.in_think else self.OPEN
            idx = self.buf.find(tag)
            if idx != -1:
                if not self.in_think:
                    out.append(self.buf[:idx])
                self.buf = self.buf[idx + len(tag):]
                self.in_think = not self.in_think
                continue
            # Mantém no buffer um possível início de tag cortado no meio.
            keep = 0
            for n in range(min(len(tag) - 1, len(self.buf)), 0, -1):
                if tag.startswith(self.buf[-n:]):
                    keep = n
                    break
            emit = self.buf[: len(self.buf) - keep]
            if not self.in_think:
                out.append(emit)
            self.buf = self.buf[len(self.buf) - keep:]
            break
        return "".join(out)

    def flush(self) -> str:
        """Devolve o que sobrou no buffer ao final da resposta."""
        rest = "" if self.in_think else self.buf
        self.buf = ""
        return rest


def api_get(path: str) -> dict:
    """Faz um GET na API do Ollama e devolve o JSON."""
    with urllib.request.urlopen(f"{OLLAMA_URL}{path}", timeout=10) as resp:
        return json.load(resp)


def run_ollama_command(args: list[str]) -> subprocess.CompletedProcess[str]:
    """Executa um comando do Ollama sem interpretar argumentos como shell."""
    return subprocess.run(
        args,
        shell=False,
        capture_output=True,
        text=True,
        check=False,
    )


def list_models() -> list[str]:
    """Lista os nomes dos modelos/agentes instalados."""
    try:
        data = api_get("/api/tags")
    except (urllib.error.URLError, TimeoutError, ConnectionError):
        print("Não consegui conectar ao Ollama. Ele está rodando?")
        print("Dica: abra o aplicativo do Ollama ou rode 'ollama serve'.")
        sys.exit(1)
    return sorted(m["name"] for m in data.get("models", []))


def choose_agent(models: list[str]) -> str | None:
    """Mostra um menu e devolve o agente escolhido (ou None para sair)."""
    if not models:
        print("Nenhum modelo instalado. Crie um com 'ollama create'.")
        sys.exit(1)
    print("\nAgentes disponíveis:")
    for i, name in enumerate(models, 1):
        print(f"  {i:>2}. {name}")
    while True:
        try:
            raw = input("\nEscolha o número ou o nome (ou 'sair'): ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return None
        if raw.lower() in {"sair", "q", "/sair"}:
            return None
        if raw.isdigit() and 1 <= int(raw) <= len(models):
            return models[int(raw) - 1]
        matches = [m for m in models if m == raw or m.split(":")[0] == raw]
        if matches:
            return matches[0]
        print("Opção inválida.")


def choose_menu_action(models: list[str]) -> str | None:
    """Mostra agentes e ações de gerenciamento; None encerra o menu."""
    print("\nAgentes disponíveis:")
    if models:
        for i, name in enumerate(models, 1):
            print(f"  {i:>2}. {name}")
    else:
        print("  Nenhum modelo instalado.")
    print("  [c] Criar agente")
    print("  [r] Remover agente")
    print("  [s] Sair")

    while True:
        try:
            raw = input("\nEscolha o número, nome ou ação: ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return None
        action = raw.lower()
        if action in {"s", "sair", "q", "/sair"}:
            return None
        if action in {"c", "criar"}:
            return "__create__"
        if action in {"r", "remover"}:
            return "__delete__"
        if raw.isdigit() and 1 <= int(raw) <= len(models):
            return models[int(raw) - 1]
        matches = [m for m in models if m == raw or m.split(":")[0] == raw]
        if matches:
            return matches[0]
        print("Opção inválida.")


def confirm_action(prompt: str) -> bool:
    """Só confirma ações quando o usuário responde afirmativamente."""
    try:
        answer = input(f"{prompt} (s/N): ").strip().lower()
    except (EOFError, KeyboardInterrupt):
        print("\nOperação cancelada.")
        return False
    return answer in {"s", "sim", "y", "yes"}


def report_command_failure(operation: str, result: subprocess.CompletedProcess[str]) -> None:
    """Exibe o diagnóstico real retornado pelo Ollama."""
    detail = (result.stderr or result.stdout).strip()
    if detail:
        print(f"Falha ao {operation}: {detail}")
    else:
        print(f"Falha ao {operation} (código {result.returncode}).")


def create_agent() -> None:
    """Cria um agente a partir de um Modelfile escolhido pelo usuário."""
    try:
        model_name = input("Nome do novo agente: ").strip()
        if not model_name:
            print("O nome do agente não pode ficar vazio.")
            return

        try:
            current_models = list_models()
        except SystemExit:
            return
        if model_name in current_models:
            print(f"O agente '{model_name}' já existe.")
            return

        modelfile_input = input("Caminho do Modelfile: ").strip().strip('"')
        if not modelfile_input:
            print("O caminho do Modelfile não pode ficar vazio.")
            return
        try:
            modelfile = Path(modelfile_input).expanduser().resolve(strict=True)
            if not modelfile.is_file():
                print(f"Modelfile não é um arquivo: {modelfile}")
                return
            with modelfile.open("rb"):
                pass
        except (OSError, RuntimeError) as exc:
            print(f"Não foi possível ler o Modelfile: {exc}")
            return

        print(f"Agente: {model_name}\nModelfile: {modelfile}")
        if not confirm_action("Criar este agente?"):
            print("Criação cancelada.")
            return
    except (EOFError, KeyboardInterrupt):
        print("\nCriação cancelada.")
        return

    try:
        result = run_ollama_command(
            ["ollama", "create", model_name, "-f", str(modelfile)]
        )
    except OSError as exc:
        print(f"Não foi possível executar o Ollama para criar o agente: {exc}")
        return
    if result.returncode != 0:
        report_command_failure("criar o agente", result)
        return
    print(f"Agente '{model_name}' criado com sucesso.")


def delete_agent(models: list[str]) -> None:
    """Remove um agente instalado somente após confirmação explícita."""
    if not models:
        print("Não há agentes instalados para remover.")
        return
    model_name = choose_agent(models)
    if model_name is None:
        print("Remoção cancelada.")
        return
    if not confirm_action(f"Remover o agente '{model_name}'?"):
        print("Remoção cancelada.")
        return

    try:
        current_models = list_models()
    except SystemExit:
        return
    if model_name not in current_models:
        print(f"O agente '{model_name}' não está mais instalado.")
        return

    try:
        result = run_ollama_command(["ollama", "rm", model_name])
    except OSError as exc:
        print(f"Não foi possível executar o Ollama para remover o agente: {exc}")
        return
    if result.returncode != 0:
        report_command_failure("remover o agente", result)
        return
    print(f"Agente '{model_name}' removido com sucesso.")


def stream_chat(model: str, messages: list[dict], show_think: bool) -> str:
    """Envia o histórico ao Ollama, imprime a resposta em tempo real e a devolve."""
    payload = json.dumps({"model": model, "messages": messages, "stream": True}).encode()
    req = urllib.request.Request(
        f"{OLLAMA_URL}/api/chat",
        data=payload,
        headers={"Content-Type": "application/json"},
    )
    think_filter = ThinkFilter()
    full = ""  # resposta completa, guardada no histórico
    try:
        with urllib.request.urlopen(req, timeout=600) as resp:
            for line in resp:
                if not line.strip():
                    continue
                chunk = json.loads(line)
                if "error" in chunk:
                    print(f"\n[Erro do Ollama] {chunk['error']}")
                    break
                msg = chunk.get("message", {})
                # Alguns modelos devolvem o raciocínio em um campo separado.
                if show_think and msg.get("thinking"):
                    print(msg["thinking"], end="", flush=True)
                text = msg.get("content", "")
                if text:
                    full += text
                    shown = text if show_think else think_filter.feed(text)
                    print(shown, end="", flush=True)
                if chunk.get("done"):
                    break
        if not show_think:
            print(think_filter.flush(), end="", flush=True)
    except urllib.error.HTTPError as exc:
        print(f"\n[Erro HTTP {exc.code}] {exc.read().decode(errors='replace')}")
    except (urllib.error.URLError, TimeoutError, ConnectionError) as exc:
        print(f"\n[Falha de conexão] {exc}")
    except KeyboardInterrupt:
        print("\n[Geração interrompida]")
    print()
    return full


def read_multiline() -> str:
    """Lê várias linhas até o usuário digitar FIM."""
    print("Cole o texto. Digite FIM em uma linha sozinha para enviar.")
    lines: list[str] = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        if line.strip() == "FIM":
            break
        lines.append(line)
    return "\n".join(lines)


def read_file(path_str: str) -> str | None:
    """Lê um arquivo de texto e devolve seu conteúdo formatado para o prompt."""
    path = Path(path_str.strip().strip('"'))
    if not path.is_file():
        print(f"Arquivo não encontrado: {path}")
        return None
    try:
        content = path.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        print(f"Não consegui ler o arquivo: {exc}")
        return None
    return f"Arquivo: {path.name}\n\n{content}"


def save_conversation(model: str, history: list[dict]) -> None:
    """Salva a conversa em um arquivo Markdown na pasta 'conversas'."""
    if not history:
        print("Nada para salvar ainda.")
        return
    SAVE_DIR.mkdir(exist_ok=True)
    stamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    safe = model.replace(":", "-").replace("/", "-")
    path = SAVE_DIR / f"{stamp}_{safe}.md"
    parts = [f"# Conversa com {model}\n"]
    for msg in history:
        who = "Você" if msg["role"] == "user" else model
        parts.append(f"## {who}\n\n{msg['content']}\n")
    path.write_text("\n".join(parts), encoding="utf-8")
    print(f"Conversa salva em: {path}")


def chat(model: str) -> str:
    """Loop de conversa. Devolve 'trocar' para mudar de agente ou 'sair'."""
    history: list[dict] = []
    show_think = False
    print(f"\nAgente: {model}  (digite /ajuda para ver os comandos)\n")
    while True:
        try:
            user = input("Você> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return "sair"
        if not user:
            continue

        cmd, _, arg = user.partition(" ")
        cmd = cmd.lower()
        if cmd == "/sair":
            return "sair"
        if cmd == "/agente":
            return "trocar"
        if cmd == "/ajuda":
            print(HELP)
            continue
        if cmd == "/limpar":
            history.clear()
            print("Histórico apagado.")
            continue
        if cmd == "/pensar":
            show_think = not show_think
            print(f"Raciocínio {'visível' if show_think else 'oculto'}.")
            continue
        if cmd == "/salvar":
            save_conversation(model, history)
            continue
        if cmd == "/multi":
            user = read_multiline()
            if not user.strip():
                continue
        elif cmd == "/arquivo":
            content = read_file(arg)
            if content is None:
                continue
            extra = input("Instrução para este arquivo (Enter para nenhuma)> ").strip()
            user = f"{extra}\n\n{content}" if extra else content

        history.append({"role": "user", "content": user})
        print(f"\n{model}>")
        answer = stream_chat(model, history, show_think)
        if answer:
            history.append({"role": "assistant", "content": answer})
        else:
            history.pop()  # não guarda a pergunta se não houve resposta
        print()


def main() -> None:
    """Ponto de entrada: escolhe o agente e inicia a conversa."""
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    models = list_models()

    model: str | None = None
    if len(sys.argv) > 1:
        wanted = sys.argv[1]
        matches = [m for m in models if m == wanted or m.split(":")[0] == wanted]
        if matches:
            model = matches[0]
        else:
            print(f"Agente '{wanted}' não encontrado.")

    while True:
        if model is None:
            action = choose_menu_action(models)
            if action is None:
                break
            if action == "__create__":
                create_agent()
                try:
                    models = list_models()
                except SystemExit:
                    models = []
                continue
            if action == "__delete__":
                delete_agent(models)
                try:
                    models = list_models()
                except SystemExit:
                    models = []
                continue
            model = action
        action = chat(model)
        if action == "sair":
            break
        model = None
    print("Até mais!")


if __name__ == "__main__":
    main()