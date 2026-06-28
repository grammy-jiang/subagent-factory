# Provenance Ledger — caching-strategy-advisor

This package was built by the per-book map→reduce authoring pipeline. The distilled spine
(claims, evidence, principles, chunk anchors) was assembled deterministically and is the
authority for every profile field; the LLM-authored layer (profile, faithfulness, skills,
references, tests, adapter) was derived from that spine and traces back to it.

## Sources

| source_id | title | author | rights | sha256 (prefix) |
|-----------|-------|--------|--------|-----------------|
| `caching-at-scale-wit-11ebbc81` | Caching at Scale With Redis | Lee Atchison (2021) | distillation-only | `11ebbc818b96…` |

The source is **distillation-only**: no verbatim quotation appears in any generated artifact;
every field is paraphrased and restructured. Official Redis documentation (redis.io/docs) and
cloud provider docs are the precedence authority for version-specific configuration, module
availability, and pricing; the source book governs architectural reasoning, trade-off
principles, and the cache-performance formula.

## Distilled spine (deterministic, not hand-edited)

- `analysis/claims.jsonl` — 123 atomic claims (`C#####`), globally renumbered by the build.
- `evidence/evidence-records.yaml` — one record per claim backing a kept principle; `source_ids`
  resolve to the manifest, `source_anchors` to the chunk-anchor index.
- `principles/principles.yaml` — 10 principles (`P001–P010`; 6 high-confidence, 4 medium), each
  `derived_from_claims` resolving into `claims.jsonl`.
- `sources/anchors/caching-at-scale-wit-11ebbc81.anchors.jsonl` — chunk (paragraph) anchors,
  shape `<sha12>-cNNNN` (e.g. `11ebbc818b96-c0000`).

## Field → source traceability

Every profile rule cites the principle IDs it is grounded in (`quality_bar`,
`forbidden_behaviours`, `modes`, and `knowledge_partition.always_on` carry `P###` references),
and each principle resolves through `derived_from_claims` → `claims.jsonl` → `source_anchors`.
The faithfulness report (`reports/faithfulness-report.yaml`) grades each gradable profile rule
against the evidence and records the supporting chunk anchors. No profile field is an orphan:

- Cache viability / break-even and metric discipline — P001, P010.
- Caching pattern and consistency by data volatility — P002, P009.
- Eviction policy selection and thrashing remedy — P003.
- Redis value data types — P005; persistence (AOF/RDB) — P006.
- Scaling by limit type (vertical, replicas, sharding) — P004, P008.
- Multi-region / Active-Active and the open-source-vs-Enterprise boundary — P007.

The side-effect caution carried in `knowledge_partition.always_on` and `forbidden_behaviours` is
source-grounded (book) but not promoted to a numbered principle; it is recorded here so the rule
is not an orphan.

## Version history

- **0.5.2** — Restored the package bookkeeping layer: re-created `provenance-ledger.md` and
  `CHANGELOG.md` (both lost when a fresh map→reduce rebuild overwrote `subagents/<slug>/`). No
  change to the distilled spine, principles, profile rules, skills, references, or tests; adapter
  re-exported to carry the new version. Faithfulness and grounding unchanged.
- **0.5.1** — Map→reduce rebuilt baseline over *Caching at Scale With Redis*: distilled spine
  (123 claims, 10 principles `P001–P010`), profile with `advise`/`compare`/`validate` modes,
  faithfulness report, five skills, three references, behaviour and golden tests, and the Claude
  Code adapter — all derived from the spine. Earlier 0.x line predates this rebuild; its
  per-version detail was not preserved across the overwrite.
