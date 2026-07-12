# Changelog — translation-quality-reviewer

All notable changes to this generated subagent package are recorded here. Versions follow the
`agent_version` field in `profile.yaml`.

## [1.1.0] — 2026-07-12

### Fixed (review loop r1)
- Re-exported the Claude Code adapter with the corrected `compile_invariants`, restoring the full
  operating invariants (the earlier export truncated P001/P002/P012/P018/P020/P029/P055-P058/P121/P122
  with a trailing `…` and silently colon-cut P003/P019/P035/P053/P054/P083/P084).
- **P003** rewritten to name all three corpus types — parallel (equivalence/shifts/alignment),
  monolingual comparable (translated vs non-translated, same target language, for
  universals/translationese, grounded in P121), and multilingual comparable (cross-linguistic
  contrast) — instead of defining "comparable" only in the multilingual sense.
- **P042** now notes that participation sat under Mode in House's earlier model and is reassigned to
  Tenor in her revised model (P075 governs), removing the Mode-vs-Tenor contradiction within the
  register skill.
- **P139** weakened to match its source (Baker C00515): the label *translationese* applies only when
  an unusual distribution is clearly the result of translator inexperience/incompetence, not as a
  blanket definition — resolving the contradiction with P002/P147.

### Changed
- All 12 skills re-authored to gold shape: added a `description:` frontmatter line (routing signal +
  neighbouring-skill boundary), and rewrote `## Anti-patterns to flag` as complete, skill-specific
  sentences (one per load-bearing principle) instead of truncated generic principle echoes.
- Profile faithfulness tightened: dropped spurious anchors (P084 from quality_bar[0], P090 from
  quality_bar[2]); narrowed the `precedence` rule (P032/P047/P115) to its cultural-filter /
  universal-tendency scope; scoped the register `always_on` bullet to "mission statements and
  comparably exhortative institutional texts" (P010/P070-P075); re-marked `handoff_rules[1]` as a
  profile-level scoping judgement (dropped unrelated P052/P077); softened the contract-as-overt
  example to "plausible candidate". Added `when_to_use` coverage for error-discipline and
  genre/accessibility triggers and split the Russian/Chinese trigger.

## [1.0.0] — 2026-07-12

### Added
- Initial release of the **translation-quality-reviewer** subagent (Tier 2), authoring the LLM layer over the
  already-assembled, deterministically-valid distilled spine (150 principles
  P001-P150 / 713 claims from five distillation-only sources).
- `profile.yaml` derived from the 150 promoted principles: role, when/when-not-to-use,
  three modes (review / advise / compare), quality bar, forbidden behaviours, handoff rules, and a
  12-skill / 2-reference `knowledge_partition` covering every principle exactly
  once.
- 12 authored skills partitioning all 150 principles; 2 references
  (principles index + evidence notes).
- `reports/faithfulness-report.yaml` — every load-bearing profile rule graded WITHIN_SCOPE against
  its principles (no rule stronger than its evidence).
- `tests/golden-tests.yaml` (6 golden, 2 negative-routing,
  2 missing-context) and `tests/principle-behaviour-tests.yaml` (one behaviour test per
  principle, 150 total).
- Claude Code adapter exported to `adapters/claude-code/` and installed under
  `.claude/agents/generated/`.

### Grounding
- Five distillation-only sources: Juliane House, *Translation Quality Assessment: Past and Present*
  (2015); Mona Baker, *Corpus Linguistics and Translation Studies* (1993); Haidee Kruger et al.,
  *Corpus-Based Translation Studies* (2011); Daria Dayter & Łukasz Grabowski, eds., corpus-based
  translation and interpreting studies in the Russian field (2023); Yu Guangzhong on the normal and
  distorted states of Chinese prose (1987).
