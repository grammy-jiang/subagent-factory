# Changelog — postgresql-sqlite-advisor

All notable changes to this generated subagent package are recorded here.

## [0.3.1] — 2026-06-22

### Changed

- Reconciled the authored layer to the rebuilt 150-principle distilled spine (`P001`–`P150`). The
  0.3.0 layer covered only the earlier 50 promoted principles; the map→reduce build since expanded
  `principles.yaml` to 150 (123 high-confidence), leaving 77 high-confidence principles without a
  behavioural test and the adapter invariant layer stale.
- Regenerated `tests/principle-behaviour-tests.yaml` from the current principles: one behaviour test
  per principle (`PB-001`–`PB-150`), each citing its `principle_id` and grounded in the principle's
  current statement + `applies_when`, so every high-confidence principle is covered.
- Re-exported the Claude Code adapter so its enforced invariant layer carries every current
  must-hold (high-confidence profile-rule) principle.

## [0.3.0] — 2026-06-22

### Changed

- Regenerated the LLM-authored layer (profile, faithfulness, skills/references, tests, adapter) over
  the map→reduce distilled spine so the package matches its 50 promoted principles
  (`P001`–`P050`). Supersedes the 0.2.0 authored layer, which described a narrower 16-principle
  schema-only advisor.

### Added

- Derived `profile.yaml` (Tier 2, multi-source, `multisource_synthesis: deferred`) grounded in the
  50 principles: a PostgreSQL/SQLite relational-design and database-fundamentals advisor with
  `advise` / `review` / `compare` / `validate` modes; every `quality_bar` and `forbidden_behaviours`
  rule cites its principle id(s), and `knowledge_partition.always_on` carries full coverage.
- `reports/faithfulness-report.yaml` — every profile rule checked against its principle's anchored
  claims; all findings `WITHIN_SCOPE` (no over-claim).
- Tests: `golden-tests.yaml` (6 positive, 2 negative routing, 1 missing-context)
  and `principle-behaviour-tests.yaml` (one behaviour test per principle, all 50 referenced).
- Authored eight skill bodies and three reference bodies, each grounded only in this package's
  principles / claims / evidence / source anchors (distillation-only, no verbatim).

### Unchanged (deterministic spine)

- `analysis/claims.jsonl` (2884 claims), `evidence/evidence-records.yaml`
  (402 records), `principles/principles.yaml` (50 principles), and the chunk
  anchors across eight `distillation-only` sources.
