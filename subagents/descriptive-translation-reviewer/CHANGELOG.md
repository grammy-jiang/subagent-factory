# Changelog — descriptive-translation-reviewer

All notable changes to this generated subagent package are recorded here. Versions follow the
`agent_version` field in `profile.yaml`.

## [1.0.0] — 2026-07-12

### Added
- Initial release of the **descriptive-translation-reviewer** subagent (Tier 1), authoring the LLM layer over the
  already-assembled, deterministically-valid distilled spine (180 principles P001-P180 /
  984 claims from three distillation-only sources).
- `profile.yaml` derived from the 180 promoted principles: role, when/when-not-to-use, three modes
  (review / advise / compare), quality bar, forbidden behaviours, handoff rules, and a
  12-skill / 2-reference `knowledge_partition` covering every principle exactly
  once.
- 12 authored skills partitioning all 180 principles; 2 references
  (principles index + evidence notes).
- `reports/faithfulness-report.yaml` — every load-bearing profile rule graded WITHIN_SCOPE against
  its principles (no rule stronger than its evidence).
- `tests/golden-tests.yaml` (6 golden, 2 negative-routing,
  2 missing-context) and `tests/principle-behaviour-tests.yaml` (one behaviour test per
  principle, 180 total).
- Claude Code adapter exported to `adapters/claude-code/` and installed under
  `.claude/agents/generated/`.

### Grounding
- Three distillation-only sources: Jeremy Munday, *Introducing Translation Studies* (2016);
  Lawrence Venuti, ed., *The Translation Studies Reader* (2012); Gideon Toury, *The Nature and Role
  of Norms in Translation* (1995).
