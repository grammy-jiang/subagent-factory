# Test Results — unix-v6-kernel-source-reviewer

**Generated:** 2026-06-11T11:18:19.049743+00:00

## Phase 8 Profile Self-Check

**Verdict:** PASS

| # | Check | Level | Detail |
|---|-------|-------|--------|
| 1 | slug | PASS | slug 'unix-v6-kernel-source-reviewer' is kebab-case and role-based |
| 2 | when-to-use | PASS | 5 triggers |
| 3 | when-not-to-use | PASS | 3 exclusions |
| 4 | modes-evidence | INFO | mode source-evidence traceability delegated to profile-reviewer |
| 5 | inputs-required | PASS | 1 required input(s) |
| 6 | primary-format | PASS | Prose commentary tracing control flow, explaining data-struc |
| 7 | mode-output | PASS | every mode states its output |
| 8 | minimum-useful-output | PASS | defined |
| 9 | canonical-owner | PASS | The UNIX Operating System Source Code, Level Six (companion  |
| 10 | may-edit-canonical | PASS | false |
| 11 | quality-bar | PASS | 5 evidence-citing checks |
| 12 | forbidden-behaviours | INFO | 4 rules; source traceability delegated to profile-reviewer |
| 13 | no-procedure-in-body | PASS | no ordered procedure detected in body |
| 14 | body-size | PASS | ~732 words |
| 15 | platform-neutral | PASS | core is platform-neutral |
| 16 | provenance-ledger | PASS | present |
| 17 | no-unresolved-conflict | INFO | conflict resolution review delegated to profile-reviewer / Phase 7 merge log |
| 18 | golden-tests | PASS | 3 golden, 2 negative routing |

## Routing Tests (structural)

**Records validated:** 6/6

| Test ID | Status | Description |
|---------|--------|-------------|
| GT-001 | SCHEMA-OK | Positive routing (advise mode) — caller asks what the swtch procedure does and how it relates to the sleep/wakeup scheduling loop. |
| GT-002 | SCHEMA-OK | Positive routing (review mode) — caller flags an apparently anomalous coding pattern in getblk and asks whether it is a defect. |
| GT-003 | SCHEMA-OK | Positive routing (extract mode) — caller asks for a structured list of the proc structure fields and their meanings. |
| NR-001 | SCHEMA-OK | Negative routing — caller asks about the Linux kernel scheduler, which is outside V6 scope. |
| NR-002 | SCHEMA-OK | Negative routing — caller asks about a user-space utility (the shell), which is outside kernel-nucleus scope. |
| MC-001 | SCHEMA-OK | Missing required input — caller asks for a review without naming a specific procedure or line range. |

> Live routing/permission execution requires a Claude invocation; the records above are validated structurally (schema + inventory).
