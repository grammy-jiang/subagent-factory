# Test Results — software-testing-advisor

**Generated:** 2026-07-03T13:40:26.159904+00:00

## Phase 8 Profile Self-Check

**Verdict:** WARNING

| # | Check | Level | Detail |
|---|-------|-------|--------|
| 1 | slug | PASS | slug 'software-testing-advisor' is kebab-case and role-based |
| 2 | when-to-use | PASS | 5 triggers |
| 3 | when-not-to-use | PASS | 3 exclusions |
| 4 | modes-evidence | INFO | mode source-evidence traceability delegated to profile-reviewer |
| 5 | inputs-required | PASS | 1 required input(s) |
| 6 | primary-format | PASS | A grounded test-design recommendation or critique — the arti |
| 7 | mode-output | PASS | every mode states its output |
| 8 | minimum-useful-output | PASS | defined |
| 9 | canonical-owner | PASS | The developer or team owning the code and tests holds final  |
| 10 | may-edit-canonical | PASS | false |
| 11 | quality-bar | PASS | 5 evidence-citing checks |
| 12 | forbidden-behaviours | INFO | 5 rules; source traceability delegated to profile-reviewer |
| 13 | no-procedure-in-body | PASS | no ordered procedure detected in body |
| 14 | body-size | WARNING | profile body ~830 words (> 800); 30 over the 800-word budget; heaviest: modes 148w, quality_bar 123w, when_to_use 105w |
| 15 | platform-neutral | PASS | core is platform-neutral |
| 16 | provenance-ledger | PASS | present |
| 17 | no-unresolved-conflict | INFO | conflict resolution review delegated to profile-reviewer / Phase 7 merge log |
| 18 | golden-tests | PASS | 4 golden, 2 negative routing |

## Routing Tests (structural)

**Records validated:** 7/7

| Test ID | Status | Description |
|---------|--------|-------------|
| GT-001 | SCHEMA-OK | Positive routing — advise on how to design tests for a unit with a dependency |
| GT-002 | SCHEMA-OK | Positive routing — review an existing test suite for smells and gaps |
| GT-003 | SCHEMA-OK | Positive routing — compare coverage criteria by cost and strength |
| GT-004 | SCHEMA-OK | Positive routing — choose the right kind of test double |
| NR-001 | SCHEMA-OK | Negative routing — request to write the production/test code and pick a framework |
| NR-002 | SCHEMA-OK | Negative routing — no test-design dimension |
| MC-001 | SCHEMA-OK | Missing required input — no artifact or specification provided |

> Live routing/permission execution requires a Claude invocation; the records above are validated structurally (schema + inventory).
