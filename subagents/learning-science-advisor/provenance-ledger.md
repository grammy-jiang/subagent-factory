# Provenance Ledger — learning-science-advisor

Canonical record of what grounds this subagent. The profile, skills, references, faithfulness
report, and tests are all derived from the distilled spine in this package
(`principles/principles.yaml` -> `analysis/claims.jsonl` -> `evidence/evidence-records.yaml` ->
`sources/anchors/*.anchors.jsonl`), assembled by the map->reduce build. No load-bearing profile rule
field is an orphan: every `quality_bar`, `forbidden_behaviours`, `handoff_rules`,
`knowledge_partition.always_on`, and `source_of_truth_policy` value cites the promoted principle(s)
it restates. (Descriptive fields — `role`, `when_to_use`, `inputs`, `outputs`, and
`minimum_useful_output` — carry no inline tags, per repo convention.)

Eight fields are **authored**, not distilled, and say so inline rather than citing a principle they
do not have.

**Inclusion rule for this table (added at 1.4.0, so future audits are mechanical rather than manual):**
a field belongs here when it is **fully** authored — it carries zero principle citations anywhere in its
text. A **mixed** field — part principle-cited, part tagged `(authored …)`, e.g. `handoff_rules[0]` and
`handoff_rules[1]` — correctly stays out, because it is not an orphan: every clause either cites the
principle it restates or is tagged authored inline. To re-derive the table, list every
`quality_bar` / `forbidden_behaviours` / `handoff_rules` / `knowledge_partition.always_on` /
`source_of_truth_policy` value with no `P###` in it; that list must equal the rows below.

| Field | Kind | Why it carries no principle |
|-------|------|------------------------------|
| `quality_bar[6]` ("Output floor") | authored output floor | Restates `outputs.primary_format` + `minimum_useful_output` so the export template, which renders neither, still carries the output floor into the deployed adapter. It is a format rule, not a domain claim. |
| `forbidden_behaviours[0]` (teaching performed) | authored scope boundary | Row added at 1.4.0; the field itself has been uncited since 1.2.1, which superseded its `(P010, P077)` citation with `(authored scope boundary)` but never added the row. Mirrors `when_not_to_use[0]`. No source principle states *who performs* teaching, delivery, authoring, or marking; the boundary is a repo-policy decision. |
| `forbidden_behaviours[2]` (placement/grading/admission/promotion/employment) | authored scope boundary | Row added at 1.4.0; uncited since 1.2.1, which superseded its `(P128, P087)` citation with `(authored scope boundary)` but never added the row. Mirrors `when_not_to_use[2]`, and `handoff_rules[1]` names the body that owns those decisions. No source principle grants or withholds authority over them. |
| `forbidden_behaviours[5]` (numeric claims) | authored evidence guardrail | Added at 1.2.0. A ban on citing an effect size, statistic, or numeric benchmark absent from the invoked principle's own statement is a guardrail on the agent's output discipline, not a claim about learning; no source principle states it. Distinct from `forbidden_behaviours[3]`, which fences over-claimed certainty and generality rather than invented precision. |
| `forbidden_behaviours[6]` | authored scope boundary | Mirrors `when_not_to_use[4]`. No source principle grants or withholds authority over education law, accreditation, safeguarding, or institutional policy; the boundary is a repo-policy decision. |
| `forbidden_behaviours[7]` (subject-matter rulings) | authored scope boundary | Added at 1.3.0. Mirrors `when_not_to_use[3]`, which until then was the only routing exclusion with no enforceable forbidden-behaviour counterpart. No source principle grants or withholds authority over the subject matter a course teaches; the advice-only/subject-matter split is a repo-policy decision. |
| `handoff_rules[2]` | authored scope boundary | The named-authority half of the `forbidden_behaviours[6]` boundary. |
| `source_of_truth_policy.canonical_owner` | authored scope boundary | Added to this table at 1.3.0 (the value itself is unchanged since 1.0.0). It names the same authorities as `handoff_rules[0]`–`[2]` — teacher/designer/institution over curriculum, materials, delivery and marks; qualified specialists over assessing or diagnosing an individual learner; the responsible body over placement, grading, admission and employment decisions — as a single ownership statement. No source principle grants or withholds those authorities, so it carries no P-code by design rather than being an orphan field value. Its sibling `precedence` is principle-cited and unaffected. |

Two principles are cited as backing inside `knowledge_partition.always_on` while carrying
`operational_mapping.profile_rule: false` in `principles/principles.yaml` — P092 (`always_on[0]`)
and P098 (`always_on[4]`). This is not a conflict: the `always_on` blocks are the scope paragraphs
of the skills that own those principles, not profile **rule** fields, and `profile_rule` governs
only whether a principle drives a rule field. The flags are correct and the citations are load-bearing
for skill scope. (P092 is `confidence: medium`, so it is also outside the adapter's compiled
must-hold invariant tier, which takes high-confidence principles only.)

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

- **1.4.0** (2026-07-27) — Review round r1 fix pass
  (`reports/review-loop/learning-science-advisor.r1.review.md`), must-fix = 3, all applied, plus every
  should-fix and the two cheap `nice` audit-trail items. Supersedes, and states what it supersedes:
  - **F1 — stray `</content>` generation artifact removed** from the last line of
    `skills/cognitive-load-worked-examples-and-scaffolding/SKILL.md`. Verified the only occurrence in the
    package; a one-off tool-wrapper leak, not a template defect. No content changed.
  - **F2 — S3 (the unexercised rights gate) is now CLOSED, not deferred.** The validator's `quote-scan`
    WARN persists in this worktree because neither `sources/markdown/` nor a local
    `cache/book-extracts/` exists here, which made the standalone `quote_scan` PASS vacuous and put
    `status: ready` in direct conflict with 1.3.0's "must be run once … before release". The warm
    map-reduce cache *does* exist in the main checkout, so the gate was run for real against it:
    `quote_scan_report(subagents/learning-science-advisor,
    cache_root=/home/grammy-jiang/projects/subagent-factory/cache/book-extracts)` →
    `{"restricted": 12, "scanned": true}`, **0 findings**. All twelve `distillation-only` sources were
    loaded and compared; no 40-word verbatim run from any of them appears anywhere in the package. The
    surviving validator WARN is now an environment fact about this worktree (no cache under its own
    root), not an open rights question, and `status: ready` no longer contradicts this ledger.
  - **F3 — the authored-field exception table superseded: "Six fields" → "Eight fields".**
    `forbidden_behaviours[0]` and `[2]` have carried zero P-codes since 1.2.1 superseded their
    `(P010, P077)` and `(P128, P087)` citations with `(authored scope boundary)`; that pass never added
    the matching table rows, so both were orphan field values under
    `.claude/rules/rights-and-quotation-policy.md` and falsified this ledger's own completeness claim.
    Rows added with the same authored-scope-boundary rationale already used for `[6]`/`[7]`. The root
    cause — no stated inclusion rule, so the audit was manual and recurred — is fixed by the new
    **inclusion rule** above the table: *fully* authored (zero citations anywhere) belongs in it, *mixed*
    fields (`handoff_rules[0]`, `[1]`) correctly stay out, and the re-derivation recipe is stated so the
    check is mechanical. Verified: the mechanical list reproduces exactly the eight rows.
  - **F4/F5 — P100 rescoped at the source and rehomed, resolving the adapter/charter contradiction that
    1.3.1 only half-closed.** 1.3.1 dropped P100's `always_on[10]` citation but left the principle in
    `expertise-development-and-transfer`, which left it charter-orphaned (present in no `always_on` block
    at all — 149 of 150 principles were carried) and still rendering, in the adapter's precedence-taking
    *Operating invariants* layer, as imperative individual-diagnostic advice against
    `router_description`, `when_not_to_use[1]` and `forbidden_behaviours[1]`. Both halves are now fixed:
    - **Statement rescoped** from "When advising on assessment for a persistent reading difficulty,
      recommend real-word reading, spelling ability and word attack skills as the diagnostic measures to
      collect …" to "When **a school or programme team designs what a reading-difficulty assessment or
      intervention screens for**, recommend that real-word reading, spelling ability and word attack
      skills **be among the measures collected**, since they are the greatest predictors of reading
      comprehension." This is a **narrowing**, not a strengthening: the "greatest predictors" clause is
      carried verbatim from C03615, and the programme-design framing is C04895's own ("assessment and
      intervention should identify the affected process"). `applies_when[0]` and `[1]` rescoped to match,
      so the statement stays self-sufficient under the invariant compiler's `applies_when` stripping.
    - **Rehomed** from `expertise-development-and-transfer` (lens: matching support to growing expertise
      and validating transfer claims) to `prior-knowledge-prediction-and-misconceptions` (lens: surfacing
      what learners already hold before instruction), which is where identifying the affected component
      process belongs. The partition stays 1:1 — 150 principles, each owned by exactly one skill — and
      P100 regains an `always_on` home: `always_on[4]` gains a matching clause and cites it. The
      expertise skill's `when to use` trigger, Procedure step, anti-pattern and Provenance list drop it;
      the prior-knowledge skill gains them, with the referral to a qualified assessor stated explicitly
      in the Procedure step. `.build/authoring/gen.py`'s `ALWAYS_ON_EXCLUDE` entry is retired (now empty)
      because the exclusion it encoded no longer exists.
    - **Derived restatements re-synced:** the `lead()`-truncated P100 entry moved between skill groups in
      `references/learning-science-principles-index.md`, and `PB-P100` in
      `tests/principle-behaviour-tests.yaml` re-pointed at the prior-knowledge lens with the rescoped
      `expected_behaviour`.
  - **F6 — `handoff_rules[1]` now enumerates "promotion"**, restoring the three-way parallel with
    `when_not_to_use[2]` and `forbidden_behaviours[2]`. Promotion decisions were forbidden and out of
    scope but no rule named who owns them; they now route to the responsible body with the rest.
  - **F7 — `inputs.required[3]` gained a defined fallback**: "If it cannot be located, state the point
    plainly without the citation and keep the safeguard." Twelve codes cited in `quality_bar` /
    `forbidden_behaviours` are not in the rendered Operating invariants, so their statements must be read
    from a skill file or the principles index before citing; until now nothing said what to do when that
    read fails (standalone `export-deployable` without the `skills/` siblings, moved file, denied read),
    leaving silent failure as the only defined outcome and the safeguards uncheckable from the adapter
    text alone.
  - **F8 — shared boilerplate removed from all 15 `skills/*/SKILL.md`** (DRY; pure context cost at every
    invocation). The byte-identical second `## Inputs` bullet is dropped — `inputs.required[0]` already
    carries it; each `## Output` section's four-line paragraph is replaced by a pointer to the profile's
    `outputs` contract and quality bar, keeping the forbidden-behaviours/handoff-rules sentence verbatim;
    and each `## Provenance` drops the ~100-word 12-source bibliography (carried by this ledger and
    `references/learning-science-evidence-notes.md`) while keeping its full `Derived from P0xx…` list and
    the frontmatter pointer. `gen.py` updated to emit the same shape so a regeneration cannot reintroduce
    the duplication. **No principle citation, anti-pattern, procedure step or worked example was
    touched**, and every frontmatter `provenance` block is byte-for-byte unchanged apart from the two
    `authored_from_digest` re-stamps forced by the P100 statement edit.
  - **F10/F14 — faithfulness report completed.** Added `rule_ref` entries for the three
    `outputs.modes[*].trigger` values (named in-scope by the faithfulness-review skill but never covered)
    and for `router_description`, `role` and `inputs.required`. All six are routing/descriptive prose with
    no source-attributed claim, so all grade `WITHIN_SCOPE` as not gradable for over-claim — an
    audit-trail gap, not a live over-claim. `always_on[4]`'s note now lists P100; the
    `outputs.primary_format` note re-synced to the trimmed field wording.
  - **F9 — the per-entry body-word-count convention restored** (recorded retrospectively on 1.3.1 above).
  - **Body-word budget.** F6 (+1) and F7 (+15) had to be paid for in the same pass; recovered by trimming
    wording only, never a citation, hedge, or boundary clause: `role` (the ledger pointer now names the
    file, not "recorded in this package's"), `when_to_use[0]`/`[2]`, `inputs.required[0]`–`[2]` (phrasing
    only — ask-for-missing-context, Glob/Grep + root-relative resolution all retain their full operative
    content), `outputs.primary_format` and `minimum_useful_output` (neither is rendered by the export
    template; `quality_bar[6]` carries the output floor into the adapter and is untouched),
    `handoff_rules[0]` ("residual trade-off" → "trade-off") and `precedence`.
    **Final body: 993 words.**
  - **Not applied (r1 `nice`, non-gating, recorded so the next touch can pick them up):** F11 — the
    `development-diversity-and-individual-differences` slug sits at exactly the 48-char limit (renaming
    churns the skill directory, its frontmatter, the partition and every cross-reference for 3 characters
    of margin); F12 — only 1 of 15 skill `description`s carries a "not X" boundary clause, and no
    mis-triggering has been observed; F13 — `router_description` is a ~165-word paragraph whose 15-clause
    `Covers:` list works against router matching, but its exclusions are load-bearing and collapsing the
    list is a behavioural change better made with a triggering measurement behind it.
  - No claim absent from `principles/principles.yaml` was introduced, and no rule was strengthened — the
    one behavioural rule that changed (P100) was **narrowed**. No hedge or safety clause was dropped.
    Adapter re-exported from the profile.

- **1.3.1** (2026-07-27) — Adversarial verify gate #2
  (`reports/review-loop/learning-science-advisor.verify2.md`), must-fix = 1, applied. Both lanes
  converged on P100 from opposite directions. Supersedes, and states what it supersedes:
  - **MUST_FIX 1a — P100's citation in `knowledge_partition.always_on[10]` superseded (dropped).**
    P100 is reading-diagnostic measure selection; the expertise/transfer paragraph is about
    goal-directed practice, feedback, coaching, simulation, applicability boundaries, far transfer and
    multi-dimensional competence, and restates none of it. It was P100's only use in `profile.yaml`, so
    the citation sent a reader to an unrelated rule. Dropped; the remaining ten citations already ground
    every claim in the paragraph, so nothing became unsupported. The skill
    `expertise-development-and-transfer` **keeps** P100 — it routes on it and restates it correctly at
    `## Procedure` step 2 — so the principle keeps a home. `.build/authoring/gen.py` gained an
    `ALWAYS_ON_EXCLUDE` entry so a regeneration does not silently re-add the link.
  - **MUST_FIX 1b — P100's imperative statement superseded.** The invariant compiler strips
    `applies_when`, so P100 reached the always-loaded layer as an unconditional "Collect real-word
    reading, spelling ability and word attack skills as the diagnostic measures" — the only invariant of
    the 54 phrased as an act-on-an-individual instruction, sitting against `forbidden_behaviours[1]`
    ("Diagnosing … an individual learner"), `when_not_to_use[1]` and the router's diagnosis exclusion.
    The statement is now self-sufficient under stripping: "When advising on assessment for a persistent
    reading difficulty, recommend real-word reading, spelling ability and word attack skills as the
    diagnostic measures to collect, since they are the greatest predictors of reading comprehension."
    The condition is P100's own `applies_when[1]` and C04895's recorded `condition`; the advisory verb
    matches the skill body's existing wording. No evidence strengthened — the "greatest predictors"
    clause is carried verbatim from C03615.
  - **NICE_TO_HAVE (P146 altitude drift) — applied in the same pass.** P146 rendered as a
    child-welfare action ("Protect developmentally sensitive periods by preventing severe early
    deprivation…") rather than a learning-design criterion, and its `operational_mapping.test_cases`
    entry read "Prioritize early enriched **placement**…" while `forbidden_behaviours[2]` forbids
    placement decisions. Statement reframed to "Advise that developmentally sensitive periods be
    protected by preventing …"; the test case renamed to "Recommend early enriched input and
    longitudinal tracking of cognitive recovery" (and its `test_id` in
    `tests/principle-behaviour-tests.yaml`, which mirrors that descriptor); `always_on[13]`'s "It
    protects…" → "It advises protecting…". Wording only — the adapter never granted authority here, and
    no evidence, hedge or scope changed.
  - **Derived restatements re-synced, not re-authored:** the `lead()`-truncated forms of P100 and P146
    in `references/learning-science-principles-index.md` and in the two `expected_behaviour` lines of
    `tests/principle-behaviour-tests.yaml`, and the `always_on[10]` note in
    `reports/faithfulness-report.yaml` (P100 removed from its "Restates …" list). The four
    `authored_from_digest` values that the two statement edits invalidated were re-stamped with
    `detect_stale --stamp` after confirming both skill bodies already state the principles in the
    advisory voice they now carry.
  - **Not applied (verify2 NICE_TO_HAVE, non-gating, recorded so the next touch can pick them up):**
    P109's citation in `always_on[9]` stays — the paragraph restates P109 near-verbatim, and the rule is
    caution-preserving, so moving it would create a fresh orphan citation in `always_on[11]` (or cost
    body words to restate it there); and the weak-linkage citations P104 / P141 / P145 / P041, all
    graded no higher than `WITHIN_SCOPE` by the gate.
  - **Final body: 991 words** against the 1000-word `phase8 check 14` FAIL threshold (unchanged from
    1.3.0 — 1.3.1 reworded two clauses and dropped one citation at net zero words). Recorded
    retrospectively at 1.4.0: the 1.3.1 entry originally omitted it, breaking the per-entry convention
    every other version entry keeps (r1 finding F9).
  - No claim absent from `principles/principles.yaml` was introduced, no rule was strengthened, and no
    hedge or safety clause was dropped. Adapter re-exported from the profile.

- **1.3.0** (2026-07-27) — Independent re-verify round r1
  (`reports/review-loop/learning-science-advisor.r1.review.md`), must-fix = 3, all applied. This round
  closes the review → grounded fix → independent re-verify loop that 1.2.1 asserted `status: ready`
  before completing (r1 finding S2). Supersedes, and states what it supersedes:
  - **M1 — `reports/faithfulness-report.yaml` `forbidden_behaviours[5]` mislabel superseded.** The
    entry labelled `rule_ref: forbidden_behaviours[5]` reviewed the *law/accreditation* rule, which is
    index **6**; the report carried `[0..5]` and no `[6]`, so the real index 5 — the numeric/effect-size
    guardrail, the one rule that polices over-claim by invented precision — had zero faithfulness
    coverage. The entry is relabelled `forbidden_behaviours[6]`, a new `forbidden_behaviours[5]` entry
    grades the numeric guardrail `WITHIN_SCOPE` as an authored evidence guardrail, and the
    `handoff_rules[2]` note's cross-reference is corrected from `[5]` to `[6]`. No rule text changed;
    only the report's index labelling was wrong (this ledger's authored-fields table already
    distinguished [5] from [6] correctly).
  - **M2 — `source_of_truth_policy.canonical_owner` orphan status superseded.** This ledger's opening
    claimed every `source_of_truth_policy` value cites its promoted principle(s), with four documented
    authored exceptions; `canonical_owner` carried zero P-codes and was in neither set, so it was an
    orphan field value under `.claude/rules/rights-and-quotation-policy.md` and falsified this ledger's
    own completeness claim. Resolved by recording it as an authored scope boundary (fifth/sixth row of
    the table above) — the same jurisdictional statement as `handoff_rules[0]`–`[2]`, which are already
    listed. The field's text is unchanged; no principle was invented to cover it.
  - **M3 — missing enforceable mirror for `when_not_to_use[3]` superseded by new
    `forbidden_behaviours[7]`.** Every other routing exclusion had a mirrored forbidden behaviour
    (teaching-performed ↔ `[0]`, diagnosis/labelling ↔ `[1]`, placement/grading/admission/employment ↔
    `[2]`, law/accreditation ↔ `[6]`); the subject-matter exclusion had none, so the routing boundary
    existed but nothing forbade answering the subject-matter question once the advisor was invoked.
    Added as an authored scope boundary (appended at index 7, so indices 0–6 and every existing citation
    keep their numbering). Row added to the authored-fields table.
  - **Body-word trims to stay inside the profile body-size gate.** The body stood at 998 words against
    the 1000-word `phase8 check 14` FAIL threshold, so the new `forbidden_behaviours[7]` had to be paid
    for in the same pass (the 1.2.0/1.2.1 trimming precedent). Recovered by trimming wording only, never
    a citation, hedge, or boundary clause: `inputs.required` items 1–4 (phrasing only — ask-for-missing-
    context, Glob/Grep + root-relative resolution, and the never-cite-a-code-from-memory guardrail all
    retain their full operative content), `outputs.primary_format`, `minimum_useful_output`, the
    `advise` mode output, `quality_bar[6]`, `handoff_rules[0]`, and `precedence` (all "residual
    trade-off" → "trade-off" style edits). Final body: 991 words.
  - **S1 — stale justification on the `always_on[13]` faithfulness note superseded.** The note claimed
    P115's caveat was "compressed from 'an average age trend in speeded reasoning' to 'an average age
    trend'"; `profile.yaml` retains the `in speeded reasoning` qualifier verbatim. The `WITHIN_SCOPE`
    verdict is unchanged; the note now records that the qualifier is retained, so no future reviewer
    infers an accepted hedge-drop that does not exist.
  - **S4/S5/S6/S8 — all 15 `skills/*/SKILL.md` bodies re-authored** (re-authoring only; every
    frontmatter `provenance` block, including `authored_from_digest`, is byte-for-byte unchanged, and
    every principle citation survives attached to the same content). `## Purpose` cut from a ~1:1 prose
    restatement of `## Procedure` to a 1–3 sentence what/for-whom/at-what-grain statement; `## Procedure`
    regrouped from a flat principle-id-ordered checklist into 2–4 named `###` decision phases; the
    verbatim ×15 charter clause at the end of `## Output` replaced by a pointer to the profile's
    forbidden behaviours and handoff rules; and the two performing-voice steps (P029 in
    `feedback-assessment-and-error-correction`, P098 in `prior-knowledge-prediction-and-misconceptions`)
    reframed as advice to the instructor. No new claim was introduced in any body.
  - **S7 / N2 / N3 / N4 / N5 / N7.** `router_description` restructured to a short identity clause +
    exclusions + a trailing `Covers: …` list (same coverage, faster router matching); `role` now points
    at this ledger rather than the `sources` profile key, which the adapter body never renders;
    `evidence-appraisal-and-learning-myths`'s `description` now excludes the design detail of a
    technique that has its own skill in this package; the P045 trigger in
    `memory-mnemonics-and-recall-accuracy` is bound to a learning/assessment/debriefing context so it
    cannot fire on pure forensic interviewing; P141 in `motivation-belonging-and-classroom-climate`
    moved from the climate trigger to a structured-discussion trigger it actually grounds; and
    `always_on[13]`'s irregular line wrap reflowed.
  - **S3 remains open and unclosed.** The validator's `quote-scan` WARN ("rights NOT verified — 12
    restricted source(s), no source text available") persists: neither `sources/markdown/` nor a warm
    cache module is present in this worktree, so the verbatim-quote gate could not run. The standalone
    `quote_scan` over the package passes, so there is no evidence of a leak, but the rights gate is
    still unexercised and must be run once in an environment holding the source markdown before release.
  - No behavioural text was added, weakened, or strengthened, and no claim absent from
    `principles/principles.yaml` was introduced. Adapter re-exported from the profile.

- **1.2.1** (2026-07-27) — Adversarial verify gate (`reports/review-loop/learning-science-advisor.verify1.md`),
  must-fix = 3, all provenance-only. Supersedes, and states what it supersedes:
  - **`forbidden_behaviours[0]` citation `(P010, P077)` superseded by `(authored scope boundary)`.**
    Neither statement is about *who performs* teaching, delivery, authoring, or marking: P010 is
    mechanism-first translation of a principle into a local implementation, P077 is not treating one's
    own learning history as proof. The boundary text itself is unchanged and load-bearing; only the
    false grounding is removed, matching the honest convention already used by `forbidden_behaviours[5]`
    and `[6]`. The same two IDs remain correctly cited in the course-design `always_on` block.
  - **`forbidden_behaviours[2]` citation `(P128, P087)` superseded by `(authored scope boundary)`.**
    P128 governs *what to assess* (plural competence dimensions rather than one static score) and P087
    the *pacing* of expectations to demonstrated readiness; neither states an authority boundary on
    placement, grading, admission, promotion, or employment outcomes. Boundary text unchanged.
  - **`handoff_rules[0]` citation `(P010, P077)` superseded.** Ownership of curriculum, materials,
    delivery, and marks is tagged `(authored scope boundary)`; P010 is retained attached only to the
    clause it does support — the design reasoning is adapted through each principle's mechanism to the
    local learners, format, and institution. P077 dropped (silent on ownership).
  - **`handoff_rules[1]` citation `(P134, P128)` narrowed to `(P134)` + `(authored scope boundary)`.**
    P134 grounds the group-evidence half only ("use group categories for bounded population inference
    without converting them into individual capacity judgments"), which is now stated inline; it does not
    ground "belongs to a qualified specialist", and P128 grounds neither that nor "to the responsible
    body". Carried in the same pass as the two must-fix items above (verify1 ADVISORY).
  - **Body-word trims to stay inside the profile body-size gate.** At 1.2.0 the body stood at exactly
    1000 words — the `phase8 check 14` FAIL threshold — so the honest citation tags and the two retained
    grounding clauses (which are longer than the codes they replace) pushed it to 1011. Recovered by
    trimming wording only, never a citation, hedge, or boundary clause: `role` (source-type description
    dropped; the `sources` pointer and the "invariants are advisory criteria, not authority to act"
    disambiguation kept verbatim), `when_to_use[1]` ("hard but ineffective" → "ineffective"),
    `inputs.required` items 1–5 (phrasing only — the ask-for-missing-context rule, the Glob/Grep and
    root-relative resolution rules, and the never-cite-a-code-from-memory guardrail all retain their full
    operative content), `outputs.primary_format`, and the `advise` mode output. Final body: 998 words.
  - No behavioural text was added, weakened, or strengthened, and no claim absent from
    `principles/principles.yaml` was introduced — every remaining `P###` in these four rules resolves to
    a statement that carries the clause it is attached to. Adapter re-exported from the profile;
    `validate` PASSES with 0 FAIL (1 pre-existing WARN: quote-scan cannot run without source text in
    this worktree).

- **1.2.0** (2026-07-27) — Review round 2 (`/review-subagent`), must-fix = 0. Supersedes, and states
  what it supersedes:
  - **39 prefix-truncated `## Procedure` / anti-pattern lines across 14 of the 15 skills superseded**
    by the full `statement` from `principles/principles.yaml`. Every affected line was a strict
    character prefix of its principle, not a paraphrase — the skill-authoring step cut statements to a
    length budget and dropped the tail with no ellipsis and no severed parenthetical, so `validate`
    and the repo's truncation greps passed green on a corrupted body. Six sites were unparseable or
    lost the rule's operative scope: P122 ("…trigger scrutiny without **replacing judgment**"), P149
    ("…support that enables, **but does not perform**, the target skill"), P143 (which lost
    "**explicitly uncertain**" and so inverted the hedge into a claim of retained benefit), P078
    ("…the learner **must justify**"), P023 (which dropped "**examples, differential treatment, and
    cues that make a negative group stereotype salient**" — the mechanism the stereotype-threat
    remediation turns on), and P091 (which dropped "**unless independent error detection and repair
    are themselves the learning target, in which case delay the intervention**", leaving an
    unconditional instruction stronger than its source support). `profile.yaml` and both adapters
    already carried these statements in full, so the running system prompt was never affected. Only
    the prose changed; frontmatter `provenance` blocks including `authored_from_digest` are untouched.
  - **`## Worked example` added to all 15 skills.** Worked examples previously existed only in
    `profile.yaml.examples` (3, touching 3 skills), so ~12 skills carried no illustrated correct-usage
    scenario. Each new section is one scenario→correction paragraph citing **only** that skill's own
    `provenance.principles` (verified mechanically); no claim outside the skill's partition was
    introduced.
  - **`forbidden_behaviours[5]` added** (authored evidence guardrail): fabricated or ungrounded
    **numeric** claims were fenced only indirectly, via the over-claim item, which targets
    certainty and generality rather than invented precision — distinct failure modes, and the
    profile's own `examples[1]` models the citation of specific effect sizes.
  - **`inputs.required` extended by two items.** (a) Adapter sections that cite principle codes
    absent from the Operating-invariants block previously gave the model a bare code with no backing
    text while modelling the habit of precise citation; the agent must now read the statement in the
    matching skill file or the principles index before citing such a code. (b) The `Canonical package`
    pointers are rendered repository-root-relative while `Read` requires an absolute path, so under
    `export-deployable` or any non-root cwd the "read the matching skill file" instruction silently
    failed to resolve; the agent must now resolve them against the repository root or locate the file
    with Glob first.
  - **Skill `description` frontmatter disambiguated** for the overlapping pair
    `cognitive-load-worked-examples-and-scaffolding` ("…within a single lesson or task") and
    `expertise-development-and-transfer` ("…across a practice regime or course as expertise
    develops"). Both previously fired on "when do I fade scaffolds as expertise grows", and whichever
    loaded first set the frame.
  - **`role`, `when_to_use`, `when_not_to_use`, `outputs`, `modes`, `quality_bar`,
    `forbidden_behaviours`, `handoff_rules`, `source_of_truth_policy` compressed** to absorb the
    additions within the profile body budget. Prose only: every principle citation is retained, and
    `role`'s source enumeration was folded into the `sources` table it duplicated.
  - **`reports/faithfulness-report.yaml` corrected.** The notes on `knowledge_partition.always_on[0]`
    and `always_on[1]` quoted the profile as saying "uncorrected retrieval **reinforces** / **will
    reinforce** confident errors" and graded that as a minor flattening of P050. The profile text at
    both sites reads "**can** reinforce" and has since 1.1.0 — the verdicts were right but the cited
    evidence was stale, so the misquotes are superseded by notes recording that P050's hedge is
    carried through unchanged.
  - **Rights verification (`quote_scan` WARN).** `validate` warns that the verbatim-quote gate could
    not run: all 12 sources are `distillation-only` but the package ships no `sources/markdown/` and no
    warm cache module, so the `quote_scan` PASS is vacuous rather than evidence of compliance.
    Recorded here per `.claude/rules/rights-and-quotation-policy.md`: rights were verified at
    authoring time — every source was rights-classified `distillation-only` before distillation, and
    the authored layer paraphrases and restructures the distilled principle statements only, with no
    verbatim source passage reproduced in any generated artifact. Re-run `quote_scan` against a
    rehydrated markdown cache before any external release.
  - Unchanged: the distilled spine (150 principles, 5006 claims, evidence records, anchors), the
    skill→principle partition, both test suites, and the tool grant (Read/Grep/Glob).

- **1.1.0** (2026-07-27) — Review round 1 (`/review-subagent`), must-fix = 0. Supersedes, and states
  what it supersedes:
  - **Skill bodies.** The `## Anti-patterns to flag` section of all 15 skills was a machine-emitted
    "Overlooking Pxxx: <restated principle>" list, cut at a fixed character budget and closed with a
    bare period, and silently capped at 7 bullets (dropping ~half the principles in 9 skills). It is
    superseded by deliberately written failure modes, one per principle, 1:1 with `## Procedure`, no
    cap. Each skill also gains a `description:` frontmatter line so a caller's topic can be matched to
    it. Frontmatter `provenance` blocks (including `authored_from_digest`) are untouched — the
    grounding did not change, only its prose.
  - **Two truncated `## Procedure` steps repaired** from their own principle statements: P115 in
    `development-diversity-and-individual-differences` (step 2 ended "…and treating.") and P068 in
    `elaboration-examples-and-self-explanation` (step 5 ended "…and fading."). Same defect class as
    the anti-patterns; missed by the review's ellipsis-only truncation grep.
  - **`router_description`** superseded: `memory-mnemonics-and-recall-accuracy` is an `always_on`
    skill whose topic appeared nowhere in the routing surface, making a shipped capability
    unreachable. Mnemonic and memory systems and recall reliability are now named.
  - **`quality_bar[2]`** superseded: it stated distributed + interleaved practice unconditionally.
    P125 states distributed practice as a **high-utility default while preserving uncertainty for
    complex structured learning, higher-order outcomes, and moderators beyond age**, and
    `source_of_truth_policy.precedence` commits to carrying source hedging through — so the prior
    wording contradicted the profile's own policy. The hedge is restored. Two smaller hedge slips
    superseded on the same grounds: P050's "**can** reinforce confident errors" (flattened to
    "reinforces"/"will reinforce" in `always_on[0]`, `examples[0]` and the retrieval skill) and
    P115's "an average age trend **in speeded reasoning**" (compressed to "an average age trend" in
    `always_on[13]` and its skill).
  - **`quality_bar[6]`, `forbidden_behaviours[5]`, `handoff_rules[2]` added** — see the authored-field
    table above. `when_not_to_use[4]`'s legal/policy exclusion previously existed only at the routing
    layer, and the export template renders neither `outputs.primary_format` nor
    `minimum_useful_output`, so the deployed adapter carried no output floor.
  - **`inputs.required` extended** with the missing-context rule (ask for learners, target competence,
    and time rather than assuming defaults) and the Glob/Grep + skill-selection rule, which motivate
    the two tools the adapter grants.
  - **`role`, `when_to_use`, `when_not_to_use`, `outputs`, `modes` compressed** to absorb the
    additions within the profile body budget. No claim was dropped, only prose; the
    responsible-authority clause moved from `when_not_to_use[4]` into the new `handoff_rules[2]`.
  - **`reports/faithfulness-report.yaml` extended 29 → 50 findings.** The prior report asserted a
    complete pass it had not run: all 29 findings covered routing/scaffolding fields and **zero**
    covered `knowledge_partition.always_on[0..14]` or `examples[*].ideal_response` — the two
    highest over-claim-risk rule sets, carrying the effect sizes and myth refutations. All 18 are now
    graded, plus the three new authored fields; all 50 land `WITHIN_SCOPE`.
  - `multisource_synthesis: deferred` alongside `status: ready` is expected and not an omission: this
    package is a P0-authored layer over a pre-built map→reduce spine, whose cross-source clustering
    happened at reduce time, so `principles/principle-clusters.json` and `principle-graph.json` are
    deliberately absent.
  - Unchanged: the distilled spine (150 principles, 5006 claims, evidence records, anchors), the
    skill→principle partition, and both test suites.

- **1.0.0** (2026-07-26) — Initial LLM-authored layer over the pre-built distilled spine: profile
  (role, three modes, quality bar, forbidden behaviours, 15-skill / 2-reference
  knowledge partition), faithfulness report, 15 skills, 2 references, golden +
  principle-behaviour tests, and the exported Claude Code adapter. No prior profile decisions
  superseded.
