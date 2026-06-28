---
name: active-active-conflict-assessment
kind: skill
status: ready
provenance:
  principles:
  - P007
  claims:
  - C00093
  - C00096
  - C00110
  - C00111
  - C00112
  evidence:
  - E00046
  - E00047
  - E00048
  - E00049
  - E00050
  source_anchors:
  - 11ebbc818b96-c0002
  - 11ebbc818b96-c0003
  authored_from_digest: d5d8166d3300b80a879dcab53e01d2221219ab46e77033f532a573987299e5a9
---

# Active-Active Conflict Assessment

## Purpose

Determine whether a multi-region cache deployment genuinely requires Active-Active
(multi-master) replication for low-latency writes, and — if it does — identify the
resulting conflict-resolution and platform obligations the design must satisfy.

Active-Active allows any node to accept writes with local latency, which makes it the
appropriate topology when multi-region write latency is a hard requirement. It is not
appropriate for single-region or read-heavy workloads. Critically, multi-region Active-Active
with CRDT-based conflict resolution requires Redis Enterprise; open-source Redis supports only
a single master (P007, c064, e030, anchor h0100/h0113).

## When to use

- A cache must serve writes with low latency from more than one geographic region.
- Multi-region write latency is a stated performance or availability requirement.
- The team is choosing a scaling topology and needs to evaluate whether Active-Active is
  warranted versus read replicas or sharding.
- A cache consistency problem has been traced to distributed nodes temporarily holding
  different values (P003 root cause 3, c055, e026, anchor h0103).

## Inputs

- Where write traffic originates: single region or multiple geographic regions.
- Stated write-latency budget and whether cross-region write round-trips are acceptable.
- Consistency tolerance: whether the application can accept transient inter-node data lag
  and strong eventual consistency, or requires immediate consistency.
- Current or planned platform: open-source Redis, managed cloud Redis (ElastiCache, Azure
  Cache, Memorystore), or Redis Enterprise Cloud / self-hosted Enterprise.

## Procedure

### Step 1 — Check write-origin geography (P007)

Determine whether writes originate from a single region or from multiple regions.

- **Single region:** Active-Active is not needed. A single primary with read replicas is
  sufficient (c048, e020, anchor h0097). Do not recommend Active-Active for single-region
  deployments — this is a `does_not_apply_when` condition for P007.
- **Multiple regions:** Continue to Step 2.

### Step 2 — Quantify the single-master write-latency penalty

With open-source Redis or any single-master topology, all writes must travel to the single
primary regardless of where the writer is located. Document the cross-region latency cost for
each remote-write origin. If the latency is acceptable within the stated budget, a single
master with read replicas may remain sufficient; if not, continue to Step 3.

### Step 3 — Evaluate Active-Active trade-offs (c051, e022, anchor h0099)

Active-Active multi-master replication allows any node to accept both reads and writes
locally, which distributes load and eliminates the cross-region write-latency penalty.
However, it introduces two costs that the application design must absorb:

1. **Write conflicts.** When two writers update the same key on different nodes
   concurrently, the nodes will exchange conflicting update messages. An algorithm must
   resolve which value prevails (c052, e023, anchor h0100).
2. **Temporary data lag.** After a write is accepted on one node, a brief propagation delay
   occurs before the value is consistent across all nodes. Any read served from a different
   node during this window may return the prior value (c053, e024; also c059, e029,
   anchor h0106 — lag is more pronounced for edge or geographically distant nodes).

If the application cannot tolerate either cost, Active-Active is not appropriate regardless
of write-latency requirements. Resolve this before proceeding.

### Step 4 — Confirm CRDT conflict resolution and platform requirement (P007, c064, e030)

If Active-Active is warranted, conflict resolution must be addressed. Redis Enterprise
Active-Active Geo-Distribution uses conflict-free replicated data types (CRDTs) to achieve
strong eventual consistency and reduce the risk of divergent values across nodes
(anchor h0100). The application still bears responsibility for tolerating inter-node lag.

**Platform check — this step is mandatory:**
- Open-source Redis does not natively support multi-master replication (c064, e030,
  anchor h0100/h0113). It supports only a single master.
- Redis Enterprise (cloud or self-hosted) is required for CRDT-based Active-Active.
- Managed cloud provider offerings (AWS ElastiCache, Azure Cache for Redis, Google
  Memorystore) do not provide Active-Active multi-master with CRDT semantics in their
  standard tiers; Redis Enterprise Cloud is the relevant product.

Do not assert Active-Active CRDT availability on platforms not supported by evidence.
The forbidden-behaviour rule in the profile prohibits claiming Redis Enterprise features
are available in open-source Redis.

### Step 5 — Classify the consistency root cause if this assessment is part of a broader
consistency investigation (P003)

If the reason for evaluating Active-Active is an observed inconsistency problem rather than
a new deployment decision, confirm that distributed nodes holding divergent values is the
actual root cause before recommending Active-Active:

- Root cause 1 (backing data changes without cache update) — mitigated by invalidation or
  write-through; Active-Active does not help (c055, e026, anchor h0103).
- Root cause 2 (update propagation lag on a single topology) — mitigated by TTL bounded to
  the staleness window; Active-Active does not help (c057, e027, anchor h0105).
- Root cause 3 (divergent distributed nodes) — the CRDT-based Active-Active mitigation
  applies here (c058, e028, anchor h0105/h0106; P003).

### Step 6 — Produce the verdict

Summarise:

1. Whether Active-Active is warranted (yes / no / not yet determinable).
2. If yes: the conflict-resolution mechanism (CRDT via Redis Enterprise Active-Active
   Geo-Distribution), the platform requirement (Redis Enterprise), and the data-lag
   tolerance the application design must accept.
3. If no: the recommended alternative topology (read replicas, sharding, single master) and
   why it is sufficient.
4. Any open questions (e.g. platform budget not yet decided, consistency root cause not
   yet confirmed).

## Output

A structured Active-Active verdict containing:

- **Decision:** Active-Active warranted or not, with the single primary reason.
- **Conflict-resolution approach** (if yes): CRDT-based strong eventual consistency via
  Redis Enterprise Active-Active Geo-Distribution; data-lag tolerance requirement stated.
- **Platform requirement** (if yes): Redis Enterprise (cloud or self-hosted); note that
  open-source Redis does not support this topology.
- **Alternative topology** (if no): the recommended technique with rationale.
- **Open questions** that must be resolved before implementation proceeds.

The output is a recommendation document. No configuration files, scripts, or runnable
artifacts are produced.

## References

- `references/scaling-technique-summary-table.md` — side-by-side comparison of read
  replicas, sharding, and Active-Active against storage and resource limits.

## Provenance

Grounded in P007 (scaling topology selection; Active-Active for multi-region writes,
Redis Enterprise required for CRDT conflict resolution, open-source Redis single-master
only) and P003 (consistency root-cause classification; root cause 3 — divergent distributed
nodes — addressed by CRDT Active-Active). Evidence: e020–e024 (cache scaling chapter,
anchors h0097–h0101), e026–e029 (cache consistency chapter, anchors h0103/h0105/h0106),
e030 (Redis Enterprise cluster deployments chapter, anchor h0113). Source: Atchison 2021,
"Caching at Scale With Redis" (distillation-only; no verbatim quotation).
