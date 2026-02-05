from __future__ import annotations

import re
from typing import List

from kruti.agent.types import Action, Message
from kruti.llm.base import LLMClient


class RuleLLM(LLMClient):
    """Deterministic 'LLM' used by default.

    Heuristic rules:
    - If user asks to calculate, call tool calc(expression=...)
    - If user asks to search/docs/retrieve, call tool retrieve(query=...)
    Otherwise return a concise final.
    """

    def next_action(self, messages: List[Message]) -> Action:
        user = next((m for m in reversed(messages) if m.role == "user"), None)
        text = (user.content if user else "").strip()

        # calculate: look for math-ish content
        if re.search(r"\b(calc|calculate|compute|math)\b", text, re.I):
            # naive: extract expression inside backticks or after keyword
            expr = None
            m = re.search(r"`([^`]+)`", text)
            if m:
                expr = m.group(1)
            else:
                m2 = re.search(r"(?:calc(?:ulate)?|compute)\s*[:]?\s*(.+)$", text, re.I)
                if m2:
                    expr = m2.group(1)
            expr = expr or "1+1"
            return Action.tool_action("calc", {"expression": expr})

        if re.search(r"\b(retrieve|search|docs|documentation|look up)\b", text, re.I):
            # take the whole message as query, but strip obvious verbs
            q = re.sub(r"\b(retrieve|search|docs|documentation|look up)\b[:]?\s*", "", text, flags=re.I).strip()
            q = q or text
            return Action.tool_action("retrieve", {"query": q})

        return Action.final(
            "I can help. If you want me to use tools, ask to **calculate** or **search docs**."
        )
