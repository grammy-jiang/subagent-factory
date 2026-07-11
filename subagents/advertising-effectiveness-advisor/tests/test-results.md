# Test Results — advertising-effectiveness-advisor

**Generated:** 2026-06-09T10:53:19.599574+00:00

## Phase 8 Profile Self-Check

**Verdict:** PASS

| # | Check | Level | Detail |
|---|-------|-------|--------|
| 1 | slug | PASS | slug 'advertising-effectiveness-advisor' is kebab-case and role-based |
| 2 | when-to-use | PASS | 4 triggers |
| 3 | when-not-to-use | PASS | 3 exclusions |
| 4 | modes-evidence | INFO | mode source-evidence traceability delegated to profile-reviewer |
| 5 | inputs-required | PASS | 1 required input(s) |
| 6 | primary-format | PASS | Written critique-and-recommendation — prose with structured  |
| 7 | mode-output | PASS | every mode states its output |
| 8 | minimum-useful-output | PASS | defined |
| 9 | canonical-owner | PASS | The company's marketing decision-maker (CMO, brand owner, or |
| 10 | may-edit-canonical | PASS | false |
| 11 | quality-bar | PASS | 4 evidence-citing checks |
| 12 | forbidden-behaviours | INFO | 4 rules; source traceability delegated to profile-reviewer |
| 13 | no-procedure-in-body | PASS | no ordered procedure detected in body |
| 14 | body-size | PASS | ~798 words |
| 15 | platform-neutral | PASS | core is platform-neutral |
| 16 | provenance-ledger | PASS | present |
| 17 | no-unresolved-conflict | INFO | conflict resolution review delegated to profile-reviewer / Phase 7 merge log |
| 18 | golden-tests | PASS | 3 golden, 1 negative routing |

## Routing Tests (structural)

**Records validated:** 5/5

| Test ID | Status | Description |
|---------|--------|-------------|
| GT-001 | SCHEMA-OK | Positive routing — advise mode; caller about to commit spend and needs it justified by selling return rather than awareness |
| GT-002 | SCHEMA-OK | Positive routing — compare mode; bounded either/or sponsorship-vs-endorser decision |
| GT-003 | SCHEMA-OK | Positive routing — validate mode; gate a completed campaign against a selling criterion |
| NR-001 | SCHEMA-OK | Negative routing — request to produce finished creative; outside scope per Q4 |
| MC-001 | SCHEMA-OK | Missing required input — no selling situation, customer, or goal provided; advisor must request it before engaging |

> Live routing/permission execution requires a Claude invocation; the records above are validated structurally (schema + inventory).
