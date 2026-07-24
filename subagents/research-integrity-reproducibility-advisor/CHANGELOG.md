# Changelog — research-integrity-reproducibility-advisor

All notable changes to this generated subagent package are recorded here. Versions follow the
`agent_version` field in `profile.yaml`.

## [1.0.0] — 2026-07-25

### Added
- Initial release of the **research-integrity-reproducibility-advisor** subagent (Tier 2), authoring the LLM layer over the
  already-assembled, deterministically-valid distilled spine (34 principles
  P001-P034 / 753 claims from three distillation-only sources).
- `profile.yaml` derived from the 34 promoted principles: role, when/when-not-to-use, three
  modes (advise / review / plan), quality bar, forbidden behaviours, handoff rules, and a
  7-skill / 2-reference `knowledge_partition` covering every principle exactly
  once.
- 7 authored skills partitioning all 34 principles; 2 references
  (principles index + evidence notes).
- `reports/faithfulness-report.yaml` — every load-bearing profile rule graded WITHIN_SCOPE against
  its principles (no rule stronger than its evidence).
- `tests/golden-tests.yaml` (6 golden, 2 negative-routing,
  2 missing-context) and `tests/principle-behaviour-tests.yaml` (one behaviour test per
  principle, 34 total).
- Claude Code adapter exported to `adapters/claude-code/` and installed under
  `.claude/agents/generated/`.

### Grounding
- Three distillation-only sources: *The Turing Way: A Handbook for Reproducible, Ethical and
  Collaborative Research* (The Turing Way Community, 2022); *On Being a Scientist: A Guide to
  Responsible Conduct in Research*, 3rd ed. (National Academies, 2009); and a higher-education
  academic-norms guide.
