# Step 5 — Principle-to-Behaviour Test Coverage

> Master: `docs/subagent_enhancement_build_plan.md` §8 Step 5. Depth: **medium** (outline).
> **Promote to full when:** Step 4 merged + `principles-v1` frozen.

## Goal
Prove that distilled principles actually change runtime behaviour — every high-confidence
principle maps to at least one behavioural test, not just documentation.

## New files (sketch)
- `.claude/skills/principle-test-generation/SKILL.md` — generates cases from principles.
- `subagents/<slug>/tests/principle-behaviour-tests.yaml` — artifact.
- `tools/subagent_factory/validate_principle_test_coverage.py` — coverage validator (no schema; counts/refs).

## Coverage rule
Each high-confidence `principle_id` → ≥1 of:
`positive routing | negative routing | output-contract | forbidden-behaviour | patch-safety` test,
with the test referencing the `principle_id`.

## Reuse
- Existing test harness: `golden-tests.yaml`, `negative_routing_tests`, `run_tests.py`,
  `profile_self_check.py` **#18** (counts golden + negative). Extend #18-style counting to the
  new file, or add a sibling coverage check.

## Dependencies
- **Step 4** (`principles.yaml`) — tests reference `principle_id`.

## Research input
None directly (this is test engineering on top of Steps 2–4). The original-plan §15 coverage
rule applies (master Enh-11): high-confidence core principle ⇒ ≥1 positive test; major
`when_not_to_use` exclusion ⇒ ≥1 negative routing test; patch mode ⇒ ≥1 patch-safety test.

## Validator (at full)
Cross-check: every principle with `confidence: high` has a referencing test; every
`principle_behaviour_tests[].principle_id` ∈ principles.

## Gate wiring
Tier 1+ (present-gated).
