---
name: refactoring-test-smells
kind: skill
status: ready
provenance:
  principles:
  - P002
  - P010
  - P011
  - P016
  - P022
  - P028
  - P036
  - P062
  claims:
  - C00550
  - C00566
  - C00586
  - C00561
  - C00640
  - C00607
  - C00558
  - C00563
  source_anchors:
  - 11f28a2119c7-c0000
  authored_from_digest: 568c700524157b5bafe394418d5a1831a5fd67c0823b13da24027d4986a35d6e
---

# Diagnosing and refactoring test smells

## Purpose

Review a test or suite by classifying each smell by its failure mode and applying a targeted,
pattern-level repair — not a symptom patch — while keeping tests self-checking, isolated,
one-condition-focused, and clearly named. Grounds the advice in Meszaros's *xUnit Test Patterns*
smell catalogue and four-phase test structure (P022, P016).

## When to use

- A suite is hard to read, brittle, slow, or flaky, or tests interfere with one another.
- A review finds giant shared fixtures, multi-assertion tests, conditional logic in tests, or
  unclear names.
- The developer wants to know *which* repair pattern fits an observed problem.

## Procedure

1. **Classify the smell by its failure mode**, not its surface symptom — for example Obscure Test,
   Eager Test, Conditional Test Logic, Fragile/Interacting Tests, or Slow Tests — and reach for the
   pattern-level repair the smell maps to (P022).
2. **Restore the four-phase structure**: setup, exercise, verification, teardown, in that order, so
   a reader can see what is arranged, what is exercised, and what is checked (P016).
3. **Fix fixtures for isolation and cohesion**: prefer specific, cohesive fixtures each test fully
   uses over a large shared fixture that forces filtering; prefer fresh fixtures for independent
   tests and introduce a shared fixture only for a measured setup cost, isolating mutable state
   (P002, P011).
4. **Extract intent-revealing helpers** (creation/finder methods, custom assertions) to cut
   repetitive setup and noise — but only when they reduce duplication without hiding the test's
   intent (P010).
5. **Split multi-condition tests** so each test exercises one condition and one path, localizing
   the failure (P036); make every test self-checking so a clean run needs no human interpretation
   (P028).
6. **Name tests systematically** so the package, class, and method reveal the SUT, the scenario,
   and the expected outcome (P062).
7. **State the failure each repair prevents** (flaky ordering, false green, unreadable failure).

## Inputs

- The test(s) or suite under review (or their described symptoms), and the behaviour they target.

## Output

A per-smell critique: the smell classified by failure mode, the targeted repair pattern, and the
resulting improvement in isolation, readability, or diagnosability — with specific corrections.

## References

- `references/test-double-taxonomy.md` — for smells rooted in over- or mis-used doubles.

## Provenance

Distilled from Meszaros, *xUnit Test Patterns* (test-smell catalogue and failure-mode
classification, four-phase test, fresh vs shared fixtures, custom assertions, self-checking tests,
test naming). Principles P002, P010, P011, P016, P022, P028, P036, P062; claims C00550, C00566,
C00586, C00561, C00640, C00607, C00558, C00563; chunk anchor 11f28a2119c7-c0000. Source is
distillation-only — no verbatim quotation.
