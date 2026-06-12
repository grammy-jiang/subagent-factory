# Research Report: Hierarchical Reading of Long Technical & Scientific Documents for Distillation

*Long-document & hierarchical summarisation · topic & discourse segmentation · document-structure extraction · candidate knowledge-unit identification over 200+ page books.*

## Contents

- [Round History](#round-history)
- [Executive Summary](#executive-summary)
- [Research Question](#research-question)
- [Methodology](#methodology)
- [Papers Reviewed](#papers-reviewed)
- [Research Landscape](#research-landscape)
- [Methodology Comparison](#methodology-comparison)
- [Confidence-Graded Findings](#confidence-graded-findings)
- [Trade-Off Analysis](#trade-off-analysis)
- [Points of Agreement](#points-of-agreement)
- [Points of Contradiction](#points-of-contradiction)
- [Research Gaps](#research-gaps)
- [Reproducibility Notes](#reproducibility-notes)
- [Practical Recommendations](#practical-recommendations)
- [Readiness Assessment](#readiness-assessment-system-building-mode)
- [Evidence Map](#evidence-map)
- [References](#references)
- [Appendix: Run Metadata](#appendix-run-metadata)

## Round History

Iterative gap-closure loop (hard cap: 4 rounds). See `references/iterative-synthesis.md`.

| Round | Run ID | Topic / Gap Focus | New Papers | Gaps Addressed | Remaining Gaps |
|-------|--------|-------------------|------------|----------------|----------------|
| 1 | longdoc-r1-20260611 | Original topic (full facet sweep) | 18 deep / 50 screened | Initial shortlist; structure-extraction, candidate-unit ID, evaluation | **2 academic HIGH** (G1 topic-segmentation, G3 claim-recall eval), 3 academic MED/LOW, 3 engineering |
| 2 | longdoc-r2-20260612 | G1 — standalone topic / linear text segmentation (TextTiling→C99→neural→long-doc coherence) | 9 curated | **G1 CLOSED** | G3 academic HIGH; 3 academic MED/LOW; 3 engineering |
| 3 | longdoc-r3-20260612 | G3 — claim / principle-level recall & coverage evaluation | 10 curated | **G3 CLOSED** | 3 academic MED/LOW (G2,G4,G5); 3 engineering (G6,G7,G8) |

**Stop reason**: *Converged on HIGH gaps in 3 rounds (cap 4).* Both HIGH-severity academic gaps are now closed with dedicated literature: G1 by a standalone-segmentation corpus (round 2) and G3 by a claim/coverage-evaluation corpus (round 3). Remaining gaps are MEDIUM/LOW academic (G2, G4, G5) and ENGINEERING (G6, G7, G8), none HIGH; per protocol iteration stops. Rounds 2–3 ran the standard pipeline with an agent-curated shortlist seeded by canonical arXiv IDs (the default arXiv backend returned only single-day recency-biased candidates, so seminal pre-2024 segmentation/claim papers were injected by ID — see Appendix).

## Executive Summary

This review asks **how to read a 200+ page technical/scientific book *structure-first*** — building a `part → chapter → section → passage` map and segmenting it into **candidate knowledge units** — so that downstream claim/principle extraction operates on structured units instead of flat-reading the whole text. Across **18 deeply analyzed papers** (from 50 screened, drawn from arXiv, Semantic Scholar, OpenAlex, DBLP and citation expansion, 2018–2026) the literature converges on a clear, buildable **7-stage reference pipeline**: parse → build hierarchy tree → segment topically → enumerate provenance-anchored candidate units → rank salience with *global* context → read nodes long-context → validate precision *and* recall. The strongest, most consistent finding is that **flat fixed-window chunking is the wrong baseline**: explicit hierarchy plus content-based (not positional) selection improves quality and, in one case, halves compute. The most consequential gap is that **standalone topic-segmentation methods (TextTiling/C99/BayesSeg/neural text segmentation) are absent from the retrieved corpus**, yet segment boundaries directly gate candidate-unit recall.

**Scope**: 18 papers deeply analyzed (50 screened) from arXiv, Semantic Scholar, OpenAlex, DBLP, HuggingFace; 2018–2026.
**Overall Confidence**: Medium-High (architecture and evaluation well-supported; segmentation + claim-level recall under-covered).
**Verdict**: **HAS_GAPS** — sufficient to design the Phase-2A/2B preprocessor; two HIGH academic gaps remain for follow-up rounds.

## Research Question

**Primary**: What methods exist to (2A) recover a hierarchical structure map of a long (200+ page) technical/scientific document from raw converted text, and (2B) segment that document into *candidate knowledge units*, such that claim/principle/skill extraction can read structure-aware and achieve higher recall **and** precision than flat reading?

**In scope**: long-document & hierarchical summarisation (as a source of structure/selection techniques); topic & discourse/linear segmentation; document-structure/layout extraction (PDF/text → tree); candidate-unit / key-point / salient-passage identification; long-context reading & semantic chunking; evaluation of the above.

**Out of scope**: general-purpose summarization quality for its own sake; model pre-training; non-document NLP; product/implementation build (this is a methods review). The downstream consumer (claim extraction, principle promotion) is treated as a fixed requirement, not redesigned here.

## Methodology

### Search Strategy

- **Sources**: arXiv, Semantic Scholar, OpenAlex, DBLP, HuggingFace (+ Semantic Scholar citation-graph expansion, BFS depth-2).
- **Query variants** (14 total): long-document/hierarchical summarization; topic/text segmentation & TextTiling; document structure & section/chapter segmentation; semantic chunking & long-context reading; key-point/candidate-unit & salient-content selection; RST/discourse parsing; document layout analysis; hierarchical attention.
- **Time window**: primary 36 months, fallback 84 months; **foundational older work admitted via citation expansion** (e.g. Longformer 2020, Discourse-Aware Attention 2018, Hierarchical Transformers 2019).
- **Screening**: heuristic BM25 (527→580 candidates) + LLM relevance sub-agent → 50 accepted across 8 facets; 24 downloadable (arXiv) curated for depth; **18 successfully converted and deeply analyzed**.

### Pipeline Summary

```mermaid
flowchart TD
    A["Searched<br/>580 candidates<br/>(6 sources + citations)"] --> B["Screened<br/>50 accepted / 8 facets"]
    B --> C["Curated + Downloaded<br/>24 arXiv PDFs"]
    C --> D["Converted (docling)<br/>18 Markdown"]
    D --> E["Deep-analyzed<br/>18 papers (4 facet batches)"]
    E --> F["Synthesized<br/>7-stage reference pipeline + gaps"]
```

| Metric | Count |
|--------|-------|
| Total candidates (after dedup) | 580 |
| After LLM screening (accepted) | 50 |
| Curated for download | 24 |
| Successfully converted | 18 |
| Deeply analyzed | 18 |
| Gap-closure rounds (planned) | ≥2 (G1, G3) |

> **Conversion note**: PDF→Markdown used the local `docling` backend (the fast `pymupdf4llm` backend was unavailable). 18 of 24 PDFs converted; 6 canonical papers (incl. the long-doc-summarization survey 2207.00939, HIBRIDS 2203.10741, efficient-attentions 2104.02112) timed out under OCR-heavy layout analysis and are cited at abstract level only — a deep-analysis gap noted in [Reproducibility Notes](#reproducibility-notes).

## Papers Reviewed

Round 1: 18 deeply analyzed. Rounds 2–3 added **19 curated gap-closure papers** (9 segmentation + 10 claim-recall), summarized below the round-1 table. Relevance = LLM screen score; Rating = analyst 1–5.

| # | Title [arxiv_id] | First Author | Year | Venue | Rating | Facet |
|---|------------------|--------------|------|-------|--------|-------|
| 1 | Trace Only What You Need: Structure-Aware On-Demand Hypergraph Memory (DocTrace) [2606.10921] | Zai et al. | 2026 | preprint | 5/5 | structure / long-context |
| 2 | Toward Unifying Text Segmentation and Long Document Summarization (Lodoss) [2210.16422] | Cho et al. | 2022 | EMNLP | 5/5 | segmentation + summ |
| 3 | HiStruct+: Extractive Summarization with Hierarchical Structure [2203.09629] | Ruan et al. | 2022 | ACL Findings | 5/5 | document structure |
| 4 | Hierarchical Transformers for Multi-Document Summarization [1905.13164] | Liu & Lapata | 2019 | ACL | 5/5 | hierarchical summ |
| 5 | BooookScore: Book-length Summarization in the Era of LLMs [2310.00785] | Chang et al. | 2023 | ICLR | 5/5 | evaluation |
| 6 | LongSumEval: QA-Based Evaluation & Feedback Refinement [2604.25130] | Nguyen et al. | 2026 | preprint | 5/5 | evaluation |
| 7 | BookSum: Datasets for Long-form Narrative Summarization [2105.08209] | Kryściński et al. | 2021 | EMNLP Findings | 4/5 | dataset / structure |
| 8 | Papers-to-Posts: Detailed Long-Document Summarization [2406.10370] | Radensky et al. | 2024 | preprint/HCI | 4/5 | candidate-unit |
| 9 | HERA: Long Document Summarization with LLMs [2502.00448] | Li et al. | 2025 | preprint | 4/5 | long-doc summ |
| 10 | Longformer: The Long-Document Transformer [2004.05150] | Beltagy et al. | 2020 | arXiv | 4/5 | long-context |
| 11 | AWESOME: Memory-constrained Long Document Summarization [2305.14806] | Cao & Wang | 2023 | NAACL | 4/5 | segmentation + salience |
| 12 | ParseFixer: Agentic Document Parsing [2606.11977] | Yu et al. | 2026 | preprint | 4/5 | layout / parsing |
| 13 | A Discourse-Aware Attention Model for Abstractive Summarization of Long Documents [1804.05685] | Cohan et al. | 2018 | NAACL | 3/5 | discourse / hierarchy |
| 14 | Incorporating Distributions of Discourse Structure (RSTformer) [2305.16784] | Liu et al. | 2023 | ACL | 3/5 | discourse (RST) |
| 15 | RST-LoRA: Discourse-Aware Low-Rank Adaptation [2405.00657] | Liu & Lapata | 2024 | NAACL | 3/5 | discourse (RST) |
| 16 | Hybrid Long Document Summarization (C2F-FAR + ChatGPT) [2306.01169] | Lu et al. | 2023 | arXiv | 3/5 | unsupervised segmentation |
| 17 | Attention Expansion: Keyphrase Extraction from Long Documents [2606.10716] | Martínez-Cruz et al. | 2026 | preprint | 3/5 | candidate-unit (KPE) |
| 18 | A Split-then-Join Approach for Very Long Documents (SPIN) [2505.06862] | Fazry et al. | 2025 | preprint | 2/5 | chunking (neg. exemplar) |

**Round 2 — standalone topic / linear text segmentation (G1):**

| # | Title [arxiv_id] | Year | Role for Stage 2 |
|---|------------------|------|------------------|
| 19 | Recent Trends in Linear Text Segmentation: a Survey [2411.16613] | 2024 | Taxonomy + "supervised+transformer is the framework of choice"; Pk/WindowDiff |
| 20 | Text Segmentation as a Supervised Learning Task (WIKI-727K) [1803.09337] | 2018 | Supervised framing + the standard benchmark dataset |
| 21 | Text Segmentation by Cross Segment Attention [2004.14535] | 2020 | **v1 default** — cheap local-context boundary classifier; new SOTA |
| 22 | Two-Level Transformer + Auxiliary Coherence Modeling [2001.00891] | 2020 | Coherence objective on sentence encoder |
| 23 | Transformer-over-Transformer (Topseg) [2110.07160] | 2021 | Enhanced topic coherence |
| 24 | Long Document Topic Segmentation w/ Enhanced Coherence [2310.11772] | 2023 | **Recommended target** — Longformer+coherence; SOTA, domain-shift-robust |
| 25 | Unsupervised Topic Segmentation of Meetings w/ BERT [2106.12978] | 2021 | Zero-training embedding-adjacency fallback |
| 26 | Unsupervised Dialogue Topic Segmentation (utterance-pair coherence) [2106.06719] | 2021 | Unsupervised coherence-scoring variant |
| 27 | Domain Knowledge for Topic Segmentation of Long MOOC Lectures [2012.07589] | 2020 | Long-form domain-adaptation evidence |

**Round 3 — claim / principle-level recall & coverage evaluation (G3):**

| # | Title [arxiv_id] | Year | Role for Step-10 gate |
|---|------------------|------|----------------------|
| 28 | FActScore: Atomic Evaluation of Factual Precision [2305.14251] | 2023 | Atomic-claim decomposition primitive |
| 29 | Towards Effective Extraction & Evaluation of Factual Claims (Claimify) [2502.10855] | 2025 | High-precision extractor + coverage/decontextualization eval framework |
| 30 | Beyond Factual Accuracy: Coverage of Diverse Factual Info in Long-form [2501.03545] | 2025 | **Long-form coverage metric** (atomic claims + aspects) |
| 31 | Exhaustiveness in Key Point Generation + Auto Coverage Metric [2404.11793] | 2024 | **Exhaustiveness/recall coverage metric** for key points |
| 32 | From Arguments to Key Points (ArgKP) [2005.01619] | 2020 | Key-point = high-level claim; **match-based coverage** primitive |
| 33 | Overview of 2021 Key Point Analysis Shared Task [2110.10577] | 2021 | Operationalized coverage track (match-counting) |
| 34 | From Key Points to Key Point Hierarchy [2306.03853] | 2023 | Hierarchical (per-section) coverage aggregation |
| 35 | Core: Robust Factual Precision w/ Sub-Claim Identification [2407.03572] | 2024 | Informative sub-claim selection |
| 36 | Check-worthy Claim Detection across Topics [2212.08514] | 2022 | Filter for which source claims are worth enumerating |
| 37 | A Benchmark Dataset of Check-worthy Factual Claims [2004.14425] | 2020 | Check-worthiness reference data |

Additionally, **32 papers were screened-accepted but not deep-analyzed** (mostly DBLP records without open PDFs, plus 6 OCR-timeout papers); the most relevant are cited at abstract level: the *Empirical Survey on Long Document Summarization* [2207.00939], *HIBRIDS* structure-aware biases [2203.10741], *Top-down/Bottom-up* inference [2203.07586], *Discourse-Aware Neural Extractive* [1910.14142], and recent DBLP methods (Context-Aware Hierarchical Merging, CoTHSSum, GraphLSS, StrucSum).

## Research Landscape

### Theme 1 — Document-structure extraction: raw text → hierarchy tree

**Coverage**: 5 papers | **Confidence**: Medium-High
**Supporting**: [2606.10921], [2105.08209], [2203.09629], [2606.11977], [1804.05685]

The core Phase-2A capability — recover a `part→chapter→section→passage` tree from raw bytes — is **demonstrably buildable but rests on one strong recent recipe**. DocTrace's `BuildDocTree` [2606.10921] is the most directly applicable: a **two-tier parser** (LLM heading-pattern recognition, with an LLM-generated parsing-function fallback guarded by validation, then per-node NER) yields a 4-level `document/chapter/section/paragraph` tree, indexed in vector + BM25, **robust to ≥250k-token documents** — the only retrieved method shown at true book scale. BookSum [2105.08209] supplies the complementary **re-anchoring** mechanism when only flat text is available: phased **coarse-to-fine alignment** (full-text → chapter-by-metadata → paragraph-by-embedding) closed with **stable matching** to tie passages to structure. HiStruct+ [2203.09629] then **stamps each unit with a structural address** — a Sentence Structure Vector $(\text{section\_index}, \text{position\_in\_section})$ plus a normalized section-title class — turning a bare tree into a salience-aware one. ParseFixer [2606.11977] is the economical ingestion front-end (backbone parser + *selective* agentic correction only on rule-flagged bad pages → clean Markdown + reading order). The 2018 Discourse-Aware Attention model [1804.05685] is the conceptual ancestor (token→section→document hierarchical encoding) but hard-capped at ~2000 tokens / 4 sections.

Key findings:
1. A raw book can be parsed to a usable TOC tree at 250k+ tokens with a two-tier parser + validation fallback [2606.10921].
2. When structure metadata is partial, **coarse-to-fine + stable matching** re-anchors flat text onto the hierarchy [2105.08209].
3. Every unit should carry a **structural address + role class**; this single feature drove SOTA extractive ROUGE in [2203.09629].

### Theme 2 — Topic & discourse segmentation

**Coverage**: 15 papers (9 standalone, added round 2) | **Confidence**: High (G1 closed)
**Supporting**: [2210.16422], [2306.01169], [2305.14806], [2305.16784], [2405.00657], [1804.05685]
**Round-2 standalone segmentation corpus**: [2411.16613] (survey), [1803.09337], [2004.14535], [2001.00891], [2110.07160], [2310.11772], [2106.12978], [2106.06719], [2012.07589]

Segmentation appears **only as a sub-component of summarization pipelines**, never as a dedicated method in the retrieved corpus (see [G1](#research-gaps)). Lodoss [2210.16422] learns segmentation *jointly* with extractive summarization via two heads on a shared Longformer encoder — the cleanest "segment + select in one pass" design, but trained on **gold author section boundaries** at article scale. The unsupervised primitives are the most transferable to raw books: C2F-FAR [2306.01169] starts a new semantic block on **adjacent-sentence embedding dissimilarity** (coarse) then filters sentences against a block centroid (fine); AWESOME [2305.14806] uses a comparable training-free **semantic-similarity** rule. Discourse (RST) structure is represented by RSTformer [2305.16784] (an **uncertainty-aware n-best distribution** over labeled relations, with graceful fallback when the parser fails) and RST-LoRA [2405.00657] (collapses the RST matrix into a **per-EDU importance scalar**) — but both are parser-fragile and demonstrated only at chapter scale.

Key findings:
1. Joint segmentation+selection works but assumes gold boundaries [2210.16422]; raw books need the unsupervised adjacency/centroid primitives [2306.01169], [2305.14806].
2. Treat structure as a **soft, uncertainty-aware signal** with graceful degradation, not a single hard parse [2305.16784].
3. Any structural matrix can be reduced to a **per-unit importance scalar** for ranking [2405.00657].

#### G1 closure — standalone topic / linear text segmentation (round 2)

The dedicated segmentation literature fills the hole round 1 flagged. The field's arc, from the round-2 survey [2411.16613], is: early **unsupervised count-based** methods (TextTiling — two adjacent sliding windows compared by lexical cohesion; C99; BayesSeg) → **supervised neural** framing → **transformer + coherence modeling**, which the survey names as the current "framework of choice," with LLMs only beginning to gain traction and **evaluation/resources as the central open problem**.

- **Supervised framing + the standard benchmark**: Koshorek et al. [1803.09337] recast segmentation as supervised sequence labeling over sentences and released **WIKI-727K** (Wikipedia auto-labeled at section boundaries) — now the field's default train/test set, and shown to generalize to unseen natural text.
- **Practical strong baseline**: Cross-segment BERT [2004.14535] classifies each candidate break from only its **local left/right token context** — a simple, cheap binary boundary classifier that nonetheless set a new SOTA; the easiest stage-2 default to implement.
- **Coherence-aware transformers**: Two-Level Transformer + Auxiliary Coherence Modeling [2001.00891] and Transformer-over-pretrained-Transformer (Topseg) [2110.07160] add an explicit coherence objective on top of the sentence encoder.
- **Long-document SOTA (best fit for books)**: Yu et al. [2310.11772] pair a **Longformer** long-context encoder with enhanced coherence modeling; it improves WIKI-727K **F1 73.74→77.16 (+3.42)** and **Pk 15.0→13.89 (−1.11)**, with only an 8.38 % relative Pk rise out-of-domain — i.e. it holds up under domain shift, the key property for arbitrary technical books.
- **Training-free fallbacks**: Unsupervised BERT-embedding adjacency segmenters for meetings [2106.12978] and utterance-pair-coherence dialogue segmentation [2106.06719] (plus domain-knowledge injection for long MOOC lectures [2012.07589]) confirm the round-1 unsupervised primitives ([2306.01169], [2305.14806]) are sound when no in-domain training data exists.
- **Evaluation**: the standard metrics are **Pk** and **WindowDiff** (penalty-windowed boundary-disagreement rates, lower = better); the survey stresses these must be reported and that cross-domain evaluation is the field's weak point.

**→ Concrete recommendation for pipeline Stage 2 (topical-unit boundaries).** Use a **supervised neural topic segmenter on a long-context transformer with an auxiliary coherence objective** — the Yu et al. [2310.11772] architecture class (Longformer + coherence) as the target, trained on WIKI-727K / WikiSection [1803.09337]. Ship **cross-segment BERT [2004.14535] as the v1 default** (cheapest to implement, strong, operates per-candidate-break so it composes with the round-1 structural tree), and keep the **unsupervised embedding-adjacency segmenter ([2306.01169]/[2106.12978]) as the zero-training fallback** for out-of-distribution books. Gate boundary quality with **Pk + WindowDiff** against a small hand-segmented book sample. This replaces the round-1 reliance on summarization-embedded heuristics with a benchmarked, domain-shift-robust segmenter.

### Theme 3 — Candidate knowledge-unit identification

**Coverage**: 5 papers | **Confidence**: Medium-High
**Supporting**: [2406.10370], [2606.10716], [2502.00448], [2210.16422], [2305.14806]

This is Phase-2B. Papers-to-Posts [2406.10370] is the best **enumeration** primitive: a "reverse source outline" emits **1–3 atomic bullets per paragraph, each backlinked to its source paragraph** — i.e. *provenance-anchored* candidate units, exactly the shape claim extraction needs. Attention-Expansion KPE [2606.10716] frames unit detection as **BIO span tagging** with an F1@K protocol and confirms (with AWESOME) that **local-chunk reading under-recalls boundary-spanning units**, fixable cheaply with neighbouring-chunk context (~3.6% overhead). HERA [2502.00448] reframes the task as **regrouping scattered evidence**: attach a one-sentence summary KEY to each segment, LLM-retrieve a topic's segments into a per-event "bag", reorder, then map-reduce (+8.8% ROUGE-1 / +17.9% FactCC, training-free). Lodoss [2210.16422] contributes a **DPP diversity selector** to deduplicate candidate units within a segment.

Key findings:
1. Emit **provenance-anchored atomic units** (bullet ↔ source paragraph) so every candidate is traceable [2406.10370].
2. **Read with neighbour context**, not isolated chunks, or boundary-spanning units are missed [2606.10716], [2305.14806].
3. **Regroup scattered evidence by topic** before unit selection to recover dispersed claims [2502.00448].

### Theme 4 — Salience & ranking with global context

**Coverage**: 5 papers | **Confidence**: High
**Supporting**: [1905.13164], [2203.09629], [2405.00657], [2305.14806], [2502.00448]

The recurring recall risk is **chunk-local salience**. Hierarchical Transformers [1905.13164] validate **rank-then-encode**: a learned ranker scores every paragraph, forwards only the best, then a **local/global** encoder models units in isolation and mixes across them — beating a flat Transformer with far fewer tokens. AWESOME [2305.14806] shows a salience model must judge importance with **global past+future context**; HERA [2502.00448] and Hierarchical Transformers concur. Structural priors feed the ranker: HiStruct+ title-class [2203.09629] and the RST-LoRA per-EDU importance scalar [2405.00657].

Key finding: **Salience must be judged globally, not per-chunk** — the single most-supported lever for candidate-unit recall (4 papers).

### Theme 5 — Long-context reading & chunking architecture

**Coverage**: 5 papers | **Confidence**: High
**Supporting**: [2004.05150], [2606.10921], [2310.00785], [2505.06862], [1905.13164]

Longformer/LED [2004.05150] is the enabling linear-cost **reader** (windowed + a few global tokens, $O(n\cdot w)$; LED improves as input grows to 16k tokens) — but even 16k ≪ a 200+ page book, so it reads *nodes* under an outer map. The decisive architectural choice is **how to build the map**: BooookScore [2310.00785] shows **hierarchical (bottom-up) merging is more coherent than incremental updating**, whose forced running-summary compression erodes recall. DocTrace's **on-demand** memory [2606.10921] materializes structure per need rather than indexing the whole book (−53% compute). SPIN [2505.06862] is the **negative exemplar**: fixed-window `L=⌈K/4096⌉` chunking is structure-blind and fragments topics.

Key finding: prefer **hierarchical merging over a structure tree** to flat or incremental reading (compute *and* recall).

### Theme 6 — Evaluating the map and the units

**Coverage**: 13 papers (10 claim/coverage-eval added round 3) | **Confidence**: High (G3 closed)
**Supporting**: [2310.00785], [2604.25130], [2606.10716]
**Round-3 claim/coverage-evaluation corpus**: [2305.14251], [2502.10855], [2501.03545], [2404.11793], [2005.01619], [2110.10577], [2306.03853], [2407.03572], [2212.08514], [2004.14425]

Validation is well-solved *for summarization*. BooookScore [2310.00785] gives a **reference-free, per-unit error-rate** metric (LLM judges each unit against an error taxonomy; judge validated on **precision, not recall**). LongSumEval [2604.25130] supplies a summarization-**recall axis**: coverage = fraction of importance-ranked source questions the output can answer (the unanswered set is an actionable miss-list), plus a **feedback-driven refinement loop**. KPE's F1@K [2606.10716] measures extractive unit precision/recall directly. Caveat: LongSumEval validated only to ~27k words and question-generation hit a ~60% comprehensiveness ceiling — and both are summary-oriented, not claim/principle-oriented.

#### G3 closure — claim / principle-level recall & coverage evaluation (round 3)

The round-3 corpus supplies the missing **claim/principle-level recall** axis that summarization-QA and keyphrase recall@K only proxied. Two complementary mechanisms recur:

1. **Atomic decomposition into a reference claim set.** FActScore [2305.14251] breaks a generation into a series of **atomic facts** and scores the fraction supported — establishing the atomic-claim as the unit of measurement (precision side; the decomposition step is the reusable primitive). Claimify [2502.10855] is an **LLM-based claim extractor that emits a claim only under high confidence and resolves ambiguity/decontextualization**, and — critically — ships an **evaluation framework with explicit coverage and decontextualization measures**. Core [2407.03572] adds informative sub-claim selection for robust precision.
2. **Coverage / exhaustiveness against that reference set via matching.** Key Point Analysis [2005.01619] frames a **key point as a high-level claim/principle** whose salience = number of matching arguments, evaluated by **key-point↔argument matching**; the KPA-2021 Shared Task [2110.10577] operationalizes a **coverage track** (fraction of reference key points matched, scored by crowd labeling) and [2306.03853] extends key points into a **hierarchy** (directly relevant to a part→chapter→principle map). Khosravani et al. [2404.11793] introduce an **automatic coverage metric that prioritizes exhaustiveness** (= recall of key points, penalizing missed ones) for key-point generation. Samarinas et al. [2501.03545] generalize this to **coverage of diverse factual information in long-form text**, decomposing into atomic claims + query aspects and defining an explicit coverage score. Check-worthy claim detection [2212.08514], [2004.14425] supplies the filter for *which* source claims are worth enumerating.

**→ Concrete recommendation for the Step-10 source-map coverage gate.** Adopt a **two-layer claim-recall protocol** that replaces the summarization-QA + keyphrase-recall@K proxies:

- **Layer A — reference set.** Build a gold/silver reference set of the source's atomic claims/principles via FActScore-style atomic decomposition [2305.14251] using a high-precision, ambiguity-aware extractor (Claimify [2502.10855]); apply a check-worthiness filter [2212.08514] to keep extractable *principles* (not trivia).
- **Layer B — coverage metric.** Define **source-map recall = fraction of reference claims matched by an extracted unit**, using KPA-style key-point↔claim **matching** [2005.01619] as the matcher and the **exhaustiveness/coverage metric** of [2404.11793] / long-form coverage of [2501.03545] as the score; aggregate **hierarchically per part→chapter→section** (mirroring the key-point hierarchy of [2306.03853]) so a 200+-page book is scored section-by-section rather than as one flat pool — this is also how to beat LongSumEval's ~60 % comprehensiveness ceiling [2604.25130].

This makes the Step-10 gate measure the **downstream objective directly** (did we enumerate every extractable principle?) instead of a summary proxy, and pairs naturally with BooookScore [2310.00785] for the precision side → a dual precision+recall harness in the *claim* unit.

```mermaid
flowchart TD
    P0["(0) Parse PDF -> clean Markdown + reading order<br/>ParseFixer 2606.11977"] --> P1
    P1["(1) Build part->chapter->section->passage tree<br/>BuildDocTree 2606.10921 · align 2105.08209 · address 2203.09629"] --> P2
    P2["(2) Segment each node topically<br/>cross-segment BERT 2004.14535 · long-doc coherence 2310.11772 · unsup fallback 2306.01169/2106.12978 · eval Pk/WindowDiff 2411.16613"] --> P3
    P3["(3) Enumerate provenance-anchored candidate units<br/>Papers-to-Posts 2406.10370 · KPE 2606.10716 · HERA 2502.00448"] --> P4
    P4["(4) Rank salience with GLOBAL context + role priors<br/>rank-then-encode 1905.13164 · HiStruct+ · RST-LoRA 2405.00657"] --> P5
    P5["(5) Read nodes long-context<br/>Longformer/LED 2004.05150 · on-demand 2606.10921"] --> P6
    P6["(6) Validate precision + CLAIM-RECALL + feedback<br/>precision BooookScore 2310.00785 · claim-recall: decompose 2305.14251/2502.10855 + match-coverage 2005.01619/2404.11793/2501.03545"]
    P6 -. "miss-list -> re-segment / re-enumerate" .-> P2
```

## Methodology Comparison

| Approach (paper) | Mechanism | Max scale shown | Structure source | Scales to 200+ pp? | Downstream role |
|---|---|---|---|---|---|
| DocTrace [2606.10921] | Two-tier parser → 4-level tree; on-demand hypergraph memory | ≥250k tokens | parsed from raw | **Yes** | Build tree (2A); selective reading |
| BookSum [2105.08209] | Coarse-to-fine alignment + stable matching | ~110k words/book | metadata + embed | Yes (narrative) | Re-anchor flat text to tree |
| HiStruct+ [2203.09629] | Structure vector + title-class embedding | arXiv/PubMed article | gold sections | Concept yes | Address/role-tag units |
| Hierarchical Transf. [1905.13164] | Rank-then-encode; local/global; structure graph | multi-doc cluster | ranker | Concept yes | Global-context ranking |
| Lodoss [2210.16422] | Joint seg+extract heads; DPP diversity | 3k–8k words | gold boundaries | Per-segment only | Joint segment + candidate select |
| C2F-FAR [2306.01169] | Adjacency-dissimilarity blocks + centroid filter | article | none (unsup.) | Yes (per node) | Unsupervised segmentation |
| AWESOME [2305.14806] | Semantic-sim segmentation + global-context salience + gated memory | long doc | none (unsup.) | Yes (per node) | Segment + salience |
| HERA [2502.00448] | Segment KEY + LLM-retrieve scattered evidence bags | arXiv/PubMed | LLM topical | Yes (training-free) | Regroup candidate units |
| Papers-to-Posts [2406.10370] | Reverse-outline provenance bullets | paper | per-paragraph | Yes (per section) | Enumerate candidate units |
| KPE [2606.10716] | BIO span tagging + neighbour-context | long doc | none | Yes (cheap) | First-pass unit generator |
| RSTformer [2305.16784] | n-best RST distribution into attention | chapter | DMRST parser | No (tensor cost) | Soft discourse prior |
| RST-LoRA [2405.00657] | RST matrix → per-EDU importance scalar (LoRA) | chapter | RST parser | No (parser) | Per-unit importance feature |
| Longformer/LED [2004.05150] | Windowed + global attention | 4k–16k tokens | none | Node-level only | Long-context node reader |
| BooookScore [2310.00785] | Per-unit error-rate; merge-vs-incremental study | book | n/a | Yes (eval) | Precision/coherence validation |
| LongSumEval [2604.25130] | QA-coverage recall + feedback loop | ~27k words | n/a | Partial (eval) | Recall validation |
| SPIN [2505.06862] | Fixed-window chunk + concat | very long | none | Negative exemplar | Fallback split / LCS align |

## Confidence-Graded Findings

### 🟢 High Confidence (3+ papers, consistent)

1. **Flat/fixed-window reading is the wrong baseline; use explicit hierarchy + content-based selection.** — [2505.06862] (neg.), [2004.05150], [2105.08209], [2606.10921], [1905.13164]. Flat input *degrades* past ~800 tokens [1905.13164]; structure-aware processing also roughly halves token cost [2606.10921].
2. **Candidate-unit salience must be judged with global context**, or boundary-spanning and scattered units are missed — the core recall risk. — [2305.14806], [2606.10716], [2502.00448], [1905.13164].
3. **Build the map by hierarchical (bottom-up) merging, not incremental running-summary**, whose compression step erodes recall. — [2310.00785], reinforced by [1905.13164], [2105.08209].
4. **Validate both precision *and* recall**, with a precision-validated LLM judge. — [2310.00785] (precision/coherence) + [2604.25130] (recall/coverage) + [2606.10716] (F1@K).
5. **Stamp every unit with a structural address + role class.** — [2203.09629], [2606.10921], [1804.05685].

### 🟡 Medium Confidence (1–2 papers or caveats)

1. **Raw book → TOC tree is solvable** with a two-tier parser + coarse-to-fine alignment. — [2606.10921] (medium confidence; single benchmark), [2105.08209] (validated on narrative books).
2. **Provenance-anchored enumeration + scattered-evidence regrouping** lifts both recall and precision. — [2406.10370], [2502.00448].
3. **A cheap per-unit salience scalar** (from structure/discourse) can feed rank-then-encode. — [2203.09629], [2405.00657].

### 🔴 Low Confidence (single-source / scale-limited)

1. **Full-document RST discourse structure** improves selection but is parser-fragile and does not scale past a chapter. — [2305.16784], [2405.00657].
2. **Joint single-encoder segmentation+salience** is elegant but demonstrated only at article scale on gold boundaries. — [2210.16422].

## Trade-Off Analysis

| Decision | Option A | Option B | Recommendation |
|---|---|---|---|
| Map construction | **Hierarchical merging** (coherent, recall-preserving) [2310.00785] | Incremental running-summary (cheap, lossy) | **A** — merge bottom-up over the tree |
| Chunking | **Structure-aware** node boundaries [2606.10921], [2210.16422] | Fixed-window `⌈K/4096⌉` [2505.06862] | **A**; keep B only as fallback when parsing fails |
| Structure source | **Parsed-from-raw** two-tier parser [2606.10921] | Assume gold sections [2203.09629], [2210.16422] | **A** for real books; B's features still apply after parsing |
| Salience context | **Global** past+future [2305.14806], [1905.13164] | Chunk-local | **A** — local under-recalls boundary units |
| Reading cost | **On-demand / selective** [2606.10921], [2606.11977] | Index/repair everything | **A** — cheap parser everywhere, costly work only where checks fail |
| Discourse signal | **Soft per-unit importance scalar** [2405.00657] | Full RST tensor in attention [2305.16784] | **A** — scalar scales; full tensor does not |

## Points of Agreement

1. **Hierarchy beats flatness** for long input — [2505.06862], [2004.05150], [2105.08209], [2606.10921], [1905.13164].
2. **Position/lead heuristics fail**; salience must be content-based and global — [2105.08209], [2305.14806], [1905.13164].
3. **Independent per-unit selection breeds redundancy/incoherence**; mix across units (DPP, local/global, hierarchical merge) — [2210.16422], [1905.13164], [2310.00785].

## Points of Contradiction

1. **Is automatic ROUGE/QA enough to trust a candidate-unit set?** C2F-FAR [2306.01169] reports automatic-metric "success" while its own human eval found coherence/faithfulness failures; BooookScore [2310.00785] argues for reference-free per-unit error rates instead. *Explanation*: ROUGE rewards lexical overlap, not unit-level faithfulness. *Implication*: validate the Phase-2B output with per-unit, reference-free checks, not ROUGE.
2. **Joint vs. staged segmentation.** Lodoss [2210.16422] argues segmentation and selection should be learned *jointly*; the DocTrace/BookSum line treats structure extraction as a separate upstream stage. *Explanation*: joint training needs gold boundaries (unavailable for arbitrary books). *Implication*: stage them for raw books; revisit joint training only where boundaries are reliable.

## Research Gaps

| # | Gap | Type | Severity | Impact on Goals |
|---|-----|------|----------|----------------|
| ~~G1~~ | ✅ **CLOSED (round 2)** — standalone topic/linear segmentation literature added (survey [2411.16613]; supervised SOTA [1803.09337], [2004.14535], [2310.11772]); Stage-2 method recommended | ACADEMIC | ~~HIGH~~ → resolved | Stage 2 now has a benchmarked, domain-shift-robust segmenter |
| ~~G3~~ | ✅ **CLOSED (round 3)** — claim/principle-recall protocol defined (decompose [2305.14251]/[2502.10855] + match-coverage [2005.01619]/[2404.11793]/[2501.03545]) | ACADEMIC | ~~HIGH~~ → resolved | Step-10 gate can now measure extraction recall directly |
| G2 | Raw-book TOC extraction for **expository** books validated thinly (one recipe; alignment shown on narrative) | ACADEMIC | MEDIUM | Phase-2A robustness on textbooks |
| G4 | Expository/technical **book discourse structure** under-represented (RST work is news/abstracts) | ACADEMIC | MEDIUM | Argument/prereq structure of textbooks |
| G5 | Cross-reference / prerequisite-dependency graph extraction across a book | ACADEMIC | LOW | Linking units across chapters |
| E1 | No released code confirmed except Longformer/LED | ENGINEERING | MEDIUM | Re-implementation cost |
| E2 | Inter-stage node-schema contract specified by no single paper | ENGINEERING | MEDIUM | Pipeline integration |
| E3 | Validator scaling (BooookScore judge cost; LongSumEval ~60% question ceiling ≤27k words) | ENGINEERING | MEDIUM | Evaluating at true book length |

### Academic Gaps

1. ✅ **G1 — Topic/linear segmentation (HIGH) — CLOSED in round 2.** 9 standalone papers added; see [Theme 2 / G1 closure](#g1-closure--standalone-topic--linear-text-segmentation-round-2). Recommendation: supervised long-context coherence segmenter ([2310.11772] class), cross-segment BERT [2004.14535] as v1 default, unsupervised embedding-adjacency fallback, evaluated with Pk/WindowDiff.
2. ✅ **G3 — Claim/principle-level recall evaluation (HIGH) — CLOSED in round 3.** 10 papers added; see [Theme 6 / G3 closure](#g3-closure--claim--principle-level-recall--coverage-evaluation-round-3). Recommendation: two-layer protocol = atomic decomposition ([2305.14251]/[2502.10855]) + key-point match-coverage/exhaustiveness ([2005.01619]/[2404.11793]/[2501.03545]), aggregated hierarchically per section.
3. **G2 — Raw-book TOC/heading-hierarchy extraction (MEDIUM, still open)**. `"table of contents extraction heading hierarchy detection long PDF book structure"`.
4. **G4 — Expository-book discourse structure (MEDIUM)**. `"expository technical textbook discourse structure segmentation argument"`.
5. **G5 — Cross-reference / prerequisite graph (LOW)**. `"cross-reference resolution prerequisite graph textbook long document"`.

### Engineering Gaps (fillable without papers)

1. **E1 — Implementations**: re-implement DocTrace `BuildDocTree`, the C2F-FAR adjacency primitive, and Papers-to-Posts reverse-outline against the BooookScore+LongSumEval harness. *Resolution*: build minimal versions; validate each stage on the existing 131k-word concurrency book.
2. **E2 — Node schema**: define one contract `{node_id, parent_id, level∈{part,chapter,section,passage}, span, title, role_class, structural_address, salience, provenance}` flowing through all stages. *Resolution*: adopt HiStruct+ address + Papers-to-Posts provenance fields.
3. **E3 — Validator scaling**: make question generation **hierarchical/per-section** (LongSumEval hits a ceiling on whole books) and sample units for the BooookScore judge. *Resolution*: per-section QA generation + stratified judging.

## Reproducibility Notes

| Paper | Code | Data | Sufficient detail | Notes |
|-------|------|------|-------------------|-------|
| Longformer/LED [2004.05150] | ✅ (allenai/longformer) | ✅ | ✅ | Widely reproduced |
| BookSum [2105.08209] | ✅ | ✅ | ✅ | Benchmark, reusable |
| BooookScore [2310.00785] | ✅ (stated) | ⚠️ contamination-controlled | ✅ | Reference-free metric |
| HiStruct+ [2203.09629] | ⚠️ | ✅ (arXiv/PubMed) | ✅ | Consumes gold structure |
| Hierarchical Transformers [1905.13164] | ⚠️ | ✅ | ✅ | Foundational |
| DocTrace [2606.10921] | ❓ (preprint) | ⚠️ single benchmark | ⚠️ | Most novel; medium confidence |
| LongSumEval [2604.25130] | ❓ (preprint) | ⚠️ ≤27k words | ✅ | Recall metric + loop |
| Others (RST/HERA/C2F-FAR/Papers-to-Posts/KPE/AWESOME/Lodoss/SPIN/ParseFixer) | mostly ❓/⚠️ | mixed | mixed | Methods transferable regardless |
| 6 OCR-timeout papers (2207.00939, 2203.10741, 2203.07586, 2104.02112, 1910.14142, 2005.01840) | — | — | — | **Not deep-analyzed** (abstract-level only) |

## Practical Recommendations

Anchored to the Phase-2A/2B preprocessor; each cites supporting evidence.

1. **Adopt the 7-stage reference pipeline** (diagram in [Theme 6](#theme-6--evaluating-the-map-and-the-units)) as the architecture: parse → build tree → segment → enumerate units → rank (global) → read → validate. *Confidence*: Medium-High. *Basis*: cross-paper convergence.
2. **Build the tree with a two-tier parser + alignment fallback** [2606.10921], [2105.08209], and **stamp each node with structural address + role class** [2203.09629]. *Confidence*: Medium.
3. **Make every candidate unit provenance-anchored and atomic** (bullet ↔ source span) [2406.10370] — this is exactly the granularity claim extraction consumes, and it gives free traceability for the factory's provenance ledger. *Confidence*: Medium-High.
4. **Read with neighbour context and rank salience globally** [2606.10716], [2305.14806], [1905.13164] — the highest-leverage move for extraction *recall*. *Confidence*: High.
5. **Prefer hierarchical merging over incremental** when rolling units up to chapter/part summaries [2310.00785]. *Confidence*: High.
6. **Segment Stage-2 boundaries with a supervised long-context coherence segmenter.** Target the Yu et al. [2310.11772] architecture class (Longformer + coherence; WIKI-727K F1 77.16 / Pk 13.89, robust under domain shift); ship **cross-segment BERT [2004.14535] as the v1 default** (cheap per-candidate-break classifier) and keep an **unsupervised embedding-adjacency segmenter ([2306.01169]/[2106.12978]) as the zero-training fallback**; evaluate boundaries with **Pk + WindowDiff** [2411.16613], [1803.09337]. *Confidence*: High. *Basis*: closes G1.
7. **Gate Step-10 source-map coverage with a two-layer claim-recall protocol.** (A) Decompose the source into a reference atomic-claim/principle set (FActScore-style [2305.14251] via high-precision Claimify [2502.10855], check-worthiness-filtered [2212.08514]); (B) score **recall = fraction of reference claims matched**, using KPA key-point matching [2005.01619] + an exhaustiveness/long-form coverage metric [2404.11793], [2501.03545], aggregated **per part→chapter→section** [2306.03853]. Pair with BooookScore [2310.00785] for precision. *Confidence*: High. *Basis*: closes G3; replaces the summary-QA/keyphrase proxies.
8. **Validate with a dual harness**: BooookScore-style per-unit error rate (precision) + the claim-recall coverage metric above (recall) with a feedback loop, made per-section for book scale [2310.00785], [2604.25130], [2501.03545]. *Confidence*: High.
9. **Keep fixed-window chunking only as a fallback** when parsing fails [2505.06862]. *Confidence*: High.

## Readiness Assessment (System-Building Mode)

### Verdict: READY_WITH_MINOR_GAPS (both HIGH gaps closed)

### Assessment Summary
The synthesis is now **sufficient to design and substantially de-risk** the Phase-2A/2B preprocessor: there is a concrete, book-scale-validated tree builder, a **benchmarked, domain-shift-robust Stage-2 segmenter recommendation** (G1 closed, round 2), transferable enumeration/salience primitives, and a **claim/principle-level recall metric** for the Step-10 coverage gate (G3 closed, round 3) that measures the downstream objective directly rather than via summary proxies. Remaining gaps are MEDIUM/LOW academic (G2 expository-TOC robustness, G4 expository discourse, G5 cross-reference graph) and ENGINEERING (E1–E3); none blocks a first implementation.

### Coverage Matrix

| Dimension | Status | Evidence |
|-----------|--------|----------|
| Architecture patterns | ✅ Sufficient | [2606.10921], [2105.08209], [1905.13164], [2310.00785] |
| Technology stack | ✅ Sufficient | Longformer/LED reader, docling/ParseFixer ingest, BM25+embedding index |
| Performance baselines | ✅ Sufficient | Segmentation Pk/WindowDiff SOTA [2310.11772], [2004.14535]; claim-recall coverage protocol [2502.10855], [2404.11793], [2501.03545] (G3 closed) |
| Segmentation method coverage | ✅ Sufficient | Standalone supervised + unsupervised segmenters [2411.16613], [1803.09337], [2310.11772] (G1 closed) |
| Trade-off map | ✅ Sufficient | [Trade-Off Analysis](#trade-off-analysis) |
| Security model | ➖ N/A | Preprocessing review |

### Gap Resolution Plan

| # | Gap | Type | Severity | Resolution |
|---|-----|------|----------|------------|
| G1 | Standalone topic segmentation | ACADEMIC | ~~HIGH~~ | ✅ **CLOSED round 2** — 9 papers; Stage-2 segmenter recommended ([2310.11772]/[2004.14535], Pk/WindowDiff) |
| G3 | Claim-level recall metric | ACADEMIC | ~~HIGH~~ | ✅ **CLOSED round 3** — 10 papers; two-layer coverage gate ([2305.14251]/[2502.10855] + [2005.01619]/[2404.11793]/[2501.03545]) |
| G2/G4/G5 | Book TOC / expository discourse / xref graph | ACADEMIC | MED/LOW | Still open; opportunistic in later work, else accept as scoped (not HIGH) |
| E1–E3 | Code / schema / validator scaling | ENGINEERING | MED | Resolved inline (above) |

## Evidence Map

| Research aspect | Tree build | Segment | Enumerate units | Rank/salience | Read | Evaluate |
|---|---|---|---|---|---|---|
| Structure extraction (2A) | ✓ 2606.10921, 2105.08209, 2203.09629, 2606.11977 | | | | | |
| Topic/discourse segmentation | ✓ 1804.05685 | ✓ 2210.16422, 2306.01169, 2305.14806, 2305.16784, 2405.00657 | | | | |
| **Standalone segmentation (R2/G1)** | | ✓ 2411.16613, 1803.09337, 2004.14535, 2001.00891, 2110.07160, 2310.11772, 2106.12978, 2106.06719, 2012.07589 | | | | ✓ Pk/WindowDiff 2411.16613 |
| **Claim/principle-recall eval (R3/G3)** | | | ✓ decompose 2305.14251, 2502.10855, 2407.03572 | | | ✓ coverage 2005.01619, 2110.10577, 2306.03853, 2404.11793, 2501.03545; filter 2212.08514, 2004.14425 |
| Candidate-unit ID (2B) | | ✓ 2210.16422 | ✓ 2406.10370, 2606.10716, 2502.00448 | | | |
| Salience / recall | | | ✓ 2305.14806 | ✓ 1905.13164, 2203.09629, 2405.00657 | | |
| Long-context reading | | | | | ✓ 2004.05150, 2606.10921 | |
| Chunking architecture | | | | | ✓ 2310.00785, 2505.06862 | ✓ 2310.00785 |
| Evaluation | | | | | | ✓ 2310.00785, 2604.25130, 2606.10716 |

## References

1. [2606.10921] Trace Only What You Need: Structure-Aware On-Demand Hypergraph Memory for Long Documents (DocTrace). Zai et al. 2026. Preprint.
2. [2210.16422] Toward Unifying Text Segmentation and Long Document Summarization (Lodoss). Cho et al. 2022. EMNLP.
3. [2203.09629] HiStruct+: Improving Extractive Text Summarization with Hierarchical Structure Information. Ruan et al. 2022. ACL Findings.
4. [1905.13164] Hierarchical Transformers for Multi-Document Summarization. Liu & Lapata. 2019. ACL.
5. [2310.00785] BooookScore: A Systematic Exploration of Book-length Summarization in the Era of LLMs. Chang et al. 2023. ICLR.
6. [2604.25130] LongSumEval: Question-Answering Based Evaluation and Feedback-Driven Refinement. Nguyen et al. 2026. Preprint.
7. [2105.08209] BookSum: A Collection of Datasets for Long-form Narrative Summarization. Kryściński et al. 2021. EMNLP Findings.
8. [2406.10370] Papers-to-Posts: Supporting Detailed Long-Document Summarization. Radensky et al. 2024. Preprint.
9. [2502.00448] HERA: Improving Long Document Summarization using Large Language Models. Li et al. 2025. Preprint.
10. [2004.05150] Longformer: The Long-Document Transformer. Beltagy et al. 2020. arXiv.
11. [2305.14806] AWESOME: GPU Memory-constrained Long Document Summarization. Cao & Wang. 2023. NAACL.
12. [2606.11977] ParseFixer: An Agentic Framework for Document Parsing. Yu et al. 2026. Preprint.
13. [1804.05685] A Discourse-Aware Attention Model for Abstractive Summarization of Long Documents. Cohan et al. 2018. NAACL.
14. [2305.16784] Incorporating Distributions of Discourse Structure for Long Document Summarization (RSTformer). Liu et al. 2023. ACL.
15. [2405.00657] RST-LoRA: A Discourse-Aware Low-Rank Adaptation for Long Document Summarization. Liu & Lapata. 2024. NAACL.
16. [2306.01169] Hybrid Long Document Summarization using C2F-FAR and ChatGPT. Lu et al. 2023. arXiv.
17. [2606.10716] Attention Expansion: Enhancing Keyphrase Extraction from Long Documents. Martínez-Cruz et al. 2026. Preprint.
18. [2505.06862] A Split-then-Join Approach to Abstractive Summarization for Very Long Documents (SPIN). Fazry et al. 2025. Preprint.

**Round 2 — standalone topic / linear text segmentation (G1):**
19. [2411.16613] Recent Trends in Linear Text Segmentation: a Survey. Ghinassi et al. 2024.
20. [1803.09337] Text Segmentation as a Supervised Learning Task (WIKI-727K). Koshorek et al. 2018. NAACL.
21. [2004.14535] Text Segmentation by Cross Segment Attention. Lukasik et al. 2020. EMNLP.
22. [2001.00891] Two-Level Transformer and Auxiliary Coherence Modeling for Improved Text Segmentation. Glavaš & Somasundaran. 2020. AAAI.
23. [2110.07160] Transformer over Pre-trained Transformer for Neural Text Segmentation with Enhanced Topic Coherence (Topseg). Lo et al. 2021. EMNLP Findings.
24. [2310.11772] Improving Long Document Topic Segmentation Models With Enhanced Coherence Modeling. Yu et al. 2023. EMNLP.
25. [2106.12978] Unsupervised Topic Segmentation of Meetings with BERT Embeddings. Solbiati et al. 2021.
26. [2106.06719] Improving Unsupervised Dialogue Topic Segmentation with Utterance-Pair Coherence Scoring. Xing & Carenini. 2021. SIGDIAL.
27. [2012.07589] Incorporating Domain Knowledge To Improve Topic Segmentation of Long MOOC Lectures. 2020.

**Round 3 — claim / principle-level recall & coverage evaluation (G3):**
28. [2305.14251] FActScore: Fine-grained Atomic Evaluation of Factual Precision in Long Form Text Generation. Min et al. 2023. EMNLP.
29. [2502.10855] Towards Effective Extraction and Evaluation of Factual Claims (Claimify). 2025.
30. [2501.03545] Beyond Factual Accuracy: Evaluating Coverage of Diverse Factual Information in Long-form Text Generation. Samarinas et al. 2025.
31. [2404.11793] Enhancing Argument Summarization: Prioritizing Exhaustiveness in Key Point Generation and Introducing an Automatic Coverage Evaluation Metric. Khosravani et al. 2024.
32. [2005.01619] From Arguments to Key Points: Towards Automatic Argument Summarization (ArgKP). Bar-Haim et al. 2020. ACL.
33. [2110.10577] Overview of the 2021 Key Point Analysis Shared Task. Friedman et al. 2021. ArgMining.
34. [2306.03853] From Key Points to Key Point Hierarchy: Structured and Expressive Opinion Summarization. 2023. ACL.
35. [2407.03572] Core: Robust Factual Precision with Informative Sub-Claim Identification. 2024.
36. [2212.08514] Check-worthy Claim Detection across Topics for Automated Fact-checking. 2022.
37. [2004.14425] A Benchmark Dataset of Check-worthy Factual Claims. 2020. ICWSM.

*Cited at abstract level (not deep-analyzed):* [2207.00939] Empirical Survey on Long Document Summarization (2022); [2203.10741] HIBRIDS (2022); [2203.07586] Top-down/Bottom-up Inference (2022); [1910.14142] Discourse-Aware Neural Extractive Summarization (2019); [2005.01840] Content Selection in Novel Chapters (2020).

## Appendix: Run Metadata

- **Run ID**: longdoc-r1-20260611
- **Sources**: arXiv, Semantic Scholar, OpenAlex, DBLP, HuggingFace + Semantic Scholar citation graph
- **Profile**: deep
- **Candidates → screened → analyzed**: 580 → 50 → 18
- **Date**: 2026-06-12
- **Artifacts**: `runs/longdoc-r1-20260611/` (plan, search, screen, expand, download, convert, extract, summarize, analysis)
- **Known limitations**: 6 canonical PDFs failed OCR-heavy conversion (abstract-level only); standalone topic-segmentation and claim-recall evaluation under-covered (G1, G3) — addressed in subsequent rounds.
