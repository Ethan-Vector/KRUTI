from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List, Tuple

from kruti.agent.loop import Agent
from kruti.config import load_config
from kruti.guardrails.runtime import Guardrails
from kruti.llm.rule import RuleLLM
from kruti.tools.registry import ToolRegistry


def _load_jsonl(path: str) -> List[Dict]:
    rows = []
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        rows.append(json.loads(line))
    return rows


def run_smoke() -> Tuple[int, int, List[str]]:
    cfg = load_config()
    guard = Guardrails(set(cfg.guardrails.allowed_tools), cfg.guardrails.tool_timeout_seconds)
    tools = ToolRegistry.default()
    llm = RuleLLM()
    agent = Agent(llm=llm, tools=tools, guardrails=guard, system_prompt=cfg.agent.system_prompt)

    dataset = _load_jsonl("evals/datasets/smoke.jsonl")
    passed = 0
    failed = 0
    failures: List[str] = []

    for row in dataset:
        prompt = row["input"]
        must_contain = row.get("must_contain", [])
        out = agent.run(prompt, max_steps=cfg.agent.max_steps)

        ok = True
        for s in must_contain:
            if s.lower() not in (out or "").lower():
                ok = False
                break

        if ok:
            passed += 1
        else:
            failed += 1
            failures.append(f"FAIL: {row.get('id','?')} -> output='{out}'")

    return passed, failed, failures


def main() -> None:
    passed, failed, failures = run_smoke()
    print(f"KRUTI evals: passed={passed} failed={failed}")
    if failures:
        for f in failures:
            print(f)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
