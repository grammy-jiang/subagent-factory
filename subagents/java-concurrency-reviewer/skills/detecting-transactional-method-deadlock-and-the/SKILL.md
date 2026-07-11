---
name: detecting-transactional-method-deadlock-and-the
kind: skill
status: ready
provenance:
  principles: []
  claims: []
  source_anchors: []
---

# Detecting Transactional-Method Deadlock and Applying Resource Ordering

## Purpose

A "transactional" method that locks two or more objects (e.g. `a.transferTo(b)`) deadlocks when
two threads acquire the same pair of locks in opposite order. This skill detects that circular
acquisition and applies the canonical remedy: impose a global lock-acquisition order, typically
via a stable per-object key such as `System.identityHashCode`, so every thread takes the locks
in the same sequence.

## When to use

- A method synchronizes on two or more distinct objects to perform one logical operation.
- Two such operations can run concurrently with the participating objects swapped.
- A design is claimed deadlock-free and the reviewer must verify lock-acquisition order across
  threads rather than take the claim on trust.

## Procedure

1. **Enumerate the locks each method acquires and the order it acquires them.** For a method
   that locks objects X then Y, record the ordered pair (X, Y). Java does not auto-resolve
   deadlock between different objects, so the order is the whole game.
2. **Search for an opposing pair.** Deadlock is possible when one call path can acquire (X, Y)
   while another concurrently acquires (Y, X). A symmetric two-argument method called as
   `a.op(b)` and `b.op(a)` is the textbook case. Any cycle in the "waits-for" graph across the
   participating threads is a deadlock path.
3. **Do not declare deadlock-free without tracing the actual order.** A vague "it uses locks"
   says nothing; the circular order across threads must be shown absent.
4. **Impose a total order on lock acquisition.** Pick a stable, unique ordering key per object —
   `System.identityHashCode(obj)` is the common choice (a business primary key works when one
   exists). Always acquire the lower-key lock first, then the higher-key lock, in every method.
   With a single global order no cycle can form.
5. **Break identity-hash ties.** `identityHashCode` collisions are rare but possible; guard the
   equal-key case with a third "tie-break" lock (a shared `static` lock) acquired before the two
   object locks, so equal-keyed pairs still serialize safely.
6. **Apply the order at every site that locks the same object class.** A single method that
   ignores the ordering reintroduces the cycle. The ordering discipline must be global to the
   class, not local to one method.
7. **Prefer reducing lock scope where ordering is impractical.** If two locks need not be held
   simultaneously, restructure to hold one at a time (see lock-scope reduction) so no nested
   acquisition exists to order.

## Inputs

- The methods that acquire two or more locks, the objects involved, and the order of acquisition
  in each.
- Whether a natural stable ordering key (business key) exists, or `identityHashCode` must be
  used.

## Output

A deadlock verdict naming the circular acquisition path (which threads, which lock pair, which
order) and a corrective recommendation: the imposed acquisition order, the ordering key, and the
tie-break lock — or a restructure that removes the nested acquisition.

## References

- `references/concurrency-pattern-taxonomy.md` — resource ordering among the liveness remedies.
- `references/safety-checklist-template-a-release-gate-for-pre.md` — the deadlock line item.

## Provenance

Tier 0. Derived from the profile `always_on` deadlock rule (circular lock-acquisition order is
the canonical cause; resource-ordering the canonical remedy; Java does not auto-resolve
cross-object deadlock), the `quality_bar` requirement to assess deadlock by resource-ordering
analysis across threads, and the `forbidden_behaviours` ban on declaring a design deadlock-free
without tracing acquisition order; synthesized against the source (Doug Lea, *Concurrent
Programming in Java*, Addison-Wesley 1997, deadlock / resource-ordering material). No
principle/claim layer at this tier; not drift-tracked. Paraphrased — no verbatim quotation
(`distillation-only` source).
