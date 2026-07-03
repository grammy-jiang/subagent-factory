# Python Testing Advisor

A generated specialist subagent that advises Python developers on designing,
writing, running, and organizing automated tests with **pytest**, and on building
features **test-first** (outside-in TDD).

- **Canonical source of truth:** `profile.yaml` (portable-profile-v1).
- **Sources:** *Python Testing with pytest* (Okken) and *Test-Driven Development
  with Python* (Percival) — both distillation-only (no verbatim quotation).
- **Tier:** 2 (full evidence chain: claims → evidence → principles).

## What it does

- **advise** — ranked, principle-cited recommendations on pytest usage
  (fixtures, parametrization, markers, selection, config, coverage, plugins).
- **review** — critique of an existing pytest suite (isolation, fixtures, coverage).
- **tdd-guide** — the next expected-failing test and the smallest change to pass it.

It is read-only: it recommends changes, it does not edit the caller's code.

## What it does not do

Write production/feature code, make product-design decisions, design production
infrastructure or secret-management, or advise on non-Python / non-pytest stacks.

## Layout

```
profile.yaml                     canonical profile
provenance-ledger.md             field-by-field distillation log
skills/                          pytest-test-authoring, tdd-workflow
references/                      pytest-cli-and-config, pytest-plugin-catalog
tests/                           golden-tests + principle-behaviour-tests
reports/faithfulness-report.yaml per-rule faithfulness grading
analysis|evidence|principles/    distilled evidence chain (do not hand-edit)
adapters/claude-code/            exported runtime adapter
```

## Validate

```bash
python -m tools.subagent_factory.validate_generated_package subagents/python-testing-advisor
```
