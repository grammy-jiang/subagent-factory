# Changelog — calibration-forecasting-reviewer

All notable changes to this generated subagent package are recorded here. Versions follow the
`agent_version` field in `profile.yaml`.

## [1.0.2] — 2026-07-11

### Fixed
- Review r2 faithfulness and release-readiness fixes (no new claims):
  - CRITICAL — faithfulness report now covers the eight `knowledge_partition.always_on` runtime rules:
    added a per-rule finding for `always_on[0..7]` with rule-specific citations (previously only
    peripheral fields were graded).
  - HIGH — qualified `forbidden_behaviours[3]`: the medium-confidence P031 clause now reads "where
    finer distinctions have not been validated against real frequencies, treating granularity as
    precision" (was an unqualified prohibition = HEDGING_REMOVED); the report finding flips to
    `add_condition`.
  - HIGH — provenance ledger: backfilled v1.0.1 and v1.0.2 Version History entries (supersession rule);
    annotated P023/P087 as skill-only, not profile-restated; updated the Faithfulness section.
  - HIGH — bumped `tests/golden-tests.yaml` `profile_version` from 1.0.0 to 1.0.2.
  - HIGH — rewrote all eight skill `description` fields from imperative to third person (agent-skills
    corpus convention; matches sibling packages).
  - MEDIUM — folded a sibling-disambiguation clause into the `forecast-scoring-and-evaluation`
    ("almost happened" defence owned by accountability) and `forecasting-accountability-and-communication`
    (proper-scoring arithmetic owned by scoring) descriptions.

## [1.0.1] — 2026-07-11

### Fixed
- Review r1 citation-integrity and over-claim fixes (no new claims):
  - HIGH-1 — dropped the P023 citation and the "use causal base rates" clause from the outside-view
    `always_on` rule (P023 is `profile_rule: false` and carries a moral caveat; P006/P007 already
    ground the uncaveated base-rate content).
  - HIGH-2 — regenerated the adapter `description` on re-export (was a mid-clause char-truncation of
    `when_to_use`).
  - MED-1 — removed the "off only on timing" clause from the `forecast-scoring-and-evaluation` skill
    anti-pattern (that check is owned by `forecasting-accountability-and-communication` / P083); added
    the correct P025 cite to `forbidden_behaviours[2]` for the "almost right" clause.
  - MED-2 — dropped stray P087 cite from the horizon/tail-risk `always_on` rule; corrected
    `forbidden_behaviours[1]` cite from P003 to P021 ("confidence untethered from a track record").
  - LOW — added P033 to the cognitive-trap `quality_bar` rule; softened the granularity-theatre
    `forbidden_behaviours` clause to its P031 source (validated-against-real-frequencies condition);
    added sibling-skill and `forecasting-evidence-notes` reference pointers to the
    `forecast-scoring-and-evaluation` skill.

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
