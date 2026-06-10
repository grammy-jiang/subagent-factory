# Step 2 — Atomic Claim Extraction

> Master: `docs/subagent_enhancement_build_plan.md` §8 Step 2. Depth: **full**.
> Research: `docs/Research/argument-mining-claim-extraction/` (full report).

## Goal
Replace vague "candidate units" with **atomic, typed, traceable claims** — each bound to
source anchors and classified by an empirically-grounded taxonomy — as the unit that
importance-ranking, evidence, and principles operate on.

## New files
| Path | Kind | Responsibility |
|------|------|----------------|
| `.claude/skills/claim-extraction/SKILL.md` | skill (LLM) | Two-stage extraction → `claims.jsonl`. |
| `.claude/agents/claim-extractor.md` | agent (LLM) | Detection + decomposition + classification. |
| `subagents/<slug>/analysis/claims.jsonl` | artifact | One claim per line. |
| `subagents/<slug>/analysis/claim-importance-scores.yaml` | artifact | `score_extracted_units` output on claims. |
| `schemas/claims-v1.schema.json` | schema | Claim shape + enums. |
| `tools/subagent_factory/validate_claims.py` | tool (validator) | Structural + referential checks. |
| `tests/fixtures/claims/` | fixtures | Sample source → expected claims; coverage + referential failures. |

## `claims-v1` schema (all enums empirically grounded — see report Merged Taxonomy)
```yaml
schema_version: claims-v1
claim_id: C-0001                       # unique within package
source_id: <sid>                       # ∈ manifest
source_anchors: ["<sid>-p0042"]        # ∈ anchor index (real IDs, master §1.2)
support_granularity: section           # section | page | heading
statement: "Explicit module boundaries reduce hidden coupling."
component_class: claim                  # major_claim | claim | premise | non_argumentative  (Stab & Gurevych, 5+ corpora)
claim_type: value                      # fact | value | policy  [+ causal: optional, domain-validate]
premise_type: null                     # common_ground|testimony|hypothetical_instance|statistics|real_example|other (AAE-FG; premises only)
evidence_type: null                    # explanation|case|research|expert|other (AQE; on linked evidence)
stance: support                        # support | contest | no_relation (IAM 3-way, not binary)
az_zone: null                          # AIM|OWN_CONC|NOV_ADV|SUPPORT|GAP_WEAK|ANTISUPP|OWN_MTHD|RELWRK|BKG|CTR|OUTSIDER  (Teufel AZ; scientific docs ONLY)
condition: null                        # nullable string; surface-cue bootstrap
exception: null                        # nullable string; undercutting-attack pattern
certainty: asserted                    # asserted | hedged | speculative (BioScope cue model)
confidence_initial: medium             # high | medium | low
```

## Extraction architecture (report §Practical-Rec 5–8)
- **Stage 1 — detection (check-worthiness).** Report recommends a fine-tuned encoder
  (XLM-RoBERTa-Large, 5:1 class-weighted loss). **Adaptation:** v1 uses an **LLM check-worthiness
  pass** (no model dep, consistent with the factory's skill/agent design); the encoder is an
  optional cost optimization deferred to Tier-1-at-scale. *Deviation logged.*
- **Stage 2 — decomposition.** LLM + nested JSON schema, **delayed-structure** (reason first,
  then emit JSON) — report [2606.09410]: JSON costs zero for capable models, delayed-structure
  recovers weaker ones.
- **Separate passes, not joint 4-tuple.** Full (claim+evidence+stance+evidence_type) joint
  extraction scores only F1=21.39 [2305.19902] → single pass for claim+type+premise; a separate
  pass for evidence-linking (Step 3). 3-way stance, not binary [2203.12257].
- **condition/exception = surface-cue bootstrap** (report §Practical-Rec 8, Low confidence):
  `unless`, `except when`, `only if`, `provided that`, `assuming`, `subject to`, `absent`,
  `if and only if`, `in the absence of`. Undercutting attack = the `exception` pattern (Pollock).

## Reuse
- `source-interrogation` Q1–Q18 + `evidence_gaps:` — upstream context for what to extract.
- `score_extracted_units.py` — **unchanged**; feed claims (carry the 9 dims) → `claim-importance-scores.yaml` (master §4.5).
- `inject_anchors.py` index — `source_anchors` cross-check target.
- `source_text.py` (Step 0) — source access for the extractor.

## `validate_claims.py` (structural + referential)
- unique `claim_id`; `source_id`/`source_ids` ∈ manifest; every `source_anchors` entry ∈ anchor index.
- all enums valid; `premise_type` only when `component_class=premise`; `az_zone` only for scientific-doc tier.
- `condition`/`exception` nullable strings; `certainty` enum.
- **Coverage gate** (report §Practical-Rec 6 [2606.09376]): compute `extracted_claims / claimable_sentences`;
  **flag < 0.50** for re-extraction (recall is a capability ceiling — precision-only is a blind spot).
- **Deterministic type post-checks** (report §Practical-Rec 7 [2606.09500]): causal connective
  (`therefore/because/thus`) in a `fact` claim; conditional phrasing (`if/unless`) with empty `condition`;
  numeric claim with wrong `claim_type` → WARN.

## Gate wiring
Tier 1+ (present-gated). Tier 0 packages never carry `claims.jsonl` → unaffected.

## LLM ↔ deterministic split
- LLM: `claim-extraction` skill / `claim-extractor` agent (detection, decomposition, classification, condition/exception).
- Deterministic: `validate_claims.py` (schema, referential, coverage ratio, type post-checks), `score_extracted_units`.

## Fixtures
- A short source with known claims → expected `claims.jsonl` (component/type/stance correct).
- A low-density source → coverage < 0.50 fails.
- Bad `source_anchors`/`claim_id`/enum → referential failures.

## Exit criteria + verify
1. `validate_claims` passes a good `claims.jsonl`, fails referential/coverage violations.
2. `score_extracted_units` runs on claims → `claim-importance-scores.yaml`.
3. Deterministic type post-checks fire on the planted mismatches.
4. All 15 Tier-0 packages still pass `validate`.

## Caveats (research limits — validate ourselves)
- **`exception`/`condition` is heuristic** — GAP-4 open: **no NLP dataset or trained model** for
  undercutting/condition extraction exists (foundational αNLI `1908.05739` not fetched; arXiv
  recency bias). Treat as surface-cue best-effort, not validated.
- **`az_zone` via secondary source** (Lawrence & Reed survey, not primary Teufel) → schema-design-grade, not classifier-grade. Scientific docs only.
- **`causal` claim_type optional** — Fact/Value/Policy validated on essays; causal needs in-domain validation before production.
- **LLM hallucination in extraction is an open threat** (report [2506.16383], no standard mitigation) → caught downstream by the deterministic type checks + Step-1/3 faithfulness, not by extraction alone.
- **No book-length benchmark** (GAP-6) → the coverage gate is our only quality proxy at chapter scale.

## Risks
- Encoder-vs-LLM detection deviation: if LLM detection recall is poor on long sources, revisit the
  XLM-R Stage-1 (the report's recommendation). Coverage gate surfaces this.
