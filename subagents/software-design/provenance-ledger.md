# Provenance Ledger — Software Design Reviewer

**Subagent slug:** `software-design`
**Profile version:** 0.1.0
**Tier:** 2 (multi-source, five long canonical books)
**Last updated:** 2026-06-20
**Originally generated:** 2026-06-20

---

## Source Registry

| ID | Title | Author | Year | Authority | Rights | Volatility | Review cadence |
|----|-------|--------|------|-----------|--------|------------|----------------|
| a-philosophy-of-soft-5e67c59e | A Philosophy of Software Design | John Ousterhout | 2018 | secondary | distillation-only | low | annual |
| code-simplicity-the-aca1f344 | Code Simplicity: The Fundamentals of Software | Max Kanat-Alexander | 2012 | secondary | distillation-only | low | annual |
| clean-code-a-handboo-5b1b9ca3 | Clean Code: A Handbook of Agile Software Craftsmanship | Robert C. Martin | 2008 | secondary | distillation-only | low | annual |
| martin-fowler-refact-0574f24e | Refactoring: Improving the Design of Existing Code | Martin Fowler | 2018 | secondary | distillation-only | low | annual |
| erich-gamma-richard-80cb534a | Design Patterns: Elements of Reusable Object-Oriented Software | Gamma, Helm, Johnson, Vlissides | 1994 | secondary | distillation-only | low | annual |

**Source-pack note — rights:** All five sources carry `rights_status: distillation-only`.
Each is a commercially published, copyrighted book with **no explicit open-source or
Creative Commons license notice** in its front matter. The classification is the
conservative default-copyright floor for an authored work (per
`.claude/rules/rights-and-quotation-policy.md`): distillation (paraphrase / synthesis)
is permitted; **verbatim quotation is prohibited** throughout all generated artifacts.
No `quote_allowed: true` evidence record exists; every evidence record sets
`quote_allowed: false`. The package is checked with `quote_scan`.

**Source-pack note — close existing match / new-slug justification:** the embedding search
and an sha256 view both surface sibling packages in this domain — `software-design-reviewer`
(A Philosophy of Software Design alone), `software-simplicity-advisor` (Code Simplicity
alone) and `software-design-simplicity-advisor` (the two fused). This package was authored
under the explicitly-supplied `--slug software-design` because its expert role is genuinely
broader and distinct: a **five-canon fusion reviewer** that unifies Ousterhout's complexity
model, Kanat-Alexander's Equation/three-flaws, Martin's clean-code rules, Fowler's code
smells + behaviour-preserving refactoring, and the Gang-of-Four interface/composition
decoupling into one design-review discipline. The sources here are fresh ingests under the
`software-design` slug (their own `source_id`s and heading anchors); no artifact is shared
with the sibling packages.

---

## Distillation Log

| Field | Source IDs | QIDs | Notes |
|-------|-----------|------|-------|
| `slug` | — | Q1 | User-supplied `--slug software-design`; kebab-case |
| `display_name` / `role` | all five | Q1, Q2 | Fusion reviewer role inferred from content, not filenames |
| `when_to_use` | OUST, CS, CC, REF, GoF | Q3 | 5 triggers, each traced to ≥1 canon |
| `when_not_to_use` | OUST Ch20; CS Ch2 | Q4 | Performance tuning, roadmap, debugging, UI aesthetics |
| `inputs.required` | all five | Q5 | Artefact + present requirements + lifetime |
| `outputs.primary_format` / `modes` | all five | Q6, Q9 | review / advise / compare / validate / patch-suggest |
| `quality_bar` | promoted principles | Q7 | Cites PRC-001/002/007/012/013/023 |
| `handoff_rules` / `canonical_owner` | all five | Q8 | Owner = engineer / tech lead of the code |
| `minimum_useful_output` | all five | Q11 | One costly flaw + bounded fix + verdict |
| `forbidden_behaviours` | promoted principles | Q10 | Cites PRC-005/007/012; Q4; rights policy |
| `knowledge_partition.always_on` | promoted principles | Q12 | 8 always-on rules, all PRC-cited |
| `knowledge_partition.skills` | OUST/CS/CC/REF/GoF | Q13 | 8 skill stubs |
| `knowledge_partition.references` | OUST/REF/CC/CS/GoF | Q14 | 5 reference stubs (catalogues) |
| `source_of_truth_policy.precedence` | all five | Q17 | Five co-equal canons; tension logged |

---

## Tier-2 Evidence Chain (Step 6.5 / 7.7)

| Artifact | Path | Count | Validator |
|----------|------|-------|-----------|
| Atomic claims | `analysis/claims.jsonl` | 82 | `validate_claims` (PASS) |
| Importance scores | `analysis/claim-importance-scores.yaml` | 82 | `cli score` (52 keep / 30 review / 0 invalid) |
| Evidence records | `evidence/evidence-records.yaml` | 82 | `validate_evidence_records` (PASS) |
| Principles | `principles/principles.yaml` | 26 | `validate_principles` (PASS) |
| Cross-source clusters | `principles/principle-clusters.json` | 6 | `validate_principle_clusters` (PASS) |
| Principle graph | `principles/principle-graph.json` | 20 edges | `validate_principle_graph` (PASS) |
| Faithfulness report | `reports/faithfulness-report.yaml` | per-rule | `validate_faithfulness_report` |
| Behaviour tests | `tests/principle-behaviour-tests.yaml` | per-principle | `validate_principle_test_coverage` |

Claims are anchored to real heading anchor IDs from each source's anchor index. Every
claim referenced by a principle carries an evidence record (`quote_allowed: false`).
Claims span all five `source_id`s (OUST 25, CS 17, CC 14, REF 16, GoF 10).

### Cross-source synthesis & one logged conflict

Principles fuse claims across sources (e.g. PRC-009 DRY draws on Code Simplicity,
Refactoring **and** A Philosophy of Software Design; PRC-017 comments draws on
Ousterhout, Martin and Fowler). One genuine tension is **retained, not dropped**:

- **C-01** — Ousterhout's "make modules somewhat general-purpose" (**PRC-026**) vs.
  Kanat-Alexander's "be only as generic as you need right now" (**PRC-007**). Reconciled
  by scope (generalise interface *shape* for a present family of needs; never add generic
  *functionality* for an imagined future). See `principles/conflict-log.md` and the
  `conflicts` edge PRC-026→PRC-007 in `principles/principle-graph.json`.

---

## Faithfulness

Tier-2 faithfulness compares each profile rule against `evidence/evidence-records.yaml`.
No rule is stronger than its evidence; hedged source claims (e.g. "somewhat
general-purpose", performance heuristics) are kept hedged. Report:
`reports/faithfulness-report.yaml`. No `CONTRADICTED` or `unsupported` findings.

---

## Version History

### 1.0.0 — 2026-06-24
- **Calibrated 0.25x rebuild + modernization.** Rebuilt the distilled spine with
  `build_map_reduce --select 0.25` over the cached per-book MAP (zero re-extraction):
  134 → **34 principles** (886 claims, 291 evidence). Regrounded the authored layer onto the
  new spine by remapping principle citations (survivors keep ids; 100 dropped ids → nearest
  survivor by similarity + curated overrides); skill/reference bodies unchanged.
- Added Step-16 GRADE confidence blocks (34/34 consistent), Step-13 ask-gate
  (`applies_when` cues on all 34 + behaviour suite with answerable twins), and Step-7 C-track
  (4 cross-source clusters, 18-edge principle graph, 1 resolved conflict).
- `validate_generated_package`: PASS. Adapter re-exported. Supersedes 0.3.x (no prior decision
  removed; the 100 dropped principles remain recoverable from the cached MAP pool).

### 0.1.0 — 2026-06-20
- Initial generation. Five-source Tier-2 fusion package authored from Ousterhout,
  Kanat-Alexander, Martin, Fowler, and Gamma et al. Full evidence chain (claims →
  evidence → principles → clusters → graph), profile with 5 modes, faithfulness report,
  golden + principle-behaviour tests. Status: `draft` (skill/reference bodies remain
  stubs; run Step 8.7 `--author-skills` to promote to `ready`).
