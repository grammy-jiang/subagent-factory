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
| mayer-multimedia-lea-40e2757d | Multimedia Learning | Richard E. Mayer | 2009 | distillation-only |
| clark-mayer-elearnin-a0fa4bb7 | e-Learning and the Science of Instruction | Ruth Colvin Clark and Richard E. Mayer | 2016 | distillation-only |
| reigeluth-instructio-a562075c | Instructional-Design Theories and Models (In Action / A New Paradigm) | Charles M. Reigeluth (ed.) | 1999 | distillation-only |

All eleven sources are **distillation-only**: paraphrase and restructure only, no verbatim quotation
(see `.claude/rules/rights-and-quotation-policy.md`; enforced by `quote_scan`). They are canonical
works on instructional and course design — backward design and assessment for understanding,
constructive alignment and university teaching, integrated course design, the revised taxonomy of
knowledge and cognitive process, systematic instructional design, first principles of instruction,
instructional theory and elaboration sequencing, iterative successive-approximation development, and
the cognitive science of multimedia learning.

## Distillation

Spine: 200 promoted principles (P001-P200; 75 high-confidence) over
7860 atomic claims, with evidence records and chunk anchors. The 200 principles are
partitioned across 13 skills, each principle owned by exactly one skill; the two
references index and ground them.

## Version History

- **1.0.0** (2026-07-26) — Initial LLM-authored layer over the pre-built distilled spine of 180
  principles from ten sources (*Multimedia Learning* present only as a partial conversion): profile,
  faithfulness report, 13 skills, 2 references, golden + principle-behaviour tests, and the exported
  Claude Code adapter.
- **1.1.0** (2026-07-26) — Source fold-in and full re-author over the rebuilt spine. Two source
  changes: the partial *Multimedia Learning* conversion was replaced by the full text
  (`mayer-multimedia-lea-f516bca0` -> `mayer-multimedia-lea-40e2757d`), and *Instructional-Design
  Theories and Models* (Reigeluth) was added — eleven sources, 200 principles, 7860
  claims. The map->reduce rebuild renumbered every principle, so the 1.0.0 principle ids do not carry
  over: the 13-skill partition, every inline citation in `quality_bar`,
  `forbidden_behaviours`, `handoff_rules`, `source_of_truth_policy.precedence`, the examples, the
  faithfulness report, and both test suites were re-derived against the new P001-P200
  numbering. No 1.0.0 profile decision was silently overwritten — the role, boundary, mode set, and
  skill partition survive; only their grounding ids and the sequencing/instructional-theory coverage
  contributed by the new sources changed.
