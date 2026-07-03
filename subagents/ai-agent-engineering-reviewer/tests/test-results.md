# Test Results — ai-agent-engineering-reviewer

**Generated:** 2026-07-03T02:46:08.617192+00:00

## Phase 8 Profile Self-Check

**Verdict:** WARNING

| # | Check | Level | Detail |
|---|-------|-------|--------|
| 1 | slug | PASS | slug 'ai-agent-engineering-reviewer' is kebab-case and role-based |
| 2 | when-to-use | PASS | 5 triggers |
| 3 | when-not-to-use | PASS | 3 exclusions |
| 4 | modes-evidence | INFO | mode source-evidence traceability delegated to profile-reviewer |
| 5 | inputs-required | PASS | 1 required input(s) |
| 6 | primary-format | PASS | A structured engineering critique or recommendation that nam |
| 7 | mode-output | PASS | every mode states its output |
| 8 | minimum-useful-output | PASS | defined |
| 9 | canonical-owner | PASS | The engineering team holds final authority over the agent's  |
| 10 | may-edit-canonical | PASS | false |
| 11 | quality-bar | PASS | 5 evidence-citing checks |
| 12 | forbidden-behaviours | INFO | 3 rules; source traceability delegated to profile-reviewer |
| 13 | no-procedure-in-body | PASS | no ordered procedure detected in body |
| 14 | body-size | WARNING | profile body ~941 words (> 800); 141 over the 800-word budget; heaviest: quality_bar 170w, when_to_use 146w, modes 143w |
| 15 | platform-neutral | PASS | core is platform-neutral |
| 16 | provenance-ledger | PASS | present |
| 17 | no-unresolved-conflict | INFO | conflict resolution review delegated to profile-reviewer / Phase 7 merge log |
| 18 | golden-tests | PASS | 6 golden, 3 negative routing |

## Routing Tests (structural)

**Records validated:** 11/11

| Test ID | Status | Description |
|---------|--------|-------------|
| GT-001 | SCHEMA-OK | Positive routing — replace a whole-history prompt dump with scored retrieval |
| GT-002 | SCHEMA-OK | Positive routing — thicken a thin action-only agent loop |
| GT-003 | SCHEMA-OK | Positive routing — a tool/retrieval bolt-on with unproven benefit |
| GT-004 | SCHEMA-OK | Positive routing — safety framed as content refusal only |
| GT-005 | SCHEMA-OK | Positive routing — evaluation reported as one aggregate number |
| GT-006 | SCHEMA-OK | Positive routing — designing retrieval-augmented generation for a knowledge task |
| NR-001 | SCHEMA-OK | Negative routing — request to write the production agent implementation |
| NR-002 | SCHEMA-OK | Negative routing — procurement of model/framework/vector store |
| NR-003 | SCHEMA-OK | Negative routing — concern outside agent engineering |
| MC-001 | SCHEMA-OK | Missing context — "is our agent safe?" with no environment described |
| MC-002 | SCHEMA-OK | Missing context — "how should we evaluate the agent?" with no response type or stage |

> Live routing/permission execution requires a Claude invocation; the records above are validated structurally (schema + inventory).
