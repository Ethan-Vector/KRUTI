# KRUTI — Setup + Extension Guide

This file is your “do this, then that” checklist.

## 1) Install

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## 2) Run the CLI

Interactive chat:
```bash
kruti chat
```

One-shot:
```bash
kruti run "calculate 19 * 7 then explain"
```

RAG demo (indexes local docs then answers):
```bash
kruti rag-demo
```

## 3) Configure

Copy env template:
```bash
cp .env.example .env
```

Main config lives in:
- `configs/kruti.yaml`

KRUTI’s core is provider-agnostic. The default provider is a deterministic **RuleLLM**.

### 3.1 Add your model provider
Implement `LLMClient` in `src/kruti/llm/`.

You’ll need to return one of:
- `Action(type="tool", name="...", args={...})`
- `Action(type="final", content="...")`

That’s it — the loop and tools stay unchanged.

## 4) Add a tool

1. Create a tool file in `src/kruti/tools/builtins/`
2. Implement `ToolSpec` + `run()`
3. Register it in `src/kruti/tools/registry.py`

Then add it to the allowlist in `configs/kruti.yaml`.

## 5) Add an eval

Add a row in:
- `evals/datasets/smoke.jsonl`

Run:
```bash
python -m kruti.evals.harness
```

## Common gotchas

- If the agent keeps looping: lower `max_steps` in config or tighten your prompt format.
- If a tool isn’t called: verify it’s in the registry and in the allowlist.
- If you add network tools: keep them gated behind allowlists + timeouts.
