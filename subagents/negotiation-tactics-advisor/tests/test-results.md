# Test Results — negotiation-tactics-advisor

**Generated:** 2026-06-10T14:13:58.871076+00:00

## Phase 8 Profile Self-Check

**Verdict:** PASS

| # | Check | Level | Detail |
|---|-------|-------|--------|
| 1 | slug | PASS | slug 'negotiation-tactics-advisor' is kebab-case and role-based |
| 2 | when-to-use | PASS | 5 triggers |
| 3 | when-not-to-use | PASS | 3 exclusions |
| 4 | modes-evidence | INFO | mode source-evidence traceability delegated to profile-reviewer |
| 5 | inputs-required | PASS | 2 required input(s) |
| 6 | primary-format | PASS | Tactical negotiation guidance: a recommended set of techniqu |
| 7 | mode-output | PASS | every mode states its output |
| 8 | minimum-useful-output | PASS | defined |
| 9 | canonical-owner | PASS | The negotiator (caller) who owns the live conversation and f |
| 10 | may-edit-canonical | PASS | false |
| 11 | quality-bar | PASS | 4 evidence-citing checks |
| 12 | forbidden-behaviours | INFO | 5 rules; source traceability delegated to profile-reviewer |
| 13 | no-procedure-in-body | PASS | no ordered procedure detected in body |
| 14 | body-size | PASS | ~738 words |
| 15 | platform-neutral | PASS | core is platform-neutral |
| 16 | provenance-ledger | PASS | present |
| 17 | no-unresolved-conflict | INFO | conflict resolution review delegated to profile-reviewer / Phase 7 merge log |
| 18 | golden-tests | PASS | 3 golden, 1 negative routing |

## Routing Tests (structural)

**Records validated:** 5/5

| Test ID | Status | Description |
|---------|--------|-------------|
| GT-001 | SCHEMA-OK | Positive routing — advise mode for a salary negotiation with an emotional counterpart. Exercises PRIN-001 (tactical empathy), PRIN-002/003 (labeling and accusation audit), PRIN-007 (calibrated questions), PRIN-008 (Ackerman bargaining), and PRIN-010 (counterpart style adaptation). |
| GT-002 | SCHEMA-OK | Positive routing — review mode critiques a planned script. Exercises PRIN-001 (tactical empathy first), PRIN-005 (No over Yes), PRIN-006 (counterfeit Yes risk), PRIN-002/004 (labeling and mirroring as corrections), PRIN-007 (Why banned). |
| GT-003 | SCHEMA-OK | Positive routing — compare mode on No-vs-Yes and leverage types. Exercises PRIN-005 (No as safety), PRIN-006 (That's Right vs counterfeit Yes), PRIN-009 (Black Swan and leverage types), PRIN-008 (Ackerman and never-split-the-difference context), PRIN-003 (accusation audit before numbers), PRIN-010 (counterpart styles). |
| NR-001 | SCHEMA-OK | Negative routing — binding legal advice is outside scope (when_not_to_use exclusion 1). This test does NOT match GT-001–GT-003 principle IDs because the correct response is non-invocation. |
| MC-001 | SCHEMA-OK | Missing required input — warn and request the negotiation context before proceeding. Exercises PRIN-009 (cannot assess leverage without situation) and the inputs.required gate (situation description and constraints both needed). |

> Live routing/permission execution requires a Claude invocation; the records above are validated structurally (schema + inventory).
