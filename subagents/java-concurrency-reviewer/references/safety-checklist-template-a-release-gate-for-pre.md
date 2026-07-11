---
name: safety-checklist-template-a-release-gate-for-pre
kind: reference
status: ready
provenance:
  principles: []
  claims: []
  source_anchors: []
---

# Concurrency Safety Checklist — Pre-Ship Release Gate

A release-gate checklist to run a concurrent class against before it ships. Each item names a
hazard category and the check that clears it. A finding must name the category (atomicity,
visibility, race, ordering, deadlock, lockout, livelock, starvation, priority inversion) and the
thread interaction that causes it — never a vague style concern.

## Safety (state correctness)

| # | Check | Hazard if it fails |
|---|-------|--------------------|
| S1 | Every access to shared mutable state occurs under the same lock (or the field is `volatile` for single-variable visibility) | Visibility gap |
| S2 | Compound operations (increment, check-then-act, multi-field updates) are atomic under one lock or a compare-and-set | Atomicity violation / race |
| S3 | `volatile` is used only for single-variable visibility, not for compound operations, array elements, or referenced-object fields | False safety |
| S4 | A fully synchronized object synchronizes **all** methods; no unsynchronized method touches the guarded state | Race through the back door |
| S5 | Immutable objects have all fields final and do not leak `this` during construction | Unsafe publication |
| S6 | Confined / `ThreadLocal` state never escapes its thread; pooled threads `remove()` it | Confinement breach / leak |

## wait/notify correctness

| # | Check | Hazard if it fails |
|---|-------|--------------------|
| W1 | `wait`/`notify`/`notifyAll` called only while holding the object's lock | `IllegalMonitorStateException` |
| W2 | `wait` is inside a `while`-condition loop, not an `if` | Spurious wakeup / stale condition |
| W3 | Every state change that could satisfy a waiter calls `notify`/`notifyAll` | Missed (lost) notification |
| W4 | `notify` vs. `notifyAll` is justified (single interchangeable condition → `notify`) | Wrong waiter woken |
| W5 | Timed waits use remaining-time arithmetic and give up at the deadline | Indefinite block |

## Liveness

| # | Check | Hazard if it fails |
|---|-------|--------------------|
| L1 | Methods acquiring 2+ locks use one global acquisition order (stable key, tie-break) | Deadlock (circular order) |
| L2 | No design is declared deadlock-free without tracing acquisition order across threads | Hidden deadlock |
| L3 | No lock is held across an outbound call to another object's blocking method (open call) | Nested-monitor lockout |
| L4 | Optimistic / retry loops are bounded with a fallback | Livelock |
| L5 | No thread can be indefinitely denied progress; fairness/confinement where needed | Starvation |

## Scheduling

| # | Check | Hazard if it fails |
|---|-------|--------------------|
| P1 | Correctness does not depend on thread priority or scheduling fairness | Non-portable, no JVM guarantee |
| P2 | A high-priority thread does not block on a lock held by a much lower-priority thread | Priority inversion |
| P3 | Scheduling findings distinguish JVM priority behavior from OS priority-mapping | Misdiagnosis |

## Lifecycle / cancellation

| # | Check | Hazard if it fails |
|---|-------|--------------------|
| C1 | No deprecated `Thread.stop`/`suspend`/`resume` | Inconsistent state / known races |
| C2 | Cancellation uses a `volatile` flag and/or `interrupt()`; run loop checks it | Unstoppable thread |
| C3 | `InterruptedException` is handled — exit cleanly or restore the flag, never swallowed | Lost cancellation |
| C4 | Executor pools are bounded and `shutdown()` on exit | Over-threading / hung JVM |

## Verdict

Pass only when every applicable item clears. A failed item becomes a finding tagged with its
hazard category, the field/method at risk, the thread interaction, and the pattern or technique
that addresses it.

## Provenance

Tier 0. Derived from the profile `quality_bar` (hazard-category naming, wait/notify verification,
`volatile` distinctions, deadlock resource-ordering, scheduling distinctions), `always_on` rules,
`forbidden_behaviours`, and `minimum_useful_output`; synthesized against both sources (Doug Lea,
*Concurrent Programming in Java*, Addison-Wesley 1997; Scott Oaks & Henry Wong, *Java Threads*,
O'Reilly 3rd ed. 2004). No principle/claim layer at this tier; not drift-tracked. Paraphrased — no
verbatim quotation (`distillation-only` sources).
