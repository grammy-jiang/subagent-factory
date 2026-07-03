---
name: deriving-test-cases-systematically
kind: skill
status: ready
provenance:
  principles:
  - P070
  - P081
  - P086
  - P089
  - P090
  - P091
  - P092
  - P093
  claims:
  - C01587
  - C01590
  - C01591
  - C01691
  - C01700
  - C01707
  source_anchors:
  - 140e06385751-c0000
  - a8da44b134be-c0000
  authored_from_digest: ee2a174cfbc1aacd3e30081ceee396efc824ed90306eb6ce0eb1f4d7b7978498
---

# Deriving test cases systematically

## Purpose

Replace "test the examples I happen to remember" with a repeatable derivation of representative
cases from the specification and structure — partitions, boundaries, invalid inputs, combinations —
then close structural gaps. Grounds the advice in Aniche's *Effective Software Testing* and Ammann
& Offutt's input-space and syntax testing (P089, P091).

## When to use

- The developer is writing tests for a function/feature with a specification and several input
  ranges or conditions.
- Testing has been ad-hoc and the developer wants confidence the important cases are covered.
- Inputs can be malformed or hostile and the rejection paths need explicit tests (P086).

## Procedure

1. **Start specification-based (no source code needed).** Read the requirement and identify the
   inputs, outputs, and their relationships (P093).
2. **Partition inputs and outputs into equivalence classes** expected to produce different
   behaviour, including relationships among multiple inputs; keep one representative per partition
   (P091, P093).
3. **Add boundary cases.** For each meaningful boundary, test the on point and the nearest off
   point; for an equality boundary test both sides. Discard cases already covered by another
   partition (P092).
4. **Add invalid and malformed inputs deliberately.** Treat rejection of malformed input as its own
   requirement, and as stress/security testing — unhandled invalid input enables overflow and
   injection faults (P070, P086).
5. **Choose a combination strategy by cost and strength** when several parameters interact: All
   Combinations is exponential and usually impractical, Each Choice is cheapest, and Pair-Wise /
   T-Wise sit between — pick per the interaction risk (P081).
6. **Then use structural testing to reveal what the spec-based set missed** — run coverage, inspect
   uncovered or partially covered branches, and consciously decide whether to add cases (P089,
   P090). Engineer the final set from requirements, boundaries, corner cases, invalid inputs, and
   structural gaps rather than remembered examples (P089).

## Inputs

- The specification/requirement, the input and output domains and their relationships, and any
  known invalid-input or security concerns.

## Output

A derived set of test cases grouped by partition, boundary, invalid-input, and combination, with
the structural gaps the developer should still close and the rationale for each.

## References

- `references/coverage-criteria-subsumption.md` — structural-coverage strength for the closing step.

## Provenance

Distilled from Aniche, *Effective Software Testing* (specification-based testing, partitions,
boundaries, structural follow-up) and Ammann & Offutt (input-space partitioning, combination
strategies, syntax/mutation and malformed-input testing). Principles P070, P081, P086, P089, P090,
P091, P092, P093; claims C01587, C01590, C01591, C01691, C01700, C01707; chunk anchors
140e06385751-c0000, a8da44b134be-c0000. Source is distillation-only — no verbatim quotation.
