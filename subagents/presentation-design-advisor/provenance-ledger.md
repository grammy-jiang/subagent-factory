# Provenance Ledger — presentation-design-advisor

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
| alley-craft-of-scien-8c1a058e | The Craft of Scientific Presentations: Critical Steps to Succeed and Critical Errors to Avoid | Michael Alley | 2013 | distillation-only |
| duarte-resonate-dc2fdbd7 | Resonate: Present Visual Stories That Transform Audiences | Nancy Duarte | 2010 | distillation-only |
| duarte-slideology-e1324c7e | slide:ology: The Art and Science of Creating Great Presentations | Nancy Duarte | 2008 | distillation-only |

All three sources are **distillation-only**: paraphrase and restructure only, no verbatim quotation
(see `.claude/rules/rights-and-quotation-policy.md`; enforced by `quote_scan`). They span two
complementary traditions: the technical-presentation craft literature, where the assertion-evidence
structure, its controlled comparison, and the delivery and contingency discipline come from
(Alley); and the visual-story and slide-design literature, where the big idea, audience persona,
story arc, ideation, and design craft come from (Duarte, *Resonate* and *slide:ology*).

## Distillation

Spine: 120 promoted principles (P001-P120; 116 high-confidence) over
1359 atomic claims, with evidence records and chunk anchors. The 120 principles are
partitioned across 13 skills, each principle owned by exactly one skill; the two
references index and ground them.

## Version History

- **1.0.0** (2026-07-26) — Initial LLM-authored layer over the pre-built distilled spine: profile
  (role, three modes, quality bar, forbidden behaviours, 13-skill / 2-reference
  knowledge partition), faithfulness report, 13 skills, 2 references, golden +
  principle-behaviour tests, and the exported Claude Code adapter. No prior profile decisions
  superseded.
