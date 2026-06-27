---
name: modularity-coupling-cohesion-review
kind: skill
status: ready
provenance:
  principles:
  - P025
  - P043
  - P042
  - P044
  claims:
  - C00626
  - C00633
  - C00402
  - C00403
  - C00374
  - C00375
  - C00411
  - C00416
  evidence:
  - E00148
  - E00149
  - E00088
  - E00089
  - E00081
  - E00082
  - E00093
  - E00094
  source_anchors:
  - 8afa2d6eafa0-c0004
  - 91e37e1ca511-c0002
  - 91e37e1ca511-c0001
  - 91e37e1ca511-c0003
  authored_from_digest: 3b9e03bd5731fa6258919cdc82a80df33dd9f6e96f296730f45b85cd2a42a08d
---

# Modularity: coupling and cohesion review

## Purpose

Judge how a system is partitioned by measurable properties, not taste. Modularity is a property
of a codebase that can be reasoned about with metrics: cohesion (how strongly the
responsibilities inside a module belong together) and coupling (how strongly modules depend on
one another). This skill reviews a decomposition for high cohesion and low coupling and explains
ripple-on-change problems in those terms.

## When to use

- Reviewing how a system is decomposed into modules, components, or services.
- A change ripples across many modules, suggesting a coupling or cohesion problem.
- The caller defends a partition by preference rather than by structural properties.

Do not invoke when the concern is runtime tuning with no bearing on module structure.

## Procedure

1. **Identify the modules and their responsibilities.** List the units under review and what each
   is supposed to own.
2. **Assess cohesion per module.** Ask whether the responsibilities inside each module belong
   together or whether the module is a grab-bag of unrelated concerns. Low cohesion (a module
   doing several unrelated jobs) is a partition smell.
3. **Assess coupling between modules.** Trace the dependencies between modules. Many or
   bidirectional dependencies between units that should be independent signal high coupling.
4. **Explain the ripple.** When one change forces edits across many modules, attribute it
   concretely to the coupling/cohesion finding rather than to "messy code."
5. **Prefer high cohesion, low coupling — as a direction, not an absolute.** Recommend moving
   responsibilities so each module is internally cohesive and externally loosely coupled, and
   note that the right level is context-dependent (over-splitting trades coupling for
   coordination cost).
6. **Make each finding actionable.** For every coupling/cohesion problem, name the module, the
   property violated, the consequence, and a concrete regrouping or boundary to introduce.

## Inputs

- The module/component/service decomposition under review and the dependencies between units.
- Optionally, a description of a change that rippled, to localize the coupling.

## Output

A findings list keyed to cohesion and coupling: which modules are low-cohesion or over-coupled,
the ripple consequence, and a concrete regrouping. Reasoning is grounded in the measurable
properties, not in preference.

## References

- [Laws of software architecture](../../references/laws-of-software-architecture.md) — modularity
  as a measurable property and the cohesion/coupling vocabulary.

## Provenance

Distilled from principle(s) **P017/P037/P036/P044**, claims **C00034/C00041/C01175/C01176/C01147/C01148**, evidence **E00011/E00012/E00215/E00216/E00208/E00209**, anchored in the cited architecture sources (`sources/anchors/`). Source is `distillation-only`: content is paraphrased, never quoted verbatim.
