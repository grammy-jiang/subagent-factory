# Changelog — strengths-based-development-coach

All notable changes to this subagent package are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [0.4.0] — 2026-06-15

### Added

- Authored an `examples` block (A4 worked-example slot): one happy-path + one failure-recovery, grounded in the existing role / when_not_to_use / forbidden_behaviours (distillation-only paraphrase). Rendered into the adapter's `## Worked examples` section.

### Changed

- Bumped `agent_version` 0.3.0 → 0.4.0.

## [0.3.0] — 2026-06-11

### Added

- Authored all 5 skill bodies and 3 reference bodies (Step 8 author-skills),
  each grounded in this package's principles → claims → source:
  - `theme-interpretation-and-interaction-effects` (P-005, P-007).
  - `ideas-for-action-contextualisation` (P-001, P-004, P-006).
  - `team-strengths-grid-construction` (P-009, P-004).
  - `strength-based-action-plan-drafting` (P-001, P-003, P-004, P-005).
  - `manager-engagement-tactics-by-theme` (P-002, P-003).
  - `34-theme-reference-card` (P-005; theme essences paraphrased from Source 1).
  - `complementary-partnering-map` (P-004, P-009).
  - `engagement-statistics-reference` (P-002, P-003, P-008).
- Drift baseline stamped (`authored_from_digest`) into every authored doc.

### Changed

- Package promoted from `status: draft` to `status: ready`; all stubs filled.
- `agent_version` bumped from 0.2.0 to 0.3.0.
- Adapter re-exported from the promoted profile.

---

## [0.2.0] — 2026-06-11

### Added

- Second source ingested: Clifton StrengthsFinder (Gallup Press, July 2015 ed.,
  ISBN 978-1-59562-024-8; source_id strengthsfinder-20260611011808). The 2015
  edition corroborates all 34-theme definitions, Ideas for Action catalogues,
  and engagement statistics from the 2007 source with no conflicts detected.
- Package promoted to `tier: 2`; principles chain run against P-001..P-009.
- `quality_bar` items annotated with principle-ID citations (P-001, P-004,
  P-005, P-006, P-009) for Tier-2 selfcheck grounding.
- `forbidden_behaviours` items annotated with principle-ID citations (P-001,
  P-004, P-005, P-006, P-007, P-008).
- New `forbidden_behaviours` item: do not reproduce or paraphrase the Gallup
  Q12 engagement items, which are proprietary per Source 2's explicit trademark
  and copyright notice (P-008).
- Two new `always_on` knowledge items: (1) strengths-zone outcome data (6x
  engagement, 3x quality-of-life) corroborated by Source 2; (2) Q12 framing
  (engagement statistics citable; item wording not reproducible).
- Updated `source_of_truth_policy.canonical_owner` to reference both the 2007
  and 2015 Gallup editions as canonical references for theme definitions.
- Provenance ledger updated: Source 2 source-pack note, updated conflict log
  (no conflicts), and 0.2.0 version history entry added.

### Changed

- `agent_version` bumped from 0.1.0 to 0.2.0.

---

## [0.1.0] — 2026-06-09

### Added

- Initial profile derived from interrogation record against StrengthsFinder 2.0
  (Tom Rath, Gallup Press, 2007).
- Three supported modes: advise, produce, extract — each with source evidence
  from Q9 interrogation record.
- Five quality-bar checks anchored to Q7 quality marks.
- Six always-on knowledge items covering the 34-theme taxonomy, the strengths
  formula, the core investment principle, engagement statistics, lesser-talent
  management strategies, and blind-spot awareness.
- Five skills extracted from Q13: theme-interpretation-and-interaction-effects,
  ideas-for-action-contextualisation, team-strengths-grid-construction,
  strength-based-action-plan-drafting, manager-engagement-tactics-by-theme.
- Three reference artefacts extracted from Q14: 34-theme-reference-card,
  complementary-partnering-map, engagement-statistics-reference.
- Three golden tests including one negative routing test and one missing-context
  test.
- Provenance ledger with full distillation log, evidence-gap registry, and
  source-pack note recording distillation-only rights basis.
