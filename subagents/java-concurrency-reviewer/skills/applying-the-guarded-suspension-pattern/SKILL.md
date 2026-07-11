---
name: applying-the-guarded-suspension-pattern
kind: skill
status: ready
provenance:
  principles: []
  claims: []
  source_anchors: []
---

# Applying the Guarded-Suspension Pattern

## Purpose

Guarded suspension makes a method wait until the object reaches a state in which the action
can legally proceed, instead of failing or returning a wrong result. This skill gives the
correct skeleton — a `while`-condition loop around `wait()`, a single state-change point that
calls `notifyAll()`, and optional timeout arithmetic — so that wait/notify code is free of
missed notifications, spurious wakeups, and stale-condition bugs.

## When to use

- A method must block until a precondition holds (buffer non-empty, resource available,
  flag set) rather than returning early or throwing.
- `wait/notify` code is suspected of a missed-notification, spurious-wakeup, or
  guarded-loop error.
- A reviewer must verify a wait site holds the lock, loops on the condition, and justifies
  `notify` vs. `notifyAll`.

## Procedure

1. **Confirm the lock is held at the wait site.** `wait()`, `notify()`, and `notifyAll()` are
   only legal while the calling thread owns the monitor of the target object — i.e. inside a
   `synchronized` method or block on that object. A call outside the monitor throws
   `IllegalMonitorStateException`. Flag any wait/notify not provably under the lock.
2. **Guard the wait inside a `while` loop, never an `if`.** Re-test the predicate after each
   wakeup: `while (!condition) wait();`. An `if` is wrong because (a) `wait()` can wake
   spuriously and (b) another awakened thread may have already consumed the state. The loop
   re-checks and re-suspends if the condition is still false.
3. **Let `wait()` release-and-reacquire atomically.** Entering `wait()` atomically releases the
   monitor and suspends the thread; on wakeup it reacquires the monitor before returning. Do
   not hand-roll any unlock/relock around it.
4. **Signal at every state change that could satisfy a waiter.** Any method that mutates state a
   guard depends on must call `notifyAll()` (still under the lock) after the mutation. A change
   with no corresponding notify is a latent missed-notification: a waiter can sleep forever.
5. **Prefer `notifyAll` unless single-waiter is proven.** `notify()` wakes one arbitrary waiting
   thread; if waiters guard different conditions, it can wake the wrong one and lose the wakeup
   for the right one. Use `notify()` only when all waiters are interchangeable and wait on the
   same condition; otherwise `notifyAll()`.
6. **For a bounded wait, track remaining time explicitly.** Compute a deadline once
   (`deadline = now + timeout`); on each loop iteration call `wait(remaining)` where
   `remaining = deadline - now`. If `remaining <= 0`, give up (return failure / throw) instead
   of calling `wait(0)`, which blocks indefinitely.
7. **Propagate interruption.** `wait()` can throw `InterruptedException`; do not swallow it.
   Either let it propagate or restore the interrupt flag so the cancellation is not lost.

## Inputs

- The class and the method that must block, the predicate it waits on, and every method that
  mutates the state the predicate reads.
- Whether multiple distinct wait conditions share the same monitor (decides `notify` vs.
  `notifyAll`), and whether a bounded timeout is required.

## Output

A verdict on the wait/notify site: whether the lock is held, the guard is a loop, every
state-changer notifies, `notify` vs. `notifyAll` is justified, the timeout arithmetic is
correct, and interruption is handled — with a minimal corrective snippet for any defect.

## References

- `references/thread-api-quick-reference.md` — `wait`/`notify`/`notifyAll` signatures and the
  monitor-ownership rule.
- `references/concurrency-pattern-taxonomy.md` — where guarded suspension sits among the
  synchronization patterns.

## Provenance

Tier 0. Derived from the profile `always_on` wait/notify protocol rule (wait under the lock,
inside a guarded loop, atomic release/reacquire, lost-notify risk, `notifyAll` safer) and the
`quality_bar` requirement that wait/notify usages hold the lock, use a guarded loop, justify
`notify` vs. `notifyAll`, and exclude lost-notification scenarios; synthesized against the
source (Doug Lea, *Concurrent Programming in Java*, Addison-Wesley 1997, guarded-suspension /
waiting patterns). No principle/claim layer at this tier; not drift-tracked. Paraphrased — no
verbatim quotation (`distillation-only` source).
