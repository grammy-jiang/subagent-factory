# Provenance Ledger — Python Code Reviewer

**Subagent slug:** `python-reviewer`
**Profile version:** 0.1.0
**Generated:** 2026-06-20
**Tier:** 2 (multi-source, content-dense)

---

## Source Registry

| ID | Title | Author | Year | Authority | Rights | Volatility | Review cadence |
|----|-------|--------|------|-----------|--------|------------|----------------|
| luciano-ramalho-flue-ca307a52 | Fluent Python: Clear, Concise, and Effective Programming (2nd ed.) | Luciano Ramalho | 2022 | high (O'Reilly, widely-cited idiomatic-Python reference) | distillation-only | low (language idioms are stable) | 24 months |
| python-distilled-pea-1baf485f | Python Distilled | David M. Beazley | 2021 | high (Addison-Wesley/Pearson, curated core-language reference) | distillation-only | low | 24 months |

**Rights note.** Both sources are authored, copyrighted books with an explicit
"All rights reserved" notice (Fluent Python © 2022 O'Reilly; Python Distilled
© 2022 Pearson) and **no open-license grant**. Per
`.claude/rules/rights-and-quotation-policy.md` the safe floor is
`distillation-only`: distillation and paraphrase are allowed, **verbatim
quotation is not**. All evidence records carry `quote_allowed: false` and every
generated statement is a paraphrase.

---

## Distillation Log

| Field | Source IDs | QIDs | Notes |
|-------|-----------|------|-------|
| `role` / `display_name` | both | Q1, Q2 | Inferred from content: a Python code reviewer for idiomatic correctness and Pythonic design. Both books teach reviewing/critiquing code against the data model, OOP design, and language semantics. |
| `when_to_use` | both | Q3 | Idiomatic-review, error-prone-pattern, approach-comparison, resource/exception-gating, minimal-fix triggers. |
| `when_not_to_use` | both | Q4 | Runtime/algorithmic perf, non-Python, defect debugging, product/architecture scope. |
| `inputs.required` | both | Q5 | The Python code under review plus purpose and constraints. |
| `outputs.modes` | both | Q6, Q9 | `review` (code-smell/"bad idea" critique), `advise`, `compare` (inheritance vs composition; listcomp vs loop), `validate` (idiom checklist gate), `patch-suggest` (before/after fixes such as HauntedBus→None, udict→UserDict). |
| `quality_bar` | both | Q7 | Falsifiable checks grounded in principles P01–P15. |
| `forbidden_behaviours` | both | Q10 | No verbatim quotation (distillation-only), no ungrounded rule, no silent patch, preserve hedges, stay in Python-idiom scope. |
| `handoff_rules` / `canonical_owner` | both | Q8, Q17 | Code owner holds the decision; larger redesigns go to a design discussion. |
| `knowledge_partition.always_on` | both | Q12 | Eight distilled cross-cutting rules folding all 15 principles. |
| `knowledge_partition.skills` | both | Q13 | Ten review activities (stubs). |
| `knowledge_partition.references` | both | Q14 | `pythonic-review-checklist`, `python-special-methods-reference` (stubs). |
| `source_of_truth_policy.precedence` | both | Q8, Q17 | Ramalho governs data model / sequences / mutability; Beazley governs core semantics / OOP / resources / exceptions; co-equal, overlaps strengthen, documented language behaviour breaks ties. |

Full atomic provenance lives in `analysis/claims.jsonl` (18 claims, each
source-anchored), `evidence/evidence-records.yaml` (18 records), and
`principles/principles.yaml` (15 operational principles P01–P15).

---

## Process notes

- **Multi-source authoring.** Both sources were ingested into the **one** package
  so the reviewer is grounded in a blend of the two canonical Python references.
  Their overlap (mutable defaults, composition over inheritance, protocols)
  strengthens the shared rules; complementary coverage (Ramalho's data model;
  Beazley's exception and resource discipline) widens the review surface.
- **Source-structure-mapping (Step 6.5-pre) skipped.** Per the
  `source-structure-mapping` skill ("skip when mapping adds no value") and the
  precedent of other book-based packages, claims were extracted from targeted,
  provenance-anchored reads of the high-value review sections rather than a full
  structural map of two ~600-page books. Anchors are real heading/code-block
  anchor IDs at section granularity; referential integrity is enforced by
  `validate_claims` / `validate_evidence_records`.
- **In-thread evidence chain.** Interrogation, claim extraction, principle
  promotion, faithfulness review, and behaviour-test generation were performed
  in-thread (headless run; the spawn-stall caution in `author-subagent` Step 6.5
  applies). The deterministic `selfcheck` / `validate` gates are the authority on
  correctness.

---

## Generated Artifacts

| Artifact | Type | Path |
|----------|------|------|
| profile.yaml | canonical profile | `subagents/python-reviewer/profile.yaml` |
| claims | evidence | `subagents/python-reviewer/analysis/claims.jsonl` |
| importance scores | evidence | `subagents/python-reviewer/analysis/claim-importance-scores.yaml` |
| evidence records | evidence | `subagents/python-reviewer/evidence/evidence-records.yaml` |
| principles | operational | `subagents/python-reviewer/principles/principles.yaml` |
| faithfulness report | review | `subagents/python-reviewer/reports/faithfulness-report.yaml` |
| golden tests | tests | `subagents/python-reviewer/tests/golden-tests.yaml` |
| principle-behaviour tests | tests | `subagents/python-reviewer/tests/principle-behaviour-tests.yaml` |
| patch policy | policy | `subagents/python-reviewer/policy/patch-policy.yaml` |

Ten skill stubs and two reference stubs are scaffolded under `skills/` and
`references/` (STATUS: STUB — package is `status: draft`).

---

## Version History

- **0.3.2** (2026-07-25) — Added `router_description` to `profile.yaml`. The adapter frontmatter `description` is the string the runtime routes on; without this field the exporter composed it from the role plus only the first two `when_to_use` triggers and the first `when_not_to_use` exclusion, dropping the remaining domains from the routing signal. The authored description states the full remit and the advice-only boundary; adapter re-exported. No principle, rule, skill, or source changed — no prior profile decision is superseded.

| Version | Date | Changes | Sources involved |
|---------|------|---------|-----------------|
| 0.1.0 | 2026-06-20 | Initial multi-source generation (Tier 2). | luciano-ramalho-flue-ca307a52, python-distilled-pea-1baf485f |

---

## Open Questions

- Skill and reference bodies remain stubs; promote to `status: ready` via Step 8.7
  when their bodies are authored.

---

## Conflict Log

_No cross-source conflicts recorded. The two references agree on the shared
rules (mutable defaults, composition over inheritance, duck typing); their
coverage is otherwise complementary._
