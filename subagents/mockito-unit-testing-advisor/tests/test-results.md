# Test Results — mockito-unit-testing-advisor

**Generated:** 2026-06-10T17:09:18.110816+00:00

## Phase 8 Profile Self-Check

**Verdict:** PASS

| # | Check | Level | Detail |
|---|-------|-------|--------|
| 1 | slug | PASS | slug 'mockito-unit-testing-advisor' is kebab-case and role-based |
| 2 | when-to-use | PASS | 5 triggers |
| 3 | when-not-to-use | PASS | 3 exclusions |
| 4 | modes-evidence | INFO | mode source-evidence traceability delegated to profile-reviewer |
| 5 | inputs-required | PASS | 2 required input(s) |
| 6 | primary-format | PASS | Annotated JUnit 4 test class (@RunWith, @Mock fields, @Befor |
| 7 | mode-output | PASS | every mode states its output |
| 8 | minimum-useful-output | PASS | defined |
| 9 | canonical-owner | PASS | Developer who owns the class under test; official Mockito do |
| 10 | may-edit-canonical | PASS | false |
| 11 | quality-bar | PASS | 5 evidence-citing checks |
| 12 | forbidden-behaviours | INFO | 5 rules; source traceability delegated to profile-reviewer |
| 13 | no-procedure-in-body | PASS | no ordered procedure detected in body |
| 14 | body-size | PASS | ~760 words |
| 15 | platform-neutral | PASS | core is platform-neutral |
| 16 | provenance-ledger | PASS | present |
| 17 | no-unresolved-conflict | INFO | conflict resolution review delegated to profile-reviewer / Phase 7 merge log |
| 18 | golden-tests | PASS | 3 golden, 1 negative routing |

## Routing Tests (structural)

**Records validated:** 4/4

| Test ID | Status | Description |
|---------|--------|-------------|
| GT-001 | SCHEMA-OK | Produce mode — generate a unit test for a Spring service with a mocked DAO. |
| GT-002 | SCHEMA-OK | Advise mode — explain how to verify a void method call with ArgumentCaptor. |
| GT-004 | SCHEMA-OK | Review mode — identify anti-pattern where integration test is submitted as a unit test. |
| GT-003 | SCHEMA-OK | Negative routing — request to mock a final class with plain Mockito. |

> Live routing/permission execution requires a Claude invocation; the records above are validated structurally (schema + inventory).
