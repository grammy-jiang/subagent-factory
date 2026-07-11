---
name: implementing-optimistic-methods
kind: skill
status: ready
provenance:
  principles: []
  claims: []
  source_anchors: []
---

# Implementing Optimistic Methods

## Purpose

An optimistic method avoids holding a lock for the whole operation: it reads state, computes a
new value off to the side, then commits only if the state has not changed since the read,
retrying on conflict. This skill structures that read–compute–commit–retry cycle and bounds its
livelock risk, so it raises concurrency without sacrificing safety.

## When to use

- A short critical section has high read contention and lock-holding is the bottleneck.
- A field can be updated with an atomic compare-and-set (J2SE 5.0+ `AtomicInteger`,
  `AtomicReference`, or a version/stamp field).
- A reviewer must judge whether an optimistic retry loop can livelock or starve a thread.

## Procedure

1. **Snapshot the state without holding a lock for the computation.** Read the current value (and
   a version/stamp if used) into locals. The expensive computation runs on the snapshot, off the
   shared object, so other threads are not blocked during it.
2. **Compute the new value as a pure function of the snapshot.** The computation must not mutate
   shared state and must be safe to repeat — it may run several times before a commit succeeds.
3. **Commit with an atomic compare-and-set.** Attempt to install the new value only if the shared
   state still equals the snapshot: `compareAndSet(expected, new)`. If it succeeds, the update was
   conflict-free. If it fails, another thread committed first.
4. **On conflict, re-read and retry.** A failed commit loops back to step 1 with a fresh
   snapshot. Do not blindly overwrite — that would lose the other thread's update (a lost-update
   race).
5. **Bound the retry to avoid livelock.** Pure spin-retry can livelock under heavy contention:
   threads keep colliding and none finishes. Cap retries and fall back (back off, yield, or take
   a real lock) so a thread cannot spin forever. Note this explicitly when reviewing an unbounded
   retry loop.
6. **Use a stamp for the ABA hazard.** If the value can change A→B→A between read and commit, a
   plain compare-and-set wrongly succeeds; use a versioned reference (`AtomicStampedReference`) or
   monotonic stamp so the commit detects the intervening change.
7. **Confirm the operation is genuinely a single set-once or replaceable update.** Optimistic
   methods fit replace-whole-value updates; multi-field invariants that must change together are
   not a fit and need a lock.

## Inputs

- The field(s) updated, whether the update is a whole-value replace or a multi-field invariant,
  the contention level, and the Java version (atomics require J2SE 5.0+).

## Output

A structured read–compute–commit–retry recommendation with the chosen atomic primitive, an
explicit retry bound and fallback, an ABA assessment, and a verdict on whether the operation is
a valid optimistic candidate or needs locking.

## References

- `references/concurrency-pattern-taxonomy.md` — optimistic methods among the synchronization
  patterns.
- `references/volatile-usage-rules.md` — why `volatile` alone cannot make a compound update
  atomic.

## Provenance

Tier 0. Derived from the profile `knowledge_partition.skills` optimistic-methods entry (read,
compute, commit, retry; livelock risk), the `always_on` `volatile`/atomicity rule (compound
operations need more than per-variable visibility), and the `when_to_use` optimistic-update
entry; synthesized against the source (Doug Lea, *Concurrent Programming in Java*, Addison-Wesley
1997, optimistic-method material) with `java.util.concurrent.atomic` compare-and-set noted as the
modern primitive. No principle/claim layer at this tier; not drift-tracked. Paraphrased — no
verbatim quotation (`distillation-only` source).
