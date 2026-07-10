# Test Results — calibration-forecasting-reviewer

**Generated:** 2026-07-10T11:38:59.229964+00:00

## Phase 8 Profile Self-Check

**Verdict:** WARNING

| # | Check | Level | Detail |
|---|-------|-------|--------|
| 1 | slug | PASS | slug 'calibration-forecasting-reviewer' is kebab-case and role-based |
| 2 | when-to-use | PASS | 5 triggers |
| 3 | when-not-to-use | PASS | 3 exclusions |
| 4 | modes-evidence | INFO | mode source-evidence traceability delegated to profile-reviewer |
| 5 | inputs-required | PASS | 1 required input(s) |
| 6 | primary-format | PASS | A structured review that, per finding, names the calibratio… |
| 7 | mode-output | PASS | every mode states its output |
| 8 | minimum-useful-output | PASS | defined |
| 9 | canonical-owner | PASS | The forecaster and the decision-maker hold final authority… |
| 10 | may-edit-canonical | PASS | false |
| 11 | quality-bar | PASS | 5 evidence-citing checks |
| 12 | forbidden-behaviours | INFO | 4 rules; source traceability delegated to profile-reviewer |
| 13 | no-procedure-in-body | PASS | no ordered procedure detected in body |
| 14 | body-size | WARNING | profile body ~998 words (> 800); 198 over the 800-word budget; heaviest: quality_bar 183w, forbidden_behaviours 131w, when_to_use 121w |
| 15 | platform-neutral | PASS | core is platform-neutral |
| 16 | provenance-ledger | PASS | present |
| 17 | no-unresolved-conflict | INFO | conflict resolution review delegated to profile-reviewer / Phase 7 merge log |
| 18 | golden-tests | PASS | 5 golden, 2 negative routing |

## Routing Tests (structural)

**Records validated:** 9/9

| Test ID | Status | Description |
|---------|--------|-------------|
| GT-001 | SCHEMA-OK | Positive routing — overconfident single-outcome forecast built from a vivid story |
| GT-002 | SCHEMA-OK | Positive routing — scoring a forecaster without a baseline |
| GT-003 | SCHEMA-OK | Positive routing — inside-view estimate ignoring the reference class |
| GT-004 | SCHEMA-OK | Positive routing — designing a forecasting process / tournament |
| GT-005 | SCHEMA-OK | Positive routing — compare ways to express an uncertain estimate |
| NR-001 | SCHEMA-OK | Negative routing — database performance, not judgment under uncertainty |
| NR-002 | SCHEMA-OK | Negative routing — asking for production code to be written |
| MC-001 | SCHEMA-OK | Missing context — "is our forecast calibrated?" with nothing supplied |
| MC-002 | SCHEMA-OK | Missing context — "should we trust this estimate?" with no reasoning or reference class |

> Live routing/permission execution requires a Claude invocation; the records above are validated structurally (schema + inventory).
