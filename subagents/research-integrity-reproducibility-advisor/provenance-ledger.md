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

> **Note on `year`:** `gaoxiao-xueshu-guifa` (the higher-education academic-norms guide) carries
> `year: null` — the ingested copy bore no unambiguous publication year, so no date is asserted rather
> than guessing one. This does not affect distillation or rights status.

## Faithfulness

`reports/faithfulness-report.yaml` grades every load-bearing profile rule against its cited principle(s)
on the five-level claim-strength scale. **Outcome: PASS** — all 27 findings (6 quality_bar, 4
forbidden_behaviours, 6 when_to_use, 1 outputs.primary_format, 2 handoff_rules, 1
source_of_truth_policy.precedence, and all 7 `knowledge_partition.always_on` skill bullets) are
`WITHIN_SCOPE` with no `SCOPE_BROADENED`, `HEDGING_REMOVED`, or `CONTRADICTED` verdict. The one
SCOPE_BROADENED candidate raised in review (P027's documentation duties in `always_on[0]` vs its
narrow `applies_when`) was resolved by broadening P027's `applies_when` to match its own general
statement, keeping the bullet within scope.

## Distillation

Spine: 34 promoted principles (P001-P034; 29 high-confidence) over
753 atomic claims, with evidence records and chunk anchors. The 34 principles are
partitioned across 7 skills, each principle owned by exactly one skill; the two
references index and ground them.

## Version History

- **1.1.0** (2026-07-25) — Review-loop r1 fixes (no principle statements changed, so the distilled
  spine and adapter invariants are unaltered; no prior profile decision superseded, only refined):
  re-authored all 7 skill bodies to the gold shape (fixed mid-clause truncations in Procedure steps,
  added a `description:` frontmatter line per skill, and rewrote Anti-patterns as concrete observable
  red-flag symptoms instead of principle restatements); added a `plan`-mode worked example and a
  `when_to_use` trigger for contributing to an existing open project (grounded in P024); extended the
  faithfulness report to cover all 7 `knowledge_partition.always_on` bullets with per-rule notes and
  recorded the PASS outcome above; broadened P027's `applies_when` to match its own general statement
  (resolving the SCOPE_BROADENED candidate); and flipped P020 and P026 `operational_mapping.profile_rule`
  to `true` to match their use in `always_on`. Field→grounding rows are unchanged: every re-authored
  skill still cites exactly its own partition principles.
- **1.0.0** (2026-07-25) — Initial LLM-authored layer over the pre-built distilled spine: profile
  (role, three modes, quality bar, forbidden behaviours, 7-skill / 2-reference
  knowledge partition), faithfulness report, 7 skills, 2 references, golden +
  principle-behaviour tests, and the exported Claude Code adapter. No prior profile decisions
  superseded.
