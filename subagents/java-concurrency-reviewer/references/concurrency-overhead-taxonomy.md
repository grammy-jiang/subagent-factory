---
name: concurrency-overhead-taxonomy
kind: reference
status: ready
provenance:
  principles: []
  claims: []
  source_anchors: []
---

# Concurrency Overhead Taxonomy

A reference for the three categories of cost that concurrency adds, used to judge whether a design's
parallelism actually pays for itself and to size pools and lock granularity. Performance must be
weighed against these, not assumed.

## Overhead categories

| Category | Sources of cost | When it dominates | Mitigation |
|----------|-----------------|-------------------|------------|
| Construction / finalization | Creating and tearing down threads; per-thread stack memory; object allocation for tasks | Many short-lived threads (thread-per-message under high arrival) | Reuse threads via a pool; amortize construction across tasks |
| Synchronization / context-switching | Lock acquire/release, monitor contention, blocking and waking, scheduler context switches, cache flush/reload on lock boundaries | High contention on a coarse lock; many threads on few cores | Reduce lock scope; split locks; confine/immutable state; size pool to cores |
| Interaction / coordination | Hand-off through queues, wait/notify wakeups, barrier/latch rendezvous, copy-on-write copies | Fine-grained tasks with heavy inter-thread communication | Coarsen task granularity; batch hand-offs; choose collection by read/write ratio |

## Sizing implications

| Decision | Driven by | Rule of thumb |
|----------|-----------|---------------|
| Pool size | Construction + context-switch overhead vs. parallel work | CPU-bound ≈ core count; I/O-bound larger to cover blocking |
| Lock granularity | Synchronization/contention overhead | Hold the lock only over shared access; split independent state |
| Collection choice | Synchronization vs. copy overhead | Read-mostly → copy-on-write; balanced/large → `ConcurrentHashMap` |
| Thread-per-message vs. pool | Construction overhead vs. queueing latency | Bounded low-rate work → per-message; high-rate short tasks → pool |

## Review note

A concurrency change is only worthwhile when the parallel speedup exceeds the added overhead of
these three categories. Flag designs that add threads or locks without a measured or reasoned net
gain — extra threads on a saturated CPU add context-switch cost without throughput. Never assume a
scheduling or fairness guarantee when reasoning about overhead.

## Provenance

Tier 0. Derived from the profile `knowledge_partition.references` overhead entry
(construction/finalization, synchronization/context-switching, interaction overhead), the
`always_on` Executor-framework and memory-model rules, and the `when_to_use` overhead-assessment
entry; synthesized against both sources (Doug Lea, *Concurrent Programming in Java*, Addison-Wesley
1997, performance material; Scott Oaks & Henry Wong, *Java Threads*, O'Reilly 3rd ed. 2004, overhead
material). No principle/claim layer at this tier; not drift-tracked. Paraphrased — no verbatim
quotation (`distillation-only` sources).
