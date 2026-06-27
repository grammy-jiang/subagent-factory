---
name: diagnosing-slow-queries-with-explain
kind: skill
status: ready
provenance:
  principles:
  - P012
  - P013
  - P046
  - P007
  claims:
  - C00313
  - C00320
  - C00314
  - C00329
  - C01429
  - C01430
  - C00383
  - C00384
  evidence:
  - E00101
  - E00103
  - E00102
  - E00104
  - E00362
  - E00363
  - E00120
  - E00121
  source_anchors:
  - b1c9b849675c-c0000
  - b1c9b849675c-c0001
  - 9269d920fbf8-c0000
  - b1c9b849675c-c0002
  authored_from_digest: 428ddfd7958ab7aa747847f7d9bbc662949c5c4d931ecf720977109ea2db8c55
---

# Diagnosing slow queries with EXPLAIN

## Purpose

Find the cause of a slow query by measurement — read its execution plan and locate the most expensive queries — rather than by guessing.

## When to use

When a query is slow and you need to find the cause and the right change.

## Procedure

1. Treat missing or wrong indexing as the first suspect for bad PostgreSQL performance; verify the expected indexes exist before tuning memory or hardware, and watch for over-indexing that slows writes. (P012)
2. Drive tuning with EXPLAIN: use EXPLAIN (ANALYZE[, BUFFERS, VERBOSE]), wrap data-changing EXPLAIN ANALYZE in BEGIN/ROLLBACK, compare costs only on the same server, and read a large estimate-vs-actual row gap as a sign of stale statistics. (P013)
3. When reading an EXPLAIN plan, run it with ANALYZE and BUFFERS and focus on the most expensive node; a Sequential Scan with a high 'Rows Removed by Filter' and large buffer reads signals a missing index. (P046)
4. Use pg_stat_statements to find the most expensive queries, ordering by total cumulative time, and reset its statistics when you need a clean measurement window. (P007)

## Grounding

Distilled (no verbatim) from this package's principles (P012, P013, P046, P007) and their anchored claims/evidence. Verify version-specific PostgreSQL or SQLite syntax and behaviour against current official documentation.
