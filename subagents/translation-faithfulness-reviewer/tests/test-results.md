# Test Results — translation-faithfulness-reviewer

**Generated:** 2026-07-13

## Phase 8 Profile Self-Check

**Verdict:** see `python -m tools.subagent_factory.validate_generated_package subagents/translation-faithfulness-reviewer` output.

## Behaviour test suites

- `tests/golden-tests.yaml` — 6 golden, 2 negative-routing, 2 missing-context.
- `tests/principle-behaviour-tests.yaml` — one behaviour test per principle (150 total; all 79 high-confidence principles covered).

Every `principle_id` and `principle_coverage` id resolves into `principles/principles.yaml`.
