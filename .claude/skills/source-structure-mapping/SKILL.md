---
name: source-structure-mapping
description: "Read a long source structure-first (Tier 1+): build a part->chapter->section->passage hierarchy + provenance-anchored atomic candidate knowledge units into sources/maps/<id>.source-map.yaml, BEFORE claim extraction — so extraction reads structure-aware instead of flat-chunking. Step 10 (Phase 2A/2B)."
---

## Purpose

Flat fixed-window chunking is the wrong baseline for distilling a 200+ page book (research
consensus). Read it **structure-first**: recover its `part → chapter → section → passage`
hierarchy and segment it into **provenance-anchored atomic candidate knowledge units**, ranked by
global salience. Claim extraction (Step 2) then consumes these units instead of flat-reading the
whole text — higher recall + precision, lower cost (read fewer, higher-salience nodes). Output
`sources/maps/<id>.source-map.yaml`, validated by `validate_source_map.py`.

## When to use

Tier 1+ packages, in author-subagent Step 6.5, **before** claim extraction (one map per source).

## Input

- `sources/markdown/<id>.md` — the converted source (load via `source_text`).
- `sources/anchors/<id>.anchors.jsonl` — real `source_anchor_v1` IDs for `source_anchors`.

## Procedure (7-stage reference pipeline — research-grounded)

1. **Parse + build the hierarchy tree.** From the markdown's heading structure, build a forest of
   nodes `part → chapter → section → passage`. Stamp each node: `node_id`, `parent_id` (null at a
   root), `level`, `title`, `structural_address` (e.g. `3.4.2`), `role_class`
   (background/method/result/definition/example/…), `source_anchors` (real anchor IDs covering the
   node's span). If headings are missing/garbled, fall back to fixed-window blocks **only then**.
2. **Segment topically within sections (G1 method).** Within a section, place a topic boundary
   where local left/right coherence drops (cross-segment reasoning over the surrounding sentences
   — the research's cross-segment / coherence approach, done in-LLM, consistent with the factory's
   LLM-not-encoder choice). Each resulting block becomes one or more candidate units.
3. **Enumerate provenance-anchored ATOMIC candidate units.** One operational statement per unit
   (`statement`), each tied to `source_anchors` (bullet ↔ source span). Atomic == exactly the
   granularity claim extraction consumes — so claims later reference `unit_id` and inherit its
   anchors (free provenance).
4. **Rank salience GLOBALLY.** Score each node/unit `salience` (0–1) using whole-document context,
   not per-chunk — this is the highest-leverage move for downstream recall. Read nodes with
   neighbour context.
5. **Coverage self-check (G3 method).** Per section, decompose it into a reference set of
   **check-worthy** atomic claims (FActScore/Claimify style — high precision, ambiguity-aware);
   compute `recall = fraction of reference claims matched by ≥1 candidate unit` (key-point↔claim
   matching). **Aggregate per-section**, not one flat pool (beats the whole-book ceiling). If a
   section's recall is low, **re-segment / re-enumerate that section** before writing.
6. **Roll up hierarchically** (not incrementally) when summarising units to chapter/part level.
7. **Write** `sources/maps/<id>.source-map.yaml` (`source-map-v1`).

## Output

`sources/maps/<id>.source-map.yaml` — must pass
`python -m tools.subagent_factory.validate_source_map`. Then claim-extraction (Step 6.5a) reads
`candidate_units` instead of the flat source.

## Rules

- **Structure-aware, never fixed-window** unless parsing genuinely fails (research: flat chunking
  is the wrong baseline).
- Every node/unit `source_anchors` must be **real anchor IDs** from the index (validator enforces).
- Units are **atomic + provenance-anchored**; distillation-only sources ⇒ paraphrase, no verbatim.
- Global (not per-chunk) salience; hierarchical (not incremental) roll-up.

## Caveats (validate ourselves)

- Segmentation (stage 2) and coverage (stage 5) are **LLM-judgment** here — the research methods
  (cross-segment-BERT / Longformer-coherence for G1; FActScore/Claimify + KPA match for G3) are
  adapted in-LLM, with no ML-model dependency. `validate_source_map` enforces *structure +
  referential integrity*; the claim-recall coverage gate is **self-applied** during stage 5 (the
  full deterministic FActScore harness is a future refinement, not this step).
- Tree-build on raw expository books is thinly validated upstream (research G2) — the fixed-window
  fallback is the safety net.
