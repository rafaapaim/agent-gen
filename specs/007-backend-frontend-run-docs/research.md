# Research: Backend and Frontend Run Documentation

## Decision 1: Document the current backend command and requirements file

- **Decision**: From the repository root, install dependencies with `python -m pip install -r backend/requirements.txt`, then run `python -m uvicorn backend.src.main:app --host 127.0.0.1 --port 8000 --reload` in the backend terminal.
- **Rationale**: `backend/requirements.txt` declares FastAPI and Uvicorn. `backend/src/main.py` defines `backend.src.main:app`, and its direct-run configuration uses host `127.0.0.1` and port `8000`.
- **Alternatives considered**:
  - Install FastAPI and Uvicorn separately: rejected because that duplicates the dependency manifest.
  - Use the module's `__main__` entrypoint: rejected for the primary instructions because the explicit Uvicorn command matches the existing README and makes host, port, and reload options visible.

## Decision 2: Serve the frontend over HTTP from the repository's `frontend` directory

- **Decision**: In a second terminal opened at the repository root, run `python -m http.server 5173 --directory frontend` and open `http://localhost:5173/public/`.
- **Rationale**: Python's standard-library server avoids a new frontend dependency. The static root contains `public/index.html`, and the HTML references `../src/styles/app.css` and `../src/app.js`, which resolve when served from the `frontend` directory. The JavaScript module fetches the backend at `http://127.0.0.1:8000/api`.
- **Alternatives considered**:
  - Open `frontend/public/index.html` directly with a `file:` URL: rejected because a served HTTP origin is the documented, consistent way to load the module application and call the API.
  - Add a Node-based dev server: rejected because there is no package manifest and no dependency on Node is necessary.

## Decision 3: Keep README and quickstart aligned and explain port coupling

- **Decision**: Both guides will show the same prerequisites, two-terminal sequence, default addresses, Ollama requirement, and recovery notes. Explain that if port 8000 is changed, `frontend/src/api.js` must use the corresponding API origin; changing only the server port will not connect the frontend.
- **Rationale**: The API origin is currently hard-coded in the frontend client, while the backend listens on port 8000. Stating this prevents a misleading workaround for an occupied backend port.
- **Alternatives considered**:
  - Suggest an alternate backend port without noting the frontend API origin: rejected because the UI would continue sending requests to port 8000.
  - Omit occupied-port guidance: rejected because it is an explicit documentation requirement and a common startup failure.
