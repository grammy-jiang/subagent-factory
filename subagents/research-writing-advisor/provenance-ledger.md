# Provenance Ledger — research-writing-advisor

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
| craft-of-research-4e-14900d77 | The Craft of Research (4th ed.) | Wayne C. Booth, Gregory G. Colomb, Joseph M. Williams, Joseph Bizup, and William T. FitzGerald | 2016 | distillation-only |
| writing-for-computer-5ddb3c95 | Writing for Computer Science (3rd ed.) | Justin Zobel | 2014 | distillation-only |
| writing-science-schi-80f45a2c | Writing Science: How to Write Papers That Get Cited and Proposals That Get Funded | Joshua Schimel | 2012 | distillation-only |
| english-writing-rese-9857a4a3 | English for Writing Research Papers (2nd ed.) | Adrian Wallwork | 2016 | distillation-only |
| science-research-wri-10f0a73c | Science Research Writing for Non-Native Speakers of English | Hilary Glasman-Deal | 2010 | distillation-only |
| how-to-write-a-lot-s-bd8de416 | How to Write a Lot: A Practical Guide to Productive Academic Writing | Paul J. Silvia | 2007 | distillation-only |
| how-to-take-smart-no-a0f38246 | How to Take Smart Notes | Sönke Ahrens | 2017 | distillation-only |
| presentation-zen-des-db533de8 | Presentation Zen Design | Garr Reynolds | 2010 | distillation-only |
| ted-talks-public-spe-7e242e4f | TED Talks: The Official TED Guide to Public Speaking | Chris Anderson | 2016 | distillation-only |

All nine sources are **distillation-only**: paraphrase and restructure only, no verbatim quotation
(see `.claude/rules/rights-and-quotation-policy.md`; enforced by `quote_scan`). They are canonical
works on research writing and scientific communication — the craft of research argument, scientific
and technical writing, English for non-native research authors, writing productivity, note-taking for
thinking, slide design, and public speaking.

## Distillation

Spine: 172 promoted principles (P001-P172; 50 high-confidence) over
3693 atomic claims, with evidence records and chunk anchors. The 172 principles are
partitioned across 13 skills, each principle owned by exactly one skill; the two
references index and ground them.

## Version History

- **1.0.0** (2026-07-25) — Initial LLM-authored layer over the pre-built distilled spine: profile
  (role, three modes, quality bar, forbidden behaviours, 13-skill / 2-reference
  knowledge partition), faithfulness report, 13 skills, 2 references, golden +
  principle-behaviour tests, and the exported Claude Code adapter. No prior profile decisions
  superseded.
