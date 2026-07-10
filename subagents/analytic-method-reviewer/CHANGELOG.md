# Changelog — analytic-method-reviewer

All notable changes to this generated subagent package are recorded here. Versions follow the
`agent_version` field in `profile.yaml` (semver).

## [1.0.0] — 2026-07-10

### Added
- Initial release. LLM-authored layer built over the deterministic map→reduce spine:
  - `profile.yaml` (portable-profile-v1) — role, scope, review/advise/compare modes, quality bar,
    forbidden behaviours, source-of-truth policy, and a nine-skill knowledge partition; every rule
    grounded in promoted principle IDs. Tier 2, status ready.
  - `reports/faithfulness-report.yaml` — 23 per-rule claim-strength findings over the profile's role,
    `when_to_use`/`when_not_to_use`, `quality_bar`, `forbidden_behaviours`, output modes, and
    `minimum_useful_output`; all verdicts EXACT_SUPPORT/WITHIN_SCOPE (the profile narrows the sources to
    a review/advise posture and never over-claims), no rule stronger than its evidence, provenance
    carried in each note via principle + claim IDs.
  - `skills/` — nine skill bodies grounding all 82 promoted principles by theme (cognitive biases,
    mind-sets and perception, structured analytic techniques, competing hypotheses and diagnostic
    evidence, probabilistic judgment and calibration, the limits of expertise and prediction,
    perception/misperception and signaling, assumptions/framing/analytic writing, and analytic
    collaboration/training/process).
  - `references/` — analytic-method principles index and evidence notes.
  - `tests/golden-tests.yaml` — routing goldens (positive, negative-routing, missing-context) plus
    `tests/principle-behaviour-tests.yaml` — one behaviour test per principle (every high-confidence
    principle covered).
  - `adapters/claude-code/analytic-method-reviewer.md` — exported Claude Code adapter.

### Fixed
- Corrected `source_type` from `md` to the schema value `markdown` in the six
  `sources/metadata/*.metadata.json` files (schema-enum conformance; no distillation content changed).

### Distilled spine (unchanged, deterministically built)
- 82 principles, 2,889 claims, 496 evidence records, 163 chunk anchors across 6 sources: Heuer's
  Psychology of Intelligence Analysis, the CIA Sherman Kent School Tradecraft Primer, Kahneman's
  Thinking, Fast and Slow, Tetlock's Superforecasting and Expert Political Judgment, and Jervis's
  Perception and Misperception in International Politics.
