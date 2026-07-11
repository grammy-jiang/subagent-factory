---
name: configuring-threadpoolexecutor
kind: skill
status: ready
provenance:
  principles: []
  claims: []
  source_anchors: []
---

# Configuring ThreadPoolExecutor

## Purpose

`ThreadPoolExecutor` decouples task submission from thread lifecycle, but its behavior under load
depends entirely on how core size, maximum size, and the work queue are chosen. This skill sets
those parameters to the workload, selects a queue and rejection policy, and uses `Callable`/`Future`
for results — avoiding the over-threading and under-threading that wreck throughput or exhaust
resources.

## When to use

- Code configures a pool via `Executors`/`ThreadPoolExecutor` and needs review of pool sizing,
  queue policy, or task lifecycle.
- A service uses `Executors.newFixedThreadPool` / `newCachedThreadPool` and the reviewer must
  judge its overload behavior.
- Tasks need result retrieval (`Callable`/`Future`) or scheduling.

## Procedure

1. **Profile the tasks first.** Determine CPU-bound vs. I/O-bound and the arrival rate. Pool sizing
   follows the bottleneck: CPU-bound pools near the available core count; I/O-bound pools larger so
   cores stay busy while threads block.
2. **Set core and max size deliberately.** Core threads stay alive for steady load; max bounds the
   burst capacity. A fixed pool (core == max) gives predictable resource use; a pool with max >
   core grows only when the queue policy allows (see below). Avoid an unbounded `newCachedThreadPool`
   for unbounded arrival — it can create threads without limit and exhaust resources (over-threading).
3. **Choose the queue to match the back-pressure you want.** A **bounded** queue plus a sane
   rejection policy applies back-pressure and protects memory under overload. An **unbounded** queue
   never rejects but can grow until OOM and makes max-size irrelevant (the pool never exceeds core
   because tasks always queue). A **direct hand-off** (`SynchronousQueue`) forces a new thread or
   rejection per task. Name the chosen queue and its consequence.
4. **Set a rejection policy for the bounded case.** Decide what happens when the queue is full —
   abort (throw), caller-runs (back-pressure onto the submitter), or drop — and pick the one whose
   failure mode the system can tolerate.
5. **Use `Callable`/`Future` for results.** When a task returns a value or can fail, submit a
   `Callable` and retrieve via `Future.get()`; handle its `ExecutionException`/`InterruptedException`
   and consider a timed `get` so a hung task does not block the caller forever.
6. **Use `ScheduledThreadPoolExecutor` for delayed/periodic work** instead of hand-rolled timers.
7. **Always shut the pool down.** Call `shutdown()` (and, if needed, `awaitTermination`) so the
   application can exit; a never-shut pool keeps non-daemon threads alive. Do not swallow the
   `InterruptedException` from `awaitTermination`.

## Inputs

- Task CPU/I-O profile, arrival rate, whether tasks return results, the overload behavior the
  system must have, and the available core count.

## Output

A pool configuration: core/max size tied to the bottleneck, a queue type with its back-pressure
consequence, a rejection policy, `Callable`/`Future` handling for results, scheduling choice, and a
shutdown plan — with the over-/under-threading risk of the current config named.

## References

- `references/executor-framework-taxonomy.md` — factory methods, parameters, queue types,
  `Callable`/`Future`.
- `references/concurrency-overhead-taxonomy.md` — construction and context-switch overhead that
  bounds useful pool size.

## Provenance

Tier 0. Derived from the profile `knowledge_partition.skills` ThreadPoolExecutor entry, the
`always_on` Executor-framework rule (pools decouple submission from lifecycle; core/max/queue
determine throughput and latency; `Callable`/`Future` for results), and the `when_to_use`
Executor-configuration entry; synthesized against the source (Scott Oaks & Henry Wong, *Java
Threads*, O'Reilly 3rd ed. 2004, Executor / thread-pool material). No principle/claim layer at this
tier; not drift-tracked. Paraphrased — no verbatim quotation (`distillation-only` source).
