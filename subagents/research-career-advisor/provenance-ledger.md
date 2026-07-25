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

## Cross-source conflict check

`multisource_synthesis` is `deferred` (no automated Step-7 synthesis / principle-graph run). A manual
cross-source conflict pass was made over the four sources, which span different eras and settings
(Hamming's 1997 Bell-Labs industrial perspective vs. present-day academic-job-market guidance in
Feibelman and the Chinese success guide; Cohen's empirical-method text is orthogonal). No contradictory
principles were found: the sources emphasize different facets (importance-and-attackability of problems,
protection factors in mentoring, communication, funding, empirical soundness) rather than opposing rules.
The one latent tension — how much to weight institutional prestige — is resolved by P010's own hedge
(established reputation is a tie-breaker only when protection factors are comparable), which `quality_bar`
and `knowledge_partition.always_on` both preserve, and by the `precedence` rule that treats purpose-tied
practices as adaptable guides rather than absolutes.

## Version History

- **1.1.0** (2026-07-25) — Re-authored all 8 skill bodies to the GOLD shape (added trigger-oriented
  `description:` frontmatter; rewrote every anti-pattern bullet as a complete observable-failure-symptom
  sentence, one per provenance principle — restoring the dropped P038 and P046 bullets and replacing
  truncated substrings; expanded stub Procedure steps), preserving `provenance:` blocks and digests
  verbatim. Profile: weakened `quality_bar[2]` to restore P010's tie-break hedge (was flattened to "not
  prestige"), shortened `role` to stop duplicating `forbidden_behaviours`, narrowed `when_to_use[3]` to
  the strategy slice and added a `when_not_to_use` handoff to `research-writing-advisor`, and added a
  `router_description` covering all five when-to-use domains. Recorded the manual cross-source conflict
  check above. No principle citations were changed for any surviving `quality_bar` /
  `forbidden_behaviours` / `handoff_rules` row, so no field→grounding row required re-mapping.
  Supersedes the 1.0.0 skill-body and profile-copy decisions; the distilled spine is unchanged.
- **1.0.0** (2026-07-25) — Initial LLM-authored layer over the pre-built distilled spine: profile
  (role, three modes, quality bar, forbidden behaviours, 8-skill / 2-reference
  knowledge partition), faithfulness report, 8 skills, 2 references, golden +
  principle-behaviour tests, and the exported Claude Code adapter. No prior profile decisions
  superseded.
