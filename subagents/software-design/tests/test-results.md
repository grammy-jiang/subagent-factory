# Test Results — software-design

**Generated:** 2026-06-24 (calibrated 0.25x rebuild, v1.0.0)

## Phase 8 Profile Self-Check

**Verdict:** PASS

| # | Check | Level | Detail |
|---|-------|-------|--------|
| 1 | slug | PASS | slug 'software-design' is kebab-case and role-based |
| 2 | when-to-use | PASS | 5 triggers |
| 3 | when-not-to-use | PASS | 4 exclusions |
| 4 | modes-evidence | INFO | mode source-evidence traceability delegated to profile-reviewer |
| 5 | inputs-required | PASS | 1 required input(s) |
| 6 | primary-format | PASS | A structured design critique: the most costly red flags or c |
| 7 | mode-output | PASS | every mode states its output |
| 8 | minimum-useful-output | PASS | defined |
| 9 | canonical-owner | PASS | The individual engineer or tech lead who owns the affected d |
| 10 | may-edit-canonical | PASS | false |
| 11 | quality-bar | PASS | 5 evidence-citing checks |
| 12 | forbidden-behaviours | INFO | 5 rules; source traceability delegated to profile-reviewer |
| 13 | no-procedure-in-body | PASS | no ordered procedure detected in body |
| 14 | body-size | PASS | ~798 words |
| 15 | platform-neutral | PASS | core is platform-neutral |
| 16 | provenance-ledger | PASS | present |
| 17 | no-unresolved-conflict | INFO | conflict resolution review delegated to profile-reviewer / Phase 7 merge log |
| 18 | golden-tests | PASS | 73 golden, 2 negative routing (across golden-tests + behaviour-tests) |

## Test inventory

Built from the calibrated 0.25x spine (34 principles, all confidence-graded).

| Suite | File | Counts |
|-------|------|--------|
| Hand-authored golden | `golden-tests.yaml` | 5 golden, 2 negative-routing, 1 missing-context |
| Ask-gate behaviour (Step-13) | `behaviour-tests.yaml` | 68 golden (incl. 34 answerable twins), 34 missing-context |
| Principle behaviour (Step-5) | `principle-behaviour-tests.yaml` | 34 (one per surviving principle) |

Each of the 34 principles is exercised by a principle-behaviour test and an
ask-gate missing-context test paired with an answerable twin (over-ask guard).

## Faithfulness (Step-3)

`reports/faithfulness-report.yaml` — 25 findings, all ≤ source support:
6 EXACT_SUPPORT, 19 WITHIN_SCOPE, 0 over-claims. `quote_scan`: PASS
(no verbatim quotation; sources are distillation-only).

## Routing Tests (structural)

**Records validated:** 8/8

| Test ID | Status | Description |
|---------|--------|-------------|
| GT-001 | SCHEMA-OK | Positive routing — review mode. A shallow class with a complex interface relative to its functionality. |
| GT-002 | SCHEMA-OK | Positive routing — compare mode (design it twice). |
| GT-003 | SCHEMA-OK | Positive routing — review mode for code smells + refactoring. |
| GT-004 | SCHEMA-OK | Positive routing — advise mode for decoupling. |
| GT-005 | SCHEMA-OK | Positive routing — validate mode. |
| NR-001 | SCHEMA-OK | Out of scope — pure runtime performance tuning with no structural-design question. |
| NR-002 | SCHEMA-OK | Out of scope — product/business roadmap decision (what to build, not how). |
| MC-001 | SCHEMA-OK | Underspecified — a design-review request with no artefact or requirements attached. |

> Live routing/permission execution requires a Claude invocation; the records above are validated structurally (schema + inventory).
