# Research Run Summary — Long-Document Structure Mapping

## 1. Final report
`long-document-structure-mapping-research-report.md`
(snapshot of round-1 state preserved as `long-document-structure-mapping-research-report.2026-06-11.md`)
Validation: **PASS, score 1.00** (`tool_validate_report`).

## 2. Round History

| Round | Run ID | Topic / Gap Focus | New Papers | Gaps Addressed | Remaining Gaps |
|-------|--------|-------------------|------------|----------------|----------------|
| 1 | longdoc-r1-20260611 | Original topic (full facet sweep, deep) | 18 | Initial shortlist (structure extraction, candidate-unit ID, evaluation) | G1, G3 academic HIGH; G2, G4 academic MED; G5 LOW; G6–G8 engineering |
| 2 | longdoc-r2-20260612 | **G1** — standalone topic / linear text segmentation (TextTiling→C99→neural→long-doc coherence) | 9 | **G1 CLOSED** | G3 HIGH; G2, G4 MED; G5 LOW; engineering |
| 3 | longdoc-r3-20260612 | **G3** — claim / principle-level recall & coverage evaluation | 10 | **G3 CLOSED** | G2, G4 MED; G5 LOW; G6–G8 engineering (no HIGH) |

**Stop reason:** Both HIGH-severity academic gaps closed in 3 rounds (hard cap 4). No HIGH gaps remain → iteration stops per the iterative-synthesis convergence rule.

## 3. Remaining open gaps

| # | Classification | Severity | Why still open (one line) |
|---|---------------|----------|---------------------------|
| G2 | ACADEMIC | MEDIUM | No standalone TOC/heading-hierarchy method evaluated on *expository* 200+ page books (only DocTrace recipe + narrative-validated BookSum alignment). |
| G4 | ACADEMIC | MEDIUM | Expository/technical-book discourse structure under-represented; strongest evidence is narrative (BookSum) or scientific-article RST, not textbooks. |
| G5 | ACADEMIC | LOW | No method extracts cross-reference / prerequisite-dependency edges across a whole book (unit defined ch.3, used ch.9). |
| G6 | ENGINEERING | MEDIUM | No released code confirmed for most corpus papers → re-implement from method descriptions (resolved inline). |
| G7 | ENGINEERING | MEDIUM | Seven-stage glue/orchestration + inter-stage node-schema contract specified by no single paper (resolved inline, E2). |
| G8 | ENGINEERING | MEDIUM | Validators must scale to 200+ pages (BooookScore judge cost; LongSumEval ~60% ceiling ≤27k words) — made hierarchical/per-section inline (E3). |

None are HIGH; G2/G4/G5 are deferred as scoped, G6–G8 resolved inline in the report.

## 4. Findings most relevant to a Tier-1 source-structure-mapping preprocessor

1. **Stage-2 segmenter — recommended target: supervised long-context coherence segmenter.** Yu et al.'s Longformer + enhanced-coherence architecture is current SOTA for *long-document* topic segmentation (WIKI-727K F1 73.74→77.16, Pk 15.0→13.89) and degrades only ~8.4% relative Pk out-of-domain — the domain-shift robustness needed for arbitrary technical books. **[2310.11772]** (+ survey **[2411.16613]**).
2. **Stage-2 v1 default — cross-segment BERT.** A cheap binary boundary classifier over the *local left/right token context* of each candidate break; set a new SOTA, trivial to implement, composes with the round-1 structural tree. **[2004.14535]**; supervised framing + the standard WIKI-727K benchmark **[1803.09337]**.
3. **Stage-2 zero-training fallback — unsupervised embedding-adjacency segmentation.** Start a new block on adjacent-sentence/utterance embedding dissimilarity / utterance-pair coherence when no in-domain training data exists. **[2106.12978]**, **[2106.06719]**, **[2306.01169]**. Evaluate all boundaries with **Pk + WindowDiff** **[2411.16613]**.
4. **Step-10 coverage gate — atomic decomposition into a reference claim/principle set.** FActScore-style atomic-fact decomposition + a high-precision, ambiguity-aware extractor (Claimify) give the reference set the gate scores against. **[2305.14251]**, **[2502.10855]** (+ sub-claim selection **[2407.03572]**).
5. **Step-10 coverage gate — recall = match-based coverage / exhaustiveness.** Score `recall = fraction of reference claims matched by an extracted unit` using KPA key-point↔claim matching and an exhaustiveness/long-form coverage metric. This replaces the summary-QA and keyphrase recall@K proxies with a claim/principle-level recall metric. **[2005.01619]**, **[2404.11793]**, **[2501.03545]**, **[2110.10577]**.
6. **Hierarchical (per part→chapter→section) coverage aggregation** beats one flat pool for a 200+ page book and is how to clear LongSumEval's ~60% comprehensiveness ceiling; mirrors the key-point-hierarchy idea. **[2306.03853]**, **[2501.03545]**, **[2604.25130]**.
7. **Check-worthiness filter** selects which source claims are worth enumerating as principles (vs. trivia) before the recall metric is applied. **[2212.08514]**, **[2004.14425]**.
8. **Dual precision+recall harness in the *claim* unit.** Pair BooookScore per-unit error-rate (precision) with the round-3 claim-recall coverage metric (recall) and a miss-list feedback loop into re-segmentation/re-enumeration. **[2310.00785]** + (5)/(6) above.
9. **Carry-over architecture invariants (round 1):** provenance-anchored atomic units **[2406.10370]**, global-context salience for recall **[1905.13164]/[2305.14806]**, hierarchical merging over incremental **[2310.00785]**, structure-aware (not fixed-window) chunking **[2606.10921]**.

---

### Run notes / caveats
- The arXiv backend returned only a single day's recency-biased candidates, so rounds 2–3 used an **agent-curated shortlist seeded by canonical arXiv IDs** (verified via the arXiv API), then ran the standard pipeline (download → convert → extract → summarize).
- Environment lacked `pymupdf4llm` → PDFs converted with **`pdftotext` (poppler)**; the summarize LLM was unavailable → **heuristic fallback summaries**, so the cross-paper synthesis was authored by the agent grounded in the converted paper text (numbers and method claims quoted from the source markdown).
- All work confined to this folder + the shared `~/.cache` pipeline cache; the subagent-factory repository was not modified.

RESEARCH RUN COMPLETE: long-document-structure-mapping-research-report.md
