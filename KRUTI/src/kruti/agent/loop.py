from __future__ import annotations

from typing import List, Optional

from kruti.agent.types import Action, Message
from kruti.guardrails.runtime import Guardrails
from kruti.llm.base import LLMClient
from kruti.observability.trace import log_event, start_span
from kruti.tools.registry import ToolRegistry


class Agent:
    def __init__(self, llm: LLMClient, tools: ToolRegistry, guardrails: Guardrails, system_prompt: str):
        self.llm = llm
        self.tools = tools
        self.guardrails = guardrails
        self.messages: List[Message] = [Message(role="system", content=system_prompt)]

    def run(self, user_input: str, max_steps: int = 6) -> str:
        self.messages.append(Message(role="user", content=user_input))
        for step in range(1, max_steps + 1):
            span = start_span("llm.next_action", step=step)
            action: Action = self.llm.next_action(self.messages)
            log_event("span_end", **span.end(type=action.type))

            if action.type == "final":
                out = action.content or ""
                self.messages.append(Message(role="assistant", content=out))
                return out

            if action.type == "tool":
                if not action.tool:
                    raise ValueError("Tool action without tool payload.")
                tool_name = action.tool.name
                self.guardrails.assert_tool_allowed(tool_name)

                tool = self.tools.get(tool_name)
                tool_span = start_span("tool.run", tool=tool_name)
                result = tool.run(action.tool.args, timeout_seconds=self.guardrails.tool_timeout_seconds)
                log_event("span_end", **tool_span.end(ok=True))

                self.messages.append(Message(role="tool", name=tool_name, content=result))

                # after tool, let LLM decide final (or more tools)
                continue

        return "KRUTI stopped: max_steps reached. Tighten the task or raise max_steps."
