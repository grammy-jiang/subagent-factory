---
name: research-software-engineering-and-testing
kind: skill
status: ready
provenance:
  principles:
  - P005
  - P021
  - P034
  - P016
  claims:
  - C00035
  - C00036
  - C00037
  - C00038
  - C00164
  - C00165
  - C00166
  - C00167
  - C00169
  - C00247
  - C00248
  - C00249
  - C00250
  - C00251
  - C00252
  - C00253
  evidence: []
  source_anchors: []
  authored_from_digest: 3811287bdbb3f20ee268844dfeabc4ed5743bbe02239d9397bc8b180bf70a0d5
---

# Research Software Engineering And Testing

## Purpose

This skill guides treating research code — even a one-off analysis script — as software worth managing and testing. It checks for a Software Management Plan proportional to the software's stated purpose, a layered test suite (smoke, embedded runtime checks, unit, and slower system tests) with both positive and negative tests, unit tests that isolate the smallest parts and pin every fixed defect, and — for open hardware — modular, documented, discoverable, citable design.

## When to use

- Research software, including analysis scripts, needs a Software Management Plan proportional to its purpose.
- A test suite needs designing or reviewing across smoke, unit, and system layers with positive and negative tests on the important and breakage-prone paths.
- Code is being changed and unit tests in isolation would give confidence and pin a defect before it recurs.
- An open-hardware project needs modular, documented, discoverable, citable, and licensed design.

## Procedure

1. Manage research software with a Software Management Plan, a living document describing how the software is developed, documented, versioned, licensed, archived, and shared; treat even one-off analysis scripts as software, draft (P005).
2. Build a layered test suite with both positive tests (P021).
3. Unit-test the smallest testable parts in isolation (P034).
4. Build open hardware to be modular and extensible with documented interfaces so a community can grow around it, be honest with collaborators about the support they can expect, make the project discoverable with a common platform (P016).

## Inputs

- The research software or hardware project, its stated purpose and management plan, and its current tests.
- The reasoning offered for the decision under review: the goal, the plan or practice in place, and any claim of reproducibility or compliance made.

## Output

Per finding: name the gap and the principle it engages, give the correction, state the residual trade-off or the referral to make, and end with a concrete next step. Order findings highest-impact first. This skill advises on research-integrity and reproducibility practice; it does not run the study, produce the output, make an institutional misconduct finding, or give legal advice.

## Anti-patterns to flag

- Overlooking P005: Manage research software with a Software Management Plan, a living document describing how the software is developed, documented, versioned.
- Overlooking P021: Build a layered test suite with both positive tests.
- Overlooking P034: Unit-test the smallest testable parts in isolation.
- Overlooking P016: Build open hardware to be modular and extensible with documented interfaces so a community can grow around it, be honest with collaborators about.

## References

See `../../references/reproducibility-integrity-principles-index.md` for the full principle catalogue grouped by skill, and `../../references/reproducibility-integrity-evidence-notes.md` for how these principles are grounded and kept faithful to the sources.

## Provenance

Derived from P005, P021, P034, P016, grounded in the distillation-only sources (*The Turing Way*, a handbook for reproducible, ethical, and collaborative research; *On Being a Scientist*, a guide to responsible conduct in research; and a higher-education academic-norms guide). The frontmatter `provenance` block lists the exact principle and claim ids, which resolve into `principles/principles.yaml` and `analysis/claims.jsonl`.
