# Structured Research Synthesis: Cross-document knowledge fusion and contradiction detection for merging expert principles distilled from multiple source documents

## Executive Summary

This synthesis covers 19 papers and is built from Step 1 extraction records. It preserves evidence, assumptions, contradictions, and conditional implications without selecting an architecture.

**Scope boundary (downstream anchor).** This spike covers ONLY the cross-document / cross-source layer for the subagent-factory Step-7 multi-source synthesis: (1) aligning + deduplicating equivalent concepts across documents, (2) detecting contradictions BETWEEN independent sources, and (3) reconciling / aggregating conflicting evidence into one principle graph. The intra-document argument-relation vocabulary (claim/premise detection, support/contest/no_relation stance, Pollock rebutting-vs-undercutting) is covered by a separate argument-mining report and is deliberately NOT re-covered here.

## Round History

| Round | Run ID | Topic / Gap Focus | New Papers | Gaps Addressed | Remaining Gaps | Outcome |
|-------|--------|-------------------|------------|----------------|----------------|---------|
| 1 | 57e857a93e69 | Original topic (deep profile, full 6-sub-area sweep) | 19 | Initial shortlist; 8 gaps classified | 4 academic (G1,G3,G4,G6,G8 — G4/G6/G8 MED), 2 engineering (G2 HIGH, G5 MED), 1 out-of-scope (G7) | Validated report (PASS 0.83); synthesis review accepted |
| 2 | round2-g3 | Cross-document NLI / stance / knowledge-conflict detection between independent docs (closes **G3**, academic HIGH) | 0 | None — search returned 103 candidates, **all 2026**, 0 topical to cross-doc contradiction/NLI/stance | G1, G3 still open | **no_new_papers** — arXiv index recency-locked (~2026); foundational pre-2026 literature unreachable |
| 3 | round3-g1 | Truth discovery / conflict reconciliation for normative/subjective claims + belief merging (closes **G1**, academic HIGH) | 0 | None — 186 candidates, 181×2026 + 5×2025, 0 on-topic (closest = 2606.12903 X-MADAM-RAG evidence-conflict, RAG-framed, off-target) | G1, G3 still open | **no_new_papers** — same recency-locked wall |

**Why iteration stopped (2 of 4 rounds' worth of gap-closure search attempted).** Both remaining HIGH-severity ACADEMIC gaps (G1, G3) were probed with dedicated gap-specific search rounds. In each, the configured arXiv source returned only recency-locked listings (≈ June 2026) with no topical match to the *foundational* literature these gaps require — cross-document NLI corpora, stance-across-documents detection, truth discovery for subjective/normative claims, and AGM-style belief merging are all pre-2026 bodies of work not reachable through this index. Per the convergence rule "a round searched and found no new relevant papers after screening → stop," further rounds would re-hit the identical wall and are not run. G1 and G3 are therefore **reclassified below as environment-limited** and deferred to manual follow-up rather than left as actionable open academic rounds.

## Cross-Source Gap Ledger

The eight gaps from the round-1 synthesis, with post-iteration status. ENGINEERING gaps are resolved inline (resolution given); ACADEMIC gaps that could not be closed are reclassified with the reason.

| ID | Class (final) | Sev | Status after iteration | Gap |
|----|---------------|-----|------------------------|-----|
| **G1** | ACADEMIC → environment-limited | HIGH | **Open, deferred** | No in-corpus method aligns/reconciles **normative/prescriptive** principles ("prefer X", "avoid Y"); all reconciliation papers (1503.00310, 1409.6428, 1708.02018) assume a factual true value. Round-3 search reached only recency-locked 2026 papers. Manual follow-up: pre-2026 social-choice / preference-aggregation + truth-discovery-for-subjective-claims literature; treat "truth" as judgement, not fact. |
| **G2** | ENGINEERING | HIGH | **Resolved inline** | No paper unifies align/dedup → detect-contradiction → reconcile end-to-end. **Resolution:** define explicit inter-stage artifacts — `(cluster_id → principle members)` from align/dedup; `(pair, conflict_type)` from detection using 2510.03418's retrieval-verifiable vs retrieval-resistant split; `(object, weighted_values, source_copy_graph)` from fusion per 1503.00310. Prototype the seam; evaluate the merge with 1509.04238's metric family. This is a composition/engineering task, not a literature gap. |
| **G3** | ACADEMIC → environment-limited | HIGH | **Open, deferred** | Cross-source contradiction detection rests on only 2 in-corpus papers (2111.08543 self-contradiction within Wikipedia articles; 2510.03418 synthetic legal benchmark) — neither is validated detection ACROSS independent documents. Round-2 search reached only recency-locked 2026 papers. Manual follow-up: pre-2026 cross-document NLI / DocNLI / stance-across-docs / knowledge-conflict benchmarks; note both in-corpus papers report even GPT-4 near chance on subtle long-document contradictions. |
| G4 | ACADEMIC | MED | Open (not separately rounded) | Deterministic-vs-LLM cost/quality boundary is asserted from method structure, never measured. Needs an ablation benchmark. |
| G5 | ENGINEERING | MED | **Resolved inline** | Adaptive/online threshold + centroid updating for streaming principle merge. **Resolution:** periodic centroid recomputation + a held-out calibration set to re-tune similarity thresholds per corpus; carry 2208.11125's landmark-bridge idea to preserve cross-block structure as books arrive. |
| G6 | ACADEMIC | MED | Open | Copy-aware weighting (1503.00310) and metric disagreement (1509.04238) are established only on factual / entity-resolution corpora; transfer to distilled-from-books principle sets is asserted, never validated. |
| G7 | OUT_OF_SCOPE | LOW | Closed (out of scope) | ECB+-only generalization of sub-area-1 coreference results — a benchmark-coverage concern outside the cross-source merge question. |
| G8 | ACADEMIC | MED | Open | Belief revision / KB merging in the AGM / logical sense is absent; sub-area 6 is represented only by embedding/EM-based KG alignment (2407.17745, 2208.11125, 2109.07401). |

## Scope and Corpus

| paper_id | version | title | year | venue |
| --- | --- | --- | --- | --- |
| 1906.01753 | v1 | Revisiting Joint Modeling of Cross-document Entity and Event Coreference Resolution |  |  |
| 2106.01210 | v1 | Cross-document Coreference Resolution over Predicted Mentions |  |  |
| 1509.04238 | v1 | A Practioner's Guide to Evaluating Entity Resolution Results |  |  |
| 1609.06265 | v2 | An Ensemble Blocking Scheme for Entity Resolution of Large and Sparse Datasets |  |  |
| 2111.08543 | v1 | WikiContradiction: Detecting Self-Contradiction Articles on Wikipedia |  |  |
| 2510.03418 | v2 | LegalWiz: A Multi-Agent Generation Framework for Contradiction Detection in Legal Documents |  |  |
| 1503.00310 | v1 | Data Fusion: Resolving Conflicts from Multiple Sources |  |  |
| 1409.6428 | v1 | Truth Discovery Algorithms: An Experimental Evaluation |  |  |
| 1908.01843 | v1 | GEAR: Graph-based Evidence Aggregating and Reasoning for Fact Verification |  |  |
| 2009.06401 | v3 | Multi-Hop Fact Checking of Political Claims |  |  |
| 2407.17745 | v1 | Beyond Entity Alignment: Towards Complete Knowledge Graph Alignment via Entity-Relation Synergy |  |  |
| 2208.11125 | v1 | Large-scale Entity Alignment via Knowledge Graph Merging, Partitioning and Embedding |  |  |
| 2210.12654 | v1 | Cross-document Event Coreference Search: Task, Dataset and Modeling |  |  |
| 2104.08413 | v1 | Sequential Cross-Document Coreference Resolution |  |  |
| 2104.05022 | v2 | WEC: Deriving a Large-scale Cross-document Event Coreference dataset from Wikipedia |  |  |
| 1603.07816 | v1 | Probabilistic Record Linkage and Deduplication after Indexing, Blocking, and Filtering |  |  |
| 1708.02018 | v1 | SmartMTD: A Graph-Based Approach for Effective Multi-Truth Discovery |  |  |
| 2109.07401 | v1 | Matching with Transformers in MELT |  |  |
| 2603.24246 | v1 | Semantic Centroids and Hierarchical Density-Based Clustering for Cross-Document Software Coreference Resolution |  |  |

## Methodology

- Loaded Step 1 PaperExtractionRecord artifacts as the only evidence source.
- Normalized statements by category, confidence, and evidence IDs.
- Built matrices, taxonomy, assumptions, contradictions, and risks from structured fields.
- Kept design implications conditional and architecture-neutral.

## Taxonomy of Approaches

- **MEDIUM** method details require structured llm...: Method details require structured LLM extraction; see linked evidence chunks.; Method details require structured LLM extraction; see linked evidence chunks.; Method details require structured LLM extraction; see linked evidence chunks. [1409.6428, 1503.00310, 1509.04238, 1603.07816, 1609.06265, 1708.02018, 1906.01753, 1908.01843, 2009.06401, 2104.05022, 2104.08413, 2106.01210, 2109.07401, 2111.08543, 2208.11125, 2210.12654, 2407.17745, 2510.03418, 2603.24246]

## Evidence Matrix

| paper_id | methods | datasets | results | assumptions | limitations |
| --- | --- | --- | --- | --- | --- |
| 1906.01753 | Method details require structured LLM extraction; see linked evidence chunks. | not_reported | Results require structured LLM extraction; see linked evidence chunks. | not_reported | Limitations were not reliably extracted in template fallback mode. |
| 2106.01210 | Method details require structured LLM extraction; see linked evidence chunks. | not_reported | Results require structured LLM extraction; see linked evidence chunks. | not_reported | Limitations were not reliably extracted in template fallback mode. |
| 1509.04238 | Method details require structured LLM extraction; see linked evidence chunks. | not_reported | Results require structured LLM extraction; see linked evidence chunks. | not_reported | Limitations were not reliably extracted in template fallback mode. |
| 1609.06265 | Method details require structured LLM extraction; see linked evidence chunks. | not_reported | Results require structured LLM extraction; see linked evidence chunks. | not_reported | Limitations were not reliably extracted in template fallback mode. |
| 2111.08543 | Method details require structured LLM extraction; see linked evidence chunks. | not_reported | Results require structured LLM extraction; see linked evidence chunks. | not_reported | Limitations were not reliably extracted in template fallback mode. |
| 2510.03418 | Method details require structured LLM extraction; see linked evidence chunks. | not_reported | Results require structured LLM extraction; see linked evidence chunks. | not_reported | Limitations were not reliably extracted in template fallback mode. |
| 1503.00310 | Method details require structured LLM extraction; see linked evidence chunks. | not_reported | Results require structured LLM extraction; see linked evidence chunks. | not_reported | Limitations were not reliably extracted in template fallback mode. |
| 1409.6428 | Method details require structured LLM extraction; see linked evidence chunks. | not_reported | Results require structured LLM extraction; see linked evidence chunks. | not_reported | Limitations were not reliably extracted in template fallback mode. |
| 1908.01843 | Method details require structured LLM extraction; see linked evidence chunks. | not_reported | Results require structured LLM extraction; see linked evidence chunks. | not_reported | Limitations were not reliably extracted in template fallback mode. |
| 2009.06401 | Method details require structured LLM extraction; see linked evidence chunks. | not_reported | Results require structured LLM extraction; see linked evidence chunks. | not_reported | Limitations were not reliably extracted in template fallback mode. |
| 2407.17745 | Method details require structured LLM extraction; see linked evidence chunks. | not_reported | Results require structured LLM extraction; see linked evidence chunks. | not_reported | Limitations were not reliably extracted in template fallback mode. |
| 2208.11125 | Method details require structured LLM extraction; see linked evidence chunks. | not_reported | Results require structured LLM extraction; see linked evidence chunks. | not_reported | Limitations were not reliably extracted in template fallback mode. |
| 2210.12654 | Method details require structured LLM extraction; see linked evidence chunks. | not_reported | Results require structured LLM extraction; see linked evidence chunks. | not_reported | Limitations were not reliably extracted in template fallback mode. |
| 2104.08413 | Method details require structured LLM extraction; see linked evidence chunks. | not_reported | Results require structured LLM extraction; see linked evidence chunks. | not_reported | Limitations were not reliably extracted in template fallback mode. |
| 2104.05022 | Method details require structured LLM extraction; see linked evidence chunks. | not_reported | Results require structured LLM extraction; see linked evidence chunks. | not_reported | Limitations were not reliably extracted in template fallback mode. |
| 1603.07816 | Method details require structured LLM extraction; see linked evidence chunks. | not_reported | Results require structured LLM extraction; see linked evidence chunks. | not_reported | Limitations were not reliably extracted in template fallback mode. |
| 1708.02018 | Method details require structured LLM extraction; see linked evidence chunks. | not_reported | Results require structured LLM extraction; see linked evidence chunks. | not_reported | Limitations were not reliably extracted in template fallback mode. |
| 2109.07401 | Method details require structured LLM extraction; see linked evidence chunks. | not_reported | Results require structured LLM extraction; see linked evidence chunks. | not_reported | Limitations were not reliably extracted in template fallback mode. |
| 2603.24246 | Method details require structured LLM extraction; see linked evidence chunks. | not_reported | Results require structured LLM extraction; see linked evidence chunks. | not_reported | Limitations were not reliably extracted in template fallback mode. |

## Recurring Mechanisms and Patterns

- **MEDIUM** details require structured extraction linked evidence: Method details require structured LLM extraction; see linked evidence chunks.; Method details require structured LLM extraction; see linked evidence chunks.; Method details require structured LLM extraction; see linked evidence chunks. [1409.6428, 1503.00310, 1509.04238, 1603.07816, 1609.06265, 1708.02018, 1906.01753, 1908.01843, 2009.06401, 2104.05022, 2104.08413, 2106.01210, 2109.07401, 2111.08543, 2208.11125, 2210.12654, 2407.17745, 2510.03418, 2603.24246]

## Assumption Map


## Contradiction Map

- **CON-001** Potential conflict (negation detected: 'not reliably'): 1906.01753: Limitations were not reliably extracted in template fallback mode.; 2106.01210: Limitations were not reliably extracted in template fallback mode.
- **CON-002** Potential conflict (negation detected: 'not reliably'): 1906.01753: Limitations were not reliably extracted in template fallback mode.; 1509.04238: Limitations were not reliably extracted in template fallback mode.
- **CON-003** Potential conflict (negation detected: 'not reliably'): 1906.01753: Limitations were not reliably extracted in template fallback mode.; 1609.06265: Limitations were not reliably extracted in template fallback mode.
- **CON-004** Potential conflict (negation detected: 'not reliably'): 1906.01753: Limitations were not reliably extracted in template fallback mode.; 2111.08543: Limitations were not reliably extracted in template fallback mode.
- **CON-005** Potential conflict (negation detected: 'not reliably'): 1906.01753: Limitations were not reliably extracted in template fallback mode.; 2510.03418: Limitations were not reliably extracted in template fallback mode.
- **CON-006** Potential conflict (negation detected: 'not reliably'): 1906.01753: Limitations were not reliably extracted in template fallback mode.; 1503.00310: Limitations were not reliably extracted in template fallback mode.
- **CON-007** Potential conflict (negation detected: 'not reliably'): 1906.01753: Limitations were not reliably extracted in template fallback mode.; 1409.6428: Limitations were not reliably extracted in template fallback mode.
- **CON-008** Potential conflict (negation detected: 'not reliably'): 1906.01753: Limitations were not reliably extracted in template fallback mode.; 1908.01843: Limitations were not reliably extracted in template fallback mode.
- **CON-009** Potential conflict (negation detected: 'not reliably'): 1906.01753: Limitations were not reliably extracted in template fallback mode.; 2009.06401: Limitations were not reliably extracted in template fallback mode.
- **CON-010** Potential conflict (negation detected: 'not reliably'): 1906.01753: Limitations were not reliably extracted in template fallback mode.; 2407.17745: Limitations were not reliably extracted in template fallback mode.
- **CON-011** Potential conflict (negation detected: 'not reliably'): 1906.01753: Limitations were not reliably extracted in template fallback mode.; 2208.11125: Limitations were not reliably extracted in template fallback mode.
- **CON-012** Potential conflict (negation detected: 'not reliably'): 1906.01753: Limitations were not reliably extracted in template fallback mode.; 2210.12654: Limitations were not reliably extracted in template fallback mode.
- **CON-013** Potential conflict (negation detected: 'not reliably'): 1906.01753: Limitations were not reliably extracted in template fallback mode.; 2104.08413: Limitations were not reliably extracted in template fallback mode.
- **CON-014** Potential conflict (negation detected: 'not reliably'): 1906.01753: Limitations were not reliably extracted in template fallback mode.; 2104.05022: Limitations were not reliably extracted in template fallback mode.
- **CON-015** Potential conflict (negation detected: 'not reliably'): 1906.01753: Limitations were not reliably extracted in template fallback mode.; 1603.07816: Limitations were not reliably extracted in template fallback mode.
- **CON-016** Potential conflict (negation detected: 'not reliably'): 1906.01753: Limitations were not reliably extracted in template fallback mode.; 1708.02018: Limitations were not reliably extracted in template fallback mode.
- **CON-017** Potential conflict (negation detected: 'not reliably'): 1906.01753: Limitations were not reliably extracted in template fallback mode.; 2109.07401: Limitations were not reliably extracted in template fallback mode.
- **CON-018** Potential conflict (negation detected: 'not reliably'): 1906.01753: Limitations were not reliably extracted in template fallback mode.; 2603.24246: Limitations were not reliably extracted in template fallback mode.
- **CON-019** Potential conflict (negation detected: 'not reliably'): 2106.01210: Limitations were not reliably extracted in template fallback mode.; 1509.04238: Limitations were not reliably extracted in template fallback mode.
- **CON-020** Potential conflict (negation detected: 'not reliably'): 2106.01210: Limitations were not reliably extracted in template fallback mode.; 1609.06265: Limitations were not reliably extracted in template fallback mode.
- **CON-021** Potential conflict (negation detected: 'not reliably'): 2106.01210: Limitations were not reliably extracted in template fallback mode.; 2111.08543: Limitations were not reliably extracted in template fallback mode.
- **CON-022** Potential conflict (negation detected: 'not reliably'): 2106.01210: Limitations were not reliably extracted in template fallback mode.; 2510.03418: Limitations were not reliably extracted in template fallback mode.
- **CON-023** Potential conflict (negation detected: 'not reliably'): 2106.01210: Limitations were not reliably extracted in template fallback mode.; 1503.00310: Limitations were not reliably extracted in template fallback mode.
- **CON-024** Potential conflict (negation detected: 'not reliably'): 2106.01210: Limitations were not reliably extracted in template fallback mode.; 1409.6428: Limitations were not reliably extracted in template fallback mode.
- **CON-025** Potential conflict (negation detected: 'not reliably'): 2106.01210: Limitations were not reliably extracted in template fallback mode.; 1908.01843: Limitations were not reliably extracted in template fallback mode.
- **CON-026** Potential conflict (negation detected: 'not reliably'): 2106.01210: Limitations were not reliably extracted in template fallback mode.; 2009.06401: Limitations were not reliably extracted in template fallback mode.
- **CON-027** Potential conflict (negation detected: 'not reliably'): 2106.01210: Limitations were not reliably extracted in template fallback mode.; 2407.17745: Limitations were not reliably extracted in template fallback mode.
- **CON-028** Potential conflict (negation detected: 'not reliably'): 2106.01210: Limitations were not reliably extracted in template fallback mode.; 2208.11125: Limitations were not reliably extracted in template fallback mode.
- **CON-029** Potential conflict (negation detected: 'not reliably'): 2106.01210: Limitations were not reliably extracted in template fallback mode.; 2210.12654: Limitations were not reliably extracted in template fallback mode.
- **CON-030** Potential conflict (negation detected: 'not reliably'): 2106.01210: Limitations were not reliably extracted in template fallback mode.; 2104.08413: Limitations were not reliably extracted in template fallback mode.
- **CON-031** Potential conflict (negation detected: 'not reliably'): 2106.01210: Limitations were not reliably extracted in template fallback mode.; 2104.05022: Limitations were not reliably extracted in template fallback mode.
- **CON-032** Potential conflict (negation detected: 'not reliably'): 2106.01210: Limitations were not reliably extracted in template fallback mode.; 1603.07816: Limitations were not reliably extracted in template fallback mode.
- **CON-033** Potential conflict (negation detected: 'not reliably'): 2106.01210: Limitations were not reliably extracted in template fallback mode.; 1708.02018: Limitations were not reliably extracted in template fallback mode.
- **CON-034** Potential conflict (negation detected: 'not reliably'): 2106.01210: Limitations were not reliably extracted in template fallback mode.; 2109.07401: Limitations were not reliably extracted in template fallback mode.
- **CON-035** Potential conflict (negation detected: 'not reliably'): 2106.01210: Limitations were not reliably extracted in template fallback mode.; 2603.24246: Limitations were not reliably extracted in template fallback mode.
- **CON-036** Potential conflict (negation detected: 'not reliably'): 1509.04238: Limitations were not reliably extracted in template fallback mode.; 1609.06265: Limitations were not reliably extracted in template fallback mode.
- **CON-037** Potential conflict (negation detected: 'not reliably'): 1509.04238: Limitations were not reliably extracted in template fallback mode.; 2111.08543: Limitations were not reliably extracted in template fallback mode.
- **CON-038** Potential conflict (negation detected: 'not reliably'): 1509.04238: Limitations were not reliably extracted in template fallback mode.; 2510.03418: Limitations were not reliably extracted in template fallback mode.
- **CON-039** Potential conflict (negation detected: 'not reliably'): 1509.04238: Limitations were not reliably extracted in template fallback mode.; 1503.00310: Limitations were not reliably extracted in template fallback mode.
- **CON-040** Potential conflict (negation detected: 'not reliably'): 1509.04238: Limitations were not reliably extracted in template fallback mode.; 1409.6428: Limitations were not reliably extracted in template fallback mode.
- **CON-041** Potential conflict (negation detected: 'not reliably'): 1509.04238: Limitations were not reliably extracted in template fallback mode.; 1908.01843: Limitations were not reliably extracted in template fallback mode.
- **CON-042** Potential conflict (negation detected: 'not reliably'): 1509.04238: Limitations were not reliably extracted in template fallback mode.; 2009.06401: Limitations were not reliably extracted in template fallback mode.
- **CON-043** Potential conflict (negation detected: 'not reliably'): 1509.04238: Limitations were not reliably extracted in template fallback mode.; 2407.17745: Limitations were not reliably extracted in template fallback mode.
- **CON-044** Potential conflict (negation detected: 'not reliably'): 1509.04238: Limitations were not reliably extracted in template fallback mode.; 2208.11125: Limitations were not reliably extracted in template fallback mode.
- **CON-045** Potential conflict (negation detected: 'not reliably'): 1509.04238: Limitations were not reliably extracted in template fallback mode.; 2210.12654: Limitations were not reliably extracted in template fallback mode.
- **CON-046** Potential conflict (negation detected: 'not reliably'): 1509.04238: Limitations were not reliably extracted in template fallback mode.; 2104.08413: Limitations were not reliably extracted in template fallback mode.
- **CON-047** Potential conflict (negation detected: 'not reliably'): 1509.04238: Limitations were not reliably extracted in template fallback mode.; 2104.05022: Limitations were not reliably extracted in template fallback mode.
- **CON-048** Potential conflict (negation detected: 'not reliably'): 1509.04238: Limitations were not reliably extracted in template fallback mode.; 1603.07816: Limitations were not reliably extracted in template fallback mode.
- **CON-049** Potential conflict (negation detected: 'not reliably'): 1509.04238: Limitations were not reliably extracted in template fallback mode.; 1708.02018: Limitations were not reliably extracted in template fallback mode.
- **CON-050** Potential conflict (negation detected: 'not reliably'): 1509.04238: Limitations were not reliably extracted in template fallback mode.; 2109.07401: Limitations were not reliably extracted in template fallback mode.
- **CON-051** Potential conflict (negation detected: 'not reliably'): 1509.04238: Limitations were not reliably extracted in template fallback mode.; 2603.24246: Limitations were not reliably extracted in template fallback mode.
- **CON-052** Potential conflict (negation detected: 'not reliably'): 1609.06265: Limitations were not reliably extracted in template fallback mode.; 2111.08543: Limitations were not reliably extracted in template fallback mode.
- **CON-053** Potential conflict (negation detected: 'not reliably'): 1609.06265: Limitations were not reliably extracted in template fallback mode.; 2510.03418: Limitations were not reliably extracted in template fallback mode.
- **CON-054** Potential conflict (negation detected: 'not reliably'): 1609.06265: Limitations were not reliably extracted in template fallback mode.; 1503.00310: Limitations were not reliably extracted in template fallback mode.
- **CON-055** Potential conflict (negation detected: 'not reliably'): 1609.06265: Limitations were not reliably extracted in template fallback mode.; 1409.6428: Limitations were not reliably extracted in template fallback mode.
- **CON-056** Potential conflict (negation detected: 'not reliably'): 1609.06265: Limitations were not reliably extracted in template fallback mode.; 1908.01843: Limitations were not reliably extracted in template fallback mode.
- **CON-057** Potential conflict (negation detected: 'not reliably'): 1609.06265: Limitations were not reliably extracted in template fallback mode.; 2009.06401: Limitations were not reliably extracted in template fallback mode.
- **CON-058** Potential conflict (negation detected: 'not reliably'): 1609.06265: Limitations were not reliably extracted in template fallback mode.; 2407.17745: Limitations were not reliably extracted in template fallback mode.
- **CON-059** Potential conflict (negation detected: 'not reliably'): 1609.06265: Limitations were not reliably extracted in template fallback mode.; 2208.11125: Limitations were not reliably extracted in template fallback mode.
- **CON-060** Potential conflict (negation detected: 'not reliably'): 1609.06265: Limitations were not reliably extracted in template fallback mode.; 2210.12654: Limitations were not reliably extracted in template fallback mode.
- **CON-061** Potential conflict (negation detected: 'not reliably'): 1609.06265: Limitations were not reliably extracted in template fallback mode.; 2104.08413: Limitations were not reliably extracted in template fallback mode.
- **CON-062** Potential conflict (negation detected: 'not reliably'): 1609.06265: Limitations were not reliably extracted in template fallback mode.; 2104.05022: Limitations were not reliably extracted in template fallback mode.
- **CON-063** Potential conflict (negation detected: 'not reliably'): 1609.06265: Limitations were not reliably extracted in template fallback mode.; 1603.07816: Limitations were not reliably extracted in template fallback mode.
- **CON-064** Potential conflict (negation detected: 'not reliably'): 1609.06265: Limitations were not reliably extracted in template fallback mode.; 1708.02018: Limitations were not reliably extracted in template fallback mode.
- **CON-065** Potential conflict (negation detected: 'not reliably'): 1609.06265: Limitations were not reliably extracted in template fallback mode.; 2109.07401: Limitations were not reliably extracted in template fallback mode.
- **CON-066** Potential conflict (negation detected: 'not reliably'): 1609.06265: Limitations were not reliably extracted in template fallback mode.; 2603.24246: Limitations were not reliably extracted in template fallback mode.
- **CON-067** Potential conflict (negation detected: 'not reliably'): 2111.08543: Limitations were not reliably extracted in template fallback mode.; 2510.03418: Limitations were not reliably extracted in template fallback mode.
- **CON-068** Potential conflict (negation detected: 'not reliably'): 2111.08543: Limitations were not reliably extracted in template fallback mode.; 1503.00310: Limitations were not reliably extracted in template fallback mode.
- **CON-069** Potential conflict (negation detected: 'not reliably'): 2111.08543: Limitations were not reliably extracted in template fallback mode.; 1409.6428: Limitations were not reliably extracted in template fallback mode.
- **CON-070** Potential conflict (negation detected: 'not reliably'): 2111.08543: Limitations were not reliably extracted in template fallback mode.; 1908.01843: Limitations were not reliably extracted in template fallback mode.
- **CON-071** Potential conflict (negation detected: 'not reliably'): 2111.08543: Limitations were not reliably extracted in template fallback mode.; 2009.06401: Limitations were not reliably extracted in template fallback mode.
- **CON-072** Potential conflict (negation detected: 'not reliably'): 2111.08543: Limitations were not reliably extracted in template fallback mode.; 2407.17745: Limitations were not reliably extracted in template fallback mode.
- **CON-073** Potential conflict (negation detected: 'not reliably'): 2111.08543: Limitations were not reliably extracted in template fallback mode.; 2208.11125: Limitations were not reliably extracted in template fallback mode.
- **CON-074** Potential conflict (negation detected: 'not reliably'): 2111.08543: Limitations were not reliably extracted in template fallback mode.; 2210.12654: Limitations were not reliably extracted in template fallback mode.
- **CON-075** Potential conflict (negation detected: 'not reliably'): 2111.08543: Limitations were not reliably extracted in template fallback mode.; 2104.08413: Limitations were not reliably extracted in template fallback mode.
- **CON-076** Potential conflict (negation detected: 'not reliably'): 2111.08543: Limitations were not reliably extracted in template fallback mode.; 2104.05022: Limitations were not reliably extracted in template fallback mode.
- **CON-077** Potential conflict (negation detected: 'not reliably'): 2111.08543: Limitations were not reliably extracted in template fallback mode.; 1603.07816: Limitations were not reliably extracted in template fallback mode.
- **CON-078** Potential conflict (negation detected: 'not reliably'): 2111.08543: Limitations were not reliably extracted in template fallback mode.; 1708.02018: Limitations were not reliably extracted in template fallback mode.
- **CON-079** Potential conflict (negation detected: 'not reliably'): 2111.08543: Limitations were not reliably extracted in template fallback mode.; 2109.07401: Limitations were not reliably extracted in template fallback mode.
- **CON-080** Potential conflict (negation detected: 'not reliably'): 2111.08543: Limitations were not reliably extracted in template fallback mode.; 2603.24246: Limitations were not reliably extracted in template fallback mode.
- **CON-081** Potential conflict (negation detected: 'not reliably'): 2510.03418: Limitations were not reliably extracted in template fallback mode.; 1503.00310: Limitations were not reliably extracted in template fallback mode.
- **CON-082** Potential conflict (negation detected: 'not reliably'): 2510.03418: Limitations were not reliably extracted in template fallback mode.; 1409.6428: Limitations were not reliably extracted in template fallback mode.
- **CON-083** Potential conflict (negation detected: 'not reliably'): 2510.03418: Limitations were not reliably extracted in template fallback mode.; 1908.01843: Limitations were not reliably extracted in template fallback mode.
- **CON-084** Potential conflict (negation detected: 'not reliably'): 2510.03418: Limitations were not reliably extracted in template fallback mode.; 2009.06401: Limitations were not reliably extracted in template fallback mode.
- **CON-085** Potential conflict (negation detected: 'not reliably'): 2510.03418: Limitations were not reliably extracted in template fallback mode.; 2407.17745: Limitations were not reliably extracted in template fallback mode.
- **CON-086** Potential conflict (negation detected: 'not reliably'): 2510.03418: Limitations were not reliably extracted in template fallback mode.; 2208.11125: Limitations were not reliably extracted in template fallback mode.
- **CON-087** Potential conflict (negation detected: 'not reliably'): 2510.03418: Limitations were not reliably extracted in template fallback mode.; 2210.12654: Limitations were not reliably extracted in template fallback mode.
- **CON-088** Potential conflict (negation detected: 'not reliably'): 2510.03418: Limitations were not reliably extracted in template fallback mode.; 2104.08413: Limitations were not reliably extracted in template fallback mode.
- **CON-089** Potential conflict (negation detected: 'not reliably'): 2510.03418: Limitations were not reliably extracted in template fallback mode.; 2104.05022: Limitations were not reliably extracted in template fallback mode.
- **CON-090** Potential conflict (negation detected: 'not reliably'): 2510.03418: Limitations were not reliably extracted in template fallback mode.; 1603.07816: Limitations were not reliably extracted in template fallback mode.
- **CON-091** Potential conflict (negation detected: 'not reliably'): 2510.03418: Limitations were not reliably extracted in template fallback mode.; 1708.02018: Limitations were not reliably extracted in template fallback mode.
- **CON-092** Potential conflict (negation detected: 'not reliably'): 2510.03418: Limitations were not reliably extracted in template fallback mode.; 2109.07401: Limitations were not reliably extracted in template fallback mode.
- **CON-093** Potential conflict (negation detected: 'not reliably'): 2510.03418: Limitations were not reliably extracted in template fallback mode.; 2603.24246: Limitations were not reliably extracted in template fallback mode.
- **CON-094** Potential conflict (negation detected: 'not reliably'): 1503.00310: Limitations were not reliably extracted in template fallback mode.; 1409.6428: Limitations were not reliably extracted in template fallback mode.
- **CON-095** Potential conflict (negation detected: 'not reliably'): 1503.00310: Limitations were not reliably extracted in template fallback mode.; 1908.01843: Limitations were not reliably extracted in template fallback mode.
- **CON-096** Potential conflict (negation detected: 'not reliably'): 1503.00310: Limitations were not reliably extracted in template fallback mode.; 2009.06401: Limitations were not reliably extracted in template fallback mode.
- **CON-097** Potential conflict (negation detected: 'not reliably'): 1503.00310: Limitations were not reliably extracted in template fallback mode.; 2407.17745: Limitations were not reliably extracted in template fallback mode.
- **CON-098** Potential conflict (negation detected: 'not reliably'): 1503.00310: Limitations were not reliably extracted in template fallback mode.; 2208.11125: Limitations were not reliably extracted in template fallback mode.
- **CON-099** Potential conflict (negation detected: 'not reliably'): 1503.00310: Limitations were not reliably extracted in template fallback mode.; 2210.12654: Limitations were not reliably extracted in template fallback mode.
- **CON-100** Potential conflict (negation detected: 'not reliably'): 1503.00310: Limitations were not reliably extracted in template fallback mode.; 2104.08413: Limitations were not reliably extracted in template fallback mode.
- **CON-101** Potential conflict (negation detected: 'not reliably'): 1503.00310: Limitations were not reliably extracted in template fallback mode.; 2104.05022: Limitations were not reliably extracted in template fallback mode.
- **CON-102** Potential conflict (negation detected: 'not reliably'): 1503.00310: Limitations were not reliably extracted in template fallback mode.; 1603.07816: Limitations were not reliably extracted in template fallback mode.
- **CON-103** Potential conflict (negation detected: 'not reliably'): 1503.00310: Limitations were not reliably extracted in template fallback mode.; 1708.02018: Limitations were not reliably extracted in template fallback mode.
- **CON-104** Potential conflict (negation detected: 'not reliably'): 1503.00310: Limitations were not reliably extracted in template fallback mode.; 2109.07401: Limitations were not reliably extracted in template fallback mode.
- **CON-105** Potential conflict (negation detected: 'not reliably'): 1503.00310: Limitations were not reliably extracted in template fallback mode.; 2603.24246: Limitations were not reliably extracted in template fallback mode.
- **CON-106** Potential conflict (negation detected: 'not reliably'): 1409.6428: Limitations were not reliably extracted in template fallback mode.; 1908.01843: Limitations were not reliably extracted in template fallback mode.
- **CON-107** Potential conflict (negation detected: 'not reliably'): 1409.6428: Limitations were not reliably extracted in template fallback mode.; 2009.06401: Limitations were not reliably extracted in template fallback mode.
- **CON-108** Potential conflict (negation detected: 'not reliably'): 1409.6428: Limitations were not reliably extracted in template fallback mode.; 2407.17745: Limitations were not reliably extracted in template fallback mode.
- **CON-109** Potential conflict (negation detected: 'not reliably'): 1409.6428: Limitations were not reliably extracted in template fallback mode.; 2208.11125: Limitations were not reliably extracted in template fallback mode.
- **CON-110** Potential conflict (negation detected: 'not reliably'): 1409.6428: Limitations were not reliably extracted in template fallback mode.; 2210.12654: Limitations were not reliably extracted in template fallback mode.
- **CON-111** Potential conflict (negation detected: 'not reliably'): 1409.6428: Limitations were not reliably extracted in template fallback mode.; 2104.08413: Limitations were not reliably extracted in template fallback mode.
- **CON-112** Potential conflict (negation detected: 'not reliably'): 1409.6428: Limitations were not reliably extracted in template fallback mode.; 2104.05022: Limitations were not reliably extracted in template fallback mode.
- **CON-113** Potential conflict (negation detected: 'not reliably'): 1409.6428: Limitations were not reliably extracted in template fallback mode.; 1603.07816: Limitations were not reliably extracted in template fallback mode.
- **CON-114** Potential conflict (negation detected: 'not reliably'): 1409.6428: Limitations were not reliably extracted in template fallback mode.; 1708.02018: Limitations were not reliably extracted in template fallback mode.
- **CON-115** Potential conflict (negation detected: 'not reliably'): 1409.6428: Limitations were not reliably extracted in template fallback mode.; 2109.07401: Limitations were not reliably extracted in template fallback mode.
- **CON-116** Potential conflict (negation detected: 'not reliably'): 1409.6428: Limitations were not reliably extracted in template fallback mode.; 2603.24246: Limitations were not reliably extracted in template fallback mode.
- **CON-117** Potential conflict (negation detected: 'not reliably'): 1908.01843: Limitations were not reliably extracted in template fallback mode.; 2009.06401: Limitations were not reliably extracted in template fallback mode.
- **CON-118** Potential conflict (negation detected: 'not reliably'): 1908.01843: Limitations were not reliably extracted in template fallback mode.; 2407.17745: Limitations were not reliably extracted in template fallback mode.
- **CON-119** Potential conflict (negation detected: 'not reliably'): 1908.01843: Limitations were not reliably extracted in template fallback mode.; 2208.11125: Limitations were not reliably extracted in template fallback mode.
- **CON-120** Potential conflict (negation detected: 'not reliably'): 1908.01843: Limitations were not reliably extracted in template fallback mode.; 2210.12654: Limitations were not reliably extracted in template fallback mode.
- **CON-121** Potential conflict (negation detected: 'not reliably'): 1908.01843: Limitations were not reliably extracted in template fallback mode.; 2104.08413: Limitations were not reliably extracted in template fallback mode.
- **CON-122** Potential conflict (negation detected: 'not reliably'): 1908.01843: Limitations were not reliably extracted in template fallback mode.; 2104.05022: Limitations were not reliably extracted in template fallback mode.
- **CON-123** Potential conflict (negation detected: 'not reliably'): 1908.01843: Limitations were not reliably extracted in template fallback mode.; 1603.07816: Limitations were not reliably extracted in template fallback mode.
- **CON-124** Potential conflict (negation detected: 'not reliably'): 1908.01843: Limitations were not reliably extracted in template fallback mode.; 1708.02018: Limitations were not reliably extracted in template fallback mode.
- **CON-125** Potential conflict (negation detected: 'not reliably'): 1908.01843: Limitations were not reliably extracted in template fallback mode.; 2109.07401: Limitations were not reliably extracted in template fallback mode.
- **CON-126** Potential conflict (negation detected: 'not reliably'): 1908.01843: Limitations were not reliably extracted in template fallback mode.; 2603.24246: Limitations were not reliably extracted in template fallback mode.
- **CON-127** Potential conflict (negation detected: 'not reliably'): 2009.06401: Limitations were not reliably extracted in template fallback mode.; 2407.17745: Limitations were not reliably extracted in template fallback mode.
- **CON-128** Potential conflict (negation detected: 'not reliably'): 2009.06401: Limitations were not reliably extracted in template fallback mode.; 2208.11125: Limitations were not reliably extracted in template fallback mode.
- **CON-129** Potential conflict (negation detected: 'not reliably'): 2009.06401: Limitations were not reliably extracted in template fallback mode.; 2210.12654: Limitations were not reliably extracted in template fallback mode.
- **CON-130** Potential conflict (negation detected: 'not reliably'): 2009.06401: Limitations were not reliably extracted in template fallback mode.; 2104.08413: Limitations were not reliably extracted in template fallback mode.
- **CON-131** Potential conflict (negation detected: 'not reliably'): 2009.06401: Limitations were not reliably extracted in template fallback mode.; 2104.05022: Limitations were not reliably extracted in template fallback mode.
- **CON-132** Potential conflict (negation detected: 'not reliably'): 2009.06401: Limitations were not reliably extracted in template fallback mode.; 1603.07816: Limitations were not reliably extracted in template fallback mode.
- **CON-133** Potential conflict (negation detected: 'not reliably'): 2009.06401: Limitations were not reliably extracted in template fallback mode.; 1708.02018: Limitations were not reliably extracted in template fallback mode.
- **CON-134** Potential conflict (negation detected: 'not reliably'): 2009.06401: Limitations were not reliably extracted in template fallback mode.; 2109.07401: Limitations were not reliably extracted in template fallback mode.
- **CON-135** Potential conflict (negation detected: 'not reliably'): 2009.06401: Limitations were not reliably extracted in template fallback mode.; 2603.24246: Limitations were not reliably extracted in template fallback mode.
- **CON-136** Potential conflict (negation detected: 'not reliably'): 2407.17745: Limitations were not reliably extracted in template fallback mode.; 2208.11125: Limitations were not reliably extracted in template fallback mode.
- **CON-137** Potential conflict (negation detected: 'not reliably'): 2407.17745: Limitations were not reliably extracted in template fallback mode.; 2210.12654: Limitations were not reliably extracted in template fallback mode.
- **CON-138** Potential conflict (negation detected: 'not reliably'): 2407.17745: Limitations were not reliably extracted in template fallback mode.; 2104.08413: Limitations were not reliably extracted in template fallback mode.
- **CON-139** Potential conflict (negation detected: 'not reliably'): 2407.17745: Limitations were not reliably extracted in template fallback mode.; 2104.05022: Limitations were not reliably extracted in template fallback mode.
- **CON-140** Potential conflict (negation detected: 'not reliably'): 2407.17745: Limitations were not reliably extracted in template fallback mode.; 1603.07816: Limitations were not reliably extracted in template fallback mode.
- **CON-141** Potential conflict (negation detected: 'not reliably'): 2407.17745: Limitations were not reliably extracted in template fallback mode.; 1708.02018: Limitations were not reliably extracted in template fallback mode.
- **CON-142** Potential conflict (negation detected: 'not reliably'): 2407.17745: Limitations were not reliably extracted in template fallback mode.; 2109.07401: Limitations were not reliably extracted in template fallback mode.
- **CON-143** Potential conflict (negation detected: 'not reliably'): 2407.17745: Limitations were not reliably extracted in template fallback mode.; 2603.24246: Limitations were not reliably extracted in template fallback mode.
- **CON-144** Potential conflict (negation detected: 'not reliably'): 2208.11125: Limitations were not reliably extracted in template fallback mode.; 2210.12654: Limitations were not reliably extracted in template fallback mode.
- **CON-145** Potential conflict (negation detected: 'not reliably'): 2208.11125: Limitations were not reliably extracted in template fallback mode.; 2104.08413: Limitations were not reliably extracted in template fallback mode.
- **CON-146** Potential conflict (negation detected: 'not reliably'): 2208.11125: Limitations were not reliably extracted in template fallback mode.; 2104.05022: Limitations were not reliably extracted in template fallback mode.
- **CON-147** Potential conflict (negation detected: 'not reliably'): 2208.11125: Limitations were not reliably extracted in template fallback mode.; 1603.07816: Limitations were not reliably extracted in template fallback mode.
- **CON-148** Potential conflict (negation detected: 'not reliably'): 2208.11125: Limitations were not reliably extracted in template fallback mode.; 1708.02018: Limitations were not reliably extracted in template fallback mode.
- **CON-149** Potential conflict (negation detected: 'not reliably'): 2208.11125: Limitations were not reliably extracted in template fallback mode.; 2109.07401: Limitations were not reliably extracted in template fallback mode.
- **CON-150** Potential conflict (negation detected: 'not reliably'): 2208.11125: Limitations were not reliably extracted in template fallback mode.; 2603.24246: Limitations were not reliably extracted in template fallback mode.
- **CON-151** Potential conflict (negation detected: 'not reliably'): 2210.12654: Limitations were not reliably extracted in template fallback mode.; 2104.08413: Limitations were not reliably extracted in template fallback mode.
- **CON-152** Potential conflict (negation detected: 'not reliably'): 2210.12654: Limitations were not reliably extracted in template fallback mode.; 2104.05022: Limitations were not reliably extracted in template fallback mode.
- **CON-153** Potential conflict (negation detected: 'not reliably'): 2210.12654: Limitations were not reliably extracted in template fallback mode.; 1603.07816: Limitations were not reliably extracted in template fallback mode.
- **CON-154** Potential conflict (negation detected: 'not reliably'): 2210.12654: Limitations were not reliably extracted in template fallback mode.; 1708.02018: Limitations were not reliably extracted in template fallback mode.
- **CON-155** Potential conflict (negation detected: 'not reliably'): 2210.12654: Limitations were not reliably extracted in template fallback mode.; 2109.07401: Limitations were not reliably extracted in template fallback mode.
- **CON-156** Potential conflict (negation detected: 'not reliably'): 2210.12654: Limitations were not reliably extracted in template fallback mode.; 2603.24246: Limitations were not reliably extracted in template fallback mode.
- **CON-157** Potential conflict (negation detected: 'not reliably'): 2104.08413: Limitations were not reliably extracted in template fallback mode.; 2104.05022: Limitations were not reliably extracted in template fallback mode.
- **CON-158** Potential conflict (negation detected: 'not reliably'): 2104.08413: Limitations were not reliably extracted in template fallback mode.; 1603.07816: Limitations were not reliably extracted in template fallback mode.
- **CON-159** Potential conflict (negation detected: 'not reliably'): 2104.08413: Limitations were not reliably extracted in template fallback mode.; 1708.02018: Limitations were not reliably extracted in template fallback mode.
- **CON-160** Potential conflict (negation detected: 'not reliably'): 2104.08413: Limitations were not reliably extracted in template fallback mode.; 2109.07401: Limitations were not reliably extracted in template fallback mode.
- **CON-161** Potential conflict (negation detected: 'not reliably'): 2104.08413: Limitations were not reliably extracted in template fallback mode.; 2603.24246: Limitations were not reliably extracted in template fallback mode.
- **CON-162** Potential conflict (negation detected: 'not reliably'): 2104.05022: Limitations were not reliably extracted in template fallback mode.; 1603.07816: Limitations were not reliably extracted in template fallback mode.
- **CON-163** Potential conflict (negation detected: 'not reliably'): 2104.05022: Limitations were not reliably extracted in template fallback mode.; 1708.02018: Limitations were not reliably extracted in template fallback mode.
- **CON-164** Potential conflict (negation detected: 'not reliably'): 2104.05022: Limitations were not reliably extracted in template fallback mode.; 2109.07401: Limitations were not reliably extracted in template fallback mode.
- **CON-165** Potential conflict (negation detected: 'not reliably'): 2104.05022: Limitations were not reliably extracted in template fallback mode.; 2603.24246: Limitations were not reliably extracted in template fallback mode.
- **CON-166** Potential conflict (negation detected: 'not reliably'): 1603.07816: Limitations were not reliably extracted in template fallback mode.; 1708.02018: Limitations were not reliably extracted in template fallback mode.
- **CON-167** Potential conflict (negation detected: 'not reliably'): 1603.07816: Limitations were not reliably extracted in template fallback mode.; 2109.07401: Limitations were not reliably extracted in template fallback mode.
- **CON-168** Potential conflict (negation detected: 'not reliably'): 1603.07816: Limitations were not reliably extracted in template fallback mode.; 2603.24246: Limitations were not reliably extracted in template fallback mode.
- **CON-169** Potential conflict (negation detected: 'not reliably'): 1708.02018: Limitations were not reliably extracted in template fallback mode.; 2109.07401: Limitations were not reliably extracted in template fallback mode.
- **CON-170** Potential conflict (negation detected: 'not reliably'): 1708.02018: Limitations were not reliably extracted in template fallback mode.; 2603.24246: Limitations were not reliably extracted in template fallback mode.
- **CON-171** Potential conflict (negation detected: 'not reliably'): 2109.07401: Limitations were not reliably extracted in template fallback mode.; 2603.24246: Limitations were not reliably extracted in template fallback mode.

## Evidence Strength Map

- **MEDIUM** details require structured extraction linked evidence: Method details require structured LLM extraction; see linked evidence chunks.; Method details require structured LLM extraction; see linked evidence chunks.; Method details require structured LLM extraction; see linked evidence chunks. [evidence: E001, E004, E007, E009, E010]
- **MEDIUM** require structured extraction linked evidence chunks: Results require structured LLM extraction; see linked evidence chunks.; Results require structured LLM extraction; see linked evidence chunks.; Results require structured LLM extraction; see linked evidence chunks. [evidence: E001, E003, E004, E006, E007, E009, E010]

## Operational Implications


## Production Readiness

- **LOW** 1906.01753: theoretical or not reported
- **LOW** 2106.01210: theoretical or not reported
- **LOW** 1509.04238: theoretical or not reported
- **LOW** 1609.06265: theoretical or not reported
- **LOW** 2111.08543: theoretical or not reported
- **LOW** 2510.03418: theoretical or not reported
- **LOW** 1503.00310: theoretical or not reported
- **LOW** 1409.6428: theoretical or not reported
- **LOW** 1908.01843: theoretical or not reported
- **LOW** 2009.06401: theoretical or not reported
- **LOW** 2407.17745: theoretical or not reported
- **LOW** 2208.11125: theoretical or not reported
- **LOW** 2210.12654: theoretical or not reported
- **LOW** 2104.08413: theoretical or not reported
- **LOW** 2104.05022: theoretical or not reported
- **LOW** 1603.07816: theoretical or not reported
- **LOW** 1708.02018: theoretical or not reported
- **LOW** 2109.07401: theoretical or not reported
- **LOW** 2603.24246: theoretical or not reported

## Reusable Mechanism Inventory

- **MECH-001** Method details require structured LLM...: Method details require structured LLM extraction; see linked evidence chunks. [1906.01753]
- **MECH-002** Method details require structured LLM...: Method details require structured LLM extraction; see linked evidence chunks. [2106.01210]
- **MECH-003** Method details require structured LLM...: Method details require structured LLM extraction; see linked evidence chunks. [1509.04238]
- **MECH-004** Method details require structured LLM...: Method details require structured LLM extraction; see linked evidence chunks. [1609.06265]
- **MECH-005** Method details require structured LLM...: Method details require structured LLM extraction; see linked evidence chunks. [2111.08543]
- **MECH-006** Method details require structured LLM...: Method details require structured LLM extraction; see linked evidence chunks. [2510.03418]
- **MECH-007** Method details require structured LLM...: Method details require structured LLM extraction; see linked evidence chunks. [1503.00310]
- **MECH-008** Method details require structured LLM...: Method details require structured LLM extraction; see linked evidence chunks. [1409.6428]
- **MECH-009** Method details require structured LLM...: Method details require structured LLM extraction; see linked evidence chunks. [1908.01843]
- **MECH-010** Method details require structured LLM...: Method details require structured LLM extraction; see linked evidence chunks. [2009.06401]
- **MECH-011** Method details require structured LLM...: Method details require structured LLM extraction; see linked evidence chunks. [2407.17745]
- **MECH-012** Method details require structured LLM...: Method details require structured LLM extraction; see linked evidence chunks. [2208.11125]
- **MECH-013** Method details require structured LLM...: Method details require structured LLM extraction; see linked evidence chunks. [2210.12654]
- **MECH-014** Method details require structured LLM...: Method details require structured LLM extraction; see linked evidence chunks. [2104.08413]
- **MECH-015** Method details require structured LLM...: Method details require structured LLM extraction; see linked evidence chunks. [2104.05022]
- **MECH-016** Method details require structured LLM...: Method details require structured LLM extraction; see linked evidence chunks. [1603.07816]
- **MECH-017** Method details require structured LLM...: Method details require structured LLM extraction; see linked evidence chunks. [1708.02018]
- **MECH-018** Method details require structured LLM...: Method details require structured LLM extraction; see linked evidence chunks. [2109.07401]
- **MECH-019** Method details require structured LLM...: Method details require structured LLM extraction; see linked evidence chunks. [2603.24246]

## Design Implications

- **MEDIUM** If the target requirements match this evidence context, consider the trade-off described by: details require structured extraction linked evidence: Method details require structured LLM extraction; see linked evidence chunks.; Method details require structured LLM extraction; see linked evidence chunks.; Method details require structured LLM extraction; see linked evidence chunks.

## Unresolved Questions

- [1906.01753] Full structured LLM extraction not enabled.
- [1906.01753] Missing critical field: contributions
- [1906.01753] Missing critical field: assumptions
- [2106.01210] Full structured LLM extraction not enabled.
- [2106.01210] Missing critical field: contributions
- [2106.01210] Missing critical field: assumptions
- [1509.04238] Full structured LLM extraction not enabled.
- [1509.04238] Missing critical field: contributions
- [1509.04238] Missing critical field: assumptions
- [1609.06265] Full structured LLM extraction not enabled.
- [1609.06265] Missing critical field: contributions
- [1609.06265] Missing critical field: assumptions
- [2111.08543] Full structured LLM extraction not enabled.
- [2111.08543] Missing critical field: contributions
- [2111.08543] Missing critical field: assumptions
- [2510.03418] Full structured LLM extraction not enabled.
- [2510.03418] Missing critical field: contributions
- [2510.03418] Missing critical field: assumptions
- [1503.00310] Full structured LLM extraction not enabled.
- [1503.00310] Missing critical field: contributions
- [1503.00310] Missing critical field: assumptions
- [1409.6428] Full structured LLM extraction not enabled.
- [1409.6428] Missing critical field: contributions
- [1409.6428] Missing critical field: assumptions
- [1908.01843] Full structured LLM extraction not enabled.
- [1908.01843] Missing critical field: contributions
- [1908.01843] Missing critical field: assumptions
- [2009.06401] Full structured LLM extraction not enabled.
- [2009.06401] Missing critical field: contributions
- [2009.06401] Missing critical field: assumptions
- [2407.17745] Full structured LLM extraction not enabled.
- [2407.17745] Missing critical field: contributions
- [2407.17745] Missing critical field: assumptions
- [2208.11125] Full structured LLM extraction not enabled.
- [2208.11125] Missing critical field: contributions
- [2208.11125] Missing critical field: assumptions
- [2210.12654] Full structured LLM extraction not enabled.
- [2210.12654] Missing critical field: contributions
- [2210.12654] Missing critical field: assumptions
- [2104.08413] Full structured LLM extraction not enabled.
- [2104.08413] Missing critical field: contributions
- [2104.08413] Missing critical field: assumptions
- [2104.05022] Full structured LLM extraction not enabled.
- [2104.05022] Missing critical field: contributions
- [2104.05022] Missing critical field: assumptions
- [1603.07816] Full structured LLM extraction not enabled.
- [1603.07816] Missing critical field: contributions
- [1603.07816] Missing critical field: assumptions
- [1708.02018] Full structured LLM extraction not enabled.
- [1708.02018] Missing critical field: contributions
- [1708.02018] Missing critical field: assumptions
- [2109.07401] Full structured LLM extraction not enabled.
- [2109.07401] Missing critical field: contributions
- [2109.07401] Missing critical field: assumptions
- [2603.24246] Full structured LLM extraction not enabled.
- [2603.24246] Missing critical field: contributions
- [2603.24246] Missing critical field: assumptions
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?
- How should downstream design handle Potential conflict (negation detected: 'not reliably')?

## Risk Register

- **LOW** Limitation risk: Limitations were not reliably extracted in template fallback mode.
- **LOW** Limitation risk: Limitations were not reliably extracted in template fallback mode.
- **LOW** Limitation risk: Limitations were not reliably extracted in template fallback mode.
- **LOW** Limitation risk: Limitations were not reliably extracted in template fallback mode.
- **LOW** Limitation risk: Limitations were not reliably extracted in template fallback mode.
- **LOW** Limitation risk: Limitations were not reliably extracted in template fallback mode.
- **LOW** Limitation risk: Limitations were not reliably extracted in template fallback mode.
- **LOW** Limitation risk: Limitations were not reliably extracted in template fallback mode.
- **LOW** Limitation risk: Limitations were not reliably extracted in template fallback mode.
- **LOW** Limitation risk: Limitations were not reliably extracted in template fallback mode.
- **LOW** Limitation risk: Limitations were not reliably extracted in template fallback mode.
- **LOW** Limitation risk: Limitations were not reliably extracted in template fallback mode.
- **LOW** Limitation risk: Limitations were not reliably extracted in template fallback mode.
- **LOW** Limitation risk: Limitations were not reliably extracted in template fallback mode.
- **LOW** Limitation risk: Limitations were not reliably extracted in template fallback mode.
- **LOW** Limitation risk: Limitations were not reliably extracted in template fallback mode.
- **LOW** Limitation risk: Limitations were not reliably extracted in template fallback mode.
- **LOW** Limitation risk: Limitations were not reliably extracted in template fallback mode.
- **LOW** Limitation risk: Limitations were not reliably extracted in template fallback mode.
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')
- **MEDIUM** Contradiction risk: Potential conflict (negation detected: 'not reliably')

## Traceability Appendix

| item_id | item_type | papers | evidence_ids | confidence |
| --- | --- | --- | --- | --- |
| TAX-001 | taxonomy | 1409.6428, 1503.00310, 1509.04238, 1603.07816, 1609.06265, 1708.02018, 1906.01753, 1908.01843, 2009.06401, 2104.05022, 2104.08413, 2106.01210, 2109.07401, 2111.08543, 2208.11125, 2210.12654, 2407.17745, 2510.03418, 2603.24246 | E001, E004, E007, E009, E010 | MEDIUM |
| PAT-001 | recurring_pattern | 1409.6428, 1503.00310, 1509.04238, 1603.07816, 1609.06265, 1708.02018, 1906.01753, 1908.01843, 2009.06401, 2104.05022, 2104.08413, 2106.01210, 2109.07401, 2111.08543, 2208.11125, 2210.12654, 2407.17745, 2510.03418, 2603.24246 | E001, E004, E007, E009, E010 | MEDIUM |
| PAT-001 | recurring_pattern | 1409.6428, 1503.00310, 1509.04238, 1603.07816, 1609.06265, 1708.02018, 1906.01753, 1908.01843, 2009.06401, 2104.05022, 2104.08413, 2106.01210, 2109.07401, 2111.08543, 2208.11125, 2210.12654, 2407.17745, 2510.03418, 2603.24246 | E001, E004, E007, E009, E010 | MEDIUM |
| EVS-002 | evidence_strength | 1409.6428, 1503.00310, 1509.04238, 1603.07816, 1609.06265, 1708.02018, 1906.01753, 1908.01843, 2009.06401, 2104.05022, 2104.08413, 2106.01210, 2109.07401, 2111.08543, 2208.11125, 2210.12654, 2407.17745, 2510.03418, 2603.24246 | E001, E003, E004, E006, E007, E009, E010 | MEDIUM |
| PRD-001 | production_readiness | 1906.01753 | E009 | LOW |
| PRD-002 | production_readiness | 2106.01210 | E009 | LOW |
| PRD-003 | production_readiness | 1509.04238 | E004 | LOW |
| PRD-004 | production_readiness | 1609.06265 | E010 | LOW |
| PRD-005 | production_readiness | 2111.08543 | E001 | LOW |
| PRD-006 | production_readiness | 2510.03418 | E001 | LOW |
| PRD-007 | production_readiness | 1503.00310 | E001 | LOW |
| PRD-008 | production_readiness | 1409.6428 | E010 | LOW |
| PRD-009 | production_readiness | 1908.01843 | E001 | LOW |
| PRD-010 | production_readiness | 2009.06401 | E007 | LOW |
| PRD-011 | production_readiness | 2407.17745 | E009 | LOW |
| PRD-012 | production_readiness | 2208.11125 | E006 | LOW |
| PRD-013 | production_readiness | 2210.12654 | E009 | LOW |
| PRD-014 | production_readiness | 2104.08413 | E001 | LOW |
| PRD-015 | production_readiness | 2104.05022 | E010 | LOW |
| PRD-016 | production_readiness | 1603.07816 | E001 | LOW |
| PRD-017 | production_readiness | 1708.02018 | E003 | LOW |
| PRD-018 | production_readiness | 2109.07401 | E006 | LOW |
| PRD-019 | production_readiness | 2603.24246 | E001 | LOW |
| DES-001 | design_implication | 1409.6428, 1503.00310, 1509.04238, 1603.07816, 1609.06265, 1708.02018, 1906.01753, 1908.01843, 2009.06401, 2104.05022, 2104.08413, 2106.01210, 2109.07401, 2111.08543, 2208.11125, 2210.12654, 2407.17745, 2510.03418, 2603.24246 | E001, E004, E007, E009, E010 | MEDIUM |
| RSK-001 | risk | 1906.01753 | E001 | LOW |
| RSK-002 | risk | 2106.01210 | E003 | LOW |
| RSK-003 | risk | 1509.04238 | E001 | LOW |
| RSK-004 | risk | 1609.06265 | E001 | LOW |
| RSK-005 | risk | 2111.08543 | E001 | LOW |
| RSK-006 | risk | 2510.03418 | E006 | LOW |
| RSK-007 | risk | 1503.00310 | E001 | LOW |
| RSK-008 | risk | 1409.6428 | E001 | LOW |
| RSK-009 | risk | 1908.01843 | E001 | LOW |
| RSK-010 | risk | 2009.06401 | E008 | LOW |
| RSK-011 | risk | 2407.17745 | E001 | LOW |
| RSK-012 | risk | 2208.11125 | E001 | LOW |
| RSK-013 | risk | 2210.12654 | E006 | LOW |
| RSK-014 | risk | 2104.08413 | E001 | LOW |
| RSK-015 | risk | 2104.05022 | E001 | LOW |
| RSK-016 | risk | 1603.07816 | E001 | LOW |
| RSK-017 | risk | 1708.02018 | E001 | LOW |
| RSK-018 | risk | 2109.07401 | E001 | LOW |
| RSK-019 | risk | 2603.24246 | E001 | LOW |
| RSK-020 | risk | 1906.01753, 2106.01210 | E001, E003 | MEDIUM |
| RSK-021 | risk | 1509.04238, 1906.01753 | E001 | MEDIUM |
| RSK-022 | risk | 1609.06265, 1906.01753 | E001 | MEDIUM |
| RSK-023 | risk | 1906.01753, 2111.08543 | E001 | MEDIUM |
| RSK-024 | risk | 1906.01753, 2510.03418 | E001, E006 | MEDIUM |
| RSK-025 | risk | 1503.00310, 1906.01753 | E001 | MEDIUM |
| RSK-026 | risk | 1409.6428, 1906.01753 | E001 | MEDIUM |
| RSK-027 | risk | 1906.01753, 1908.01843 | E001 | MEDIUM |
| RSK-028 | risk | 1906.01753, 2009.06401 | E001, E008 | MEDIUM |
| RSK-029 | risk | 1906.01753, 2407.17745 | E001 | MEDIUM |
| RSK-030 | risk | 1906.01753, 2208.11125 | E001 | MEDIUM |
| RSK-031 | risk | 1906.01753, 2210.12654 | E001, E006 | MEDIUM |
| RSK-032 | risk | 1906.01753, 2104.08413 | E001 | MEDIUM |
| RSK-033 | risk | 1906.01753, 2104.05022 | E001 | MEDIUM |
| RSK-034 | risk | 1603.07816, 1906.01753 | E001 | MEDIUM |
| RSK-035 | risk | 1708.02018, 1906.01753 | E001 | MEDIUM |
| RSK-036 | risk | 1906.01753, 2109.07401 | E001 | MEDIUM |
| RSK-037 | risk | 1906.01753, 2603.24246 | E001 | MEDIUM |
| RSK-038 | risk | 1509.04238, 2106.01210 | E001, E003 | MEDIUM |
| RSK-039 | risk | 1609.06265, 2106.01210 | E001, E003 | MEDIUM |
| RSK-040 | risk | 2106.01210, 2111.08543 | E001, E003 | MEDIUM |
| RSK-041 | risk | 2106.01210, 2510.03418 | E003, E006 | MEDIUM |
| RSK-042 | risk | 1503.00310, 2106.01210 | E001, E003 | MEDIUM |
| RSK-043 | risk | 1409.6428, 2106.01210 | E001, E003 | MEDIUM |
| RSK-044 | risk | 1908.01843, 2106.01210 | E001, E003 | MEDIUM |
| RSK-045 | risk | 2009.06401, 2106.01210 | E003, E008 | MEDIUM |
| RSK-046 | risk | 2106.01210, 2407.17745 | E001, E003 | MEDIUM |
| RSK-047 | risk | 2106.01210, 2208.11125 | E001, E003 | MEDIUM |
| RSK-048 | risk | 2106.01210, 2210.12654 | E003, E006 | MEDIUM |
| RSK-049 | risk | 2104.08413, 2106.01210 | E001, E003 | MEDIUM |
| RSK-050 | risk | 2104.05022, 2106.01210 | E001, E003 | MEDIUM |
| RSK-051 | risk | 1603.07816, 2106.01210 | E001, E003 | MEDIUM |
| RSK-052 | risk | 1708.02018, 2106.01210 | E001, E003 | MEDIUM |
| RSK-053 | risk | 2106.01210, 2109.07401 | E001, E003 | MEDIUM |
| RSK-054 | risk | 2106.01210, 2603.24246 | E001, E003 | MEDIUM |
| RSK-055 | risk | 1509.04238, 1609.06265 | E001 | MEDIUM |
| RSK-056 | risk | 1509.04238, 2111.08543 | E001 | MEDIUM |
| RSK-057 | risk | 1509.04238, 2510.03418 | E001, E006 | MEDIUM |
| RSK-058 | risk | 1503.00310, 1509.04238 | E001 | MEDIUM |
| RSK-059 | risk | 1409.6428, 1509.04238 | E001 | MEDIUM |
| RSK-060 | risk | 1509.04238, 1908.01843 | E001 | MEDIUM |
| RSK-061 | risk | 1509.04238, 2009.06401 | E001, E008 | MEDIUM |
| RSK-062 | risk | 1509.04238, 2407.17745 | E001 | MEDIUM |
| RSK-063 | risk | 1509.04238, 2208.11125 | E001 | MEDIUM |
| RSK-064 | risk | 1509.04238, 2210.12654 | E001, E006 | MEDIUM |
| RSK-065 | risk | 1509.04238, 2104.08413 | E001 | MEDIUM |
| RSK-066 | risk | 1509.04238, 2104.05022 | E001 | MEDIUM |
| RSK-067 | risk | 1509.04238, 1603.07816 | E001 | MEDIUM |
| RSK-068 | risk | 1509.04238, 1708.02018 | E001 | MEDIUM |
| RSK-069 | risk | 1509.04238, 2109.07401 | E001 | MEDIUM |
| RSK-070 | risk | 1509.04238, 2603.24246 | E001 | MEDIUM |
| RSK-071 | risk | 1609.06265, 2111.08543 | E001 | MEDIUM |
| RSK-072 | risk | 1609.06265, 2510.03418 | E001, E006 | MEDIUM |
| RSK-073 | risk | 1503.00310, 1609.06265 | E001 | MEDIUM |
| RSK-074 | risk | 1409.6428, 1609.06265 | E001 | MEDIUM |
| RSK-075 | risk | 1609.06265, 1908.01843 | E001 | MEDIUM |
| RSK-076 | risk | 1609.06265, 2009.06401 | E001, E008 | MEDIUM |
| RSK-077 | risk | 1609.06265, 2407.17745 | E001 | MEDIUM |
| RSK-078 | risk | 1609.06265, 2208.11125 | E001 | MEDIUM |
| RSK-079 | risk | 1609.06265, 2210.12654 | E001, E006 | MEDIUM |
| RSK-080 | risk | 1609.06265, 2104.08413 | E001 | MEDIUM |
| RSK-081 | risk | 1609.06265, 2104.05022 | E001 | MEDIUM |
| RSK-082 | risk | 1603.07816, 1609.06265 | E001 | MEDIUM |
| RSK-083 | risk | 1609.06265, 1708.02018 | E001 | MEDIUM |
| RSK-084 | risk | 1609.06265, 2109.07401 | E001 | MEDIUM |
| RSK-085 | risk | 1609.06265, 2603.24246 | E001 | MEDIUM |
| RSK-086 | risk | 2111.08543, 2510.03418 | E001, E006 | MEDIUM |
| RSK-087 | risk | 1503.00310, 2111.08543 | E001 | MEDIUM |
| RSK-088 | risk | 1409.6428, 2111.08543 | E001 | MEDIUM |
| RSK-089 | risk | 1908.01843, 2111.08543 | E001 | MEDIUM |
| RSK-090 | risk | 2009.06401, 2111.08543 | E001, E008 | MEDIUM |
| RSK-091 | risk | 2111.08543, 2407.17745 | E001 | MEDIUM |
| RSK-092 | risk | 2111.08543, 2208.11125 | E001 | MEDIUM |
| RSK-093 | risk | 2111.08543, 2210.12654 | E001, E006 | MEDIUM |
| RSK-094 | risk | 2104.08413, 2111.08543 | E001 | MEDIUM |
| RSK-095 | risk | 2104.05022, 2111.08543 | E001 | MEDIUM |
| RSK-096 | risk | 1603.07816, 2111.08543 | E001 | MEDIUM |
| RSK-097 | risk | 1708.02018, 2111.08543 | E001 | MEDIUM |
| RSK-098 | risk | 2109.07401, 2111.08543 | E001 | MEDIUM |
| RSK-099 | risk | 2111.08543, 2603.24246 | E001 | MEDIUM |
| RSK-100 | risk | 1503.00310, 2510.03418 | E001, E006 | MEDIUM |
| RSK-101 | risk | 1409.6428, 2510.03418 | E001, E006 | MEDIUM |
| RSK-102 | risk | 1908.01843, 2510.03418 | E001, E006 | MEDIUM |
| RSK-103 | risk | 2009.06401, 2510.03418 | E006, E008 | MEDIUM |
| RSK-104 | risk | 2407.17745, 2510.03418 | E001, E006 | MEDIUM |
| RSK-105 | risk | 2208.11125, 2510.03418 | E001, E006 | MEDIUM |
| RSK-106 | risk | 2210.12654, 2510.03418 | E006 | MEDIUM |
| RSK-107 | risk | 2104.08413, 2510.03418 | E001, E006 | MEDIUM |
| RSK-108 | risk | 2104.05022, 2510.03418 | E001, E006 | MEDIUM |
| RSK-109 | risk | 1603.07816, 2510.03418 | E001, E006 | MEDIUM |
| RSK-110 | risk | 1708.02018, 2510.03418 | E001, E006 | MEDIUM |
| RSK-111 | risk | 2109.07401, 2510.03418 | E001, E006 | MEDIUM |
| RSK-112 | risk | 2510.03418, 2603.24246 | E001, E006 | MEDIUM |
| RSK-113 | risk | 1409.6428, 1503.00310 | E001 | MEDIUM |
| RSK-114 | risk | 1503.00310, 1908.01843 | E001 | MEDIUM |
| RSK-115 | risk | 1503.00310, 2009.06401 | E001, E008 | MEDIUM |
| RSK-116 | risk | 1503.00310, 2407.17745 | E001 | MEDIUM |
| RSK-117 | risk | 1503.00310, 2208.11125 | E001 | MEDIUM |
| RSK-118 | risk | 1503.00310, 2210.12654 | E001, E006 | MEDIUM |
| RSK-119 | risk | 1503.00310, 2104.08413 | E001 | MEDIUM |
| RSK-120 | risk | 1503.00310, 2104.05022 | E001 | MEDIUM |
| RSK-121 | risk | 1503.00310, 1603.07816 | E001 | MEDIUM |
| RSK-122 | risk | 1503.00310, 1708.02018 | E001 | MEDIUM |
| RSK-123 | risk | 1503.00310, 2109.07401 | E001 | MEDIUM |
| RSK-124 | risk | 1503.00310, 2603.24246 | E001 | MEDIUM |
| RSK-125 | risk | 1409.6428, 1908.01843 | E001 | MEDIUM |
| RSK-126 | risk | 1409.6428, 2009.06401 | E001, E008 | MEDIUM |
| RSK-127 | risk | 1409.6428, 2407.17745 | E001 | MEDIUM |
| RSK-128 | risk | 1409.6428, 2208.11125 | E001 | MEDIUM |
| RSK-129 | risk | 1409.6428, 2210.12654 | E001, E006 | MEDIUM |
| RSK-130 | risk | 1409.6428, 2104.08413 | E001 | MEDIUM |
| RSK-131 | risk | 1409.6428, 2104.05022 | E001 | MEDIUM |
| RSK-132 | risk | 1409.6428, 1603.07816 | E001 | MEDIUM |
| RSK-133 | risk | 1409.6428, 1708.02018 | E001 | MEDIUM |
| RSK-134 | risk | 1409.6428, 2109.07401 | E001 | MEDIUM |
| RSK-135 | risk | 1409.6428, 2603.24246 | E001 | MEDIUM |
| RSK-136 | risk | 1908.01843, 2009.06401 | E001, E008 | MEDIUM |
| RSK-137 | risk | 1908.01843, 2407.17745 | E001 | MEDIUM |
| RSK-138 | risk | 1908.01843, 2208.11125 | E001 | MEDIUM |
| RSK-139 | risk | 1908.01843, 2210.12654 | E001, E006 | MEDIUM |
| RSK-140 | risk | 1908.01843, 2104.08413 | E001 | MEDIUM |
| RSK-141 | risk | 1908.01843, 2104.05022 | E001 | MEDIUM |
| RSK-142 | risk | 1603.07816, 1908.01843 | E001 | MEDIUM |
| RSK-143 | risk | 1708.02018, 1908.01843 | E001 | MEDIUM |
| RSK-144 | risk | 1908.01843, 2109.07401 | E001 | MEDIUM |
| RSK-145 | risk | 1908.01843, 2603.24246 | E001 | MEDIUM |
| RSK-146 | risk | 2009.06401, 2407.17745 | E001, E008 | MEDIUM |
| RSK-147 | risk | 2009.06401, 2208.11125 | E001, E008 | MEDIUM |
| RSK-148 | risk | 2009.06401, 2210.12654 | E006, E008 | MEDIUM |
| RSK-149 | risk | 2009.06401, 2104.08413 | E001, E008 | MEDIUM |
| RSK-150 | risk | 2009.06401, 2104.05022 | E001, E008 | MEDIUM |
| RSK-151 | risk | 1603.07816, 2009.06401 | E001, E008 | MEDIUM |
| RSK-152 | risk | 1708.02018, 2009.06401 | E001, E008 | MEDIUM |
| RSK-153 | risk | 2009.06401, 2109.07401 | E001, E008 | MEDIUM |
| RSK-154 | risk | 2009.06401, 2603.24246 | E001, E008 | MEDIUM |
| RSK-155 | risk | 2208.11125, 2407.17745 | E001 | MEDIUM |
| RSK-156 | risk | 2210.12654, 2407.17745 | E001, E006 | MEDIUM |
| RSK-157 | risk | 2104.08413, 2407.17745 | E001 | MEDIUM |
| RSK-158 | risk | 2104.05022, 2407.17745 | E001 | MEDIUM |
| RSK-159 | risk | 1603.07816, 2407.17745 | E001 | MEDIUM |
| RSK-160 | risk | 1708.02018, 2407.17745 | E001 | MEDIUM |
| RSK-161 | risk | 2109.07401, 2407.17745 | E001 | MEDIUM |
| RSK-162 | risk | 2407.17745, 2603.24246 | E001 | MEDIUM |
| RSK-163 | risk | 2208.11125, 2210.12654 | E001, E006 | MEDIUM |
| RSK-164 | risk | 2104.08413, 2208.11125 | E001 | MEDIUM |
| RSK-165 | risk | 2104.05022, 2208.11125 | E001 | MEDIUM |
| RSK-166 | risk | 1603.07816, 2208.11125 | E001 | MEDIUM |
| RSK-167 | risk | 1708.02018, 2208.11125 | E001 | MEDIUM |
| RSK-168 | risk | 2109.07401, 2208.11125 | E001 | MEDIUM |
| RSK-169 | risk | 2208.11125, 2603.24246 | E001 | MEDIUM |
| RSK-170 | risk | 2104.08413, 2210.12654 | E001, E006 | MEDIUM |
| RSK-171 | risk | 2104.05022, 2210.12654 | E001, E006 | MEDIUM |
| RSK-172 | risk | 1603.07816, 2210.12654 | E001, E006 | MEDIUM |
| RSK-173 | risk | 1708.02018, 2210.12654 | E001, E006 | MEDIUM |
| RSK-174 | risk | 2109.07401, 2210.12654 | E001, E006 | MEDIUM |
| RSK-175 | risk | 2210.12654, 2603.24246 | E001, E006 | MEDIUM |
| RSK-176 | risk | 2104.05022, 2104.08413 | E001 | MEDIUM |
| RSK-177 | risk | 1603.07816, 2104.08413 | E001 | MEDIUM |
| RSK-178 | risk | 1708.02018, 2104.08413 | E001 | MEDIUM |
| RSK-179 | risk | 2104.08413, 2109.07401 | E001 | MEDIUM |
| RSK-180 | risk | 2104.08413, 2603.24246 | E001 | MEDIUM |
| RSK-181 | risk | 1603.07816, 2104.05022 | E001 | MEDIUM |
| RSK-182 | risk | 1708.02018, 2104.05022 | E001 | MEDIUM |
| RSK-183 | risk | 2104.05022, 2109.07401 | E001 | MEDIUM |
| RSK-184 | risk | 2104.05022, 2603.24246 | E001 | MEDIUM |
| RSK-185 | risk | 1603.07816, 1708.02018 | E001 | MEDIUM |
| RSK-186 | risk | 1603.07816, 2109.07401 | E001 | MEDIUM |
| RSK-187 | risk | 1603.07816, 2603.24246 | E001 | MEDIUM |
| RSK-188 | risk | 1708.02018, 2109.07401 | E001 | MEDIUM |
| RSK-189 | risk | 1708.02018, 2603.24246 | E001 | MEDIUM |
| RSK-190 | risk | 2109.07401, 2603.24246 | E001 | MEDIUM |
| CON-001 | contradiction | 1906.01753, 2106.01210 | E001, E003 | MEDIUM |
| CON-002 | contradiction | 1509.04238, 1906.01753 | E001 | MEDIUM |
| CON-003 | contradiction | 1609.06265, 1906.01753 | E001 | MEDIUM |
| CON-004 | contradiction | 1906.01753, 2111.08543 | E001 | MEDIUM |
| CON-005 | contradiction | 1906.01753, 2510.03418 | E001, E006 | MEDIUM |
| CON-006 | contradiction | 1503.00310, 1906.01753 | E001 | MEDIUM |
| CON-007 | contradiction | 1409.6428, 1906.01753 | E001 | MEDIUM |
| CON-008 | contradiction | 1906.01753, 1908.01843 | E001 | MEDIUM |
| CON-009 | contradiction | 1906.01753, 2009.06401 | E001, E008 | MEDIUM |
| CON-010 | contradiction | 1906.01753, 2407.17745 | E001 | MEDIUM |
| CON-011 | contradiction | 1906.01753, 2208.11125 | E001 | MEDIUM |
| CON-012 | contradiction | 1906.01753, 2210.12654 | E001, E006 | MEDIUM |
| CON-013 | contradiction | 1906.01753, 2104.08413 | E001 | MEDIUM |
| CON-014 | contradiction | 1906.01753, 2104.05022 | E001 | MEDIUM |
| CON-015 | contradiction | 1603.07816, 1906.01753 | E001 | MEDIUM |
| CON-016 | contradiction | 1708.02018, 1906.01753 | E001 | MEDIUM |
| CON-017 | contradiction | 1906.01753, 2109.07401 | E001 | MEDIUM |
| CON-018 | contradiction | 1906.01753, 2603.24246 | E001 | MEDIUM |
| CON-019 | contradiction | 1509.04238, 2106.01210 | E001, E003 | MEDIUM |
| CON-020 | contradiction | 1609.06265, 2106.01210 | E001, E003 | MEDIUM |
| CON-021 | contradiction | 2106.01210, 2111.08543 | E001, E003 | MEDIUM |
| CON-022 | contradiction | 2106.01210, 2510.03418 | E003, E006 | MEDIUM |
| CON-023 | contradiction | 1503.00310, 2106.01210 | E001, E003 | MEDIUM |
| CON-024 | contradiction | 1409.6428, 2106.01210 | E001, E003 | MEDIUM |
| CON-025 | contradiction | 1908.01843, 2106.01210 | E001, E003 | MEDIUM |
| CON-026 | contradiction | 2009.06401, 2106.01210 | E003, E008 | MEDIUM |
| CON-027 | contradiction | 2106.01210, 2407.17745 | E001, E003 | MEDIUM |
| CON-028 | contradiction | 2106.01210, 2208.11125 | E001, E003 | MEDIUM |
| CON-029 | contradiction | 2106.01210, 2210.12654 | E003, E006 | MEDIUM |
| CON-030 | contradiction | 2104.08413, 2106.01210 | E001, E003 | MEDIUM |
| CON-031 | contradiction | 2104.05022, 2106.01210 | E001, E003 | MEDIUM |
| CON-032 | contradiction | 1603.07816, 2106.01210 | E001, E003 | MEDIUM |
| CON-033 | contradiction | 1708.02018, 2106.01210 | E001, E003 | MEDIUM |
| CON-034 | contradiction | 2106.01210, 2109.07401 | E001, E003 | MEDIUM |
| CON-035 | contradiction | 2106.01210, 2603.24246 | E001, E003 | MEDIUM |
| CON-036 | contradiction | 1509.04238, 1609.06265 | E001 | MEDIUM |
| CON-037 | contradiction | 1509.04238, 2111.08543 | E001 | MEDIUM |
| CON-038 | contradiction | 1509.04238, 2510.03418 | E001, E006 | MEDIUM |
| CON-039 | contradiction | 1503.00310, 1509.04238 | E001 | MEDIUM |
| CON-040 | contradiction | 1409.6428, 1509.04238 | E001 | MEDIUM |
| CON-041 | contradiction | 1509.04238, 1908.01843 | E001 | MEDIUM |
| CON-042 | contradiction | 1509.04238, 2009.06401 | E001, E008 | MEDIUM |
| CON-043 | contradiction | 1509.04238, 2407.17745 | E001 | MEDIUM |
| CON-044 | contradiction | 1509.04238, 2208.11125 | E001 | MEDIUM |
| CON-045 | contradiction | 1509.04238, 2210.12654 | E001, E006 | MEDIUM |
| CON-046 | contradiction | 1509.04238, 2104.08413 | E001 | MEDIUM |
| CON-047 | contradiction | 1509.04238, 2104.05022 | E001 | MEDIUM |
| CON-048 | contradiction | 1509.04238, 1603.07816 | E001 | MEDIUM |
| CON-049 | contradiction | 1509.04238, 1708.02018 | E001 | MEDIUM |
| CON-050 | contradiction | 1509.04238, 2109.07401 | E001 | MEDIUM |
| CON-051 | contradiction | 1509.04238, 2603.24246 | E001 | MEDIUM |
| CON-052 | contradiction | 1609.06265, 2111.08543 | E001 | MEDIUM |
| CON-053 | contradiction | 1609.06265, 2510.03418 | E001, E006 | MEDIUM |
| CON-054 | contradiction | 1503.00310, 1609.06265 | E001 | MEDIUM |
| CON-055 | contradiction | 1409.6428, 1609.06265 | E001 | MEDIUM |
| CON-056 | contradiction | 1609.06265, 1908.01843 | E001 | MEDIUM |
| CON-057 | contradiction | 1609.06265, 2009.06401 | E001, E008 | MEDIUM |
| CON-058 | contradiction | 1609.06265, 2407.17745 | E001 | MEDIUM |
| CON-059 | contradiction | 1609.06265, 2208.11125 | E001 | MEDIUM |
| CON-060 | contradiction | 1609.06265, 2210.12654 | E001, E006 | MEDIUM |
| CON-061 | contradiction | 1609.06265, 2104.08413 | E001 | MEDIUM |
| CON-062 | contradiction | 1609.06265, 2104.05022 | E001 | MEDIUM |
| CON-063 | contradiction | 1603.07816, 1609.06265 | E001 | MEDIUM |
| CON-064 | contradiction | 1609.06265, 1708.02018 | E001 | MEDIUM |
| CON-065 | contradiction | 1609.06265, 2109.07401 | E001 | MEDIUM |
| CON-066 | contradiction | 1609.06265, 2603.24246 | E001 | MEDIUM |
| CON-067 | contradiction | 2111.08543, 2510.03418 | E001, E006 | MEDIUM |
| CON-068 | contradiction | 1503.00310, 2111.08543 | E001 | MEDIUM |
| CON-069 | contradiction | 1409.6428, 2111.08543 | E001 | MEDIUM |
| CON-070 | contradiction | 1908.01843, 2111.08543 | E001 | MEDIUM |
| CON-071 | contradiction | 2009.06401, 2111.08543 | E001, E008 | MEDIUM |
| CON-072 | contradiction | 2111.08543, 2407.17745 | E001 | MEDIUM |
| CON-073 | contradiction | 2111.08543, 2208.11125 | E001 | MEDIUM |
| CON-074 | contradiction | 2111.08543, 2210.12654 | E001, E006 | MEDIUM |
| CON-075 | contradiction | 2104.08413, 2111.08543 | E001 | MEDIUM |
| CON-076 | contradiction | 2104.05022, 2111.08543 | E001 | MEDIUM |
| CON-077 | contradiction | 1603.07816, 2111.08543 | E001 | MEDIUM |
| CON-078 | contradiction | 1708.02018, 2111.08543 | E001 | MEDIUM |
| CON-079 | contradiction | 2109.07401, 2111.08543 | E001 | MEDIUM |
| CON-080 | contradiction | 2111.08543, 2603.24246 | E001 | MEDIUM |
| CON-081 | contradiction | 1503.00310, 2510.03418 | E001, E006 | MEDIUM |
| CON-082 | contradiction | 1409.6428, 2510.03418 | E001, E006 | MEDIUM |
| CON-083 | contradiction | 1908.01843, 2510.03418 | E001, E006 | MEDIUM |
| CON-084 | contradiction | 2009.06401, 2510.03418 | E006, E008 | MEDIUM |
| CON-085 | contradiction | 2407.17745, 2510.03418 | E001, E006 | MEDIUM |
| CON-086 | contradiction | 2208.11125, 2510.03418 | E001, E006 | MEDIUM |
| CON-087 | contradiction | 2210.12654, 2510.03418 | E006 | MEDIUM |
| CON-088 | contradiction | 2104.08413, 2510.03418 | E001, E006 | MEDIUM |
| CON-089 | contradiction | 2104.05022, 2510.03418 | E001, E006 | MEDIUM |
| CON-090 | contradiction | 1603.07816, 2510.03418 | E001, E006 | MEDIUM |
| CON-091 | contradiction | 1708.02018, 2510.03418 | E001, E006 | MEDIUM |
| CON-092 | contradiction | 2109.07401, 2510.03418 | E001, E006 | MEDIUM |
| CON-093 | contradiction | 2510.03418, 2603.24246 | E001, E006 | MEDIUM |
| CON-094 | contradiction | 1409.6428, 1503.00310 | E001 | MEDIUM |
| CON-095 | contradiction | 1503.00310, 1908.01843 | E001 | MEDIUM |
| CON-096 | contradiction | 1503.00310, 2009.06401 | E001, E008 | MEDIUM |
| CON-097 | contradiction | 1503.00310, 2407.17745 | E001 | MEDIUM |
| CON-098 | contradiction | 1503.00310, 2208.11125 | E001 | MEDIUM |
| CON-099 | contradiction | 1503.00310, 2210.12654 | E001, E006 | MEDIUM |
| CON-100 | contradiction | 1503.00310, 2104.08413 | E001 | MEDIUM |
| CON-101 | contradiction | 1503.00310, 2104.05022 | E001 | MEDIUM |
| CON-102 | contradiction | 1503.00310, 1603.07816 | E001 | MEDIUM |
| CON-103 | contradiction | 1503.00310, 1708.02018 | E001 | MEDIUM |
| CON-104 | contradiction | 1503.00310, 2109.07401 | E001 | MEDIUM |
| CON-105 | contradiction | 1503.00310, 2603.24246 | E001 | MEDIUM |
| CON-106 | contradiction | 1409.6428, 1908.01843 | E001 | MEDIUM |
| CON-107 | contradiction | 1409.6428, 2009.06401 | E001, E008 | MEDIUM |
| CON-108 | contradiction | 1409.6428, 2407.17745 | E001 | MEDIUM |
| CON-109 | contradiction | 1409.6428, 2208.11125 | E001 | MEDIUM |
| CON-110 | contradiction | 1409.6428, 2210.12654 | E001, E006 | MEDIUM |
| CON-111 | contradiction | 1409.6428, 2104.08413 | E001 | MEDIUM |
| CON-112 | contradiction | 1409.6428, 2104.05022 | E001 | MEDIUM |
| CON-113 | contradiction | 1409.6428, 1603.07816 | E001 | MEDIUM |
| CON-114 | contradiction | 1409.6428, 1708.02018 | E001 | MEDIUM |
| CON-115 | contradiction | 1409.6428, 2109.07401 | E001 | MEDIUM |
| CON-116 | contradiction | 1409.6428, 2603.24246 | E001 | MEDIUM |
| CON-117 | contradiction | 1908.01843, 2009.06401 | E001, E008 | MEDIUM |
| CON-118 | contradiction | 1908.01843, 2407.17745 | E001 | MEDIUM |
| CON-119 | contradiction | 1908.01843, 2208.11125 | E001 | MEDIUM |
| CON-120 | contradiction | 1908.01843, 2210.12654 | E001, E006 | MEDIUM |
| CON-121 | contradiction | 1908.01843, 2104.08413 | E001 | MEDIUM |
| CON-122 | contradiction | 1908.01843, 2104.05022 | E001 | MEDIUM |
| CON-123 | contradiction | 1603.07816, 1908.01843 | E001 | MEDIUM |
| CON-124 | contradiction | 1708.02018, 1908.01843 | E001 | MEDIUM |
| CON-125 | contradiction | 1908.01843, 2109.07401 | E001 | MEDIUM |
| CON-126 | contradiction | 1908.01843, 2603.24246 | E001 | MEDIUM |
| CON-127 | contradiction | 2009.06401, 2407.17745 | E001, E008 | MEDIUM |
| CON-128 | contradiction | 2009.06401, 2208.11125 | E001, E008 | MEDIUM |
| CON-129 | contradiction | 2009.06401, 2210.12654 | E006, E008 | MEDIUM |
| CON-130 | contradiction | 2009.06401, 2104.08413 | E001, E008 | MEDIUM |
| CON-131 | contradiction | 2009.06401, 2104.05022 | E001, E008 | MEDIUM |
| CON-132 | contradiction | 1603.07816, 2009.06401 | E001, E008 | MEDIUM |
| CON-133 | contradiction | 1708.02018, 2009.06401 | E001, E008 | MEDIUM |
| CON-134 | contradiction | 2009.06401, 2109.07401 | E001, E008 | MEDIUM |
| CON-135 | contradiction | 2009.06401, 2603.24246 | E001, E008 | MEDIUM |
| CON-136 | contradiction | 2208.11125, 2407.17745 | E001 | MEDIUM |
| CON-137 | contradiction | 2210.12654, 2407.17745 | E001, E006 | MEDIUM |
| CON-138 | contradiction | 2104.08413, 2407.17745 | E001 | MEDIUM |
| CON-139 | contradiction | 2104.05022, 2407.17745 | E001 | MEDIUM |
| CON-140 | contradiction | 1603.07816, 2407.17745 | E001 | MEDIUM |
| CON-141 | contradiction | 1708.02018, 2407.17745 | E001 | MEDIUM |
| CON-142 | contradiction | 2109.07401, 2407.17745 | E001 | MEDIUM |
| CON-143 | contradiction | 2407.17745, 2603.24246 | E001 | MEDIUM |
| CON-144 | contradiction | 2208.11125, 2210.12654 | E001, E006 | MEDIUM |
| CON-145 | contradiction | 2104.08413, 2208.11125 | E001 | MEDIUM |
| CON-146 | contradiction | 2104.05022, 2208.11125 | E001 | MEDIUM |
| CON-147 | contradiction | 1603.07816, 2208.11125 | E001 | MEDIUM |
| CON-148 | contradiction | 1708.02018, 2208.11125 | E001 | MEDIUM |
| CON-149 | contradiction | 2109.07401, 2208.11125 | E001 | MEDIUM |
| CON-150 | contradiction | 2208.11125, 2603.24246 | E001 | MEDIUM |
| CON-151 | contradiction | 2104.08413, 2210.12654 | E001, E006 | MEDIUM |
| CON-152 | contradiction | 2104.05022, 2210.12654 | E001, E006 | MEDIUM |
| CON-153 | contradiction | 1603.07816, 2210.12654 | E001, E006 | MEDIUM |
| CON-154 | contradiction | 1708.02018, 2210.12654 | E001, E006 | MEDIUM |
| CON-155 | contradiction | 2109.07401, 2210.12654 | E001, E006 | MEDIUM |
| CON-156 | contradiction | 2210.12654, 2603.24246 | E001, E006 | MEDIUM |
| CON-157 | contradiction | 2104.05022, 2104.08413 | E001 | MEDIUM |
| CON-158 | contradiction | 1603.07816, 2104.08413 | E001 | MEDIUM |
| CON-159 | contradiction | 1708.02018, 2104.08413 | E001 | MEDIUM |
| CON-160 | contradiction | 2104.08413, 2109.07401 | E001 | MEDIUM |
| CON-161 | contradiction | 2104.08413, 2603.24246 | E001 | MEDIUM |
| CON-162 | contradiction | 1603.07816, 2104.05022 | E001 | MEDIUM |
| CON-163 | contradiction | 1708.02018, 2104.05022 | E001 | MEDIUM |
| CON-164 | contradiction | 2104.05022, 2109.07401 | E001 | MEDIUM |
| CON-165 | contradiction | 2104.05022, 2603.24246 | E001 | MEDIUM |
| CON-166 | contradiction | 1603.07816, 1708.02018 | E001 | MEDIUM |
| CON-167 | contradiction | 1603.07816, 2109.07401 | E001 | MEDIUM |
| CON-168 | contradiction | 1603.07816, 2603.24246 | E001 | MEDIUM |
| CON-169 | contradiction | 1708.02018, 2109.07401 | E001 | MEDIUM |
| CON-170 | contradiction | 1708.02018, 2603.24246 | E001 | MEDIUM |
| CON-171 | contradiction | 2109.07401, 2603.24246 | E001 | MEDIUM |
| MECH-001 | reusable_mechanism | 1906.01753 | E001 | MEDIUM |
| MECH-002 | reusable_mechanism | 2106.01210 | E001 | MEDIUM |
| MECH-003 | reusable_mechanism | 1509.04238 | E001 | MEDIUM |
| MECH-004 | reusable_mechanism | 1609.06265 | E009 | MEDIUM |
| MECH-005 | reusable_mechanism | 2111.08543 | E001 | MEDIUM |
| MECH-006 | reusable_mechanism | 2510.03418 | E007 | MEDIUM |
| MECH-007 | reusable_mechanism | 1503.00310 | E001 | MEDIUM |
| MECH-008 | reusable_mechanism | 1409.6428 | E001 | MEDIUM |
| MECH-009 | reusable_mechanism | 1908.01843 | E001 | MEDIUM |
| MECH-010 | reusable_mechanism | 2009.06401 | E001 | MEDIUM |
| MECH-011 | reusable_mechanism | 2407.17745 | E001 | MEDIUM |
| MECH-012 | reusable_mechanism | 2208.11125 | E010 | MEDIUM |
| MECH-013 | reusable_mechanism | 2210.12654 | E001 | MEDIUM |
| MECH-014 | reusable_mechanism | 2104.08413 | E004 | MEDIUM |
| MECH-015 | reusable_mechanism | 2104.05022 | E001 | MEDIUM |
| MECH-016 | reusable_mechanism | 1603.07816 | E001 | MEDIUM |
| MECH-017 | reusable_mechanism | 1708.02018 | E001 | MEDIUM |
| MECH-018 | reusable_mechanism | 2109.07401 | E001 | MEDIUM |
| MECH-019 | reusable_mechanism | 2603.24246 | E001 | MEDIUM |
