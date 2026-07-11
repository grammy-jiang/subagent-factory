# Changelog — translation-equivalence-advisor

All notable changes to this generated subagent package are recorded here. Versions follow the
`agent_version` field in `profile.yaml`.

## [1.2.7] — 2026-07-12

### Fixed
- **P094 CONTRADICTION (adversarial-verify triage residual).** The review-loop's own r4 narrowing
  over-corrected P094 into "this is stylistic concordance, not subject-matter terminology
  consistency", which CONTRADICTS its source claim C00360 (concordant rendering is useful
  *especially for key terms in technical or philosophical texts*). Restated P094 as a
  formal-equivalence device — keep concordance where readers must track a recurring key term (incl.
  technical/philosophical texts) for study/interpretation, relax it where rigid consistency makes the
  receptor text unnatural or meaningless (C00360/C00361). Re-synced the dynamic-and-formal-equivalence
  skill step 6 and profile `handoff_rules`: mandated subject-matter *glossary governance* routes to
  technical-translation-advisor as an ownership boundary, not a redefinition of concordance. Adapter
  re-exported.

## [1.2.6] — 2026-07-12

### Fixed
- **Test hygiene (r1 MF1):** the Phase-8 self-check and golden-test artifacts were stale relative to the
  shipped `agent_version` — `golden-tests.yaml` `profile_version` read 1.2.4 and `tests/test-results.md` was
  generated pre-v1.2.5. Regenerated `test-results.md` via `cli selfcheck` against the current profile, bumped
  `golden-tests.yaml` `profile_version` → 1.2.6, re-confirmed the body-size WARNING against the fresh count,
  and re-exported the adapter.

### Changed
- **Routing/scope (r1 SF5, SF6):** `when_not_to_use[0]` reworded to name the real disambiguating axis rather
  than theory-topics — a sibling-axis "review my translation" (equivalence-as-evidence-for-a-norm,
  domestication/foreignization, translator (in)visibility → descriptive; a *systematic ST-vs-TT register
  profile* (House field/tenor/mode) or corpus metrics → quality-reviewer; technical usability/terminology →
  technical) versus the linguistic equivalence mechanism itself (typicality, cohesive-tie fit, register as one
  local factor), which stays here. No profile claim changed.
- **Faithfulness (r1 SF7):** `handoff_rules[1]` reworded so the unqualified "terminology consistency" now reads
  "source-term concordance (stylistic or study tracking, not subject-matter glossary consistency)", carrying
  the v1.2.5 P094 scope-narrowing instead of re-claiming the narrowed-away subject-matter scope (P094, P115).
- **Faithfulness (r1 SF4):** `pragmatic-equivalence-coherence-and-implicature` step 3 hedged — any cited
  discourse/rhetoric norm is read as a loose tendency to verify against the actual target readership, not a
  fixed national pattern (grounded in P033's culture-relative claim + P019/P020 target-reader assessment).
- **Reference drift (r5 MF1 / out-of-scope note):** `references/translation-equivalence-principles-index.md`
  P094 and P100 lines updated to the current `principles.yaml` wording (the round-4 stylistic-concordance and
  pedagogical-illustration narrowings), which the index had not carried.

### Added
- **Agent design (r1 SF8):** a fourth `examples` entry (`kind: happy-path`) exercising `compare` mode — a
  side-by-side of formal vs dynamic equivalence for one emotive segment under a stated brief, ending in a
  purpose-weighted recommendation (P021, P034, P035, P022, P005, P078).
- **Skill-authoring (r1 SF9):** one grounded `## Worked example` (source snippet → flaw at that lens →
  strategy → residual loss, citing only that skill's own principle ids) added to all nine skills, closing the
  operational-recipe gap the earlier rounds deferred.
- **Skill-authoring (r1 SF10):** run-on decision-table procedure steps reformatted into nested bullet lists —
  `word-level-nonequivalence-and-strategies` step 5 and `dynamic-and-formal-equivalence` steps 2/5/8 — one
  option/strategy + citation per line for live-review scannability. (`collocation-idiom` step 5 was a
  single-clause step, not a crammed table, so only the worked example was added there.)

### Deferred
- **SF1 (inclusive-language / singular-they options)** and **SF3 (regulated-domain back-translation QA role)**
  require claims absent from the two grounded sources (Baker 1992, Nida 1964) — same deferral as v1.2.0 (S5)
  and v1.2.3 (S6); applying them would introduce ungrounded claims.
- **SF2 (relabel Grice's fourth maxim "Relevance" → "Relation")** NOT applied: P032 and Baker's own *In Other
  Words* name the maxim "Relevance"; switching to "Relation" would make the package *less* faithful to its
  source, not more. Left as-is.
- **N1–N14** — non-blocking NICE items (dated-source hedges, ledger archiving, adapter-template phrasing),
  carried forward with the same discipline as prior rounds.

## [1.2.5] — 2026-07-12

### Fixed
- **Routing (r4 MF1):** the exported adapter `description` — the only pre-dispatch signal an orchestrator
  sees — kept only the first `when_to_use`/`when_not_to_use` bullet, dropping the review-mode trigger and
  the load-bearing sibling-redirect clause (a misrouting risk across four near-identical siblings). General
  compiler fix in `tools/subagent_factory/export_claude_agent.py` `_compose_description`: budget 320→640 and
  per-clause clips widened (exclusion 85→320, triggers 85→90) so a second trigger and a full sibling-redirect
  exclusion survive; `when_not_to_use` reordered so the sibling-redirect is the primary exclusion. No profile
  claim changed.

### Changed
- **Faithfulness (r4 SF1):** P100 back-translation scoped to its pedagogical-illustration origin (Baker) so
  the rule no longer reads as a blanket "never use back-translation"; it is "not by itself a general test of
  translation quality." `dynamic-and-formal-equivalence` step 7 reworded to match.
- **Faithfulness (r4 SF2):** P094 concordance narrowed to stylistic/literary concordance and scoped out of
  subject-matter terminology consistency (routed to `technical-translation-advisor`); step 6 reworded to match.
- **Terminology (r4 SF3):** grounded provenance note that "dynamic equivalence" is Nida's own (1964) term
  added to the `dynamic-and-formal-equivalence` skill and the key-concepts glossary (no operational change;
  the external "functional equivalence" reframing is out of source scope and not added).
- **Terminology (r4 SF4):** key-concepts "Adequacy" entry disambiguated — it is Nida's fitness-for-brief
  sense here, not a source-oriented technical label, so it is not read as the antonym of "acceptable" when a
  finding is carried into a descriptive-norms review.
- **Skill-authoring (r4 SF5):** the repeated advise/review/compare Output boilerplate (9×) moved once into
  the key-concepts "Response-shape protocol" section; each skill `Output` now states only its domain-specific
  finding fields plus a pointer.
- **Skill-authoring (r4 SF6):** a concrete "Use when a caller asks/says…" trigger added to the eight skill
  descriptions that lacked one, prioritising the confusable pairs (thematic vs cohesion; pragmatic vs cohesion).
- **Skill-authoring (r4 SF7):** `thematic-and-information-structure` step 5 now notes reference-tracking
  mechanics belong to `cohesion-and-texture`; this skill only reads a referenced participant's given/new status.
- **Agent design (r4 SF8):** a third worked example added exercising `review` mode (a short draft returned as
  a findings list across pragmatic/collocation/information-structure levels).
- **Body-size (r4 SF10):** two quality_bar clauses tightened to buy back headroom under the 1000-word
  hard-fail (~968 words).

### Deferred
- N1–N4 (dated-source hedges, inline-citation widening, Baker 3rd-ed. fold-in, ledger polish) — non-blocking
  NICE items. The external parts of SF3/SF4 (Nida's later "functional equivalence"; Toury's adequate/acceptable
  dichotomy) are out of this package's source scope and were addressed only via grounded, self-referential notes.

## [1.2.4] — 2026-07-12

### Fixed
- **Faithfulness (r3 MF-1):** `forbidden_behaviours[3]` restated P038 ("rework, don't transfer cohesion")
  as a hard-forbidden absolute, omitting **P091** (which licenses following source cohesion when the
  translation's purpose calls for it) — the same P038-vs-P091 conflict already reconciled in
  `always_on[4]`. Split so thematic markedness / voice / tense-aspect stay absolute (P024, P009, P046)
  while the cohesion clause is conditioned "where the purpose does not call for following source cohesion"
  and cites P038, P091. Faithfulness-report `forbidden_behaviours[3]` re-graded EXACT_SUPPORT → WITHIN_SCOPE
  with the correction note.
- **Faithfulness (r3 SF-1):** `quality_bar[4]` cohesion criterion "reworked, not transferred" (categorical,
  P091 omitted) → "reworked by default, not transferred … unless the translation's purpose favours
  following source patterns (P038 … P091)"; faithfulness-report note updated.
- **Routing (r3 SF-7):** added a fourth `when_not_to_use` disambiguator naming the three corpus siblings and
  their distinct lenses — norms/retranslation/visibility → descriptive-translation-reviewer; corpus quality
  metrics or register profile → translation-quality-reviewer; technical-document usability/terminology →
  technical-translation-advisor.
- **Body-size (r3 MF-3):** trimmed the profile body off the 1000-word hard-fail edge (was ~1000, 0 headroom)
  to ~974 while absorbing the MF-1/SF-1/SF-7 additions — collapsed the `quality_bar` per-clause citation
  lists to their primary principle IDs (the full clusters remain in `knowledge_partition.always_on` and the
  faithfulness report) and tightened the two heaviest clauses plus `modes`, `role`, `handoff`, and
  `precedence`. Residual body-size **WARNING** is grounding-bounded: the body faithfully encodes nine
  equivalence levels with their source hedges, which cannot be cut further without HEDGING_REMOVED
  regressions.
- **Test hygiene (r3 MF-2):** Phase-8 `tests/test-results.md` regenerated and the adapter re-exported against
  v1.2.4 (both prior artifacts still read 2026-07-11 / v1.2.2); `golden-tests.yaml` `profile_version` → 1.2.4.

Deferred (out of grounding scope or lower value): SF-2 (P009 confidence downgrade — P009 is a compiled
adapter invariant; a confidence change alters the must-hold invariant set, out of scope for a faithfulness
patch), SF-3 (P066 "always-definite" — a domain-typology critique, not a source over-claim; softening would
understate Baker), SF-4/SF-5/SF-6/SF-8/SF-9 and the NICE items (glossary coverage, per-skill worked
examples, procedure sub-bullets, report-filename traceability, Nida-1986 "functional equivalence" note) —
carried to a future skill-authoring / source-addition cycle, same discipline as the v1.2.0–v1.2.3 deferrals.

## [1.2.3] — 2026-07-12

### Fixed
- **Faithfulness (r2 M1):** `knowledge_partition.always_on[0]` hardened conditional P095 into an
  unconditional prohibition — "never erase a culturally embedded item merely to sound natural"
  (HEDGING_REMOVED). Reworded to "…when its foreignness carries meaning for the text (P095)", restoring
  P095's condition and aligning with the word-level skill and `examples[0]`.
- **Faithfulness (r2 M2):** `knowledge_partition.always_on[4]` opened with an absolute "Do not transfer
  the source text's cohesive devices" (P038) yet closed with a purpose-conditioned exception (P091) — an
  internal contradiction. Reframed as default-with-exception: "As a default (P038)… but, as a
  purpose-driven exception (P091), decide … by the translation's purpose."
- **Faithfulness (r2 S1):** `quality_bar[7]` and `always_on[7]` restated P041 as unconditional
  register-matching (HEDGING_REMOVED). Appended "unless the brief calls for preserving source-culture
  flavour" (P041) to both; `skills/register-style-and-literary-form` step 2 and its anti-pattern carry the
  same exception.
- **Faithfulness (r2 S2):** `examples[1].ideal_response` dropped the genre-default clause ("a marketing
  brief typically prioritizes the receptor's response") it told the advisor not to assume — now "ask what
  this brief's purpose and audience favour before setting the orientation, without defaulting by genre
  (P034, P041, P021)".
- **Mode coverage (r2 S4):** added a `compare`-mode branch to the `## Output` of the remaining seven
  skills — word-level (P106), collocation-idiom (P044), thematic (P024), cohesion (P091), pragmatic
  (P050), register (P005), grammatical (P046) — mirroring the two skills that already had it.
- **Routing (r2 S7):** `when_to_use[1]` tightened so the exported router `description` surfaces the
  review-mode trigger alongside the culture-specific-item trigger.
- **Routing (r2 S8):** `skills/text-level-approach-and-limits-of-equivalence` frontmatter `description`
  folds in the concrete caller phrasing ("right," "literal enough," "faithful") that most naturally selects it.
- **Faithfulness-report (r2 S3):** notes for `always_on[0]`, `always_on[4]`, `quality_bar[7]`, and
  `always_on[7]` re-graded from silently-clean to documented "Corrected in v1.2.3" entries.
- **Test hygiene (r2 S10):** Phase-8 `test-results.md` regenerated and adapter re-exported against v1.2.3.

Deferred (out of grounding scope): S5 (P015 inclusive-language / singular-they options) and S6 (P100
regulated-domain back-translation QA role) require claims absent from the two grounded sources (Baker 1992,
Nida 1964); S9 (missing v1.2.2 review-loop artifact) and the NICE items are non-blocking. Same discipline
as the v1.2.0/v1.2.2 deferrals.

## [1.2.2] — 2026-07-12

### Fixed
- **Routing (SF-1):** seven skill `description` openers broadened from "Reviews …" to "Diagnoses and
  reviews …" so the load-time trigger covers the pre-draft advise/diagnose path the bodies already build
  (mirrors the `word-level` skill).
- **Mode coverage (SF-2):** added a `compare`-mode branch to the `## Output` of
  `dynamic-and-formal-equivalence` (P021) and `text-level-approach-and-limits-of-equivalence` (P079) —
  side-by-side favours/costs before a purpose-weighted recommendation.
- **Faithfulness (SF-3):** `quality_bar[0]` "No one-to-one match at word level" → "Don't assume a
  one-to-one match at word level" to restore P037's hedge (never *assume* one-to-one). Faithfulness-report
  `quality_bar[0]` note extended (SF-13).
- **Faithfulness (SF-6):** `examples[1].ideal_response` de-genre-defaulted from "a marketing text usually
  calls for dynamic equivalence" to brief-conditioned wording (P034, P041, P021); root cause
  `.build/authoring/gen.py` fixed.
- **Grammatical (SF-5, SF-9):** step 3 adds the grounded caveat that "masculine as unmarked" is a
  structural fact, not a target default (restructure where the distinction is arbitrary — P015); step 6
  relabelled to P084's grammar (closed/obligatory) vs lexis (open/optional) contrast.
- **Dynamic-formal (SF-8):** anti-pattern added — a fluent read is not proof of equivalent effect;
  "similar audience response" is a directional target tested across audience and context, not a single
  pass/fail (P035, P036).
- **Test hygiene (SF-10):** `golden-tests.yaml` `profile_version` → 1.2.2; Phase-8 `test-results.md`
  regenerated against the v1.2.2 profile (MF-2).
- **Provenance/faithfulness (SF-12):** ledger per-field citation claim qualified for
  `forbidden_behaviours[0]` (declared advisory-boundary policy, no inline citation by design).

Deferred (out of grounding scope): SF-4 back-translation QA role and SF-7 Nida-1986 "functional
equivalence" rename require claims absent from this spine; SF-11 adapter description-synthesis is a shared
factory-template concern.

## [1.2.1] — 2026-07-12

### Fixed
- **Faithfulness (verify1 MF-1):** `skills/grammatical-equivalence/SKILL.md` step 7 conflated a
  term-TYPE with a STRATEGY — it classified terms as "ordinary parallels, functional equivalents, or
  borrowings", silently swapping P055's diagnostic third category "culture-specific items" for the
  strategy "borrowings" and dropping "cultural" from the second. Restated to P055's sense (ordinary
  parallels / functional cultural analogues / culture-specific items), with strategy choice deferred to
  the word-level skill — restoring the package's own no-map-type-to-strategy discipline.
- **Faithfulness (verify1 MF-2):** `profile.yaml` `quality_bar[0]` broadened word-scoped P037/P001 to
  "word **or phrase** level" — a SCOPE_BROADENED extension the citations do not support (phrase/
  collocation level is governed by P042/P043 target-typicality, which presupposes typical target
  patterns often exist). Narrowed to "word level"; phrase/collocation/idiom coverage stays in
  `quality_bar[1]`.

## [1.2.0] — 2026-07-12

### Changed
- **Faithfulness (must-fix MF-1):** the receptor-response over-claim corrected in `quality_bar[6]` at
  v1.1.0 was still live verbatim in four non-profile artifacts — the `dynamic-and-formal-equivalence`
  skill Purpose and anti-pattern, the key-concepts glossary Adequacy entry, and golden test GT-004
  (`must_do`/`minimum_output`). All rewritten brief-conditioned (receptor response for a dynamic task;
  closeness to source form and structure where readers need that access, per P022/P035). Root cause
  `.build/authoring/gen.py` fixed so regeneration will not reintroduce it.
- **Faithfulness (must-fix MF-2):** `quality_bar[1]` reversed P044's hedge — "assume no idiom has a
  target equivalent" (presume none) instead of P044's "do not assume an idiom has a target equivalent"
  (stay agnostic), which also biased against P014's similar-meaning-and-form idiom strategy. Reworded to
  match `always_on[1]` and P044. `faithfulness-report.yaml` `quality_bar[1]` note corrected.
- **Routing (should-fix SF-1):** `when_to_use` reordered so the most distinctive triggers
  (culture-specific item/idiom/collocation/marked-structure/poetic-form and whole-text review) occupy
  the first two slots the exported router `description` samples, instead of dropping them.
- **Scope clarity (should-fix SF-2):** `review` mode output now states that "correction" names the
  strategy or target-language device, not verbatim replacement prose that would reconstruct the finished
  text (consistent with `forbidden_behaviours[0]`).
- **Provenance (should-fix SF-5):** the Nida source citation dropped the fabricated subtitle "dynamic
  and formal equivalence" and now records that this source is a derived ~10k-word secondary extract, not
  the primary monograph (matching `sources/metadata` `authority: secondary`).
- **Profile size (should-fix SF-6):** `quality_bar` clauses trimmed to keep the body under the 1000-word
  hard limit after the MF-1 propagation.
- **Advise-mode fit (should-fix SF-3):** eight skill `## Output` sections gained a no-draft branch —
  in `advise` mode (no draft supplied) state the recommended strategy and its principle directly rather
  than critique a draft that does not exist.
- **Test hygiene (should-fix SF-7/SF-8):** `golden-tests.yaml` `profile_version` bumped to 1.2.0 and the
  Phase-8 `test-results.md` self-check regenerated against the v1.2.0 profile.

### Grounding
- No new claim introduced: every edited rule restates principles already in `principles/principles.yaml`
  (P001–P116). SF-9…SF-14 and NICE items that would require claims from outside the two grounded sources
  (regulatory back-translation mandates, Nida's 1986 "functional equivalence" relabel, Kaplan-critique
  hedges, inclusive-language policy) were deliberately NOT applied.

## [1.1.0] — 2026-07-12

### Changed
- **Faithfulness (must-fix M2):** `quality_bar[6]` no longer asserts the universal negation "adequacy
  is judged by receptor response, **not** formal closeness" (stronger than P021/P034/P035/P022 — P022
  endorses formal-equivalence/gloss for close source access; P035 lists four adequacy criteria). Rewritten
  brief-conditioned: adequacy judged by the brief's own criterion (sense/spirit/natural expression/similar
  response for receptor-response tasks; closeness to source form and structure when readers need it).
- **Faithfulness (should-fix S9):** `source_of_truth_policy.precedence` reworded from "preserve it only
  where…" to the graded "preserving it more strongly where…" to match P005's graded wording.
- **Routing (should-fix S1):** `when_to_use[0]` split so its first sentence is a complete clause, giving
  the exported router `description` a well-formed, scope-signalling trigger instead of a mid-list cut.
- **Profile size (should-fix S2):** `quality_bar` compressed (shared "function, not form" framing tightened)
  to reclaim body-word headroom against the 1000-word hard limit.
- **Skill lens-fit (should-fix S8):** `text-level-approach-and-limits-of-equivalence` "When to use"
  tightened to its distinct whole-text/relative-standard trigger (was overlapping every sibling skill).
- **Adapter (must-fix M1):** re-exported so the `## Operating invariants (must hold)` layer emits P038
  and P058 whole (the stale adapter truncated them mid-clause with a trailing `…`; `compile_invariants`
  was already fixed upstream, this package's adapter predated the fix).

### Grounding
- No new claim introduced: every edited rule restates principles already in `principles/principles.yaml`
  (P001–P116). Faithfulness-report entries for `quality_bar[6]` and `precedence` updated accordingly.

## [1.0.0] — 2026-07-11

### Added
- Initial release of the **translation-equivalence-advisor** subagent (Tier 2), authoring the LLM layer over the
  already-valid distilled spine (116 principles P001–P116, 415 claims, two distillation-only
  sources).
- `profile.yaml` derived from the 116 promoted principles: role, when/when-not-to-use, three modes
  (advise / review / compare), a nine-bullet quality bar, forbidden behaviours, handoff rules, and a
  nine-skill / two-reference `knowledge_partition` covering all principles exactly once.
- Nine authored skills: word-level-nonequivalence-and-strategies, collocation-idiom-and-fixed-expression, grammatical-equivalence, thematic-and-information-structure, cohesion-and-texture, pragmatic-equivalence-coherence-and-implicature, dynamic-and-formal-equivalence, register-style-and-literary-form, text-level-approach-and-limits-of-equivalence.
- Two references: translation-equivalence-principles-index, translation-equivalence-key-concepts.
- `reports/faithfulness-report.yaml` — every load-bearing profile rule graded EXACT_SUPPORT or
  WITHIN_SCOPE against its principles (no rule stronger than its evidence).
- `tests/golden-tests.yaml` (5 golden, 2 negative-routing, 2 missing-context) and
  `tests/principle-behaviour-tests.yaml` (one behaviour test per principle, 116 total).
- Claude Code adapter exported to `adapters/claude-code/` and installed under
  `.claude/agents/generated/`, with the five high-confidence principles compiled into the
  `## Operating invariants (must hold)` layer.

### Grounding
- Two distillation-only sources: Mona Baker, *In Other Words: A Coursebook on Translation* (1992),
  and Eugene A. Nida's account of dynamic and formal equivalence (*Toward a Science of Translating*,
  1964). Spine: 116 principles, 415 atomic claims, 28 chunk anchors — unchanged by this layer.
