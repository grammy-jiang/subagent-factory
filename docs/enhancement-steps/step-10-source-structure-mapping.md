# Step 10 — Source Structure Mapping (Tier-1 preprocessor)

> Master: extends `docs/subagent_enhancement_build_plan.md` (post-roadmap; realises the deferred
> Phase 2A/2B "Source Structure Mapping + Candidate Unit Extraction"). Depth: **full** — the
> research completed (3 rounds, 37 papers) and **closed both HIGH gaps**: G1 (segmentation method)
> and G3 (claim-recall coverage metric). Only G2/G4 (MEDIUM) + G5 (LOW) remain — acceptable.
> Research: `docs/Research/long-document-structure-mapping/` (report + SUMMARY.md).
>
> **Deterministic half already built** (commit 68e0ae1): `schemas/source-map-v1.schema.json` +
> `tools/subagent_factory/validate_source_map.py` (schema + tree integrity + anchor referential) +
> present-gated gate block + 7 tests. What remains to implement: the LLM mapper (skill+agent), the
> Stage-2 segmenter choice, and the claim-recall coverage gate (now specified below).

## Goal

Read a long book **structure-first** before claim extraction: build a `part → chapter → section
→ passage` hierarchy and segment it into **provenance-anchored atomic candidate units**, so Tier-1
claim/principle extraction operates on structured, salience-ranked units instead of **flat-reading
the whole text**. The research's strongest, most consistent finding: *flat fixed-window chunking is
the wrong baseline* — explicit hierarchy + content-based selection improves extraction quality and
(in one case) halves compute. This is the highest-leverage unbuilt quality lever for the long-book
packages that dominate the corpus (e.g. the 131k-word concurrency book, the microservice book).

## Where it slots in

`author-subagent` **Step 6.5**, **before** claim extraction (6.5a): `classify_tier` → if Tier 1+,
run structure-mapping → claim-extraction consumes the map's candidate units (not flat text). Today
6.5a reads the source flat; this inserts the missing preprocessor the build plan reserved (§6.1
"(later) source-structure-mapping skill").

## The 7-stage reference pipeline (research consensus)

`parse → build hierarchy tree → segment topically → enumerate provenance-anchored candidate units
→ rank salience with GLOBAL context → read nodes long-context → validate precision AND recall.`

## New files (medium sketch)

| Path | Kind | Responsibility |
|------|------|----------------|
| `.claude/skills/source-structure-mapping/SKILL.md` | skill (LLM) | Run stages 1–6: tree + segments + candidate units + salience |
| `.claude/agents/source-structure-mapper.md` | agent (LLM) | Per-source mapping; Write limited to `sources/maps/` |
| `subagents/<slug>/sources/maps/<source_id>.source-map.yaml` | artifact (Tier 1+) | The hierarchy + candidate units |
| `schemas/source-map-v1.schema.json` | schema | Node + unit shape |
| `tools/subagent_factory/validate_source_map.py` | tool (validator) | Structural + referential + coverage |

## `source-map-v1` node schema (research gap E2 — adopt HiStruct+ address + Papers-to-Posts provenance)

```yaml
schema_version: source-map-v1
source_id: <sid>
nodes:
  - node_id: n0042
    parent_id: n0007                 # resolves within file (tree)
    level: section                   # part | chapter | section | passage
    title: "Guarded Suspension"
    structural_address: "3.4.2"      # HiStruct+ positional address
    role_class: method               # background|method|result|definition|example|... (role tag)
    source_anchors: ["<sid>-h0042"]  # ∈ anchor index (span)
    salience: 0.81                   # globally-ranked (Stage 5)
candidate_units:
  - unit_id: u0113
    node_id: n0042                   # the section it came from
    statement: "Use a while-condition-wait loop to guard a suspended action."
    source_anchors: ["<sid>-p0231"]  # provenance-anchored, atomic (bullet ↔ span)
    salience: 0.79
```

## `validate_source_map.py` (structural + referential + coverage)
- schema valid; `level` enum; `parent_id` resolves within the file (no cycles; single-root forest).
- every `source_anchors` entry ∈ the package anchor index (real IDs — master §1.2).
- **coverage gate — claim-recall (G3 RESOLVED).** Build a reference claim/principle set per section
  via FActScore-style atomic-fact decomposition + a high-precision, ambiguity-aware extractor
  (Claimify) [2305.14251, 2502.10855]; `recall = fraction of reference claims matched by ≥1
  candidate unit`, matched with KPA key-point↔claim matching + an exhaustiveness metric
  [2005.01619, 2404.11793, 2501.03545]. **Aggregate hierarchically (per part→chapter→section), not
  one flat pool** — beats the LongSumEval ~60% whole-book ceiling [2306.03853, 2604.25130]. A
  check-worthiness filter [2212.08514] selects which source claims count as reference (vs trivia).
  Flag low per-section recall for re-segmentation/re-enumeration. (The reference-set build + match
  are LLM steps; the deterministic gate counts the matches + applies the threshold.)

## Reuse
- `classify_tier` (gate it Tier 1+), `inject_anchors` index (span anchors), `source_text` (read).
- Feeds **Step 2 claim-extraction**: claims reference `unit_id` + inherit `source_anchors` → free
  provenance for the ledger (research Rec 3 — candidate-unit granularity == what claim extraction consumes).

## LLM ↔ deterministic split
- **LLM** (skill/agent): parse/tree/segment/enumerate/salience/long-context read (stages 1–6).
- **Deterministic**: `validate_source_map` (schema, tree integrity, anchor referential, coverage),
  `classify_tier`, anchor index.

## Research inputs → concrete decisions (cited)
- 7-stage pipeline + "flat chunking is wrong baseline" — cross-paper convergence (High).
- Tree: two-tier parser + alignment fallback [2606.10921, 2105.08209]; node = address + role [2203.09629].
- Units: provenance-anchored + atomic [2406.10370] (High-leverage; == claim granularity).
- Salience: neighbour-context read + **global** ranking [2606.10716, 2305.14806, 1905.13164] — *highest-leverage for recall* (High).
- Roll-up: hierarchical merge > incremental [2310.00785] (High).
- Validate: BooookScore precision + LongSumEval recall, per-section [2310.00785, 2604.25130] (High).
- Fallback: fixed-window only when parsing fails [2505.06862] (High).

## Stage-2 segmenter (G1 RESOLVED — research round 2)
The topic/linear segmentation that bounds candidate units (pipeline stage 3) — three tiers by
available training data; evaluate all boundaries with **Pk + WindowDiff** [2411.16613]:
- **Target (best):** supervised long-context coherence segmenter — Longformer + enhanced
  coherence, SOTA on WIKI-727K and ~8% Pk degradation out-of-domain (the robustness needed for
  arbitrary technical books) [2310.11772].
- **v1 default (cheap, ship first):** cross-segment BERT — a binary boundary classifier over the
  local left/right token context of each candidate break; trivial to implement, composes with the
  structural tree [2004.14535] (supervised framing + WIKI-727K benchmark [1803.09337]).
- **Zero-training fallback:** unsupervised embedding-adjacency segmentation (new block on
  adjacent-sentence embedding dissimilarity) when no in-domain data [2106.12978, 2106.06719].

## Remaining gaps (none HIGH — acceptable)
| Gap | Sev | Status |
|-----|-----|--------|
| ~~G1 segmentation~~ | ~~HIGH~~ | **CLOSED** (round 2) — see Stage-2 above |
| ~~G3 claim-recall metric~~ | ~~HIGH~~ | **CLOSED** (round 3) — see coverage gate above |
| G2 — TOC/heading extraction on *expository* 200+pg books (only narrative-validated) | MED | accept scoped; alignment + fixed-window fallback |
| G4 — expository-book discourse structure under-represented | MED | accept scoped |
| G5 — cross-reference / prerequisite-graph across a book | LOW | future |
| E1–E3 (code/schema/validator-scaling) | MED (eng) | resolved inline: minimal stage impls validated on the 131k-word concurrency book; node schema built; per-section aggregation |

## Exit criteria (when promoted to full + built)
1. `validate_source_map` passes a good map; fails tree/anchor/coverage violations.
2. Structure-map produced for a real Tier-1 book; claim-extraction consumes its units (claims carry `unit_id`).
3. Coverage gate fires on a low-coverage map.
4. A/B on one book: structure-mapped extraction vs flat — claims/principles recall + cost compared.
5. All Tier-0 packages unaffected (Tier-1+ only).

## Risks
- Segmentation quality is the recall ceiling; the Stage-2 segmenter is now specified (G1 closed —
  cross-segment BERT v1 → Longformer-coherence target), so this is an implementation choice, not an unknown.
- Tree-build on raw expository books is thinly validated (G2) — alignment fallback + fixed-window safety net.
- Cost: an extra LLM preprocessing pass per Tier-1 source — offset by the "halve compute" finding (read fewer, higher-salience nodes) + tiering.
