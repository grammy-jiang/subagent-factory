# Test Results — microservice-patterns-advisor

**Generated:** 2026-06-11T09:25:38.529806+00:00

## Phase 8 Profile Self-Check

**Verdict:** WARNING

| # | Check | Level | Detail |
|---|-------|-------|--------|
| 1 | slug | PASS | slug 'microservice-patterns-advisor' is kebab-case and role-based |
| 2 | when-to-use | PASS | 6 triggers |
| 3 | when-not-to-use | PASS | 3 exclusions |
| 4 | modes-evidence | INFO | mode source-evidence traceability delegated to profile-reviewer |
| 5 | inputs-required | PASS | 1 required input(s) |
| 6 | primary-format | PASS | A named shortlist of candidate patterns from the relevant gr |
| 7 | mode-output | PASS | every mode states its output |
| 8 | minimum-useful-output | PASS | defined |
| 9 | canonical-owner | PASS | The architect or engineering team that owns the system desig |
| 10 | may-edit-canonical | PASS | false |
| 11 | quality-bar | PASS | 4 evidence-citing checks |
| 12 | forbidden-behaviours | INFO | 4 rules; source traceability delegated to profile-reviewer |
| 13 | no-procedure-in-body | PASS | no ordered procedure detected in body |
| 14 | body-size | WARNING | profile body ~831 words (> 800); 31 over the 800-word budget; heaviest: when_to_use 173w, quality_bar 124w, modes 120w |
| 15 | platform-neutral | PASS | core is platform-neutral |
| 16 | provenance-ledger | PASS | present |
| 17 | no-unresolved-conflict | INFO | conflict resolution review delegated to profile-reviewer / Phase 7 merge log |
| 18 | golden-tests | PASS | 3 golden, 1 negative routing |

## Routing Tests (structural)

**Records validated:** 5/5

| Test ID | Status | Description |
|---------|--------|-------------|
| GT-001 | SCHEMA-OK | Positive routing — advise on cross-service data consistency |
| GT-002 | SCHEMA-OK | Positive routing — advise on service decomposition |
| GT-003 | SCHEMA-OK | Positive routing — compare alternative communication patterns |
| NR-001 | SCHEMA-OK | Negative routing — product/technology selection is out of scope |
| MC-001 | SCHEMA-OK | Missing required input — no architecture concern stated |

> Live routing/permission execution requires a Claude invocation; the records above are validated structurally (schema + inventory).
