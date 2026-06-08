PY ?= python

.PHONY: install lint format-check typecheck security audit test verify bootstrap clean

install:  ## Install package with dev, convert, and lint extras
	$(PY) -m pip install -e ".[dev,convert,lint]"

lint:  ## Ruff lint
	ruff check tools tests

format-check:  ## Ruff format check (non-mutating)
	ruff format --check tools tests

typecheck:  ## Mypy (non-blocking on legacy untyped code)
	-mypy tools/subagent_factory

security:  ## Bandit SAST over factory code
	bandit -q -c pyproject.toml -r tools/subagent_factory

secrets:  ## detect-secrets scan of code + config against the baseline
	git ls-files --cached --others --exclude-standard -- 'tools/*.py' 'tools/**/*.py' 'tests/**/*.py' '*.toml' 'Makefile' '.pre-commit-config.yaml' | xargs detect-secrets-hook --baseline .secrets.baseline

audit:  ## pip-audit the installed environment
	pip-audit

test:  ## Run the test suite
	$(PY) -m pytest -q

verify: lint security secrets test  ## Full gate: lint + SAST + secrets + tests (must pass to ship)
	@echo "verify: OK"

bootstrap:  ## Ensure converter dependencies are available
	$(PY) -m tools.subagent_factory.cli bootstrap

clean:
	find . -type d -name __pycache__ -prune -exec rm -rf {} +
	find . -type d -name .pytest_cache -prune -exec rm -rf {} +
