# Changelog — instructional-design-advisor

All notable changes to this generated subagent package are recorded here. Versions follow the
`agent_version` field in `profile.yaml`.

## [1.0.0] — 2026-07-26

### Added
- Initial release of the **instructional-design-advisor** subagent (Tier 2), authoring the LLM layer over the
  already-assembled, deterministically-valid distilled spine (180 principles
  P001-P180 / 6851 claims from ten distillation-only sources).
- `profile.yaml` derived from the 180 promoted principles: role, router description,
  when/when-not-to-use, three modes (advise / review / plan), quality bar, forbidden behaviours,
  handoff rules, and a 13-skill / 2-reference `knowledge_partition` covering
  every principle exactly once.
- 13 authored skills partitioning all 180 principles; 2 references
  (principles index + evidence notes).
- `reports/faithfulness-report.yaml` — every load-bearing profile rule graded WITHIN_SCOPE against
  its principles (no rule stronger than its evidence).
- `tests/golden-tests.yaml` (7 golden, 3 negative-routing,
  3 missing-context) and `tests/principle-behaviour-tests.yaml` (one behaviour test per
  principle, 180 total).
- Claude Code adapter exported to `adapters/claude-code/` and installed under
  `.claude/agents/generated/`.

### Grounding
- Ten distillation-only sources: *Understanding by Design* (Wiggins & McTighe, 2005); *Teaching for
  Quality Learning at University* (Biggs & Tang, 2011); *Creating Significant Learning Experiences*
  (Fink, 2013); *A Taxonomy for Learning, Teaching, and Assessing* (Anderson & Krathwohl, 2001);
  *Principles of Instructional Design* (Gagné, Briggs & Wager, 1992); *First Principles of
  Instruction* (Merrill, 2002); *The Systematic Design of Instruction* (Dick, Carey & Carey, 2015);
  *Leaving ADDIE for SAM* (Allen, 2012); *Multimedia Learning* (Mayer, 2009); and *e-Learning and
  the Science of Instruction* (Clark & Mayer, 2016).
