---
name: database-storage-and-distributed-internals
kind: skill
status: ready
provenance:
  principles:
  - P027
  - P028
  - P035
  - P036
  - P037
  - P038
  - P039
  claims:
  - C01016
  - C01017
  - C01042
  - C01043
  - C01063
  - C01064
  - C01092
  - C01093
  - C01256
  - C01257
  - C01270
  - C01271
  - C01296
  - C01297
  evidence:
  - E00269
  - E00270
  - E00279
  - E00280
  - E00284
  - E00285
  - E00294
  - E00295
  - E00312
  - E00313
  - E00320
  - E00321
  - E00328
  - E00329
  source_anchors:
  - 7bf3da04ec81-c0000
  - 7bf3da04ec81-c0001
  - 7bf3da04ec81-c0002
  - 7bf3da04ec81-c0005
  - 7bf3da04ec81-c0006
  authored_from_digest: c395153008283a749635b730b26f16075e00aae8919ab8547b7024d1c8cc2dd4
---

# Database storage and distributed internals

## Purpose

Reason from storage-engine and distributed-systems fundamentals — page layout, buffer cache, engine selection, replication consistency, and consensus — that underpin engine and topology choices.

## When to use

When choosing a storage engine, an on-disk layout, or a replication/consistency strategy, or reasoning about why one fits a workload.

## Procedure

1. Select a database/storage engine by simulating the real anticipated workload and measuring the metrics that matter, not by comparing components, popularity rank, or implementation language; treat the choice as hard to reverse. (P027)
2. Choose index and data-file organization by the read/write mix: index-organized/clustered tables and direct-offset references favour read-mostly access, while primary-key indirection is better for write-heavy workloads with multiple secondary indexes. (P028)
3. Use the slotted-page layout (cells on one side, sorted offset pointers on the other) to store variable-size records, allow binary search without relocating cells, and reclaim space via an availability list, defragmentation, and overflow pages. (P035)
4. Manage the page cache deliberately: pin hot upper-tree pages, choose a recency/frequency-aware replacement policy (a bigger cache alone can worsen evictions via Bélády's anomaly), prefetch range scans, and flush dirty pages before eviction. (P036)
5. Repair replica divergence with the anti-entropy mechanism that matches the need — read-repair and hinted handoff for scope, bitmap version vectors for recency, Merkle trees for completeness — and use gossip for reliable large-scale dissemination. (P037)
6. For multi-partition atomicity use atomic commitment (no commit unless all participants vote yes; it fails under Byzantine faults): 2PC is simple but blocks on coordinator failure (mitigate with durable decision logs and a backup coordinator), while 3PC is non-blocking yet splits under network partitions. (P038)
7. Use a consensus algorithm (Paxos, Multi-Paxos, Raft) for agreement under crash failures with majority quorums (2f+1 tolerate f, and quorum overlap gives safety), a distinguished leader to skip the propose phase, and random backoff against livelock; once a value is accepted future proposers must keep it. (P039)

## Grounding

Distilled (no verbatim) from this package's principles (P027, P028, P035, P036, P037, P038, P039) and their anchored claims/evidence. Verify version-specific PostgreSQL or SQLite syntax and behaviour against current official documentation.
