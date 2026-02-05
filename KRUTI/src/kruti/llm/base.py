from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List

from kruti.agent.types import Action, Message


class LLMClient(ABC):
    @abstractmethod
    def next_action(self, messages: List[Message]) -> Action:
        """Return either a tool action or a final answer."""
        raise NotImplementedError
