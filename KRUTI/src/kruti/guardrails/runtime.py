from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Set


@dataclass(frozen=True)
class Guardrails:
    allowed_tools: Set[str]
    tool_timeout_seconds: int = 10

    def assert_tool_allowed(self, name: str) -> None:
        if name not in self.allowed_tools:
            raise PermissionError(f"Tool '{name}' is not allowed by guardrails.")
