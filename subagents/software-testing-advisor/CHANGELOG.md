# Changelog — Software Testing Advisor

All notable changes to this subagent are documented here.

## [0.1.1] — 2026-07-25

### Added
- `router_description` in `profile.yaml`: the adapter frontmatter `description` is the string the
  runtime routes on, and without this field the exporter composes it from the role plus only the
  first two `when_to_use` triggers and the first `when_not_to_use` exclusion — silently dropping the
  remaining domains and every sibling hand-off. The authored description names the full remit and boundary. Adapter
  re-exported; no principle, rule, or skill changed.

## [0.1.0] — 2026-07-03

### Added

- Initial LLM-authored layer generated over the deterministically-assembled distilled spine
  (map→reduce build): `profile.yaml`, `provenance-ledger.md`, `reports/faithfulness-report.yaml`,
  four skills, two references, and the behaviour + golden test suites.
- Sources (Tier 2, four books): *xUnit Test Patterns* (Meszaros, 2007), *Effective Software
  Testing* (Aniche, 2022), *Introduction to Software Testing* (Ammann & Offutt, 2017), and
  *Growing Object-Oriented Software, Guided by Tests* (Freeman & Pryce, 2009).

### Profile

- Role: a testing advisor that guides test design and reviews existing tests across the four works.
- Modes: advise, review, compare.
- Skills: selecting-test-doubles, designing-coverage-criteria, deriving-test-cases-systematically,
  refactoring-test-smells.
- References: test-double-taxonomy, coverage-criteria-subsumption.

### Distilled spine (assembled deterministically — not edited in this layer)

- 100 principles (P001–P100; 79 high-confidence), over 2,847 claims (`C#####`) and the
  chunk-anchored evidence records for the four sources.

### Tests

- `tests/principle-behaviour-tests.yaml` covers every high-confidence principle (79 behaviour
  tests, one per principle).
- `tests/golden-tests.yaml` provides positive-routing, negative-routing, and missing-context tests.

### Notes

- `reports/faithfulness-report.yaml` grades the profile rules against the evidence and chunk
  anchors; no rule is stronger than its evidence.
- Sources are `distillation-only`; no verbatim quotation is shipped.
