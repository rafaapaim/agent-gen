"""Agent-related data model for the web API."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Literal


Status = Literal["available", "offline", "error"]


@dataclass(slots=True)
class Agent:
    """Represents an installed Ollama agent or model."""

    name: str
    status: Status = "available"
    source: str = "installed"
    created_at: datetime = field(default_factory=datetime.utcnow)

    def to_dict(self) -> dict[str, object]:
        return {
            "name": self.name,
            "status": self.status,
            "source": self.source,
            "createdAt": self.created_at.isoformat(timespec="seconds") + "Z",
        }
