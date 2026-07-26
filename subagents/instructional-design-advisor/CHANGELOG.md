# Changelog — instructional-design-advisor

All notable changes to this generated subagent package are recorded here. Versions follow the
`agent_version` field in `profile.yaml`.

## [1.1.0] — 2026-07-26

### Added
- *Instructional-Design Theories and Models: A New Paradigm of Instructional Theory / In Action*
  (Reigeluth, ed.) folded in as an eleventh source, adding instructional-theory selection
  (prescribe a method together with the situation it fits) and elaboration sequencing (the
  epitome -> elaborate -> synthesize zoom-lens cycle).

### Changed
- *Multimedia Learning* (Mayer) re-ingested from the full text, replacing the partial conversion
  (`mayer-multimedia-lea-f516bca0` -> `mayer-multimedia-lea-40e2757d`); the multimedia principles no
  longer lean on *e-Learning and the Science of Instruction* to cover Mayer's own material.
- Distilled spine rebuilt over the eleven sources: 200 principles (was 180) over
  7860 claims (was 6851). The rebuild renumbered every principle.
- LLM-authored layer fully re-derived against the new P001-P200 numbering — the
  13-skill partition, `profile.yaml` (quality bar, forbidden behaviours, handoff rules,
  precedence, examples, `knowledge_partition.always_on`), `reports/faithfulness-report.yaml`, all
  13 skills, both references, `tests/golden-tests.yaml`, and
  `tests/principle-behaviour-tests.yaml` (200 tests, one per principle). The 1.0.0 principle
  ids do not carry over.
- Claude Code adapter re-exported to `adapters/claude-code/` and reinstalled under
  `.claude/agents/generated/`.

### Fixed
- `sources/metadata/*.metadata.json`: `source_type` written as `md` by the rebuild, which is not a
  member of the `source-metadata-v1` enum; normalised back to `markdown`.

## [1.0.0] — 2026-07-26

### Added
- Initial release of the **instructional-design-advisor** subagent (Tier 2), authoring the LLM layer over the
  already-assembled, deterministically-valid distilled spine (180 principles / 6851 claims from ten
  distillation-only sources).
- `profile.yaml` derived from the promoted principles: role, router description,
  when/when-not-to-use, three modes (advise / review / plan), quality bar, forbidden behaviours,
  handoff rules, and a 13-skill / 2-reference `knowledge_partition` covering
  every principle exactly once.
- 13 authored skills; 2 references (principles index + evidence notes).
- `reports/faithfulness-report.yaml` — every load-bearing profile rule graded WITHIN_SCOPE against
  its principles (no rule stronger than its evidence).
- `tests/golden-tests.yaml` and `tests/principle-behaviour-tests.yaml`.
- Claude Code adapter exported to `adapters/claude-code/` and installed under
  `.claude/agents/generated/`.

### Grounding
- Eleven distillation-only sources: *Understanding by Design* (Wiggins & McTighe, 2005); *Teaching
  for Quality Learning at University* (Biggs & Tang, 2011); *Creating Significant Learning
  Experiences* (Fink, 2013); *A Taxonomy for Learning, Teaching, and Assessing* (Anderson &
  Krathwohl, 2001); *Principles of Instructional Design* (Gagné, Briggs & Wager, 1992); *First
  Principles of Instruction* (Merrill, 2002); *The Systematic Design of Instruction* (Dick, Carey &
  Carey, 2015); *Leaving ADDIE for SAM* (Allen, 2012); *Multimedia Learning* (Mayer, 2009);
  *e-Learning and the Science of Instruction* (Clark & Mayer, 2016); and *Instructional-Design
  Theories and Models* (Reigeluth, ed., 1999).
