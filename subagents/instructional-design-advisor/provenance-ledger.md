# Provenance Ledger — instructional-design-advisor

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
| wiggins-mctighe-unde-b6dc4e0e | Understanding by Design (expanded 2nd ed.) | Grant Wiggins and Jay McTighe | 2005 | distillation-only |
| biggs-tang-teaching-108b0793 | Teaching for Quality Learning at University | John Biggs and Catherine Tang | 2011 | distillation-only |
| fink-creating-signif-cae1a56f | Creating Significant Learning Experiences | L. Dee Fink | 2013 | distillation-only |
| anderson-krathwohl-t-2e6259ce | A Taxonomy for Learning, Teaching, and Assessing | Lorin W. Anderson and David R. Krathwohl (eds.) | 2001 | distillation-only |
| gagne-briggs-wager-p-e2418d40 | Principles of Instructional Design | Robert M. Gagné, Leslie J. Briggs, and Walter W. Wager | 1992 | distillation-only |
| merrill-first-princi-dd2a4ed2 | First Principles of Instruction | M. David Merrill | 2002 | distillation-only |
| dick-carey-systemati-65eb3dad | The Systematic Design of Instruction | Walter Dick, Lou Carey, and James O. Carey | 2015 | distillation-only |
| allen-leaving-addie-36548667 | Leaving ADDIE for SAM | Michael Allen with Richard Sites | 2012 | distillation-only |
| mayer-multimedia-lea-f516bca0 | Multimedia Learning | Richard E. Mayer | 2009 | distillation-only |
| clark-mayer-elearnin-a0fa4bb7 | e-Learning and the Science of Instruction | Ruth Colvin Clark and Richard E. Mayer | 2016 | distillation-only |

All ten sources are **distillation-only**: paraphrase and restructure only, no verbatim quotation
(see `.claude/rules/rights-and-quotation-policy.md`; enforced by `quote_scan`). They are canonical
works on instructional and course design — backward design and assessment for understanding,
constructive alignment and university teaching, integrated course design, the revised taxonomy of
knowledge and cognitive process, systematic instructional design, first principles of instruction,
iterative successive-approximation development, and the cognitive science of multimedia learning.

## Distillation

Spine: 180 promoted principles (P001-P180; 52 high-confidence) over
6851 atomic claims, with evidence records and chunk anchors. The 180 principles are
partitioned across 13 skills, each principle owned by exactly one skill; the two
references index and ground them.

## Version History

- **1.0.0** (2026-07-26) — Initial LLM-authored layer over the pre-built distilled spine: profile
  (role, three modes, quality bar, forbidden behaviours, 13-skill / 2-reference
  knowledge partition), faithfulness report, 13 skills, 2 references, golden +
  principle-behaviour tests, and the exported Claude Code adapter. No prior profile decisions
  superseded.
