# Provenance Ledger — pragmatic-programming-advisor

Every profile field, principle, and authored artifact in this package traces back to the
single source below through the deterministic claim → evidence → principle chain.

## Source

| source_id | title | rights_status | sha256 |
|-----------|-------|---------------|--------|
| `andrew-hunt-david-th-13ff3ba5` | The Pragmatic Programmer: From Journeyman to Master (Hunt & Thomas, 1999) | distillation-only | `13ff3ba5042aa1682f6c85bbba17fd0b6b531604ebf5a7e96d8e1bde931d6a1e` |

Rights: `distillation-only` — distillation and paraphrase allowed; no verbatim quotation in
generated artifacts (see `.claude/rules/rights-and-quotation-policy.md`). The quote scan gate
enforces this on every release.

## Lineage

```
sources/original/original.pdf
  → sources/markdown/andrew-hunt-david-th-13ff3ba5.md        (Docling conversion)
  → sources/anchors/andrew-hunt-david-th-13ff3ba5.anchors.jsonl  (chunk anchors 13ff3ba5042a-cNNNN)
  → analysis/claims.jsonl                                     (381 atomic claims C00001..C00381)
  → evidence/evidence-records.yaml                            (evidence chain)
  → principles/principles.yaml                                (78 promoted principles P001..P078)
  → profile.yaml + skills/ + references/ + tests/             (authored layer, re-grounded)
```

The distilled spine (claims, evidence, anchors, principles) was assembled by the per-book
map → reduce build. Every claim's `source_anchors` resolves into the chunk anchor index; every
principle's `derived_from_claims` resolves into `claims.jsonl`. Each profile rule, skill, and
reference cites principle (`P###`) and claim (`C#####`) ids that exist in this package.

## Principle coverage

- 78 principles total; 13 at `confidence: high`
  (P001, P003, P010, P015, P016, P020, P030, P031, P039, P040, P041, P059, P068).
- Every high-confidence principle is exercised by ≥1 behavioural test in
  `tests/principle-behaviour-tests.yaml` (principle → test coverage gate).

## Version history

Supersession rule: prior decisions stay visible; new versions are appended, not overwritten.

### 0.3.1 — 2026-07-25

- Added `router_description` to `profile.yaml`. The adapter frontmatter `description` is the string the runtime routes on; without this field the exporter composed it from the role plus only the first two `when_to_use` triggers and the first `when_not_to_use` exclusion, dropping the remaining domains from the routing signal. The authored description states the full remit and the advice-only boundary; adapter re-exported. No principle, rule, skill, or source changed — no prior profile decision is superseded.

### 0.3.0 — 2026-06-28

- Distilled layer rebuilt via per-book map → reduce: 381 globally-renumbered claims
  (`C#####`) and 78 promoted principles (`P001..P078`), replacing the original
  14-principle (`ppa-p001..ppa-p014`) hand-distilled layer.
- Authored layer re-grounded onto the new spine: `profile.yaml` rules, all 6 skills, and all
  5 references now cite real `P###`/`C#####` ids; behaviour and golden test suites regenerated;
  faithfulness report re-run against `evidence-records.yaml` + `claims.jsonl`.
- Fixed `sources[].source_id` from the legacy timestamp id
  (`andrew-hunt-david-th-20260611015103`) to the content-sha id (`andrew-hunt-david-th-13ff3ba5`)
  and corrected the recorded sha256 to match the manifest.

### 0.2.0 / 0.1.0 — 2026-06-11 (superseded)

- Original hand-distilled package: 14 promoted principles (`ppa-p001..ppa-p014`) authored from
  the same source. Superseded by the 0.3.0 map → reduce rebuild above; the `ppa-*` id scheme is
  no longer present in this package.
