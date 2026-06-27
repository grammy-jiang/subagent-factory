---
name: choosing-isolation-and-transactions
kind: skill
status: ready
provenance:
  principles:
  - P005
  - P038
  claims:
  - C00298
  - C00299
  - C01270
  - C01271
  evidence:
  - E00093
  - E00094
  - E00320
  - E00321
  source_anchors:
  - b1c9b849675c-c0000
  - 7bf3da04ec81-c0006
  authored_from_digest: c3d5d78eead3901bae81f0e346a86ac6862aa53194d3c19938ed59f3c52d90dd
---

# Choosing isolation levels and transactions

## Purpose

Select the transaction isolation level by the anomalies that must be prevented, and reason about atomic commitment across partitions.

## When to use

When choosing an isolation level or designing multi-partition transactional behaviour.

## Procedure

1. Choose the isolation level by the anomalies you must prevent (dirty/nonrepeatable/phantom reads, lost update/dirty write/write skew), remembering snapshot isolation prevents lost updates but not write skew and that serializability requires coordination. (P005)
2. For multi-partition atomicity use atomic commitment (no commit unless all participants vote yes; it fails under Byzantine faults): 2PC is simple but blocks on coordinator failure (mitigate with durable decision logs and a backup coordinator), while 3PC is non-blocking yet splits under network partitions. (P038)

## Grounding

Distilled (no verbatim) from this package's principles (P005, P038) and their anchored claims/evidence. Verify version-specific PostgreSQL or SQLite syntax and behaviour against current official documentation.
