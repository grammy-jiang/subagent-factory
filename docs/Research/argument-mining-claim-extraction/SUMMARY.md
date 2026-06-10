# Research Summary: Argument Mining and Atomic Claim Extraction

**Topic**: Argument mining and atomic claim extraction from long-form technical and scientific documents: claim and premise detection, claim typing, condition and exception extraction, and evidence linking

**Completed**: 2026-06-10 | **Rounds**: 4 (hard cap reached) | **Papers analyzed**: 37

---

## Final State

| Gap | Status | Priority |
|-----|--------|----------|
| GAP-1: Core AM annotation frameworks | CLOSED | — |
| GAP-2: Argument zoning for scientific documents | PARTIALLY CLOSED | MEDIUM |
| GAP-3: Claim typing taxonomies | CLOSED | — |
| GAP-4: Condition/exception extraction | PARTIALLY CLOSED (search exhausted) | HIGH |
| GAP-5: LLM prompt templates | ENGINEERING (resolvable) | MEDIUM |
| GAP-6: Book-length benchmarks | OPEN | MEDIUM |
| GAP-7: Claims schema JSON artifact | ENGINEERING (resolvable) | MEDIUM |

---

## What Was Found (Per Round)

**Round 1** (bae6a1aa8656) — 2026 arXiv papers:
- LLM + JSON schema extraction: ~95% accuracy vs. 75-80% for classifiers [2606.09251]
- Precision-abstention trade-off: coverage (recall) is a model capability ceiling [2606.09376]
- JSON schema format costs zero for capable models [2606.09410]
- Deterministic integrity gates: 27 seeded defects, zero false positives [2606.09500]

**Round 2** (r2-9afd1a87) — 10-year window, foundational AM literature:
- Stab & Gurevych 4-class scheme (Major Claim/Claim/Premise/Non-argumentative) confirmed across 5+ corpora [2103.04518], [2004.14677]
- Fact/Value/Policy claim types; 6-way premise sub-types (AAE-FG) [2510.16363]
- AQE evidence types (Explanation/Case/Research/Expert/Others) [2305.19902]
- IAM 3-way stance (support/contest/no-relation); alpha=0.57 for evidence links [2203.12257]
- 2025 LLM-in-AM survey covering full field [2506.16383]

**Round 3** (r3-5d60a587) — AM Survey + citation expansion:
- Teufel AZ scheme: 7-category (1999, kappa=0.71) and 14-category (2009) for scientific papers [s2-a2ae7155d9]
- AZ → AM mapping: AIM=Major Claim, OWN CONC=Claim(result), NOV ADV=Claim(contribution), SUPPORT=Premise, GAP WEAK=Claim(gap), ANTISUPP=Claim(conflict)
- Pollock (1986): rebutting vs. undercutting attacks — undercutting = "unless/except" qualifier in natural language
- Joint pointer architecture confirms joint > pipeline for AM link extraction [s2-0cf565a684]

**Round 4** (r4-1f1d4457) — Defeasible NLI search:
- 270 arXiv candidates; all 2026 papers; 0 relevant
- arXiv API returns only recent papers (sorted by recency); defeasible NLI papers (αNLI, 2020-2021) not retrieved
- Semantic Scholar API rate-limited; citation expansion failed
- 4-round cap reached; pipeline exhausted

---

## Key Grounded Decisions for Implementation

### Claims Schema Fields (all empirically grounded)

```
component_class: major_claim | claim | premise | non_argumentative
claim_type:      fact | value | policy [+ causal: validate before use]
premise_type:    common_ground | testimony | hypothetical_instance | statistics | real_example | other
evidence_type:   explanation | case | research | expert | other
stance:          support | contest | no_relation
az_zone:         AIM | OWN_CONC | NOV_ADV | SUPPORT | GAP_WEAK | ANTISUPP | OWN_MTHD | RELWRK | BKG | CTR | OUTSIDER [scientific docs only]
condition:       string | null  [bootstrap: "unless/only if/provided that/assuming"]
exception:       string | null  [bootstrap: Pollock undercutting attack pattern]
certainty:       asserted | hedged | speculative  [BioScope cue-word model]
```

### Extraction Architecture
1. **Stage 1**: Fine-tuned encoder (XLM-RoBERTa-Large) for sentence-level check-worthiness (5:1 class-weighted loss)
2. **Stage 2**: LLM + nested JSON schema; delayed-structure pattern (reason first, then JSON)
3. **Stage 3**: Deterministic post-extraction type checks (number/type mismatches)
4. **Coverage gate**: ratio of extracted claim count to claimable sentence count ≥ 0.50

### Condition/Exception Bootstrap (pending formal NLP validation)
Surface-cue markers for undercutting attacks:
- `unless`, `except when`, `only if`, `provided that`, `assuming`, `subject to`, `absent`, `if and only if`, `in the absence of`

---

## Limitations

1. **GAP-4 not fully closed**: No NLP extraction dataset or trained model for condition/exception (undercutting attack) identification found. The 2020-2021 defeasible NLI papers (αNLI by Bhagavatula et al., defeasible NLI benchmarks) exist on arXiv but were not retrieved by the automated pipeline (arXiv API recency-first sorting + Semantic Scholar API rate limiting). Direct fetch of `1908.05739` and similar papers would be needed in a follow-on session.

2. **AZ primary sources not obtained**: Teufel (1999, 2009) papers are pre-arXiv or on ACL Anthology only. Coverage is via the Lawrence & Reed (2020) AM Survey secondary description. The AZ zone labels and mappings are sufficient for schema design but not for implementing a standalone AZ classifier.

3. **CoreSC/Liakata not found**: Details of the Liakata CoreSC scheme (alternative to Teufel AZ for chemistry/biology) not retrieved in any round.

4. **No book-length benchmarks**: All corpora in this search target essays, forum posts, or abstracts. No empirical baseline for extraction quality at book-chapter scale.

5. **Joint 4-tuple extraction not production-ready**: Full (claim + evidence + stance + evidence_type) joint extraction achieves F1=21.39. Use separate passes for each sub-task.

---

## Final Report

`argument-mining-and-atomic-claim-extraction-from-long-form-technical-and-scientific-documents-claim-and-premise-detection-claim-typing-condition-and-exception-extraction-and-evidence-linking-research-report.md`

---

## Artifacts

```
runs/bae6a1aa8656/     Round 1 (19 papers analyzed)
runs/r2-9afd1a87/      Round 2 (15 papers analyzed)
runs/r3-5d60a587/      Round 3 (3 papers analyzed)
runs/r4-1f1d4457/      Round 4 (search exhausted)
workflow_state.json    Round 4 final state (complete)
workflow_state_round1.json
workflow_state_round2.json
workflow_state_round3.json
gaps.json              Final gap analysis
PROMPT.md              Original research prompt
```
