# Adding Tools (Step-by-step)

## 1) Create a tool
Create `src/kruti/tools/builtins/my_tool.py`:

- define `spec = ToolSpec(...)`
- implement `run(args, timeout_seconds) -> str`

## 2) Register it
Add the tool in `ToolRegistry.default()`.

## 3) Allowlist it
Add tool name to `configs/kruti.yaml -> guardrails.allowed_tools`.

## 4) Add an eval
Add a row to `evals/datasets/smoke.jsonl`.
