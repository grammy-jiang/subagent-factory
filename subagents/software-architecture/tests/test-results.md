# Test Results — software-architecture

**Generated:** 2026-06-19T14:30:04.094049+00:00

## Phase 8 Profile Self-Check

**Verdict:** PASS

| # | Check | Level | Detail |
|---|-------|-------|--------|
| 1 | slug | PASS | slug 'software-architecture' is kebab-case and role-based |
| 2 | when-to-use | PASS | 6 triggers |
| 3 | when-not-to-use | PASS | 3 exclusions |
| 4 | modes-evidence | INFO | mode source-evidence traceability delegated to profile-reviewer |
| 5 | inputs-required | PASS | 1 required input(s) |
| 6 | primary-format | PASS | A structured architecture review or recommendation that name |
| 7 | mode-output | PASS | every mode states its output |
| 8 | minimum-useful-output | PASS | defined |
| 9 | canonical-owner | PASS | The architect or engineering team that owns the system holds |
| 10 | may-edit-canonical | PASS | false |
| 11 | quality-bar | PASS | 5 evidence-citing checks |
| 12 | forbidden-behaviours | INFO | 4 rules; source traceability delegated to profile-reviewer |
| 13 | no-procedure-in-body | PASS | no ordered procedure detected in body |
| 14 | body-size | PASS | ~729 words |
| 15 | platform-neutral | PASS | core is platform-neutral |
| 16 | provenance-ledger | PASS | present |
| 17 | no-unresolved-conflict | INFO | conflict resolution review delegated to profile-reviewer / Phase 7 merge log |
| 18 | golden-tests | PASS | 3 golden, 1 negative routing |

## Routing Tests (structural)

**Records validated:** 5/5

| Test ID | Status | Description |
|---------|--------|-------------|
| GT-001 | SCHEMA-OK | Positive routing — review an existing architecture for structural problems |
| GT-002 | SCHEMA-OK | Positive routing — advise on a structural decision against driving forces |
| GT-003 | SCHEMA-OK | Positive routing — compare two architecture styles |
| NR-001 | SCHEMA-OK | Negative routing — product/vendor selection is out of scope |
| MC-001 | SCHEMA-OK | Missing required input — no architecture or forces stated |

> Live routing/permission execution requires a Claude invocation; the records above are validated structurally (schema + inventory).
