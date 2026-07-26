# learning-science-advisor — review round 1

Package: `subagents/learning-science-advisor/` (v1.0.0, tier 2, status `ready`)
Mode: review only — no files changed except this report.

## Deterministic gates

| Gate | Result |
|------|--------|
| `validate_generated_package` | **PASSED** — 0 FAIL, 1 WARN |
| `quote_scan` | **PASS** — no potential verbatim quotation found |
| ellipsis truncation grep (`…`) in skills + adapter | no hits |
| severed-parenthetical grep in adapter invariants | no hits |

The one validator WARN (`quote-scan: rights NOT verified — 12 restricted source(s) but no source
text available`) is recorded below as should-fix, not must-fix: the standalone `quote_scan`
run passed and the WARN reports an un-runnable gate (no `sources/markdown/`, no warm cache
module), not a detected violation.

Note on the truncation gate: it detects `…` only. Finding 1 below is a real silent truncation
that the gate cannot see because the severed clauses are closed with a bare period.

---

## Findings

### MUST-FIX

#### 1. Every `## Anti-patterns to flag` bullet in all 15 skills is truncated mid-clause

- **Where:** all 15 of `subagents/learning-science-advisor/skills/*/SKILL.md`, `## Anti-patterns to flag` section
  (e.g. `retrieval-practice-and-low-stakes-quizzing/SKILL.md:88`)
- **Severity:** must-fix *(panel rated should-fix; elevated — this is exactly the
  "silently-truncated skill body" class the STEP 1 gate defines as must-fix, missed only
  because the cut is closed with a period rather than an ellipsis)*
- **Problem:** Each bullet restates a principle but is cut at a fixed character budget and
  closed with a bare period, producing a grammatically broken clause. Verified samples from
  `retrieval-practice-and-low-stakes-quizzing`:
  - P059 — "…successful retrieval strengthens later access directly and can improve." (source
    sentence at `## Procedure` step 6 continues "…organization and subsequent encoding.")
  - P060 — "…when learners can produce meaningful answers, while allowing."

  Other files show the same shape ("…that must.", "…rather than treating memory.", "…while
  respecting biological."). 15/15 files affected. The agent reads these bullets as its
  failure-mode checklist, so it is loading a checklist of half-sentences.
- **Fix:** Complete each bullet from the matching `## Procedure` step (the full clause already
  exists verbatim in the same file), or replace the section with one deliberately-written
  one-line anti-pattern per principle. Then re-run the truncation grep with a broadened
  pattern that also catches clause-final `and|while|that|because|rather than` before `.`.

#### 2. `router_description` omits an entire always_on skill domain (memory / mnemonics / recall accuracy)

- **Where:** `subagents/learning-science-advisor/profile.yaml:8-16` (`router_description`) vs
  `:340` (skill `memory-mnemonics-and-recall-accuracy`)
- **Severity:** must-fix
- **Problem:** 14 of the 15 `knowledge_partition.always_on` topics appear in
  `router_description`; `memory-mnemonics-and-recall-accuracy` appears nowhere.
  Verified: `grep -ciE 'mnemonic|memory|recall accuracy'` over the router_description block
  returns 0. A caller asking "how do I build a mnemonic/memory-palace system for my students"
  or "how far can I trust this student's recollection" will not match the routing signal, even
  though a dedicated always_on skill exists for exactly that. The router description is the
  only routing surface — an unlisted capability is an unreachable capability.
- **Fix:** Add the topic to `router_description`, e.g. "…mnemonic systems and recall
  reliability, and appraising a claimed technique or learning myth against its evidence…".
  Bump `agent_version`, add a CHANGELOG entry, re-run `cli export`, re-validate.

#### 3. `faithfulness-report.yaml` never reviewed the profile's substantive behavioural content

- **Where:** `subagents/learning-science-advisor/reports/faithfulness-report.yaml`
- **Severity:** must-fix
- **Problem:** The report holds 29 findings. Verified by `rule_ref` census — all 29 are
  routing/scaffolding fields (`quality_bar[0..5]`, `forbidden_behaviours[0..4]`,
  `when_to_use[0..4]`, `when_not_to_use[0..4]`, `handoff_rules[0..1]`, `outputs.*`,
  `source_of_truth_policy.precedence`, `minimum_useful_output`). **Zero** findings cover:
  - `knowledge_partition.always_on[0..14]` — the 15 paragraph blocks at `profile.yaml:119-327`
    that carry the actual technique-level claims (effect sizes, myth refutations, conditioned
    retrieval/spacing/interleaving guidance);
  - `examples[0..2].ideal_response` — including the example stating P103's specific effect
    sizes ("around 0.18, 0.09 and 0.18 respectively") and the learning-styles refutation.

  These are the *highest* over-claim-risk rule sets in a learning-science profile and they were
  skipped entirely. As written the report asserts a complete faithfulness pass it did not run.
  (A manual substitute audit of the always_on blocks against `principles.yaml` found them
  largely faithful, with the one exception at finding 4 — so this is a false-assurance defect,
  not evidence of widespread over-claim.)
- **Fix:** Extend the report with one finding per `knowledge_partition.always_on[i]` and per
  `examples[i].ideal_response`, scored on the five-level scale.

---

### SHOULD-FIX

#### 4. `quality_bar[2]` drops a hedge the profile's own precedence policy commits to carrying

- **Where:** `profile.yaml:78-79`
- **Claim strength:** HEDGING_REMOVED
- **Problem:** The rule states distributed + interleaved practice unconditionally. P125 states
  it as a "**high-utility default** … **while preserving uncertainty for complex structured
  learning, higher-order outcomes, and moderators beyond age**." The sibling
  `always_on[1]` block (`:131-132`) *does* retain the hedge, and
  `source_of_truth_policy.precedence` (`:114-116`) explicitly commits to carrying source
  hedging through (P143, P125, P105). So the profile contradicts itself. The existing report
  scored `quality_bar[2]` WITHIN_SCOPE and missed this.
- **Fix (supported wording):** "Practice is distributed rather than massed **as a high-utility
  default**, with the gap set against the retention horizon, and interleaved when learners must
  discriminate categories or select strategies — **except where complex structured learning or
  higher-order outcomes leave the benefit uncertain** (P125, P061, P142, P028)."

#### 5. Anti-pattern bullets silently capped at 7, dropping ~half the principles in 9 skills

- **Where:** 9 of 15 `skills/*/SKILL.md`
- **Problem:** Verified counts (anti-patterns / principles in Procedure): retrieval 7/13,
  spacing 7/13, metacognition 7/13, course-design 7/13, motivation 7/14, evidence-appraisal
  7/14, cognitive-load 7/12, expertise 7/11, elaboration 7/10, prior-knowledge 7/8. Skills with
  ≤7 principles get 1:1 coverage. The cut is by principle-id order, not importance — it is a
  generation artifact, and the dropped principles are arbitrary relative to risk.
- **Fix:** Emit one anti-pattern per principle (matching Procedure 1:1, as the small skills
  already do), or make the cap deliberate and importance-ranked and state it in the section.

#### 6. Adapter never renders `outputs.primary_format` or `minimum_useful_output`

- **Where:** `.claude/agents/generated/learning-science-advisor.md` (absent) vs
  `profile.yaml:52-55, 88-89`
- **Problem:** Verified — `grep -c 'never a bare verdict'` and
  `grep -c 'At least one finding that names'` both return 0 in the adapter. The deployed system
  prompt therefore carries no output-format floor and no minimum-useful-output rule. Note
  `adapter-fresh` passes, so this is a **renderer gap**, not hand-edit drift — fixing it
  requires a template change, not an adapter edit.
- **Fix:** Render `primary_format` as the intro line under "## Supported modes and outputs" and
  `minimum_useful_output` there or folded into "Quality bar", in the export template.

#### 7. `forbidden_behaviours` / `handoff_rules` do not mirror the legal/policy exclusion

- **Where:** `profile.yaml:46-47` (`when_not_to_use[4]`) vs `:90-100`, `:101-105`
- **Problem:** `when_not_to_use[4]` excludes "a binding ruling on education law, accreditation,
  safeguarding, or institutional policy". The other four exclusions each have a parallel
  forbidden-behaviour or handoff-rule; this one has neither, so the boundary exists only at the
  routing layer with nothing reinforcing it in the guardrail fields that drive skill authoring.
- **Fix:** Add a matching `forbidden_behaviours` entry plus a `handoff_rules` entry naming the
  responsible authority; cite grounding principles or mark it a scope-only boundary.

#### 8. `minimum_useful_output` is an uncited load-bearing rule outside the ledger's carve-out

- **Where:** `profile.yaml:88-89` vs `provenance-ledger.md:6-10`
- **Problem:** The ledger claims every `quality_bar` / `forbidden_behaviours` / `handoff_rules`
  / `always_on` / `source_of_truth_policy` value cites its principle, and carves out `role`,
  `when_to_use`, `inputs`, `outputs` as untagged by convention. `minimum_useful_output` is in
  neither list yet prescribes a normative rule with no citation — a real gap in the ledger's
  own completeness statement.
- **Fix:** Either add it to the ledger's carve-out list (if it's a format rule) or cite its
  grounding principle inline.

#### 9. Grep/Glob granted but never motivated; no missing-context or skill-selection rule

- **Where:** `.claude/agents/generated/learning-science-advisor.md` frontmatter line 4, and
  body `:162-166` ("Required inputs"), `:266-292` (skill list)
- **Problem:** Three related operating-instruction gaps. (a) Grep and Glob are granted but
  nothing in the body ties them to a behaviour — dead capability. (b) "Required inputs" lists
  learners / target competence / time available but never says what to do when the caller omits
  them, so the missing-context path is unspecified. (c) 15 skill files are listed "for deeper
  context" with no rule for matching a caller's topic to the right one.
- **Fix:** Add three lines — use Glob/Grep to enumerate and locate passages when the caller
  points at a course or lesson file; ask for learners/competence/time before recommending
  rather than assuming defaults; match the caller's topic to the corresponding skill file and
  read that one.

#### 10. Verbatim-quote gate could not run (validator WARN)

- **Where:** `subagents/learning-science-advisor/` — no `sources/markdown/`, no warm cache module
- **Problem:** 12 of 12 sources are `distillation-only`, i.e. no verbatim quotation is permitted
  anywhere, and that is precisely the gate that could not execute. The standalone `quote_scan`
  passed, which is real but weaker evidence than a source-text-backed check.
- **Fix:** Warm the MAP cache module (or restore `sources/markdown/`) and re-run validate so
  the rights gate executes against source text before release.

---

### NICE

#### 11. `P039` cited in `evidence-appraisal-and-learning-myths` but owned by another skill
`skills/evidence-appraisal-and-learning-myths/SKILL.md:54` cites `(P033, P039, P105)`, but
P039 is in `expertise-development-and-transfer`'s provenance set (verified: P039 appears in
both files). Internal citation only, not user-facing. Correct so trigger bullets cite only the
skill's own principle set.

#### 12. `when_to_use[0..1]` reuses the verb "diagnosing" that marks the forbidden case
`profile.yaml:29-30` — "Diagnosing why learning is not sticking" (in scope) vs "diagnosing a
learner" (forbidden). The substantive distinction is correct and well-illustrated by the worked
example at `:384-400`, but the shared verb adds routing friction. Consider "Investigating why
learning is not sticking".

#### 13. `multisource_synthesis: deferred` alongside `status: ready` is unexplained
`profile.yaml:5-7`; no ledger note. Expected for a P0-authored-layer build, but the Version
History should say so in one line rather than leave it to inference.

#### 14. Frontmatter `description` and body `## Role` restate the same scope near-verbatim
`.claude/agents/generated/learning-science-advisor.md:3` vs `:17-19` — token-inefficient
duplication at the top of the system prompt. Trim `## Role` to what the description doesn't
already carry (audience, source list, invariant-precedence note).

#### 15. `P092` / `P098` cited as backing while flagged `profile_rule: false`
P092 is cited in `always_on[0]`, P098 in `always_on[4]`; both are `operational_mapping.
profile_rule: false` in `principles.yaml`. The wording does not exceed what they state, so this
is not over-claim — but the flag conflicts with their use as cited backing. Check whether the
flag is stale or the citation is decorative.

#### 16. Effect sizes P103 (0.18/0.09/0.18) and P084 (d=0.19) not re-verified against source
The profile is faithful *to the principle as written* (figures match verbatim). Whether the
principle itself preserved the source's moderators and sample context was out of this pass's
scope. Worth a targeted spot-check against source text, since "effect size stated without
moderators" is the highest-risk domain trap in this profile.

---

## Panel

| Lens | Reviewer | Must-fix |
|------|----------|----------|
| Deterministic gates | validate + quote_scan + truncation greps | 0 |
| Skill authoring quality | `agent-skills-advisor` | 0 (1 elevated here → finding 1) |
| Profile release-readiness | `profile-reviewer` | 1 |
| Faithfulness / over-claim | `faithfulness-reviewer` | 1 |
| Agent design | `ai-agent-engineering-reviewer` | 0 |

No cross-lens duplicates required merging; findings 1, 2 and 3 come from distinct lenses and do
not overlap. All three must-fix claims were independently re-verified by direct file inspection
before consolidation.

MUST_FIX_COUNT: 3
