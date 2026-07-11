# Provenance Ledger — analytic-method-reviewer

Every profile field traces to the distilled spine of this package: promoted principles in
`principles/principles.yaml` (each `derived_from_claims` resolves into `analysis/claims.jsonl`),
their evidence in `evidence/evidence-records.yaml`, and chunk anchors in
`sources/anchors/*.anchors.jsonl`. No profile value is an orphan.

## Sources

| source_id | title | rights_status |
|-----------|-------|---------------|
| psychology-of-intell-3a2b4f82 | Psychology of Intelligence Analysis (Heuer) | distillation-only |
| tradecraft-primer-6ec9d9fb | A Tradecraft Primer — Structured Analytic Techniques (CIA / Kent School) | distillation-only |
| thinking-fast-and-sl-d88ef771 | Thinking, Fast and Slow (Kahneman) | distillation-only |
| superforecasting-e3c7c0b4 | Superforecasting (Tetlock & Gardner) | distillation-only |
| expert-political-jud-5da0a790 | Expert Political Judgment (Tetlock) | distillation-only |
| perception-and-mispe-a445f294 | Perception and Misperception in International Politics (Jervis) | distillation-only |

All sources are `distillation-only`: distillation is permitted; verbatim quotation is not. The
verbatim `sources/original` and `sources/markdown` layers are withheld from any rights-clean export
per `.claude/rules/rights-and-quotation-policy.md`.

## Field → grounding

Profile rules are grounded in promoted principles, cited by ID in each rule and graded in
`reports/faithfulness-report.yaml`. The load-bearing map:

| Profile field | Grounded in principles |
|---------------|------------------------|
| role | P013, P052, P057 (review analytic method; narrow to review/advise) |
| quality_bar[0] (fact vs opinion, explicit uncertainty & assumptions) | P057, P073, P074, P047 |
| quality_bar[1] (competing hypotheses, diagnosticity, refute) | P013, P027, P054, P060, P061 |
| quality_bar[2] (surface & challenge mind-set / assumptions) | P045, P047, P011, P046 |
| quality_bar[3] (probabilistic coherence & calibration) | P005, P034, P068, P012 |
| quality_bar[4] (counter mirror-imaging & single-outcome) | P004, P006, P020, P058, P080 |
| forbidden_behaviours | P008, P010, P013, P046, P052, P054, P057, P059, P061, P074 |
| knowledge_partition.always_on | the nine skills below, covering all 82 principles |

## Skill partition → principles

Each skill in `skills/` groups a disjoint set of principles; together they cover all 82.

| Skill | Principles |
|-------|------------|
| cognitive-biases-and-dual-process-reasoning | P009 P038 P051 P053 P064 P065 P066 P067 P082 |
| mindsets-schemata-and-perception | P002 P016 P017 P025 P031 P045 P046 P055 |
| structured-analytic-techniques | P004 P006 P007 P011 P026 P030 P033 P039 P042 P043 P072 P079 P080 |
| competing-hypotheses-and-diagnostic-evidence | P003 P013 P014 P020 P027 P028 P032 P054 P060 P061 P062 P070 |
| probabilistic-judgment-and-calibration | P005 P012 P034 P035 P044 P050 P068 |
| limits-of-expertise-and-prediction | P018 P019 P041 P048 P049 P052 P076 |
| perception-misperception-and-signaling | P021 P023 P029 P036 P037 P056 P069 P077 P078 |
| assumptions-framing-and-analytic-writing | P047 P057 P059 P073 P074 P075 |
| analytic-collaboration-training-and-process | P001 P008 P010 P015 P022 P024 P040 P058 P063 P071 P081 |

The full per-principle statement and home skill is tabulated in
`references/analytic-method-principles-index.md`.

## Version History

### 1.1.2 — 2026-07-11

Auto-routing disambiguation from the sibling `calibration-forecasting-reviewer` (RESIDUAL-TRIAGE cal-fore
H1: both packages' `when_to_use` claim "calibration" and "cognitive bias", so the auto-router could not
tell them apart). No new claims and no distilled-spine change; superseded decisions stay visible above.

- Appended one mutual-exclusion boundary bullet to `when_not_to_use`: when the concern is the PROBABILITY
  itself — its calibration, proper scoring (Brier), base-rate and regression grounding, or overconfidence
  in the number — rather than the reasoning structure, the calibration-forecasting reviewer owns it. This
  narrows routing scope; like the other `when_not_to_use` entries it restates no source claim, so it
  carries no principle tag, matching the uncited scope boundaries already in `when_not_to_use`.
- Profile body is ~833 words after the +33-word bullet (was ~800), under the 1000-word hard FAIL, so no
  prose was trimmed; the body-size self-check now WARNs over its 800-word soft budget. Re-exported the
  adapter.

### 1.1.1 — 2026-07-11

R2 review fix pass (`reports/intel-review-loop/subagent-analytic-method-reviewer.r2.review.md`); all
changes grounded in existing principle IDs, no new claims. Superseded decisions stay visible above.

- `handoff_rules[0]`: dropped the P001/P059 citations that false-grounded the analyst/organization
  decision-ownership assertion (no source establishes decision authority); now presented as an
  uncited scope boundary, matching `when_not_to_use`.
- `knowledge_partition.always_on` bullet 7: dropped P010 (a conditional ACH-mandate, not an ownership
  claim — over-claim); P010 remains correctly cited in `forbidden_behaviours[1]`.
- Routing: `when_to_use[0]` and `when_not_to_use[0]` reworded so the exported adapter `description`
  retains the inclusion keys (hypotheses, evidence, assumptions, uncertainty) and the full exclusion
  list (collection tasking, HUMINT, interrogation, targeting, covert action) within the truncation
  budget; no scope change.
- Removed a stray `</content>` generation-tooling tag from
  `skills/limits-of-expertise-and-prediction/SKILL.md`.
- Refreshed this ledger's field→grounding rows: `quality_bar[4]` now lists P080; `forbidden_behaviours`
  now lists P010 (both were cited in the 1.1.0 profile but missing from the table).

### 1.1.0 — 2026-07-11

R1 review fix pass; all changes grounded in existing principle IDs, no new claims.

- `profile.yaml` body trimmed to the ~800-word budget so `profile_self_check` check 14 (body-size)
  passes; role/`when_to_use`/`modes`/`quality_bar` tightened without dropping a principle citation.
- Faithfulness: two over-claims weakened to their source support — `quality_bar[4]` scopes Red Team /
  Alternative Futures / competing-view procedures to where stakes and cost justify them (adds P080);
  `forbidden_behaviours[1]` scopes the single-outcome prohibition to high-stakes / deception-serious
  issues (adds P010).
- Adapter routing `description` regenerated; nine `skills/*/SKILL.md` refined surgically (negative
  routing boundary in each `description`, `## References` point to the evidence notes, `## Anti-patterns
  to flag` compressed). Procedure steps and provenance frontmatter preserved verbatim.

### 1.0.0 — 2026-07-10

Initial LLM-authored layer (profile, faithfulness report, nine skills, two references, tests, adapter)
over the deterministically-built distilled spine (82 principles, 2,889 claims, 496 evidence records,
163 chunk anchors across 6 sources). Distilled spine unchanged. No prior profile decisions superseded.
