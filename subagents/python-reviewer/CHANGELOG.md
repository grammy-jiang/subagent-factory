# Changelog — Python Code Reviewer

All notable changes to this generated subagent package are recorded here.

## 0.2.1 — 2026-06-26

### Changed

- Renamed subagent slug `python-code-reviewer` → `python-reviewer` (canonical
  package dir, all source-of-truth artifacts, and the installed Claude Code
  adapter). Historical/dated factory records keep the prior name.
- Re-validated and re-exported under the refactored factory tooling (`ee1937a`
  batched changes + the cli/validator/converter refactor series). No behavioural
  change to principles, profile rules, or evidence.

## 0.2.0 — 2026-06-20

### Added

- Authored the bodies of all ten skills (`skills/<name>/SKILL.md`) and both
  references (`references/<name>.md`), each grounded in this package's own
  principles / claims / evidence / source anchors — no invention, no verbatim
  quotation (`distillation-only` sources). Stub markers removed.
- Drift baseline stamped (`provenance.authored_from_digest`) into every authored
  doc via `cli stale --stamp`.

### Changed

- Promoted package from `status: draft` to `status: ready`; bumped
  `agent_version` 0.1.0 → 0.2.0.
- Re-exported the Claude Code adapter from the updated profile.

### Notes

- `validate_skill_authoring`: all 10 skills + 2 references authored (0 stub).
- `quote_scan`: PASS (no verbatim quotation). Faithfulness unchanged — profile
  rules/principles were not modified, only skill/reference bodies authored.

## 0.1.0 — 2026-06-20

### Added

- Initial multi-source generation (Tier 2) from two canonical Python references:
  - *Fluent Python*, 2nd ed. (Luciano Ramalho, 2022) — `distillation-only`
  - *Python Distilled* (David M. Beazley, 2021) — `distillation-only`
- `profile.yaml`: a Python code reviewer with five modes (`review`, `advise`,
  `compare`, `validate`, `patch-suggest`), grounded in 15 operational principles.
- Evidence chain: 18 source-anchored claims (`analysis/claims.jsonl`),
  importance scores (all 18 `keep`), 18 evidence records
  (`evidence/evidence-records.yaml`), and 15 principles
  (`principles/principles.yaml`).
- Tests: `tests/golden-tests.yaml` (3 golden, 2 negative-routing, 1
  missing-context) and `tests/principle-behaviour-tests.yaml` (one per principle).
- `policy/patch-policy.yaml` (`patch_suggest_only`) for the patch-suggest mode.
- `reports/faithfulness-report.yaml`: every profile rule checked against the
  evidence records; no `CONTRADICTED` findings.
- Ten skill stubs and two reference stubs (`STATUS: STUB`).

### Notes

- Package is `status: draft`. Skill and reference bodies are stubs; run Step 8.7
  (author skills) to author them and promote to `status: ready`.
- Both sources are `distillation-only`; no verbatim quotation appears in any
  artifact (`quote_allowed: false` throughout).
