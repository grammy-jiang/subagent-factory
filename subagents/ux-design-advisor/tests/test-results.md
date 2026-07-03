# Test Results — ux-design-advisor

**Generated:** 2026-07-03T01:26:53.594752+00:00

## Phase 8 Profile Self-Check

**Verdict:** WARNING

| # | Check | Level | Detail |
|---|-------|-------|--------|
| 1 | slug | PASS | slug 'ux-design-advisor' is kebab-case and role-based |
| 2 | when-to-use | PASS | 5 triggers |
| 3 | when-not-to-use | PASS | 3 exclusions |
| 4 | modes-evidence | INFO | mode source-evidence traceability delegated to profile-reviewer |
| 5 | inputs-required | PASS | 1 required input(s) |
| 6 | primary-format | PASS | A structured UX critique or recommendation that names the us |
| 7 | mode-output | PASS | every mode states its output |
| 8 | minimum-useful-output | PASS | defined |
| 9 | canonical-owner | PASS | The product team and its designers hold final authority over |
| 10 | may-edit-canonical | PASS | false |
| 11 | quality-bar | PASS | 5 evidence-citing checks |
| 12 | forbidden-behaviours | INFO | 3 rules; source traceability delegated to profile-reviewer |
| 13 | no-procedure-in-body | PASS | no ordered procedure detected in body |
| 14 | body-size | WARNING | profile body ~803 words (> 800); 3 over the 800-word budget; heaviest: when_to_use 126w, modes 120w, quality_bar 119w |
| 15 | platform-neutral | PASS | core is platform-neutral |
| 16 | provenance-ledger | PASS | present |
| 17 | no-unresolved-conflict | INFO | conflict resolution review delegated to profile-reviewer / Phase 7 merge log |
| 18 | golden-tests | PASS | 5 golden, 2 negative routing |

## Routing Tests (structural)

**Records validated:** 9/9

| Test ID | Status | Description |
|---------|--------|-------------|
| GT-001 | SCHEMA-OK | Positive routing — make a dense page self-evident and scannable |
| GT-002 | SCHEMA-OK | Positive routing — organize IA from users, content, and context |
| GT-003 | SCHEMA-OK | Positive routing — match research to the problem's maturity and manage bias |
| GT-004 | SCHEMA-OK | Positive routing — genuine conversation, not a chat facade |
| GT-005 | SCHEMA-OK | Positive routing — judge navigation by click difficulty, not count |
| NR-001 | SCHEMA-OK | Out of scope — production code and tooling selection |
| NR-002 | SCHEMA-OK | Out of scope — security and legal review |
| MC-001 | SCHEMA-OK | Underspecified — no user, goal, or channel given |
| MC-002 | SCHEMA-OK | Underspecified — research request with no problem-stage detail |

> Live routing/permission execution requires a Claude invocation; the records above are validated structurally (schema + inventory).
