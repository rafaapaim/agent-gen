# Documentation Contract: Local Web App Startup

## Required startup sequence

From the repository root:

1. Ensure Ollama is running locally at `http://localhost:11434`.
2. Install backend dependencies with `python -m pip install -r backend/requirements.txt`.
3. In Terminal 1, start the API:

   ```powershell
   python -m uvicorn backend.src.main:app --host 127.0.0.1 --port 8000 --reload
   ```

4. In Terminal 2, serve the static frontend:

   ```powershell
   python -m http.server 5173 --directory frontend
   ```

5. Open `http://localhost:5173/public/` in the browser.

## Expected endpoints

- Frontend: `http://localhost:5173/public/`
- Backend API: `http://127.0.0.1:8000/api`
- Backend health check: `http://127.0.0.1:8000/api/health`
- Ollama: `http://localhost:11434`

## Recovery guidance

- If a port is already occupied, stop the process using the default port before starting the server.
- If the backend port is changed, update the frontend API base address in `frontend/src/api.js` to match.
- If agent loading fails, confirm the backend is running and Ollama is available.
- Do not instruct users to open the HTML file directly with a `file:` URL.

## Documentation consistency

`README.md` and `quickstart.md` must document the same prerequisites, terminal sequence, default ports, frontend URL, and Ollama dependency.
