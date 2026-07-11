# Changelog — analytic-method-reviewer

All notable changes to this generated subagent package are recorded here. Versions follow the
`agent_version` field in `profile.yaml` (semver).

## [1.1.1] — 2026-07-11

### Fixed
- Review R2 fix pass (`reports/intel-review-loop/subagent-analytic-method-reviewer.r2.review.md`),
  all changes grounded in existing principle IDs — no new claims.
- Faithfulness: dropped the P001/P059 citations from `handoff_rules[0]` — neither principle
  establishes decision-authority, so citing them false-grounded the analyst/organization ownership
  assertion; now an uncited scope boundary. Dropped P010 from `knowledge_partition.always_on` bullet 7
  (P010 is a conditional ACH-mandate, not an ownership claim; it stays cited in
  `forbidden_behaviours[1]`).
- Adapter routing `description`: reworded `when_to_use[0]` and `when_not_to_use[0]` so the exported
  description retains the inclusion keys (hypotheses, evidence, assumptions, uncertainty) and the full
  operational exclusion list (collection tasking, HUMINT, interrogation, targeting, covert action)
  within the truncation budget.
- Removed a stray `</content>` generation-tooling tag from
  `skills/limits-of-expertise-and-prediction/SKILL.md`.
- Provenance ledger: added the previously-missing 1.1.0 and this 1.1.1 Version History entries; added
  P080 to the `quality_bar[4]` field→grounding row and P010 to the `forbidden_behaviours` row (both
  cited in profile since 1.1.0 but stale in the table).
- `tests/golden-tests.yaml` `profile_version` bumped 1.0.0 → 1.1.1 (no golden expectation changed).
- Re-exported the adapter so all cited principles (through P082) render and the routing description
  reflects the above.

## [1.1.0] — 2026-07-11

### Changed
- Review R1 fix pass (`reports/intel-review-loop/subagent-analytic-method-reviewer.r1.review.md`),
  all changes grounded in existing principle IDs — no new claims.
- `profile.yaml` body trimmed to the ~800-word budget so `profile_self_check` check 14 (body-size)
  now PASSes instead of failing the hard cap; role/`when_to_use`/`modes`/`quality_bar` tightened
  without dropping any principle citation.
- Faithfulness: weakened two over-claims to their source support —
  - `quality_bar[5]` no longer states an unconditional "no hypothesis without a competitor"; it now
    scopes Red Team / Alternative Futures / competing-view procedures to where stakes and cost justify
    them, with hypothesis count scaled to uncertainty and policy impact (adds P080).
  - `forbidden_behaviours[1]` scopes the single-outcome prohibition to key/high-stakes issues where
    the cost of error is high or deception is a serious possibility (adds P010).
- Adapter routing `description` regenerated: `when_not_to_use` reordered so the
  operational/collection/HUMINT/targeting exclusion is surfaced first, preventing an operational
  request from mis-routing to this read-only analytic-method reviewer.
- All nine `skills/*/SKILL.md` refined (surgical): each `description` gained a negative
  routing boundary naming its most-confusable sibling; each `## References` now points to
  `analytic-method-evidence-notes.md`; each `## Anti-patterns to flag` compressed to terse
  flaw-name + principle-ID bullets (removing the near-duplicate restatement of the Procedure).
  Procedure steps and provenance frontmatter preserved verbatim.

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
