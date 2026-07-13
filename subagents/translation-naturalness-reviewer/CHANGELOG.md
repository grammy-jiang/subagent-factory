# Changelog — translation-naturalness-reviewer

All notable changes to this generated subagent package are recorded here. Versions follow the
`agent_version` field in `profile.yaml`.

## [1.0.0] — 2026-07-13

### Added
- Initial release of the **translation-naturalness-reviewer** subagent (Tier 2), authoring the LLM layer over the
  already-assembled, deterministically-valid distilled spine (150 principles
  P001-P150 / 2717 claims from nine distillation-only sources).
- `profile.yaml` derived from the 150 promoted principles: role, when/when-not-to-use,
  three modes (review / advise / compare), quality bar, forbidden behaviours, handoff rules, and a
  15-skill / 2-reference `knowledge_partition` covering every principle exactly
  once.
- 15 authored skills partitioning all 150 principles; 2 references
  (principles index + evidence notes).
- `reports/faithfulness-report.yaml` — every load-bearing profile rule graded WITHIN_SCOPE against
  its principles (no rule stronger than its evidence).
- `tests/golden-tests.yaml` (6 golden, 2 negative-routing,
  2 missing-context) and `tests/principle-behaviour-tests.yaml` (one behaviour test per
  principle, 150 total).
- Claude Code adapter exported to `adapters/claude-code/` and installed under
  `.claude/agents/generated/`.

### Grounding
- Nine distillation-only sources: Eugene Nida, *Principles of Correspondence* (1964); Gideon Toury,
  *The Nature and Role of Norms in Translation* (1995); Juliane House, *Translation Quality
  Assessment* (2015); Jody Byrne, *Technical Translation* (2006) and *Scientific and Technical
  Translation Explained* (2012); Mona Baker, *In Other Words* (2011); Jeremy Munday, *Introducing
  Translation Studies* (2016); Lawrence Venuti, ed., *The Translation Studies Reader* (2012); and Yu
  Guangzhong on the naturalness and Europeanization of Chinese.
