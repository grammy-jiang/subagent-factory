# Provenance Ledger — documentation-as-code-advisor

This package was built by the per-book map→reduce authoring pipeline. The distilled spine
(claims, evidence, principles, chunk anchors) was assembled deterministically and is the
authority for every profile field; the LLM-authored layer (profile, faithfulness, skills,
references, tests, adapter) was derived from that spine and traces back to it.

## Sources

| source_id | title | author | rights | sha256 (prefix) |
|-----------|-------|--------|--------|-----------------|
| `diataxis-7065cb6e` | Diátaxis — A Systematic Framework for Technical Documentation | Daniele Procida | distillation-only | `7065cb6e73a0…` |
| `google-tech-writing-3ae5f96e` | Google Technical Writing Courses (One & Two) | Google | distillation-only | `3ae5f96ea0cd…` |
| `docs-like-code-stori-9b3c3a53` | Docs Like Code — Case Studies and Stories | Anne Gentle | distillation-only | `9b3c3a535ed6…` |

All three sources are **distillation-only**: no verbatim quotation appears in any generated
artifact; every field is paraphrased and restructured.

## Distilled spine (deterministic, not hand-edited)

- `analysis/claims.jsonl` — 354 atomic claims (`C#####`), globally renumbered across the three
  books (diataxis 125, google 165, docs-like-code 64).
- `evidence/evidence-records.yaml` — one record per claim backing a kept principle; `source_ids`
  resolve to the manifest, `source_anchors` to the chunk-anchor index.
- `principles/principles.yaml` — 64 principles (`P001–P064`; 42 high-confidence, 22 medium),
  each `derived_from_claims` resolving into `claims.jsonl`.
- `sources/anchors/*.anchors.jsonl` — chunk (paragraph) anchors, shape `<sha12>-cNNNN`.

## Field → source traceability

Every profile rule cites the principle IDs it is grounded in (e.g. `quality_bar` and
`forbidden_behaviours` carry `P###` references), and each principle resolves through
`derived_from_claims` → `claims.jsonl` → `source_anchors`. The faithfulness report
(`reports/faithfulness-report.yaml`) grades each gradable profile rule against the evidence and
records the supporting chunk anchors. No profile field is an orphan: the four Diátaxis types and
the compass come from `diataxis-7065cb6e`; the clarity, audience, list/table, and sample-code
rules from `google-tech-writing-3ae5f96e`; the docs-as-code workflow and capacity-planning rules
from `docs-like-code-stori-9b3c3a53`.

## Version history

- **0.1.0** — Initial release. Distilled spine assembled by the map→reduce build over the three
  docs-as-code sources; profile, faithfulness report, four skills, one reference, behaviour and
  golden tests, and the Claude Code adapter derived from the 64 principles. Source layer
  (manifest + `sources/{original,markdown,metadata,reports}`) reconciled to the spine via the
  deterministic ingest; chunk anchors preserved from the build.

## Version History

- **0.1.1** (2026-07-25) — Added `router_description` to `profile.yaml`. The adapter frontmatter `description` is the string the runtime routes on; without this field the exporter composed it from the role plus only the first two `when_to_use` triggers and the first `when_not_to_use` exclusion, dropping the remaining domains from the routing signal. The authored description states the full remit and the advice-only boundary; adapter re-exported. No principle, rule, skill, or source changed — no prior profile decision is superseded.
