# Changelog — learning-science-advisor

All notable changes to this generated subagent package are recorded here. Versions follow the
`agent_version` field in `profile.yaml`.

## [1.1.0] — 2026-07-27

Review round 1 (`/review-subagent learning-science-advisor`) — all must-fix and all high-value
should-fix findings applied. See `provenance-ledger.md` § Version History for the supersession
reasoning behind each change.

### Fixed
- **All 15 skills — `## Anti-patterns to flag` rewritten.** Every bullet was a machine-emitted
  "Overlooking Pxxx: <restated principle>" cut at a fixed character budget and closed with a bare
  period, so the agent loaded a checklist of severed half-sentences ("…and can improve.", "…while
  allowing.", "…that must."). Replaced with deliberately written failure modes, **one per principle,
  1:1 with `## Procedure`** — which also removes the silent 7-bullet cap that had dropped roughly
  half the principles in 9 of the 15 skills.
- **Two truncated `## Procedure` steps** completed from their own principle statements: P115 in
  `development-diversity-and-individual-differences` and P068 in
  `elaboration-examples-and-self-explanation`.
- **`router_description`** now names mnemonic and memory systems and recall reliability. The
  `memory-mnemonics-and-recall-accuracy` skill is `always_on` but appeared nowhere in the routing
  surface, so a shipped capability was unreachable.
- **`quality_bar[2]`** restores P125's own hedge — distributed practice as a *high-utility default*,
  "except where complex structured learning or higher-order outcomes leave the benefit uncertain".
  The unconditional wording contradicted `source_of_truth_policy.precedence`, which commits to
  carrying source hedging through.
- **Two further hedge slips** corrected against their principles: P050's "**can** reinforce confident
  errors" and P115's "an average age trend **in speeded reasoning**".
- **`skills/evidence-appraisal-and-learning-myths`** no longer cites P039, which belongs to
  `expertise-development-and-transfer`'s principle set.

### Added
- A `description:` frontmatter line on each of the 15 skills, so a caller's topic can be matched to
  the right skill file.
- `quality_bar[6]` — an authored output floor carrying `outputs.primary_format` and
  `minimum_useful_output` into the exported adapter, which the export template renders from neither.
- `forbidden_behaviours[5]` and `handoff_rules[2]` — the guardrail and named-authority halves of the
  education-law / accreditation / safeguarding / institutional-policy boundary that previously
  existed only in `when_not_to_use[4]`.
- `inputs.required` — a missing-context rule (ask for learners, target competence, and time rather
  than assuming defaults) and a Glob/Grep + skill-selection rule that motivate the adapter's two
  granted tools.
- `reports/faithfulness-report.yaml` extended **29 → 50 findings**: one per
  `knowledge_partition.always_on[0..14]` and per `examples[*].ideal_response` — the technique-level
  claims carrying the effect sizes and myth refutations, previously ungraded — plus the three new
  authored fields. All 50 grade `WITHIN_SCOPE`.
- `provenance-ledger.md` — an authored-field table (why `quality_bar[6]`,
  `forbidden_behaviours[5]`, `handoff_rules[2]` carry no principle citation), a note resolving
  P092/P098's `profile_rule: false` against their `always_on` citations, and a note on why
  `multisource_synthesis: deferred` is expected for a P0-authored layer.

### Changed
- `role`, `when_to_use`, `when_not_to_use`, `outputs.primary_format`, `minimum_useful_output`, and
  the three mode trigger/output lines compressed to absorb the additions within the profile body
  budget (985 words; hard limit 1000). No claim dropped — only prose.
- `when_to_use[1]` opens with "Investigating" rather than "Diagnosing", which was the verb marking
  the forbidden case ("diagnosing a learner").
- Adapter re-exported from the updated profile.

### Unchanged
- The distilled spine — 150 principles, 5006 claims, evidence records, anchors — the
  skill→principle partition, every skill's frontmatter `provenance` block (including
  `authored_from_digest`), and both test suites.

## [1.0.0] — 2026-07-26

### Added
- Initial release of the **learning-science-advisor** subagent (Tier 2), authoring the LLM layer over the
  already-assembled, deterministically-valid distilled spine (150 principles
  P001-P150 / 5006 claims from twelve distillation-only sources).
- `profile.yaml` derived from the 150 promoted principles: role, when/when-not-to-use, three
  modes (advise / review / plan), quality bar, forbidden behaviours, handoff rules, and a
  15-skill / 2-reference `knowledge_partition` covering every principle exactly
  once.
- 15 authored skills partitioning all 150 principles; 2 references
  (principles index + evidence notes).
- `reports/faithfulness-report.yaml` — every load-bearing profile rule graded WITHIN_SCOPE against
  its principles (no rule stronger than its evidence; the sources' own hedging on far transfer,
  durability and classroom generality is carried through).
- `tests/golden-tests.yaml` (7 golden, 3 negative-routing,
  2 missing-context) and `tests/principle-behaviour-tests.yaml` (one behaviour test per
  principle, 150 total).
- Claude Code adapter exported to `adapters/claude-code/` and installed under
  `.claude/agents/generated/`.

### Fixed
- `sources/metadata/*.metadata.json`: `source_type` normalised from the map->reduce short form
  `md` to the schema enum value `markdown`.

### Grounding
- Twelve distillation-only sources: Dunlosky et al. (2013); *Make It Stick* (Brown, Roediger &
  McDaniel, 2014); *Understanding How We Learn* (Weinstein & Sumeracki, 2018); *Principles of
  Instruction* (Rosenshine, 2012); *How Learning Works* (Ambrose et al., 2010); *Why Don't Students
  Like School?* (Willingham, 2009); *Powerful Teaching* (Agarwal & Bain, 2019); *Small Teaching*
  (Lang, 2016); *Small Teaching Online* (Darby & Lang, 2019); *Visible Learning* (Hattie, 2008);
  *The Science of Learning* (Deans for Impact); and *How People Learn II* (NASEM, 2018).
