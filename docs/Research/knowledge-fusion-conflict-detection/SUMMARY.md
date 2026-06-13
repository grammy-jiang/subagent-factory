# Research Run Summary — Cross-Document Knowledge Fusion & Contradiction Detection

## 1. Final report

`cross-document-knowledge-fusion-and-contradiction-detection-for-merging-expert-principles-distilled-from-multiple-source-documents-research-report.md`

(Round-1 snapshot preserved as `…-research-report.2026-06-13.md`.)
Validation: **PASS, score 0.83**; synthesis review accepted (faithfulness 0.9, coherence 0.9, gap_completeness 0.88, citation_integrity true). 19 papers synthesized.

## 2. Round History

| Round | Run ID | Topic / Gap Focus | New Papers | Gaps Addressed | Remaining Gaps | Outcome |
|-------|--------|-------------------|------------|----------------|----------------|---------|
| 1 | 57e857a93e69 | Original topic (deep profile, 6-sub-area sweep) | 19 | Initial shortlist; 8 gaps classified | 4 academic (G1,G3 HIGH; G4,G6,G8 MED), 2 engineering (G2 HIGH, G5 MED), 1 OOS (G7) | Complete; validated PASS 0.83 |
| 2 | round2-g3 | G3 — cross-doc NLI / stance / knowledge-conflict detection between independent docs (academic HIGH) | 0 | None | G1, G3 | **no_new_papers** — 103 candidates **all 2026**, 0 topical; arXiv recency-locked |
| 3 | round3-g1 | G1 — truth discovery / reconciliation for normative/subjective claims + belief merging (academic HIGH) | 0 | None | G1, G3 | **no_new_papers** — 186 candidates (181×2026, 5×2025), 0 on-topic; arXiv recency-locked |

**Stopped at round 3 of 4** under the `no_new_papers` convergence rule (not the round cap).

## 3. Remaining open gaps

| ID | Classification | Severity | Why still open |
|----|----------------|----------|----------------|
| **G1** | ACADEMIC (environment-limited) | HIGH | Reconciling **normative/prescriptive** principles ("prefer X"/"avoid Y") has no in-corpus method — all fusion papers assume a factual true value. Round-3 search reached only recency-locked ~2026 arXiv; the pre-2026 social-choice / preference-aggregation / subjective-truth-discovery foundations are unreachable via this index. Deferred to manual follow-up. |
| **G3** | ACADEMIC (environment-limited) | HIGH | Cross-source contradiction detection rests on only 2 in-corpus papers (2111.08543 intra-article self-contradiction; 2510.03418 synthetic legal benchmark) — neither validated ACROSS independent documents. Round-2 search reached only recency-locked ~2026 arXiv; pre-2026 cross-document NLI / DocNLI / stance-across-docs benchmarks unreachable. Deferred. |
| G4 | ACADEMIC | MEDIUM | Deterministic-vs-LLM cost/quality boundary asserted from method structure, never measured; needs an ablation benchmark (not separately rounded — MED severity). |
| G6 | ACADEMIC | MEDIUM | Copy-aware weighting (1503.00310) + metric disagreement (1509.04238) validated only on factual/ER corpora; transfer to distilled-from-books principles unproven. |
| G8 | ACADEMIC | MEDIUM | AGM / logical belief-revision KB merging absent; sub-area 6 represented only by embedding/EM KG alignment (2407.17745, 2208.11125, 2109.07401). |
| G2 | ENGINEERING | HIGH | **Resolved inline** — explicit inter-stage artifact contracts defined in report. |
| G5 | ENGINEERING | MEDIUM | **Resolved inline** — periodic centroid recompute + held-out threshold calibration. |
| G7 | OUT_OF_SCOPE | LOW | ECB+-only generalization — benchmark-coverage concern outside the cross-source merge question. |

## 4. Findings most relevant to the downstream use (Step-7 multi-source synthesis)

1. **Three-stage pipeline keyed to the three operations.** Build the merge as ALIGN/DEDUP → DETECT-CONTRADICTION → RECONCILE; each sub-area is studied in isolation in the literature, so design the seams explicitly. — synthesis of all 19; structurally anchored by **2109.07401, 2106.01210, 2104.08413, 1503.00310, 2510.03418**.

2. **Recall-then-filter is the dominant cross-document architecture, and the split maps cleanly onto deterministic-seed vs LLM.** Cheap deterministic recall (normalize + block/retrieve + embed + cluster) then a precision judgement stage (transformer/LLM equivalence filter). The recall stage MUST be tuned for recall — the LLM filter can only remove/re-weight candidates, never recover a missed equivalence. — **2109.07401, 2106.01210, 2104.08413, 2603.24246**.

3. **Deterministic vs LLM division of labour (the requested split).** Deterministic = normalization, multi-key blocking, FAISS/dense retrieval, clustering, accuracy-weighted voting, copy-graph estimation, lexical NLI features. LLM = semantic-equivalence judgement at the precision seam + retrieval-resistant conflict adjudication. — **2109.07401, 1609.06265, 1503.00310, 2510.03418**.

4. **Blocking/retrieval is necessary AND a bias source.** Quadratic all-pairs comparison must be pruned; prefer an ensemble/union of blocking keys over any single key to avoid systematically missing cross-source equivalences. — **1609.06265, 1603.07816, 2208.11125, 2210.12654, 2111.08543**.

5. **Reconcile by accuracy-weighting + copy-discounting, but allow multi-truth.** Weight each source by estimated accuracy and explicitly down-weight copying so N near-duplicate books cannot outvote one independent authority — yet adopt the multi-truth stance so a topic may retain several co-valid principles instead of forcing one winner. — **1503.00310, 1409.6428, 1708.02018** (1708.02018 = multi-truth; contradicts 1503.00310's single-value default).

6. **Triage every detected conflict: retrieval-verifiable vs retrieval-resistant.** Resolve verifiable conflicts deterministically against a canonical source; route only retrieval-resistant conflicts to LLM judgement — and do not trust the LLM detector on subtle long-context conflicts (even GPT-4 near chance). — **2510.03418, 2111.08543**.

7. **Align relations, not just principles — output a principle GRAPH.** Capture inter-principle relations ("prefer X over Y", "X is precondition for Y"); aligning only the nodes loses the rationale graph. — **2407.17745** (entity-relation synergy), 2208.11125.

8. **Evaluate the merge with a metric family, not one score.** Use pairwise + closest-cluster + Variation of Information together; ER metrics disagree on rankings and exact-match is brittle — so the fusion/eval stages must be swappable and tuned per corpus. — **1509.04238, 1409.6428**.

9. **Key open contradiction for the align/dedup design choice.** Pairwise-scorer + agglomerative clustering with a tuned threshold (**1906.01753**) vs incremental/sequential cluster composition that avoids the brittle threshold (**2104.08413**, also 2603.24246) — pick per corpus stability needs.

## Caveat
Both HIGH academic gaps (G1 normative-principle reconciliation, G3 validated cross-document contradiction detection) are the two most central to the downstream task and remain **environment-limited**, not closed: the configured arXiv index is recency-locked to ~2026 (see project memory `arxiv-index-recency-locked`), so the foundational pre-2026 literature could not be retrieved. Recommend a manual literature pull (Semantic Scholar / ACL Anthology) for DocNLI, cross-document NLI, stance-across-documents, truth discovery for subjective claims, and AGM belief merging before relying on these two operations in production.

---
RESEARCH RUN COMPLETE: cross-document-knowledge-fusion-and-contradiction-detection-for-merging-expert-principles-distilled-from-multiple-source-documents-research-report.md
