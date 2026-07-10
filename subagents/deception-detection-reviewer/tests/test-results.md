# Test Results — deception-detection-reviewer

**Generated:** 2026-07-11

## Phase 8 Profile Self-Check

**Verdict:** see `python -m tools.subagent_factory.validate_generated_package` output.

| # | Check | Level | Detail |
|---|-------|-------|--------|
| 1 | slug | PASS | slug 'deception-detection-reviewer' is kebab-case and role-based |
| 2 | when-to-use | PASS | 5 triggers |
| 3 | when-not-to-use | PASS | 4 exclusions |
| 4 | modes-evidence | INFO | mode source-evidence traceability delegated to profile-reviewer |
| 5 | inputs-required | PASS | 1 required input |
| 6 | primary-format | PASS | per-finding structured review format defined |
| 7 | mode-output | PASS | every mode states its output |
| 8 | minimum-useful-output | PASS | defined |
| 9 | canonical-owner | PASS | operation owner + commander hold authority |
| 10 | may-edit-canonical | PASS | false |
| 11 | quality-bar | PASS | 5 evidence-citing checks |
| 12 | forbidden-behaviours | INFO | 4 rules; source traceability delegated to profile-reviewer |
| 13 | no-procedure-in-body | PASS | no ordered procedure detected in body |
| 14 | body-size | INFO | profile body within/near budget |
| 15 | platform-neutral | PASS | core is platform-neutral |
| 16 | provenance-ledger | PASS | present |
| 17 | no-unresolved-conflict | INFO | conflict resolution delegated to profile-reviewer |
| 18 | golden-tests | PASS | 5 golden, 2 negative routing, 2 missing-context |

## Routing Tests (structural)

**Records validated:** 9/9

| Test ID | Status | Description |
|---------|--------|-------------|
| GT-001 | SCHEMA-OK | Positive routing — decisive deception on one channel, announced baldly |
| GT-002 | SCHEMA-OK | Positive routing — claim that a walk-in is controlled, no evidence |
| GT-003 | SCHEMA-OK | Positive routing — premature confidence relaxing vigilance on a turned agent |
| GT-004 | SCHEMA-OK | Positive routing — no single approval gate on outgoing traffic |
| GT-005 | SCHEMA-OK | Positive routing — compare running one channel vs several for a coup |
| NR-001 | SCHEMA-OK | Negative routing — routine logistics, no deception dimension |
| NR-002 | SCHEMA-OK | Negative routing — request to plan real-world harm against a named target |
| MC-001 | SCHEMA-OK | Missing context — 'is our agent really controlled?' with nothing supplied |
| MC-002 | SCHEMA-OK | Missing context — 'will the enemy believe this feed?' with no feed shown |

> Live routing/permission execution requires a Claude invocation; the records above are validated structurally (schema + inventory).
