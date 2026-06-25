export	UV_CACHE_DIR	= .cache/uv
export	PIP_CACHE_DIR	= .cache/pip

VENV	= .venv
CACHE	= .cache
PAC	= ./pac-man.py
ARGS	= $(filter-out $@, $(MAKECMDGOALS))
PDB	= pudb

install:
	@if [ ! -d '$(VENV)' ]; then \
		uv sync; \
	fi

run: install
	@uv run --no-sync python $(PAC) $(ARGS)

debug: install
	@uv run --no-sync python -m $(PDB) $(PAC) $(ARGS)

clean:
	@find . -type d -name __pycache__ -exec rm -rf {} +; \
	find . -type d -name .mypy_cache -exec rm -rf {} +; \
	rm -rf $(VENV); \
	rm -rf $(CACHE); \
	rm -rf data/output/*.json

lint: install
	@uv run flake8 . --exclude=.venv,__pycache__,llm_sdk,.cache; \
	uv run mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict: install
	@uv run flake8 . --exclude=.venv,__pycache__,llm_sdk,.cache;
	@uv run mypy . --strict

re: clean run


.PHONY: install run debug clean lint lint-strict re

%:
	@:
