# Changelog — k6-load-test-scripting-advisor

All notable changes to this subagent package are documented here.

## [0.4.0] — 2026-06-15

### Added

- Authored an `examples` block (A4 worked-example slot): one happy-path + one failure-recovery, grounded in the existing role / when_not_to_use / forbidden_behaviours (distillation-only paraphrase). Rendered into the adapter's `## Worked examples` section.

### Changed

- Bumped `agent_version` 0.3.0 → 0.4.0.

## [0.3.0] — 2026-06-12

### Changed
- SUPERSESSION re-author grounded to new Docling heading anchors. Prior conversion
  (k6-guideline-20260608232906, MarkItDown) produced 0 heading anchors; all field
  provenance was unanchored. Re-ingested as k6-guideline-20260612112658 with Docling,
  yielding 52 real heading anchors (h0000–h0063).
- All profile-field provenance in `provenance-ledger.md` re-anchored to real section
  headings from the new source_id.
- Interrogation re-run (Q1–Q18) with anchor-grounded evidence for every field.
- Tier set to `1`: atomic evidence-backed principles k6-p001–k6-p008 (derived from
  claims layer with full provenance chain) now ground `quality_bar`,
  `forbidden_behaviours`, `modes`, and `knowledge_partition.always_on`.
- `quality_bar` items cite principle IDs (k6-p001–k6-p007).
- `forbidden_behaviours` items cite source anchors and principle IDs.
- Mode triggers cite principle IDs with source-anchor evidence.
- `always_on` items updated to reference new source_id and heading anchors.
- Package status set back to `draft`; skill bodies will be re-authored in a later step
  to refresh anchor citations.

### Notes
- Role, display_name, when_to_use, when_not_to_use, skill names, and reference name
  are preserved verbatim so principles' operational_mapping remains valid.
- No patch-policy.yaml required: no produce or patch-suggest mode.
- Source rights remain `distillation-only`; no verbatim quotation.

## [0.2.0] — 2026-06-11

### Added
- Authored all 4 skill bodies (`k6-options-and-stages-configuration`, `k6-thresholds-and-checks`, `k6-scenarios-and-executors`, `k6-metrics-interpretation`) and the `k6-terminology-glossary` reference, grounded Tier 0 in the profile `always_on`/`when_to_use` rules and the source cheat sheet. No principle/claim layer (empty provenance arrays).

### Changed
- Promoted package from `status: draft` to `status: ready`; all stub markers removed.

### Notes
- `validate_skill_authoring`, `quote_scan`, and `stale --stamp` all clean. Source remains `distillation-only`; bodies are paraphrased with standard k6 API identifiers only — no verbatim quotation.

## [0.1.0] — 2026-06-09

### Added
- Initial generated package derived from the source "Most commonly used terms in K6" (Anshita Bhasin), classified `distillation-only`.
- `profile.yaml` with two source-justified modes: `advise` and `compare`.
- `provenance-ledger.md` mapping every profile field to its interrogation QID and source evidence.
- Golden tests: positive routing for `advise` and `compare`, one negative-routing test (cross-tool comparison, out of scope), and one missing-context test.
- Knowledge partition: 4 skill stubs and 1 reference stub (all `STATUS: STUB`).

### Notes
- Package remains `status: draft` until all skills and references are authored.
- Source PDF carries no license notice; rights set conservatively to `distillation-only` (no verbatim quotation).
