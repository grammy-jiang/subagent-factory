# Test Results — requirements-use-case-advisor

Version: 0.1.0
Date: 2026-06-28

## Suites

- `tests/golden-tests.yaml` — 4 golden (review ×2, advise, validate), 2 negative
  routing, 1 missing-context. Schema `golden-tests-v1`: valid.
- `tests/principle-behaviour-tests.yaml` — 90 behavioural tests, one per principle
  `P001`–`P090`, keyed by `principle_id`.

## Deterministic gates

- Phase 8 profile self-check: PASS (one advisory WARNING on body size, ~885 words;
  under the 1000-word fail threshold).
- Principle → behaviour test coverage: PASS — every high-confidence principle is
  referenced by a behavioural test; no test references an unknown principle.
- Faithfulness report (`reports/faithfulness-report.yaml`): valid — 24 findings over
  the operative profile rules, all `WITHIN_SCOPE` / `EXACT_SUPPORT`, no over-claim.
- Package validation (`validate_generated_package`): PASS.

## Notes

Prompts are paraphrased review scenarios; the three sources are `distillation-only`
and are never quoted verbatim. Behavioural-test grading (LLM replay) is not run as
part of this deterministic record; these suites define the expected behaviour for
that replay.
