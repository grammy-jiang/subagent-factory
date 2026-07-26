# Provenance Ledger — requirements-use-case-advisor

This package advises and reviews requirements capture via use cases and user
stories. Its distilled layer (claims, principles, evidence, anchors) was built by
the per-book map → reduce pipeline; the authored layer (profile, skills,
references, tests, faithfulness, adapter) was derived from those principles.

## Sources

| source_id | title | author | year | rights |
|-----------|-------|--------|------|--------|
| `writing-effective-us-be2d4265` | Writing Effective Use Cases | Alistair Cockburn | 2001 | distillation-only |
| `user-stories-applied-e226b8db` | User Stories Applied: For Agile Software Development | Mike Cohn | 2004 | distillation-only |
| `use-case-2-0-jacobso-d3719142` | Use-Case 2.0: The Guide to Succeeding with Use Cases | Ivar Jacobson, Ian Spence, Kurt Bittner | 2011 | distillation-only |

`sha256` for each source is taken over the converted Markdown (the basis of the
`source_id` and the chunk anchors), recorded in `source-pack.manifest.yaml` and in
each `sources/metadata/<source_id>.metadata.json`. The same digests appear in
`profile.yaml sources[]`.

## Distilled layer (map → reduce, not edited here)

- `analysis/claims.jsonl` — globally-renumbered atomic claims (`C#####`).
- `principles/principles.yaml` — 90 principles (`P001`–`P090`); each
  `derived_from_claims` resolves into `claims.jsonl`.
- `evidence/evidence-records.yaml` — one record per claim backing a kept
  principle; `source_ids` resolve to the manifest, `source_anchors` to the
  chunk-anchor index.
- `sources/anchors/<source_id>.anchors.jsonl` — chunk (paragraph) anchors,
  id shape `<sha12>-cNNNN`.

## Field → principle traceability (profile)

Every operative profile field cites the principle IDs that ground it; the
faithfulness report (`reports/faithfulness-report.yaml`) grades each rule against
its evidence on the EXACT_SUPPORT → CONTRADICTED ladder. Representative mapping:

- `role`, `quality_bar`, `when_to_use` → P001, P002, P017, P018, P027, P046, P058,
  P059, P087 (scope/level, readability, ceremony, story quality).
- `forbidden_behaviours` → P010 (UI out of requirements), P052 (no IEEE-830
  shall-lists as primary), P059/P088 (do not invent requirements), P041/P049
  (do not force every requirement into a story).
- `outputs.modes` → P002, P017, P026, P027, P046, P087 (review/validate),
  P001/P023/P051 (advise), P005/P003/P059 (draft).
- `knowledge_partition.skills` / `references` → the principle clusters listed in
  each authored skill/reference frontmatter `provenance.principles`.

No profile field value is an orphan: each maps to ≥1 principle, which maps to
≥1 claim, which carries source anchors.

## Version history

### 0.1.1 — 2026-07-25

- Added `router_description` to `profile.yaml`. The adapter frontmatter `description` is the string the runtime routes on; without this field the exporter composed it from the role plus only the first two `when_to_use` triggers and the first `when_not_to_use` exclusion, dropping the remaining domains from the routing signal. The authored description states the full remit and the advice-only boundary; adapter re-exported. No principle, rule, skill, or source changed — no prior profile decision is superseded.

### 0.1.0 — 2026-06-28
Initial authored layer over the existing map→reduce distilled spine. Authored
`profile.yaml`, six skills, four references, `golden-tests.yaml`,
`principle-behaviour-tests.yaml` (90 tests), `reports/faithfulness-report.yaml`,
and the reconstructed deterministic `source-pack.manifest.yaml` +
`sources/metadata/*`. Package promoted to `status: ready`. No prior profile
decisions are superseded (first version).
