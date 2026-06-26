# Provenance Ledger — test-driven-development-advisor

## Source pack

| source_id | title | author | year | rights_status | sha256 (short) |
|-----------|-------|--------|------|---------------|----------------|
| kent-beck-test-drive-47a4610a | Test-Driven Development By Example | Kent Beck | 2002 | distillation-only | 47a4610a |

**Rights note.** The source is an authored Addison-Wesley title (ISBN 0-321-14653-0)
carrying copyright with no open license. Classified `distillation-only` (distillation
allowed, no verbatim quotation) per the conservative floor for authored works. The
`quote_scan` gate enforces no verbatim spans; all evidence records set
`quote_allowed: false`.

**Conversion note.** Converted PDF → Markdown via **docling** (`conversion_status=ok`,
252 anchors, 38,655 words). The ingested PDF is a **66-page partial** covering the
**Introduction + Part I (The Money Example, Chapters 1–17, incl. the Money
Retrospective)**. Part II (the xUnit Example) and Part III (Patterns for TDD) are **not
present in this source file**. The package is therefore grounded in the TDD rhythm and
two rules (Introduction), the general cycle and the three get-to-green strategies
(Chapter 2 + Triangulation in Chapter 3), and the worked example — but **not** the
finer Part III pattern catalogue (Child Test, Isolated Test, etc.). This scope limit is
recorded as an `evidence_gap` in the interrogation record.

## Tier + evidence chain

Tier **1** (classify_tier = 1). Evidence chain:

- `sources/maps/kent-beck-test-drive-47a4610a.source-map.yaml` — structure-first map
  (`source-map-v1`): Introduction + Part I hierarchy + 11 provenance-anchored candidate
  units. Validated.
- `analysis/claims.jsonl` (`claims-v1`) — 11 atomic, source-anchored claims (TDD-001…011).
- `evidence/evidence-records.yaml` (`evidence-records-v1`) — one record per claim,
  `quote_allowed: false` throughout.
- `principles/principles.yaml` (`principles-v1`) — 7 operational principles
  (P001, P002, P004, P006, P008, P009, P010), each mapped to profile rules / skills /
  references / tests.
- `analysis/claim-importance-scores.yaml` (`importance-scores-v1`) — 9-dimension scores.

## Q1–Q18 derivation map

| Q | Field | Source basis |
|---|-------|--------------|
| Q1 | display_name / role | Introduction + Part I opener: TDD rhythm, "Readers will learn to…" (h0000, h0001) |
| Q2 | role / modes | Ch.2 general cycle "write a test / make it run / make it right" (h0024) |
| Q3 | when_to_use | Ch.1–2 worked loop; get-to-green strategy choice (h0002, h0024, h0041) |
| Q4 | when_not_to_use | Scope boundary — book teaches the test loop, not architecture/tooling/security |
| Q5 | inputs.required | Implicit in every cycle: a behaviour to specify + code/interface under test |
| Q6 | outputs | Ch.2 deliverable — the next cycle step with rationale (h0024) |
| Q7 | quality_bar | Small steps, quick green then refactor, strategy fit (h0001, h0024) |
| Q8 | handoff / canonical_owner | Developer owns the code and decision; advisor guides the practice |
| Q9 | supported_modes | advise (teaching text), review (cycle critique), compare (3 strategies) |
| Q10 | forbidden_behaviours | Two rules (h0000) + refactor obligation (h0024) |
| Q11 | minimum_useful_output | A single concrete next step in the cycle |
| Q12 | always_on | Cycle + two rules; work/clean split; strategy choice; small increments |
| Q13 | skills | red-green-refactor-cycle, get-to-green-then-refactor, getting-to-green-strategies |
| Q14 | references | tdd-to-do-list |
| Q15 | mcp | none |
| Q16 | caller_supplied | none (inputs are required artifacts, not per-project context) |
| Q17 | source_of_truth | Beck, TDD By Example (2002), Part I + Introduction |
| Q18 | volatility | Low — cycle/rules/strategies stable; framework idioms drift; partial-source caveat |

## Mode evidence

- **advise** — the book is an explicit teaching text ("Readers will learn to… Use
  patterns to decide what tests to write"); recommends/consults on practising TDD.
- **review** — Ch.2 + retrospective evaluate whether work followed the cycle and whether
  duplication was removed → supports critique of an existing change.
- **compare** — the source explicitly contrasts Fake It / Obvious Implementation /
  Triangulation and when to shift between them.

`produce` and `patch-suggest` were **not** assigned — the source teaches a practice and
critiques work; it does not justify generating the developer's production code or issuing
bounded code patches. No `policy/patch-policy.yaml` is required.

## Domain-risk

Non-regulated technical domain → `domain_risk_category` unset; the J-track no-advice
boundary does not apply.

## Faithfulness

`reports/faithfulness-report.yaml` (`faithfulness-report-v1`) — every profile rule
checked against the evidence records; no CONTRADICTED/unsupported findings.

## Review schedule

Annual (`review_cadence: annual`, `volatility: low`). Re-interrogate if the full book
(Parts II–III) is later ingested, which would extend the package toward the Part III
pattern catalogue.

## Version history

- 0.1.0 (2026-06-15) — initial Tier-1 package from the 66-page Part I source.
