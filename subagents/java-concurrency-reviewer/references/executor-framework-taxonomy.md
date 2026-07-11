---
name: executor-framework-taxonomy
kind: reference
status: ready
provenance:
  principles: []
  claims: []
  source_anchors: []
---

# Executor Framework Taxonomy

A reference for the `java.util.concurrent` execution framework (J2SE 5.0+): the factory shortcuts,
the `ThreadPoolExecutor` parameters that actually decide behavior, the scheduled variant, and the
`Callable`/`Future` result model. Used to review or recommend pool configuration.

## Executors factory shortcuts

| Factory method | Produces | Watch out for |
|----------------|----------|---------------|
| `newFixedThreadPool(n)` | Fixed `n` threads, unbounded queue | Unbounded queue can grow to OOM under overload |
| `newCachedThreadPool()` | Grows threads on demand, 60s idle reap, `SynchronousQueue` | Unbounded thread creation — over-threading risk under bursty load |
| `newSingleThreadExecutor()` | One worker, unbounded queue | Serializes all tasks; queue can still grow unbounded |
| `newScheduledThreadPool(n)` | Delayed / periodic execution | Replaces hand-rolled timers |

For overload safety, prefer constructing `ThreadPoolExecutor` directly with a **bounded** queue and
an explicit rejection policy instead of the unbounded factory shortcuts.

## ThreadPoolExecutor parameters

| Parameter | Role | Guidance |
|-----------|------|----------|
| corePoolSize | Threads kept alive at steady state | CPU-bound ≈ core count; I/O-bound larger |
| maximumPoolSize | Upper bound on threads | Only grows beyond core when the queue is full (non-unbounded) |
| keepAliveTime | Idle reap time for threads above core | Trims burst capacity after load drops |
| workQueue | Holds tasks awaiting a thread | See queue types below |
| RejectedExecutionHandler | What to do when saturated | Abort / CallerRuns / DiscardOldest / Discard |

## Work-queue types

| Queue | Behavior | Consequence |
|-------|----------|-------------|
| Bounded (`ArrayBlockingQueue`) | Capacity cap, back-pressure | Rejects when full → overload protection |
| Unbounded (`LinkedBlockingQueue`) | Never rejects | maximumPoolSize never reached; OOM risk |
| Direct hand-off (`SynchronousQueue`) | No storage; hand to a thread or reject | Forces new thread or rejection per task |
| Priority (`PriorityBlockingQueue`) | Ordered by task priority | Starvation risk for low-priority tasks |

## Callable / Future

| Element | Use |
|---------|-----|
| `Runnable` | Fire-and-forget task, no result |
| `Callable<T>` | Task that returns `T` or throws | 
| `Future<T>` | Handle to the result; `get()` blocks, `get(timeout)` bounds the wait |
| `ExecutionException` | Wraps a task-thrown exception, surfaced by `get()` |
| `cancel(mayInterrupt)` | Requests cancellation of a submitted task |

Prefer a timed `Future.get(timeout)` so a hung task does not block the caller forever; always
`shutdown()` (and optionally `awaitTermination`) the pool so the application can exit.

## Provenance

Tier 0. Derived from the profile `knowledge_partition.references` Executor entry, the `always_on`
Executor-framework rule (pools decouple submission from lifecycle; core/max/queue determine
throughput and latency; `Callable`/`Future` for results), and the `when_to_use` Executor entry;
synthesized against the source (Scott Oaks & Henry Wong, *Java Threads*, O'Reilly 3rd ed. 2004,
Executor material). No principle/claim layer at this tier; not drift-tracked. Paraphrased — no
verbatim quotation (`distillation-only` source).
