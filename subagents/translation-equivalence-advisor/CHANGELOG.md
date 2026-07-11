# Changelog — translation-equivalence-advisor

All notable changes to this generated subagent package are recorded here. Versions follow the
`agent_version` field in `profile.yaml`.

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
