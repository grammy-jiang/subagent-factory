---
name: coverage-criteria-subsumption
kind: reference
status: ready
provenance:
  principles:
  - P058
  - P082
  - P083
  - P100
  claims:
  - C00234
  - C00235
  - C00257
  - C00004
  - C00346
  source_anchors:
  - 140e06385751-c0000
  authored_from_digest: 0d9f12c240fbdbac905d9a41e579ac76efd8ab1af2717ff037decb559bce496e
---

# Coverage-criteria subsumption and the RIPR model

A reference for reasoning about the *strength* of coverage criteria and the fault-detection
conditions they do (and do not) assure. Use it with the `designing-coverage-criteria` skill.
Terminology follows Ammann & Offutt, *Introduction to Software Testing* (P083, P058).

## Subsumption (a criterion C1 subsumes C2 if every C1-adequate test set is also C2-adequate)

- **Edge Coverage subsumes Node Coverage** (but not vice versa).
- **Prime Path Coverage subsumes Edge-Pair Coverage** (without side-trips) and Edge/Node Coverage;
  prefer it for loop-bearing graphs because a prime path is a maximal simple path, keeping the
  number of test requirements manageable (P082, P083).
- **Complete Path Coverage** subsumes all graph criteria but is infeasible with loops.
- For logic: **Combinatorial (Multiple Condition) Coverage** subsumes the Active Clause Coverage
  family, which subsumes **Clause** and **Predicate (Decision)** Coverage. **General ACC does not
  subsume Predicate Coverage**; **Correlated ACC (CACC)** is the most practical flavour and does
  (P100).

Subsumption bounds *thoroughness*, not fault-detection: a stronger criterion generates more test
requirements but still guarantees no specific bug is found. Choose strength contextually (branch
coverage as a pragmatic default; condition/MC-DC for complex expressions).

## The RIPR model (why a passing suite can still miss a fault)

For a fault to cause an observable failure, four conditions must hold in order:

1. **Reachability** — the test reaches the faulty location.
2. **Infection** — execution corrupts the program state.
3. **Propagation** — the corrupted state reaches the output.
4. **Revealability** — the tester observes the wrong output.

By criterion family (P058):

| Criterion family | Assures |
|------------------|---------|
| Input-space (partitioning) | none of R/I/P/R by itself |
| Graph | reachability |
| Logic | reachability and infection |
| Syntax / mutation | reachability, infection, and (for strong mutation) propagation |

So a suite that is adequate for a weak criterion may reach a fault without infecting, or infect
without propagating — the coverage number overstates confidence. Always name the criterion *and*
the RIPR gap it leaves.

## Provenance

Distilled from Ammann & Offutt, *Introduction to Software Testing* (subsumption relationships, prime
paths, the ACC hierarchy, and the RIPR model). Principles P058, P082, P083, P100; claims C00234,
C00235, C00257, C00004, C00346; chunk anchor 140e06385751-c0000. Source is distillation-only — no
verbatim quotation; the tables are synthesized summaries.
