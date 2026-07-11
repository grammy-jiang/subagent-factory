# Changelog — translation-equivalence-advisor

All notable changes to this generated subagent package are recorded here. Versions follow the
`agent_version` field in `profile.yaml`.

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
