# Provenance Ledger — learning-science-advisor

Canonical record of what grounds this subagent. The profile, skills, references, faithfulness
report, and tests are all derived from the distilled spine in this package
(`principles/principles.yaml` -> `analysis/claims.jsonl` -> `evidence/evidence-records.yaml` ->
`sources/anchors/*.anchors.jsonl`), assembled by the map->reduce build. No load-bearing profile rule
field is an orphan: every `quality_bar`, `forbidden_behaviours`, `handoff_rules`,
`knowledge_partition.always_on`, and `source_of_truth_policy` value cites the promoted principle(s)
it restates. (Descriptive fields — `role`, `when_to_use`, `inputs`, `outputs`, and
`minimum_useful_output` — carry no inline tags, per repo convention.)

Three fields are **authored**, not distilled, and say so inline rather than citing a principle they
do not have:

| Field | Kind | Why it carries no principle |
|-------|------|------------------------------|
| `quality_bar[6]` ("Output floor") | authored output floor | Restates `outputs.primary_format` + `minimum_useful_output` so the export template, which renders neither, still carries the output floor into the deployed adapter. It is a format rule, not a domain claim. |
| `forbidden_behaviours[5]` | authored scope boundary | Mirrors `when_not_to_use[4]`. No source principle grants or withholds authority over education law, accreditation, safeguarding, or institutional policy; the boundary is a repo-policy decision. |
| `handoff_rules[2]` | authored scope boundary | The named-authority half of the same boundary. |

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
