---
name: diagnosing-priority-inversion
kind: skill
status: ready
provenance:
  principles: []
  claims: []
  source_anchors: []
---

# Diagnosing Priority Inversion

## Purpose

Priority inversion occurs when a high-priority thread blocks waiting on a lock held by a
low-priority thread, while a middle-priority thread keeps preempting the low-priority holder — so
the high-priority thread is effectively stalled by lower-priority work. This skill identifies that
pattern in Java code and evaluates whether a fair-mode locking strategy or design change resolves
it, while keeping platform-scheduling caveats explicit.

## When to use

- Code sets thread priorities and a high-priority thread shares a lock with a lower-priority one.
- A latency-sensitive thread misses deadlines and the suspect is a lock held by background work.
- A reviewer must separate a real priority-inversion from ordinary contention or a JVM/OS priority
  mismatch.

## Procedure

1. **Map priorities to shared locks.** List threads, their assigned priorities, and the locks they
   contend. Inversion needs a high-priority thread that blocks on a lock a lower-priority thread
   holds.
2. **Confirm the inversion shape.** The hazard is: high-priority thread H waits for lock L; L is
   held by low-priority thread Lo; a medium-priority thread M (not needing L) preempts Lo so Lo
   cannot run to release L. H is now blocked by M, an unrelated lower-priority thread. Name H, Lo,
   M, and L explicitly.
3. **Separate the scheduling concerns.** Distinguish (a) genuine priority inversion, (b) JVM
   priority behavior — the JVM requires preemptive priority-based scheduling with 11 developer
   levels, but (c) OS priority mapping varies by platform, so assigned priorities may not behave as
   written. Do not diagnose inversion when the real cause is an OS that collapses or ignores Java
   priorities.
4. **Do not invent scheduling guarantees.** The JVM offers no fairness guarantee and platform
   scheduling varies; never assert a priority assignment will be honored uniformly across systems.
   Note portability implications in the finding.
5. **Evaluate remedies.** Options: shorten the low-priority thread's hold time (reduce lock scope);
   avoid sharing the lock across wide priority gaps (confinement, immutability, or a copy); or use
   a fair-mode lock (`ReentrantLock(true)` on J2SE 5.0+) so waiters are served in order. Assess
   whether fair mode actually resolves this case — fairness orders waiters but does not by itself
   implement priority inheritance, so it helps starvation more than classic inversion.
6. **Recommend the minimal effective change.** Prefer eliminating the shared lock or its hold time
   over relying on priority tuning, since priority behavior is platform-dependent.

## Inputs

- The threads, their priorities, the shared locks and who holds them, the latency requirement, and
  the target platform(s).

## Output

A priority-inversion verdict naming H/Lo/M/L and the lock, a clear separation of true inversion
from JVM-vs-OS priority-mapping effects, the portability caveat, and a ranked remedy (reduce hold
time / don't share the lock / fair-mode lock) with an assessment of whether fair mode resolves
this specific case.

## References

- `references/thread-scheduling-overview.md` — JVM priority levels, preemption, OS mapping,
  inversion scenario.
- `references/safety-checklist-template-a-release-gate-for-pre.md` — the scheduling/liveness line.

## Provenance

Tier 0. Derived from the profile `knowledge_partition.skills` priority-inversion entry, the
`always_on` thread-priority-model rule (11 levels, OS mapping varies, inversion definition), the
`quality_bar` requirement to distinguish JVM priority, OS mismatch, and inversion, and the
`forbidden_behaviours` no-fairness-guarantee rule; synthesized against the source (Scott Oaks &
Henry Wong, *Java Threads*, O'Reilly 3rd ed. 2004, scheduling / priority material). No
principle/claim layer at this tier; not drift-tracked. Paraphrased — no verbatim quotation
(`distillation-only` source).
