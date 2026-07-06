# Test Results — product-blueprint-reviewer

**Generated:** 2026-07-06T00:50:11.869927+00:00

## Phase 8 Profile Self-Check

**Verdict:** WARNING

| # | Check | Level | Detail |
|---|-------|-------|--------|
| 1 | slug | PASS | slug 'product-blueprint-reviewer' is kebab-case and role-based |
| 2 | when-to-use | PASS | 5 triggers |
| 3 | when-not-to-use | PASS | 3 exclusions |
| 4 | modes-evidence | INFO | mode source-evidence traceability delegated to profile-reviewer |
| 5 | inputs-required | PASS | 1 required input(s) |
| 6 | primary-format | PASS | A structured blueprint critique that names the outcome at s… |
| 7 | mode-output | PASS | every mode states its output |
| 8 | minimum-useful-output | PASS | defined |
| 9 | canonical-owner | PASS | The product team and its leadership hold final authority ov… |
| 10 | may-edit-canonical | PASS | false |
| 11 | quality-bar | PASS | 5 evidence-citing checks |
| 12 | forbidden-behaviours | INFO | 3 rules; source traceability delegated to profile-reviewer |
| 13 | no-procedure-in-body | PASS | no ordered procedure detected in body |
| 14 | body-size | WARNING | profile body ~930 words (> 800); 130 over the 800-word budget; heaviest: quality_bar 152w, modes 151w, when_to_use 133w |
| 15 | platform-neutral | PASS | core is platform-neutral |
| 16 | provenance-ledger | PASS | present |
| 17 | no-unresolved-conflict | INFO | conflict resolution review delegated to profile-reviewer / Phase 7 merge log |
| 18 | golden-tests | PASS | 8 golden, 3 negative routing |

## Routing Tests (structural)

**Records validated:** 15/15

| Test ID | Status | Description |
|---------|--------|-------------|
| GT-001 | SCHEMA-OK | Positive routing — blueprint leaks technology and vendor names |
| GT-002 | SCHEMA-OK | Positive routing — blueprint thinks in outputs, not outcomes |
| GT-003 | SCHEMA-OK | Positive routing — academic gap folded into MVP-0 |
| GT-004 | SCHEMA-OK | Positive routing — hypotheses are sprawling and untested |
| GT-005 | SCHEMA-OK | Positive routing — downstream routing is unevidenced |
| GT-006 | SCHEMA-OK | Positive routing — interaction modes and AI Skill vs MCP unclassified |
| GT-007 | SCHEMA-OK | Positive routing — capability with no evidence trace |
| GT-008 | SCHEMA-OK | Positive routing — compare two MVP-0 boundaries |
| NR-001 | SCHEMA-OK | Out of scope — write the downstream architecture, stack, and code |
| NR-002 | SCHEMA-OK | Out of scope — more literature research / second summary |
| NR-003 | SCHEMA-OK | Out of scope — legal / HR decision |
| MC-001 | SCHEMA-OK | Underspecified — review request with no artifact |
| MC-002 | SCHEMA-OK | Underspecified — MVP scope question with no outcome or evidence |
| MC-003 | SCHEMA-OK | Underspecified — routing question with no risk signals |
| MC-004 | SCHEMA-OK | Underspecified — vague product-experience help |

> Live routing/permission execution requires a Claude invocation; the records above are validated structurally (schema + inventory).
