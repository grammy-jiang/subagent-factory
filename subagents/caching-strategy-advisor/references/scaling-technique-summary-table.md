---
name: scaling-technique-summary-table
kind: reference
status: ready
provenance:
  principles:
  - P004
  - P008
  claims:
  - C00079
  - C00080
  - C00081
  - C00082
  - C00083
  - C00084
  - C00087
  - C00088
  - C00089
  - C00090
  evidence:
  - E00036
  - E00037
  - E00038
  - E00039
  - E00040
  - E00041
  - E00042
  - E00043
  - E00044
  - E00045
  source_anchors:
  - 11ebbc818b96-c0002
  authored_from_digest: 3e6e8c9f7061fd9228d119eb0d54d4b9d694c882ff707ffd2397b590b54e23cf
---

# Scaling Technique Summary Table

Caches encounter two categories of limit (c046, h0094): **storage limits** — the cache cannot
hold the full working dataset — and **resource limits** — CPU or network capacity is saturated
before storage is exhausted. Diagnose which limit is binding before selecting a remedy; applying
the wrong technique leaves the bottleneck untouched (P006).

## Technique reference

| Technique | Constraint addressed | What it improves | Key limitations |
|-----------|---------------------|-----------------|----------------|
| **Vertical scaling (scale up)** | Storage + resource | Both read and write capacity on a single node by enlarging RAM, CPU, and network | Bounded by the largest available single-node instance; provides no topology redundancy |
| **Read replicas** | Resource (reads only) | Read throughput and read availability by distributing reads across replica nodes (c048, h0097) | All writes still route to the single primary — write throughput does not improve; does not help multi-region writes (c064, h0113) |
| **Sharding** | Storage + throughput (reads and writes) | Near-linear capacity and throughput growth as shards are added; each shard holds a deterministic subset of keys (c049, h0098) | Shard-selector tuning required in generic implementations; re-sharding/rebalancing adds operational complexity; single-shard failure can affect availability if not managed |
| **Active-Active (multi-master)** | Write throughput + multi-region write latency | Both read and write throughput; any node accepts writes at local latency across regions (c051, h0099) | Write conflicts arise when two nodes receive updates to the same key concurrently; inter-node replication lag means nodes may briefly hold divergent values; requires Redis Enterprise for CRDT-based conflict resolution — open-source Redis does not natively support multi-master (c052, c053, h0100; c064, h0113) |

## Selection guidance (P006, P007)

Apply the following decision sequence:

1. **Identify the binding limit first.** Measure whether evictions, storage exhaustion, or CPU/network saturation is the observed symptom before picking a technique (P006).

2. **Read-bound, single region** → read replicas distribute read load across replica nodes while keeping the topology simple. No write-scaling benefit.

3. **Storage-bound or write-bound, single region** → sharding partitions data across nodes, expanding both capacity and write throughput. Combine with read replicas when the workload is simultaneously read-heavy and write-intensive.

4. **Multi-region low-latency writes** → Active-Active multi-master via Redis Enterprise. Single-region write workloads do not require it and should not pay the conflict-resolution overhead. Open-source Redis supports only a single master; multi-region write performance requires Redis Enterprise Active-Active with CRDT conflict resolution (c064, h0113, P007).

Use in conjunction with the `active-active-conflict-assessment` and `cache-performance-break-even` skills.

## Provenance

Distillation-only source: Atchison, *Caching at Scale With Redis* (2021).
Principles P006 (diagnose storage vs resource binding limit) and P007 (match topology to dominant constraint).
Claims c046 (two limit types, h0094), c048 (read replicas, h0097), c049 (sharding, h0098),
c051 (Active-Active mechanism, h0099), c052 (write conflicts, h0100), c053 (Redis Enterprise CRDT, h0100),
c064 (open-source single-master constraint + multi-region requires Redis Enterprise, h0113).
