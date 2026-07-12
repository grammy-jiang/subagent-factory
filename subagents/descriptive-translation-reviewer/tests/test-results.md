# Test Results — descriptive-translation-reviewer

**Generated:** 2026-07-12

## Phase 8 Profile Self-Check

**Verdict (v1.8.0):** PASS with one non-blocking WARNING (`body-size`, profile body under the 1000-word FAIL
threshold). Regenerate with `python -m tools.subagent_factory.validate_generated_package subagents/descriptive-translation-reviewer`.

## Behaviour test suites

- `tests/golden-tests.yaml` — 6 golden, 5 negative-routing, 2 missing-context.
- `tests/principle-behaviour-tests.yaml` — one behaviour test per principle (180 total; all 141 high-confidence principles covered).

Every `principle_id` and `principle_coverage` id resolves into `principles/principles.yaml`.
