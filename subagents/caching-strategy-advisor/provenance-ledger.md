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
- `evidence/evidence-records.yaml` — 119 records, one per claim backing a kept principle;
  `source_ids` resolve to the manifest, `source_anchors` to the chunk-anchor index.
- `principles/principles.yaml` — 38 principles (`P001–P038`; 22 high-confidence, 16 medium),
  each `derived_from_claims` resolving into `claims.jsonl`.
- `sources/anchors/caching-at-scale-wit-11ebbc81.anchors.jsonl` — chunk (paragraph) anchors,
  shape `<sha12>-cNNNN` (e.g. `11ebbc818b96-c0000`).

## Field → principle traceability

Every profile rule cites the principle IDs it is grounded in (`quality_bar`,
`forbidden_behaviours`, `modes`, and `knowledge_partition.always_on` carry `P###` references),
and each principle resolves through `derived_from_claims` → `claims.jsonl` → `source_anchors`.
The faithfulness report (`reports/faithfulness-report.yaml`) grades each gradable profile rule
against the evidence and records the supporting chunk anchors. No profile field is an orphan.
The 38-principle spine refines the headline rules into finer sub-rules; the profile cites the
headline IDs and the adapter's must-hold invariant layer enforces every high-confidence,
profile-rule principle:

- Cache viability, value-preconditions, and break-even — P001, P012, P010, P035.
- Caching as a deliberate tradeoff and its three risks — P023; standard read-path — P025.
- Side-effect handling for cached operations — P013.
- Consistency as a first-class concern and the write-side mechanism — P002, P014, P015, P016;
  write-behind bounds — P017; TTL expiry — P018; cross-node eventual consistency — P028.
- Eviction policy selection, up-front planning, and thrashing remedy — P003, P024, P033, P036.
- Pattern and usage by data volatility — P009; Redis value data types — P005.
- Persistence (AOF/RDB) and the Redis-on-Flash caveat — P006, P022, P026, P032.
- Scaling by limit type: vertical, read replicas, sharding — P004, P008, P027, P038.
- Multi-region and the open-source-vs-Enterprise boundary; Active-Active conflict handling —
  P007, P019.

The side-effect caution carried in `knowledge_partition.always_on` and `forbidden_behaviours` is
now a promoted principle (P013); it remains recorded here so the rule is not an orphan.

## Version history

- **0.6.0** — Re-authored the LLM layer over a deeper map→reduce spine: the distilled spine was
  rebuilt from *Caching at Scale With Redis* to 123 claims and **38 principles** (`P001–P038`;
  22 high-confidence, 16 medium) with 119 evidence records, superseding the earlier 10-principle
  (`P001–P010`) spine. Regenerated the behaviour-test suite (golden coverage for every
  high-confidence principle), the per-principle behaviour tests (one citing test per
  high-confidence principle), the golden scenario tests (re-aligned to the new principle IDs),
  this provenance ledger, and the `CHANGELOG`; re-exported the adapter so its must-hold invariant
  layer covers all 22 high-confidence profile-rule principles. Profile rules, skills, references,
  and the faithfulness report were verified consistent with the new spine; grounding unchanged.
- **0.5.x** — Earlier map→reduce baseline over the same source with a 10-principle (`P001–P010`)
  spine. Its per-version bookkeeping was not preserved across the rebuild that produced the
  current 38-principle spine.
