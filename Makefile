VENV = .venv

install:
	uv sync

run:
	uv run python $(pac) $(config)

debug:
	uv run python -m pdb $(pac) $(config)

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type d -name .mypy_cache -exec rm -rf {} +
	rm -rf $(VENV)
	rm -rf data/output/*.json

lint:
	uv run flake8 . --exclude=.venv,__pycache__,llm_sdk
	uv run mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	uv run flake8 . --exclude=.venv,__pycache__,llm_sdk
	uv run mypy . --strict

re: clean install run
