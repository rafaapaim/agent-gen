# Implementation Plan: Full-Viewport Web Layout

**Branch**: `main` | **Date**: 2026-10-13 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `specs/006-fullscreen-web-layout/spec.md`

## Summary

Fix the browser layout so the existing agent sidebar and chat use the available viewport instead of appearing in a narrow strip. The current page assigns the `app-shell` grid class both to the root `#app` element and to the shell rendered inside it. The root grid therefore constrains its child and causes the observed narrow layout. Keep one application grid shell, ensure it fills the viewport, and retain responsive stacking and usable scrolling for shorter or narrower windows. No agent, chat, API, or persistence behavior changes are in scope.

## Technical Context

**Language/Version**: HTML5, CSS, and browser-native JavaScript modules

**Primary Dependencies**: No frontend framework or package dependencies; browser-native CSS Grid and Flexbox

**Storage**: N/A; this feature changes presentation only

**Testing**: Browser viewport smoke checks at desktop and compact dimensions; existing `pytest` tests cover unrelated CLI behavior and are regression coverage only

**Target Platform**: Modern desktop browsers, with narrow and short viewport support

**Project Type**: Local web application

**Performance Goals**: Layout fills the visible viewport immediately on initial render and after resizing; no additional network requests or runtime dependencies

**Constraints**: Preserve existing visual styling and all agent/chat workflows; occupy the available browser viewport rather than triggering operating-system fullscreen; retain access to controls and scrolling content at compact sizes

**Scale/Scope**: One static browser UI, focused on the app root and its layout styles; no backend, API, or data changes

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

The constitution file contains only unfilled template placeholders and defines no active project principles or gates. This change is limited to the existing front-end layout, introduces no dependencies or persisted data, and preserves all existing workflows. No constitution violations or exceptions are identified.

## Project Structure

### Documentation (this feature)

```text
specs/006-fullscreen-web-layout/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   └── full-viewport-layout.md
└── checklists/
    └── requirements.md
```

### Source Code (repository root)

```text
frontend/
├── public/
│   └── index.html          # Application root element
└── src/
    ├── app.js              # Renders the single application shell
    └── styles/
        └── app.css         # Viewport and responsive layout rules

tests/
└── test_agent_management.py # Existing CLI regression tests
```

**Structure Decision**: Keep the current single-project layout. The change belongs to the static frontend's root markup and stylesheet; it does not require new runtime modules, backend routes, or dependencies.

## Complexity Tracking

No constitution violations require justification. The plan removes an unintended nested layout constraint and keeps the existing frontend architecture.
