# Research Report: Argument Mining Foundational Literature (Round 2)

**Topic**: Argument mining foundational literature: claim premise annotation argument component classification scientific discourse zoning claim typing taxonomy
**Date**: 2026-06-10 | **Round**: 2 of ≤4 | **Run ID**: r2-9afd1a87
**Note**: This is the Round 2 gap-closure report. The canonical combined research report is at `argument-mining-and-atomic-claim-extraction-from-long-form-technical-and-scientific-documents-claim-and-premise-detection-claim-typing-condition-and-exception-extraction-and-evidence-linking-research-report.md`.

---

## Summary

Round 2 extended the search window to 10 years (2016–2026) to retrieve foundational argument mining literature missed in Round 1. 15 new papers were analyzed (11 directly relevant). Two of the three HIGH-severity academic gaps from Round 1 were closed: GAP-1 (core AM annotation frameworks) and GAP-3 (claim typing taxonomies).

**Papers analyzed**: 15 (Round 2 only), 34 total (Rounds 1+2)
**Gaps closed**: GAP-1, GAP-3
**Gaps remaining**: GAP-2 (HIGH: argument zoning), GAP-4 (HIGH: condition/exception extraction)

---

## Key Findings

### Claim/Premise Annotation Frameworks (GAP-1 CLOSED)

The Stab & Gurevych 4-class annotation scheme (Major Claim / Claim / Premise / Non-argumentative) is confirmed as the de-facto standard across 5+ independent corpora and 2+ languages.

- Token-level BIO tagging required when premises co-occur with claims within sentences (~62% of cases) — [2103.04518]
- Contextual fine-tuning on topic-relevant data yields 12-point F1 improvement — [2004.14677]
- IBM Debater, Walton, and Peldszus schemes surveyed; Stab & Gurevych most widely replicated — [2506.16383]
- Cross-language validation in Bahasa Indonesia — [s2-05b4fead2c]

### Claim Type Taxonomy (GAP-3 CLOSED)

Fact/Value/Policy is the validated 3-way claim type taxonomy with automatic classifiability:
- **Fact**: Empirical or descriptive statement
- **Value**: Normative or evaluative judgement
- **Policy**: Prescriptive or action-oriented directive

From AAE-FG via AASP [2510.16363]; 6-way premise sub-types also validated.

Walton Argument from Consequences templates cover 74.6% of policy arguments at kappa=0.80 — [s2-5a41c4f399]

### Argument Quadruplet Schema (AQE)

5-way evidence types (Explanation/Case/Research/Expert/Others) validated by [2305.19902].
3-way stance (support/contest/no-relation) at alpha=0.63 by [2203.12257].
Full 4-tuple joint extraction achieves F1=21.39 — not production-ready; use separate passes.

### IAA Norms

- Span detection: ~0.79
- Stance: ~0.63
- Evidence links: ~0.57

---

## Gap Status After Round 2

| Gap | Status | Priority |
|-----|--------|----------|
| GAP-1: Core AM annotation frameworks | CLOSED | — |
| GAP-2: Argument zoning for scientific documents | OPEN → Round 3 | HIGH |
| GAP-3: Claim typing taxonomies | CLOSED | — |
| GAP-4: Condition/exception extraction | OPEN → Round 3-4 | HIGH |

---

## Papers Analyzed (Round 2)

- [2506.16383] LLMs in Argument Mining: A Survey (2025) — relevance 0.97
- [2305.19902] AQE: Argument Quadruplet Extraction (2023) — relevance 0.92
- [2510.16363] AASP: End-to-End Argument Mining (2025) — relevance 0.90
- [2203.12257] IAM: Integrated Argument Mining Dataset (2022) — relevance 0.88
- [2103.04518] Argument Component Segmentation in Essays (2021) — relevance 0.82
- [2004.14677] AMPERSAND: AM for Persuasive Discussions (2020) — relevance 0.82
- [s2-5a41c4f399] Policy Argument Templates (Walton) (~2020) — relevance 0.82
- [s2-fa21a9c006] Legal Argument Extraction (ILP) (~2019) — relevance 0.75
- [s2-4756981949] AM from Speech: Political Debates (~2018) — relevance 0.72
- [s2-433127191a] LLM Argument Quality for SemMedDB (~2023) — relevance 0.72
- [s2-05b4fead2c] AM in Bahasa Indonesia (~2021) — relevance 0.65
