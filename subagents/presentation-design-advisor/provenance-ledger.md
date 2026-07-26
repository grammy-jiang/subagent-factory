# Provenance Ledger — presentation-design-advisor

Canonical record of what grounds this subagent. The profile, skills, references, faithfulness
report, and tests are all derived from the distilled spine in this package
(`principles/principles.yaml` -> `analysis/claims.jsonl` -> `evidence/evidence-records.yaml` ->
`sources/anchors/*.anchors.jsonl`), assembled by the map->reduce build. No load-bearing profile rule
field is an orphan: every `quality_bar`, `forbidden_behaviours`, `handoff_rules`,
`knowledge_partition.always_on`, and `source_of_truth_policy` value cites the promoted principle(s)
it restates.

## Field grounding

The descriptive fields carry no inline `(Pxxx)` tags — they would clutter routing text a router reads
— so their grounding is recorded here instead of being declared exempt (round-1 review, F13).

| Field | Grounding |
|-------|-----------|
| `role` | The three sources in the table below (`source-pack.manifest.yaml`); the topic list is the skill partition in `knowledge_partition.skills`; the advice-only boundary restates `forbidden_behaviours` (P062, P026). |
| `when_to_use` | Bullet 1 → P014/P045/P069 (does each slide assert and evidence something); 2 → P039/P077/P113 (the ways a talk loses its audience); 3 → P060/P061/P035/P088/P065 (big idea, persona, story order, length, preparation); 4 → P020/P052/P043/P109/P106/P104 (rehearsal, transitions, questions, room, equipment); 5 → P006/P038/P119 (three appeals against prior bias and tolerance). |
| `when_not_to_use` | 1 → P062 (the work belongs to the presenter and the illustrator); 2, 3 → authored scope boundary plus P038/P028 (prior bias and a failed demonstration can override any design); 4 → P068 (build up, never deceive); 5 → P009/P031 (a document is a document). |
| `inputs.required` | Artifact + audience gate from P061/P075 (the audience must be characterised); the recommended set from P065 (preparation), P088 (length), P066/P104 (room and equipment); the file-reading bullet is an authored operating instruction with no domain claim. |
| `outputs` | `primary_format` and `minimum_useful_output` → P012/P056 (the audience's comprehension is the measure); `advise` → P027/P051/P103 (state the occasion-condition); `review` → P036/P012 (four perspectives, ordered by what distracts); `plan` → P065/P088 (scoped to slot and preparation time). |
| `multisource_synthesis: deferred` | Version 1.0.0 authored a single-pass LLM layer over the pre-built spine; cross-source synthesis artifacts (`principle-clusters.json`, `principle-graph.json`) were deliberately not generated, so `deferred` records "not attempted", not "attempted and empty". Generating them is a later minor-version step and would change no existing principle. |

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
1359 atomic claims, with evidence records and chunk anchors. As of 1.1.0, 118 of the 120 principles
are partitioned across 14 skills, each owned by exactly one skill; the two references index and
ground them. Two sit outside the partition on purpose: P036 (critique from four perspectives) is a
cross-cutting review method and lives in the profile's `quality_bar`, and P048 carries
`operational_mapping.profile_rule: false` — a descriptive claim about institutional adoption
timelines — so nothing in the profile or a skill treats it as an operative instruction.

## Version History

- **1.1.0** (2026-07-27) — Round-1 review fixes. **Superseded decisions, stated explicitly:**
  (a) 1.0.0's skill bodies capped `## Anti-patterns to flag` at seven entries and cut Procedure and
  anti-pattern text at a fixed character length; all 14 skill bodies are re-authored with one
  anti-pattern per principle, no truncation, anti-patterns written as observable failure signatures
  rather than restatements of the Procedure step, and steps ordered by workflow dependency instead of
  principle ID. (b) The 15-principle `rehearsal-and-extemporaneous-delivery` skill is **retired** and
  split into `rehearsal-and-memorisation` (P020, P052, P054, P072, P094, P095, P105) and
  `in-room-delivery-and-composure` (P016, P066, P079, P106, P107, P108, P110, P111); both it and
  `questions-challenge-and-composure` now state which kind of composure they cover. (c) P048 was
  operative in `knowledge_partition.always_on` and in a skill Procedure step despite its own
  `profile_rule: false`; both citations are removed. (d) P036 moves from the format skill to
  `quality_bar` and P074 to `audience-analysis-and-persona-design`, matching what each states.
  (e) `forbidden_behaviours[2]` cited P001/P091 and the precedence tie-breaker cited P012/P056 for
  claims neither pair carries; both are relabelled authored policy with no principle citation.
  (f) The persuasion `always_on` paragraph no longer widens P006's "science" to "technical work"
  unsupported — it keeps P006's own domain and grounds the wider reach in the Duarte-derived P120.
  (g) `inputs.required` no longer gates on seven facts; artifact plus audience gate, the rest is
  recommended, and a file-reading instruction covers the granted read tools. (h) `review` mode now
  triggers on a post-mortem account as well as an artifact; an `examples` entry demonstrates
  declining to rule on the result and declining to guarantee approval. (i) The faithfulness report
  grew from 29 findings over the rule fields to 53, covering every `always_on` paragraph and every
  example, with the numeric claims (28 points, 120–140 wpm, four-item groupings, over 2,000 words,
  twenty-or-thirty seconds, within an hour) checked against the principle that carries each.
  (j) P111's ten-minute condition, dropped in 1.0.0, is restored to the `always_on` text.
  No principle statement, claim, or evidence record was changed — the spine is untouched.
- **1.0.0** (2026-07-26) — Initial LLM-authored layer over the pre-built distilled spine: profile
  (role, three modes, quality bar, forbidden behaviours, 13-skill / 2-reference
  knowledge partition), faithfulness report, 13 skills, 2 references, golden +
  principle-behaviour tests, and the exported Claude Code adapter. No prior profile decisions
  superseded.
