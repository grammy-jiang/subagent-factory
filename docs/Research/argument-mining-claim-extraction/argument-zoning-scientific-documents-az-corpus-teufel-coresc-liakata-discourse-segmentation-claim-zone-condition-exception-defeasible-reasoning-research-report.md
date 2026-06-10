# Research Report: Argument Zoning and Defeasible Reasoning (Round 3)

**Topic**: Argument zoning for scientific documents: AZ-corpus Teufel CoreSC Liakata discourse segmentation claim zone condition exception defeasible reasoning
**Date**: 2026-06-10 | **Round**: 3 of ≤4 | **Run ID**: r3-5d60a587
**Note**: This is the Round 3 gap-closure report. The canonical combined research report is at `argument-mining-and-atomic-claim-extraction-from-long-form-technical-and-scientific-documents-claim-and-premise-detection-claim-typing-condition-and-exception-extraction-and-evidence-linking-research-report.md`.

---

## Summary

Round 3 targeted GAP-2 (argument zoning) and GAP-4 (condition/exception extraction). 441 candidates were searched (352 arXiv + 89 citation-expanded). 3 new papers were analyzed. The AM Survey (Lawrence & Reed 2020) partially closed both gaps.

**Papers analyzed**: 3 (Round 3 only), 37 total (Rounds 1-3)
**Gaps partially closed**: GAP-2 (argument zoning, MEDIUM), GAP-4 (defeasible reasoning, HIGH)
**Gaps remaining**: GAP-4 (HIGH: no NLP extraction dataset), GAP-6 (MEDIUM: no book-length benchmarks)

**Search limitation**: arXiv API returns only recency-sorted results (all 2026 papers). Semantic Scholar API rate-limited (429). AZ-corpus/CoreSC primary papers (pre-arXiv) not accessible through automated pipeline. AM Survey secondary source is sufficient for schema design.

---

## Key Findings

### Argumentative Zoning for Scientific Documents (GAP-2 PARTIALLY CLOSED)

The Teufel AZ scheme (via Lawrence & Reed 2020 AM Survey) provides the standard framework:

**Teufel et al. 1999**: 7-category scheme for CL conference papers (kappa=0.71)
**Teufel et al. 2009**: 14-category extension to chemistry+CL (kappa=0.71 chemistry, 0.65 CL)

Zone-to-argument-mining mapping:
- `AIM` → Major Claim (hypothesis/research goal)
- `OWN_CONC` → Claim (non-measurable finding)
- `NOV_ADV` → Claim (novelty/contribution)
- `SUPPORT` → Premise (other work supports current)
- `GAP_WEAK` → Claim (gap/problem with field)
- `ANTISUPP` → Claim (conflict with other results)
- `OWN_MTHD` → Background (method description)
- `RELWRK / BKG` → Non-argumentative (context)

Automated AZ achieves 0.76–0.97 F-score using max entropy + n-gram features.

### Defeasible Reasoning Foundations (GAP-4 PARTIALLY CLOSED)

Pollock (1986) distinction (via AM Survey secondary source):
- **Rebutting attack**: Directly conflicts with a conclusion
- **Undercutting attack**: Attacks the inference rule between premise and conclusion; provides "reason for no longer believing the conclusion, rather than for believing the negation"

Undercutting attacks = computational model for "unless/except/only if" qualifiers.

Green (2018a/2018b): Domain-concept argumentation schemes for biological Results/Discussion sections with conditional slots, implemented as Prolog. Example: "Failed to Observe Effect of Hypothesized Cause" scheme.

No NLP extraction dataset or trained model for undercutting attack identification found.

---

## Gap Status After Round 3

| Gap | Status | Priority |
|-----|--------|----------|
| GAP-2: Argument zoning for scientific documents | PARTIALLY CLOSED | MEDIUM |
| GAP-4: Condition/exception extraction | PARTIALLY CLOSED | HIGH |

---

## Papers Analyzed (Round 3)

- [s2-a2ae7155d9] Argument Mining: A Survey, Lawrence & Reed (2020) — relevance 0.92
- [s2-0cf565a684] Here's My Point: Joint Pointer Architecture, Potash et al. EMNLP 2017 — relevance 0.38
- [s2-5ce2c9e681] AM for Automated Essay Scoring, AAAI 2018 — relevance 0.31
