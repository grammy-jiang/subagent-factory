# Changelog — calibration-forecasting-reviewer

All notable changes to this generated subagent package are recorded here. Versions follow the
`agent_version` field in `profile.yaml`.

## [1.0.4] — 2026-07-11

### Changed
- Auto-routing disambiguation from `analytic-method-reviewer` (RESIDUAL-TRIAGE cal-fore H1: both
  packages' `when_to_use` claim "calibration" and "cognitive bias", so Claude Code's auto-router could
  not tell them apart). Appended one mutual-exclusion boundary bullet to `when_not_to_use`: when the
  concern is the reasoning STRUCTURE — competing hypotheses (ACH), a key-assumptions check, which
  structured technique to run, or how evidence is weighed — rather than the probability's calibration,
  scoring, or base-rate grounding, that belongs to the analytic-method reviewer. A scope/authority
  boundary, so no principle citation (like the other `when_not_to_use` entries); no new grounded rule
  and no distilled-spine change.
- Body-size guard: the +39-word bullet tipped the profile body to ~1035 words, over the 1000-word
  `profile_self_check` hard FAIL. Trimmed ~45 words of purely illustrative, duplicative parentheticals
  — the correction list and anti-pattern list in `outputs.primary_format`, the flaw-class list in the
  `review` mode output, and the example list in the `compare` mode trigger — with no rule meaning or
  principle citation removed. Body now ~990 words (under the FAIL line; body-size stays a WARNING as it
  was at v1.0.3's ~996).
- `tests/golden-tests.yaml` `profile_version` bumped 1.0.3 → 1.0.4 (no golden expectation changed);
  adapter re-exported so the routing `description` reflects the new exclusion.

## [1.0.3] — 2026-07-11

### Fixed
- Review r3 residual faithfulness fixes (no new claims):
  - MUST (M1, HEDGING_REMOVED) — `forbidden_behaviours[2]` reworded from a flat ban on scoring
    "almost right" / "off on timing" as success to forbidding it as **full rather than proportionally
    discounted** success, restoring the graduated P025/P086 hedge (the excuse earns only a small
    proportional fraction of credit, not zero) and matching `always_on[7]`; the report finding flips
    to `add_condition`.
  - MUST (M2) — `reports/faithfulness-report.yaml`: replaced the byte-identical `P015/P006/P022`
    citation shared by ~16 findings with per-rule content-specific groundings; corrected the
    `when_to_use[3]` cognitive-trap trigger (now P008/P020/P038/P034/P057) and the role-separation
    rules (`when_not_to_use[0]`, `forbidden_behaviours[0]`, `handoff_rules[0]`), which are marked
    advisory-boundary design decisions instead of the mis-attributed P039; multi-cite notes labelled
    representative.
  - Profile: dropped the mis-attributed `(P039)` from `forbidden_behaviours[0]` and the failure-recovery
    example; reduced `handoff_rules[0]` to `(P080)`.
  - LOW (L2) — `role` credits Gardner ("Tetlock (with Gardner)") as Superforecasting co-author;
    tightened role prose to keep the profile body under the word budget.
  - Provenance ledger + CHANGELOG updated; adapter re-exported.

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
