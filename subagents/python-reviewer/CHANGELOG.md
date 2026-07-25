# Changelog — Python Code Reviewer

All notable changes to this generated subagent package are recorded here.

## [0.3.2] — 2026-07-25

### Added
- `router_description` in `profile.yaml`: the adapter frontmatter `description` is the string the
  runtime routes on, and without this field the exporter composes it from the role plus only the
  first two `when_to_use` triggers and the first `when_not_to_use` exclusion — silently dropping the
  remaining domains. The authored description names the full remit and boundary. Adapter
  re-exported; no principle, rule, or skill changed.

## 0.3.1 — 2026-06-27

### Changed

- Re-aligned the LLM-authored layer to the re-assembled distilled spine. The
  map→reduce build was re-run with full coverage and now carries 142 globally
  renumbered principles `P001`–`P142` (up from 60); claims, evidence records, and
  chunk anchors were re-assembled to match. No spine statement, `derived_from_claims`,
  confidence, evidence record, or anchor was edited by this step.
- Populated `operational_mapping` for the 75 principles the build carried without
  one (`profile_rule: false`, `skill`/`reference: null`, `test_cases: []`), so
  `principles.yaml` validates against `principles-v1`. The 28 must-hold principles
  (`confidence: high` + `profile_rule: true`) the build selected are unchanged.
- Regenerated `tests/principle-behaviour-tests.yaml` so every principle
  `P001`–`P142` has a behaviour test (all 126 high-confidence principles covered;
  no dangling `principle_id`).
- Re-exported the adapter, refreshing the must-hold invariant layer to the full
  28-principle set. Profile rules, skill/reference bodies, and the faithfulness
  report were not changed (still grounded; grounding unchanged).
- Bumped `agent_version` 0.3.0 → 0.3.1.

## 0.3.0 — 2026-06-26

### Changed

- Regenerated the LLM-authored layer to match the map→reduce-rebuilt distilled
  spine (60 globally-renumbered principles `P001`–`P060`, claims `C#####`,
  evidence `E#####`). The deterministic spine (claims, principles, evidence,
  chunk anchors) was not altered except to populate each principle's
  `operational_mapping` (skill / reference / profile_rule / test_cases).
- Re-pointed the source layer at this build's chunk-anchor ingestion: manifest,
  metadata, and `profile.sources[]` now carry `luciano-ramalho-flue-5c81071a`
  (Fluent Python) and `python-distilled-pea-2bf21990` (Python Distilled) with
  matching sha256; the prior paragraph-anchor ingestion (`…-ca307a52`,
  `…-1baf485f`) and its markdown/metadata/anchors/original were removed.
- Rewired all 10 skills and 2 references to the new principle / claim / evidence
  / chunk-anchor IDs and re-stamped `authored_from_digest`; bodies preserved.
- Regenerated `tests/principle-behaviour-tests.yaml` so every principle
  `P001`–`P060` has a behaviour test, and refreshed `golden-tests` coverage IDs.
- Regenerated `reports/faithfulness-report.yaml` against the new evidence,
  citing chunk anchors (`<sha12>-cNNNN`) only.
- Bumped `agent_version` 0.2.1 → 0.3.0 and re-exported the adapter.

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
