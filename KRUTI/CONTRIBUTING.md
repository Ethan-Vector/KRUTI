# Contributing

## Dev setup
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## Quality gates
```bash
ruff check .
pytest
python -m kruti.evals.harness
```

## Style
- Keep the agent loop deterministic under tests.
- Prefer small, composable tools.
- Add an eval row for every new capability.
