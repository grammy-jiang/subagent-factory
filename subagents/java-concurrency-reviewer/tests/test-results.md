# Test Results — java-concurrency-reviewer

**Generated:** 2026-06-11T11:18:17.924656+00:00

## Phase 8 Profile Self-Check

**Verdict:** PASS

| # | Check | Level | Detail |
|---|-------|-------|--------|
| 1 | slug | PASS | slug 'java-concurrency-reviewer' is kebab-case and role-based |
| 2 | when-to-use | PASS | 6 triggers |
| 3 | when-not-to-use | PASS | 3 exclusions |
| 4 | modes-evidence | INFO | mode source-evidence traceability delegated to profile-reviewer |
| 5 | inputs-required | PASS | 2 required input(s) |
| 6 | primary-format | PASS | structured critique with named safety and liveness findings, |
| 7 | mode-output | PASS | every mode states its output |
| 8 | minimum-useful-output | PASS | defined |
| 9 | canonical-owner | PASS | developer or tech lead who owns the concurrent code under re |
| 10 | may-edit-canonical | PASS | false |
| 11 | quality-bar | PASS | 5 evidence-citing checks |
| 12 | forbidden-behaviours | INFO | 6 rules; source traceability delegated to profile-reviewer |
| 13 | no-procedure-in-body | PASS | no ordered procedure detected in body |
| 14 | body-size | PASS | ~799 words |
| 15 | platform-neutral | PASS | core is platform-neutral |
| 16 | provenance-ledger | PASS | present |
| 17 | no-unresolved-conflict | INFO | conflict resolution review delegated to profile-reviewer / Phase 7 merge log |
| 18 | golden-tests | PASS | 6 golden, 3 negative routing |

## Routing Tests (structural)

**Records validated:** 10/10

| Test ID | Status | Description |
|---------|--------|-------------|
| GT-001 | SCHEMA-OK | Positive routing — invoke for primary review trigger (synchronized counter suspected of atomicity gap) |
| GT-002 | SCHEMA-OK | Positive routing — invoke for advise mode (pattern selection for producer-consumer pipeline) |
| GT-003 | SCHEMA-OK | Positive routing — invoke for compare mode (two wait/notify designs for a bounded buffer) |
| GT-004 | SCHEMA-OK | Positive routing — invoke for patch-suggest mode (minimal volatile correction on a thread-stop flag) |
| GT-005 | SCHEMA-OK | Positive routing — invoke for Executor/thread-pool configuration review (new trigger from source 2) |
| GT-006 | SCHEMA-OK | Positive routing — invoke for scheduling/priority hazard review (new trigger from source 2) |
| NR-001 | SCHEMA-OK | Negative routing — do not invoke for purely sequential algorithm review with no concurrency constructs |
| NR-002 | SCHEMA-OK | Negative routing — do not invoke for OS or JVM scheduler tuning request |
| NR-003 | SCHEMA-OK | Negative routing — do not invoke for distributed-system architecture design (new exclusion from source 2) |
| MC-001 | SCHEMA-OK | Missing required input — review requested without any code artifact |

> Live routing/permission execution requires a Claude invocation; the records above are validated structurally (schema + inventory).
