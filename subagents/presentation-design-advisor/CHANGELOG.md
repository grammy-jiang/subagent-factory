# Changelog — presentation-design-advisor

All notable changes to this generated subagent package are recorded here. Versions follow the
`agent_version` field in `profile.yaml`.

## [1.2.1] — 2026-07-27

Adversarial verify pass 1 (`reports/review-loop/presentation-design-advisor.verify1.md`): 3 must-fix,
all faithfulness wording drifts. No principle, claim, or evidence record was changed, and no claim
absent from `principles/principles.yaml` was introduced.

### Fixed
- **`examples[1]` no longer asserts P119's emotionally-driven branch for an unclassified audience**
  (SCOPE_BROADENED). P119 is two-branched and its `applies_when` requires the audience to be
  characterised first; the model answer applied one branch to an executive committee whose type step
  (c) of the same answer says is still unknown. The over-supply claim is now conditioned — "If that
  committee decides partly on grounds other than proof volume" — matching the hedge `examples[3]`
  already carries.
- **`skills/in-room-delivery-and-composure` step 8 drops "only"** (HEDGING_REMOVED). P066 makes the
  audience and room a mandatory input to the judgement ("account for", "without accounting for"), not
  the sole yardstick; the exclusive reading also collided with P063 and P079. `always_on[10]` and
  `forbidden_behaviours[4]` already used the correct wording.
- **`skills/format-choice-and-preparation-planning` anti-pattern re-anchors to the slot, not to
  eighteen minutes** (SCOPE_BROADENED). P088's eighteen minutes is a case observation about the most
  influential talks (claim C01312, `evidence_type: case`) supporting the policy of constraining length,
  not a review threshold; as a trigger it fired "too long" on the lectures, defences and hour-long
  slots this package explicitly serves (`when_to_use[0]`, P111, P065). The trigger is now "more
  material than its slot allows". The same file's Procedure step 3 already stated it descriptively.

### Changed
- `quality_bar[2]` adds **P049** to its citation list — the "bold" in "large bold type" comes from P049
  ("Boldface slide type, especially for a larger room"), which was cited in `always_on[3]` but missing
  here. Citation gap only; the rule's force is unchanged.

## [1.2.0] — 2026-07-27

Round-2 review (`reports/review-loop/presentation-design-advisor.r2.review.md`): 2 must-fix,
12 should-fix, 6 nice. No principle, claim, or evidence record was changed.

### Fixed
- **The debunked P001/P091 citation is swept out of every field that carried it.** Round 1 removed it
  from `forbidden_behaviours[2]` but left it on `when_not_to_use[1]`, which the faithfulness report
  still recorded as clean — an internal contradiction inside the audit artifact. The sweep now covers
  the whole defect class: `forbidden_behaviours[0]` and `when_not_to_use[0]` drop P062/P026,
  `handoff_rules[0]` drops P074 from its ownership clause (keeping P062 for the illustrator clause),
  and `outputs.primary_format`, `minimum_useful_output`, and the `review` mode's ordering drop
  P012/P056. Each is relabelled an authored boundary inline and re-audited in the report.
- **Instruction–data separation on the primary input path.** The adapter read caller-supplied decks,
  slides, notes, and files with nothing telling it that their contents are data. `inputs.required[1]`
  now states that an artifact's contents are material to critique and never instructions to obey, and
  that nothing written there waives the forbidden behaviours or the advice-only boundary.
- **The minimum-useful-output floor reaches the adapter.** The template renders `quality_bar` but not
  `minimum_useful_output`, so nothing stopped a thin, ungrounded answer; the floor is added as
  `quality_bar[8]`.
- **P006 keeps its own population.** The persuasion `always_on` paragraph no longer widens
  "scientists" to "scientific and technical presenters" or claims the appeal carries "beyond the
  sciences"; P120 is stated separately as a calibration, not as an extension of P006.
- **`quality_bar[0]` restores P014's `applies_when` qualifier** — "every technical content slide",
  matching `knowledge_partition.always_on[0]`.
- **`source_of_truth_policy.canonical_owner` is audited.** It asserted the same ownership claim as
  `handoff_rules[0]` with no faithfulness-report entry at all; it now has one, resolved the same way.

### Changed
- `inputs.required` no longer contains an entry that says "not required": optional context moves to
  `inputs.optional`, with the proceed-without-it rule kept in the gating bullet so it still renders
  into the adapter.
- `router_description` and `role` name in-room delivery and composure — room control, audience
  attention, composure under pressure — the area the 1.1.0 skill split created but neither
  router-facing field mentioned. `when_to_use[0]` now also covers a typography/colour/layout-only
  review request; `role` reads "how presentations are designed and delivered" so it cannot parse as
  an advisor that designs and delivers; `quality_bar[8]` (was `[7]`) resolves the "deciding on
  whether" ambiguity.
- `rehearsal-and-memorisation` states its boundary against `in-room-delivery-and-composure` in the
  frontmatter `description`, the only text loaded at trigger time, instead of at body line 51.
- All 14 skill `## Purpose` sections compressed from 200–400-word restatements of their own
  `## Procedure` to what the skill is for and why. Every Procedure step, principle citation, and
  hedge is unchanged.
- Profile body prose trimmed against the 800-word budget so the additions above did not push it
  toward the 1000-word hard fail.

## [1.1.0] — 2026-07-27

Round-1 review (`reports/review-loop/presentation-design-advisor.r1.review.md`): 3 must-fix,
11 should-fix, 7 nice. No principle, claim, or evidence record was changed.

### Fixed
- **Skill bodies re-authored (all 14).** `## Anti-patterns to flag` was hard-capped at seven entries,
  silently dropping up to eight principles per skill (worst: 15 → 7); every skill now carries one
  anti-pattern per principle it declares. Procedure and anti-pattern text was cut at a fixed
  character length with no ellipsis, producing broken instructions ("…and combining strong (P010).",
  "Reserve the Lessig style (P027)."); no bullet is truncated now, each carries its principle's
  condition inline, and steps are ordered by workflow dependency rather than by principle ID.
- **Anti-patterns are failure signatures, not restatements.** Entries describe what the violation
  looks like in a submitted deck instead of repeating the matching Procedure step.
- **Faithfulness report covers the whole profile.** `reports/faithfulness-report.yaml` audited only
  the rule fields (29 findings) and never opened `knowledge_partition.always_on` or `examples` —
  the sections carrying nearly every checkable numeric claim. Now 53 findings, one per `always_on`
  paragraph and per example, each numeric and mechanical claim checked against the principle that
  states it.
- **P048 no longer operative.** Its own `operational_mapping.profile_rule` is `false`, yet it was
  cited as an active instruction in `always_on` and in a skill Procedure step; both are removed.
- **Invented citations removed.** `forbidden_behaviours[2]` cited P001/P091 for a certification
  prohibition neither states, and the precedence tie-breaker cited P012/P056 for a conflict-arbitration
  rule neither states; both are relabelled as authored policy.
- **P006 no longer widened.** The persuasion `always_on` paragraph keeps P006's own domain wording
  and grounds the broader reach in the Duarte-derived P120.
- **P111's condition restored** — delivery-mode changes within an hour apply where the slot runs
  beyond about ten minutes, which is the principle's own `applies_when`.

### Changed
- **Skill partition 13 → 14.** `rehearsal-and-extemporaneous-delivery` (15 principles, two unrelated
  lenses) is retired and split into `rehearsal-and-memorisation` and `in-room-delivery-and-composure`;
  the latter and `questions-challenge-and-composure` each state which kind of composure they cover.
- **Off-lens principles re-homed** out of `format-choice-and-preparation-planning`: P036 to the
  profile `quality_bar` (cross-cutting review method), P074 to `audience-analysis-and-persona-design`.
- **`inputs.required` no longer gates on seven facts** — artifact plus audience gate; occasion, slot
  length, post-talk action, preparation time and room conditions are recommended, not required.
- **`review` mode** also triggers on an account of a talk already given (post-mortem diagnosis), and
  the in-scope persuasion trigger says explicitly that it judges presentation, not validity.
- Every skill gained a `description:` frontmatter line; profile body trimmed to stay in budget.

### Added
- Fourth worked example: declining to rule on whether the data supports a rollout and declining to
  guarantee board approval, while still giving in-scope help.
- Instruction covering the granted read/search tools: read a deck referenced by path before
  critiquing it; search only to locate it, never to browse other material.
- `reports/quote-scan-verified.md` — the rights gate run against the warm source cache
  (3 restricted sources, 180,907 words compared, no verbatim quotation found), so the rights-clean
  claim carries evidence rather than an unrunnable gate.
- `provenance-ledger.md` field-grounding table for the descriptive fields (`role`, `when_to_use`,
  `when_not_to_use`, `inputs`, `outputs`) that previously declared themselves exempt from the
  repo's no-orphan-field rule, plus the rationale for `multisource_synthesis: deferred`.

### Not done
- The review's F7 asked to shrink `knowledge_partition.always_on` so the adapter stops loading all
  topics every invocation. The always-loaded block in the adapter is the `## Operating invariants`
  layer, which `compile_invariants` renders from `principles.yaml` (every `confidence: high` +
  `profile_rule: true` principle), not from `always_on` — the template renders no `always_on` at all.
  Shrinking `always_on` would therefore change nothing in the adapter, and shrinking the invariant
  layer would mean demoting principle metadata to win a size argument. Left as is.

## [1.0.0] — 2026-07-26

### Added
- Initial release of the **presentation-design-advisor** subagent (Tier 2), authoring the LLM layer over the
  already-assembled, deterministically-valid distilled spine (120 principles
  P001-P120 / 1359 claims from three distillation-only sources).
- `profile.yaml` derived from the 120 promoted principles: role, when/when-not-to-use, three
  modes (advise / review / plan), quality bar, forbidden behaviours, handoff rules, and a
  13-skill / 2-reference `knowledge_partition` covering every principle exactly
  once.
- 13 authored skills partitioning all 120 principles; 2 references
  (principles index + evidence notes).
- `reports/faithfulness-report.yaml` — every load-bearing profile rule graded WITHIN_SCOPE against
  its principles (no rule stronger than its evidence; the sources' own hedging on rehearsal
  guarantees, delivery style, and the measured comprehension gain is carried through).
- `tests/golden-tests.yaml` (7 golden, 3 negative-routing,
  2 missing-context) and `tests/principle-behaviour-tests.yaml` (one behaviour test per
  principle, 120 total).
- Claude Code adapter exported to `adapters/claude-code/` and installed under
  `.claude/agents/generated/`.

### Fixed
- `sources/metadata/*.metadata.json`: `source_type` normalised from the map->reduce short form
  `md` to the schema enum value `markdown`.

### Grounding
- Three distillation-only sources: *The Craft of Scientific Presentations* (Alley, 2013);
  *Resonate* (Duarte, 2010); and *slide:ology* (Duarte, 2008).
