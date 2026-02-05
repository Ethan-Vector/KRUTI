# KRUTI — Agent Kit for Reliable Tool Use + Lightweight RAG + Evals

KRUTI is a small, production-friendly **agent skeleton** you can clone to ship:
- a **tool-using** agent loop (Action / Observation / Final)
- a minimal **tool registry** + allowlists (guardrails)
- a lightweight **local retrieval** module (RAG without heavy deps)
- a simple **eval harness** (smoke + regression)
- CI, Docker, and clean project hygiene

> The repo is intentionally lean. You can swap the LLM provider, add tools, and expand evals without rewriting the core.

## Quickstart

### 1) Setup
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

### 2) Run the demo CLI
```bash
kruti chat
```

### 3) Run tests + evals
```bash
pytest
python -m kruti.evals.harness
```

## What you get

- `src/kruti/agent/` — agent loop, state, message types
- `src/kruti/tools/` — tool protocol, registry, built-in tools
- `src/kruti/rag/` — tiny document index + retrieval
- `src/kruti/guardrails/` — allowlists + runtime budgets
- `src/kruti/evals/` — dataset + harness + metrics
- `.github/workflows/ci.yml` — ruff + pytest + eval smoke

## Using a real model (optional)

KRUTI ships with a **Mock/Rule LLM** so tests are deterministic.
To use a real provider, implement `LLMClient` (see `src/kruti/llm/base.py`)
and wire it in via config (see `configs/kruti.yaml`).

See: **INSTRUCTIONS.md** for the exact steps.

## License
MIT — see `LICENSE`.
