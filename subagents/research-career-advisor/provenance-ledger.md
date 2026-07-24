# Provenance Ledger — research-career-advisor

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
| a-phd-is-not-enough-9a264724 | A PhD Is Not Enough! A Guide to Survival in Science | Peter J. Feibelman | 2011 | distillation-only |
| hamming-meta-5bf0ea64 | The Art of Doing Science and Engineering: Learning to Learn / You and Your Research | Richard W. Hamming | 1997 | distillation-only |
| xueshu-yanjiu-chengg-ff70b27e | The Road to Success in Academic Research (学术研究成功之道) | Academic-research success guide (Chinese) | None | distillation-only |
| empirical-methods-co-de09d1d7 | Empirical Methods for Artificial Intelligence | Paul R. Cohen | 1995 | distillation-only |

All four sources are **distillation-only**: paraphrase and restructure only, no verbatim quotation
(see `.claude/rules/rights-and-quotation-policy.md`; enforced by `quote_scan`). They are canonical
works on the scientific research career and empirical method: Feibelman's survival guide for a
career in science, Hamming's essays on doing high-impact research and learning to learn, a Chinese
guide to succeeding in academic research, and Cohen's textbook on empirical methods for AI.

## Distillation

Spine: 48 promoted principles (P001-P048; 0 high-confidence) over
611 atomic claims, with evidence records and chunk anchors. The 48 principles are
partitioned across 8 skills, each principle owned by exactly one skill; the two
references index and ground them.

## Version History

- **1.0.0** (2026-07-25) — Initial LLM-authored layer over the pre-built distilled spine: profile
  (role, three modes, quality bar, forbidden behaviours, 8-skill / 2-reference
  knowledge partition), faithfulness report, 8 skills, 2 references, golden +
  principle-behaviour tests, and the exported Claude Code adapter. No prior profile decisions
  superseded.
