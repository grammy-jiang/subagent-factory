# Test Results — agent-skills-advisor

**Generated:** 2026-07-04T11:01:10.938830+00:00

## Phase 8 Profile Self-Check

**Verdict:** PASS

| # | Check | Level | Detail |
|---|-------|-------|--------|
| 1 | slug | PASS | slug 'agent-skills-advisor' is kebab-case and role-based |
| 2 | when-to-use | PASS | 5 triggers |
| 3 | when-not-to-use | PASS | 3 exclusions |
| 4 | modes-evidence | INFO | mode source-evidence traceability delegated to profile-reviewer |
| 5 | inputs-required | PASS | 1 required input(s) |
| 6 | primary-format | PASS | A prioritized set of recommendations, each naming the specif |
| 7 | mode-output | PASS | every mode states its output |
| 8 | minimum-useful-output | PASS | defined |
| 9 | canonical-owner | PASS | Fifty-seven ingested primary and secondary sources on Agent  |
| 10 | may-edit-canonical | PASS | false |
| 11 | quality-bar | PASS | 5 evidence-citing checks |
| 12 | forbidden-behaviours | INFO | 5 rules; source traceability delegated to profile-reviewer |
| 13 | no-procedure-in-body | PASS | no ordered procedure detected in body |
| 14 | body-size | PASS | ~704 words |
| 15 | platform-neutral | PASS | core is platform-neutral |
| 16 | provenance-ledger | PASS | present |
| 17 | no-unresolved-conflict | INFO | conflict resolution review delegated to profile-reviewer / Phase 7 merge log |
| 18 | golden-tests | PASS | 10 golden, 3 negative routing |

## Routing Tests (structural)

**Records validated:** 16/16

| Test ID | Status | Description |
|---------|--------|-------------|
| GT-001 | SCHEMA-OK | Positive — author a lean SKILL.md with progressive disclosure |
| GT-002 | SCHEMA-OK | Positive — write the description for reliable triggering |
| GT-003 | SCHEMA-OK | Positive — deploy a skill to a target surface with the right permissions |
| GT-004 | SCHEMA-OK | Positive — prove a skill helps with a baseline comparison |
| GT-005 | SCHEMA-OK | Positive — choose between a skill, a subagent, and an MCP server |
| GT-006 | SCHEMA-OK | Positive — bundle a deterministic script instead of generating code |
| GT-007 | SCHEMA-OK | Positive — review an existing skill folder layout |
| GT-008 | SCHEMA-OK | Positive — keep a skill portable across platforms |
| GT-009 | SCHEMA-OK | Positive — a pre-deploy three-class test matrix |
| GT-010 | SCHEMA-OK | Positive — treat a third-party skill as untrusted |
| NR-001 | SCHEMA-OK | Negative — write the production feature, not the skill |
| NR-002 | SCHEMA-OK | Negative — product/UI design out of scope |
| NR-003 | SCHEMA-OK | Negative — cluster infrastructure out of scope |
| MC-001 | SCHEMA-OK | Missing context — which surface and current file |
| MC-002 | SCHEMA-OK | Missing context — deploy target unspecified |
| MC-003 | SCHEMA-OK | Missing context — no eval criteria |

> Live routing/permission execution requires a Claude invocation; the records above are validated structurally (schema + inventory).
