from __future__ import annotations

import os
from typing import Optional

import typer
from rich.console import Console
from rich.prompt import Prompt

from kruti.agent.loop import Agent
from kruti.config import load_config
from kruti.guardrails.runtime import Guardrails
from kruti.llm.rule import RuleLLM
from kruti.tools.registry import ToolRegistry

app = typer.Typer(add_completion=False)
console = Console()


def _build_agent() -> Agent:
    cfg = load_config()
    guard = Guardrails(set(cfg.guardrails.allowed_tools), cfg.guardrails.tool_timeout_seconds)
    tools = ToolRegistry.default()

    # Default: deterministic provider. Swap here for your real provider.
    llm = RuleLLM()

    return Agent(llm=llm, tools=tools, guardrails=guard, system_prompt=cfg.agent.system_prompt)


@app.command()
def run(prompt: str):
    """Run a one-shot prompt."""
    agent = _build_agent()
    out = agent.run(prompt)
    console.print(out)


@app.command()
def chat():
    """Interactive chat."""
    agent = _build_agent()
    console.print("[bold]KRUTI[/bold] ready. Type 'exit' to quit.")
    while True:
        text = Prompt.ask("you")
        if text.strip().lower() in {"exit", "quit"}:
            break
        out = agent.run(text)
        console.print(f"[bold]kruti[/bold]: {out}")


@app.command("rag-demo")
def rag_demo():
    """Demonstrate local retrieval."""
    agent = _build_agent()
    q = "search docs: what are guardrails and why allowlists matter?"
    console.print(f"[italic]prompt:[/italic] {q}")
    out = agent.run(q)
    console.print(out)


if __name__ == "__main__":
    app()
