# Quickstart: Full-Viewport Layout Validation

## Prerequisites

- Python 3.11 or newer
- A modern desktop browser
- The project checked out locally
- Ollama is optional for visual layout checks; it is needed only to verify live agent and chat behavior

## Start the frontend

From the repository root, serve the static frontend:

```powershell
python -m http.server 5173 --directory frontend
```

Open `http://localhost:5173/public/` in a browser.

## Validation scenarios

### Desktop viewport

1. Use a desktop-sized browser window, for example 1600 × 900 CSS pixels.
2. Confirm the application shell spans the available page width and at least the viewport height.
3. Confirm the agent sidebar and chat panel are both visible and arranged side by side.
4. Confirm the shell uses at least 95% of the visible page area and no large blank region remains beside it.

### Narrow viewport and resize

1. Resize the window to a narrow width, for example 800 CSS pixels.
2. Confirm the sidebar and chat adapt without clipping the agent controls, chat content, or message entry.
3. Resize the window back to desktop dimensions and confirm the desktop arrangement returns without reloading the page.

### Short viewport and overflowing content

1. Reduce the viewport height, for example to 600 CSS pixels.
2. Confirm the agent list and conversation can scroll when needed.
3. Confirm agent-management controls and chat message entry remain reachable.

## Expected outcome

The existing application fills the browser's content viewport, rearranges at compact dimensions, and preserves agent and chat interactions. The layout behavior contract is documented in [contracts/full-viewport-layout.md](contracts/full-viewport-layout.md).
