.PHONY: install lint test evals all

install:
	pip install -e ".[dev]"

lint:
	ruff check .

test:
	pytest

evals:
	python -m kruti.evals.harness

all: lint test evals
