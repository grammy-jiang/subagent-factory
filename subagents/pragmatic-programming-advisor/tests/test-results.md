# Test Results — pragmatic-programming-advisor

**Generated:** 2026-06-28 (agent_version 0.3.0, post map → reduce rebuild + authored-layer re-ground)

## Suites

| Suite | File | Count |
|-------|------|-------|
| Principle behaviour tests | `tests/principle-behaviour-tests.yaml` | 78 (one per principle P001..P078) |
| Golden / negative / missing-context | `tests/golden-tests.yaml` | 13 golden, 3 negative-routing, 3 missing-context |
| Generated behaviour matrix | `tests/behaviour-tests.yaml` | 82 (golden / negative-routing / missing-context cells) |

Every high-confidence principle (P001, P003, P010, P015, P016, P020, P030, P031, P039, P040,
P041, P059, P068) is referenced by ≥1 behaviour test, so
`validate_principle_test_coverage` reports no coverage gaps.

## Phase 8 Profile Self-Check

**Verdict:** WARNING (one benign body-size warning; no failures)

| # | Check | Level | Detail |
|---|-------|-------|--------|
| 1 | slug | PASS | kebab-case, role-based |
| 2 | when-to-use | PASS | 6 triggers |
| 3 | when-not-to-use | PASS | 3 exclusions |
| 4 | modes-evidence | INFO | delegated to profile-reviewer |
| 5 | inputs-required | PASS | 3 required inputs |
| 6 | primary-format | PASS | structured advisory text |
| 7 | mode-output | PASS | every mode states its output |
| 8 | minimum-useful-output | PASS | defined |
| 9 | canonical-owner | PASS | developer/team owning the artefact |
| 10 | may-edit-canonical | PASS | false |
| 11 | quality-bar | PASS | 5 evidence-citing checks |
| 12 | forbidden-behaviours | INFO | 6 rules; traceability delegated to profile-reviewer |
| 13 | no-procedure-in-body | PASS | no ordered procedure in body |
| 14 | body-size | WARNING | profile body ~979 words (> 800 budget) |
| 15 | platform-neutral | PASS | core platform-neutral |
| 16 | provenance-ledger | PASS | present |
| 17 | no-unresolved-conflict | INFO | delegated to profile-reviewer |
| 18 | golden-tests | PASS | golden + negative-routing suites present |

## Package validation

`python -m tools.subagent_factory.validate_generated_package subagents/pragmatic-programming-advisor`
→ **VALIDATION PASSED** (0 failures).

> Note: behaviour/golden suites define expected routing and minimum outputs; executing them
> against a live model engine (behaviour_replay) is a separate step not run in this rebuild.
