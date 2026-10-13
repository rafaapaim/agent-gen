# Agent Manager

Gerencie agentes locais do Ollama de forma simples, usando uma interface de terminal ou uma UI web local.

## Visão geral

Este projeto permite:

- listar modelos e agentes instalados no Ollama;
- criar novos agentes a partir de um Modelfile;
- remover agentes com confirmação;
- conversar com um agente selecionado;
- usar uma interface web leve para o mesmo fluxo de gestão.

O objetivo é facilitar o uso de modelos locais em um ambiente pessoal ou de desenvolvimento, sem depender de uma plataforma externa.

## O que está incluído

- CLI principal em `agents.py`
- backend em FastAPI em `backend/`
- frontend web em `frontend/`
- testes de verificação em `tests/`

## Requisitos

Antes de executar o projeto, confirme que:

- Python 3.11 ou superior está instalado;
- Ollama está instalado localmente;
- o serviço do Ollama está rodando em `http://localhost:11434`;
- você tem acesso a um terminal e ao navegador local.

Se o Ollama não estiver ativo, a aplicação não conseguirá listar nem conversar com os modelos.

## Estrutura do projeto

```text
agentes/
├── agents.py                 # CLI principal
├── README.md                # documentação do projeto
├── quickstart.md            # guia rápido
├── backend/
│   └── src/
│       ├── main.py          # aplicação FastAPI
│       ├── api/             # rotas HTTP do backend
│       ├── services/        # integração com Ollama
│       └── models/          # modelos de domínio
├── frontend/
│   ├── public/
│   └── src/
├── tests/
│   └── test_agent_management.py
├── conversas/               # gerada em runtime para históricos salvos
└── specs/
```

## Como usar a CLI

Na raiz do projeto, execute:

```bash
python agents.py
```

Você verá um menu com os modelos disponíveis e opções para criar, remover ou conversar.

Também é possível abrir um agente diretamente:

```bash
python agents.py llama3.2
```

### Comandos internos do chat

Dentro do chat, os comandos disponíveis são:

- `/multi` - enviar texto em múltiplas linhas até a linha `FIM`
- `/arquivo` - incluir o conteúdo de um arquivo na conversa
- `/agente` - trocar de agente
- `/limpar` - limpar o histórico da conversa atual
- `/pensar` - mostrar ou ocultar o raciocínio do modelo
- `/salvar` - salvar a conversa em Markdown
- `/ajuda` - exibir a ajuda
- `/sair` - encerrar a sessão

## Como usar a interface web

Antes de iniciar a interface, instale as dependências do backend na raiz do projeto:

```bash
python -m pip install -r backend/requirements.txt
```

Confirme também que o Ollama está instalado e rodando em `http://localhost:11434`. A interface pode carregar sem ele, mas listar agentes e conversar com modelos depende do serviço.

Mantenha os dois servidores abaixo rodando em terminais separados, ambos abertos na raiz do projeto.

### 1) Backend da API — Terminal 1

```bash
python -m uvicorn backend.src.main:app --host 127.0.0.1 --port 8000 --reload
```

A API estará disponível em `http://127.0.0.1:8000/api`. Para verificar a saúde do backend, acesse `http://127.0.0.1:8000/api/health`.

### 2) Frontend — Terminal 2

```bash
python -m http.server 5173 --directory frontend
```

Abra `http://localhost:5173/public/` no navegador. Não abra o arquivo HTML diretamente (`file:`); a interface deve ser servida por HTTP.

Se a porta 8000 estiver ocupada, libere-a antes de iniciar o backend. Caso use outra porta para a API, atualize também a URL base em `frontend/src/api.js`. Se a porta 5173 estiver ocupada, libere-a ou escolha outra porta para o servidor estático e abra a URL correspondente.

Se a interface não conseguir listar agentes, confirme que o backend está ativo e que o Ollama está rodando em `http://localhost:11434`; depois, atualize a página.

A interface web se comunica com o backend em `http://127.0.0.1:8000/api` e permite:

- listar agentes;
- criar um agente a partir de um Modelfile;
- remover um agente;
- enviar mensagens para o modelo selecionado.

## Fluxo de trabalho típico

1. Inicie o Ollama localmente.
2. Verifique os modelos disponíveis com `ollama list`.
3. Abra a CLI ou a interface web.
4. Escolha um agente ou crie um novo a partir de um Modelfile.
5. Inicie a conversa.
6. Salve, limpe ou alterne entre agentes conforme necessário.

## Solução de problemas

### Ollama não está acessível

Verifique se o serviço está rodando:

```bash
ollama serve
```

ou inicie o aplicativo local do Ollama e tente novamente.

### Nenhum modelo está instalado

Execute:

```bash
ollama list
```

Se a lista estiver vazia, instale ou crie um modelo antes de iniciar a conversa.

### Modelfile inválido

Ao criar um agente, confirme que:

- o caminho do arquivo está correto;
- o arquivo existe;
- o arquivo é legível;
- o conteúdo é um Modelfile válido para o Ollama.

### Erro ao conversar ou gerenciar agentes

Confirme que:

- o nome do agente está correto;
- o serviço do Ollama está ativo;
- o modelo está instalado e disponível;
- não há problemas de permissão no sistema de arquivos local.

## Testes

Os testes automatizados cobrem o comportamento principal de gerenciamento de agentes:

```bash
pytest
```

## Observações de manutenção

Este projeto foi pensado para ser simples e local. A parte principal da lógica está concentrada em:

- `agents.py` para terminal;
- `backend/src/services/ollama_service.py` para integração com o Ollama;
- `frontend/src/app.js` para a interface web.

Ao atualizar a aplicação, mantenha a documentação alinhada com a experiência real do usuário, especialmente em relação a:

- criação de agentes;
- remoção de agentes;
- uso de modelos locais;
- integração com Ollama;
- fluxo de chat e comandos interativos.

## Licença

Este repositório ainda não declara uma licença no diretório raiz. Se você pretende compartilhar ou distribuir o projeto publicamente, é recomendável adicionar um arquivo de licença explícito antes da publicação.
