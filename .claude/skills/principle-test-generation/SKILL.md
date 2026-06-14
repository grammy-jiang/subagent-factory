---
name: principle-test-generation
description: "Generate behavioural tests from promoted principles into tests/principle-behaviour-tests.yaml, so every high-confidence principle is exercised by a test that references it (principle_id). Tier 1+."
---

## Purpose

A principle is not useful until it changes behaviour. Generate behavioural tests that prove the
distilled principles actually affect the subagent's output, and make coverage checkable. Output
`tests/principle-behaviour-tests.yaml`, checked by `validate_principle_test_coverage.py`.

## Input

- `principles/principles.yaml` (Step 4) — especially the `confidence: high` principles.
- `profile.yaml` — `when_not_to_use` (for negative routing tests), modes (for patch-safety).

## Procedure

For each **high-confidence** principle, author ≥1 test that **references its `principle_id`**.
Give that test the deterministic `test_id` `PB-<principle_id>` so it matches the principle's
`operational_mapping.test_cases` (see the principle-promotion convention) — this keeps both
`validate_principles` and `validate_principle_test_coverage` green regardless of which file was
authored first:
```yaml
schema_version: principle-behaviour-tests-v1
principle_behaviour_tests:
  - test_id: PB-P001          # PB-<principle_id>, matching operational_mapping.test_cases
    principle_id: P001
    prompt: "<a task that should trigger the principle>"
    expected_behaviour: ["<observable behaviour>", "cites P001"]
    must_not: ["<the failure mode the principle prevents>"]
```

Coverage rule:
- each high-confidence core principle → ≥1 positive routing test;
- each major `when_not_to_use` exclusion → ≥1 negative routing test;
- each patch mode → ≥1 patch-safety test (Step 6).

A test may also live on a `golden-tests.yaml` entry carrying `principle_id` — both count.

## Output

`tests/principle-behaviour-tests.yaml`. Must pass
`python -m tools.subagent_factory.validate_principle_test_coverage` (run on `principles.yaml`):
every high-confidence principle is referenced, and no test cites an unknown principle.

## Caveats

- Coverage proves *linkage* (a test cites the principle), not test *quality*; write tests that
  genuinely exercise the behaviour, and rely on runtime smoke tests for real validation.
