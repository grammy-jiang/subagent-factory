# Test Results — cloud-native-kubernetes-advisor

**Generated:** 2026-06-14T05:53:10.221732+00:00

## Phase 8 Profile Self-Check

**Verdict:** PASS

| # | Check | Level | Detail |
|---|-------|-------|--------|
| 1 | slug | PASS | slug 'cloud-native-kubernetes-advisor' is kebab-case and role-based |
| 2 | when-to-use | PASS | 5 triggers |
| 3 | when-not-to-use | PASS | 3 exclusions |
| 4 | modes-evidence | INFO | mode source-evidence traceability delegated to profile-reviewer |
| 5 | inputs-required | PASS | 4 required input(s) |
| 6 | primary-format | PASS | Actionable architectural recommendations and decision guidan |
| 7 | mode-output | PASS | every mode states its output |
| 8 | minimum-useful-output | PASS | defined |
| 9 | canonical-owner | PASS | Engineering leadership or platform/DevOps team at the organi |
| 10 | may-edit-canonical | PASS | false |
| 11 | quality-bar | PASS | 5 evidence-citing checks |
| 12 | forbidden-behaviours | INFO | 5 rules; source traceability delegated to profile-reviewer |
| 13 | no-procedure-in-body | PASS | no ordered procedure detected in body |
| 14 | body-size | PASS | ~788 words |
| 15 | platform-neutral | PASS | core is platform-neutral |
| 16 | provenance-ledger | PASS | present |
| 17 | no-unresolved-conflict | INFO | conflict resolution review delegated to profile-reviewer / Phase 7 merge log |
| 18 | golden-tests | PASS | 3 golden, 1 negative routing |

## Routing Tests (structural)

**Records validated:** 5/5

| Test ID | Status | Description |
|---------|--------|-------------|
| GT-001 | SCHEMA-OK | Positive routing — advise mode: managed-vs-self-hosted decision for a startup engineering team on AWS. |
| GT-002 | SCHEMA-OK | Positive routing — validate mode: production-readiness check for a proposed self-managed cluster architecture. |
| GT-003 | SCHEMA-OK | Positive routing — produce mode: request for a minimal Dockerfile for a Go service. |
| NR-001 | SCHEMA-OK | Negative routing — do not invoke for application source code debugging request. |
| MC-001 | SCHEMA-OK | Missing required input — advise mode called without infrastructure context or team size; advisor must request before proceeding. |

> Live routing/permission execution requires a Claude invocation; the records above are validated structurally (schema + inventory).
