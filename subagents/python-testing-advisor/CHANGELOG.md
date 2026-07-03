# Changelog — Python Testing Advisor

All notable changes to this subagent are documented here.

## [0.3.0] — 2026-07-04

### Fixed

- Re-set source metadata `source_type` from the invalid `md` to the schema value
  `markdown` for all three ingested sources (the map→reduce rebuild had reintroduced
  the invalid value).
- Re-grounded the stale skills and references, whose principle citations had been
  scrambled by the rebuild's global principle renumbering (e.g. a fixture-scope skill
  step had come to cite a Docker/Ansible principle). `pytest-test-authoring`,
  `tdd-workflow`, `pytest-cli-and-config`, and `pytest-plugin-catalog` now cite the
  correct current principle ids, and their drift digests were re-stamped.

### Added

- Extended `tests/principle-behaviour-tests.yaml` to cover all 35 high-confidence
  principles (added behaviour tests for P001, P002, P014, P019, P025, P037, P042–P045,
  P062–P065, and P082–P085).
- Added the third governing source, *Testing In Python* (Gift & Deza,
  `testing-in-python-ro-8cdadfe3`), to the profile `sources[]` and source-of-truth
  policy, matching the rebuilt three-source spine.

### Changed

- Re-exported the Claude Code adapter so its must-hold invariant layer covers all 35
  high-confidence profile-rule principles.
- Bumped `agent_version` 0.2.0 → 0.3.0.

### Notes

- Distillation-only sources: no verbatim quotation. The distilled spine
  (claims / evidence / principles / anchors) was not modified.

## [0.2.0] — 2026-07-03

### Added

- Regenerated the LLM-authored layer to match the merged principles produced by
  the map→reduce build:
  - `profile.yaml` (portable-profile-v1, tier 2, status ready) with role, triggers,
    three read-only advisory modes (advise / review / tdd-guide), quality bar,
    forbidden behaviours, and handoff rules grounded in the package principles.
  - Two skills — `pytest-test-authoring`, `tdd-workflow`.
  - Two references — `pytest-cli-and-config`, `pytest-plugin-catalog`.
  - `reports/faithfulness-report.yaml` grading each gradable profile rule against the
    evidence.
  - `tests/golden-tests.yaml` (positive / negative-routing / missing-context) and
    `tests/principle-behaviour-tests.yaml` covering every high-confidence principle.
  - `provenance-ledger.md` and this changelog.

### Fixed

- Corrected `source_type` in both source metadata files from the invalid `md` to the
  schema value `markdown`.

### Sources

- Python Testing with pytest (Okken); Test-Driven Development with Python (Percival).

### Notes

- Distillation-only sources: no verbatim quotation. The distilled spine
  (claims / evidence / principles / anchors) was not modified.
