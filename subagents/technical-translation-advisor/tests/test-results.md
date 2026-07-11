# Test Results — technical-translation-advisor

**Generated:** 2026-07-11T13:19:25.123226+00:00

## Phase 8 Profile Self-Check

**Verdict:** WARNING

| # | Check | Level | Detail |
|---|-------|-------|--------|
| 1 | slug | PASS | slug 'technical-translation-advisor' is kebab-case and role-based |
| 2 | when-to-use | PASS | 5 triggers |
| 3 | when-not-to-use | PASS | 4 exclusions |
| 4 | modes-evidence | INFO | mode source-evidence traceability delegated to profile-reviewer |
| 5 | inputs-required | PASS | 1 required input(s) |
| 6 | primary-format | PASS | Structured advice that, per point, names the applicable pri… |
| 7 | mode-output | PASS | every mode states its output |
| 8 | minimum-useful-output | PASS | defined |
| 9 | canonical-owner | PASS | The client and commissioner hold final authority over the b… |
| 10 | may-edit-canonical | PASS | false |
| 11 | quality-bar | PASS | 6 evidence-citing checks |
| 12 | forbidden-behaviours | INFO | 5 rules; source traceability delegated to profile-reviewer |
| 13 | no-procedure-in-body | PASS | no ordered procedure detected in body |
| 14 | body-size | WARNING | profile body ~869 words (> 800); 69 over the 800-word budget; heaviest: role 132w, quality_bar 123w, when_to_use 102w |
| 15 | platform-neutral | PASS | core is platform-neutral |
| 16 | provenance-ledger | PASS | present |
| 17 | no-unresolved-conflict | INFO | conflict resolution review delegated to profile-reviewer / Phase 7 merge log |
| 18 | golden-tests | PASS | 6 golden, 3 negative routing |

## Routing Tests (structural)

**Records validated:** 11/11

| Test ID | Status | Description |
|---------|--------|-------------|
| GT-001 | SCHEMA-OK | Positive routing — audience/brief analysis |
| GT-002 | SCHEMA-OK | Positive routing — strategy/procedure choice |
| GT-003 | SCHEMA-OK | Positive routing — terminology/units/mandated naming |
| GT-004 | SCHEMA-OK | Positive routing — usability evaluation design |
| GT-005 | SCHEMA-OK | Positive routing — safety/warning content review |
| GT-006 | SCHEMA-OK | Positive routing — iconic linkage / consistency |
| NR-001 | SCHEMA-OK | Negative — literary translation, no technical dimension |
| NR-002 | SCHEMA-OK | Negative — pure commercial/pricing decision |
| NR-003 | SCHEMA-OK | Negative — CAT/DTP software operation |
| MC-001 | SCHEMA-OK | Missing context — no audience or brief |
| MC-002 | SCHEMA-OK | Missing context — usability claim, no test data |

> Live routing/permission execution requires a Claude invocation; the records above are validated structurally (schema + inventory).
