---
name: review-mutable-default-arguments
kind: skill
status: ready
provenance:
  principles:
  - P04
  claims:
  - C006
  evidence:
  - E006
  source_anchors:
  - luciano-ramalho-flue-ca307a52-c0920
  authored_from_digest: 9065909f74b6d45ec8ac94a6f3fa293f55d064261bcda661946296689fd0eefe
---

# Review mutable default arguments

## Purpose

Detect the mutable-default-argument defect — a list, dict, set, or other mutable used as a
parameter default — and recommend the `None`-sentinel fix. (P04)

## When to use

- A function or method signature uses a mutable value (`[]`, `{}`, `set()`, a mutable
  object) as a parameter default.

Do not flag a default that is immutable: `None`, a number, a string, a tuple, or a frozen
type are safe.

## Procedure

1. **Inspect every parameter default.** Flag any default that is a mutable object —
   `def f(x=[])`, `def g(opts={})`, and the like.
2. **State why it is a defect.** The default expression is evaluated once, when the
   function is defined, and the *same* object is reused on every call that omits the
   argument. Mutating it inside the body (appending, assigning keys) therefore leaks state
   into later calls, producing a hard-to-trace aliasing bug. (C006)
3. **Give the minimal fix.** Default the parameter to `None` and build the real object
   inside the body:

   ```python
   def f(x=None):
       if x is None:
           x = []
       ...
   ```

4. **Confirm scope.** Leave immutable defaults unchanged; the defect is specific to mutable
   default values.

## Inputs

- The function or method signatures under review and how each defaulted parameter is used
  inside the body.

## Output

A `review`/`patch-suggest` finding: the offending signature, a one-line explanation of the
shared-default aliasing bug, and the `None`-sentinel before/after, traced to P04. This is a
high-impact correctness defect — order it ahead of stylistic nits.

## References

- [pythonic-review-checklist](../../references/pythonic-review-checklist.md) — the
  mutable-default row.

## Provenance

Derived from principle **P04** (claim **C006**, evidence **E006**), grounded in the Fluent
Python worked aliasing example (anchor `luciano-ramalho-flue-ca307a52-c0920`).
Distillation-only source: paraphrased, no verbatim quotation.
