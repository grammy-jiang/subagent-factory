# Research Report: Defeasible NLI and Condition/Exception Extraction (Round 4)

**Topic**: Defeasible NLI and condition exception extraction from argumentative text: undercutting attacks, abductive reasoning, conditional NLI datasets, argument defeat conditions
**Date**: 2026-06-10 | **Round**: 4 of 4 (FINAL) | **Run ID**: r4-1f1d4457
**Note**: This is the Round 4 gap-closure report. The canonical combined research report is at `argument-mining-and-atomic-claim-extraction-from-long-form-technical-and-scientific-documents-claim-and-premise-detection-claim-typing-condition-and-exception-extraction-and-evidence-linking-research-report.md`.

---

## Summary

Round 4 targeted GAP-4 (condition/exception extraction; defeasible reasoning NLP). 270 arXiv candidates were retrieved. All 8 BM25-shortlisted papers were off-topic 2026 arXiv papers. 0 relevant papers were found.

**4-round hard cap reached. Pipeline exhausted.**

**Papers analyzed**: 0 (Round 4), 37 total (Rounds 1-4)
**Gaps closed**: None
**Search limitations**: arXiv API returns recency-sorted results (all 2026). The foundational defeasible NLI papers — αNLI (Bhagavatula et al. 2020, arXiv 1908.05739) and defeasible NLI benchmarks (2020-2021) — exist on arXiv but were not retrieved by the automated pipeline. Semantic Scholar API was rate-limited throughout Round 3-4. Manual direct fetch of `1908.05739` and similar papers in a follow-on session is recommended.

---

## Final Gap Status (All Rounds)

| Gap | Status | Priority |
|-----|--------|----------|
| GAP-1: Core AM annotation frameworks | CLOSED | — |
| GAP-2: Argument zoning for scientific documents | PARTIALLY CLOSED | MEDIUM |
| GAP-3: Claim typing taxonomies | CLOSED | — |
| GAP-4: Condition/exception extraction | PARTIALLY CLOSED | HIGH |
| GAP-5: LLM prompt templates | ENGINEERING (resolvable) | MEDIUM |
| GAP-6: Book-length benchmarks | OPEN | MEDIUM |
| GAP-7: Claims schema JSON artifact | ENGINEERING (resolvable) | MEDIUM |

---

## Available for GAP-4 Implementation

Despite no new NLP papers found, the following is available from prior rounds:

**Theoretical grounding** (from [s2-a2ae7155d9], Round 3):
- Pollock (1986): Undercutting attacks = attacks on inference rule between premise and conclusion
- These are the computational equivalent of "unless/except/only if" qualifiers
- Green (2018): Domain-concept schemes for biomedical text with condition slots

**Engineering mitigation (bootstrap)**:
Surface-cue markers for undercutting attack extraction:
`unless`, `except when`, `only if`, `provided that`, `assuming`, `subject to`, `absent`, `if and only if`, `in the absence of`

The `condition` and `exception` fields in the claims schema should be nullable strings populated via surface-cue detection as an interim measure pending a validated NLP extraction model.
