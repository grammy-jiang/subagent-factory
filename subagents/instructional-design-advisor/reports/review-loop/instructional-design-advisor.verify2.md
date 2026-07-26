# Adversarial verify — instructional-design-advisor (verify2)

Gate: Step 6 of `/review-subagent`, run against the just-converged package after the review loop
reported must-fix = 0. The loop's own verdict was **not** trusted: both checks below re-derived
their grades from the primary artifacts (`principles/principles.yaml`, the installed adapter),
not from the authored `reports/faithfulness-report.yaml` or from `verify1.md`.

Scope of edits by this gate: this file only. Nothing else was modified.

Reviewers run in parallel:

| Reviewer | Scope | Raw MUST_FIX |
|---|---|---|
| faithfulness-reviewer | every profile rule re-graded vs its cited principle | 2 |
| adapter safety/invariant check | invariant truncation, role contradiction, structural integrity | 0 |

Consolidated after adjudication: **1 must-fix**, 1 raw must-fix downgraded, 5 advisories.

---

## MUST-FIX 1 — HEDGING_REMOVED: worked example turns P067's degree-caution into a categorical bar

**Where**
- `profile.yaml:307-309` — `examples[0].ideal_response`
- Propagates verbatim to `.claude/agents/generated/instructional-design-advisor.md:277`

**Profile text**

> (3) A multiple-choice quiz **cannot show understanding** — a right answer can come from rote
> recall, test-taking skill, or a lucky guess (P067)…

**Cited principle P067** (`principles/principles.yaml:1386-1391`)

> Expect evidence of understanding to be **less direct and more complicated than** objective-test
> evidence, since a right answer can come from rote recall, test-taking skill, or a lucky guess,
> and therefore ferret out the reasons behind answers and the meaning the learner makes of results
> rather than the percentage correct.

**Derived grade: HEDGING_REMOVED.**

P067 is a *directness/complexity* caution with a prescribed remedy — objective-test evidence is
harder to read, so interrogate the reasoning behind the answers instead of the percentage correct.
It does not rule multiple-choice evidence out. The profile flattens this into an absolute
impossibility: "cannot show understanding". The second half of the profile sentence is a faithful
paraphrase of P067's *reason* clause, which is exactly what makes the overclaim readable as
sourced.

**Why must-fix rather than advisory.** Two aggravating factors that do not apply to the advisories
below:

1. This is an `ideal_response`, i.e. text that *models the exact phrasing the generated subagent
   should emit to a caller*. An over-strong claim here is not a citation-hygiene slip; it is a
   template for agent output.
2. It survives export unchanged into the installed adapter (`:277`), so it is live in the runtime
   artifact, not confined to the canonical package.

It is also the precise failure mode the evidence protocol names: a conditional/hedged source claim
rendered as an unconditional rule.

**Suggested repair** (not applied — this gate edits nothing): restore the source's strength, e.g.
"a multiple-choice quiz is weak evidence of understanding — a right answer can come from rote
recall, test-taking skill, or a lucky guess, so ferret out the reasoning behind the answer rather
than the percentage correct (P067)". This keeps the example's rhetorical force and the following
transfer-testing recommendation intact.

---

## DOWNGRADED — raw must-fix from faithfulness-reviewer, adjudicated to ADVISORY

### D1. P107 cited on `forbidden_behaviours[0]` (`profile.yaml:80-81`)

> Building the deliverable for the caller — the course, materials, or item bank produced end to
> end; the advisor supplies review criteria and the practitioner makes the teaching theory their
> own (P107).

P107 ("Make the teaching theory shaping the learning environment explicit, then use evidence and a
coherent framework to diagnose problems and adapt responses to local learners and constraints")
grounds the sentence's **second** clause, not the deliverable-building prohibition in the first.
The reviewer graded this SCOPE_BROADENED. Downgraded for two independent reasons:

1. **Direction of the claim.** Faithfulness bars a rule being *stronger* than its evidence — an
   agent asserting more about the world than the source supports. This rule is a self-restricting
   role boundary: it forbids the agent from acting. Under-claiming its own authority carries none
   of the risk the rule exists to prevent, and the prohibition itself is a factory-level boundary
   that no domain principle is expected to ground.
2. **Already adjudicated.** `verify1.md:124-125` examined this exact construction ("Compound
   sentence: the second clause is genuinely P107/P134. The citation sits at the end…") and accepted
   it, while stripping P107 from the sites where it was cited to ground an *ownership/authority*
   claim (`verify1.md:82-119`). Those strips were applied. Re-flagging the accepted half of that
   same decision is re-litigation, not a surviving defect.

Real but minor: a trailing citation on a compound sentence reads as covering the whole sentence.
Worth tightening on a future pass; not a gate blocker.

---

## ADVISORY (no action required to pass this gate)

### A1. Invariant compiler drops an operative second sentence on 6 of 75 rules

`compile_invariants._to_invariant()` renders only each principle's first sentence. For 69 of 75
rules the discarded tail is the terminal period. For 6, a second prescriptive sentence is lost:

| Adapter | Dropped sentence |
|---|---|
| `:158` P157 | "Prefer narration over concurrent onscreen text." |
| `:150` P153 | "Do not accept retention evidence alone as evidence that a design worked." |
| `:144` P122 | "A recommendation that names a technique without naming its situation is incomplete." |
| `:136` P092 | "Say which criterion is missing when only one holds." |
| `:156` P156 | "Reject delivery-device counting as a design frame." |
| `:26` P002 | "Each of the three scenarios has a different remedy." |

Not truncation in this gate's sense: every retained rule is a grammatically complete, self-
sufficient sentence — no mid-clause cut, no dangling conjunction, no unclosed paren, no `…`. This
is documented, deliberate behaviour (`compile_invariants.py:52-76`) and systemic across all
packages, not a defect of this package. Residual risk is real but small — P153's and P092's
dropped halves are the *enforcement* clause, surviving downstream only via the quality bar
(`:239`) and the skill bodies.

### A2. Invariants phrased in the domain's "do the teaching" imperative voice

e.g. `:80` P033 "Give students opportunities to rehearse…", `:88` P037 "Teach a concrete concept
by…", `:54` P018 "Write each standard on a rubric scale as…". Read literally these instruct the
agent to teach or to author. Contained, not a contradiction: three explicit precedence guards
override them — `:19` ("The invariants below are advisory criteria, not authority to act: this
advice-only boundary and the forbidden behaviours override every invariant"), `:23`, `:291` — plus
the failure-recovery worked example at `:280-284` that demonstrates declining exactly this.

### A3. `quality_bar[5]` (`profile.yaml:75-76`) — "evaluated for learning and workplace transfer"

Cites `(P148, P152, P140, P004)`; none of the four states workplace transfer (P140 covers
formative *draft* evaluation). The claim is true and grounded elsewhere in the profile
(`always_on` block 11, `forbidden_behaviours[1]`). Citation-precision gap, not an invented claim.

### A4. `forbidden_behaviours[3]` (`profile.yaml:87-88`) — P093 on "added interest as evidence"

P093 bars *adding* seductive details (a design instruction); the rule concerns *treating* added
interest as evidence learning occurred (an inferential fallacy). Adjacent theme, imprecise fit; a
fair reader can call it WITHIN_SCOPE.

### A5. Orphaned citation-list entries

`always_on` block 11 lists P041 (innovation persistence / constituency / cost-effective monitoring)
among its IDs with no sentence in the block reflecting it. `source_of_truth_policy.precedence`
(`profile.yaml:112-117`) cites only P193 for a clause also covering teacher-of-record and
institutional grade ownership (grounded elsewhere, e.g. P021, but not re-cited here). Nothing is
wrongly attributed in either case — list hygiene only.

---

## Clean — checked and confirmed sound

- **Adapter structural integrity.** `GENERATED FILE. DO NOT EDIT DIRECTLY.` marker at line 8
  (within first 20). No whole-file truncation — ends at line 330/331 on a complete bullet with a
  trailing newline. No duplicate headings or invariant lines. Only non-ASCII chars are 68
  em-dashes; no mojibake. Frontmatter parses.
- **Invariant layer intact.** 75 must-hold principles compiled, 75 rendered — 0 missing, 0 extra,
  0 text mismatch. `attach_invariants` is on and the layer is not stale. Zero lines with `…`/`...`,
  unbalanced parens or quotes, or a trailing conjunction / preposition / `(e.g`.
- **Advice-only role holds.** Every occurrence of certify / accredit / grade / score in the adapter
  (`:3`, `:197`, `:251`, `:280`, `:284`, `:289`) is a **negation**, never an instruction to do it.
- **No authority escalation.** `tools: Read, Grep, Glob` — read-only; no Edit/Write/Bash, no patch
  policy, no permission-widening or escalation language.
- **Citation resolution.** All 22 non-invariant principle IDs resolve in
  `references/instructional-design-principles-index.md`. No profile citation anywhere names a
  nonexistent P-number.
- **Artifact consistency.** Installed adapter is byte-identical to
  `subagents/instructional-design-advisor/adapters/claude-code/instructional-design-advisor.md`;
  all 15 package pointer paths in the adapter exist on disk;
  `validate_generated_package` exits 0 (adapter-quality passed, 13/13 skills authored).

## Coverage

- **Faithfulness:** all 6 `quality_bar`, all 6 `forbidden_behaviours`, both `handoff_rules`, all 3
  `source_of_truth_policy` sub-fields, all 13 `always_on` blocks (covering all 200 principle IDs
  via block membership), both worked `examples` and every inline citation therein. `role`,
  `router_description`, `when_to_use` / `when_not_to_use`, `inputs` / `outputs` / `modes` carry no
  citations and were checked for consistency only, not graded.
- **Adapter:** all 330 lines — frontmatter, Role, all 75 operating invariants, When to use, When
  NOT to use, Required inputs, all 3 modes, Quality bar, Forbidden behaviours, Handoff rules, both
  worked examples, Source of truth policy, Canonical package.
- **Not rendered by the adapter template** (verified systemic, not a per-package drop, against
  `templates/claude-agent-adapter.md.j2`): `outputs.primary_format`, `minimum_useful_output`,
  `knowledge_partition.always_on`. The `always_on` content stays reachable via the 13 `skills/*/
  SKILL.md` pointers at `:301-325`, all of which exist.

MUST_FIX_COUNT: 1
