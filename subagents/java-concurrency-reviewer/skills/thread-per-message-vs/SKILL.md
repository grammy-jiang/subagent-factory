---
name: thread-per-message-vs
kind: skill
status: ready
provenance:
  principles: []
  claims: []
  source_anchors: []
---

# Thread-per-Message vs. Worker-Thread-Pool Selection

## Purpose

Two structurally similar designs handle incoming work very differently: thread-per-message
spawns a fresh thread for each request, while a worker-thread pool reuses a fixed set of threads
fed by a queue. This skill selects between them by weighing latency against throughput and
accounting for the real cost of thread construction, so a design does not collapse under load or
add needless latency.

## When to use

- A thread-per-message, worker-thread, or producer-consumer design needs liveness and overhead
  assessment.
- A server or handler creates a `new Thread()` per request and the reviewer must judge whether it
  will exhaust resources under load.
- A team weighs spawning threads on demand against a bounded pool.

## Procedure

1. **Characterize the workload.** Estimate task arrival rate, task duration, and whether tasks
   block (I/O) or compute. Unbounded arrival with a per-message thread is the danger case.
2. **Account for thread-construction overhead.** Creating and tearing down a thread per task adds
   per-task cost and consumes a finite OS resource. For short or high-frequency tasks this
   overhead dominates and unbounded thread creation can exhaust memory or OS limits.
3. **Pick thread-per-message when latency matters and volume is bounded.** It starts work
   immediately with no queue wait and no shared-pool contention — good for low-rate, long-running,
   or latency-sensitive tasks where the construction cost is amortized over a long task.
4. **Pick a worker pool when throughput and stability matter.** A fixed pool caps concurrent
   threads, amortizes construction across many tasks, and back-pressures via its queue — good for
   high-rate, short tasks. The tradeoff is queueing latency when all workers are busy.
5. **Size the pool to the bottleneck.** For CPU-bound tasks, pool size near the core count avoids
   context-switch thrash; for I/O-bound tasks, a larger pool keeps cores busy while threads block.
   Bound the queue so overload is rejected or throttled rather than buffered until OOM.
6. **Do not assume scheduling fairness.** The JVM offers no fairness guarantee and OS scheduling
   varies; do not design either approach to depend on a particular thread being scheduled
   promptly.
7. **Prefer the Executor framework over hand-rolled threads on J2SE 5.0+.** `Executors` /
   `ThreadPoolExecutor` implement the worker-pool pattern with tested lifecycle and queue
   policies; recommend it instead of manual thread management where available.

## Inputs

- Task arrival rate, duration, and CPU-vs-I/O profile; latency vs. throughput priority; resource
  limits; and the Java version.

## Output

A recommendation of thread-per-message or worker-pool with the deciding factor named (latency vs.
throughput, construction overhead, overload behavior), a pool-sizing and queue-bounding suggestion
where a pool is chosen, and a pointer to the Executor framework on J2SE 5.0+.

## References

- `references/concurrency-overhead-taxonomy.md` — construction and context-switch overhead that
  drives the tradeoff.
- `references/executor-framework-taxonomy.md` — the pooled implementation to recommend.

## Provenance

Tier 0. Derived from the profile `when_to_use` thread-per-message / worker-thread entry, the
`knowledge_partition.skills` selection entry (latency vs. throughput, construction overhead), the
`always_on` Executor-framework rule, and the `forbidden_behaviours` no-fairness-guarantee rule;
synthesized against both sources (Doug Lea, *Concurrent Programming in Java*, Addison-Wesley 1997,
thread-per-message / worker-thread patterns; Scott Oaks & Henry Wong, *Java Threads*, O'Reilly 3rd
ed. 2004, thread overhead and pooling). No principle/claim layer at this tier; not drift-tracked.
Paraphrased — no verbatim quotation (`distillation-only` sources).
