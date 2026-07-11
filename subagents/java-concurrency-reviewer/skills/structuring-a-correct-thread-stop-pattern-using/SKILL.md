---
name: structuring-a-correct-thread-stop-pattern-using
kind: skill
status: ready
provenance:
  principles: []
  claims: []
  source_anchors: []
---

# Structuring a Correct Thread-Stop Pattern

## Purpose

`Thread.stop()`, `suspend()`, and `resume()` are deprecated and unsafe — they release locks at
arbitrary points and leave objects in inconsistent states. This skill structures cooperative
cancellation instead: a `volatile boolean` flag the run loop polls, and/or `interrupt()` to
unblock a waiting thread, with `InterruptedException` handled rather than swallowed.

## When to use

- Code stops a thread with the deprecated `Thread.stop()`/`suspend()`/`resume()`.
- A long-running or blocking task needs a clean shutdown signal.
- A reviewer sees an `InterruptedException` caught and ignored, or a loop with no cancellation
  check.

## Procedure

1. **Ban the deprecated stop methods.** `stop()`/`suspend()`/`resume()` have known race
   conditions and must never be used. Flag any occurrence and replace it with cooperative
   cancellation.
2. **Add a `volatile boolean` stop flag for compute loops.** Declare `private volatile boolean
   running = true;`. The run loop checks `while (running) { ... }`. `volatile` is required so the
   stopping thread's write is visible to the worker; a plain field may never be observed as
   changed.
3. **Poll the flag at a safe granularity.** Check the flag often enough to stop promptly but at
   points where the object's invariants hold, so the thread exits cleanly between units of work,
   not mid-mutation.
4. **Use `interrupt()` to unblock a waiting/sleeping thread.** A flag alone cannot wake a thread
   blocked in `wait`, `sleep`, or `join`. Call `interrupt()` to make those methods throw
   `InterruptedException`; combine it with the flag so both blocked and running states cancel.
5. **Handle `InterruptedException` — never swallow it.** On catching it, either (a) clean up and
   exit the run loop, or (b) restore the interrupt status with `Thread.currentThread().interrupt()`
   so callers up the stack still see the cancellation. An empty catch block discards the signal
   and is a defect.
6. **Check `isInterrupted()` in loops that do not block.** A purely computational loop should
   test `Thread.currentThread().isInterrupted()` alongside (or instead of) the flag so an
   interrupt-based cancellation is honored.
7. **Make shutdown idempotent and leave state consistent.** Setting the flag twice, or
   interrupting an already-stopping thread, must be harmless; the thread must finish or roll back
   the current unit so shared state is left valid.

## Inputs

- The thread's run loop, whether it blocks (wait/sleep/join) or only computes, the current stop
  mechanism, and how `InterruptedException` is currently handled.

## Output

A corrective stop pattern: a `volatile` flag and/or `interrupt()`, the polling/checking points,
correct `InterruptedException` handling (exit or restore-flag, never swallow), and removal of any
deprecated `stop`/`suspend`/`resume`.

## References

- `references/thread-api-quick-reference.md` — `interrupt`, `isInterrupted`, and the deprecated
  methods.
- `references/volatile-usage-rules.md` — why the flag must be `volatile`.

## Provenance

Tier 0. Derived from the profile `knowledge_partition.skills` thread-stop entry, the `always_on`
interrupt-protocol rule (interrupt sets a flag and unblocks blocked methods; check
`isInterrupted()`; deprecated `stop()` must never be used) and `volatile` visibility rule, and
the `forbidden_behaviours` ban on `Thread.stop`/`suspend`/`resume`; synthesized against the
source (Scott Oaks & Henry Wong, *Java Threads*, O'Reilly 3rd ed. 2004, thread cancellation /
interrupt material). No principle/claim layer at this tier; not drift-tracked. Paraphrased — no
verbatim quotation (`distillation-only` source).
