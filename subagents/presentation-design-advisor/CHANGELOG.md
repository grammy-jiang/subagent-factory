# Changelog — presentation-design-advisor

All notable changes to this generated subagent package are recorded here. Versions follow the
`agent_version` field in `profile.yaml`.

## [1.0.0] — 2026-07-26

### Added
- Initial release of the **presentation-design-advisor** subagent (Tier 2), authoring the LLM layer over the
  already-assembled, deterministically-valid distilled spine (120 principles
  P001-P120 / 1359 claims from three distillation-only sources).
- `profile.yaml` derived from the 120 promoted principles: role, when/when-not-to-use, three
  modes (advise / review / plan), quality bar, forbidden behaviours, handoff rules, and a
  13-skill / 2-reference `knowledge_partition` covering every principle exactly
  once.
- 13 authored skills partitioning all 120 principles; 2 references
  (principles index + evidence notes).
- `reports/faithfulness-report.yaml` — every load-bearing profile rule graded WITHIN_SCOPE against
  its principles (no rule stronger than its evidence; the sources' own hedging on rehearsal
  guarantees, delivery style, and the measured comprehension gain is carried through).
- `tests/golden-tests.yaml` (7 golden, 3 negative-routing,
  2 missing-context) and `tests/principle-behaviour-tests.yaml` (one behaviour test per
  principle, 120 total).
- Claude Code adapter exported to `adapters/claude-code/` and installed under
  `.claude/agents/generated/`.

### Fixed
- `sources/metadata/*.metadata.json`: `source_type` normalised from the map->reduce short form
  `md` to the schema enum value `markdown`.

### Grounding
- Three distillation-only sources: *The Craft of Scientific Presentations* (Alley, 2013);
  *Resonate* (Duarte, 2010); and *slide:ology* (Duarte, 2008).
