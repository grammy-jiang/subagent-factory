# Changelog — research-writing-advisor

All notable changes to this generated subagent package are recorded here. Versions follow the
`agent_version` field in `profile.yaml`.

## [1.0.0] — 2026-07-25

### Added
- Initial release of the **research-writing-advisor** subagent (Tier 2), authoring the LLM layer over the
  already-assembled, deterministically-valid distilled spine (172 principles
  P001-P172 / 3693 claims from nine distillation-only sources).
- `profile.yaml` derived from the 172 promoted principles: role, when/when-not-to-use, three
  modes (advise / review / plan), quality bar, forbidden behaviours, handoff rules, and a
  13-skill / 2-reference `knowledge_partition` covering every principle exactly
  once.
- 13 authored skills partitioning all 172 principles; 2 references
  (principles index + evidence notes).
- `reports/faithfulness-report.yaml` — every load-bearing profile rule graded WITHIN_SCOPE against
  its principles (no rule stronger than its evidence).
- `tests/golden-tests.yaml` (7 golden, 3 negative-routing,
  3 missing-context) and `tests/principle-behaviour-tests.yaml` (one behaviour test per
  principle, 172 total).
- Claude Code adapter exported to `adapters/claude-code/` and installed under
  `.claude/agents/generated/`.

### Grounding
- Nine distillation-only sources: *The Craft of Research* (4th ed., Booth et al., 2016); *Writing
  for Computer Science* (Zobel, 2014); *Writing Science* (Schimel, 2012); *English for Writing
  Research Papers* (Wallwork, 2016); *Science Research Writing for Non-Native Speakers of English*
  (Glasman-Deal, 2010); *How to Write a Lot* (Silvia, 2007); *How to Take Smart Notes* (Ahrens,
  2017); *Presentation Zen Design* (Reynolds, 2010); and *TED Talks* (Anderson, 2016).
