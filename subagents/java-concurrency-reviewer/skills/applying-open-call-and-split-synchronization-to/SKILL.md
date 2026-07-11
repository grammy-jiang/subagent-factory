---
name: applying-open-call-and-split-synchronization-to
kind: skill
status: ready
provenance:
  principles: []
  claims: []
  source_anchors: []
---

# Applying Open-Call and Split-Synchronization to Avoid Nested-Monitor Lockout

## Purpose

When a synchronized method on one object calls a synchronized method on another while still
holding its own lock, the held lock can prevent the second object from ever reaching the state
the caller waits on — a nested-monitor lockout, and a deadlock risk. This skill applies two
remedies: the **open call** (release your own lock before invoking the other object) and
**split synchronization** (guard independent state with separate locks so an outbound call need
not hold the wrong one).

## When to use

- A synchronized method invokes another object's synchronized (especially blocking) method while
  holding its own monitor.
- Objects are composed hierarchically (a container delegating to held components) and a guard in
  one waits on a change made through another.
- A reviewer sees a wait/notify on object B reached only through a path that holds object A's
  lock — a lockout candidate.

## Procedure

1. **Map the held locks at each outbound call.** For every call from object A into another
   object's synchronized method, record which locks A still holds. A held lock across an
   outbound call is the hazard to examine.
2. **Identify lockout: a waiter that can never be notified.** Lockout occurs when the thread
   that would change the awaited state must first acquire a lock the waiter holds. If A holds its
   monitor while waiting for an effect that requires A's monitor to produce, no thread can ever
   satisfy it.
3. **Apply the open call.** Before invoking the other object, copy any needed state into locals,
   release A's lock (exit the synchronized block), make the call, then reacquire and re-validate
   if you must act on the result. The call happens with no lock held, so it cannot block other
   threads from progressing A's state. Re-check invariants after reacquisition — state may have
   changed while the lock was open.
4. **Apply split synchronization where state is independent.** If a class guards several
   independent fields under one lock, give each independent group its own lock object. A method
   touching only group 1 need not block — or hold — the lock that an outbound call interacts
   with. This shrinks the set of locks held across calls.
5. **Preserve invariants that span the split.** Splitting locks is only safe when the groups are
   genuinely independent; if an invariant spans both, splitting breaks atomicity. Keep
   cross-group operations under a documented ordering or a coarser lock.
6. **Re-verify no cycle remains.** After applying open call / split, re-run the lock-ordering
   check (see transactional-method deadlock) to confirm the restructuring did not create a new
   acquisition cycle.

## Inputs

- The class hierarchy, the synchronized methods, which locks are held across outbound calls, and
  which fields each lock guards.
- The invariants the class must preserve, to judge whether a lock can be split or a call opened.

## Output

A verdict naming each held-lock-across-call site and its lockout risk, plus a restructuring
recommendation — which call to open (with the re-validation needed after reacquisition) or which
lock to split — and confirmation that no new deadlock cycle is introduced.

## References

- `references/concurrency-pattern-taxonomy.md` — open call and split synchronization among the
  liveness techniques.
- `references/safety-checklist-template-a-release-gate-for-pre.md` — nested-call / lockout check.

## Provenance

Tier 0. Derived from the profile `knowledge_partition.skills` open-call/split-synchronization
entry, the `always_on` liveness-taxonomy (lockout) and lock-reentrancy rules, and the
`when_to_use` concurrency-design entry; synthesized against the source (Doug Lea, *Concurrent
Programming in Java*, Addison-Wesley 1997, liveness / open-call material). No principle/claim
layer at this tier; not drift-tracked. Paraphrased — no verbatim quotation (`distillation-only`
source).
