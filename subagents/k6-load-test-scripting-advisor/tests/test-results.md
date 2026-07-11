# Test Results — k6-load-test-scripting-advisor

**Generated:** 2026-06-12T11:41:35.301518+00:00

## Phase 8 Profile Self-Check

**Verdict:** WARNING

| # | Check | Level | Detail |
|---|-------|-------|--------|
| 1 | slug | PASS | slug 'k6-load-test-scripting-advisor' is kebab-case and role-based |
| 2 | when-to-use | PASS | 5 triggers |
| 3 | when-not-to-use | PASS | 3 exclusions |
| 4 | modes-evidence | INFO | mode source-evidence traceability delegated to profile-reviewer |
| 5 | inputs-required | PASS | 1 required input(s) |
| 6 | primary-format | PASS | A written explanation and recommendation naming the correct  |
| 7 | mode-output | PASS | every mode states its output |
| 8 | minimum-useful-output | PASS | defined |
| 9 | canonical-owner | PASS | The engineer or tester who owns the k6 test script and execu |
| 10 | may-edit-canonical | PASS | false |
| 11 | quality-bar | PASS | 4 evidence-citing checks |
| 12 | forbidden-behaviours | INFO | 3 rules; source traceability delegated to profile-reviewer |
| 13 | no-procedure-in-body | PASS | no ordered procedure detected in body |
| 14 | body-size | WARNING | profile body ~806 words (> 800); 6 over the 800-word budget; heaviest: quality_bar 154w, when_to_use 139w, modes 135w |
| 15 | platform-neutral | PASS | core is platform-neutral |
| 16 | provenance-ledger | PASS | present |
| 17 | no-unresolved-conflict | INFO | conflict resolution review delegated to profile-reviewer / Phase 7 merge log |
| 18 | golden-tests | PASS | 3 golden, 1 negative routing |

## Routing Tests (structural)

**Records validated:** 5/5

| Test ID | Status | Description |
|---------|--------|-------------|
| GT-001 | SCHEMA-OK | Positive routing — advise mode: shape a ramping load profile in the k6 options object. |
| GT-002 | SCHEMA-OK | Positive routing — compare mode: checks vs thresholds for pass/fail. |
| GT-003 | SCHEMA-OK | Positive routing — advise mode: which metric type for a measurement. |
| NR-001 | SCHEMA-OK | Negative routing — cross-tool comparison is out of scope for a k6-only source. |
| MC-001 | SCHEMA-OK | Missing required input — no script fragment or load behaviour provided. |

> Live routing/permission execution requires a Claude invocation; the records above are validated structurally (schema + inventory).
