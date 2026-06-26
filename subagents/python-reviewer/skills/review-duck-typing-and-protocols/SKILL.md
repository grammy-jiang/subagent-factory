---
name: review-duck-typing-and-protocols
kind: skill
status: ready
provenance:
  principles:
  - P09
  claims:
  - C010
  evidence:
  - E010
  source_anchors:
  - python-distilled-pea-1baf485f-h0214
  authored_from_digest: 95f86014ef159c276d091c57357796870d415209f9032b302b03b008b5cdedaa
---

# Review duck typing and protocols

## Purpose

Favour duck typing: have code depend on the attributes and methods (the protocol) an
object provides, rather than on its concrete class or an explicit type check. (P09)

## When to use

- Code performs `isinstance`/`type(...)` checks that gate behaviour and could instead rely
  on the object simply supporting the required attributes or methods.

Do not apply when a genuine type guard is required for correctness, safety, or dispatch —
that is a legitimate use of an explicit check.

## Procedure

1. **Find class-based gating.** Locate `isinstance(x, C)` / `type(x) is C` checks that
   decide what the code does, and ask what the code actually needs from `x` — which
   methods or attributes it calls.
2. **Prefer the protocol.** Python resolves attributes by dynamic binding, so code works
   with any object that provides the needed attributes and methods regardless of its
   concrete type. Recommend depending on that protocol (call the method; optionally guard
   with `hasattr` or `try/except AttributeError`) instead of branching on the class. (C010)
3. **Respect genuine type guards.** Keep an explicit check where it is needed for
   correctness, safety, or to dispatch on truly distinct types — do not strip a guard that
   is doing real work.
4. **Frame as a preference, not an absolute.** This principle is medium-confidence; present
   it as "favour duck typing here" with the trade-off, not as a hard defect.

## Inputs

- The Python code under review, the `isinstance`/`type` checks it performs, and what
  behaviour each object actually needs to support.

## Output

A `review`/`advise` finding per issue: the type check, the protocol the code really
depends on, and the suggested protocol-based form — framed as a preference and traced to
P09, with genuine type guards left in place.

## References

- [pythonic-review-checklist](../../references/pythonic-review-checklist.md) — the
  duck-typing row.

## Provenance

Derived from principle **P09** (claim **C010**, evidence **E010**; medium confidence),
grounded in Python Distilled's account of dynamic binding / duck typing (anchor
`python-distilled-pea-1baf485f-h0214`). Distillation-only source: paraphrased, no verbatim
quotation.
