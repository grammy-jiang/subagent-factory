# Step 7 — Multi-Source Synthesis (Principle Graph)

> Master: `docs/subagent_enhancement_build_plan.md` §8 Step 7. Depth: **full (building)**.
> Triggers met 2026-06-13 (see checklist). Research: `docs/Research/knowledge-fusion-conflict-detection/`
> (PASS 0.83, 19 papers) + `docs/Research/argument-mining-claim-extraction/` (relation vocabulary).

## Goal
For subagents built from 2+ high-value sources, merge **principles** (not just profiles): cluster
aliases, detect cross-source conflicts, and record a principle graph — so the agent reasons from one
reconciled knowledge model instead of two side-by-side summaries.

## Measured gap (the first real Tier-2 package)
`software-design-simplicity-advisor` (Code Simplicity + A Philosophy of Software Design): 96 claims
(71/25 by book), **0 cross-source relations, only 3/23 principles fuse both books** → concatenation,
not synthesis. This is the test case.

## Architecture (research-grounded) — three stages, recall-then-filter
1. **ALIGN / DEDUP (Phase A).** Cluster co-expressed principles across sources.
   *Recall-then-filter:* a cheap deterministic recall pass proposes candidates, an LLM precision pass
   confirms — the recall stage must be recall-tuned because the LLM filter can only remove, never
   recover a missed equivalence. Our principle sets are small (~tens), so the LLM does semantic recall
   over the full set; the lexical seeder is a prior, not the sole recall stage. Multi-key blocking
   beats any single key.
2. **DETECT CONTRADICTION (Phase B).** Triage each candidate conflict: *retrieval-verifiable* →
   resolve deterministically against a canonical source; *retrieval-resistant* → LLM adjudication
   (and do not over-trust the LLM on subtle long-context conflicts — keep it to clear disagreements).
3. **RECONCILE (Phase C/graph).** **Multi-truth**: do NOT force one winner. Accuracy-weight +
   copy-discount (N near-duplicate books must not outvote one independent authority), but a topic may
   keep several co-valid principles. A `conflicts` edge carries a `resolution` that SCOPES each side
   (context-dependent applicability), never deletes one. Output a **principle graph** (relations, not
   just nodes: alias / refines / specializes / supports / conflicts).

### Deterministic vs LLM split
- **Deterministic:** normalize, multi-key blocking/retrieval, clustering, accuracy-weighted voting,
  copy-graph estimation, lexical features, and ALL structural validation (schema, referential,
  acyclic hierarchy).
- **LLM:** semantic-equivalence judgement at the precision seam, canonical-statement wording,
  retrieval-resistant conflict adjudication + scoped resolution prose.

## Built (deterministic scaffolding — done)
- `schemas/principle-clusters-v1.schema.json` + `seed_principle_clusters.py` (recall seeder) +
  `validate_principle_clusters.py` (Phase A).
- `schemas/principle-graph-v1.schema.json` + `validate_principle_graph.py` (Phase C).
- Both wired into `validate_generated_package` (validate-if-present, min_tier 99).

## To build (LLM steps, now unblocked)
- Phase A/C LLM-confirm: seed → `principle-clusters.json` + `principle-graph.json` (in progress on
  the test package).
- Phase B conflict triage + `conflict-log.md`.
- Phase D: adapter dedup (surface canonical principles; flag unresolved conflicts) + promote the
  cluster/graph gate entries from min_tier 99 → required at Tier-2-multi-source.

## Open caveats (carry forward)
Both HIGH academic gaps are **environment-limited** (arXiv index recency-locked to ~2026, see
[[arxiv-index-recency-locked]]): **G1** reconciling *normative* principles ("prefer X") has no
in-corpus method (fusion assumes a factual truth) — handled here by the multi-truth/scoped-conflict
stance; **G3** cross-document contradiction detection rests on thin in-corpus evidence. Before
relying on B in production, do a manual lit pull (Semantic Scholar / ACL: DocNLI, cross-document NLI,
truth discovery for subjective claims, AGM belief merging).

## Trigger checklist (met)
- [x] ≥1 real Tier-2 (multi-source) package exists — `software-design-simplicity-advisor`.
- [x] `principles.yaml` stable + many single-source packages using it.
- [x] Steps 1 + 3 gates enforced (safety + faithfulness).
- [x] Knowledge-fusion research spike done (PASS 0.83; HIGH gaps environment-limited, documented).
