# Step 14 — Runtime Retrieval (distill-vs-retrieve + grounded citation)

> Folds `docs/Research/rag-graphrag/` (20+ papers, validated PASS 1.0) into an executable spec. This
> is the **G-track** of `research-integration-plan.md` and the long-open **§20 #10 (RAG/GraphRAG)**.
> **Post-v0 / design capture** — it specs a *runtime knowledge layer* for generated agents; nothing
> here is built yet, and 3 of its core questions are open in the literature (see Caveats).

**Goal** — Give a generated expert a principled **runtime knowledge layer**: a *deterministic*
distill-vs-retrieve routing rule + a passage-grounded retrieval/citation spine, so it carries stable
rules in-prompt and retrieves volatile / long-tail / large / citation-bearing knowledge at runtime,
**always citing real source passages**.

## Core finding

**Distill and retrieve are complementary, not exclusive.** Bake stable, transferable, always-on rules
into the prompt/parameters; retrieve volatile, long-tail, large, or citation-bearing knowledge at
runtime, via a **self-routing hybrid**. The retrieval spine should be **deterministic** — LLM calls
reserved for index build, (optional) gating, and synthesis. For graphs: **use the graph to aid
retrieval of real, citable passages — do not replace the corpus with LLM summaries.**

## Relationship to existing work

- **Extends `knowledge_partition`** — today the factory decides *by hand* what goes in `always_on`
  (distilled) vs `skills`/`references` (files). Step 14 makes that a deterministic routing rule.
- **Runtime, not authoring-time.** Step 7 (principle graph) + knowledge-fusion build the graph at
  authoring time; Step 14 is *retrieval over that store at answer time*. Distinct concerns.
- **Pairs with Step 13** (ask-gate): the retrieval gate ("when to consult the store") is the same
  selective-prediction shape as the ask-gate ("when to ask/abstain").

## Built so far (2026-06-15) — G1 routing rule only

- **G1 — `tools/subagent_factory/knowledge_partition.py` BUILT.** `route_knowledge_item(reuse,
  volatility, size, citation_need)` + `partition_plan(items)` deterministically route each knowledge
  item **distill** (`always_on`) vs **retrieve** (`skills`/`references`): distill stable+high-reuse+
  small+non-citable; retrieve volatile / long-tail / large / citation-bearing; the research's
  *fine-tune* bucket degrades to retrieve (no training step) with a flag. **Advisory, not a gate** —
  defaults skew conservative (unknown → retrieve), and `measurement_required` reminds the caller that
  G1 is unproven (A/B the partition on the package's behaviour-tests before trusting it). Wired as
  guidance into the profile-generation skill §1.6. 11 tests. CLI:
  `python -m tools.subagent_factory.knowledge_partition --reuse … | --plan items.json`.
- **G2–G6 — still spec (deliberately).** The retrieval spine below stays unbuilt; the research's own
  guidance is to ship retrieval behind a per-package measurement, and G1–G3 are inherent ACADEMIC gaps
  (see Caveats). Building a speculative dense+rerank+PPR engine would violate the factory's "no
  building ahead of evidence" rule.

## New files (proposed — G2–G6 not built)

| Path | Kind | Purpose |
|---|---|---|
| `tools/subagent_factory/knowledge_partition.py` | tool (det) | ✅ **BUILT** — routing rule: classify each knowledge item distill / retrieve (/ fine-tune→retrieve) by reuse, volatility, size, citation-need. |
| retrieval spine | tool (det) | *(spec)* Hybrid dense(λ≈0.8)+BM25 over fixed-size chunks → distilled cross-encoder reranker; LLM only builds the index. |
| passage-grounded graph store | tool (det) | *(spec)* Principle/evidence graph that **returns real source passages**; Personalized-PageRank traversal for multi-hop; a deterministic classifier routes global-sensemaking queries to a precomputed-summary path. |
| retrieval gate | tool (det) | *(spec)* Selective "when to retrieve": uncertainty/complexity threshold + hard ≤3-iteration cap (never always-on top-1, never an unbounded LLM sufficiency gate). |
| grounded-citation + eval | tool (det) + LLM | *(spec)* Generate-then-cite (self-generate extractive quotes, then answer) + a deterministic verifier loop; evaluate grounding by **precision AND coverage**, never precision alone. |

## LLM ↔ deterministic split

| Deterministic | LLM |
|---|---|
| partition routing rule; hybrid retrieve + rerank; PPR traversal; gate threshold + iteration cap; citation verifier; precision+coverage scoring | index/summary build; (optional) sufficiency gating; final synthesis |

## Research inputs (recommendations → spec, with paper IDs)

1. **knowledge_partition = deterministic routing, not either/or** — distill stable/high-reuse/non-citable;
   retrieve volatile/long-tail/large/citable; fine-tune transferable bulk skill. [2401.08406],
   [2407.16833], [2005.11401]
2. **Default retrieval stack = deterministic** — hybrid dense(λ≈0.8)+BM25 over fixed chunks →
   distilled cross-encoder reranker; LLM only builds the index. [2401.04055], [2504.19754],
   [2304.09542], [2004.04906]
3. **Passage-grounded graph** — traverse deterministically (PPR) for multi-hop, **always return real
   source passages** for citation, route global queries to a precomputed-summary path via a
   deterministic classifier. [2502.14802], [2405.14831], [2404.16130], [2605.20815]
4. **Gate retrieval selectively** — deterministic uncertainty/complexity threshold + hard ≤3-iteration
   cap; learned policy if trainable; never always-on, never unbounded LLM sufficiency gate. [2604.26649],
   [2310.11511], [2510.22344]
5. **Ground with generate-then-cite; evaluate precision AND coverage** — self-generate extractive
   quotes then answer; deterministic verifier loop; never precision alone. [2408.04568], [2606.09376],
   [2309.15217]
6. **Distill at index time to cut runtime cost** — precompute summaries/community reports for global
   queries; keep runtime retrieval cheap + incremental (edge-addition updates). *(Medium)* [2404.16130],
   [2410.05779], [2405.14831]

## Caveats — 3 inherent open gaps (why this stays a spec)

The literature does **not** contain the factory's exact case, so these cannot be closed by more
research rounds (the round-3 attempt was rate-limited, but the gaps are inherent, not searchable):

- **G1 (HIGH, ACADEMIC):** no paper empirically compares an agent's **own** distilled principle store
  vs runtime retrieval (Expert Mind [2603.14541] proposes it, no results). Central to the partition
  rule — the factory would be charting new ground, so any partition policy ships behind a measurement.
- **G2 (HIGH, ACADEMIC):** retrieval over a **principle/argument graph** (typed claims with
  supports/contradicts/decision-criterion edges) is unstudied; all graph evidence uses entity KGs.
- **G3 (HIGH, ACADEMIC):** **graph-native per-claim citation/provenance** is open — keep passages
  (HippoRAG-2 style) and adapt flat-passage quote-citation (FRONT) until studied.
- ENGINEERING (resolved inline): a unified cost/latency budget model; graph scalability beyond ~10k
  passages; concrete default stack config; access-control/PII over the store.

## Exit criteria (when built)

- A deterministic `knowledge_partition` routing rule classifies a package's knowledge items, with a
  measurement comparing in-prompt vs retrieved on that package's behaviour-tests (closes G1 locally).
- A passage-grounded retrieval spine returns real source passages with per-claim citations; grounding
  scored on precision **and** coverage.
- `make verify` green; Tier-0 packages untouched (the layer is opt-in per package).

## Risks

- *Graph-replaces-corpus* (the GraphRAG failure mode) → rec 3: graph aids retrieval of real passages,
  never substitutes LLM summaries for sources.
- *Unbounded retrieval cost/loops* → rec 4: deterministic gate + hard iteration cap.
- *Citation theatre* (precision-only) → rec 5: precision + coverage, verifier loop.
- *Building ahead of evidence* (G1–G3) → ship any partition/retrieval policy behind a per-package
  measurement, not as a global default.
