# Test Results — translation-equivalence-advisor

**Generated:** 2026-07-11T20:31:56.464230+00:00

## Phase 8 Profile Self-Check

**Verdict:** WARNING

| # | Check | Level | Detail |
|---|-------|-------|--------|
| 1 | slug | PASS | slug 'translation-equivalence-advisor' is kebab-case and role-based |
| 2 | when-to-use | PASS | 4 triggers |
| 3 | when-not-to-use | PASS | 4 exclusions |
| 4 | modes-evidence | INFO | mode source-evidence traceability delegated to profile-reviewer |
| 5 | inputs-required | PASS | 1 required input(s) |
| 6 | primary-format | PASS | A structured, principle-cited recommendation or findings li… |
| 7 | mode-output | PASS | every mode states its output |
| 8 | minimum-useful-output | PASS | defined |
| 9 | canonical-owner | PASS | The translator and the commissioner hold final authority ov… |
| 10 | may-edit-canonical | PASS | false |
| 11 | quality-bar | PASS | 9 evidence-citing checks |
| 12 | forbidden-behaviours | INFO | 4 rules; source traceability delegated to profile-reviewer |
| 13 | no-procedure-in-body | PASS | no ordered procedure detected in body |
| 14 | body-size | WARNING | profile body ~981 words (> 800); 181 over the 800-word budget; heaviest: quality_bar 237w, when_not_to_use 118w, forbidden_behaviours 115w |
| 15 | platform-neutral | PASS | core is platform-neutral |
| 16 | provenance-ledger | PASS | present |
| 17 | no-unresolved-conflict | INFO | conflict resolution review delegated to profile-reviewer / Phase 7 merge log |
| 18 | golden-tests | PASS | 5 golden, 2 negative routing |

## Routing Tests (structural)

**Records validated:** 9/9

| Test ID | Status | Description |
|---------|--------|-------------|
| GT-001 | SCHEMA-OK | Word-level non-equivalence — culture-specific term |
| GT-002 | SCHEMA-OK | Grammatical equivalence — voice by function |
| GT-003 | SCHEMA-OK | Cohesion — do not transfer source devices |
| GT-004 | SCHEMA-OK | Orientation — formal vs dynamic for a brief |
| GT-005 | SCHEMA-OK | Information structure — thematic markedness by function |
| NR-001 | SCHEMA-OK | Out of scope — tool selection |
| NR-002 | SCHEMA-OK | Out of scope — deliver the finished translation |
| MC-001 | SCHEMA-OK | Underspecified — no brief or audience |
| MC-002 | SCHEMA-OK | Underspecified — orientation with no purpose |

> Live routing/permission execution requires a Claude invocation; the records above are validated structurally (schema + inventory).
