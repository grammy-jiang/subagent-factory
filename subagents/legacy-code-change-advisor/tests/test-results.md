# Test Results — legacy-code-change-advisor

**Generated:** 2026-06-14T22:44:30.656953+00:00

## Phase 8 Profile Self-Check

**Verdict:** WARNING

| # | Check | Level | Detail |
|---|-------|-------|--------|
| 1 | slug | PASS | slug 'legacy-code-change-advisor' is kebab-case and role-based |
| 2 | when-to-use | PASS | 5 triggers |
| 3 | when-not-to-use | PASS | 3 exclusions |
| 4 | modes-evidence | INFO | mode source-evidence traceability delegated to profile-reviewer |
| 5 | inputs-required | PASS | 3 required input(s) |
| 6 | primary-format | PASS | Structured advisory guidance naming the seam(s) and enabling |
| 7 | mode-output | PASS | every mode states its output |
| 8 | minimum-useful-output | PASS | defined |
| 9 | canonical-owner | PASS | The developer or team who owns the legacy codebase under cha |
| 10 | may-edit-canonical | PASS | false |
| 11 | quality-bar | PASS | 5 evidence-citing checks |
| 12 | forbidden-behaviours | INFO | 5 rules; source traceability delegated to profile-reviewer |
| 13 | no-procedure-in-body | PASS | no ordered procedure detected in body |
| 14 | body-size | WARNING | profile body ~926 words (> 800); 126 over the 800-word budget; heaviest: modes 183w, when_to_use 139w, quality_bar 132w |
| 15 | platform-neutral | PASS | core is platform-neutral |
| 16 | provenance-ledger | PASS | present |
| 17 | no-unresolved-conflict | INFO | conflict resolution review delegated to profile-reviewer / Phase 7 merge log |
| 18 | golden-tests | PASS | 3 golden, 2 negative routing |

## Routing Tests (structural)

**Records validated:** 6/6

| Test ID | Status | Description |
|---------|--------|-------------|
| G-001 | SCHEMA-OK | Core algorithm + dependency-breaking advice for untested code |
| G-002 | SCHEMA-OK | Characterization-test technique for unknown behaviour |
| G-003 | SCHEMA-OK | Time-pressured feature addition to untested class |
| N-001 | SCHEMA-OK | Greenfield design question — out of scope |
| N-002 | SCHEMA-OK | Exploratory bug-hunting QA — out of scope |
| M-001 | SCHEMA-OK | No code or change described |

> Live routing/permission execution requires a Claude invocation; the records above are validated structurally (schema + inventory).
