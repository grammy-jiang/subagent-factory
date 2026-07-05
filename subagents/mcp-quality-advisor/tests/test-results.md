# Test Results — mcp-quality-advisor

**Generated:** 2026-07-05T07:39:57.521548+00:00

## Phase 8 Profile Self-Check

**Verdict:** WARNING

| # | Check | Level | Detail |
|---|-------|-------|--------|
| 1 | slug | PASS | slug 'mcp-quality-advisor' is kebab-case and role-based |
| 2 | when-to-use | PASS | 5 triggers |
| 3 | when-not-to-use | PASS | 3 exclusions |
| 4 | modes-evidence | INFO | mode source-evidence traceability delegated to profile-reviewer |
| 5 | inputs-required | PASS | 1 required input(s) |
| 6 | primary-format | PASS | A prioritized set of recommendations, each naming the speci… |
| 7 | mode-output | PASS | every mode states its output |
| 8 | minimum-useful-output | PASS | defined |
| 9 | canonical-owner | PASS | Twenty-nine ingested primary and secondary sources on MCP s… |
| 10 | may-edit-canonical | PASS | false |
| 11 | quality-bar | PASS | 5 evidence-citing checks |
| 12 | forbidden-behaviours | INFO | 5 rules; source traceability delegated to profile-reviewer |
| 13 | no-procedure-in-body | PASS | no ordered procedure detected in body |
| 14 | body-size | WARNING | profile body ~876 words (> 800); 76 over the 800-word budget; heaviest: quality_bar 160w, when_to_use 147w, forbidden_behaviours 124w |
| 15 | platform-neutral | PASS | core is platform-neutral |
| 16 | provenance-ledger | PASS | present |
| 17 | no-unresolved-conflict | INFO | conflict resolution review delegated to profile-reviewer / Phase 7 merge log |
| 18 | golden-tests | PASS | 8 golden, 3 negative routing |

## Routing Tests (structural)

**Records validated:** 11/11

| Test ID | Status | Description |
|---------|--------|-------------|
| GT-001 | SCHEMA-OK | Positive — scope and describe a large tool surface |
| GT-002 | SCHEMA-OK | Positive — cut per-turn tool-schema cost |
| GT-003 | SCHEMA-OK | Positive — review a tool description |
| GT-004 | SCHEMA-OK | Positive — verify protocol compliance |
| GT-005 | SCHEMA-OK | Positive — design an evaluation with judges |
| GT-006 | SCHEMA-OK | Positive — operate MCP on serverless cost-effectively |
| GT-007 | SCHEMA-OK | Negative-adjacent — CLI vs MCP decision |
| GT-008 | SCHEMA-OK | Missing-context — under-specified request |
| NR-001 | SCHEMA-OK | Negative — write the production feature, not the MCP surface |
| NR-002 | SCHEMA-OK | Negative — unauthorized offensive testing of a third-party server |
| NR-003 | SCHEMA-OK | Negative — non-MCP REST/UI concern |

> Live routing/permission execution requires a Claude invocation; the records above are validated structurally (schema + inventory).
