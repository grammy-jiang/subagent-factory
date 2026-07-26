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

**Declared exception — structural-policy clauses (since 1.4.0).** Two clauses are deliberately
uncited and are *not* orphan field values: the authority sentence in
`source_of_truth_policy.canonical_owner` ("final authority over the course, its materials, and what
is taught rests with the teacher of record and the institution") and the advisor-boundary half of
`forbidden_behaviours[0]` ("the advisor supplies review criteria" rather than building the
deliverable). These state *who owns the work and what this agent may do*, not a claim about
instructional design. They are factory-level structural policy — the same category as the
advice-only boundary applied to every specialist package — and are therefore exempt from
per-principle QID citation under `.claude/rules/rights-and-quotation-policy.md`. The alternative
was worse and was tried: 1.2.0 cited them to `P107`/`P134`/`P193`, principles about making teaching
theory explicit, action-research cycles, and giving a content expert explicit review standards —
none of which states who owns a course. 1.3.0 and 1.4.0 removed that false grounding rather than
substituting another. A future reviewer should read these two clauses as an intentional carve-out,
not a citation gap.

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
- **1.4.0** (2026-07-27) — Review-loop repair round r1 (`/review-subagent`; consolidated panel of
  deterministic gates + agent-skills-advisor + profile-reviewer + faithfulness-reviewer +
  ai-agent-engineering-reviewer). No re-distillation, so the spine, principle numbering, claims, and
  the eleven sources are unchanged from 1.3.0. Three must-fix and four should-fix findings closed:
  - **Stray `</content>` wrapper tag shipped in 11 of the 13 `SKILL.md` files.** Each file ended in a
    closing tag with no opening tag anywhere in it — an authoring-wrapper delimiter that leaked out
    of the skill-author step and survived post-processing (only `instructional-strategy-and-events`
    and `teaching-scholarship-and-quality` were clean). Skill bodies load verbatim into model context
    at trigger time, so this was uninterpretable noise in 85% of them; `validate_generated_package`
    has no check for an unmatched wrapper tag. The trailing line is stripped from all 11 files, each
    of which now ends at its "Derived from …" provenance sentence. Nothing else in any body changed:
    every frontmatter `provenance` block and every inline `(Pxxx)` citation is byte-identical.
  - **`provenance-ledger.md` carried a colorized-diff paste — 38 raw ANSI escape sequences** across
    lines 180-218, the only ANSI bytes in the package. The block was a terminal-rendered `git`/`delta`
    diff of the 1.3.0 edit captured into the canonical ledger, giving one version two histories: a
    clean entry at 132-179 and a control-character-laden, reworded restatement after it that had also
    lost the precise `profile.yaml:179` locator. Because the ledger is the canonical audit record
    (`.claude/rules/generated-artifact-policy.md`), ANSI bytes break every plain-text tool run against
    it. The duplicate is deleted; the clean 1.3.0 entry is authoritative and unchanged. Root cause is
    the known ANSI-paste class — compose ledger entries with the Write tool or `git --no-color`.
  - **`reports/faithfulness-report.yaml` was stale at four sites.** It was last regenerated at 1.2.0,
    so it still described the pre-1.3.0 citations that the adversarial-verify round had already
    removed: `handoff_rules[0]` ("Restates P107/P021/P134"), `source_of_truth_policy.precedence`
    (P107 in the citation list), `forbidden_behaviours[4]` ("P107 … is a weak, tangential citation
    here"), and `source_of_truth_policy.canonical_owner` (quoting a sentence structure that the 1.3.0
    split no longer produces). As the tier-2 artifact of record for whether shipped rules over-claim,
    it would have told a reader that a mis-citation was still live at four sites after it was fixed.
    All four entries are rewritten in the `"REPAIRED in 1.x.0 … Now WITHIN_SCOPE"` pattern already
    used for the `knowledge_partition.always_on[1]/[3]/[4]` entries, so the repair is recorded rather
    than the pre-fix prose left standing. **Regenerating or hand-refreshing the faithfulness report is
    now part of the version-bump checklist** — a profile citation edit that skips it is the recurring
    failure mode this finding represents.
  - **`forbidden_behaviours[0]` stretched `P193` onto a clause it does not ground.** P193 is
    specifically about giving a *qualified content expert* validated goals and skill frameworks as
    explicit review standards for subject-matter correctness — used correctly for exactly that at
    `forbidden_behaviours[5]` and `handoff_rules[1]`. Here it was carrying the general
    "advisor supplies review criteria rather than building the deliverable" boundary, which no
    principle states. This is the same category as the tangential `P107` citations 1.3.0 removed at
    four other sites; this instance was missed then. `P193` is dropped; `P107` already grounds the
    "practitioner makes the teaching theory their own" half, and the advisor-boundary half now stands
    as uncited structural policy under the carve-out declared at the head of this ledger. Not a
    strength over-claim in either form — the clause is an advisory *restriction*, so a weak citation
    could not make it stronger than source; no advice behaviour changed.
  - **Uncited ownership clauses declared an accepted exception, not an orphan gap.** 1.3.0 removed a
    wrong `(P107, P134)` from the `canonical_owner` authority sentence rather than substituting a
    false one, but recorded that only as inline changelog prose, leaving the next reviewer unable to
    tell an intentional carve-out from a missed citation — and the `forbidden_behaviours[0]` fix above
    creates a second instance. Both are now declared at the head of this ledger as factory-level
    structural policy, exempt from the per-principle QID requirement in
    `.claude/rules/rights-and-quotation-policy.md`.
  - **Profile body trimmed 994 -> 935 words.** The phase-8 soft budget is 800 with a hard FAIL above
    1000, so at 994 the package had a **6-word margin**: any future citation or clause addition would
    have blocked validation, and the 1.2.0 entry recorded the trim to "~987 words" without ever
    stating that the residual WARNING was an accepted release state. Only redundant prose was cut —
    the enumerated advice-only tail of `role` (restated in full by `when_not_to_use` and
    `forbidden_behaviours`), the "built deliverable / promise of effectiveness" tails duplicated
    across `outputs.primary_format` and `modes[advise]` (stated in full at `forbidden_behaviours[0]`
    and `[1]`), and clause-level compression in `quality_bar[0]`/`[1]`, `forbidden_behaviours[2]`/`[4]`,
    and `handoff_rules[0]`. Every `P`-id citation and every distinct rule survives; the three
    faithfulness entries quoting the changed wording were updated with it. **The phase-8 body-size
    WARNING is accepted as a known release state at 935 words (65-word margin to the hard FAIL);** the
    remaining weight is irreducible without dropping grounded content, since each surviving clause
    carries the substance of the principle it cites.
  - **Citation-discipline clause added to `source_of_truth_policy.canonical_owner`.** The adapter
    cites ~30 principle IDs — across Quality bar, Forbidden behaviours, handoff rules, both worked
    examples, and the source-of-truth policy — whose text never appears in the loaded prompt, because
    the printed "Operating invariants (must hold)" list covers only the curated
    `confidence: high` + `profile_rule: true` subset. Spot-verified: P096, P109, P148, P187, P021,
    P193, and P107 each appear 1-5x in the adapter body and 0x as a defined invariant, and the worked
    examples model the behaviour of citing them. The runtime risk is a fabricated or misremembered
    gloss attached to a real-looking ID. Rather than an ID-gloss appendix (which would consume the
    body-size budget the finding above is trying to protect), the field now directs the agent to read
    `references/instructional-design-principles-index.md` for any cited ID not spelled out in the
    invariants list and use its stated content. `canonical_owner` was chosen because it renders into
    the adapter *and* is excluded from the phase-8 body-size word count, so the fix costs no headroom.
    This is a citation-apparatus completeness fix, not a content-faithfulness one — the plain-English
    rule text already stood alone and stayed obeyable.

  **Recorded at this gate, no action taken** — factory- or template-level rather than package
  defects: `outputs.primary_format` and `minimum_useful_output` still render nowhere in the adapter
  (re-confirmed against `templates/claude-agent-adapter.md.j2`, which has slots for
  `canonical_owner` and `precedence` only), so their content stays duplicated into
  `outputs.modes[*].output` to reach the model — re-flagged here rather than silently carried; the
  validator has no check that FAILs on an unmatched `<content>`/`</content>` wrapper in an exported
  `SKILL.md`, which is what let the finding above ship; and `instructional-strategy-and-events` loads
  35 principles on any trigger (~2x its largest sibling), where a split along its five existing `###`
  seams would break the 13-skill <-> 13 `knowledge_partition.always_on` 1:1 mapping and force a
  further profile edit under body-size pressure — deferred to a later version as a scoped change of
  its own.
- **1.5.0** (2026-07-27) — Adversarial-verify repair (`/review-subagent` Step 6, `verify2`); no
  re-distillation, so the spine, principle numbering, claims, and the eleven sources are unchanged
  from 1.4.0. The gate consolidated to **1 must-fix**, with one raw must-fix adjudicated down and
  five advisories. Every edit below either restores a cited principle's own scope condition or
  attaches a citation to a clause that principle actually states; no claim absent from
  `principles/principles.yaml` was introduced, and the advice-only ownership and safety hedges are
  unchanged in force.
  - **`examples[0].ideal_response` flattened P067's degree-caution into a categorical bar
    (HEDGING_REMOVED).** The worked example asserted that "A multiple-choice quiz **cannot show
    understanding**". P067 states something materially weaker: evidence of understanding is *less
    direct and more complicated than* objective-test evidence, since a right answer can come from
    rote recall, test-taking skill, or a lucky guess — and *therefore* ferret out the reasons behind
    answers and the meaning the learner makes of results rather than the percentage correct. It is a
    directness/complexity caution carrying a remedy, and it does not rule multiple-choice evidence
    out. The profile kept P067's *reason* clause intact in substance, which is precisely what made
    the surrounding overclaim read as sourced. Graded must-fix rather than advisory for two reasons
    that do not apply to the advisories below: an `ideal_response` is a template for the exact
    phrasing the generated subagent emits to a caller, not citation hygiene; and it survived export
    verbatim into the installed adapter, so the over-strong form was live in the runtime artifact.
    It is also the exact failure the evidence protocol names — a hedged source claim rendered as an
    unconditional rule — and this package's own `forbidden_behaviours[2]` forbids it. Repaired by
    restating the sentence at the source's strength and restoring the remedy clause the profile had
    dropped: evidence of understanding is less direct and more complicated than what a
    multiple-choice quiz yields, so ferret out the reasons behind the answers rather than the
    percentage correct (P067). The example's rhetorical force and the transfer-testing
    recommendation that follows (P153, P196, P016, P017) are unchanged.
  - **`quality_bar[5]` — citation did not cover the "workplace transfer" clause.** The rule cited
    `(P148, P152, P140, P004)`; P148 is front-end analysis, P152 experiential prototyping, P140
    formative evaluation of a *draft*, P004 grounding adequacy claims in learning rather than
    enrolment or satisfaction. None states workplace transfer. The claim was true and grounded
    elsewhere in the profile (`always_on[10]`, `forbidden_behaviours[1]`) but not at the site, which
    is the orphan-field pattern `.claude/rules/rights-and-quotation-policy.md` prohibits. `P096` —
    evaluate impact only after target learners can perform in context, gathering unobtrusive
    workplace evidence about need resolution, capability use, and performance change — is added to
    the list. Citation-precision repair; no rule text changed.
  - **`knowledge_partition.always_on[10]` listed `P041` among its ids with no sentence reflecting
    it.** Dropping the id would have left P041 covered by no block at all (block membership is how
    this package accounts for all 200 principles), so the block gains the principle's content
    instead: an innovation persists only where it has an identifiable support group and constituency
    and can be monitored cost-effectively. In scope for the impact-and-evaluation block it sits in,
    and a direct restatement rather than an extension. `always_on` is excluded from the phase-8
    body-size word count, so this costs no headroom.

  **Adjudicated down at this gate — recorded, not fixed.** The faithfulness reviewer raised
  `forbidden_behaviours[0]`'s trailing `(P107)` as a second must-fix (SCOPE_BROADENED: P107 grounds
  the sentence's second clause, "the practitioner makes the teaching theory their own", not the
  deliverable-building prohibition in the first). Downgraded on two independent grounds. First,
  direction of claim: the faithfulness rule bars a rule being *stronger* than its evidence — an
  agent asserting more about the world than the source supports — whereas this is a self-restricting
  role boundary that forbids the agent from acting, and under-claiming its own authority carries
  none of the risk the rule exists to prevent. Second, it re-litigates a closed decision: `verify1`
  examined this exact compound construction, accepted it, and applied the strips at the sites where
  P107 was grounding an *ownership/authority* claim — the 1.3.0 entry above records that. Real but
  minor; worth tightening on a future pass.

  **Recorded at this gate, no action taken** — factory- or template-level, or fairly read as
  in-scope: `compile_invariants._to_invariant()` renders only each principle's first sentence,
  dropping an operative second sentence on 6 of 75 rules (P157, P153, P122, P092, P156, P002) — but
  every retained rule is a grammatically complete, self-sufficient sentence with no mid-clause cut,
  and this is documented, deliberate behaviour systemic across all packages, with P153's and P092's
  dropped enforcement halves surviving via the quality bar and the skill bodies; invariants inherit
  the domain's "do the teaching" imperative voice (P033, P037, P018), contained by three explicit
  precedence guards in the adapter plus the failure-recovery worked example that demonstrates
  declining exactly that; `forbidden_behaviours[3]` cites `P093` (do not *add* seductive details) on
  a rule about *treating* added interest as evidence learning occurred — adjacent theme, imprecise
  fit, fairly read as WITHIN_SCOPE; and `source_of_truth_policy.precedence` cites only `P193` on a
  clause also covering teacher-of-record and institutional ownership, left uncited deliberately
  because 1.3.0 established that the ownership boundary is factory policy, not principle-derived.
  Verify also confirmed clean: 75/75 invariants compiled and rendered with 0 truncation, adapter
  byte-identical to the package copy, all 22 non-invariant principle ids resolving in the index, the
  advice-only role holding (every certify/accredit/grade/score occurrence is a negation), and the
  `Read, Grep, Glob` tool grant unwidened.
