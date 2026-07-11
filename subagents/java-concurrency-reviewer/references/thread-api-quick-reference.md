---
name: thread-api-quick-reference
kind: reference
status: ready
provenance:
  principles: []
  claims: []
  source_anchors: []
---

# Thread API Quick Reference

A compact reference for the `Thread` lifecycle methods, the `Object` monitor methods, and
interrupt semantics the reviewer checks against. Behavior summaries are paraphrased from the Java
threading model.

## Thread lifecycle states

| State | Meaning |
|-------|---------|
| NEW | Created, not yet started |
| RUNNABLE | Eligible to run (running or waiting for CPU) |
| BLOCKED | Waiting to acquire a monitor lock |
| WAITING | Waiting indefinitely in `wait()`/`join()`/`park()` |
| TIMED_WAITING | Waiting with a timeout (`sleep`, timed `wait`/`join`) |
| TERMINATED | Run completed; cannot be restarted |

A thread must be `start()`ed before it runs; a terminated thread cannot be restarted.

## Thread methods

| Method | Effect | Review note |
|--------|--------|-------------|
| `start()` | Begins execution in a new thread; calls `run()` | Calling `run()` directly does **not** start a thread |
| `join()` / `join(ms)` | Caller waits until target terminates (or timeout) | Throws `InterruptedException`; do not swallow |
| `sleep(ms)` | Suspends current thread; **does not release locks** | Holding a lock across `sleep` blocks others |
| `interrupt()` | Sets interrupt flag; unblocks `wait`/`sleep`/`join` with `InterruptedException` | Cooperative — target must check/handle it |
| `isInterrupted()` | Tests the flag without clearing it | Poll in non-blocking loops |
| `interrupted()` (static) | Tests **and clears** the current thread's flag | Easy to lose the signal — prefer `isInterrupted()` |
| `setPriority(int)` | Sets priority (1–10; `MIN`/`NORM`/`MAX`) | JVM behavior; OS mapping varies, no guarantee |
| `setDaemon(boolean)` | Marks a daemon thread (JVM exits without waiting) | Must be set before `start()` |
| `stop()` / `suspend()` / `resume()` | **Deprecated, unsafe** | Never recommend; use cooperative cancellation |

## Object monitor methods (call only while holding the object's lock)

| Method | Effect | Review note |
|--------|--------|-------------|
| `wait()` / `wait(ms)` | Atomically releases the lock and suspends until notified/timeout/interrupt | Must be inside a `while`-condition loop |
| `notify()` | Wakes one arbitrary waiter | Safe only when all waiters are interchangeable |
| `notifyAll()` | Wakes all waiters; each re-tests its condition | Default safe choice |

Calling any monitor method without owning the lock throws `IllegalMonitorStateException`.

## Interrupt protocol summary

1. `interrupt()` sets a flag and makes blocking methods throw `InterruptedException`.
2. Code must poll `isInterrupted()` in compute loops and handle `InterruptedException` in blocking
   calls — either exit cleanly or restore the flag (`Thread.currentThread().interrupt()`).
3. Never swallow `InterruptedException` with an empty catch.

## Provenance

Tier 0. Derived from the profile `knowledge_partition.references` thread-API entry, the `always_on`
thread-lifecycle, wait/notify-protocol, and interrupt-protocol rules, and the `forbidden_behaviours`
ban on deprecated `stop`/`suspend`/`resume`; synthesized against the source (Scott Oaks & Henry
Wong, *Java Threads*, O'Reilly 3rd ed. 2004, Thread/Object API material). No principle/claim layer
at this tier; not drift-tracked. Paraphrased — no verbatim quotation (`distillation-only` source).
