# Step 5 — Principle-to-Behaviour Test Coverage

> Master: `docs/subagent_enhancement_build_plan.md` §8 Step 5. Depth: **full**
> (promoted from medium — Step 4 merged, `principles-v1` frozen).

## Goal
Prove distilled principles change runtime behaviour, not just docs: every high-confidence
principle maps to at least one behavioural test that references it.

## New files
| Path | Kind | Responsibility |
|------|------|----------------|
| `.claude/skills/principle-test-generation/SKILL.md` | skill (LLM) | Generate behavioural tests from principles. |
| `subagents/<slug>/tests/principle-behaviour-tests.yaml` | artifact | The generated tests (one list of cases). |
| `tools/subagent_factory/validate_principle_test_coverage.py` | tool (validator) | Coverage + referential. |
| `tests/subagent_factory/test_validate_principle_test_coverage.py` | fixtures | Validator tests. |

## Artifact shape (schema-exempt, like `golden-tests.yaml`)
```yaml
schema_version: principle-behaviour-tests-v1
principle_behaviour_tests:
  - test_id: PB-001
    principle_id: P-001              # ∈ principles.yaml
    prompt: "Review this module where two teams depend on implicit shared state."
    expected_behaviour: ["identifies hidden coupling risk", "cites P-001"]
    must_not: ["proposes broad rewrite without scope"]
```
Tests files in this repo (e.g. `golden-tests.yaml`) carry no JSON schema; they are validated by
referential checks, not jsonschema. `principle-behaviour-tests.yaml` follows that precedent.

## `validate_principle_test_coverage.py` (coverage + referential)
Reads `principles/principles.yaml` + every `tests/*.yaml`:
- **Coverage:** each principle with `confidence: high` is referenced by ≥1 test (any
  `tests/*.yaml` list-item carrying a matching `principle_id`). Missing → error.
- **Dangling:** every `principle_id` referenced by a test exists in `principles.yaml`.

A test may live in `principle-behaviour-tests.yaml` or carry `principle_id` on a `golden-tests`
entry — both count toward coverage.

## Gate wiring
`_TIER_ARTIFACTS.append(("principles/principles.yaml", 99, validate_principle_test_coverage))`
— **present-gated** (min_tier 99): coverage is checked whenever principles exist; the file's
Tier-1 *requiredness* is already enforced by `validate_principles` (no duplicate "missing").

## LLM ↔ deterministic split
- LLM: `principle-test-generation` skill (authors the test cases + expected behaviour).
- Deterministic: `validate_principle_test_coverage.py` (coverage + dangling refs).

## Coverage rule (skill)
Each high-confidence core principle → ≥1 positive routing test. Each major `when_not_to_use`
exclusion → ≥1 negative routing test. Each patch mode → ≥1 patch-safety test (Step 6).

## Fixtures
- high-confidence principle with a referencing test → `[]`.
- high-confidence principle with no referencing test → coverage error.
- a test referencing an unknown `principle_id` → dangling error.

## Exit criteria + verify
1. Validator passes a covered set; fails uncovered high-confidence principles + dangling refs.
2. `make verify` green; **0/15 packages regressed**.

## Caveats
- Coverage proves *linkage* (a test cites the principle), not that the test is *good*; test
  quality is the skill's job + runtime smoke tests.
