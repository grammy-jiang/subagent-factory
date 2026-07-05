# Test Results — mcp-protocol-advisor

**Generated:** 2026-07-05T07:36:41.296774+00:00

## Phase 8 Profile Self-Check

**Verdict:** WARNING

| # | Check | Level | Detail |
|---|-------|-------|--------|
| 1 | slug | PASS | slug 'mcp-protocol-advisor' is kebab-case and role-based |
| 2 | when-to-use | PASS | 5 triggers |
| 3 | when-not-to-use | PASS | 3 exclusions |
| 4 | modes-evidence | INFO | mode source-evidence traceability delegated to profile-reviewer |
| 5 | inputs-required | PASS | 1 required input(s) |
| 6 | primary-format | PASS | A structured review or recommendation that, per finding, na… |
| 7 | mode-output | PASS | every mode states its output |
| 8 | minimum-useful-output | PASS | defined |
| 9 | canonical-owner | PASS | The engineering team and its MCP implementation owners hold… |
| 10 | may-edit-canonical | PASS | false |
| 11 | quality-bar | PASS | 5 evidence-citing checks |
| 12 | forbidden-behaviours | INFO | 3 rules; source traceability delegated to profile-reviewer |
| 13 | no-procedure-in-body | PASS | no ordered procedure detected in body |
| 14 | body-size | WARNING | profile body ~974 words (> 800); 174 over the 800-word budget; heaviest: quality_bar 189w, when_to_use 135w, modes 130w |
| 15 | platform-neutral | PASS | core is platform-neutral |
| 16 | provenance-ledger | PASS | present |
| 17 | no-unresolved-conflict | INFO | conflict resolution review delegated to profile-reviewer / Phase 7 merge log |
| 18 | golden-tests | PASS | 3 golden, 2 negative routing |

## Routing Tests (structural)

**Records validated:** 6/6

| Test ID | Status | Description |
|---------|--------|-------------|
| GT-001 | SCHEMA-OK | Positive routing — task-augmented tools/call, ungated + wrong result channel |
| GT-002 | SCHEMA-OK | Positive routing — host-centered trust and consent for tool invocation |
| GT-003 | SCHEMA-OK | Positive routing — transport choice against the negotiated revision |
| GT-NEG-001 | SCHEMA-OK | Negative routing — production implementation request |
| GT-NEG-002 | SCHEMA-OK | Negative routing — out-of-protocol product/model decision |
| GT-MC-001 | SCHEMA-OK | Missing context — underspecified conformance request |

> Live routing/permission execution requires a Claude invocation; the records above are validated structurally (schema + inventory).
