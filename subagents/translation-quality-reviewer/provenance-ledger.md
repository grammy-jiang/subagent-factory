# Provenance Ledger — translation-quality-reviewer

Canonical record of what grounds this subagent. The profile, skills, references, faithfulness
report, and tests are all derived from the distilled spine in this package
(`principles/principles.yaml` -> `analysis/claims.jsonl` -> `evidence/evidence-records.yaml` ->
`sources/anchors/*.anchors.jsonl`), assembled by the map->reduce build. No load-bearing profile rule
field is an orphan: every `quality_bar`, `forbidden_behaviours`, `handoff_rules`,
`knowledge_partition.always_on`, and `source_of_truth_policy` value cites the promoted principle(s)
it restates. (Descriptive fields — `role`, `when_to_use`, `inputs`, `outputs` — carry no inline
tags, per repo convention.)

## Sources

| source_id | title | author | year | rights |
|-----------|-------|--------|------|--------|
| translation-quality-c0dd203d | Translation Quality Assessment: Past and Present | Juliane House | 2015 | distillation-only |
| corpus-linguistics-t-ceffdb40 | Corpus Linguistics and Translation Studies: Implications and Applications | Mona Baker | 1993 | distillation-only |
| corpus-based-transla-98c56c2d | Corpus-Based Translation Studies: Research and Applications | Haidee Kruger, Kim Wallmach and Jeremy Munday (eds.) | 2011 | distillation-only |
| corpus-translation-r-b10b2ead | Corpus-Based Translation and Interpreting Studies (the Russian field) | Daria Dayter and Łukasz Grabowski (eds.) | 2023 | distillation-only |
| chinglish-europeaniz-5798beb7 | On the Normal and Distorted States of Chinese (Europeanized Chinese / Chinglish) | Yu Guangzhong | 1987 | distillation-only |

All five sources are **distillation-only**: paraphrase and restructure only, no verbatim quotation
(see `.claude/rules/rights-and-quotation-policy.md`; enforced by `quote_scan`). They are canonical
translation-quality and corpus-translation-studies works: House's functional-pragmatic quality
model, Baker's and Kruger et al.'s corpus programme and universals, the Dayter & Grabowski Russian-
field volume, and Yu Guangzhong on Europeanized Chinese prose.

## Distillation

Spine: 150 promoted principles (P001-P150; 19 high-confidence) over
713 atomic claims, with evidence records and chunk anchors. The 150
principles are partitioned across 12 skills, each principle owned by exactly one skill;
the two references index and ground them.

## Version History

- **1.1.0** (2026-07-12) — Review-loop r1 fixes (supersedes 1.0.0 on the points below; earlier
  decisions remain visible above). Re-exported the adapter to restore truncated operating invariants.
  Grounded principle rewrites: **P003** now names parallel / monolingual comparable / multilingual
  comparable corpus types (monolingual-comparable sense grounded in P121); **P042** labels
  participation-under-Mode as House's earlier model, superseded by **P075** (Tenor) in the revised
  model; **P139** restores Baker's conditional framing (translationese only when a distribution is
  clearly incompetence-driven), resolving the P002/P147 contradiction. All 12 skills re-authored to
  gold shape (added `description:` frontmatter, complete skill-specific anti-patterns). Profile
  faithfulness tightened: dropped spurious anchors P084 (quality_bar[0]) and P090 (quality_bar[2]);
  narrowed `precedence` (P032/P047/P115) to its cultural-filter/universal-tendency scope; scoped the
  register `always_on` bullet to mission statements and comparably exhortative institutional texts
  (P010/P070-P075); re-marked `handoff_rules[1]` as profile-level scoping judgement (dropped
  unrelated P052/P077); added `when_to_use` coverage for error-discipline and genre/accessibility.
- **1.0.0** (2026-07-12) — Initial LLM-authored layer over the pre-built distilled spine: profile
  (role, three modes, quality bar, forbidden behaviours, 12-skill / 2-reference
  knowledge partition), faithfulness report, 12 skills, 2 references, golden +
  principle-behaviour tests, and the exported Claude Code adapter. No prior profile decisions
  superseded.
