---
name: thread-scheduling-overview
kind: reference
status: ready
provenance:
  principles: []
  claims: []
  source_anchors: []
---

# Thread Scheduling Overview

A reference for the scheduling and priority semantics the reviewer reasons about — what the JVM
guarantees, what is platform-dependent, and the priority-inversion scenario — so scheduling findings
separate the layer that is portable from the layer that is not.

## Priority model

| Aspect | Behavior | Portability |
|--------|----------|-------------|
| Priority levels | 10 priorities available to developers (`MIN_PRIORITY` 1 … `NORM_PRIORITY` 5 … `MAX_PRIORITY` 10) | JVM-level; values are portable |
| Scheduling discipline | JVM requires preemptive, priority-based scheduling: a runnable higher-priority thread preempts a lower one | JVM-required, but realized via the OS |
| OS priority mapping | Java priorities are mapped onto OS priorities, which differ per platform (number of levels, semantics) | **Platform-dependent** — same priorities behave differently across OSes |
| Time-slicing | Whether equal-priority threads are time-sliced is not guaranteed by the JVM; depends on the OS | **Platform-dependent** |
| Fairness | No fairness guarantee; no promise a given thread is scheduled promptly | **Not guaranteed** |

## Preemption rules of thumb

- A higher-priority runnable thread generally runs in preference to a lower-priority one.
- Equal-priority threads may or may not be time-sliced — do not depend on rotation.
- Do not design correctness around priorities; use them only as hints. Liveness must hold even if
  priorities are flattened by the OS.

## Priority-inversion scenario

| Element | Role |
|---------|------|
| H (high priority) | Blocks waiting on lock **L** |
| Lo (low priority) | Holds lock **L**, needs CPU to release it |
| M (medium priority) | Does not need **L**, but preempts **Lo** |

Result: M (lower than H) indirectly blocks H by starving Lo of the CPU it needs to release L. H is
inverted below M.

Remedies, in preference order:

1. Reduce Lo's hold time on L (shrink the critical section).
2. Do not share L across a wide priority gap (confinement, immutability, copy).
3. Use a fair-mode lock (`ReentrantLock(true)`, J2SE 5.0+) — orders waiters, helps starvation, but
   is not full priority inheritance.

## Caveats the reviewer must state

- Java program priority settings are in scope; OS-level scheduler tuning is **not** — platform
  scheduling is implementation-dependent.
- Never assert a synchronization or fairness guarantee beyond the Java memory model.

## Provenance

Tier 0. Derived from the profile `knowledge_partition.references` scheduling entry, the `always_on`
thread-priority-model rule (levels, OS mapping varies, inversion definition), the `quality_bar`
requirement to distinguish JVM priority, OS mismatch, and inversion, the `forbidden_behaviours`
no-fairness-guarantee rule, and the `when_not_to_use` OS-tuning exclusion; synthesized against the
source (Scott Oaks & Henry Wong, *Java Threads*, O'Reilly 3rd ed. 2004, scheduling material). No
principle/claim layer at this tier; not drift-tracked. Paraphrased — no verbatim quotation
(`distillation-only` source).
