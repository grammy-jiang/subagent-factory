# Test Results — strengths-based-development-coach

**Generated:** 2026-06-11T01:43:09.576289+00:00

## Phase 8 Profile Self-Check

**Verdict:** WARNING

| # | Check | Level | Detail |
|---|-------|-------|--------|
| 1 | slug | PASS | slug 'strengths-based-development-coach' is kebab-case and role-based |
| 2 | when-to-use | PASS | 5 triggers |
| 3 | when-not-to-use | PASS | 3 exclusions |
| 4 | modes-evidence | INFO | mode source-evidence traceability delegated to profile-reviewer |
| 5 | inputs-required | PASS | 3 required input(s) |
| 6 | primary-format | PASS | Structured personalised development advisory: interpretation |
| 7 | mode-output | PASS | every mode states its output |
| 8 | minimum-useful-output | PASS | defined |
| 9 | canonical-owner | PASS | The individual whose StrengthsFinder 2.0 assessment results  |
| 10 | may-edit-canonical | PASS | false |
| 11 | quality-bar | PASS | 5 evidence-citing checks |
| 12 | forbidden-behaviours | INFO | 6 rules; source traceability delegated to profile-reviewer |
| 13 | no-procedure-in-body | PASS | no ordered procedure detected in body |
| 14 | body-size | WARNING | profile body ~886 words (> 800); 86 over the 800-word budget; heaviest: forbidden_behaviours 178w, modes 152w, when_to_use 114w |
| 15 | platform-neutral | PASS | core is platform-neutral |
| 16 | provenance-ledger | PASS | present |
| 17 | no-unresolved-conflict | INFO | conflict resolution review delegated to profile-reviewer / Phase 7 merge log |
| 18 | golden-tests | PASS | 3 golden, 1 negative routing |

## Routing Tests (structural)

**Records validated:** 5/5

| Test ID | Status | Description |
|---------|--------|-------------|
| GT-001 | SCHEMA-OK | Positive routing advise mode — individual provides top-five themes and current role and wants personalised interpretation and action ideas. |
| GT-002 | SCHEMA-OK | Positive routing produce mode — manager requests a Strength-Based Action Plan document for a direct report. |
| GT-003 | SCHEMA-OK | Positive routing extract mode — team leader provides all team members' themes and wants a team strengths grid. |
| NR-001 | SCHEMA-OK | Negative routing — request is for clinical depression diagnosis, which is outside the framework's scope. |
| MC-001 | SCHEMA-OK | Missing required input — caller asks for coaching without providing their top-five theme names. |

> Live routing/permission execution requires a Claude invocation; the records above are validated structurally (schema + inventory).
