# Test Results — scalability-mr

**Generated:** 2026-06-21T05:03:31.464997+00:00

## Phase 8 Profile Self-Check

**Verdict:** PASS

| # | Check | Level | Detail |
|---|-------|-------|--------|
| 1 | slug | PASS | slug 'scalability-mr' is kebab-case and role-based |
| 2 | when-to-use | PASS | 4 triggers |
| 3 | when-not-to-use | PASS | 3 exclusions |
| 4 | modes-evidence | INFO | mode source-evidence traceability delegated to profile-reviewer |
| 5 | inputs-required | PASS | 1 required input(s) |
| 6 | primary-format | PASS | A structured scalability review or recommendation that names |
| 7 | mode-output | PASS | every mode states its output |
| 8 | minimum-useful-output | PASS | defined |
| 9 | canonical-owner | PASS | The engineering team that owns the system holds final author |
| 10 | may-edit-canonical | PASS | false |
| 11 | quality-bar | PASS | 5 evidence-citing checks |
| 12 | forbidden-behaviours | INFO | 3 rules; source traceability delegated to profile-reviewer |
| 13 | no-procedure-in-body | PASS | no ordered procedure detected in body |
| 14 | body-size | PASS | ~673 words |
| 15 | platform-neutral | PASS | core is platform-neutral |
| 16 | provenance-ledger | PASS | present |
| 17 | no-unresolved-conflict | INFO | conflict resolution review delegated to profile-reviewer / Phase 7 merge log |
| 18 | golden-tests | PASS | 8 golden, 3 negative routing |

## Routing Tests (structural)

**Records validated:** 13/13

| Test ID | Status | Description |
|---------|--------|-------------|
| GT-001 | SCHEMA-OK | Positive routing — scalability advice for P001 |
| GT-002 | SCHEMA-OK | Positive routing — scalability advice for P003 |
| GT-003 | SCHEMA-OK | Positive routing — scalability advice for P009 |
| GT-004 | SCHEMA-OK | Positive routing — scalability advice for P010 |
| GT-005 | SCHEMA-OK | Positive routing — scalability advice for P015 |
| GT-006 | SCHEMA-OK | Positive routing — scalability advice for P021 |
| GT-007 | SCHEMA-OK | Positive routing — scalability advice for P033 |
| GT-008 | SCHEMA-OK | Positive routing — scalability advice for P039 |
| NR-001 | SCHEMA-OK | Negative routing — request for production code is out of scope |
| NR-002 | SCHEMA-OK | Negative routing — product selection is out of scope |
| NR-003 | SCHEMA-OK | Negative routing — UI styling is outside scalability scope |
| MC-001 | SCHEMA-OK | Missing context — no bottleneck or load stated |
| MC-002 | SCHEMA-OK | Missing context — caching advice without access pattern |

> Live routing/permission execution requires a Claude invocation; the records above are validated structurally (schema + inventory).
