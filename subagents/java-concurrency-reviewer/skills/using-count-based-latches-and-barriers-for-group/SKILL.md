---
name: using-count-based-latches-and-barriers-for-group
kind: skill
status: ready
provenance:
  principles: []
  claims: []
  source_anchors: []
---

# Using Count-Based Latches and Barriers for Group Algorithms

## Purpose

Iterative group algorithms need threads to rendezvous: wait until N events have happened
(a latch) or until all participants reach a phase boundary before any proceeds (a barrier). This
skill selects and structures the right count-based coordinator so phases stay synchronized
without a hand-rolled, race-prone counter.

## When to use

- A computation runs in parallel phases where every worker must finish phase *k* before any
  starts phase *k+1*.
- A controller must block until a fixed number of one-time events (initializations, task
  completions) have occurred.
- A reviewer sees a hand-rolled shared counter with wait/notify coordinating group progress and
  must judge its correctness.

## Procedure

1. **Distinguish one-shot from cyclic coordination.** A **latch** counts down to zero once and
   then stays open — for one-time start/finish gating. A **barrier** resets after each trip — for
   repeated phase boundaries in an iterative algorithm. Choosing the wrong one (latch where a
   barrier is needed) breaks after the first iteration.
2. **For a latch, set the count to the number of awaited events.** Each event decrements the
   count; waiters block until it reaches zero, then all proceed. The count cannot be reused —
   create a new latch per round (`CountDownLatch` on J2SE 5.0+).
3. **For a barrier, set the party count to the number of participants.** Each worker calls await
   at the phase boundary; the barrier releases all of them only when the last arrives, then resets
   for the next phase (`CyclicBarrier` on J2SE 5.0+). Optionally run a barrier action once per
   trip for phase aggregation.
4. **Guard the count under a lock and loop on the condition.** If hand-rolled, the counter and its
   wait must follow the guarded-suspension rules: mutate under the lock, wait in a `while` loop,
   `notifyAll` on each decrement. An `if`-guarded or unlocked counter races.
5. **Handle a participant that fails or is interrupted.** A barrier where one party never arrives
   blocks all of them forever. Use a timeout or the barrier's broken-state handling so a failed
   worker breaks the barrier rather than deadlocking the group.
6. **Verify count arithmetic against participant count.** An off-by-one in the initial count is a
   silent deadlock (waiters never released) or premature release (proceed before all done). Check
   that the count equals exactly the number of decrements/arrivals expected.
7. **Prefer the library primitives over a hand-rolled counter on J2SE 5.0+.** `CountDownLatch`,
   `CyclicBarrier`, and `Phaser` implement these contracts correctly; recommend them.

## Inputs

- The number of participants/events, whether coordination is one-shot or per-iteration, failure
  and timeout requirements, and the Java version.

## Output

A recommendation of latch vs. barrier with the count set correctly, the failure/timeout handling,
a verdict on any hand-rolled counter's correctness (lock, loop, arithmetic), and a pointer to the
matching `java.util.concurrent` primitive.

## References

- `references/concurrency-pattern-taxonomy.md` — coordination primitives among the patterns.
- `references/thread-api-quick-reference.md` — `join`, monitor methods used in hand-rolled
  coordination.

## Provenance

Tier 0. Derived from the profile `knowledge_partition.skills` latches/barriers entry, the
`always_on` wait/notify protocol and liveness-taxonomy (deadlock) rules, and the `when_to_use`
concurrency-design entry; synthesized against the source (Doug Lea, *Concurrent Programming in
Java*, Addison-Wesley 1997, group-coordination material) with `CountDownLatch`/`CyclicBarrier`
noted as the J2SE 5.0+ primitives. No principle/claim layer at this tier; not drift-tracked.
Paraphrased — no verbatim quotation (`distillation-only` source).
