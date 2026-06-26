# Test Results — test-driven-development-advisor

**Generated:** 2026-06-15T13:18:22.864801+00:00

## Phase 8 Profile Self-Check

**Verdict:** WARNING

| # | Check | Level | Detail |
|---|-------|-------|--------|
| 1 | slug | PASS | slug 'test-driven-development-advisor' is kebab-case and role-based |
| 2 | when-to-use | PASS | 5 triggers |
| 3 | when-not-to-use | PASS | 3 exclusions |
| 4 | modes-evidence | INFO | mode source-evidence traceability delegated to profile-reviewer |
| 5 | inputs-required | PASS | 1 required input(s) |
| 6 | primary-format | PASS | A concrete next step in the TDD cycle — the next small faili |
| 7 | mode-output | PASS | every mode states its output |
| 8 | minimum-useful-output | PASS | defined |
| 9 | canonical-owner | PASS | The developer or team owning the code holds final authority  |
| 10 | may-edit-canonical | PASS | false |
| 11 | quality-bar | PASS | 4 evidence-citing checks |
| 12 | forbidden-behaviours | INFO | 4 rules; source traceability delegated to profile-reviewer |
| 13 | no-procedure-in-body | WARNING | possible multi-step workflow in profile body; extract to a skill |
| 14 | body-size | PASS | ~748 words |
| 15 | platform-neutral | PASS | core is platform-neutral |
| 16 | provenance-ledger | PASS | present |
| 17 | no-unresolved-conflict | INFO | conflict resolution review delegated to profile-reviewer / Phase 7 merge log |
| 18 | golden-tests | PASS | 3 golden, 1 negative routing |

## Routing Tests (structural)

**Records validated:** 4/4

| Test ID | Status | Description |
|---------|--------|-------------|
| GT-001 | SCHEMA-OK | Positive routing — advise on the next test-first step |
| GT-002 | SCHEMA-OK | Positive routing — compare get-to-green strategies |
| GT-003 | SCHEMA-OK | Positive routing — review whether a change was test-driven |
| NR-001 | SCHEMA-OK | Negative routing — out-of-scope architecture/technology selection |

> Live routing/permission execution requires a Claude invocation; the records above are validated structurally (schema + inventory).
