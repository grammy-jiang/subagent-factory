# Provenance Ledger — learning-science-advisor

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
| dunlosky-2013-improv-13b90eb5 | Improving Students' Learning With Effective Learning Techniques: Promising Directions From Cognitive and Educational Psychology | John Dunlosky, Katherine A. Rawson, Elizabeth J. Marsh, Mitchell J. Nathan and Daniel T. Willingham | 2013 | distillation-only |
| brown-roediger-mcdan-9a1ca554 | Make It Stick: The Science of Successful Learning | Peter C. Brown, Henry L. Roediger III and Mark A. McDaniel | 2014 | distillation-only |
| weinstein-sumeracki-5e470598 | Understanding How We Learn: A Visual Guide | Yana Weinstein and Megan Sumeracki | 2018 | distillation-only |
| rosenshine-principle-98e74dd1 | Principles of Instruction: Research-Based Strategies That All Teachers Should Know | Barak Rosenshine | 2012 | distillation-only |
| ambrose-how-learning-163bde10 | How Learning Works: Seven Research-Based Principles for Smart Teaching | Susan A. Ambrose, Michael W. Bridges, Michele DiPietro, Marsha C. Lovett and Marie K. Norman | 2010 | distillation-only |
| willingham-why-dont-61f71765 | Why Don't Students Like School? A Cognitive Scientist Answers Questions About How the Mind Works and What It Means for the Classroom | Daniel T. Willingham | 2009 | distillation-only |
| agarwal-bain-powerfu-5b75ae90 | Powerful Teaching: Unleash the Science of Learning | Pooja K. Agarwal and Patrice M. Bain | 2019 | distillation-only |
| lang-small-teaching-1c0df7f4 | Small Teaching: Everyday Lessons from the Science of Learning | James M. Lang | 2016 | distillation-only |
| darby-lang-small-tea-84140e5a | Small Teaching Online: Applying Learning Science in Online Classes | Flower Darby with James M. Lang | 2019 | distillation-only |
| hattie-visible-learn-aa5d2ed3 | Visible Learning: A Synthesis of Over 800 Meta-Analyses Relating to Achievement | John Hattie | 2008 | distillation-only |
| deans-for-impact-sci-c50ecdcd | The Science of Learning (2nd edition) | Deans for Impact | 2019 | distillation-only |
| nasem-how-people-lea-a3bb4079 | How People Learn II: Learners, Contexts, and Cultures | National Academies of Sciences, Engineering, and Medicine | 2018 | distillation-only |

All twelve sources are **distillation-only**: paraphrase and restructure only, no verbatim
quotation (see `.claude/rules/rights-and-quotation-policy.md`; enforced by `quote_scan`). They span
three layers of the field: primary research reviews and syntheses (Dunlosky et al.'s techniques
review, Hattie's meta-analytic synthesis, the National Academies' *How People Learn II*, the Deans
for Impact consensus summary, Rosenshine's *Principles of Instruction*); cognitive-science
translations for practitioners (*Make It Stick*, *Understanding How We Learn*, *Why Don't Students
Like School?*); and applied teaching handbooks (*How Learning Works*, *Powerful Teaching*, *Small
Teaching*, *Small Teaching Online*).

## Distillation

Spine: 150 promoted principles (P001-P150; 55 high-confidence) over
5006 atomic claims, with evidence records and chunk anchors. The 150 principles are
partitioned across 15 skills, each principle owned by exactly one skill; the two
references index and ground them.

## Version History

- **1.0.0** (2026-07-26) — Initial LLM-authored layer over the pre-built distilled spine: profile
  (role, three modes, quality bar, forbidden behaviours, 15-skill / 2-reference
  knowledge partition), faithfulness report, 15 skills, 2 references, golden +
  principle-behaviour tests, and the exported Claude Code adapter. No prior profile decisions
  superseded.
