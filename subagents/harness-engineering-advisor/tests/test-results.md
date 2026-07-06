# Test Results — harness-engineering-advisor

**Generated:** 2026-07-06T01:31:39.711028+00:00

## Phase 8 Profile Self-Check

**Verdict:** WARNING

| # | Check | Level | Detail |
|---|-------|-------|--------|
| 1 | slug | PASS | slug 'harness-engineering-advisor' is kebab-case and role-based |
| 2 | when-to-use | PASS | 4 triggers |
| 3 | when-not-to-use | PASS | 3 exclusions |
| 4 | modes-evidence | INFO | mode source-evidence traceability delegated to profile-reviewer |
| 5 | inputs-required | PASS | 1 required input(s) |
| 6 | primary-format | PASS | A structured review or recommendation that, per finding, na… |
| 7 | mode-output | PASS | every mode states its output |
| 8 | minimum-useful-output | PASS | defined |
| 9 | canonical-owner | PASS | The engineering team and its harness owners hold final auth… |
| 10 | may-edit-canonical | PASS | false |
| 11 | quality-bar | PASS | 5 evidence-citing checks |
| 12 | forbidden-behaviours | INFO | 3 rules; source traceability delegated to profile-reviewer |
| 13 | no-procedure-in-body | PASS | no ordered procedure detected in body |
| 14 | body-size | WARNING | profile body ~900 words (> 800); 100 over the 800-word budget; heaviest: quality_bar 156w, modes 122w, when_to_use 118w |
| 15 | platform-neutral | PASS | core is platform-neutral |
| 16 | provenance-ledger | PASS | present |
| 17 | no-unresolved-conflict | INFO | conflict resolution review delegated to profile-reviewer / Phase 7 merge log |
| 18 | golden-tests | PASS | 5 golden, 3 negative routing |

## Routing Tests (structural)

**Records validated:** 10/10

| Test ID | Status | Description |
|---------|--------|-------------|
| GT-001 | SCHEMA-OK | Positive routing — ungated commit on self-rating, broad tools, unbounded context |
| GT-002 | SCHEMA-OK | Positive routing — memory stored as unverified prose |
| GT-003 | SCHEMA-OK | Positive routing — trusting pass@1 and a leaderboard for reliability |
| GT-004 | SCHEMA-OK | Positive routing — trusting the local-agent supply chain by default |
| GT-005 | SCHEMA-OK | Positive routing — multi-agent shared state with no coordination |
| NR-001 | SCHEMA-OK | Negative routing — asked to implement the production harness |
| NR-002 | SCHEMA-OK | Negative routing — asked to attack a system the caller does not own |
| NR-003 | SCHEMA-OK | Negative routing — model training, outside harness scope |
| MC-001 | SCHEMA-OK | Missing context — "review our harness" with no layers or gates described |
| MC-002 | SCHEMA-OK | Missing context — memory-substrate choice with no workload stated |

> Live routing/permission execution requires a Claude invocation; the records above are validated structurally (schema + inventory).
