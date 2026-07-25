# Changelog — pragmatic-programming-advisor

All notable changes to this generated subagent package are recorded here. Versions track
`agent_version` in `profile.yaml`.

## [0.3.1] — 2026-07-25

### Added
- `router_description` in `profile.yaml`: the adapter frontmatter `description` is the string the
  runtime routes on, and without this field the exporter composes it from the role plus only the
  first two `when_to_use` triggers and the first `when_not_to_use` exclusion — silently dropping the
  remaining domains. The authored description names the full remit and boundary. Adapter
  re-exported; no principle, rule, or skill changed.

## [0.3.0] — 2026-06-28

### Changed

- **Distilled layer rebuilt** via the per-book map → reduce pipeline: 381 globally-renumbered
  claims (`C#####`) and 78 promoted principles (`P001..P078`), replacing the original
  14-principle (`ppa-p001..ppa-p014`) hand-distilled layer.
- **Authored layer re-grounded** onto the rebuilt spine:
  - `profile.yaml` — all rule citations remapped to current `P###` ids (DRY → P040,
    orthogonality → P001, Law of Demeter → P015, tracer bullets → P025, prototypes → P004,
    refactoring → P024, broken windows → P039, ruthless testing → P041/P013/P014, estimation
    → P006, assertions → P045, wizard code → P076, no-best-tech → P052).
  - All 6 skills and all 5 references re-authored to cite real `P###`/`C#####` ids; every
    stale `ppa-*` token removed.
  - `tests/principle-behaviour-tests.yaml` regenerated — one test per principle P001..P078;
    every high-confidence principle is covered.
  - `tests/golden-tests.yaml` and `tests/behaviour-tests.yaml` regenerated against current ids.
  - `reports/faithfulness-report.yaml` re-run against `evidence-records.yaml` + `claims.jsonl`.

### Fixed

- `sources[].source_id` corrected from the legacy timestamp id
  (`andrew-hunt-david-th-20260611015103`) to the content-sha id (`andrew-hunt-david-th-13ff3ba5`),
  and the recorded `sha256` corrected to match `source-pack.manifest.yaml`.
- Added the previously-missing `provenance-ledger.md` and this `CHANGELOG.md`.

## [0.1.0] — 2026-06-11

- Initial hand-distilled package: 14 promoted principles authored from
  *The Pragmatic Programmer* (Hunt & Thomas, 1999). Superseded by 0.3.0.
