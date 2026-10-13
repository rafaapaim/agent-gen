# Data Model: Full-Viewport Web Layout

## Overview

This feature changes how existing interface regions use available screen space. It introduces no domain data, persisted data, API payloads, or state transitions.

## Layout Entities

### Application Viewport

Represents the visible browser content area available to the application.

| Property | Meaning | Constraint |
|---|---|---|
| Width | Available horizontal space | Application layout spans the available width |
| Height | Available vertical space | Application layout fills at least the visible viewport height |

### Application Shell

The single top-level layout containing the agent management sidebar and chat panel.

| Region | Meaning | Constraint |
|---|---|---|
| Agent sidebar | Agent list and agent-management controls | Remains accessible; can scroll when its content exceeds available height |
| Chat panel | Selected-agent heading, status, conversation, and message form | Uses remaining layout space; conversation can scroll without hiding message entry |

## Relationships

- One application viewport contains one application shell.
- The application shell contains one agent sidebar and one chat panel.
- The chat panel displays the existing selected agent and conversation state; those values are unchanged by this feature.

## Validation Rules

- The shell must not be constrained by a second nested grid using the same application layout.
- At desktop widths, the sidebar and chat panel appear side by side.
- At narrow widths, content rearranges without clipping the primary controls.
- Overflowing agent or message content remains reachable through scrolling.

## State Transitions

No application or domain state transitions are added. Resizing the browser changes only the rendered arrangement of the existing regions.
