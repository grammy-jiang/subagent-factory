# Changelog — mockito-unit-testing-advisor

All notable changes to this subagent package are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [0.3.0] — 2026-06-15

### Added

- Authored an `examples` block (A4 worked-example slot): one happy-path + one failure-recovery, grounded in the existing role / when_not_to_use / forbidden_behaviours (distillation-only paraphrase). Rendered into the adapter's `## Worked examples` section.

### Changed

- Bumped `agent_version` 0.2.0 → 0.3.0.

## [0.2.0] — 2026-06-11

### Added

- Authored the six skill bodies (`test-double-selection`, `mock-initialisation`,
  `stub-query-methods`, `interaction-verification`, `mockito-limitations`,
  `spring-unit-isolation`) from PRP-001..PRP-007 and their cited claims, replacing the
  `STATUS: STUB` placeholders.

### Changed

- Promoted package `status: draft → ready` after skill-authoring validation, quote-scan,
  and drift-baseline stamping all passed.

---

## [0.1.0] — 2026-06-11

### Added

- Initial `profile.yaml` (portable-profile-v1, Tier 1) derived from
  `interrogation-records.yaml` Q1–Q18 and `principles/principles.yaml` (PRP-001–007).
- Four evidence-backed modes: `advise`, `produce`, `review`, `patch-suggest`.
- `policy/patch-policy.yaml` (patch-policy-v1, default_mode: patch_suggest_only)
  required by the patch-capable mode contract.
- `provenance-ledger.md` with full field-level distillation log, conflict log, and
  evidence-gap register.
- `tests/golden-tests.yaml` with four golden tests (GT-001 produce, GT-002 advise,
  GT-003 negative-routing, GT-004 review).
- `README.md` package overview.
- Six knowledge-partition skills named as operational_mapping targets in all seven
  principles: `test-double-selection`, `mock-initialisation`, `stub-query-methods`,
  `interaction-verification`, `mockito-limitations`, `spring-unit-isolation`.
- Quality bar and forbidden_behaviours grounded in PRP-001 through PRP-007.

### Source

- `mockito-for-spring-l-20260610164325` — Sujoy Acharya, *Mockito for Spring*,
  Packt Publishing, 2015. Rights: distillation-only (no explicit open-license notice).
