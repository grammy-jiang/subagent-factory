# Test Results — domain-driven-design-reviewer

**Generated:** 2026-06-12T23:57:18.046931+00:00

## Phase 8 Profile Self-Check

**Verdict:** PASS

| # | Check | Level | Detail |
|---|-------|-------|--------|
| 1 | slug | PASS | slug 'domain-driven-design-reviewer' is kebab-case and role-based |
| 2 | when-to-use | PASS | 6 triggers |
| 3 | when-not-to-use | PASS | 3 exclusions |
| 4 | modes-evidence | INFO | mode source-evidence traceability delegated to profile-reviewer |
| 5 | inputs-required | PASS | 2 required input(s) |
| 6 | primary-format | PASS | structured review report |
| 7 | mode-output | PASS | every mode states its output |
| 8 | minimum-useful-output | PASS | defined |
| 9 | canonical-owner | PASS | development team in collaboration with domain experts |
| 10 | may-edit-canonical | PASS | false |
| 11 | quality-bar | PASS | 6 evidence-citing checks |
| 12 | forbidden-behaviours | INFO | 5 rules; source traceability delegated to profile-reviewer |
| 13 | no-procedure-in-body | PASS | no ordered procedure detected in body |
| 14 | body-size | PASS | ~770 words |
| 15 | platform-neutral | PASS | core is platform-neutral |
| 16 | provenance-ledger | PASS | present |
| 17 | no-unresolved-conflict | INFO | conflict resolution review delegated to profile-reviewer / Phase 7 merge log |
| 18 | golden-tests | PASS | 3 golden, 2 negative routing |

## Routing Tests (structural)

**Records validated:** 6/6

| Test ID | Status | Description |
|---------|--------|-------------|
| GT-001 | SCHEMA-OK | Positive routing — review mode for submitted domain model covering Entity/Value Object misclassification and layer violation (P003, P004, P005) |
| GT-002 | SCHEMA-OK | Positive routing — advise mode for Bounded Context and inter-context integration pattern selection (P011, P012) |
| GT-003 | SCHEMA-OK | Positive routing — validate mode for Aggregate invariant check (P007) |
| NR-001 | SCHEMA-OK | Negative routing — pure DevOps concern with no domain-modeling dimension |
| NR-002 | SCHEMA-OK | Negative routing — trivial CRUD application, Smart UI acknowledged |
| MC-001 | SCHEMA-OK | Missing required input — model artifact not provided |

> Live routing/permission execution requires a Claude invocation; the records above are validated structurally (schema + inventory).
