# Research Summary — Factual Consistency and Faithfulness Evaluation of LLM-Generated Text

**Run IDs**: 3154f302744b (Round 1), dffa8f92250f (Round 2)
**Date**: 2026-06-10
**Profile**: deep
**Pipeline version**: research-pipeline 0.28.0
**Sources**: arXiv (cs.CL, cs.AI)

---

## Round History

| Round | Run ID | Topic / Gap Focus | New Papers | Gaps Addressed | Remaining Gaps |
|-------|--------|-------------------|------------|----------------|----------------|
| 1 | 3154f302744b | Original topic: hallucination detection, faithfulness vs. factuality, overclaiming signals, NLI/QA metrics | 11 | Initial shortlist: certainty distortion, CCHD, constrained paraphrase, LLM introspection | 2 HIGH academic, 1 MEDIUM academic, 2 MEDIUM engineering |
| 2 | dffa8f92250f | Gap-closure: NLI/QA metric design (FactCC, SummaC, QAFactEval, FActScore, AlignScore, RefChecker, MiniCheck) + claim-strength building blocks | 29 | gap-2 CLOSED (all 9 metrics documented); gap-1 PARTIAL (3 building blocks identified, reclassified ENGINEERING) | 2 HIGH engineering, 1 MEDIUM engineering |

**Convergence**: Stopped after Round 2. No ACADEMIC gaps remain that require additional literature search. All remaining gaps are ENGINEERING (original annotation/fine-tuning work, taxonomy authoring, domain calibration).

---

## Pipeline Results

| Stage | Round 1 | Round 2 |
|-------|---------|---------|
| Candidates searched | 534 | 430 |
| After BM25 screen | 20 | 30 |
| LLM-accepted | 11 | 20 |
| Downloaded | 11 | 29 |
| Converted | 11 | 29 |
| Deeply analysed | 11 | 29 |
| Synthesis reviewer | accepted | accepted_with_issues (non-blocking) |
| Validate report | PASS 1.00 | PASS 1.00 |

---

## Open Gaps

| # | Gap | Type | Severity |
|---|-----|------|----------|
| gap-1 | Build claim-strength overclaim detector (building blocks: WiCE, Janus, RefChecker) | ENGINEERING | HIGH |
| gap-3 | Author claim-strength ordering taxonomy (EXACT_SUPPORT → CONTRADICTED) | ENGINEERING | HIGH |
| gap-4 | Domain-adapt MiniCheck/AlignScore for subagent-generated rules | ENGINEERING | MEDIUM |

**gap-2** (design details of 9 NLI/QA metrics) is **CLOSED**.

---

## Top Findings

1. **MiniCheck-RBTA matches GPT-4 at 1/400th cost** — Fine-tuned DeBERTa/Flan-T5, binary sentence-level NLI, no decomposition overhead. Recommended base faithfulness checker. [2404.10774]

2. **Sentence-level NLI is the minimum effective granularity** — Document-level NLI assigns high entailment probability to demonstrably inconsistent summaries. Triplet-level adds +10 pts for relational claims. [1910.12840, 2111.09525, 2405.14486]

3. **Hybrid NLI+QA outperforms either alone** — AlignScore (4.7M examples, 7 task types) achieves SOTA on 22 datasets; QAFactEval ablation shows +2–5 pts from combining approaches. [2305.16739, 2112.08542]

4. **WiCE Partially-Supported label is the only existing overclaim proxy** — Three-way entailment (Supported/Partially-Supported/Not-Supported) directly measures claim-strength distortion. [2303.01432]

5. **Janus Specificity + Framing dimensions map to overclaim taxonomy** — Specificity = numeric precision loss; Framing = hedge removal. Both are direct automated overclaim proxies. [2606.10852]

6. **Faithfulness ≠ factuality** — A faithful claim is grounded in source; a factual claim is true in the world. A summary can be faithful-but-false (source is wrong) or factual-but-unfaithful (correct fact not in source). [dblp-7766119394, 2005.00661]

7. **Exact provenance tracking outperforms post-hoc retrieval** — Source span pointers maintained during generation give higher faithfulness checking accuracy than retrieval-based approaches. [2606.11127]

8. **Uncertainty scores are unreliable faithfulness proxies** — Near-zero correlation with hallucination labels; do not use model confidence as faithfulness signal. [2605.27016]

---

## Top Papers

| # | Paper | Key Contribution |
|---|-------|-----------------|
| 1 | 2404.10774 (MiniCheck) | GPT-4-parity NLI at 1/400th cost; 35K synthetic training data |
| 2 | 2305.16739 (AlignScore) | Unified NLI+QA; SOTA on 22 benchmarks; 4.7M training examples |
| 3 | 2405.14486 (RefChecker) | Triplet-level NLI; +10 pts over response-level; three-way verdict |
| 4 | 2303.01432 (WiCE) | Partially-Supported label; only existing overclaim category |
| 5 | 2606.10852 (Janus) | Five information distortion dimensions; Specificity + Framing = overclaim proxies |
| 6 | 2305.14251 (FActScore) | Atomic fact decomposition; 58% ChatGPT factual precision on biographies |
| 7 | 2111.09525 (SummaC) | Sentence-level NLI benchmark; 74.4% accuracy; defines granularity standard |

---

## Artifacts

| Artifact | Path |
|----------|------|
| Final report | `factual-consistency-and-faithfulness-evaluation-of-llm-generated-text-against-source-documents-hallucination-and-overgeneralization-detection-claim-verification-and-entailment-and-qa-based-metrics-research-report.md` |
| Round 1 workspace | `3154f302744b/` |
| Round 2 workspace | `runs/dffa8f92250f/` |
| Gap classification | `gaps.json` |
| Round 2 synthesis | `runs/dffa8f92250f/analysis/synthesis.json` |
| Round 2 synthesis review | `runs/dffa8f92250f/review/synthesis_review.json` |
| Validation result | `validation_result.json` |
| Workflow state | `workflow_state.json` (status: complete) |
