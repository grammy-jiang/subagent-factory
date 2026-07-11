---
name: reducing-synchronized-lock-scope
kind: skill
status: ready
provenance:
  principles: []
  claims: []
  source_anchors: []
---

# Reducing Synchronized Lock Scope

## Purpose

A method marked `synchronized` in its entirety holds the lock across work that does not touch
shared state — I/O, computation, logging — needlessly serializing other threads. This skill
shrinks the critical section to just the shared-state access, releasing the lock earlier to raise
concurrency, without breaking the atomicity the lock was protecting.

## When to use

- A large `synchronized` method holds the lock across non-shared work and is a throughput
  bottleneck.
- A reviewer must judge whether a critical section can be narrowed safely.
- Lock contention is high and profiling points to a coarse-grained lock.

## Procedure

1. **Classify each statement as shared or local.** Walk the method and mark which statements read
   or write shared mutable state and which operate only on locals, parameters, or immutable data.
   Only the shared accesses need the lock.
2. **Move computation and I/O out of the critical section.** Compute new values into locals before
   entering the lock, and perform I/O / logging / callbacks after leaving it. Holding a lock
   across a blocking call is both a throughput loss and a deadlock risk (see open-call).
3. **Narrow `synchronized` from method to block.** Replace `synchronized` on the whole method with
   a `synchronized (lock) { ... }` block wrapping only the shared accesses, so the lock is held for
   the minimum span.
4. **Preserve the atomic unit.** The shared reads and writes that must happen together must stay in
   one critical section. Do not split a compound operation (e.g. check-then-act, increment) across
   two blocks — that reintroduces a race the single lock prevented. Narrowing is safe only when the
   moved-out work does not depend on, or invalidate, the locked invariant.
5. **Re-validate after a gap.** If you read shared state, release the lock, then act on it, the
   state may have changed in between; re-acquire and re-check rather than acting on a stale read.
6. **Consider a finer lock granularity.** Where independent fields are guarded by one lock, give
   them separate locks (split synchronization) so unrelated operations no longer contend — a
   structural complement to shrinking a single block.
7. **Confirm visibility is preserved.** Every access to the shared field must still occur under the
   same lock (or be `volatile`); narrowing must not leave a read or write outside all
   synchronization, which would lose the visibility guarantee.

## Inputs

- The synchronized method, which statements touch shared state, which compound operations must
  remain atomic, and the contention profile.

## Output

A narrowed critical section (method → block), with non-shared work moved out, the preserved
atomic unit identified, any required re-validation after a lock gap, and confirmation that no
shared access was left unsynchronized.

## References

- `references/concurrency-overhead-taxonomy.md` — synchronization and contention overhead.
- `references/concurrency-pattern-taxonomy.md` — split synchronization and related techniques.

## Provenance

Tier 0. Derived from the profile `knowledge_partition.skills` lock-scope-reduction entry, the
`always_on` Java-memory-model rule (synchronized provides atomicity and visibility) and
fully-synchronized-object rule, and the `quality_bar` atomicity requirements; synthesized against
the source (Doug Lea, *Concurrent Programming in Java*, Addison-Wesley 1997, lock-granularity /
performance material). No principle/claim layer at this tier; not drift-tracked. Paraphrased — no
verbatim quotation (`distillation-only` source).
