# Changelog — xv6-kernel-internals-reviewer

All notable changes to this generated subagent package are recorded here.

## [0.4.0] — 2026-06-15

### Added

- Authored an `examples` block (A4 worked-example slot): one happy-path + one failure-recovery, grounded in the existing role / when_not_to_use / forbidden_behaviours (distillation-only paraphrase). Rendered into the adapter's `## Worked examples` section.

### Changed

- Bumped `agent_version` 0.3.0 → 0.4.0.

## [0.3.0] — 2026-06-13

### Changed
- Re-authored from Docling re-conversion; rules re-grounded to real heading
  anchors via principles pr-001..pr-012.
- Set `tier: 1` (previously absent).
- `quality_bar`, `always_on`, and `forbidden_behaviours` each cite specific
  principle IDs (pr-001..pr-012) derived from 71 claims and 30 evidence records.
- `source_id` updated to `a-simple-unix-like-t-20260613000613` (Docling
  conversion; 126 headings recovered vs. 0 from prior markitdown run).
- Mode outputs updated to reference applicable principles.
- `minimum_useful_output` updated to include principle citation requirement.

### Unchanged
- Role, when_to_use, when_not_to_use, modes (advise/review/compare), skills,
  and references are identical to 0.2.0.
- `status: ready` retained.

## [0.2.0] — 2026-06-11

### Added
- Authored all 3 skill bodies (`kernel-concurrency-review`,
  `address-space-and-trap-walkthrough`, `filesystem-crash-recovery-review`) and
  2 reference bodies (`xv6-subsystem-map`, `real-world-os-comparisons`) from the
  source commentary (Tier 0: grounded in profile `always_on`/`quality_bar` and the
  named source chapters; no principle/claim layer).

### Changed
- Package `status: draft` → `ready` (all stubs filled; skill-authoring validation,
  quote scan, and package validation pass).

## [0.1.0] — 2026-06-09

### Added
- Initial profile derived from *xv6: a simple, Unix-like teaching operating
  system* (Cox, Kaashoek, Morris, 2019).
- Modes: `advise`, `review`, `compare` (each justified by source evidence in the
  provenance ledger mode decision log).
- Knowledge partition: 3 skill stubs (`kernel-concurrency-review`,
  `address-space-and-trap-walkthrough`, `filesystem-crash-recovery-review`) and
  2 reference stubs (`xv6-subsystem-map`, `real-world-os-comparisons`).
- Phase 2.5 importance ranking: 7 subsystem units kept, exercises unit discarded.
- Golden tests: 3 positive routing, 1 negative routing, 1 missing-context.

### Notes
- Rights status `distillation-only` (authored work, no explicit license notice —
  conservative floor; no verbatim quotation).
- Package `status: draft` until all skills and references are authored.
