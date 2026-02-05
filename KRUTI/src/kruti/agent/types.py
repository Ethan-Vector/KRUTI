from __future__ import annotations

from typing import Any, Dict, Literal, Optional

from pydantic import BaseModel, Field


class Message(BaseModel):
    role: Literal["system", "user", "assistant", "tool"]
    content: str
    name: Optional[str] = None


class ToolCall(BaseModel):
    name: str
    args: Dict[str, Any] = Field(default_factory=dict)


class Action(BaseModel):
    type: Literal["tool", "final"]
    tool: Optional[ToolCall] = None
    content: Optional[str] = None

    @classmethod
    def tool_action(cls, name: str, args: Dict[str, Any]) -> "Action":
        return cls(type="tool", tool=ToolCall(name=name, args=args))

    @classmethod
    def final(cls, content: str) -> "Action":
        return cls(type="final", content=content)
