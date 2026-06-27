# Test Results — postgresql-sqlite-advisor

Generated: 2026-06-22

This package ships:

- `golden-tests.yaml` — 6 golden (positive-routing), 2 negative-routing,
  1 missing-context test, exercising the `advise` / `review` / `compare` / `validate` modes.
- `principle-behaviour-tests.yaml` — 50 behaviour tests, one per promoted principle
  (`P001`–`P050`); every high-confidence principle is referenced by `principle_id`.

The deterministic gates (`profile_self_check`, `validate_principle_test_coverage`,
`validate_skill_authoring`, `validate_faithfulness_report`) pass. Behavioural execution against a
live model is recorded here when run; the routing/grounding oracles above are the acceptance
criteria.
