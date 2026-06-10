# Step 4 — Principle Promotion

> Master: `docs/subagent_enhancement_build_plan.md` §8 Step 4. Depth: **medium** (outline).
> **Promote to full when:** Step 3 merged + `claims-v1` and `evidence-records-v1` schemas frozen.

## Goal
Promote a selected subset of high-value, evidence-backed claims into **operational principles**
that drive subagent behaviour (profile rules, skills, tests) — keeping the line between *source
knowledge* (claims) and *operational rule* (principle) explicit.

## New files (sketch)
- `.claude/skills/principle-promotion/SKILL.md` — selection skill.
- `.claude/agents/principle-promoter.md` — agent (named to avoid colliding with `profile-deriver`).
- `subagents/<slug>/principles/principles.yaml` — artifact.
- `schemas/principles-v1.schema.json` — schema.
- `tools/subagent_factory/validate_principles.py` — referential validator.

## `principles-v1` (draft — finalize at promotion)
```yaml
principle_id: P-001
statement: "Prefer explicit interfaces at stable module boundaries."
derived_from_claims: [C-0001, C-0014]   # ∈ claims.jsonl
confidence: medium
applies_when: ["public API design", "cross-team dependency"]
does_not_apply_when: ["throwaway prototype"]
operational_mapping:
  profile_rule: true
  skill: api-boundary-review            # ∈ knowledge_partition.skills / stubs
  reference: modularity-checklist
  test_cases: [GT-003]                  # ∈ tests
```

## Reuse
- Existing keep/review/discard pattern (`score_extracted_units`) — promotion criteria mirror it.
- `knowledge_partition` (profile) — `operational_mapping` targets must resolve to real skills/refs.

## Dependencies
- **Step 2** (`claims.jsonl`) — `derived_from_claims` references.
- **Step 3** (`evidence-records.yaml`) — promotion requires ≥1 evidence record per source claim.

## Validator (referential, at full)
`derived_from_claims` ∈ claims; each has ≥1 evidence record; `operational_mapping.skill/reference`
∈ knowledge_partition or stubs; `test_cases` ∈ tests.

## Research input (light)
Argument-mining: high-value claims = candidates; AM relation types (support/attack) inform
principle relationships later (Step 7 graph). Promotion criteria (master §11 Enh-7): high
actionability + reusability + clear operational fit + evidence exists + conditions/exceptions known-or-marked.

## Open questions (resolve at promotion)
- Exact principle↔claim cardinality; how `operational_mapping` interacts with `cli stubs`.
- Whether principle promotion replaces or augments current direct profile derivation for Tier-1.

## Gate wiring
Tier 1+ (present-gated).
