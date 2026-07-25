---
name: research-software-engineering-and-testing
kind: skill
status: ready
description: Software Management Plan for research code and one-off scripts, layered test suite (smoke/runtime/unit/system), positive and negative tests, unit tests in isolation, pinning a defect with a test, open-hardware modular/documented/discoverable/citable design
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

This skill guides treating research code — even a one-off analysis script — as software worth managing and testing. It checks for a Software Management Plan proportional to the software's stated purpose, a layered test suite (smoke, embedded runtime checks, unit, and slower system tests) with both positive and negative tests, unit tests that isolate the smallest parts and pin every fixed defect, and — for open hardware — modular, documented, discoverable, citable design. Open research hardware is deliberately in scope here, not a lens mismatch: this skill treats research artefacts broadly as managed, tested, shareable software, and the same discipline of managed development, documentation, and citability that governs a codebase governs an open-hardware design.

## When to use

- Research software, including analysis scripts, needs a Software Management Plan proportional to its purpose.
- A test suite needs designing or reviewing across smoke, unit, and system layers with positive and negative tests on the important and breakage-prone paths.
- Code is being changed and unit tests in isolation would give confidence and pin a defect before it recurs.
- An open-hardware project needs modular, documented, discoverable, citable, and licensed design.

## Procedure

1. Manage research software with a Software Management Plan — a living document describing how the software is developed, documented, versioned, licensed, archived, and shared; treat even one-off analysis scripts as software with a management level proportional to their stated purpose; draft the plan during the planning phase alongside the Data Management Plan and update it at major releases (P005).
2. Build a layered test suite with both positive tests (something works) and negative tests (something errors when it should): quick smoke tests that reject a broken build, runtime checks embedded in the program to catch edge cases early, unit tests of the smallest parts, and slower system or end-to-end tests that verify outward functionality (and performance, migration, stress, usability, and recovery); run the slower system tests only after the lower-level tests pass, and prioritise coverage on the most common, important, and breakage-prone paths (P021).
3. Unit-test the smallest testable parts in isolation, replacing dependencies with stubs or mocks, because unit tests give confidence when changing code, pinpoint bugs fast, and strongly incentivise modular, reusable code; keep unit tests independent of each other, aim to cover all paths including loop conditions, and whenever a defect is found write a test that exposes it before fixing so it cannot recur (P034).
4. Build open hardware to be modular and extensible with documented interfaces so a community can grow around it; be honest with collaborators about the support they can expect; make the project discoverable with a common platform and descriptive metadata; make it citable by archiving versions with a DOI for long-term reproducibility; and remember that without an open licence others cannot legally use it, and that hardware licensing is more complex than software licensing because patent law sometimes applies (P016).

## Inputs

- The research software or hardware project, its stated purpose and management plan, and its current tests.
- The reasoning offered for the decision under review: the goal, the plan or practice in place, and any claim of reproducibility or compliance made.

## Output

Per finding: name the gap and the principle it engages, give the correction, state the residual trade-off or the referral to make, and end with a concrete next step. Order findings highest-impact first. This skill advises on research-integrity and reproducibility practice; it does not run the study, produce the output, make an institutional misconduct finding, or give legal advice.

## Anti-patterns to flag

- The analysis is "just a script" — untested, unversioned, with no Software Management Plan and no stated purpose to size the management effort against; give it a plan proportional to its purpose, drafted alongside the Data Management Plan and updated at major releases (P005).
- The only tests are slow end-to-end runs (or there are no tests at all), with no fast smoke check to reject a broken build and no embedded runtime checks catching edge cases early, and every test only confirms the happy path with no negative test for an expected error; build the missing layers and add negative tests, prioritised on the most common and breakage-prone paths (P021).
- Changes to a function or module are validated only by running the whole system, with no isolated unit test exercising that part on its own, dependencies are real instead of stubbed or mocked, and a previously fixed bug has no test guarding against its return; add an isolated unit test and, for any fixed defect, a test that would have caught it before the fix (P034).
- An open-hardware design ships with no licence file (so no one can legally use it), no way to find or cite it (no common platform listing, no descriptive metadata, no versioned DOI archive), and undocumented interfaces that make it hard for anyone else to build on or extend, with no clarity on what support collaborators can expect; add the missing licence (noting hardware licensing is more complex than software due to patent law), documented interfaces, discoverable metadata, and a citable DOI-archived version (P016).

## References

See `../../references/reproducibility-integrity-principles-index.md` for the full principle catalogue grouped by skill, and `../../references/reproducibility-integrity-evidence-notes.md` for how these principles are grounded and kept faithful to the sources.

## Provenance

Derived from P005, P021, P034, P016, grounded in the distillation-only sources (*The Turing Way*, a handbook for reproducible, ethical, and collaborative research; *On Being a Scientist*, a guide to responsible conduct in research; and a higher-education academic-norms guide). The frontmatter `provenance` block lists the exact principle and claim ids, which resolve into `principles/principles.yaml` and `analysis/claims.jsonl`.
