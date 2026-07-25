# Changelog — ui-design-advisor

All notable changes to this generated subagent package are recorded here. The canonical source of
truth is `profile.yaml`; the installed adapter is a derived artifact.

## [0.1.1] — 2026-07-25

### Added
- `router_description` in `profile.yaml`: the adapter frontmatter `description` is the string the
  runtime routes on, and without this field the exporter composes it from the role plus only the
  first two `when_to_use` triggers and the first `when_not_to_use` exclusion — silently dropping the
  remaining domains and every sibling hand-off. The authored description names the full remit and boundary. Adapter
  re-exported; no principle, rule, or skill changed.

## [0.1.0] — 2026-07-03

### Added

- Authored the LLM layer over the deterministic map→reduce distilled spine (1597 claims, 671
  evidence records, 110 principles / 94 high-confidence, chunk anchors).
- `profile.yaml` — UI-design advisor role, when-to-use / when-not-to-use, three modes
  (review / advise / compare), five evidence-citing quality-bar checks, forbidden behaviours,
  handoff and source-of-truth policy, and a seven-group `knowledge_partition.always_on` covering the
  110 principles.
- `reports/faithfulness-report.yaml` — per-rule claim-strength findings; no profile rule is stronger
  than its principle evidence.
- Seven skills grounded in their principles, claims, evidence, and source anchors:
  `visual-hierarchy-and-layout`, `typography-color-and-visual-polish`, `form-and-input-design`,
  `navigation-and-information-structure`, `interaction-controls-and-feedback`,
  `goal-directed-design-and-research`, `posture-platform-and-mobile-context`.
- Two references: `references/ui-design-principles-index.md` (all 110 principles grouped by skill)
  and `references/ui-design-evidence-notes.md` (empirical thresholds and measurements — label
  placement, touch targets, response-time budgets — and their evidence base).
- `tests/principle-behaviour-tests.yaml` (one behaviour test per principle) and
  `tests/golden-tests.yaml` (routing + negative-routing + missing-context golden tests).

### Fixed

- Corrected the four source metadata records' `source_type` from the invalid `md` to `markdown`
  (schema enum) so the source-metadata validation passes; source content is unchanged.
