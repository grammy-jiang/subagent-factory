# Provenance Ledger — research-integrity-reproducibility-advisor

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
| turing-way-reproduci-96a0665f | The Turing Way: A Handbook for Reproducible, Ethical and Collaborative Research | The Turing Way Community | 2022 | distillation-only |
| on-being-a-scientist-f5840c5b | On Being a Scientist: A Guide to Responsible Conduct in Research (3rd ed.) | National Academy of Sciences, National Academy of Engineering, and Institute of Medicine | 2009 | distillation-only |
| gaoxiao-xueshu-guifa-782202ce | A Guide to Academic Norms in Higher-Education Institutions (高校学术规范指南) | Academic-norms guide (higher education) | None | distillation-only |

All three sources are **distillation-only**: paraphrase and restructure only, no verbatim quotation
(see `.claude/rules/rights-and-quotation-policy.md`; enforced by `quote_scan`). They are canonical
works on reproducible research and the responsible conduct of research: The Turing Way's handbook of
reproducible/ethical/collaborative practice, the U.S. National Academies' On Being a Scientist, and a
higher-education academic-norms guide.

## Distillation

Spine: 34 promoted principles (P001-P034; 29 high-confidence) over
753 atomic claims, with evidence records and chunk anchors. The 34 principles are
partitioned across 7 skills, each principle owned by exactly one skill; the two
references index and ground them.

## Version History

- **1.0.0** (2026-07-25) — Initial LLM-authored layer over the pre-built distilled spine: profile
  (role, three modes, quality bar, forbidden behaviours, 7-skill / 2-reference
  knowledge partition), faithfulness report, 7 skills, 2 references, golden +
  principle-behaviour tests, and the exported Claude Code adapter. No prior profile decisions
  superseded.
