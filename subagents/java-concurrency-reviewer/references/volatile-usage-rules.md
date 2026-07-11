---
name: volatile-usage-rules
kind: reference
status: ready
provenance:
  principles: []
  claims: []
  source_anchors: []
---

# Volatile Usage Rules

A decision table for when `volatile` is sufficient and when it is not. `volatile` provides
visibility and ordering for a **single variable** — it never provides atomicity for a compound
operation. Use this to validate or reject every `volatile` field in review.

## Rule table

| Scenario | `volatile` sufficient? | Why |
|----------|------------------------|-----|
| Single read or single write of one field, visible across threads | **Yes** | Forces load/store to main memory; establishes happens-before on that variable |
| Stop / status flag polled in a loop | **Yes** | Single-variable visibility is exactly what a flag needs |
| Set-once / monotonic reference (with safe publication) | **Yes** (J2SE 5.0+) | Field transitions once; `volatile` gives the ordering double-checked locking needs |
| Increment / decrement (`count++`) | **No** | Read-modify-write is three steps; two threads can interleave and lose an update |
| Check-then-act (`if (x == null) x = ...`) | **No** | The gap between check and act is a race; needs a lock or compare-and-set |
| Compound invariant across two fields | **No** | `volatile` is per-variable; cannot make two writes atomic together |
| Element of a `volatile` array | **No** | The reference is volatile, the **elements** are not |
| Field of an object held via a `volatile` reference | **No** | Only the reference is volatile; the referenced object's fields are not |

## Replacement when `volatile` is insufficient

| Need | Use |
|------|-----|
| Atomic increment / accumulate | `AtomicInteger` / `AtomicLong` (J2SE 5.0+) |
| Atomic compare-and-set on a reference | `AtomicReference` (+ `AtomicStampedReference` for ABA) |
| Atomic update of array elements | `AtomicIntegerArray` / `AtomicReferenceArray` |
| Multi-field invariant | `synchronized` block / explicit `Lock` |

## Review checklist

1. Is the field read/written as a single operation, or part of a compound one? Compound → reject
   `volatile`.
2. Is it an array element or a referenced object's field? Then `volatile` on the reference does not
   cover it.
3. Is it a set-once value relying on `volatile` for double-checked locking? Confirm J2SE 5.0+ and
   that it is truly write-once.

## Provenance

Tier 0. Derived from the profile `knowledge_partition.references` volatile entry, the `always_on`
`volatile`-semantics rule (single-variable visibility; no atomicity for compound operations; not
array elements or referenced objects), and the `quality_bar`/`forbidden_behaviours` constraints that
`volatile` is not a substitute for `synchronized` on compound operations; synthesized against the
source (Doug Lea, *Concurrent Programming in Java*, Addison-Wesley 1997, memory-model material) with
the `java.util.concurrent.atomic` replacements noted. No principle/claim layer at this tier; not
drift-tracked. Paraphrased — no verbatim quotation (`distillation-only` source).
