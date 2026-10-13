# Quickstart: Validate Web App Startup Documentation

## Prerequisites

- Python 3.11 or newer installed and available as `python`
- Ollama installed and running locally at `http://localhost:11434`
- A terminal opened at the repository root
- A browser available on the same machine

## Setup

Install the backend packages:

```powershell
python -m pip install -r backend/requirements.txt
```

## Start the application

Keep each server running in its own terminal. Run both commands from the repository root.

### Terminal 1: Backend API

```powershell
python -m uvicorn backend.src.main:app --host 127.0.0.1 --port 8000 --reload
```

The API is available at `http://127.0.0.1:8000/api`. Verify backend health at `http://127.0.0.1:8000/api/health`.

### Terminal 2: Frontend

```powershell
python -m http.server 5173 --directory frontend
```

Open `http://localhost:5173/public/` in the browser. Serve the frontend over HTTP; do not open `frontend/public/index.html` directly from the filesystem.

## Validation scenarios

1. Confirm the health endpoint returns a response indicating whether Ollama is available.
2. Open the frontend URL and confirm the page loads.
3. With Ollama running and at least one model installed, confirm the UI lists agents.
4. With no models installed, confirm the UI shows the empty-agent guidance rather than a page-load failure.

## Troubleshooting

- **Backend port 8000 is busy**: stop the process using that port. If you choose another port, update the backend base URL in `frontend/src/api.js` to use the same port before opening the UI.
- **Frontend port 5173 is busy**: stop the process using the port, or select another static-server port and open the matching URL.
- **Ollama is unavailable**: start the Ollama desktop application or run `ollama serve`, then refresh the UI.
- **Module or dependency error**: run the dependency installation command above from the repository root and verify Python is installed.

## Expected outcome

The web page loads from the local frontend server, the API responds on port 8000, and agent listing/chat can use the local Ollama service. These commands and addresses must remain aligned with `README.md` and the startup contract in [contracts/web-app-startup.md](contracts/web-app-startup.md).
