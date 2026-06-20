# Research Run Summary — Cross-Document Knowledge Fusion & Contradiction Detection

## 1. Final report

`cross-document-knowledge-fusion-and-contradiction-detection-for-merging-expert-principles-distilled-from-multiple-source-documents-research-report.md`

Validation: **PASS, score 1.00** (no issues). Built from a **real cross-paper synthesis** over
**27 analyzed papers** (19 prior + 8 round-4 injected). The earlier degraded report (template
fallback) is snapshot-preserved as `…-research-report.2026-06-20.md`; the round-1 snapshot remains
`…-research-report.2026-06-13.md`.

**What was fixed (JOB A).** The prior top-level report rendered in template-fallback (62 `structured
LLM extraction` placeholders, a `not_reported` Evidence Matrix, ~342 auto `CON-###` negation-spam
lines, empty Assumption/Operational/Design sections). Root cause: the 19 per-paper `analysis/*.json`
(paper-analyzer) were rich and real, but the CLI `summarize`/`report` stages had no LLM backend and
fell back. Fix: drove the `paper-synthesizer` sub-agent over the real analyses to produce a genuine
`analysis/synthesis.json` + `synthesis.md` (18 findings, 6 substantive contradictions, 8 classified
gaps, 0 placeholders), then authored the final report from it. Forbidden-content check on the final
report: `structured LLM extraction` = 0, `not_reported` = 0, `CON-###` = 0.

## 2. Round History

| Round | Run ID | Topic / Gap Focus | New Papers | Gaps Addressed | Remaining | Outcome |
|-------|--------|-------------------|------------|----------------|-----------|---------|
| 1 | 57e857a93e69 | Original topic (deep profile, 6-sub-area sweep) | 19 | Initial shortlist; 8 gaps classified | G1,G3 HIGH; G4,G6,G8 MED; G2 HIGH/G5 MED eng; G7 OOS | Complete; validated PASS 0.83 |
| 2 | round2-g3 | G3 — cross-doc NLI/stance/knowledge-conflict (academic HIGH) | 0 | none | G1, G3 | **no_new_papers** — 103 cands all ~2026; arXiv recency-locked |
| 3 | round3-g1 | G1 — normative/subjective truth discovery + belief merging (academic HIGH) | 0 | none | G1, G3 | **no_new_papers** — 186 cands (181×2026); arXiv recency-locked |
| 4 | 57e857a93e69-r4 | **G1+G3 foundational arXiv-ID injection** (recency-lock workaround) | 8 | **G1, G3, G8 reclassified ACADEMIC LOW w/ citations** | G4, G6 (MED) | **Converged at 4-round hard cap**; report PASS 1.00 |

**Round-4 mechanism (JOB B).** The pipeline arXiv *search* is recency-locked to ~2026, so rounds 2–3
found 0 foundational papers. Round 4 bypassed search by injecting **8 foundational papers by arXiv
ID** (direct ID fetch is not recency-locked). Every ID was **verified** to resolve to the real paper
(title+authors confirmed via arxiv.org/abs; all 8 also resolved in Semantic Scholar during
`expand --paper-ids`, which fetched 595 related papers). The 8 were downloaded, converted (docling),
and analyzed by `paper-analyzer` sub-agents so they carry **real structured extraction**, then
integrated by the synthesizer.

**Injected papers**
- **G3** (cross-document contradiction across independent docs): `2106.09449` DocNLI; `1906.03538`
  PERSPECTRUM (cross-source SUPPORT/UNDERMINE stance + perspective-equivalence clustering);
  `2109.05052` Entity-Based Knowledge Conflicts; `2103.08541` VitaminC (contrastive 3-way verification);
  `2403.08319` Knowledge Conflicts for LLMs: A Survey (inter-context conflict taxonomy + benchmarks).
- **G1 / G8** (normative reconciliation + logical belief merging): `2404.10271` Social Choice Should
  Guide AI Alignment (preference aggregation; impossibility results); `1404.6445` Belief merging within
  fragments of propositional logic (IC operators under constraints); `2112.13557` AGM Belief Revision,
  Semantically (minimal-change revision).

## 3. Remaining open gaps

| ID | Classification | Severity | Why still open |
|----|----------------|----------|----------------|
| **G4** | ACADEMIC | MEDIUM | Deterministic-vs-LLM cost/quality crossover is asserted from method structure, never measured; needs an ablation benchmark to budget LLM spend across the three operations. |
| **G6** | ACADEMIC | MEDIUM | Copy-aware source weighting (1503.00310) + metric disagreement (1509.04238) validated only on factual/ER corpora; transfer to LLM-distilled normative principles unproven (distillation may itself homogenize phrasing and manufacture false corroboration). |
| G1 | ACADEMIC | LOW (was HIGH) | **Reclassified/closed-foundation:** social-choice + AGM/IC belief merging foundations injected (2404.10271, 1404.6445, 2112.13557). Residual = applied/empirical (instantiate on NL principles; no eval yet). |
| G3 | ACADEMIC | LOW (was HIGH) | **Reclassified/closed-method:** DocNLI + cross-source stance + contrastive verification + survey injected. Residual = no eval on distilled-from-books principles; data largely synthetic/claim-anchored. |
| G8 | ACADEMIC | LOW (was MED) | **Reclassified:** logical belief merging/revision injected (1404.6445, 2112.13557). Residual = tractable NL/description-logic instantiation. |
| G2 | ENGINEERING | LOW | **Resolved inline** — explicit inter-stage artifact contracts in report. |
| G5 | ENGINEERING | LOW | **Resolved inline** — incremental centroid assignment + periodic recompute + held-out threshold calibration. |
| G7 | OUT_OF_SCOPE | LOW | Closed — ECB+-only generalization is a benchmarking concern outside the cross-source merge question. |

Both HIGH academic gaps (G1, G3) that blocked the prior run are now **closed on the method/foundation
side with citations to injected papers**. The only genuinely-open gaps (G4, G6) are MEDIUM-severity
*measurement* gaps, not blockers. The decisive residual risk is **empirical**: no paper in the corpus
evaluates on expert principles distilled from books, so all transfer is analogical and must be
re-validated in-the-wild.

## 4. Findings most relevant to the downstream use (Step-7 multi-source synthesis = ALIGN/DEDUP → DETECT-CONTRADICTION → RECONCILE)

1. **Build each operation as deterministic recall → LLM precision.** Recall-then-filter is the
   convergent architecture: deterministic normalize + multi-key (ensemble) blocking + dense/FAISS
   centroid retrieval proposes candidates; a transformer/LLM filter only confirms/re-weights (never
   invents links). The recall stage must be tuned for recall — the filter can't recover a missed
   equivalence. — **2109.07401, 2603.24246, 2106.01210, 2104.08413, 1609.06265**.
2. **Detect cross-document contradiction with a 3-way SUPPORTS/REFUTES/NEI stance head, not a bare LLM.**
   Assemble document-level NLI (DocNLI) + claim-anchored SUPPORT/UNDERMINE stance & equivalence
   clustering (PERSPECTRUM) + contrastive verification (VitaminC); keep "contradiction" distinct from
   "neutral". This closes the **G3 method side**. — **2106.09449, 1906.03538, 2103.08541, 2403.08319**.
3. **Off-the-shelf LLMs are weak, biased contradiction detectors** — they over-trust memorized priors
   over conflicting source text (worse at larger scale) and are near chance on subtle conflicts; ground
   them with contrastive/controlled-conflict training (verdict-flip sensitivity 56%→86%). — **2403.08319,
   2109.05052, 2510.03418, 2103.08541**.
4. **Split RECONCILE by conflict nature — the central design decision.** Classify each conflict as
   **factual** (→ accuracy-weighted, copy-aware, multi-truth discovery) vs **normative** (→ social-choice
   aggregation; impossibility results mean some conflicts are irreducible, so keep multiple co-valid
   principles). Accuracy-weighting a normative conflict is a category error. This is the **G1 answer**.
   — factual: **1503.00310, 1708.02018, 1409.6428**; normative: **2404.10271**.
5. **Dedup BEFORE voting (independence of clones) + copy-detection.** Weight sources by estimated
   accuracy and down-weight copying so N near-duplicate books can't outvote one independent authority —
   and so an LLM-distillation pass that homogenizes phrasing doesn't manufacture false corroboration.
   Sharing the same *false* value is a strong copying signal. — **1503.00310, 1708.02018, 2404.10271**.
6. **Add a logical belief layer for principled merge/update.** IC belief **merging** (symmetric fusion
   under integrity constraints, distance-based, fragment-closure) and AGM belief **revision**
   (asymmetric minimal-change update of a standing base via a plausibility order) give the
   consistency-preserving machinery the prior corpus lacked; impossibility results warn no operator keeps
   all postulates. Closes **G8**. — **1404.6445, 2112.13557**.
7. **Align relations, not just principles — output a principle GRAPH.** Capture inter-principle
   relations ("prefer X over Y", "X precondition for Y"); entity-only alignment loses the rationale
   graph, and entity+relation alignment mutually reinforce. — **2407.17745, 2208.11125**.
8. **Anchor dedup on a shared claim.** Equivalence is claim-conditional (two principles can be
   equivalent under one claim but not another) and harder than generic paraphrase — cluster
   claim-conditionally, not by raw paraphrase similarity. — **1906.03538**.
9. **Evaluate with a metric family, and prefer incremental clustering for streaming.** ER/clustering
   metrics disagree on rankings and exact-match is brittle — report pairwise F1 + closest-cluster +
   Variation of Information and keep the aggregator swappable. For streaming book-arrival, prefer
   incremental centroid assignment (avoids a global tuned threshold). — **1509.04238, 1409.6428,
   1906.01753, 2104.08413, 2603.24246**.
10. **Bootstrap supervision from cheap structural signals.** Shared citations / defined-term IDs as free
    alignment labels; "disputed" markers as weak contradiction labels; revision diffs as token-level
    rationales. — **2104.05022, 2111.08543, 2103.08541**.

## Key open contradiction for the align/dedup design choice
Pairwise-scorer + agglomerative clustering with a tuned threshold (**1906.01753**) vs
incremental/sequential cluster composition that avoids the brittle threshold (**2104.08413**, also
**2603.24246**) — pick per corpus stability/streaming needs.

---
RESEARCH RUN COMPLETE: cross-document-knowledge-fusion-and-contradiction-detection-for-merging-expert-principles-distilled-from-multiple-source-documents-research-report.md
