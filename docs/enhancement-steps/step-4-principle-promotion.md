# Step 4 — Principle Promotion

> Master: `docs/subagent_enhancement_build_plan.md` §8 Step 4. Depth: **full**
> (promoted from medium — Step 3 merged, `claims-v1` + `evidence-records-v1` frozen).

## Goal
Promote a selected subset of high-value, evidence-backed claims into **operational
principles** that drive subagent behaviour — keeping the line between *source knowledge*
(claims) and *operational rule* (principle) explicit and traceable.

## New files
| Path | Kind | Responsibility |
|------|------|----------------|
| `.claude/skills/principle-promotion/SKILL.md` | skill (LLM) | Select promotable claims → `principles.yaml`. |
| `.claude/agents/principle-promoter.md` | agent (LLM) | Runs promotion (named to avoid colliding with `profile-deriver`). |
| `subagents/<slug>/principles/principles.yaml` | artifact | Promoted principles. |
| `schemas/principles-v1.schema.json` | schema | Principle shape + enums. |
| `tools/subagent_factory/validate_principles.py` | tool (validator) | Structural + referential. |
| `tests/subagent_factory/test_validate_principles.py` | fixtures | Validator tests. |

## `principles-v1` schema
```yaml
schema_version: principles-v1
principles:
  - principle_id: P-001
    statement: "Prefer explicit interfaces at stable module boundaries."
    derived_from_claims: [C-0001, C-0014]   # ≥1; ∈ analysis/claims.jsonl
    confidence: high | medium | low
    applies_when: ["public API design", "cross-team dependency"]
    does_not_apply_when: ["throwaway prototype"]
    operational_mapping:
      profile_rule: true
      skill: api-boundary-review            # null or ∈ profile.knowledge_partition.skills
      reference: modularity-checklist        # null or ∈ profile.knowledge_partition.references
      test_cases: [GT-003]                   # ⊆ test ids in tests/
```

## Reuse
- `analysis/claims.jsonl` (Step 2) — `derived_from_claims` target.
- `evidence/evidence-records.yaml` (Step 3) — the **promotable-coverage** check deferred from
  Step 3 lands here: every claim a principle derives from must have ≥1 evidence record.
- `profile.yaml` `knowledge_partition.{skills,references}` — `operational_mapping` targets.
- `tests/` — `test_cases` targets.
- keep/review/discard intuition from `score_extracted_units` (promotion criteria mirror it).

## `validate_principles.py` (structural + referential — the teeth)
- schema-valid; unique `principle_id`.
- `derived_from_claims` ⊆ claim IDs in `analysis/claims.jsonl` (when present); ≥1 each (schema).
- **promotable coverage:** every `derived_from_claims` entry has ≥1 record in
  `evidence/evidence-records.yaml` (when present).
- `operational_mapping.skill` (if non-null) ∈ `knowledge_partition.skills`;
  `operational_mapping.reference` (if non-null) ∈ `knowledge_partition.references`.
- `operational_mapping.test_cases` ⊆ test IDs found in `tests/*.yaml`.

## Gate wiring
`_TIER_ARTIFACTS.append(("principles/principles.yaml", 1, validate_principles))` — required at
Tier 1+, validated whenever present. Tier-0 packages unaffected.

## LLM ↔ deterministic split
- LLM: `principle-promotion` skill / `principle-promoter` agent (which claims become principles,
  the `statement`, `applies_when`/`does_not_apply_when`, `operational_mapping`).
- Deterministic: `validate_principles.py` (schema + referential + coverage).

## Promotion criteria (skill)
Promote a claim only when: high actionability + reusability + clear operational fit +
≥1 evidence record + conditions/exceptions known-or-explicitly-unknown. This prevents profile
bloat and overfitting (not every claim becomes behaviour).

## Fixtures
- valid principles → `[]`.
- `derived_from_claims` referencing a missing claim → error.
- a derived claim with no evidence record → coverage error.
- `operational_mapping.skill` not in `knowledge_partition` → error.
- `test_cases` referencing a missing test → error.
- duplicate `principle_id` → error.

## Exit criteria + verify
1. `validate_principles` passes good principles; fails each referential/coverage violation.
2. `make verify` green; **0/15 packages regressed** (Tier-0 unaffected; present-gated + Tier-1).

## Caveats
- Principle promotion is LLM selection; the validator enforces *traceability*, not *quality*.
- Cross-source principle merge / alias clustering / conflict graph is **Step 7** (deferred);
  Step 4 is single-source promotion.

## Risks
- Over-promotion (profile bloat) → the criteria + `score_extracted_units` gate it; the validator
  ensures every principle is claim+evidence-traceable.
