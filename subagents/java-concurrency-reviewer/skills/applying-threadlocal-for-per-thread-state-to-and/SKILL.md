---
name: applying-threadlocal-for-per-thread-state-to-and
kind: skill
status: ready
provenance:
  principles: []
  claims: []
  source_anchors: []
---

# Applying ThreadLocal for Per-Thread State

## Purpose

`ThreadLocal` gives each thread its own copy of a variable, so state that would otherwise be
shared and locked becomes confined to one thread — eliminating the contention and the race
entirely. This skill applies thread confinement via `ThreadLocal` where state is naturally
per-thread, and guards its two failure modes: leaks in pooled threads and accidental sharing of
the held object.

## When to use

- A field is mutable and shared only because it is convenient, not because threads must see each
  other's value (e.g. per-request context, a non-thread-safe formatter, a scratch buffer).
- Lock contention exists on state that each thread could own privately.
- A reviewer evaluates whether confinement can replace synchronization.

## Procedure

1. **Confirm the state is genuinely per-thread.** `ThreadLocal` fits when no thread needs another
   thread's value. If threads must coordinate on a shared value, confinement is wrong — keep the
   lock. Reusable-but-not-shareable objects (`SimpleDateFormat`, scratch buffers) are ideal.
2. **Give each thread its own value via `initialValue`/`withInitial`.** Override `initialValue()`
   (or use `ThreadLocal.withInitial(...)`) so each thread lazily gets its own instance; never seed
   one shared instance into a `ThreadLocal`, which defeats the purpose and reintroduces sharing.
3. **Do not leak the confined object outside the thread.** Returning or storing the per-thread
   instance where another thread can reach it breaks confinement and the safety guarantee. Keep it
   inside the owning thread's call stack.
4. **Remove the value in pooled threads.** In a thread pool, a thread is reused across tasks, so a
   `ThreadLocal` set in one task is still present in the next — a state-bleed and a memory leak.
   Call `remove()` in a `finally` block at the end of each unit of work so the value does not
   outlive the task.
5. **Prefer immutability or a method parameter when simpler.** If the value can simply be passed as
   a parameter or made immutable, that is clearer than a `ThreadLocal`; reserve `ThreadLocal` for
   cross-cutting per-thread context that is awkward to thread through call signatures.
6. **Verify the reduction in synchronization is real.** Confirm that confining the state actually
   removes the lock (no remaining shared access of the same data), otherwise the `ThreadLocal` adds
   complexity without the concurrency benefit.

## Inputs

- The shared field, whether any thread needs another's value, whether the code runs in a thread
  pool, and the object's reusability/immutability.

## Output

A confinement recommendation: whether `ThreadLocal` fits, the per-thread initialization, the
`remove()`-in-`finally` requirement for pooled threads, the no-leak rule, and confirmation that it
removes a real lock — or a verdict that the state must stay shared and synchronized.

## References

- `references/concurrency-pattern-taxonomy.md` — confinement / immutability among the safety
  patterns.
- `references/thread-api-quick-reference.md` — thread lifecycle context for pooled reuse.

## Provenance

Tier 0. Derived from the profile `knowledge_partition.skills` ThreadLocal entry (per-thread state
to eliminate sharing and reduce synchronization), the `always_on` immutability/confinement and
memory-model rules, and the `when_to_use` confinement design entry; synthesized against both
sources (Doug Lea, *Concurrent Programming in Java*, Addison-Wesley 1997, confinement material;
Scott Oaks & Henry Wong, *Java Threads*, O'Reilly 3rd ed. 2004, `ThreadLocal` material). No
principle/claim layer at this tier; not drift-tracked. Paraphrased — no verbatim quotation
(`distillation-only` sources).
