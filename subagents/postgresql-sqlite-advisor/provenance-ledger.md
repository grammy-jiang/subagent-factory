# Provenance Ledger — postgresql-sqlite-advisor

## Package summary

- **Slug:** `postgresql-sqlite-advisor`
- **Role:** Relational database schema-design and database-fundamentals advisor across PostgreSQL and SQLite.
- **Tier:** 2 (multi-source: 8 sources).
- **Status:** ready (skill/reference bodies authored).
- **Build:** distilled spine assembled by the chunk→book→corpus map→reduce build (`.build/` stamps);
  claims globally renumbered (`C#####`) with paragraph/chunk anchors. The LLM-authored layer
  (profile, faithfulness, skills/references, tests, adapter) was (re)generated to match this
  package's 50 promoted principles.
- **Rights:** every source is an authored, copyrighted book or course text → `distillation-only`.
  No verbatim quotation appears in any generated artifact; all grounding is distilled and anchored
  to source chunks. `quote_allowed: false` on every evidence record.

## Sources

| source_id | Title | Rights |
|-----------|-------|--------|
| comp-230-82a20f58 | Database Design (COMP-230 course text) | distillation-only |
| comp-312-b1c9b849 | PostgreSQL Administration (COMP-312 course text) | distillation-only |
| postgresql-up-and-ru-b86b08da | PostgreSQL: Up and Running | distillation-only |
| the-definitive-guide-9aa0ce19 | The Definitive Guide to SQLite | distillation-only |
| alex-petrov-database-7bf3da04 | Database Internals: A Deep Dive into How Distributed Data Systems Work | distillation-only |
| effective-indexing-i-163dcf34 | Effective Indexing in Postgres | distillation-only |
| pganalyze-best-pract-9269d920 | Best Practices for Optimizing Postgres Query Performance | distillation-only |
| sql-performance-expl-78ffa022 | SQL Performance Explained | distillation-only |

## Evidence chain

- **Claims:** `analysis/claims.jsonl` — 2884 atomic, typed, source-anchored claims (`claims-v1`).
- **Evidence:** `evidence/evidence-records.yaml` — 402 evidence records keyed by `claim_id` (`quote_allowed: false`).
- **Principles:** `principles/principles.yaml` — 50 promoted principles (`P001`–`P050`); each `derived_from_claims` resolves into `claims.jsonl`.
- **Anchors:** `sources/anchors/*.anchors.jsonl` — 49 chunk/paragraph anchors; every claim's `source_anchors` resolve.

## Profile derivation

`profile.yaml` is grounded in the 50 principles: a relational-database design and fundamentals
advisor with `advise` / `review` / `compare` / `validate` modes. Each `quality_bar` and
`forbidden_behaviours` rule cites the principle id(s) it rests on; `knowledge_partition.always_on`
carries the full principle coverage. `reports/faithfulness-report.yaml` checks each rule against its
principle's anchored claims — all findings `WITHIN_SCOPE` (no rule stronger than its evidence).

## Authored knowledge partition

- **Skills:** `designing-schemas-keys-and-normalization`, `enforcing-data-integrity-and-constraints`, `designing-and-selecting-indexes`, `diagnosing-slow-queries-with-explain`, `choosing-isolation-and-transactions`, `operating-postgresql-server`, `working-with-sqlite`, `database-storage-and-distributed-internals`.
- **References:** `index-type-selection`, `normalization-and-integrity-checklist`, `sqlite-type-affinity-and-rowid`.

Each authored body declares `status: ready` with a `provenance` block whose principle / claim /
evidence / anchor ids all resolve into the spine.

## Version history

- **0.3.0 (2026-06-22):** regenerated the LLM-authored layer over the map→reduce distilled
  spine — profile, faithfulness report, golden + principle-behaviour tests, eight skills, three
  references, and the exported Claude Code adapter. Supersedes the prior 0.2.0 authored layer
  (16-principle focus); the distilled spine (50 principles) is unchanged.

## Version History

- **0.3.2** (2026-07-25) — Added `router_description` to `profile.yaml`. The adapter frontmatter `description` is the string the runtime routes on; without this field the exporter composed it from the role plus only the first two `when_to_use` triggers and the first `when_not_to_use` exclusion, dropping the remaining domains from the routing signal. The authored description states the full remit and the advice-only boundary; adapter re-exported. No principle, rule, skill, or source changed — no prior profile decision is superseded.
