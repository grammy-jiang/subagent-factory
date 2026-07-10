# Changelog — bias-perception-reviewer

All notable changes to this generated subagent package are recorded here. Versions follow the
`agent_version` field in `profile.yaml` (semver).

## [1.0.0] — 2026-07-10

### Added
- Initial release. LLM-authored layer built over the deterministic map→reduce spine:
  - `profile.yaml` (portable-profile-v1) — role, scope, review/advise/compare modes, quality bar,
    forbidden behaviours, source-of-truth policy, and a ten-skill knowledge partition, every rule
    grounded in promoted principle IDs.
  - `reports/faithfulness-report.yaml` — per-rule claim-strength check over the profile's role,
    `when_to_use`/`when_not_to_use`, `quality_bar`, `forbidden_behaviours`, and output modes; all
    verdicts EXACT_SUPPORT/WITHIN_SCOPE (the profile narrows the sources to bias review and advice),
    no rule stronger than its evidence, provenance carried in each note via principle + claim IDs.
  - `skills/` — ten skill bodies grounding all 200 promoted principles by theme, each with a
    `## Procedure` citing its own principle IDs.
  - `references/` — principles index and evidence notes.
  - `tests/golden-tests.yaml` + `tests/principle-behaviour-tests.yaml` — routing goldens plus one
    behaviour test per principle (every high-confidence principle covered).
  - `adapters/claude-code/bias-perception-reviewer.md` — exported Claude Code adapter.

### Distilled spine (unchanged, deterministically built)
- 200 principles, 2,889 claims, 1,482 evidence records, 163 chunk anchors across six sources:
  the CIA Tradecraft Primer, Heuer's Psychology of Intelligence Analysis, Kahneman's Thinking, Fast
  and Slow, Tetlock's Superforecasting and Expert Political Judgment, and Jervis's Perception and
  Misperception in International Politics.
