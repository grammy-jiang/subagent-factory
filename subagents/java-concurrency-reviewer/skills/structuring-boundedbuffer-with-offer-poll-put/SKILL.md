---
name: structuring-boundedbuffer-with-offer-poll-put
kind: skill
status: ready
provenance:
  principles: []
  claims: []
  source_anchors: []
---

# Structuring a BoundedBuffer with offer/poll/put/take

## Purpose

A bounded buffer is the canonical producer–consumer hand-off: producers add, consumers remove,
and capacity is finite. This skill fixes the synchronization contract of its four access
variants — the non-blocking `offer`/`poll` pair and the blocking `put`/`take` pair — so the
buffer never overflows, never returns from an empty take, and never loses a wakeup.

## When to use

- A producer–consumer or worker-thread design hands work through a fixed-capacity buffer.
- A reviewer must decide whether a buffer method should block, fail fast, or time out.
- Existing buffer code is suspected of overflow, lost items, or a thread blocked forever on a
  full or empty buffer.

## Procedure

1. **Separate the two contracts explicitly.** Non-blocking variants return a status instead of
   waiting: `offer` returns `false` (or rejects) when full; `poll` returns `null` (or a sentinel)
   when empty. Blocking variants wait: `put` suspends until space exists; `take` suspends until
   an item exists. Never let a "non-blocking" method silently block, or a "blocking" method
   silently drop.
2. **Guard `put` on not-full and `take` on not-empty.** Each blocking method waits in a `while`
   loop on its precondition (`while (count == capacity) wait();` for `put`;
   `while (count == 0) wait();` for `take`) so spurious wakeups and races re-test the condition.
3. **Notify the opposite side after every successful mutation.** A successful `put` must signal
   waiting takers (buffer is now non-empty); a successful `take` must signal waiting putters
   (buffer now has space). A mutation with no matching notify strands the other side.
4. **Choose `notifyAll` unless the buffer uses condition-specific signaling.** With a single
   monitor guarding both not-full and not-empty waiters, `notify()` can wake a putter when only
   a taker should proceed (and vice versa), losing the wakeup; use `notifyAll()`. (Two separate
   `Condition` objects on an explicit `Lock` let you signal each side precisely — prefer that on
   J2SE 5.0+.)
5. **Keep the critical section minimal.** Hold the lock only to test the guard, mutate the
   slot/count, and notify. Do not perform producer/consumer work (I/O, computation) while
   holding the buffer lock.
6. **Offer a timed variant where unbounded blocking is unacceptable.** A timed `offer`/`poll`
   waits up to a deadline using the same remaining-time arithmetic as guarded suspension, then
   returns failure rather than blocking forever.

## Inputs

- The buffer's capacity, element type, and which call sites need blocking vs. non-blocking vs.
  timed semantics.
- The Java version (J2SE 5.0+ enables `java.util.concurrent` `BlockingQueue`, `Lock`, and
  `Condition`, which usually replace a hand-rolled buffer).

## Output

A per-method synchronization contract (block / fail-fast / timeout), the guard condition and
notify target for each, a verdict on overflow/underflow/lost-wakeup risk, and — on J2SE 5.0+ —
a recommendation to use `ArrayBlockingQueue`/`LinkedBlockingQueue` instead of a hand-rolled
buffer.

## References

- `references/concurrency-pattern-taxonomy.md` — producer–consumer / bounded-buffer pattern.
- `references/executor-framework-taxonomy.md` — bounded work queues feeding a thread pool.

## Provenance

Tier 0. Derived from the profile `when_to_use` producer–consumer entry, the `always_on`
wait/notify protocol and fully-synchronized-object rules, and the `quality_bar` wait/notify
verification; synthesized against the source (Doug Lea, *Concurrent Programming in Java*,
Addison-Wesley 1997, bounded-buffer / producer–consumer material) with the
`java.util.concurrent` `BlockingQueue` contract noted as the modern replacement. No
principle/claim layer at this tier; not drift-tracked. Paraphrased — no verbatim quotation
(`distillation-only` source).
