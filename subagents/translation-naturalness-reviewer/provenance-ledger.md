# Provenance Ledger — translation-naturalness-reviewer

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
| dynamic-formal-equiv-e6872198 | Principles of Correspondence (Dynamic and Formal Equivalence) | Eugene A. Nida | 1964 | distillation-only |
| norms-in-translation-ad249b8d | The Nature and Role of Norms in Translation | Gideon Toury | 1995 | distillation-only |
| translation-quality-c0dd203d | Translation Quality Assessment: Past and Present | Juliane House | 2015 | distillation-only |
| technical-translatio-41f3c47c | Technical Translation: Usability Strategies for Translating Technical Documentation | Jody Byrne | 2006 | distillation-only |
| in-other-words-baker-8e6c3cb1 | In Other Words: A Coursebook on Translation | Mona Baker | 2011 | distillation-only |
| scientific-technical-d92653ac | Scientific and Technical Translation Explained | Jody Byrne | 2012 | distillation-only |
| introducing-translat-4a29c5ca | Introducing Translation Studies: Theories and Applications | Jeremy Munday | 2016 | distillation-only |
| translation-studies-45ee8f34 | The Translation Studies Reader | Lawrence Venuti (ed.) | 2012 | distillation-only |
| chinglish-europeaniz-5798beb7 | On the Naturalness and Europeanization of Chinese (Chinglish) | Yu Guangzhong | 1987 | distillation-only |

All nine sources are **distillation-only**: paraphrase and restructure only, no verbatim quotation
(see `.claude/rules/rights-and-quotation-policy.md`; enforced by `quote_scan`). They span the
equivalence/naturalness (Nida), descriptive/norms (Toury), quality-assessment (House),
technical/usability (Byrne x2), cohesion-and-idiom (Baker), survey (Munday), and primary-essay
(Venuti reader) strands of translation studies, plus a Chinese-language naturalness perspective (Yu
Guangzhong on Europeanized Chinese) that anchors the de-interference criteria.

## Distillation

Spine: 150 promoted principles (P001-P150; 79 high-confidence) over
2717 atomic claims, with evidence records and chunk anchors. The 150
principles are partitioned across 15 skills, each principle owned by exactly one skill;
the two references index and ground them.

## Version History

- **1.0.1** (2026-07-25) — Added `router_description` to `profile.yaml`. The adapter frontmatter `description` is the string the runtime routes on; without this field the exporter composed it from the role plus only the first two `when_to_use` triggers and the first `when_not_to_use` exclusion, dropping the remaining domains from the routing signal. The authored description states the full remit and the advice-only boundary; adapter re-exported. No principle, rule, skill, or source changed — no prior profile decision is superseded.

- **1.0.0** (2026-07-13) — Initial LLM-authored layer over the pre-built distilled spine: profile
  (role, three modes, quality bar, forbidden behaviours, 15-skill / 2-reference
  knowledge partition), faithfulness report, 15 skills, 2 references, golden +
  principle-behaviour tests, and the exported Claude Code adapter. No prior profile decisions
  superseded.
