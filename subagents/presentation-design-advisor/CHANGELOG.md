# Changelog — presentation-design-advisor

All notable changes to this generated subagent package are recorded here. Versions follow the
`agent_version` field in `profile.yaml`.

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
