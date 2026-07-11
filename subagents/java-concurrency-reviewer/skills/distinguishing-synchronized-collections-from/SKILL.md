---
name: distinguishing-synchronized-collections-from
kind: skill
status: ready
provenance:
  principles: []
  claims: []
  source_anchors: []
---

# Distinguishing Synchronized Collections from Concurrent Collections

## Purpose

A `Collections.synchronizedMap`/`synchronizedList` wrapper locks every method on one lock;
`ConcurrentHashMap`, `CopyOnWriteArrayList`, and friends use finer-grained or copy-on-write
strategies. They are not interchangeable: choosing wrong gives either a contention bottleneck or a
broken compound operation. This skill selects the right collection by the read/write ratio and the
atomicity the call site needs.

## When to use

- Shared collection access is a contention bottleneck, or a `synchronizedXxx` wrapper is used in a
  hot path.
- A reviewer sees iteration over, or check-then-act on, a shared collection and must judge its
  safety.
- A team must pick a thread-safe collection for a given read/write profile (J2SE 5.0+).

## Procedure

1. **Identify the access profile.** Measure or estimate the read/write ratio and the contention.
   Read-mostly, write-rarely is the case for copy-on-write; mixed read/write at scale is the case
   for `ConcurrentHashMap`.
2. **Know what a synchronized wrapper does and does not give.** `Collections.synchronizedMap`
   serializes every method on a single lock — simple, but a bottleneck under contention, AND it
   does **not** make compound operations (iterate, put-if-absent, check-then-act) atomic. Those need
   external synchronization on the wrapper.
3. **Use `ConcurrentHashMap` for high-concurrency maps.** It allows concurrent reads and scales
   writes without a single global lock, and provides atomic compound methods (`putIfAbsent`,
   `compute`, `merge`) that replace error-prone check-then-act. Iteration is weakly consistent — it
   does not throw `ConcurrentModificationException` but may not reflect concurrent updates.
4. **Use `CopyOnWriteArrayList`/`CopyOnWriteArraySet` for read-mostly collections.** Each write
   copies the backing array, so reads and iteration are lock-free and never throw on concurrent
   modification — but writes are O(n) and costly. Only correct when writes are rare relative to
   reads.
5. **Match the atomic primitive to the compound operation.** Replace "if absent then put" with
   `putIfAbsent`, "get-modify-set" with `compute`/`merge`. Do not emulate these with separate calls
   on a concurrent map — the gap between calls is a race even though each call is individually safe.
6. **Guard iteration explicitly.** Over a synchronized wrapper, hold the wrapper's lock for the
   whole iteration. Over a concurrent collection, accept weakly-consistent iteration and do not
   assume a stable snapshot unless using a copy-on-write type.
7. **Recommend by ratio.** Read-dominated → copy-on-write; balanced/large → `ConcurrentHashMap`;
   low-traffic/simple → a synchronized wrapper is acceptable. State the deciding ratio.

## Inputs

- The collection, its read/write ratio and contention, the compound operations performed on it,
  iteration requirements, and the Java version (concurrent collections need J2SE 5.0+).

## Output

A collection recommendation (synchronized wrapper vs. `ConcurrentHashMap` vs. copy-on-write) keyed
to the read/write ratio, the atomic method to use for each compound operation, the iteration
guarantee, and a verdict on any unsafe check-then-act on the current collection.

## References

- `references/concurrency-overhead-taxonomy.md` — synchronization vs. copy overhead tradeoff.
- `references/volatile-usage-rules.md` — why per-call safety does not make a compound operation
  atomic.

## Provenance

Tier 0. Derived from the profile `knowledge_partition.skills` collections entry (synchronized vs.
concurrent; select by read/write ratio), the `always_on` Java-memory-model and `volatile`/atomicity
rules (per-call safety ≠ compound atomicity), and the `quality_bar` atomicity requirement;
synthesized against the source (Scott Oaks & Henry Wong, *Java Threads*, O'Reilly 3rd ed. 2004,
concurrent-collections material). No principle/claim layer at this tier; not drift-tracked.
Paraphrased — no verbatim quotation (`distillation-only` source).
