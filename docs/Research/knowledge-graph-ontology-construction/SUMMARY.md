# Research Run Summary — Knowledge Graph & Ontology Construction for Principle Graphs

## 1. Final Report

**`knowledge-graph-ontology-construction-research-report.md`** — validated PASS (score 1.00).

Downstream use: Phase 7A of the subagent factory (the GRAPH half of Step 7 multi-source synthesis). Scope = graph/ontology representation + alias/relationship/taxonomy induction + provenance + deterministic-vs-LLM split. Cross-document contradiction detection deliberately excluded (sibling knowledge-fusion spike).

## 2. Round History

| Round | Run ID | Focus | New Papers | Gaps Addressed | Remaining |
|-------|--------|-------|------------|----------------|-----------|
| 1 | `4b9ab6b1354b` | Full topic | 18 full-text + 12 metadata-only | All 6 sub-questions covered | 2 HIGH academic, 1 MED academic, 3 engineering |
| 2 | `4b9ab6b1354b` (re-screen recovery) | Replace title-only DBLP shortlist with content-bearing OpenAlex full text | +18 converted | Grounding fidelity restored | HIGH academic gaps environment-limited |

**Stop reason**: HIGH academic gaps reclassified as environment-limited. Pipeline pathology this run: the original screen promoted 15 title-only DBLP records (no abstract, no PDF); the recency-locked arXiv slice returned off-topic 2026 preprints; Semantic Scholar was HTTP-429 throttled. A corpus-recovery re-screen pulled 30 on-topic OpenAlex classics (KG survey, NER, hypernymy, TransH/DistMult, PROV-O, WSD/entity-linking, semantic similarity); 20 downloaded, 18 converted (Docling), 10 paywalled failures. More search rounds cannot retrieve the remaining foundational corpus in this environment.

## 3. Remaining Open Gaps

| # | Gap | Type | Severity | One line |
|---|-----|------|----------|----------|
| 1 | Principle-graph induction (`refines`/`supports` over normative text) | ACADEMIC | HIGH | No reviewed work models normative-principle graphs; reclassified environment-limited (argumentation-mining literature paywalled / pre-recency-slice). |
| 2 | Principle-level deduplication / canonicalisation | ACADEMIC | HIGH | Aliasing abstract principles (not named entities) is unstudied; partially addressable by transferring entity-resolution cascades. |
| 3 | Taxonomy induction for small expert corpora | ACADEMIC | MEDIUM | Distributional hypernymy methods assume large text; `specialises` recall on small inputs uncertain. |
| 4 | Deterministic-vs-LLM division of labour | ENGINEERING | MEDIUM | Resolved inline (see report's Deterministic vs LLM Split). |
| 5 | Provenance edge schema for principle nodes/edges | ENGINEERING | LOW | Resolved via PROV-O mapping. |
| 6 | Foundational on-topic corpus not retrievable | ACADEMIC (env) | MEDIUM | Hogan KG survey, Wikidata, ConceptNet, distant-supervision RE, DBpedia full text paywalled / outside arXiv slice. |

## 4. Findings Most Relevant to the Downstream Use (Phase 7A)

1. **Represent the principle graph as a typed-triple multigraph with a separate concept/ontology (schema) layer** — field-wide consensus; keep principle-instances distinct from the concept taxonomy that types them. [openalex-W3003265726], [openalex-W3010336026], [openalex-W2622701666] *(High)*

2. **Use a small, closed, explicitly-directional edge vocabulary** (`refines`, `supports`, `specialises`, `alias`); edge type is the load-bearing design decision, exactly as KGs fix `subClassOf`/`instanceOf`. [openalex-W3003265726] *(High)*

3. **Never score asymmetric edges (`refines`/`specialises`) with a symmetric model.** DistMult's diagonal-bilinear score `h·diag(r)·t` cannot represent asymmetric relations; use a TransH-style hyperplane translation or record direction explicitly. [openalex-W1533230146], [openalex-W2283196293] *(High)*

4. **Deduplicate concepts / emit `alias` edges with a three-stage cascade**: deterministic surface blocking → distributional cosine similarity → graph-structural similarity once the graph is seeded. [openalex-W2050273484], [openalex-W1662133657], [openalex-W2523199059] *(High)*

5. **Treat aliasing as joint WSD + entity-linking** against a canonical inventory — "is this mention the same principle as an existing node?" is one decision, not two. [openalex-W2131540451] *(High)*

6. **Induce `specialises`/taxonomy edges with hybrid hypernymy detection** — combine Hearst-style dependency-path patterns with distributional similarity (HypeNET); propose, don't auto-commit. [openalex-W2962724755], [openalex-W2136930489], [openalex-W2145071552] *(Medium)*

7. **Adopt PROV-O for the provenance layer** rather than inventing one: `wasDerivedFrom` (source → principle), `wasAttributedTo` (deterministic stage vs LLM), `wasGeneratedBy` (extraction activity). Provenance is a quality differentiator, not optional metadata. [openalex-W1608781114], [openalex-W2622701666] *(High)*

8. **Deterministic-vs-LLM split = LLM proposes, deterministic layer decides.** LLMs already store recoverable relational knowledge (good proposers of nodes/edges/aliases) but hallucinate, so the canonical commit must be a deterministic, provenance-stamped, confidence-thresholded decision. [openalex-W2970476646], [openalex-W4388585881], [openalex-W2107598941] *(Medium)*

9. **Linking/disambiguation — not mention extraction — is the hard sub-problem** of construction; extraction (BiLSTM-CRF NER) is reliably learnable, so invest engineering effort in the alias/dedup and edge-typing layers. [openalex-W2296283641], [openalex-W2131540451], [openalex-W2523199059] *(High)*

## Artifacts
- Final report: `knowledge-graph-ontology-construction-research-report.md`
- Validation: `validation_result.json` / `validation.json` (PASS, 1.00)
- Gaps: `gaps.json`
- Run workspace: `runs/4b9ab6b1354b/` (18 converted markdowns, 114 scored claims, synthesis)
- State: `workflow_state.json` (status: complete), `round_state.json`
