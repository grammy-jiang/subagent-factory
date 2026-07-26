# Review — learning-science-advisor (round 2)

Date: 2026-07-27
Package: `subagents/learning-science-advisor/`
Mode: REVIEW ONLY (no fixes applied)

## Deterministic gates

| Gate | Result |
|------|--------|
| `validate_generated_package` | **PASSED** (0 FAIL, 1 WARN) |
| `quote_scan` | **PASS** — no potential verbatim quotation |
| ellipsis truncation grep (`…`) | clean |
| severed-parenthetical grep (adapter invariants) | clean |

WARN (not a FAIL, carried as should-fix S-4 below):
`quote-scan: rights NOT verified — 12 restricted source(s) but no source text available (no sources/markdown/, no warm cache module); verbatim-quote gate could not run`

## Reviewer panel

| Lens | Agent | must-fix |
|------|-------|----------|
| Skill-authoring quality | agent-skills-advisor | 1 |
| Profile release-readiness | profile-reviewer | 0 |
| Faithfulness / over-claim | faithfulness-reviewer | 0 |
| Agent design (adapter) | ai-agent-engineering-reviewer | 0 |

The panel's single must-fix (P122) was independently confirmed and then generalised by a
systematic sweep comparing every `## Procedure` / anti-pattern line against its principle's
`statement` in `principles/principles.yaml`. That sweep found **39 prefix-truncated lines across
14 of the 15 skills** — the panel finding was one instance of a systemic defect. Six of the 39
sites are must-fix (unparseable, or the truncation strips the rule's scope condition); the rest
lose mechanism detail but still parse.

**Scope note:** the truncation is confined to `skills/*/SKILL.md`. `profile.yaml` and both
adapters carry the full principle statements (verified: adapter lines 44, 126 render P023 and
P143 complete), so the running system prompt is unaffected — only the on-demand skill bodies the
agent Reads for topic depth are corrupted.

---

## Findings

### MUST-FIX

**M-1 — `skills/expertise-development-and-transfer/SKILL.md:67` | must-fix**
*Problem:* Procedure step 9 is severed mid-clause and does not parse: `"… using varied
comparisons and heuristics that trigger scrutiny without (P122)."` P122 ends `"… that trigger
scrutiny without **replacing judgment**."`
*Fix:* restore the trailing `replacing judgment`.

**M-2 — `skills/cognitive-load-worked-examples-and-scaffolding/SKILL.md:69` | must-fix**
*Problem:* Procedure step 12 severed on a transitive verb with no object: `"… and use support
that enables (P149)."` P149 reads `"… use support that enables, **but does not perform**, the
target skill."` Beyond being unparseable, the lost clause is the operative scaffolding
constraint (support must not do the work for the learner) — the step as written is an
instruction to add support with no limit.
*Fix:* restore `, but does not perform, the target skill`.

**M-3 — `skills/elaboration-examples-and-self-explanation/SKILL.md:66` | must-fix**
*Problem:* Procedure step 9 severed at `"… while keeping far transfer, durability, classroom
generality, and learner moderators (P143)."` The lost words are `**explicitly uncertain**`.
This does not merely truncate — it inverts the hedge: "keeping far transfer, durability …" reads
as *retain these benefits*, the opposite of P143's "hold these outcomes as uncertain". The
adapter renders P143 correctly (line 126); the skill body contradicts it.
*Fix:* restore `explicitly uncertain`.

**M-4 — `skills/prior-knowledge-prediction-and-misconceptions/SKILL.md:60` | must-fix**
*Problem:* Procedure step 5 severed mid-relative-clause and does not parse: `"… and then
constructing a more adequate alternative the learner (P078)."` P078 ends `"… the learner **must
justify**."`
*Fix:* restore `must justify`.

**M-5 — `skills/motivation-belonging-and-classroom-climate/SKILL.md:63` | must-fix**
*Problem:* Procedure step 2 severed mid-enumeration: `"… and reduce it by auditing task framing,
assumptions (P023)."` P023 continues `", **examples, differential treatment, and cues that make a
negative group stereotype salient**."` The truncation drops the operative item — the salience
cue is the mechanism the whole stereotype-threat remediation turns on, so the step names a
remedy that omits its own active ingredient. The adapter renders P023 in full (line 44).
*Fix:* restore the full enumeration.

**M-6 — `skills/feedback-assessment-and-error-correction/SKILL.md:60` | must-fix**
*Problem:* Procedure step 6 parses, but the truncation removes P091's exception clause: `" —
**unless independent error detection and repair are themselves the learning target, in which
case delay the intervention**."` What remains is an unconditional instruction to interrupt error
early — stronger than its source support, and wrong exactly when self-correction is the
objective. Same class as a profile-level HEDGING_REMOVED finding, applied to a skill body.
*Fix:* restore the `unless …` exception.

---

### SHOULD-FIX

**S-1 — `skills/*/SKILL.md` (39 sites, 14 of 15 skills) | should-fix — ROOT CAUSE of M-1…M-6**
*Problem:* Every affected Procedure/anti-pattern line is a **strict character prefix** of its
principle's `statement`, not a rewritten summary. That signature says the skill-authoring step
truncated statements to a length budget and dropped the tail silently, rather than
paraphrasing. The repo's existing truncation gates do not catch this class: it emits no `…` and
no severed parenthetical, so `validate` and both greps pass green on a corrupted body.
Sites (file:line — principle):

- cognitive-load-worked-examples-and-scaffolding: 60 P021, 61 P047, 62 P063, 67 P121, **69 P149**
- collaborative-and-peer-learning: 55 P095, 56 P097
- course-design-technology-and-online-teaching: 63 P052, 64 P056, 65 P062, 66 P077, 71 P102
- development-diversity-and-individual-differences: 53 P087, 58 P146
- elaboration-examples-and-self-explanation: **66 P143**
- evidence-appraisal-and-learning-myths: 70 P084, 71 P103
- expertise-development-and-transfer: 60 P009, 63 P100, **67 P122**
- feedback-assessment-and-error-correction: 55 P029, **60 P091**
- interleaving-variation-and-discrimination: 56 P035, 57 P064
- metacognition-study-habits-and-self-regulation: 66 P049, 68 P076, 70 P090
- motivation-belonging-and-classroom-climate: **63 P023**, 64 P037, 74 P140
- prior-knowledge-prediction-and-misconceptions: 59 P043, **60 P078**, 62 P114
- retrieval-practice-and-low-stakes-quizzing: 64 P050, 69 P092, 72 P135
- spacing-distributed-practice-and-consolidation: 62 P024, 67 P093, 69 P118

(bold = the six must-fix sites; `memory-mnemonics-and-recall-accuracy` is the only clean skill.)
*Fix:* re-render all 39 lines from the full `statement` in `principles/principles.yaml`. Then add
a prefix-truncation check to the validator — for each `(Pxxx)`-tagged skill line, FAIL if the
line text is a strict prefix of the principle statement — so this class cannot pass green again.

**S-2 — `skills/*/SKILL.md`, ~12 Procedure steps | should-fix**
*Problem:* A subset of S-1's truncations collapse the step to a bare restatement of the
principle's title, so the section that is supposed to be the operational core carries less
"how" than the anti-pattern bullet for the same principle. Examples: `spacing…:69` "Schedule
retrieval adaptively (P118)"; `evidence-appraisal…:71` "Reject modality matching (P103)";
`collaborative…:55` "Impose structure on peer learning (P095)"; `metacognition…:66` "Make
otherwise invisible reasoning inspectable (P049)"; `course-design…:63` "Apply universal design
as the default framework (P052)"; also `retrieval…:72` (P135), `prior-knowledge…:62` (P114),
`motivation…:64` (P037), `feedback…:55` (P029), `expertise…:60` (P009), `interleaving…:56`
(P035), `cognitive-load…:61` (P047).
*Fix:* subsumed by S-1 — restoring the full statement restores the mechanism in place.

**S-3 — `skills/cognitive-load-worked-examples-and-scaffolding/SKILL.md:62` (P063) | should-fix**
*Problem:* Truncation drops P063's refutation `", but do not assume domain-specific memory-span
training will improve learning generally"`. The step now reads as unqualified endorsement of
chunking-plus-memory-training, and the skill loses a myth-refutation it is supposed to carry.
*Fix:* restore the clause (subsumed by S-1).

**S-4 — `reports/` / package rights verification | should-fix**
*Problem:* `validate` WARNs that the verbatim-quote gate could not run — 12 `distillation-only`
sources but no `sources/markdown/` and no warm cache module. The `quote_scan` PASS is therefore
vacuous, not evidence of compliance, for a package where all 12 sources forbid verbatim
quotation.
*Fix:* re-run the gate with source text present (rehydrate the markdown cache) before release,
or record an explicit provenance-ledger note that rights were verified at authoring time.

**S-5 — `.claude/agents/generated/learning-science-advisor.md` (Quality bar / Forbidden
behaviours / Handoff rules / examples: lines 197, 199, 201, 203, 205, 207, 215, 219, 221, 223,
231, 233, 245, 259, 266) | should-fix**
*Problem:* These load-bearing sections cite principle codes (P013, P126, P107, P028, P067, P047,
P136, P033, P140, P070, P099, P010, P077, P128, P105, P039, P135, P046, P090, P041) whose
statements are never rendered inline in the adapter's Operating-invariants block. A model reading
only the running prompt sees a bare code with no backing text, while the surrounding text models
the habit of citing precise codes — an invitation to fabricate or misattribute.
*Fix:* add an explicit instruction near "Required inputs" — before citing a P-code absent from
Operating invariants, Read the matching skill file or `learning-science-principles-index` to
confirm its text — or drop precise codes from those sections and keep traceability in the ledger.

**S-6 — `.claude/agents/generated/learning-science-advisor.md:169`, `:268–309` | should-fix**
*Problem:* Line 169 tells the agent to Read the matching skill file, but the "Canonical package"
pointers are **repo-relative** paths while Read requires an absolute path. Under
`export-deployable` (package installed standalone into another repo) or any non-root cwd, the
instruction silently fails to resolve.
*Fix:* render the pointers as absolute paths at export time, or state the root they resolve
against and require the agent to join before calling Read.

**S-7 — `profile.yaml:92-104` (`forbidden_behaviours`) | should-fix**
*Problem:* No item explicitly fences fabricated or ungrounded **numeric** claims. Coverage is
only indirect via item [3] ("Stating a rule more strongly than its source supports"), which
targets certainty/generality, not invented precision — distinct failure modes. The profile's own
`examples[1]` cites d≈0.18/0.09/0.18, modelling the citation of specific effect sizes.
*Fix:* add e.g. "Citing or inventing a specific effect size, statistic, or numeric benchmark not
directly grounded in the source of the invoked principle."

**S-8 — `reports/faithfulness-report.yaml` (~lines 268-270, ~418-421) | should-fix**
*Problem:* Two notes misquote the profile they grade. The note on
`knowledge_partition.always_on[0]` quotes "uncorrected retrieval **reinforces** confident errors"
and the note on `examples[0].ideal_response` quotes "**will reinforce**"; the actual profile text
(`profile.yaml:130-132` and `:368`) reads "**can reinforce**" in both places — already hedged,
matching P050. The `WITHIN_SCOPE` verdicts happen to be right, but the cited evidence is stale.
*Fix:* correct the quoted wording, or drop the two "minor observation" notes.

**S-9 — skill trigger overlap: `cognitive-load-worked-examples-and-scaffolding` vs
`expertise-development-and-transfer` (frontmatter `description`) | should-fix**
*Problem:* Both descriptions fire on "when do I stop giving worked examples / fade scaffolds as
expertise grows" (P067/P101/P112 vs P009). Whichever loads determines the frame — within-lesson
working-memory management vs longitudinal practice-regime design.
*Fix:* add a disambiguating clause to each description: cognitive-load "…within a single lesson
or task"; expertise-development "…across a practice regime or course as expertise develops".

**S-10 — `skills/*/SKILL.md` (all 15) | should-fix**
*Problem:* No skill carries its own worked example. The only worked examples live in
`profile.yaml.examples` (3 of them), touching topics in 3 skills; the other ~12 skills have no
illustrated correct-usage scenario anywhere in their own file.
*Fix:* add one short scenario→correction paragraph per skill, in the style already used at
profile level.

---

### NICE

**N-1 — `skills/evidence-appraisal-and-learning-myths/SKILL.md:62, 66, 71` | nice**
Steps for P011, P044 and P103 all land on "don't match instruction to a stated modality/style
preference". Each is individually grounded and distinct (categorization claim vs
preference-vs-outcome distinction vs effect sizes), but three near-identical-sounding lines in a
14-item list read as padding. Consider merging into two steps that each state their distinct
empirical content.

**N-2 — `.claude/agents/generated/learning-science-advisor.md:21–132` (Operating invariants) | nice**
~55–60 full principle statements (>100 lines) are inlined on every invocation before any
task-specific section. Consider keeping only cross-cutting and safety-critical principles inline
and routing the rest through the on-demand skill-file Read already specified at line 169.

**N-3 — `profile.yaml:8-17` / adapter frontmatter `description` | nice**
`router_description` is one dense ~180-word run-on enumerating all 15 subtopics plus exclusions.
Substantively correct (no vagueness, no cross-routing to a sibling subagent — the "advisors work
alone" rule is respected), but hard to scan for a routing decision. Light segmentation if it is
revised for other reasons.

**N-4 — `provenance-ledger.md:9-10` | nice**
The descriptive-field citation exemption (`role`, `when_to_use`, `inputs`, `outputs`,
`minimum_useful_output` carry no inline tags) is re-justified per package because
`.claude/rules/rights-and-quotation-policy.md` does not carve it out. Fold the convention into
the repo-level policy doc once instead of restating it in each ledger.

**N-5 — `skills/spacing-distributed-practice-and-consolidation/SKILL.md:67` (P093),
`skills/retrieval-practice-and-low-stakes-quizzing/SKILL.md:69` (P092),
`skills/cognitive-load-worked-examples-and-scaffolding/SKILL.md:60` (P021) | nice**
Three S-1 truncations that still parse but shift meaning: P093 loses "needs when it becomes
unwieldy" (so "future performance" replaces "future performance needs" and the trigger condition
vanishes); P092 loses "they reveal"; P021 loses "or harm". Subsumed by S-1's re-render.

---

## Verified clean (no findings)

- Tool grant is exactly Read/Grep/Glob; nothing in the adapter body implies write, edit, execute,
  or fetch authority.
- `when_not_to_use` names no sibling subagent — the standing "generated subagents work alone"
  rule is respected in both profile and adapter.
- `forbidden_behaviours`, `quality_bar` and `when_not_to_use` all survived into the adapter
  essentially verbatim; `adapter-sync` and `adapter-fresh` both green.
- Faithfulness: no profile rule at SCOPE_BROADENED or worse. Hedges on P125, P143, P050, P011,
  P044, P074, P021, P134 all carried through at source strength; effect sizes in `examples[1]`
  match P103 exactly.
- `agent_version: 1.1.0` matches the ledger's latest Version History entry; all 12 sources carry
  `rights_status: distillation-only` (none `unknown`); no TODO/placeholder/empty fields.
- `knowledge_partition.always_on` citations sum to 150 across 15 skills with 1:1 skill ownership.
- Each skill's Procedure and Anti-patterns sections are in 1:1 correspondence with its frontmatter
  `provenance.principles` — no dropped or orphaned principle in any of the 15 files.

MUST_FIX_COUNT: 6
