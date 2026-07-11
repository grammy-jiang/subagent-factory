# Provenance Ledger — calibration-forecasting-reviewer

Canonical record of what grounds this subagent. The profile, skills, references, faithfulness
report, and tests are all derived from the distilled spine in this package
(`principles/principles.yaml` → `analysis/claims.jsonl` → `evidence/evidence-records.yaml` →
`sources/anchors/*.anchors.jsonl`), which was assembled by the map→reduce build. No profile field
value is an orphan: every load-bearing rule cites the promoted principle(s) it restates.

## Sources

| source_id | title | author | year | rights |
|-----------|-------|--------|------|--------|
| thinking-fast-and-sl-d88ef771 | Thinking, Fast and Slow | Daniel Kahneman | 2011 | distillation-only |
| superforecasting-e3c7c0b4 | Superforecasting: The Art and Science of Prediction | Philip E. Tetlock and Dan Gardner | 2015 | distillation-only |
| expert-political-jud-5da0a790 | Expert Political Judgment: How Good Is It? How Can We Know? | Philip E. Tetlock | 2005 | distillation-only |
| perception-and-mispe-a445f294 | Perception and Misperception in International Politics | Robert Jervis | 1976 | distillation-only |
| psychology-of-intell-3a2b4f82 | Psychology of Intelligence Analysis | Richards J. Heuer Jr. | 1999 | distillation-only |
| tradecraft-primer-6ec9d9fb | A Tradecraft Primer: Structured Analytic Techniques | US Government (CIA) | 2009 | distillation-only |

All sources are **distillation-only**: paraphrase and restructure only, no verbatim quotation
(see `.claude/rules/rights-and-quotation-policy.md`; enforced by `quote_scan`).

## Distilled spine

- **91 promoted principles** (`principles/principles.yaml`, P001–P091; 83 high-confidence, 8 medium).
- **2,889 atomic claims** (`analysis/claims.jsonl`, C-ids), each source-anchored.
- **697 evidence records** (`evidence/evidence-records.yaml`, E-ids keyed by `claim_id`).
- **Paragraph anchors** per source (`sources/anchors/*.anchors.jsonl`, `<sha12>-cNNNN`).

## Profile → principle mapping

The eight skills partition all 91 principles (each principle cited at least once); the profile's
`quality_bar`, `forbidden_behaviours`, `handoff_rules`, and `always_on` carry the `(Pxxx)` tags of
the principles they restate. Coverage:

| Skill | Principles |
|-------|-----------|
| calibration-and-probability-hygiene | P002, P003, P010, P014, P018, P028, P031, P032, P038, P052, P058, P073, P076, P078 |
| forecast-scoring-and-evaluation | P013, P015, P025, P035, P039, P048, P050, P059, P065, P068, P071, P075, P077, P090 |
| base-rates-outside-view-and-regression | P005, P006, P007, P023, P049, P051, P066, P067, P082, P091 |
| bayesian-belief-updating | P012, P022, P024, P046, P053, P054, P069, P074, P080 |
| cognitive-bias-and-mindset-control | P001, P008, P016, P017, P019, P020, P027, P033, P034, P041, P042, P045, P057 |
| forecaster-style-and-aggregation | P009, P011, P021, P029, P030, P036, P044, P060, P061, P063, P064, P070, P088 |
| scenarios-horizon-and-tail-risk | P004, P026, P040, P047, P055, P056, P079, P081, P084, P085, P087, P089 |
| forecasting-accountability-and-communication | P037, P043, P062, P072, P083, P086 |

**Skill-only principles (not restated in the profile).** `P023` (base-rates skill) and `P087`
(scenarios skill) are cited by their skill bodies but were removed from the profile `always_on` rules
in v1.0.1 — `P023` carries a moral caveat and `profile_rule: false`; `P087` was a stray cite. They
partition into the skills but the profile does **not** restate them, so no profile-level grounding
depends on them.

## Faithfulness

`reports/faithfulness-report.yaml` grades each load-bearing profile rule — including the eight
`knowledge_partition.always_on` runtime rules — against its promoted principles on the five-level
claim-strength scale. Every finding is `WITHIN_SCOPE`; one (`forbidden_behaviours[3]`) carries an
`add_condition` action, where a validation condition was added so the medium-confidence P031 clause
keeps its source hedge rather than reading as a flat ban. No rule is stronger than its evidence.
`source_anchors` are omitted deliberately; provenance is carried in each finding's note via principle
+ claim IDs.

## Version History

### v1.0.2 — 2026-07-11
Review r2 faithfulness and release-readiness fixes (no new claims):
- Qualified `forbidden_behaviours[3]`: the P031 (medium) clause now reads "where finer distinctions
  have not been validated against real frequencies, treating granularity as precision", restoring the
  source hedge (was HEDGING_REMOVED against high-confidence P059/P035).
- Faithfulness report: added per-rule findings for all eight `knowledge_partition.always_on` runtime
  rules with rule-specific citations; flipped the `forbidden_behaviours[3]` finding to `add_condition`
  documenting the P031 validation condition.
- Provenance ledger: backfilled this Version History; annotated P023/P087 as skill-only (not
  profile-restated) and updated the Faithfulness section.
- Bumped `tests/golden-tests.yaml` `profile_version` to match; rewrote all eight skill `description`
  fields to third person; folded a sibling-disambiguation clause into the `forecast-scoring-and-evaluation`
  and `forecasting-accountability-and-communication` descriptions.

### v1.0.1 — 2026-07-11
Review r1 citation-integrity and over-claim fixes (no new claims). Dropped the P023 citation and the
"use causal base rates" clause from the outside-view `always_on` rule (P023 is `profile_rule: false`
and carries a moral caveat; P006/P007 ground the uncaveated content); dropped the stray P087 cite from
the horizon/tail-risk `always_on` rule; corrected `forbidden_behaviours[1]` cite P003→P021; added P025
to `forbidden_behaviours[2]` and P033 to the cognitive-trap `quality_bar` rule; removed the "off only
on timing" clause from the `forecast-scoring-and-evaluation` skill anti-pattern (owned by
`forecasting-accountability-and-communication`/P083); softened the granularity-theatre
`forbidden_behaviours` clause to its P031 source; regenerated the adapter `description` on re-export.
No prior profile decisions superseded beyond the corrected citations above.

### v1.0.0 — 2026-07-10
Initial release. LLM-authored layer (profile, 8 skills, 2 references, faithfulness report, golden +
principle-behaviour tests, adapter) generated over the map→reduce distilled spine. No prior profile
decisions superseded (first version).
