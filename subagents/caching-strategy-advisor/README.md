# caching-strategy-advisor

**Version:** 0.3.0
**Tier:** 1
**Status:** ready

## Purpose

A senior caching architect advisor that guides engineering teams and technical
decision-makers on caching architecture and strategy for highly scaled enterprise
applications using Redis. Covers strategy selection, eviction and TTL policy, cache
consistency, cache scaling, cloud deployment options, and quantitative performance
analysis.

## Source

- "Caching at Scale With Redis" — Lee Atchison (2021)
- Rights: distillation-only (no verbatim quotation in any generated artefact)
- Conversion: Docling (92 heading anchors; re-converted 2026-06-12 from MarkItDown
  0-heading baseline)

## Supported Modes

| Mode | Use when |
|------|----------|
| `advise` | Need a recommendation on caching pattern, eviction policy, consistency strategy, or scaling approach |
| `compare` | Need trade-off analysis between two or more caching options |
| `validate` | Need to check a proposed or existing cache design against viability conditions and the break-even formula |

## Required Inputs

Before engaging, provide:

1. Data-access pattern (frequency, distribution shape, whether data changes after write)
2. Backing operation latency and, if a cache exists, current hit/miss rate
3. Whether the operation has side effects (and what they are)
4. Application consistency tolerance (max acceptable staleness)

## Out of Scope

- Operations with side effects that have not been fully audited
- Data with flat access distributions where cache overhead exceeds benefit
- Production-ready Redis configuration files or runnable scripts

## Package Layout

```
subagents/caching-strategy-advisor/
  profile.yaml                        canonical profile
  provenance-ledger.md                field-by-field distillation log
  CHANGELOG.md                        version history
  README.md                           this file
  interrogation-records.yaml          Q1-Q18 source interrogation
  principles/principles.yaml          Tier-1 principles P001-P010
  evidence/evidence-records.yaml      Tier-1 evidence records
  analysis/claims.jsonl               extracted claims
  analysis/claim-importance-scores.yaml  importance scoring
  sources/                            ingested source material
  tests/golden-tests.yaml             golden test suite
```

## Validation

```bash
python -m tools.subagent_factory.cli selfcheck caching-strategy-advisor
```
