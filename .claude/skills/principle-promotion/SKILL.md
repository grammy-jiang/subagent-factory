---
name: principle-promotion
description: "Promote high-value, evidence-backed claims into operational principles (principles-v1) that drive subagent behaviour, mapping each to profile rules / skills / tests. Tier 1+."
---

## Purpose

Decide which claims become **behaviour**. A principle is stronger than a claim: a reusable
rule that drives the subagent. Keeping claims (source knowledge) separate from principles
(operational rules) prevents profile bloat and overfitting. Output `principles/principles.yaml`,
validated by `validate_principles.py`.

## Input

- `analysis/claims.jsonl` + `analysis/claim-importance-scores.yaml` (Step 2) — candidates.
- `evidence/evidence-records.yaml` (Step 3) — a claim may be promoted only if it has ≥1 record.
- `profile.yaml` `knowledge_partition.{skills,references}` and `tests/` — `operational_mapping` targets.

## Promotion criteria

Promote a claim only when **all** hold:
- high actionability + reusability + clear operational fit (mirror the keep/review/discard rule);
- ≥1 evidence record exists for it;
- its conditions/exceptions are known, or explicitly marked unknown.

Not every claim is promoted. Prefer fewer, load-bearing principles.

## Procedure

For each promoted principle write a `principles-v1` entry:
- `principle_id`, `statement` (the operational rule, not the raw claim),
- `derived_from_claims` (≥1, real claim IDs),
- `confidence` (high/medium/low),
- `applies_when` / `does_not_apply_when` (from the claims' conditions/exceptions),
- `operational_mapping`: `profile_rule` (bool), `skill` (∈ knowledge_partition.skills or null),
  `reference` (∈ knowledge_partition.references or null), `test_cases` (⊆ test IDs in `tests/`).

## Output

`principles/principles.yaml` (schema `principles-v1`). Must pass
`python -m tools.subagent_factory.validate_principles` — every principle traces to claims that
each have evidence, and every `operational_mapping` target resolves.

## Caveats

- Single-source promotion only. **Cross-source** principle merge / alias clustering / conflict
  graph is **Step 7** (deferred).
- The validator enforces *traceability*, not *quality*; apply the promotion criteria yourself.
