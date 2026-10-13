"""Conversation-related data structures for the web API."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


@dataclass(slots=True)
class Message:
    """Single message in a chat conversation."""

    role: str
    content: str
    timestamp: datetime = field(default_factory=datetime.utcnow)

    def to_dict(self) -> dict[str, str]:
        return {
            "role": self.role,
            "content": self.content,
            "timestamp": self.timestamp.isoformat(timespec="seconds") + "Z",
        }


@dataclass(slots=True)
class Conversation:
    """Conversation history for a selected agent."""

    agent_name: str
    messages: list[Message] = field(default_factory=list)
    conversation_id: str = "conversation-default"

    def to_dict(self) -> dict[str, object]:
        return {
            "id": self.conversation_id,
            "agentName": self.agent_name,
            "messages": [message.to_dict() for message in self.messages],
        }
