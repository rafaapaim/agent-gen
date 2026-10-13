# Research: Full-Viewport Web Layout

## Decision 1: Use a single application grid shell

- **Decision**: The page should have one element responsible for the `.app-shell` grid. The outer `#app` wrapper should not create a second grid; the shell rendered by the application should own the two-column layout.
- **Rationale**: `frontend/public/index.html` currently gives `#app` the `app-shell` class, and `frontend/src/app.js` renders another `.app-shell` inside it. The stylesheet gives each `.app-shell` a fixed 350px sidebar column and a flexible second column. The nested grid constrains the rendered application and matches the narrow interface shown in the user-provided screenshot.
- **Alternatives considered**:
  - Keep both grids and separately size the outer and inner elements: rejected because it retains unnecessary nesting and makes responsive layout harder to reason about.
  - Add a fixed width to the inner application shell: rejected because it would not use the browser viewport and would reproduce the reported problem.

## Decision 2: Size the application to the browser viewport and preserve responsive flow

- **Decision**: The single application shell should occupy the available viewport width and at least the viewport height. Keep the existing two-column desktop presentation and narrow-screen stacked presentation, adjusting the layout only as needed to prevent clipping.
- **Rationale**: This directly satisfies FR-001 through FR-004 while retaining the current visual hierarchy and interaction patterns. The existing stylesheet already defines a responsive transition at 900px, so the implementation can build on existing behavior rather than add a new responsive system.
- **Alternatives considered**:
  - Use browser/operating-system fullscreen mode: rejected because the request is about page layout within the browser window.
  - Replace the current interface with a different dashboard or navigation model: rejected as unrelated scope.

## Decision 3: Validate with viewport-based browser checks

- **Decision**: Verify the rendered application bounds and access to primary controls in a desktop viewport, a narrow viewport, and a short viewport; verify again after resizing.
- **Rationale**: The defect is visible in the rendered page and is caused by CSS/layout composition. Browser checks directly validate the reported appearance and the responsive acceptance criteria. The repository currently has Python CLI tests but no frontend test harness.
- **Alternatives considered**:
  - Add a browser testing framework: rejected for this narrowly scoped styling fix because it adds dependencies and setup beyond the current project structure.
  - Rely only on Python tests: rejected because those tests do not exercise frontend rendering or viewport layout.
