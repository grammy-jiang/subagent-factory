---
name: review-comprehension-style
kind: skill
status: ready
provenance:
  principles:
  - P06
  claims:
  - C007
  evidence:
  - E007
  source_anchors:
  - luciano-ramalho-flue-ca307a52-h0115
  authored_from_digest: 744c700da2e1801142f76b5301b3e205b7a1806d0f2705fad83f4018ae301570
---

# Review comprehension style

## Purpose

Steer sequence-building toward short, side-effect-free comprehensions and generator
expressions, and flag the two ways they are abused: growing too long, or being used only
for their side effects. (P06)

## When to use

- Code builds a list, dict, or set, uses `map`/`filter`, or runs a comprehension for its
  side effects.

Do not apply when an existing comprehension is short, pure, and already the most readable
form — leave it alone.

## Procedure

1. **Prefer the comprehension form for building.** Where a sequence is built with `map`,
   `filter`, or an accumulation loop, note that a short list/dict/set comprehension or a
   generator expression usually reads more clearly. (C007)
2. **Flag the over-long comprehension.** When a comprehension runs to more than a couple of
   lines (multiple `for`/`if` clauses, nested logic), recommend rewriting it as an ordinary
   loop or a named generator function, which is easier to read and debug.
3. **Flag the side-effect-only comprehension.** A comprehension written purely to run side
   effects (calling a function per item and discarding the result) should be a plain `for`
   loop — recommend the rewrite.
4. **Preserve the hedge.** Do not flag a comprehension that is already short, pure, and the
   most readable option; the rule is about abuse, not a ban.

## Inputs

- The Python code under review and which expressions build sequences or run per-item logic,
  with their length and whether they produce or only cause side effects.

## Output

A `review`/`compare` finding per issue: the comprehension or loop at fault, why it is less
readable (too long; side-effect-only) or why a comprehension would improve a `map`/`filter`
/loop, and the minimal rewrite, traced to P06 with the readability hedge preserved.

## References

- [pythonic-review-checklist](../../references/pythonic-review-checklist.md) — the
  comprehension-style row.

## Provenance

Derived from principle **P06** (claim **C007**, evidence **E007**), grounded in Fluent
Python's guidance on comprehension readability and abuse (anchor
`luciano-ramalho-flue-ca307a52-h0115`). Distillation-only source: paraphrased, no verbatim
quotation.
