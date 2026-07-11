# Test Results — kafka-benchmarking-advisor

**Generated:** 2026-06-08T22:44:46.531083+00:00

## Phase 8 Profile Self-Check

**Verdict:** WARNING

| # | Check | Level | Detail |
|---|-------|-------|--------|
| 1 | slug | PASS | slug 'kafka-benchmarking-advisor' is kebab-case and role-based |
| 2 | when-to-use | PASS | 5 triggers |
| 3 | when-not-to-use | PASS | 3 exclusions |
| 4 | modes-evidence | INFO | mode source-evidence traceability delegated to profile-reviewer |
| 5 | inputs-required | PASS | 5 required input(s) |
| 6 | primary-format | PASS | Structured advisory report mapping the caller's scenario to  |
| 7 | mode-output | PASS | every mode states its output |
| 8 | minimum-useful-output | PASS | defined |
| 9 | canonical-owner | PASS | Infrastructure or platform engineer responsible for the Kafk |
| 10 | may-edit-canonical | PASS | false |
| 11 | quality-bar | PASS | 5 evidence-citing checks |
| 12 | forbidden-behaviours | INFO | 4 rules; source traceability delegated to profile-reviewer |
| 13 | no-procedure-in-body | PASS | no ordered procedure detected in body |
| 14 | body-size | WARNING | profile body ~911 words (> 800) |
| 15 | platform-neutral | PASS | core is platform-neutral |
| 16 | provenance-ledger | PASS | present |
| 17 | no-unresolved-conflict | INFO | conflict resolution review delegated to profile-reviewer / Phase 7 merge log |
| 18 | golden-tests | PASS | 4 golden, 2 negative routing |

## Routing Tests (structural)

**Records validated:** 7/7

| Test ID | Status | Description |
|---------|--------|-------------|
| GT-001 | SCHEMA-OK | Positive routing — advise mode: JDK upgrade recommendation for TLS cluster |
| GT-002 | SCHEMA-OK | Positive routing — compare mode: gzip vs. Zstd compression algorithms |
| GT-003 | SCHEMA-OK | Positive routing — validate mode: benchmark methodology review |
| GT-004 | SCHEMA-OK | Positive routing — advise mode: Intel ISA-L vs IPP gzip replacement |
| NR-001 | SCHEMA-OK | Negative routing — encryption-at-rest design: explicitly out of scope per source |
| NR-002 | SCHEMA-OK | Negative routing — non-Intel hardware: AMD EPYC instance family |
| MC-001 | SCHEMA-OK | Missing required input — no instance type or KPI provided |

> Live routing/permission execution requires a Claude invocation; the records above are validated structurally (schema + inventory).
