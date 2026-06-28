# Test Results — devops-sre-advisor

**Generated:** 2026-06-20T00:00:14.011041+00:00

## Phase 8 Profile Self-Check

**Verdict:** PASS

| # | Check | Level | Detail |
|---|-------|-------|--------|
| 1 | slug | PASS | slug 'devops-sre-advisor' is kebab-case and role-based |
| 2 | when-to-use | PASS | 5 triggers |
| 3 | when-not-to-use | PASS | 3 exclusions |
| 4 | modes-evidence | INFO | mode source-evidence traceability delegated to profile-reviewer |
| 5 | inputs-required | PASS | 3 required input(s) |
| 6 | primary-format | PASS | Actionable, evidence-grounded recommendations and assessment |
| 7 | mode-output | PASS | every mode states its output |
| 8 | minimum-useful-output | PASS | defined |
| 9 | canonical-owner | PASS | Engineering leadership and the owning service team, supporte |
| 10 | may-edit-canonical | PASS | false |
| 11 | quality-bar | PASS | 5 evidence-citing checks |
| 12 | forbidden-behaviours | INFO | 5 rules; source traceability delegated to profile-reviewer |
| 13 | no-procedure-in-body | PASS | no ordered procedure detected in body |
| 14 | body-size | PASS | ~766 words |
| 15 | platform-neutral | PASS | core is platform-neutral |
| 16 | provenance-ledger | PASS | present |
| 17 | no-unresolved-conflict | INFO | conflict resolution review delegated to profile-reviewer / Phase 7 merge log |
| 18 | golden-tests | PASS | 4 golden, 2 negative routing |

## Routing Tests (structural)

**Records validated:** 7/7

| Test ID | Status | Description |
|---------|--------|-------------|
| GT-001 | SCHEMA-OK | Positive routing — advise mode: a team causing outages while shipping fast asks how to balance feature work and reliability. |
| GT-002 | SCHEMA-OK | Positive routing — validate mode: production-readiness review of a manual, single-stage deployment process. |
| GT-003 | SCHEMA-OK | Positive routing — review mode: critique of a noisy cause-based alerting and on-call setup. |
| GT-004 | SCHEMA-OK | Positive routing — compare mode: branching strategy choice for faster, safer integration. |
| NR-001 | SCHEMA-OK | Negative routing — application feature development is out of scope. |
| NR-002 | SCHEMA-OK | Negative routing — accountable regulatory/legal sign-off is not this advisor's decision. |
| MC-001 | SCHEMA-OK | Missing required input — request the delivery/reliability question and system context. |

> Live routing/permission execution requires a Claude invocation; the records above are validated structurally (schema + inventory).
