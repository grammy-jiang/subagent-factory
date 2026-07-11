# Test Results — employee-payment-scheme-advisor

**Generated:** 2026-06-12T12:04:12.561847+00:00

## Phase 8 Profile Self-Check

**Verdict:** WARNING

| # | Check | Level | Detail |
|---|-------|-------|--------|
| 1 | slug | PASS | slug 'employee-payment-scheme-advisor' is kebab-case and role-based |
| 2 | when-to-use | PASS | 5 triggers |
| 3 | when-not-to-use | PASS | 3 exclusions |
| 4 | modes-evidence | INFO | mode source-evidence traceability delegated to profile-reviewer |
| 5 | inputs-required | PASS | 2 required input(s) |
| 6 | primary-format | PASS | A reasoned set of evidence-grounded recommendations and guid |
| 7 | mode-output | PASS | every mode states its output |
| 8 | minimum-useful-output | PASS | defined |
| 9 | canonical-owner | PASS | The managers and management team responsible for the organis |
| 10 | may-edit-canonical | PASS | false |
| 11 | quality-bar | PASS | 5 evidence-citing checks |
| 12 | forbidden-behaviours | INFO | 5 rules; source traceability delegated to profile-reviewer |
| 13 | no-procedure-in-body | PASS | no ordered procedure detected in body |
| 14 | body-size | WARNING | profile body ~861 words (> 800); 61 over the 800-word budget; heaviest: quality_bar 156w, when_to_use 150w, forbidden_behaviours 143w |
| 15 | platform-neutral | PASS | core is platform-neutral |
| 16 | provenance-ledger | PASS | present |
| 17 | no-unresolved-conflict | INFO | conflict resolution review delegated to profile-reviewer / Phase 7 merge log |
| 18 | golden-tests | PASS | 3 golden, 2 negative routing |

## Routing Tests (structural)

**Records validated:** 6/6

| Test ID | Status | Description |
|---------|--------|-------------|
| GT-001 | SCHEMA-OK | Positive routing — advise mode (how to design an incentive scheme through participation) |
| GT-002 | SCHEMA-OK | Positive routing — review mode (existing scheme underperformed; scheme modification/subversion failure mode) |
| GT-003 | SCHEMA-OK | Positive routing — validate mode (check a proposed scheme against success criteria before site-wide extension) |
| NR-001 | SCHEMA-OK | Negative routing — technical/financial payment-processing system (the role-inference trap) |
| NR-002 | SCHEMA-OK | Negative routing — collective-bargaining dispute (source assigns to negotiation channels, not participative team design) |
| MC-001 | SCHEMA-OK | Missing required input — request with no scheme description or organisation context |

> Live routing/permission execution requires a Claude invocation; the records above are validated structurally (schema + inventory).
