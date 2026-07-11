# Provenance Ledger — descriptive-translation-reviewer

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
| introducing-translat-4a29c5ca | Introducing Translation Studies: Theories and Applications | Jeremy Munday | 2016 | distillation-only |
| translation-studies-45ee8f34 | The Translation Studies Reader | Lawrence Venuti (ed.) | 2012 | distillation-only |
| norms-in-translation-ad249b8d | The Nature and Role of Norms in Translation | Gideon Toury | 1995 | distillation-only |

All three sources are **distillation-only**: paraphrase and restructure only, no verbatim quotation
(see `.claude/rules/rights-and-quotation-policy.md`; enforced by `quote_scan`). They are canonical
descriptive-translation-studies works: Munday's survey of the discipline, Venuti's reader of primary
essays, and Toury's statement of the norms programme.

## Distillation

Spine: 180 promoted principles (P001-P180; 141 high-confidence) over
984 atomic claims, with evidence records and chunk anchors. The 180 principles are
partitioned across 12 skills, each principle owned by exactly one skill; the two
references index and ground them.

## Version History

- **1.1.0** (2026-07-12) — Review-loop round 1 fixes (no prior decision silently overwritten; the
  spine is unchanged except two faithfulness re-wordings below). (1) Re-exported the adapter to
  repair the truncated invariant layer + frontmatter description. (2) Re-authored all 12 skills to the
  GOLD shape (complete Procedure/Anti-pattern sentences before each `(Pxxx)`; Anti-patterns cover
  every principle in the skill; added `description:` frontmatter). (3) **Field→grounding changes:**
  `handoff_rules[0]` re-anchored **P070, P009 → P029, P070** (publication authority now grounded in
  P029; macro/micro split in P070); `handoff_rules[1]` re-anchored **P162, P080 → P029** (commercial/
  economic constraints in P029; legal-validity/typesetting left as an uncited scope boundary); added
  `handoff_rules[2]` (sibling-routing directive, no principle cite — routing only). (4) Weakened two
  principle statements to match source support: **P047** (Blum-Kulka explicitation hypothesis: "later
  confirmed by corpus study" → proposed, contested tendency with varying support) and **P115** (frames
  the technical-texts-easier point as Ortega's comparative observation, marks technical/scientific
  subject-matter risk out of remit). (5) `tier: 1 → 2`; profile body trimmed. `faithfulness-report.yaml`
  extended with `handoff_rules[0..2]` and `canonical_owner` entries.
- **1.0.0** (2026-07-12) — Initial LLM-authored layer over the pre-built distilled spine: profile
  (role, three modes, quality bar, forbidden behaviours, 12-skill / 2-reference
  knowledge partition), faithfulness report, 12 skills, 2 references, golden +
  principle-behaviour tests, and the exported Claude Code adapter. No prior profile decisions
  superseded.
