# Provenance Ledger — presentation-design-advisor

Canonical record of what grounds this subagent. The profile, skills, references, faithfulness
report, and tests are all derived from the distilled spine in this package
(`principles/principles.yaml` -> `analysis/claims.jsonl` -> `evidence/evidence-records.yaml` ->
`sources/anchors/*.anchors.jsonl`), assembled by the map->reduce build. No load-bearing profile rule
field is an orphan: every `quality_bar`, `forbidden_behaviours`, `handoff_rules`,
`knowledge_partition.always_on`, and `source_of_truth_policy` value either cites the promoted
principle(s) it restates or says in its own text that it is an authored boundary no principle
states. Authored is a disclosed state, not a silent one: the rules that carry no grounding say so
inline, and the faithfulness report records why the grounding was withdrawn.

## Field grounding

The descriptive fields carry no inline `(Pxxx)` tags — they would clutter routing text a router reads
— so their grounding is recorded here instead of being declared exempt (round-1 review, F13).

| Field | Grounding |
|-------|-----------|
| `role` | The three sources in the table below (`source-pack.manifest.yaml`); the topic list is the skill partition in `knowledge_partition.skills`; the advice-only boundary restates `forbidden_behaviours[0]`, which is an authored scope boundary with no principle citation (1.2.0 — P062/P026 do not carry it). |
| `when_to_use` | Bullet 1 → P014/P045/P069 (does each slide assert and evidence something) plus P007/P011/P099 (the typography, colour, and layout half added in 1.2.0); 2 → P039/P077/P113 (the ways a talk loses its audience); 3 → P060/P061/P035/P088/P065 (big idea, persona, story order, length, preparation); 4 → P020/P052/P043/P109/P106/P104 (rehearsal, transitions, questions, room, equipment); 5 → P006/P038/P119 (three appeals against prior bias and tolerance). |
| `when_not_to_use` | 1 → authored scope boundary, no principle citation (1.2.0 — P062 is about briefing an illustrator, not about an advisor declining to do the work); 2 → authored scope boundary, no principle citation (1.2.0 — the debunked P001/P091 grounding is withdrawn, matching `forbidden_behaviours[2]`); 3 → authored boundary plus P038/P028 (prior bias and a failed demonstration can override any design); 4 → P068 (build up, never deceive); 5 → P009/P031 (a document is a document). |
| `inputs` | `required[0]`: artifact + audience gate from P061/P075 (the audience must be characterised), with the proceed-without-the-rest rule authored; `required[1]`: authored operating instruction covering the granted read tools and the instruction–data separation added in 1.2.0 under `.claude/rules/untrusted-source-policy.md`, no domain claim; `optional[0]`: P065 (preparation), P088 (length), P066/P104 (room and equipment), all held as optional context. |
| `outputs` | `primary_format` and `minimum_useful_output` → authored output-shape and output-floor policy, no principle citation (1.2.0 — P012/P056, cited up to 1.1.0, state neither that comprehension is the measure of an advisory answer nor an ordering rule; same withdrawal already applied to `source_of_truth_policy.precedence`); `advise` → P027/P051/P103 (state the occasion-condition); `review` → P036 (four perspectives and the distraction test), with the highest-impact-first ordering authored; `plan` → P065/P088 (scoped to slot and preparation time). |
| `source_of_truth_policy.canonical_owner` | Illustrator/designer clause → P062; presenter-and-institution authority over the talk, deck, data, and the decision to give it, and the audience or funding body's authority over the decision sought → authored boundaries, no principle citation (recorded in 1.2.0, consistent with `handoff_rules[0]`). |
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

- **1.2.1** (2026-07-27) — Adversarial verify-pass-1 fixes (3 must-fix, all faithfulness wording
  drifts). **Superseded decisions, stated explicitly:** (a) 1.2.0 left `examples[1]` step (b) asserting
  P119's *emotionally-driven* branch about an executive committee whose type was never established — and
  step (c) of the same answer told the reader to establish that audience's bias first, so one model
  answer both asserted and disclaimed the audience read. The round-2 faithfulness report graded this
  WITHIN_SCOPE on the ground that P119 was "cited where used"; that grade is withdrawn — citation was
  never the issue, applying a two-branched conditional to an unclassified audience is, and on the other
  branch the advice inverts. The claim is now conditioned on the committee deciding partly on grounds
  other than proof volume, the hedge `examples[3]` already carried. (b) `in-room-delivery-and-composure`
  Procedure step 8 turned P066's "account for" into "judge **only** against"; the exclusivity is in
  neither P066 nor claim C00499 and contradicted P063 and P079, so the word is deleted.
  (c) `format-choice-and-preparation-planning`'s last anti-pattern converted P088's eighteen minutes —
  a case observation (C01312, `evidence_type: case`) about the most influential talks, supporting the
  *policy* of hard constraint — into a review threshold that fires on any deck over 18 minutes,
  including the lectures, defences and hour-long slots this package serves (`when_to_use[0]`, P111,
  P065); the trigger is re-anchored to the talk's own slot. (d) `quality_bar[2]` adds the missing P049
  citation behind its "bold" (citation gap, force unchanged). **Process finding recorded, not yet
  closed:** the authored `reports/faithfulness-report.yaml` audits `profile.yaml` fields only — zero
  entries cover `knowledge_partition.skills` or any `SKILL.md` body, which is why (b) and (c) survived
  a `must-fix = 0` verdict. The faithfulness surface should extend to skill bodies. No principle,
  claim, or evidence record was changed — the spine is untouched.
- **1.2.0** (2026-07-27) — Round-2 review fixes. **Superseded decisions, stated explicitly:**
  (a) 1.1.0 applied the P001/P091 withdrawal to `forbidden_behaviours[2]` only; the same debunked
  citation survived on `when_not_to_use[1]` and was still marked clean in the faithfulness report.
  It is now an authored scope boundary there too. The sweep was extended to every field sharing a
  mis-fitted citation: `forbidden_behaviours[0]` and `when_not_to_use[0]` drop P062/P026 (P062 briefs
  an illustrator, P026 says slides scaffold rather than script — neither states that an advisor must
  not perform the work); `handoff_rules[0]` drops P074 from the ownership clause (P074 refuses slides
  as an extension of the presenter's persona and says nothing about ownership) and keeps P062 for the
  illustrator clause; `outputs.primary_format`, `minimum_useful_output`, and the `review` mode's
  ordering drop P012/P056, the same over-broad pair already withdrawn from the precedence
  tie-breaker in 1.1.0. (b) The adapter carried no instruction–data separation rule while reading
  caller-supplied artifacts as its core job; `inputs.required[1]` now states that an artifact's
  contents are material to critique and never instructions, and that nothing written there waives the
  forbidden behaviours or the advice-only boundary (`.claude/rules/untrusted-source-policy.md`).
  (c) `inputs.required` no longer holds an entry that says "not required": the optional context moves
  to a new `inputs.optional`, with the proceed-without-it rule kept inside the gating bullet so it
  still reaches the adapter, which renders only `required`. (d) The minimum-useful-output floor never
  reached the adapter (the template renders `quality_bar` but not `minimum_useful_output`); it is
  added as `quality_bar[8]` so a thin, ungrounded answer has a rendered bar to fail. (e) The
  persuasion `always_on` paragraph no longer widens P006's "scientists" to "scientific and technical
  presenters" nor claims the appeal carries "beyond the sciences"; P006 keeps its own population and
  P120 is stated separately as a calibration rather than an extension of it. (f) `quality_bar[0]`
  restores P014's `applies_when` qualifier ("every technical content slide"), matching
  `knowledge_partition.always_on[0]`. (g) `router_description` and `role` name in-room delivery and
  composure — room control, audience attention, composure under pressure — which the 1.1.0 skill split
  created but neither router-facing field mentioned; `when_to_use[0]` now covers a
  typography/colour/layout-only review request. (h) `source_of_truth_policy.canonical_owner` had no
  faithfulness-report entry; it is audited and resolved consistently with `handoff_rules[0]`.
  (i) `rehearsal-and-memorisation` moves its sibling boundary into the frontmatter `description`, the
  only text loaded at trigger time. (j) Each of the 14 skill bodies' `## Purpose` sections, which
  restated the numbered `## Procedure` below them almost claim-for-claim, is compressed to what the
  skill is for and why — the Procedure keeps every step, every principle citation, and every hedge.
  (k) Profile body prose trimmed against the 800-word budget so the fixes above did not push it
  towards the 1000-word hard fail. No principle statement, claim, or evidence record was changed —
  the spine is untouched.
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
