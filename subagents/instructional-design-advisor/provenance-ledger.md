# Provenance Ledger — instructional-design-advisor

Canonical record of what grounds this subagent. The profile, skills, references, faithfulness
report, and tests are all derived from the distilled spine in this package
(`principles/principles.yaml` -> `analysis/claims.jsonl` -> `evidence/evidence-records.yaml` ->
`sources/anchors/*.anchors.jsonl`), assembled by the map->reduce build. No load-bearing profile rule
field is an orphan: every `quality_bar`, `forbidden_behaviours`, `handoff_rules`,
`knowledge_partition.always_on`, and `source_of_truth_policy` value — including
`source_of_truth_policy.canonical_owner`, cited since 1.2.0 — cites the promoted principle(s) it
restates. (Descriptive fields — `role`, `when_to_use`, `inputs`, `outputs` — carry no inline
tags, per repo convention.)

`multisource_synthesis: deferred` in `profile.yaml` records that no *cross-source synthesis pass*
was run: the eleven sources were folded into one spine by the map->reduce build and de-duplicated by
principle clustering, so a principle can be grounded in several sources, but no separate artifact
reconciles where two sources disagree. It is an intentional flag on an eleven-source package, not a
stale template field.

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
- **1.2.0** (2026-07-27) — Review-loop repair round 1 (`/review-subagent`); no re-distillation, so
  the spine, principle numbering, claims, and source set are unchanged from 1.1.0. What changed:
  - **Skill bodies (all 13).** The deterministic body generator had truncated `## Procedure` steps
    and every `## Anti-patterns to flag` bullet at a ~150-character prefix, closing the fragment
    with a period so no ellipsis or unbalanced parenthesis existed for the truncation gate to see.
    101 procedure steps and 87 anti-pattern bullets were re-authored from the **full** principle
    statements in `principles/principles.yaml`; conditions and list members that the prefix cut
    (e.g. P095's five triangulation sources, P158's three processing demands, P157's system-paced
    bound) are restored. No new claim was introduced: each body still cites only the principle ids
    in its own frontmatter `provenance` block, which is unchanged byte-for-byte.
  - **Anti-pattern sections** are no longer a mechanical `Overlooking Pxxx:` dump capped at seven
    regardless of skill size (which gave the 35-principle strategy skill 20% coverage and small
    skills near-100%). They are now curated, symptom-phrased failure modes scaled to the skill:
    all principles for the 6- and 9-principle skills, roughly half for the larger ones, with the
    curation stated in the section.
  - **`description:` frontmatter** added to all 13 `SKILL.md` files, so triggering does not rest
    only on in-body `## When to use` prose.
  - **`instructional-strategy-and-events`** (35 steps, 5-6x its siblings) grouped under five `###`
    sub-headers with one continuous 1-35 numbering run.
  - **Skill `## Provenance`** reduced to the principle-id list plus a pointer to
    `references/instructional-design-principles-index.md`; the identical ~130-word eleven-book
    citation block no longer repeats in all 13 files.
  - **Faithfulness — four `always_on` over-claims, all repaired** and mirrored into the matching
    skill `## Purpose`: `[5]` (SCOPE_BROADENED) the narration-over-on-screen-text preference now
    carries P157's "in a system-paced presentation" bound; `[1]` (HEDGING_REMOVED) P153's "alone"
    restored, so retention evidence is insufficient by itself rather than rejected outright; `[3]`
    (SCOPE_BROADENED) P165's immediate self-checkable feedback re-stated as the repair it is,
    conditioned on formative evidence exposing a relevance or fairness problem, not a default design
    element; `[4]` (HEDGING_REMOVED) P163's "solely from prior attainment" restored, so the rule
    forbids lowering expectations on prior attainment alone, not lowering them at all. Only `[5]`
    was visible before the report's coverage was extended.
  - **Mis-cited clause.** `source_of_truth_policy.canonical_owner` attributed certification and
    accreditation authority to P021/P172, neither of which mentions accreditation. Split into a
    grading-conversion clause (P021, P172) and a certification clause citing P096, P109, P004 — the
    same grounding `forbidden_behaviours[1]` uses.
  - **`forbidden_behaviours`** gained the two role-level prohibitions that were stated in `role`
    and `when_not_to_use` but never reached the enforcement list: never assigns a grade, mark, or
    score (P021, P172, P107) and never rules on subject-matter correctness (P193).
  - **`source_of_truth_policy.canonical_owner`** now cites the principles it restates (P107, P134,
    P193, P021, P172), closing the orphan-field gap against the ledger claim above.
  - **`outputs.primary_format` / `minimum_useful_output`** have no slot in the shared adapter
    template, so their unique "never a bare good/bad verdict" constraint never reached the model.
    Rather than edit the template shared by every package, the constraint was folded into each
    `outputs.modes[*].output`, which does render; the two fields now duplicate rendered content
    instead of holding unique content.
  - **`role`** reworded from "prototype materials" to "plan prototyping and evaluation" so no verb
    reads as build authority.
  - **Faithfulness-report coverage.** `reports/faithfulness-report.yaml` previously graded 19 rule
    locations and had zero entries for `knowledge_partition.always_on` — the 13 dense paragraphs
    compressing all 200 principles, where the over-claims above lived undetected. The report now
    carries 43 entries — per-entry verdicts for `always_on[0]`-`[12]` (per-clause where dense) plus
    the rules changed in this round — and that extension is what surfaced `[1]`, `[3]`, `[4]` and the
    `canonical_owner` mis-citation. All 43 read WITHIN_SCOPE against the repaired profile.
  - **Rights gate actually ran.** `quote_scan` had been reporting "rights NOT verified" (11
    distillation-only sources, no `sources/markdown/`, cold cache). With the book-extract cache
    warm, the 40-consecutive-word gate executed against all 11 sources: no verbatim quotation found.
  - Body trimmed to ~987 words to stay inside the profile body budget after the additions.

  **Deferred, not fixed:** the adapter's always-on invariant layer (~90 bullets loaded on every
  invocation) is compiled deterministically by `compile_invariants` from every principle that is
  `confidence: high` + `operational_mapping.profile_rule: true`, and `validate_invariant_coverage`
  gates the adapter against exactly that set. Tiering it to the ~15-20 genuinely cross-cutting
  invariants needs a generator-level notion of "cross-cutting" that does not exist; doing it from
  this package alone would either drop must-hold rules or desync the coverage gate. Recorded as a
  factory-level change, not a package edit.
