# Changelog — calibration-forecasting-reviewer

All notable changes to this generated subagent package are recorded here. Versions follow the
`agent_version` field in `profile.yaml`.

## [1.0.0] — 2026-07-10

### Added
- Initial release of the **calibration-forecasting-reviewer** subagent (Tier 2).
- `profile.yaml` derived from the 91 promoted principles (P001–P091): role, when/when-not-to-use,
  three modes (review / advise / compare), quality bar, forbidden behaviours, handoff rules, and an
  eight-skill / two-reference `knowledge_partition` covering all principles.
- Eight authored skills: calibration-and-probability-hygiene, forecast-scoring-and-evaluation,
  base-rates-outside-view-and-regression, bayesian-belief-updating, cognitive-bias-and-mindset-control,
  forecaster-style-and-aggregation, scenarios-horizon-and-tail-risk,
  forecasting-accountability-and-communication.
- Two references: calibration-forecasting-principles-index, forecasting-evidence-notes.
- `reports/faithfulness-report.yaml` — every load-bearing profile rule graded WITHIN_SCOPE against
  its principles (no rule stronger than its evidence).
- `tests/golden-tests.yaml` (5 golden, 2 negative-routing, 2 missing-context) and
  `tests/principle-behaviour-tests.yaml` (one behaviour test per principle, 91 total).
- Claude Code adapter exported to `adapters/claude-code/` and installed under
  `.claude/agents/generated/`.

### Grounding
- Six distillation-only sources: Kahneman *Thinking, Fast and Slow*; Tetlock *Expert Political
  Judgment* and (with Gardner) *Superforecasting*; Jervis *Perception and Misperception*; Heuer
  *Psychology of Intelligence Analysis*; the intelligence-community tradecraft primer.
