# Prefer the project-managed venv interpreter when present (created by
# `cli bootstrap --venv` / `uv venv .venv`), so `make verify` runs the pinned
# dev+lint toolchain (mypy, ruff, bandit, types-PyYAML, slugify) regardless of
# what `python` resolves to on PATH. Override with `make PY=... <target>`.
PY ?= $(shell test -x "$(CURDIR)/.venv/bin/python" && "$(CURDIR)/.venv/bin/python" -c 'import ruff,mypy,bandit,yaml,slugify' >/dev/null 2>&1 && echo "$(CURDIR)/.venv/bin/python" || echo python)

.PHONY: install lint format-check typecheck security secrets audit test verify toolcheck bootstrap clean

install:  ## Install package with dev, convert, and lint extras
	$(PY) -m pip install -e ".[dev,convert,lint]"

lint:  ## Ruff lint
	$(PY) -m ruff check tools tests

format-check:  ## Ruff format check (non-mutating)
	$(PY) -m ruff format --check tools tests

typecheck:  ## Mypy static type check (gating)
	$(PY) -m mypy tools/subagent_factory

security:  ## Bandit SAST over factory code
	$(PY) -m bandit -q -c pyproject.toml -r tools/subagent_factory

secrets:  ## detect-secrets scan of code + config against the baseline
	git ls-files --cached --others --exclude-standard -- 'tools/*.py' 'tools/**/*.py' 'tests/**/*.py' '*.toml' 'Makefile' '.pre-commit-config.yaml' | xargs detect-secrets-hook --baseline .secrets.baseline

audit:  ## pip-audit the installed environment
	pip-audit

test:  ## Run the test suite
	$(PY) -m pytest -q

toolcheck:  ## Fail fast (with a fix hint) if the lint/type toolchain is missing from $(PY)
	@$(PY) -c "import mypy, ruff, bandit, yaml, slugify" 2>/dev/null || { \
	  echo "ERROR: lint/type toolchain missing from interpreter: $(PY)"; \
	  echo "  The .venv was likely created by 'bootstrap --venv' (convert extras only)."; \
	  echo "  Install the dev+lint toolchain into it:  make install"; \
	  exit 1; }

verify: toolcheck lint format-check typecheck security secrets test  ## Full gate: lint + format + types + SAST + secrets + tests (must pass to ship)
	@echo "verify: OK"

bootstrap:  ## Ensure converter dependencies are available
	$(PY) -m tools.subagent_factory.cli bootstrap

clean:
	find . -type d -name __pycache__ -prune -exec rm -rf {} +
	find . -type d -name .pytest_cache -prune -exec rm -rf {} +
