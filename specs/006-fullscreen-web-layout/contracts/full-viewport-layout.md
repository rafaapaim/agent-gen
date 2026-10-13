# UI Contract: Full-Viewport Layout

## Scope

This contract specifies the visible layout behavior of the existing local web application. It does not change frontend/backend endpoints, agent data, chat payloads, or user workflows.

## Viewport behavior

- The application shell spans the available browser content width and at least its height.
- At desktop widths, the agent sidebar and chat panel are presented side by side.
- At narrow widths, the regions stack or otherwise adapt so neither is clipped or inaccessible.
- Resizing the browser updates the layout without requiring a page reload.
- The agent list and conversation remain scrollable when their contents exceed the available space.
- Chat message entry and agent-management controls remain reachable at short viewport heights.

## Content and workflow compatibility

- Existing agent names, status, selected-agent state, errors, conversation messages, and forms remain unchanged.
- Users retain the existing ability to refresh, create, and delete agents and to send chat messages.
- When measured at the desktop viewport used for validation, the application shell occupies at least 95% of the visible page area.

## Verification

Validate the rendered layout at desktop, narrow, and short viewport sizes. Confirm the shell bounds, responsive region arrangement, access to primary controls, and continued scrolling of long content. See [quickstart.md](../quickstart.md) for runnable setup and checks.
