# Architecture

KRUTI follows an explicit **agent loop**:

1. User message
2. LLM chooses:
   - Tool(name, args)  OR
   - Final(content)
3. Tool execution yields Observation (tool output)
4. Loop continues until Final or max_steps

Key modules:
- `kruti/agent/loop.py` — orchestration + message history
- `kruti/tools/` — registry + built-in tools
- `kruti/guardrails/` — allowlists, timeouts
- `kruti/rag/` — local indexing + retrieval

Why this shape works:
- tool calls are explicit and auditable
- guardrails are centralized
- evals are runnable in CI
