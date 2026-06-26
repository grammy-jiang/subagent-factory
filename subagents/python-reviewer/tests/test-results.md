# Test Results — python-reviewer

**Generated:** 2026-06-19T23:55:34.022682+00:00

## Phase 8 Profile Self-Check

**Verdict:** PASS

| # | Check | Level | Detail |
|---|-------|-------|--------|
| 1 | slug | PASS | slug 'python-reviewer' is kebab-case and role-based |
| 2 | when-to-use | PASS | 5 triggers |
| 3 | when-not-to-use | PASS | 4 exclusions |
| 4 | modes-evidence | INFO | mode source-evidence traceability delegated to profile-reviewer |
| 5 | inputs-required | PASS | 1 required input(s) |
| 6 | primary-format | PASS | A structured idiomatic-Python review: the most error-prone o |
| 7 | mode-output | PASS | every mode states its output |
| 8 | minimum-useful-output | PASS | defined |
| 9 | canonical-owner | PASS | The engineer or author who owns the Python code under review |
| 10 | may-edit-canonical | PASS | false |
| 11 | quality-bar | PASS | 5 evidence-citing checks |
| 12 | forbidden-behaviours | INFO | 5 rules; source traceability delegated to profile-reviewer |
| 13 | no-procedure-in-body | PASS | no ordered procedure detected in body |
| 14 | body-size | PASS | ~800 words |
| 15 | platform-neutral | PASS | core is platform-neutral |
| 16 | provenance-ledger | PASS | present |
| 17 | no-unresolved-conflict | INFO | conflict resolution review delegated to profile-reviewer / Phase 7 merge log |
| 18 | golden-tests | PASS | 3 golden, 2 negative routing |

## Routing Tests (structural)

**Records validated:** 6/6

| Test ID | Status | Description |
|---------|--------|-------------|
| G-001 | SCHEMA-OK | Multiple idiomatic defects in one class (mutable default, shallow copy, missing data model) |
| G-002 | SCHEMA-OK | Inheritance versus composition comparison |
| G-003 | SCHEMA-OK | Exception and resource handling review |
| N-001 | SCHEMA-OK | Runtime performance tuning — out of scope |
| N-002 | SCHEMA-OK | Non-Python code — out of scope |
| M-001 | SCHEMA-OK | No code supplied |

> Live routing/permission execution requires a Claude invocation; the records above are validated structurally (schema + inventory).
