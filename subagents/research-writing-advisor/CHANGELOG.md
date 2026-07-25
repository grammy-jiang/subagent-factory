# Changelog — research-writing-advisor

All notable changes to this generated subagent package are recorded here. Versions follow the
`agent_version` field in `profile.yaml`.

## [1.2.1] — 2026-07-25

### Fixed
- Re-exported the adapter so the `router_description` added in 1.2.0 actually reaches the runtime.
  The 1.2.0 entry below states that `export_claude_agent` "now honours an optional
  `router_description`" — that generator change was never committed (the field appeared nowhere in
  `tools/` on master), so the adapter kept shipping the truncated composed description while the
  changelog claimed otherwise. The exporter support landed separately; this re-export makes the
  package's own claim true. Profile text unchanged apart from the version.

## [1.2.0] — 2026-07-25

### Fixed (review-loop round 2 — must-fix)
- **Adapter `description` truncation (MF1).** The router description surfaced only the first
  `when_to_use` item and cut the `when_not_to_use` exclusion mid-list, under-firing on
  talk/slide/note requests and weakening the boundary signal. Fixed at the generator level
  (the S2 deferral in 1.1.0): `export_claude_agent._compose_description` now honours an
  optional `router_description` in the profile, used verbatim (clause-clipped to the 320-char
  budget) instead of the composed-from-clipped-clauses fallback. Added a complete, standalone
  `router_description` to `profile.yaml` covering the full in-scope span (writing, argument,
  structure, clarity, academic English, figures, sources, claims, slides, talks) plus the
  advice-only boundary (not writing it, not guaranteeing acceptance, not ruling on
  domain-science/legal-rights). Backward-compatible: profiles without the field are unchanged.
- **`source_of_truth_policy.canonical_owner` orphan field (MF2).** It carried no principle
  citations while the ledger guarantees every `source_of_truth_policy` value cites its
  principle(s). Added `(P080)` (author/team own the manuscript, data, and what to claim),
  `(P135)` (editors/reviewers own acceptance), and `(P140)` (counsel/institution own
  legal-rights/plagiarism) — the same IDs already used for these assertions in `handoff_rules`.

### Changed (review-loop round 2 — should-fix)
- **`role` DRY (SF3).** Removed the enumerated "never writes… never guarantees… never rules…"
  clause that restated `forbidden_behaviours` bullets 1/2/4 verbatim; `role` now points to
  `forbidden_behaviours` as the one authoritative statement of the hard boundaries. Also trims
  the largest profile-body contributor.
- **Faithfulness report coverage (SF4).** Extended `reports/faithfulness-report.yaml` from 19
  to 41 scored locations, adding the 13 `always_on` skill charters, `when_not_to_use[0-3]`,
  `minimum_useful_output`, `outputs.modes`, `canonical_owner`, and both `examples` — all graded
  WITHIN_SCOPE. Fixed two stale report notes (SF9): `forbidden_behaviours[3]` dropped P150
  (profile cites only P140); `handoff_rules[0]` dropped P022 (profile cites only P080).
- **Multisource deferral documented (SF5).** Added a ledger line stating why
  `multisource_synthesis: deferred` is correct for this 9-source package.
- **`when_to_use[4]` reworded (SF11)** to "wants recommendations for a durable writing practice"
  so the trigger reads unambiguously advisory rather than as a build/setup request.
- **Skill References footers (SF7).** Replaced the byte-identical boilerplate footer across all
  13 skills with a scoped trigger stating *when* to open each reference (principles-index only
  when a finding needs its full source-grounded statement or may belong to a sibling skill;
  evidence-notes only when the caller disputes a finding's grounding).
- **YAML block-scalar normalization (SF12).** `paper-sections-and-organization` and
  `slide-and-visual-design` frontmatter `description:` changed from `>` to `>-` to match the
  other 11 skills.

### Deferred
- SF6 (`paper-sections-and-organization` is the family outlier at ~29 steps) — the skill
  validates and is well under the 500-line body limit; moving grounded procedure steps into the
  compact principles index risks reducing actionability and fracturing the IMRaD charter the
  review itself cautions against splitting. Left as an advisory body-size optimization.

## [1.1.0] — 2026-07-25

### Changed (review-loop round 1 fixes)
- Re-authored all 13 skill bodies to the GOLD shape: `Procedure` and `Anti-patterns to flag`
  lines rebuilt from each principle's full statement (fixing mid-clause truncations such as
  `…while using (P050)`, `…delaying your true central characters when (P094)`, and the
  one-sided binary `Choose between point-first (P002)`), so no step or anti-pattern ends
  mid-clause before its citation. (M1)
- Added a routing `description:` frontmatter line to every skill. (S1)
- Removed the 7-item anti-pattern cap and rewrote each entry as an observable failure
  signature distinct from its paired procedure step; largest skills now cover one
  anti-pattern per principle. (S3, S4)

### Changed (profile faithfulness / grounding)
- Narrowed `source_of_truth_policy.precedence` P080 clause: author owns science/story and
  final language, but this never overrides the no-over-claim invariant. (S8)
- `forbidden_behaviours` domain-science/legal bullet: dropped mis-cited P150 (methodology
  fitness), marked domain-science authority an advice-only boundary, kept P140 for
  legal-rights/plagiarism. (S9)
- `handoff_rules[0]`: dropped structural P022 from the claim-authority clause; author owns
  substance (P080), claim-decision marked advice-only boundary. (S10)
- Restored P135's condition + exception ("whether a revision path is open… unless the
  required changes are genuinely impossible or unacceptable") in `knowledge_partition.always_on`. (S11)
- Added a `forbidden_behaviours` bullet barring fabricated/uncheckable citations and
  presenting copied source wording as the caller's own (P016, P026, P168). (S6)
- Trimmed `role`/`when_to_use`/`quality_bar`/`forbidden_behaviours` to bring the profile body
  back under the 1000-word budget (self-check ~981 w). (S5)
- Re-exported the Claude Code adapter from the updated profile.

### Deferred
- S2 (adapter `description` composed from clipped first when-to-use / when-not-to-use bullets,
  ending on a dangling list) is a shared-generator concern in
  `tools/subagent_factory/export_claude_agent.py::_compose_description` (a redesign affecting
  every package's adapter, with its own pinned test suite) — not a package-local or hand-edit
  fix (the installed adapter is generated and policy-forbidden to edit). Left for a
  generator-level change so this review-loop pass does not destabilise the factory.

## [1.0.0] — 2026-07-25

### Added
- Initial release of the **research-writing-advisor** subagent (Tier 2), authoring the LLM layer over the
  already-assembled, deterministically-valid distilled spine (172 principles
  P001-P172 / 3693 claims from nine distillation-only sources).
- `profile.yaml` derived from the 172 promoted principles: role, when/when-not-to-use, three
  modes (advise / review / plan), quality bar, forbidden behaviours, handoff rules, and a
  13-skill / 2-reference `knowledge_partition` covering every principle exactly
  once.
- 13 authored skills partitioning all 172 principles; 2 references
  (principles index + evidence notes).
- `reports/faithfulness-report.yaml` — every load-bearing profile rule graded WITHIN_SCOPE against
  its principles (no rule stronger than its evidence).
- `tests/golden-tests.yaml` (7 golden, 3 negative-routing,
  3 missing-context) and `tests/principle-behaviour-tests.yaml` (one behaviour test per
  principle, 172 total).
- Claude Code adapter exported to `adapters/claude-code/` and installed under
  `.claude/agents/generated/`.

### Grounding
- Nine distillation-only sources: *The Craft of Research* (4th ed., Booth et al., 2016); *Writing
  for Computer Science* (Zobel, 2014); *Writing Science* (Schimel, 2012); *English for Writing
  Research Papers* (Wallwork, 2016); *Science Research Writing for Non-Native Speakers of English*
  (Glasman-Deal, 2010); *How to Write a Lot* (Silvia, 2007); *How to Take Smart Notes* (Ahrens,
  2017); *Presentation Zen Design* (Reynolds, 2010); and *TED Talks* (Anderson, 2016).
