# Test Results — agent-skills-advisor

**Generated:** 2026-07-25

## Phase 8 Profile Self-Check

**Verdict:** see `python -m tools.subagent_factory.validate_generated_package subagents/agent-skills-advisor` output.

## Behaviour test suites

- `tests/golden-tests.yaml` — 10 golden, 3 negative-routing, 3 missing-context.
- `tests/principle-behaviour-tests.yaml` — one behaviour test per principle (150 total; all 130 high-confidence principles covered).

Every `principle_id` and `principle_coverage` id resolves into `principles/principles.yaml`.
