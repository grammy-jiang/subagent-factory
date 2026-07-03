# software-testing-advisor

A subagent that **advises on how to design tests and reviews existing tests**, grounded in four
canonical works:

- Gerard Meszaros, *xUnit Test Patterns* (Addison-Wesley, 2007) — test doubles, fixtures, smells.
- Mauricio Aniche, *Effective Software Testing* (Manning, 2022) — systematic case derivation.
- Paul Ammann & Jeff Offutt, *Introduction to Software Testing*, 2nd ed. (Cambridge, 2017) —
  coverage criteria and the RIPR model.
- Steve Freeman & Nat Pryce, *Growing Object-Oriented Software, Guided by Tests* (Addison-Wesley,
  2009) — mocking roles and end-to-end testing.

## What it does

Helps model the artifact under test and choose a coverage criterion, derive representative cases
systematically (partitions, boundaries, invalid inputs), pick and place the right test double
(dummy / stub / mock / spy / fake), and diagnose and repair test smells. It **advises and
reviews**; it does not write the developer's production or test code or pick a test framework.

## Modes

- **advise** — recommend a test design for the behaviour or code described.
- **review** — critique existing tests or a suite for smells, verification style, and coverage gaps.
- **compare** — contrast testing techniques (criteria, double kinds, combination strategies).

## When not to use

- The caller wants production or test code written, or a specific framework chosen/configured.
- The task has no unit- or integration-level test-design dimension.
- The caller wants red/green/refactor TDD-cycle coaching — hand off to a
  test-driven-development advisor.

## Package layout

- `profile.yaml` — canonical source of truth (role, modes, quality bar, forbidden behaviours).
- `principles/`, `analysis/`, `evidence/`, `sources/` — the distilled spine and its provenance.
- `skills/`, `references/` — file-backed knowledge the agent reads on demand.
- `tests/` — golden + principle-behaviour tests.
- `reports/faithfulness-report.yaml` — over-claim review of the profile rules.
- `adapters/claude-code/software-testing-advisor.md` — the exported runtime adapter.

Regenerate the adapter with `python -m tools.subagent_factory.cli export software-testing-advisor`
and validate with `python -m tools.subagent_factory.validate_generated_package
subagents/software-testing-advisor`.
