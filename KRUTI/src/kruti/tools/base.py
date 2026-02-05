from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass(frozen=True)
class ToolSpec:
    name: str
    description: str
    args_schema: Dict[str, Any]


class Tool(ABC):
    spec: ToolSpec

    @abstractmethod
    def run(self, args: Dict[str, Any], timeout_seconds: int = 10) -> str:
        raise NotImplementedError
