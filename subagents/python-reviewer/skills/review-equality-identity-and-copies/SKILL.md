---
name: review-equality-identity-and-copies
kind: skill
status: ready
provenance:
  principles:
  - P02
  - P03
  claims:
  - C003
  - C004
  evidence:
  - E003
  - E004
  source_anchors:
  - luciano-ramalho-flue-ca307a52-h0883
  - luciano-ramalho-flue-ca307a52-c0895
  authored_from_digest: 0fc51e5a2343d914bb26dfac461ead438be69986435d5e1a40b79f10262936c4
---

# Review equality, identity, and copies

## Purpose

Catch two related correctness pitfalls: confusing value equality (`==`) with object
identity (`is`), and assuming a shallow copy gives independent nested data. (P02, P03)

## When to use

- Code compares objects for equality or tests a variable against `None` or a sentinel.
- Code copies a container with `list(x)`, `x[:]`, or `copy.copy` and then mutates the copy
  (or the original) while expecting the two to be independent.

Do not apply when an identity comparison against a documented singleton is exactly what is
intended, or when every item in a copied container is immutable (sharing is then harmless).

## Procedure

1. **Scan `==` versus `is`.** `==` compares values (it dispatches to `__eq__`); `is`
   compares identity. Treat `==` as the default for value comparison.
2. **Flag misused `is`.** The one common correct use of `is` is testing against a singleton
   — chiefly `x is None`. Flag any other `is` comparison (e.g. `x is 0`, `s is "foo"`) and
   recommend `==`. Conversely, flag `== None` / `!= None` and recommend `is None` /
   `is not None`. (C003)
3. **Preserve the hedge.** Do not report `is` as a defect when it is a deliberate identity
   check against a documented singleton — that is its correct use. When the intent is
   unclear, default the recommendation to `==`.
4. **Scan copies of containers.** `list(x)`, the `x[:]` slice, and `copy.copy` duplicate
   the outer container but keep the *same* element references. For nested mutable elements
   (a list of lists, a dict of dicts), the copy and the original still share those inner
   objects. (C004)
5. **Flag shared-nested-state bugs.** Where a copy is later mutated and the nested mutable
   items must be independent of the original, recommend `copy.deepcopy` (or an explicit
   deep clone). If every item is immutable, leave the shallow copy alone — note that the
   exception applies and no change is needed.

## Inputs

- The Python code under review and which objects are expected to be equal-by-value versus
  the same object, and which copies are expected to be independent.

## Output

A `review`/`patch-suggest` finding per issue: the comparison or copy at fault, why it is
wrong (identity vs value; shared nested references), and the minimal fix (`is None`, `==`,
or `copy.deepcopy`), each traced to P02 or P03 with hedges preserved.

## References

- [pythonic-review-checklist](../../references/pythonic-review-checklist.md) — the
  `==`/`is` and shallow/deep-copy rows.

## Provenance

Derived from principles **P02** (claim **C003**, evidence **E003**) and **P03** (claim
**C004**, evidence **E004**), grounded in Fluent Python (anchors
`luciano-ramalho-flue-ca307a52-h0883`, `luciano-ramalho-flue-ca307a52-c0895`).
Distillation-only source: paraphrased, no verbatim quotation.
