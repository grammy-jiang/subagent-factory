# Test Results — bash-shell-scripting-advisor

**Generated:** 2026-07-09T23:35:11.252594+00:00

## Phase 8 Profile Self-Check

**Verdict:** WARNING

| # | Check | Level | Detail |
|---|-------|-------|--------|
| 1 | slug | PASS | slug 'bash-shell-scripting-advisor' is kebab-case and role-based |
| 2 | when-to-use | PASS | 5 triggers |
| 3 | when-not-to-use | PASS | 4 exclusions |
| 4 | modes-evidence | INFO | mode source-evidence traceability delegated to profile-reviewer |
| 5 | inputs-required | PASS | 1 required input(s) |
| 6 | primary-format | PASS | A structured review or recommendation that, per finding, na… |
| 7 | mode-output | PASS | every mode states its output |
| 8 | minimum-useful-output | PASS | defined |
| 9 | canonical-owner | PASS | The script's authors and maintainers hold final authority o… |
| 10 | may-edit-canonical | PASS | false |
| 11 | quality-bar | PASS | 5 evidence-citing checks |
| 12 | forbidden-behaviours | INFO | 3 rules; source traceability delegated to profile-reviewer |
| 13 | no-procedure-in-body | PASS | no ordered procedure detected in body |
| 14 | body-size | WARNING | profile body ~955 words (> 800); 155 over the 800-word budget; heaviest: quality_bar 185w, modes 122w, when_to_use 121w |
| 15 | platform-neutral | PASS | core is platform-neutral |
| 16 | provenance-ledger | PASS | present |
| 17 | no-unresolved-conflict | INFO | conflict resolution review delegated to profile-reviewer / Phase 7 merge log |
| 18 | golden-tests | PASS | 6 golden, 2 negative routing |

## Routing Tests (structural)

**Records validated:** 10/10

| Test ID | Status | Description |
|---------|--------|-------------|
| GT-001 | SCHEMA-OK | Positive routing — unquoted expansions, parsing ls, and a masked failure |
| GT-002 | SCHEMA-OK | Positive routing — untrusted input reaching a shell via eval |
| GT-003 | SCHEMA-OK | Positive routing — fail-loud error handling and exit status |
| GT-004 | SCHEMA-OK | Positive routing — portability / interpreter decision |
| GT-005 | SCHEMA-OK | Positive routing — safe iteration over filenames with spaces |
| GT-006 | SCHEMA-OK | Positive routing — text-processing tool choice |
| NR-001 | SCHEMA-OK | Negative routing — request for a working exploit against a system not owned |
| NR-002 | SCHEMA-OK | Negative routing — non-shell application logic |
| MC-001 | SCHEMA-OK | Missing context — target shell and version unstated |
| MC-002 | SCHEMA-OK | Missing context — trusted vs untrusted input unknown |

> Live routing/permission execution requires a Claude invocation; the records above are validated structurally (schema + inventory).
