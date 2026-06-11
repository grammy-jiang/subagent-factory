# Step 10 — Source Structure Mapping (Tier-1 preprocessor)

> Master: extends `docs/subagent_enhancement_build_plan.md` (post-roadmap; realises the deferred
> Phase 2A/2B "Source Structure Mapping + Candidate Unit Extraction"). Depth: **medium** — design
> is settled; promote to **full** after research rounds 2–3 close gaps G1 (segmentation) and G3
> (claim-recall metric).
> Research: `docs/Research/long-document-structure-mapping/long-document-structure-mapping-research-report.md`
> (18 papers, verdict HAS_GAPS — "sufficient to design the preprocessor end-to-end").

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
- **coverage gate** (research Rec 6, dual harness adapted): candidate units cover ≥ a threshold of
  the source's claimable sections (per-section, not whole-book — research E3: LongSumEval ceilings
  on full books). Flag low coverage for re-mapping. (Until G3 closes, recall uses a
  summarization-QA proxy, not a true claim-recall metric — *logged limitation*.)

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

## Open gaps (why medium, not full)
| Gap | Sev | Plan |
|-----|-----|------|
| **G1** — no standalone topic/linear segmenter (TextTiling/C99/neural) in corpus; boundaries gate unit recall | HIGH | **Research round 2** (seg methods). Until then: summarization-embedded segmentation primitives. |
| **G3** — no claim/principle-level **recall** metric (only summ-QA/keyphrase proxies) | HIGH | **Research round 3** (claim/keypoint coverage eval). Until then: QA-coverage proxy in the coverage gate. |
| G2/G4/G5 | MED/LOW | opportunistic later rounds, else accept scoped |
| E1–E3 (code/schema/validator-scaling) | MED | resolved inline: minimal stage impls validated on the 131k-word concurrency book; node schema above; per-section QA + stratified judging |

## Exit criteria (when promoted to full + built)
1. `validate_source_map` passes a good map; fails tree/anchor/coverage violations.
2. Structure-map produced for a real Tier-1 book; claim-extraction consumes its units (claims carry `unit_id`).
3. Coverage gate fires on a low-coverage map.
4. A/B on one book: structure-mapped extraction vs flat — claims/principles recall + cost compared.
5. All Tier-0 packages unaffected (Tier-1+ only).

## Risks
- Segmentation quality is the recall ceiling and rests on embedded primitives until G1 closes (research-flagged).
- Tree-build on raw expository books is thinly validated (G2) — alignment fallback + fixed-window safety net.
- Cost: an extra LLM preprocessing pass per Tier-1 source — offset by the "halve compute" finding (read fewer, higher-salience nodes) + tiering.
