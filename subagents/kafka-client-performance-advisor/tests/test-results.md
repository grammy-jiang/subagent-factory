# Test Results — kafka-client-performance-advisor

**Generated:** 2026-06-08T22:38:43.250975+00:00

## Phase 8 Profile Self-Check

**Verdict:** WARNING

| # | Check | Level | Detail |
|---|-------|-------|--------|
| 1 | slug | PASS | slug 'kafka-client-performance-advisor' is kebab-case and role-based |
| 2 | when-to-use | PASS | 5 triggers |
| 3 | when-not-to-use | PASS | 3 exclusions |
| 4 | modes-evidence | INFO | mode source-evidence traceability delegated to profile-reviewer |
| 5 | inputs-required | PASS | 3 required input(s) |
| 6 | primary-format | PASS | Prioritised set of Kafka client configuration parameter reco |
| 7 | mode-output | PASS | every mode states its output |
| 8 | minimum-useful-output | PASS | defined |
| 9 | canonical-owner | PASS | Confluent official documentation for Confluent Platform and  |
| 10 | may-edit-canonical | PASS | false |
| 11 | quality-bar | PASS | 5 evidence-citing checks |
| 12 | forbidden-behaviours | INFO | 4 rules; source traceability delegated to profile-reviewer |
| 13 | no-procedure-in-body | PASS | no ordered procedure detected in body |
| 14 | body-size | WARNING | profile body ~860 words (> 800) |
| 15 | platform-neutral | PASS | core is platform-neutral |
| 16 | provenance-ledger | PASS | present |
| 17 | no-unresolved-conflict | INFO | conflict resolution review delegated to profile-reviewer / Phase 7 merge log |
| 18 | golden-tests | PASS | 3 golden, 1 negative routing |

## Routing Tests (structural)

**Records validated:** 5/5

| Test ID | Status | Description |
|---------|--------|-------------|
| GT-001 | SCHEMA-OK | Positive routing — advise mode for throughput service goal with complete inputs |
| GT-002 | SCHEMA-OK | Positive routing — review mode for consumer configuration against latency goal |
| GT-003 | SCHEMA-OK | Positive routing — validate mode using consumer lag metrics |
| NR-001 | SCHEMA-OK | Negative routing — do not invoke for broker-side infrastructure administration |
| MC-001 | SCHEMA-OK | Missing required input — no service goal stated; must ask before proceeding |

> Live routing/permission execution requires a Claude invocation; the records above are validated structurally (schema + inventory).
