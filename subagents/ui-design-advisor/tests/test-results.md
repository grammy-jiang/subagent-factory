# Test Results — ui-design-advisor

**Generated:** 2026-07-03T08:46:29.608804+00:00

## Phase 8 Profile Self-Check

**Verdict:** PASS

| # | Check | Level | Detail |
|---|-------|-------|--------|
| 1 | slug | PASS | slug 'ui-design-advisor' is kebab-case and role-based |
| 2 | when-to-use | PASS | 5 triggers |
| 3 | when-not-to-use | PASS | 3 exclusions |
| 4 | modes-evidence | INFO | mode source-evidence traceability delegated to profile-reviewer |
| 5 | inputs-required | PASS | 1 required input(s) |
| 6 | primary-format | PASS | A structured UI critique or recommendation that names the us |
| 7 | mode-output | PASS | every mode states its output |
| 8 | minimum-useful-output | PASS | defined |
| 9 | canonical-owner | PASS | The product team, its designers, and engineers hold final au |
| 10 | may-edit-canonical | PASS | false |
| 11 | quality-bar | PASS | 5 evidence-citing checks |
| 12 | forbidden-behaviours | INFO | 3 rules; source traceability delegated to profile-reviewer |
| 13 | no-procedure-in-body | PASS | no ordered procedure detected in body |
| 14 | body-size | PASS | ~797 words |
| 15 | platform-neutral | PASS | core is platform-neutral |
| 16 | provenance-ledger | PASS | present |
| 17 | no-unresolved-conflict | INFO | conflict resolution review delegated to profile-reviewer / Phase 7 merge log |
| 18 | golden-tests | PASS | 6 golden, 2 negative routing |

## Routing Tests (structural)

**Records validated:** 10/10

| Test ID | Status | Description |
|---------|--------|-------------|
| GT-001 | SCHEMA-OK | Positive routing — establish visual hierarchy on a flat screen |
| GT-002 | SCHEMA-OK | Positive routing — reduce form effort and validation friction |
| GT-003 | SCHEMA-OK | Positive routing — cut excise and add feedback in an interaction |
| GT-004 | SCHEMA-OK | Positive routing — choose typography and color to communicate |
| GT-005 | SCHEMA-OK | Positive routing — fit posture, platform, and mobile context |
| GT-006 | SCHEMA-OK | Positive routing — ground a decision in the user goal and persona |
| NR-001 | SCHEMA-OK | Out of scope — production code and tooling selection |
| NR-002 | SCHEMA-OK | Out of scope — backend and brand strategy |
| MC-001 | SCHEMA-OK | Underspecified — no user, goal, platform, or context given |
| MC-002 | SCHEMA-OK | Underspecified — a form to fix but no purpose or audience |

> Live routing/permission execution requires a Claude invocation; the records above are validated structurally (schema + inventory).
