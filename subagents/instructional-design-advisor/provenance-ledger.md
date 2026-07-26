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
- **1.3.0** (2026-07-27) — Adversarial-verify repair (`/review-subagent` Step 6, `verify1`); no
  re-distillation, so the spine, principle numbering, claims, and source set are unchanged from
  1.2.0. Two must-fix findings, both closed:
  - **P157's invariant dropped the scope condition that bounds it (SCOPE_BROADENED, non-negotiable
    tier).** `compile_invariants._to_invariant` reduces a principle to its **first sentence**, and
    P157's bound ("in a system-paced presentation") sat in the second sentence — so the adapter
    stated the narration-over-onscreen-text prescription unconditioned, at the tier the adapter
    itself labels non-negotiable, while `profile.yaml:179` and
    `skills/multimedia-and-elearning-design/SKILL.md` all retained the bound. That tripped the
    package's own `forbidden_behaviours[2]` ("omitting the conditions that make a rule hold"), and
    P011 — "state the conditions with the rule" — is itself an invariant. Repaired at the root, not
    in the adapter: P157's `statement` in `principles/principles.yaml` is reordered so its first
    sentence is self-sufficient. Nothing was added to or removed from the claim — the same two
    clauses, with the condition moved to the front — and the exported invariant now opens "In a
    system-paced presentation". The one-line P157 restatement in
    `references/instructional-design-principles-index.md` was given the same bound. Three authored
    docs whose digest moved (`multimedia-and-elearning-design` and both references) were re-stamped
    via `detect_stale --stamp`; their bodies already stated the bound, so their grounding did not
    change, only the upstream digest. A sweep of all 75 invariants found P157 the only statement
    whose dropped tail narrowed scope (P092's tail adds an action, so its retained clause is not
    broadened).
  - **P107/P134 cited to ground ownership and authority claims they do not state (mis-citation,
    four sites in `profile.yaml`).** P107 = make the teaching theory explicit, then diagnose and
    adapt to local learners and constraints; P134 = improve teaching through systematic
    action-research cycles. Neither states who *owns* the course, the subject matter, the grades, or
    the decision to run it, so the advice-only ownership boundary was an orphan field value dressed
    as principle-derived (`.claude/rules/rights-and-quotation-policy.md`, Provenance requirement).
    The boundary itself is legitimate factory policy and is unchanged in force; only its false
    grounding is removed. `source_of_truth_policy.precedence` drops `P107` and leaves `P193`
    attached to the subject-matter-referral clause alone. `handoff_rules[0]` drops `P107, P134`,
    keeping `P021` on the criterion-based outcome-judgement clause it does ground.
    `source_of_truth_policy.canonical_owner` is split so `(P107, P134)` attaches only to the
    make-the-theory-explicit / adapt-to-local-constraints clause, with final authority over the
    course and its materials stated separately and uncited as policy. `forbidden_behaviours[4]`
    drops the spurious `P107`, being already fully grounded by `P021` and `P172`. All four sites
    *restrict* the advisor rather than widening a design claim, so no advice behaviour changed —
    this is a provenance repair. This supersedes the 1.2.0 decision to cite `(P107, P134, P193,
    P021, P172)` across `canonical_owner` as orphan-field closure: the citation set was right for
    the pedagogical clauses and wrong for the ownership clauses, which carry no principle support.

  **Recorded at this gate, no action taken** — all template- or factory-level rather than package
  defects: the invariant-preamble carve-out at `templates/claude-agent-adapter.md.j2:23` names only
  Role and Forbidden behaviours, omitting `When NOT to use`, `Handoff rules`, and
  `Source of truth policy` (neutralised in practice by the Role paragraph); and
  `minimum_useful_output` / `outputs.primary_format` still have no template block in any package.
  Verify also confirmed clean: 0/75 truncated invariants, adapter vs `compile_invariants`
  byte-identical, all 97 inline `PNNN` citations resolving, profile→adapter fidelity verbatim across
  every rendered block, and the `Read, Grep, Glob` tool grant unwidened.
[38;2;102;102;102m-[39m[38;2;187;187;187m [39m[38;2;102;102;102m**[39m[38;2;102;102;102m1.3[39m[38;2;102;102;102m.0[39m[38;2;102;102;102m**[39m[38;2;187;187;187m [39m([38;2;102;102;102m2026[39m[38;2;102;102;102m-[39m[38;2;102;102;102m07[39m[38;2;102;102;102m-[39m[38;2;102;102;102m27[39m)[38;2;187;187;187m [39m—[38;2;187;187;187m [39mAdversarial[38;2;102;102;102m-[39mverify[38;2;187;187;187m [39m[38;2;170;34;255;01mrepair[39;00m[38;2;187;187;187m [39m(`/review-subagent`[38;2;187;187;187m [39mStep[38;2;187;187;187m [39m[38;2;102;102;102m6[39m,[38;2;187;187;187m [39m`verify1`);[38;2;187;187;187m [39m[38;2;170;34;255;01mno[39;00m
[38;2;187;187;187m  [39mre[38;2;102;102;102m-[39mdistillation,[38;2;187;187;187m [39mso[38;2;187;187;187m [39mthe[38;2;187;187;187m [39mspine,[38;2;187;187;187m [39mprinciple[38;2;187;187;187m [39mnumbering,[38;2;187;187;187m [39mclaims,[38;2;187;187;187m [39m[38;2;170;34;255;01mand[39;00m[38;2;187;187;187m [39m[38;2;170;34;255;01msource[39;00m[38;2;187;187;187m [39m[38;2;170;34;255;01mset[39;00m[38;2;187;187;187m [39mare[38;2;187;187;187m [39munchanged[38;2;187;187;187m [39m[38;2;170;34;255;01mfrom[39;00m
[38;2;187;187;187m  [39m[38;2;102;102;102m1.2[39m[38;2;102;102;102m.0[39m.[38;2;187;187;187m [39mTwo[38;2;187;187;187m [39mmust[38;2;102;102;102m-[39mfix[38;2;187;187;187m [39mfindings,[38;2;187;187;187m [39m[38;2;170;34;255;01mboth[39;00m[38;2;187;187;187m [39mclosed[38;2;102;102;102m:[39m
[38;2;187;187;187m  [39m[38;2;102;102;102m-[39m[38;2;187;187;187m [39m[38;2;102;102;102m**[39mP157[38;2;187;187;187m [39minvariant[38;2;187;187;187m [39mdropped[38;2;187;187;187m [39mthe[38;2;187;187;187m [39mscope[38;2;187;187;187m [39m[38;2;170;34;255;01mcondition[39;00m[38;2;187;187;187m [39mthat[38;2;187;187;187m [39mbounds[38;2;187;187;187m [39mit[38;2;187;187;187m [39m(SCOPE_BROADENED,[38;2;187;187;187m [39mnon[38;2;102;102;102m-[39mnegotiable
[38;2;187;187;187m    [39mtier).[38;2;102;102;102m**[39m[38;2;187;187;187m [39m`compile_invariants._to_invariant`[38;2;187;187;187m [39mreduces[38;2;187;187;187m [39ma[38;2;187;187;187m [39mprinciple[38;2;187;187;187m [39m[38;2;170;34;255;01mto[39;00m[38;2;187;187;187m [39mits[38;2;187;187;187m [39m[38;2;102;102;102m**[39m[38;2;170;34;255;01mfirst[39;00m[38;2;187;187;187m [39msentence[38;2;102;102;102m**[39m;
[38;2;187;187;187m    [39mP157[38;2;187;68;68m'[39m[38;2;187;68;68ms bound ("in a system-paced presentation") sat in the second sentence, so the adapter[39m
[38;2;187;68;68m    stated the narration-over-onscreen-text prescription unconditioned, at the tier the adapter[39m
[38;2;187;68;68m    itself labels non-negotiable — while `profile.yaml` and[39m
[38;2;187;68;68m    `skills/multimedia-and-elearning-design/SKILL.md` all retained the bound. This tripped the[39m
[38;2;187;68;68m    package[39m[38;2;187;68;68m'[39ms[38;2;187;187;187m [39mown[38;2;187;187;187m [39m`forbidden_behaviours[2]`[38;2;187;187;187m [39m([38;2;187;68;68m"[39m[38;2;187;68;68momitting the conditions that make a rule hold[39m[38;2;187;68;68m"[39m).
[38;2;187;187;187m    [39mRepaired[38;2;187;187;187m [39m[38;2;170;34;255;01mat[39;00m[38;2;187;187;187m [39mthe[38;2;187;187;187m [39mroot,[38;2;187;187;187m [39m[38;2;170;34;255;01mnot[39;00m[38;2;187;187;187m [39m[38;2;170;34;255;01min[39;00m[38;2;187;187;187m [39mthe[38;2;187;187;187m [39madapter[38;2;102;102;102m:[39m[38;2;187;187;187m [39mP157[38;2;187;68;68m'[39m[38;2;187;68;68ms `statement` in[39m
[38;2;187;68;68m    `principles/principles.yaml` is reordered so the first sentence is self-sufficient. Nothing[39m
[38;2;187;68;68m    was added or removed from the claim — the same two clauses, the condition moved to the front —[39m
[38;2;187;68;68m    and the exported invariant now carries "In a system-paced presentation". Re-stamped the three[39m
[38;2;187;68;68m    authored docs whose digest moved (`multimedia-and-elearning-design` and both references); their[39m
[38;2;187;68;68m    bodies already stated the bound, so only the upstream digest changed, not their grounding.[39m
[38;2;187;68;68m  - **P107/P134 cited to ground ownership and authority claims they do not state (mis-citation,[39m
[38;2;187;68;68m    four sites).** P107 = make the teaching theory explicit and adapt it to local learners and[39m
[38;2;187;68;68m    constraints; P134 = improve teaching through systematic action-research cycles. Neither states[39m
[38;2;187;68;68m    who owns the course, the subject matter, the grades, or the decision to run it, so the[39m
[38;2;187;68;68m    advice-only ownership boundary was an orphan field value dressed as principle-derived[39m
[38;2;187;68;68m    (`.claude/rules/rights-and-quotation-policy.md`, Provenance requirement). The boundary itself is[39m
[38;2;187;68;68m    legitimate factory policy and is unchanged in force; only its false grounding is removed:[39m
[38;2;187;68;68m    `source_of_truth_policy.precedence` drops `P107` and leaves `P193` on the subject-matter-referral[39m
[38;2;187;68;68m    clause alone; `handoff_rules[0]` drops `P107, P134` and keeps `P021` on the criterion-based[39m
[38;2;187;68;68m    outcome-judgement clause; `source_of_truth_policy.canonical_owner` is split so `(P107, P134)`[39m
[38;2;187;68;68m    attaches only to the make-explicit/adapt clause, with final authority over the course stated[39m
[38;2;187;68;68m    separately and uncited; `forbidden_behaviours[4]` drops the spurious `P107`, already fully[39m
[38;2;187;68;68m    grounded by `P021` and `P172`. All four sites *restrict* the advisor, so no advice-quality[39m
[38;2;187;68;68m    behaviour changed — this is a provenance repair.[39m

[38;2;187;68;68m  **Recorded, no action at this gate** (from the same verify pass, all template- or factory-level[39m
[38;2;187;68;68m  rather than package defects): the invariant-preamble carve-out at[39m
[38;2;187;68;68m  `templates/claude-agent-adapter.md.j2:23` names only Role and Forbidden behaviours, omitting[39m
[38;2;187;68;68m  `When NOT to use`, `Handoff rules`, and `Source of truth policy` — neutralised in practice by the[39m
[38;2;187;68;68m  Role paragraph; and `minimum_useful_output` / `outputs.primary_format` still have no template[39m
[38;2;187;68;68m  block in any package. Verify also confirmed clean: 0/75 truncated invariants, adapter-vs-[39m
[38;2;187;68;68m  `compile_invariants` byte-identical, all 97 inline `PNNN` citations resolving, profile→adapter[39m
[38;2;187;68;68m  fidelity verbatim across all rendered blocks, and the `Read, Grep, Glob` tool grant.[39m
