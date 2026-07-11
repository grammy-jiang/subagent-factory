# Changelog — descriptive-translation-reviewer

All notable changes to this generated subagent package are recorded here. Versions follow the
`agent_version` field in `profile.yaml`.

## [1.3.0] — 2026-07-12

Review-loop round 3 (`reports/review-loop/descriptive-translation-reviewer.r3.review.md`): applied the
must-fix and the high-value should-fixes, staying grounded in the existing 180-principle spine.

### Fixed
- **M1 — stale citation in `examples[1]`** — the never-translate/never-sign-off note cited
  `(forbidden behaviours, P070, P100)`, but v1.2.0 had dropped P070/P100 from the matching
  `forbidden_behaviours[0]` as an uncited-by-design product-scope boundary. P100 appeared nowhere else,
  making it a dangling citation. Changed to `(forbidden behaviours)` so the example matches the rule.
- **S3 — `minimum_useful_output`** — the bar was phrased only in review-mode "flaw" terms; broadened to
  gate `advise` (recommendation + orientation) and `compare` (brief-weighted side-by-side) as well.
- **S4 — `when_to_use[2]`** — reworded the garden-path/comma-spliced fluency-and-visibility trigger into
  a single unambiguous sentence (it seeds the exported routing description).
- **S5 / S6 — `when_not_to_use[0]`** — narrowed the routed-away scope to the linguistic-equivalence
  **mechanism** (disjoint from this package's orientation-fit judgment in P106/P109), and reordered so the
  exported `description` surfaces the `translation-equivalence-advisor` sibling cue within the router's
  character budget.
- **S8 — House's two same-named axes** — `register-discourse-and-audiovisual-constraints` Purpose now
  states the overt/covert translation-**type** typology (P021) and the overtly-/covertly-**erroneous**
  error taxonomy (P065) name different judgments and are not to be conflated.
- **S9 — theorist attribution** — named the originators at point of use: Lefevere (refraction/rewriting,
  P001/P050), Even-Zohar/polysystem (P002), Vermeer (Auftrag/skopos, P009/P062), with the echoing skill
  steps updated to match. Attribution only; no claim strengthened.

### Changed
- **S1 — faithfulness coverage** — `faithfulness-report.yaml` extended from 20 to 35 findings, adding the
  12 `knowledge_partition.always_on` bullets, `minimum_useful_output`, and `when_not_to_use[0..4]`
  (all WITHIN_SCOPE, no over-claim).
- **S2 — provenance accounting** — the ledger's citation-accounting sentence now lists `examples` and
  declares example citations audited + re-checked on every version bump (M1's root cause).

### Deferred
- **S7 — skill-body footprint** — an optimization on a passing package; all 12 skills already sit under
  the 500-line factory limit. Left to a dedicated pass to avoid regression risk. NICE items N1-N14 not applied.

## [1.2.0] — 2026-07-12

Review-loop round 2 (`reports/review-loop/descriptive-translation-reviewer.r2.review.md`): applied
the 3 must-fixes and the high-value should-fixes, staying grounded in the existing 180-principle spine.

### Fixed
- **M1 — Chaume signifying-code count** — P019 said "ten" but broke into 1+4+6 = 11. Corrected to
  "one linguistic, three acoustic and six visual" (= 10) in P019, and reworded the matching
  `register-discourse-and-audiovisual-constraints` Procedure step to "one linguistic code, three
  further acoustic codes, and six visual codes" so principle and skill agree on one reading.
- **M2 — `quality_bar[2]` over-claim** — "Translation **is** driven by an explicit brief and the
  text's predominant function" stated a functionalist/skopos prescription as settled fact (the exact
  anti-pattern `forbidden_behaviours[2]` forbids). Hedged to "Where a brief and predominant function
  apply, translation is judged against them; a fulfilled skopos never excuses micro-level neglect".
- **M3 — Adapter routing `description`** — the exported `description` truncated mid-clause
  ("…wants its equivalence — Not for:") and dropped the sibling-routing disambiguator. Reworded
  `when_to_use[0]` so its clipped clause reads as a complete sentence, and reordered `when_not_to_use`
  so the sibling-axis routing bullet leads (surfacing it in the routing description); re-exported.
  The v1.1.0 ledger claim that the description had already been repaired is corrected below.

### Changed
- **S1 — Profile body trimmed** from ~931 to ~851 words: dropped the duplicated sibling-routing
  `handoff_rules[2]` (routing now stated once, in `when_not_to_use`) and tightened role, modes,
  `quality_bar`, and `when_*` prose. Residual (~851w) is above the 800-word soft budget, so the
  `body-size` self-check still emits a non-blocking WARNING (FAIL threshold is 1000).
- **S4** — `quality_bar[1]` gains P059 (illusory equivalent effect), matching `knowledge_partition`.
- **S5** — `forbidden_behaviours[0]` citations (P070, P100) dropped; the "never translate / never
  sign off" boundary is a product-scope decision, left as an uncited scope boundary.
- **S7** — P106 and `equivalence-orientations-and-effect` step 6 reworded: Koller's five relations
  weighed against each other as simultaneous competing frames, not a fixed-order escalation ladder.
- **S8** — P121 no longer mis-dates Newmark's semantic/communicative pair as "1960s-70s" theory;
  the decade qualifier is dropped.
- **S9(a)** — `meaning-signification-and-equivalence-critique` description no longer repeats the same
  clause verbatim twice.
- **S2** — `tests/golden-tests.yaml` re-stamped `profile_version: 1.2.0`, `tier: 2`.
- `agent_version` 1.1.0 → 1.2.0.

## [1.1.0] — 2026-07-12

Review-loop round 1 (`reports/review-loop/descriptive-translation-reviewer.r1.review.md`): applied
all must-fixes and the high-value should-fixes, staying grounded in the existing 180-principle spine.

### Fixed
- **Adapter invariant layer truncation** — the installed/canonical adapter had 101 `…`-severed
  invariant lines and a mid-clause frontmatter `description`. Re-exported through the current
  `compile_invariants`/`export_claude_agent` path so each invariant renders its full principle
  sentence and the routing description ends at a clause boundary.
- **Skill bodies re-authored to the GOLD shape** — all 12 `skills/*/SKILL.md` rewritten so every
  Procedure and Anti-patterns bullet is a complete, self-contained sentence before its `(Pxxx)` cite
  (removing the mid-clause truncations such as "Surface a translation's (P113)."), Anti-patterns now
  cover every principle in the skill (not a silent 7-item cap) as concrete bad-finding symptoms, and
  each gains a `description:` frontmatter field for routing. Frontmatter provenance preserved.
- **Faithfulness re-grounding** — `handoff_rules[0]` re-anchored to P029 (publisher holds the publish
  decision) + P070 (macro/micro split), dropping the mis-grounded P009/P162/P080; `handoff_rules[1]`
  re-anchored to P029 for commercial/economic constraints. `faithfulness-report.yaml` gains entries
  for `handoff_rules[0..2]` and `canonical_owner`.
- **Cross-sibling routing** — `when_not_to_use` + `handoff_rules` now name `translation-equivalence-advisor`,
  `translation-quality-reviewer`, and `technical-translation-advisor` by slug/axis; `when_to_use[0]`
  differentiated from the quality-reviewer sibling.
- **Faithfulness weakening** — P047 no longer states Blum-Kulka's explicitation hypothesis as
  "confirmed by corpus study" (now a proposed, contested tendency with varying support); P115 frames
  the technical-texts-easier point as Ortega's comparative observation and marks technical/scientific
  subject-matter risk out of remit.

### Changed
- `tier: 1` → `tier: 2` (3-source manifest; matches siblings and the build record).
- Profile body trimmed (removed quality_bar/forbidden redundancy) toward the word budget.
- `agent_version` 1.0.0 → 1.1.0.

## [1.0.0] — 2026-07-12

### Added
- Initial release of the **descriptive-translation-reviewer** subagent (Tier 1), authoring the LLM layer over the
  already-assembled, deterministically-valid distilled spine (180 principles P001-P180 /
  984 claims from three distillation-only sources).
- `profile.yaml` derived from the 180 promoted principles: role, when/when-not-to-use, three modes
  (review / advise / compare), quality bar, forbidden behaviours, handoff rules, and a
  12-skill / 2-reference `knowledge_partition` covering every principle exactly
  once.
- 12 authored skills partitioning all 180 principles; 2 references
  (principles index + evidence notes).
- `reports/faithfulness-report.yaml` — every load-bearing profile rule graded WITHIN_SCOPE against
  its principles (no rule stronger than its evidence).
- `tests/golden-tests.yaml` (6 golden, 2 negative-routing,
  2 missing-context) and `tests/principle-behaviour-tests.yaml` (one behaviour test per
  principle, 180 total).
- Claude Code adapter exported to `adapters/claude-code/` and installed under
  `.claude/agents/generated/`.

### Grounding
- Three distillation-only sources: Jeremy Munday, *Introducing Translation Studies* (2016);
  Lawrence Venuti, ed., *The Translation Studies Reader* (2012); Gideon Toury, *The Nature and Role
  of Norms in Translation* (1995).
