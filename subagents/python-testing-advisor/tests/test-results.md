# Test Results — python-testing-advisor

**Generated:** 2026-07-03T14:54:40.892720+00:00

## Phase 8 Profile Self-Check

**Verdict:** PASS

| # | Check | Level | Detail |
|---|-------|-------|--------|
| 1 | slug | PASS | slug 'python-testing-advisor' is kebab-case and role-based |
| 2 | when-to-use | PASS | 5 triggers |
| 3 | when-not-to-use | PASS | 3 exclusions |
| 4 | modes-evidence | INFO | mode source-evidence traceability delegated to profile-reviewer |
| 5 | inputs-required | PASS | 1 required input(s) |
| 6 | primary-format | PASS | A prioritized set of testing recommendations, each stating t |
| 7 | mode-output | PASS | every mode states its output |
| 8 | minimum-useful-output | PASS | defined |
| 9 | canonical-owner | PASS | Three ingested books govern: pytest usage follows Okken's Py |
| 10 | may-edit-canonical | PASS | false |
| 11 | quality-bar | PASS | 5 evidence-citing checks |
| 12 | forbidden-behaviours | INFO | 5 rules; source traceability delegated to profile-reviewer |
| 13 | no-procedure-in-body | PASS | no ordered procedure detected in body |
| 14 | body-size | PASS | ~630 words |
| 15 | platform-neutral | PASS | core is platform-neutral |
| 16 | provenance-ledger | PASS | present |
| 17 | no-unresolved-conflict | INFO | conflict resolution review delegated to profile-reviewer / Phase 7 merge log |
| 18 | golden-tests | PASS | 3 golden, 1 negative routing |

## Routing Tests (structural)

**Records validated:** 5/5

| Test ID | Status | Description |
|---------|--------|-------------|
| GT-001 | SCHEMA-OK | Positive routing — how to structure fixtures and parametrize a pytest test |
| GT-002 | SCHEMA-OK | Positive routing — outside-in TDD for a new web feature |
| GT-003 | SCHEMA-OK | Positive routing — review an existing suite for isolation and coverage |
| NR-001 | SCHEMA-OK | Negative routing — production infrastructure / secret-management decision |
| MC-001 | SCHEMA-OK | Missing required input — no code or pytest context provided |

> Live routing/permission execution requires a Claude invocation; the records above are validated structurally (schema + inventory).
