# Test Results — analytic-method-reviewer

**Generated:** 2026-07-10T11:34:40.384626+00:00

## Phase 8 Profile Self-Check

**Verdict:** FAIL

| # | Check | Level | Detail |
|---|-------|-------|--------|
| 1 | slug | PASS | slug 'analytic-method-reviewer' is kebab-case and role-based |
| 2 | when-to-use | PASS | 5 triggers |
| 3 | when-not-to-use | PASS | 4 exclusions |
| 4 | modes-evidence | INFO | mode source-evidence traceability delegated to profile-reviewer |
| 5 | inputs-required | PASS | 1 required input(s) |
| 6 | primary-format | PASS | A structured review or recommendation that, per finding, na… |
| 7 | mode-output | PASS | every mode states its output |
| 8 | minimum-useful-output | PASS | defined |
| 9 | canonical-owner | PASS | The analyst and the analytic organization hold final author… |
| 10 | may-edit-canonical | PASS | false |
| 11 | quality-bar | PASS | 5 evidence-citing checks |
| 12 | forbidden-behaviours | INFO | 4 rules; source traceability delegated to profile-reviewer |
| 13 | no-procedure-in-body | PASS | no ordered procedure detected in body |
| 14 | body-size | FAIL | profile body ~1134 words (> 1000); 334 over the 800-word budget; heaviest: quality_bar 203w, when_to_use 158w, modes 140w |
| 15 | platform-neutral | PASS | core is platform-neutral |
| 16 | provenance-ledger | PASS | present |
| 17 | no-unresolved-conflict | INFO | conflict resolution review delegated to profile-reviewer / Phase 7 merge log |
| 18 | golden-tests | PASS | 6 golden, 4 negative routing |

## Routing Tests (structural)

**Records validated:** 13/13

| Test ID | Status | Description |
|---------|--------|-------------|
| GT-001 | SCHEMA-OK | Positive routing — a confident single-outcome estimate with no competing hypothesis |
| GT-002 | SCHEMA-OK | Positive routing — consistent-but-not-diagnostic evidence read as confirmation |
| GT-003 | SCHEMA-OK | Positive routing — advise which structured technique breaks a stuck mind-set |
| GT-004 | SCHEMA-OK | Positive routing — a probability with no reference class and no updating |
| GT-005 | SCHEMA-OK | Positive routing — mirror-imaging in an adversary assessment |
| GT-006 | SCHEMA-OK | Positive routing — compare devil's advocacy with adversarial collaboration |
| NR-001 | SCHEMA-OK | Out of scope — asked to make the substantive judgment |
| NR-002 | SCHEMA-OK | Out of scope — operational HUMINT / interrogation tradecraft |
| NR-003 | SCHEMA-OK | Out of scope — domain substance, not analytic method |
| NR-004 | SCHEMA-OK | Out of scope — unrelated software task |
| MC-001 | SCHEMA-OK | Underspecified — asks whether the analysis is biased with no analysis attached |
| MC-002 | SCHEMA-OK | Underspecified — hypothesis count without uncertainty or stakes |
| MC-003 | SCHEMA-OK | Underspecified — review a forecast with no forecast or evidence provided |

> Live routing/permission execution requires a Claude invocation; the records above are validated structurally (schema + inventory).
