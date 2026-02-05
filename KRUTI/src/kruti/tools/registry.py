from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

from kruti.tools.base import Tool
from kruti.tools.builtins.calc import CalcTool
from kruti.tools.builtins.retrieve import RetrieveTool


@dataclass
class ToolRegistry:
    tools: Dict[str, Tool]

    @classmethod
    def default(cls) -> "ToolRegistry":
        builtins = [CalcTool(), RetrieveTool()]
        return cls({t.spec.name: t for t in builtins})

    def get(self, name: str) -> Tool:
        if name not in self.tools:
            raise KeyError(f"Tool '{name}' not found in registry.")
        return self.tools[name]
