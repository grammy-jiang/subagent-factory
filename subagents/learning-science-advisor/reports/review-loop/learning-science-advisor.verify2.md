# Adversarial verify #2 — learning-science-advisor

Gate: Step 6 of `/review-subagent`, run **after** the loop reported must-fix=0. The prior
convergence signal was not trusted; both lanes re-derived from source.

- **Lane A — faithfulness**: every `P###`-cited rule in `profile.yaml` re-graded against
  `principles/principles.yaml` (authored grades in `reports/faithfulness-report.yaml` and
  `provenance-ledger.md` deliberately not read).
- **Lane B — safety / adapter**: `.claude/agents/generated/learning-science-advisor.md`
  invariant layer, role consistency, adapter↔profile drift, generated-file hygiene.
- Consolidator independently re-read the two disputed principles and the adapter's
  precedence text before assigning final severity; one lane finding is downgraded below,
  with the reason stated.

---

## MUST_FIX

### 1. P100 (reading-diagnostics) is both mis-cited in the profile and rendered as a bare act-on-a-learner imperative in the always-on invariant layer

- **Location A:** `subagents/learning-science-advisor/profile.yaml:282`
  (`knowledge_partition.always_on`, *expertise-development-and-transfer* paragraph)
- **Location B:** `.claude/agents/generated/learning-science-advisor.md:102`
  (Operating invariants), compiled from `principles/principles.yaml` P100
- **Rule text (A):** "...assesses analytical, creative, and practical competence and
  context-developed expertise rather than inferring everything from one static score.
  (P005, P009, P018, P039, **P100**, P104, P108, P117, P122, P128, P131)"
- **Invariant text (B):** "**[P100]** Collect real-word reading, spelling ability and word
  attack skills as the diagnostic measures, since they are the greatest predictors of
  reading comprehension"
- **Cited principle:** P100 — statement as above; `applies_when: ["Choosing reading
  assessments for diagnosis", "Evaluating or supporting persistent reading difficulty"]`
- **Grade:** SCOPE_BROADENED (mis-citation — different topic) + role tension

**Why.** Two independent lanes converged on P100 from opposite directions.

*Provenance side:* P100 is a narrow claim about which measures best predict reading
comprehension. Nothing in the expertise/transfer paragraph — goal-directed practice,
feedback, coaching, simulation, applicability boundaries, far transfer, multi-dimensional
competence — corresponds to reading-diagnostic selection. P100 is cited nowhere else in
`profile.yaml`, so this is its only, mismatched, use. A reader following the citation to
check the rule lands on an unrelated principle.

*Role side:* the invariant compiler strips `applies_when`, so P100 reaches the always-loaded
layer as an unconditional imperative to **collect diagnostic measures on a learner** — the
only invariant of the 54 phrased as an act-on-an-individual instruction. It sits against
`forbidden_behaviours` "Diagnosing a learner", `when_not_to_use` "The caller wants a learner
assessed, diagnosed, or labelled", and the router's "Not for diagnosing a learning
disability". The skill body correctly says "**recommend** collecting…"; only the
always-loaded layer states it bare.

**Mitigation that keeps this at must-fix rather than critical:** the adapter carries explicit
precedence text in three places — line 19 ("The invariants below are advisory criteria, not
authority to act; the advice-only boundary and forbidden behaviours override them"), line 23,
and line 272 — and the `failure-recovery` worked example declines a diagnosis request
outright. So the agent is not *authorised* to diagnose. The defect is a must-hold line that
reads as an instruction to do a forbidden thing, plus a false provenance link.

**Fix (smallest).**
1. `profile.yaml:282` — drop `P100` from the citation list. The other ten citations already
   ground the paragraph's claims in full; nothing becomes unsupported.
2. `principles/principles.yaml` P100 — make the single statement self-sufficient and
   advisory so it survives `applies_when` stripping, e.g. "When advising on assessment for a
   persistent reading difficulty, recommend real-word reading, spelling ability and word
   attack skills as the measures the qualified assessor collects, since they are the greatest
   predictors of reading comprehension."
3. Re-export the adapter, MINOR/PATCH `agent_version` bump, CHANGELOG entry, re-validate.

---

## NICE_TO_HAVE (not gating)

### P109 cited in the evidence-appraisal paragraph — downgraded from Lane A's MUST_FIX

- `profile.yaml:264-265`: "...and refuses to infer truth from familiarity, vividness,
  confidence, or consensus. (… P109 …)"
- P109's `applies_when` is squarely eyewitness/episodic-memory reliability ("Recollection or
  subjective certainty is being treated as factual evidence"), not appraisal of a claimed
  learning technique. Lane A graded this SCOPE_BROADENED / MUST_FIX and proposed moving the
  citation to the *memory-mnemonics-and-recall-accuracy* paragraph (lines 283-292), where it
  fits naturally next to P045.

**Why downgraded.** The must-fix bar for this gate is *a rule stronger than its evidence*.
Here the profile text is a near-verbatim restatement of P109's own statement, and it is a
**negative, caution-preserving** rule ("do not infer truth from X") — applying it in a wider
context makes the agent more sceptical, not more assertive. The paragraph is independently
grounded by P053, P072 and P105. Real provenance untidiness; no over-claim, no safety
consequence. Worth fixing on the next touch, not worth reopening the loop.

### Other Lane A weak-linkage citations (no grade above WITHIN_SCOPE)

- `profile.yaml:282` — P104 (mental/imagined rehearsal) cited in the expertise-transfer
  paragraph, which never mentions mental rehearsal. On-topic, no textual anchor.
- `profile.yaml:234` — P141 (structured comparison to make ambiguity safe) in the
  motivation/belonging paragraph; only anchor is "preserving safely facilitated disagreement".
- `profile.yaml:152` — P145 (cross-context knowledge linking) cited for the spacing
  paragraph's "pruned reusable pool" claim; P093 (assessment-item pool management) is the
  more precise match.
- `profile.yaml:217-218` — P041 is scoped "At home…" in its statement; the metacognition
  paragraph cites it without that qualifier. The worked example at lines 407-408 restores the
  scoping correctly, so this is paragraph-level generalisation, not contradiction.

### P146 altitude drift (Lane B)

`.claude/agents/generated/learning-science-advisor.md:132` — "Protect developmentally
sensitive periods by preventing severe early deprivation and providing high-quality
relational, linguistic, sensory, and educational inputs as early as possible…" reads as a
child-welfare/safeguarding action rather than a learning-design criterion, and its principle
metadata pairs it with a `test_cases` entry "Prioritize early enriched **placement**" —
placement decisions are forbidden. The adapter text grants no authority, so this is wording.
Optional fix: reframe as "Advise that … be protected/provided …" and drop the
placement-flavoured test case.

---

## Clean — checks that found nothing

Lane B verified mechanically, not by inspection:

- **Truncation:** programmatic sweep of the whole adapter for trailing `…` / `...` / `—` /
  `:` / ` and` / ` or` / `(e.g`, and for unbalanced `(` or `"` — **zero hits** (only match was
  the legitimate heading "For deeper context, read:"). The specific failure mode this gate
  was told to hunt — an invariant ending `(e.g` or an ellipsis — **does not occur**. P146,
  the longest invariant, is complete through its final clause.
- **No dropped must-hold layer:** re-compiled the invariant set from source with
  `compile_invariants(load_principles(...))` and diffed against the 54 rendered
  `- **[Pnnn]**` lines — **54 compiled == 54 rendered**, zero missing, zero extra, zero text
  drift. Each rendered invariant is the *complete* principle statement, no first-sentence cut.
- **Adapter↔profile parity:** `when_to_use` 5/5, `when_not_to_use` 5/5, `quality_bar` 7/7,
  `forbidden_behaviours` 8/8, `handoff_rules` 3/3 — element-for-element equal. Frontmatter
  `name` == slug; `description` == `router_description` (whitespace-normalised exact).
- **Tools:** `Read, Grep, Glob` — read-only default; no `produce`/`patch-suggest` mode, no
  `patch_policy` block. **No tool granted beyond the profile.**
- **Export freshness:** installed adapter byte-identical to
  `subagents/learning-science-advisor/adapters/claude-code/learning-science-advisor.md`
  (md5 `37660b02b80cc65e394012bb8c55a3fe`); `validate_generated_package` → VALIDATION PASSED
  incl. `adapter-sync` and `adapter-fresh` (no unexported profile change).
  `adapter_policy_scan` → PASS.
- **Hygiene:** `GENERATED FILE. DO NOT EDIT DIRECTLY.` at line 8 (< 20).
- **Numeric claims:** the two numbers in the profile — P061's "one tenth to one fifth" spacing
  heuristic and P103's 0.18/0.09/0.18 modality-matching effect sizes — are carried verbatim
  from their cited principle statements. No invented thresholds.
- **Hedging:** `quality_bar`, `forbidden_behaviours`, `handoff_rules`,
  `source_of_truth_policy.precedence` and 13 of 15 `always_on` paragraphs preserve their
  principles' conditional language (novice/expert reversal, "where feasible", "unless
  independent error detection is the target", "except where complex structured or
  higher-order outcomes leave the benefit uncertain"). No unconditional "always/never" found
  sitting on a conditional principle.
- **Orphan IDs:** none — every cited `P###` exists in `principles/principles.yaml`.

Only outstanding validator WARN is `quote-scan: rights NOT verified` (no `sources/markdown/`
in the package) — pre-existing and unrelated to this gate.

---

## Verdict

The loop's must-fix=0 claim was **near-correct but not correct**. No truncated invariant, no
dropped must-hold layer, no tool-grant widening, no export drift — the structural safety
surface is clean. One real defect survived: **P100**, flagged independently by both lanes,
mis-cited in `profile.yaml` and rendered in the always-on layer as a bare instruction to
collect diagnostic measures on a learner, which the package elsewhere forbids. Contained by
the adapter's advisory-criteria precedence text, so not critical, but it is a must-hold line
telling the agent to do a forbidden thing on a false citation. Fix it, re-export, re-validate.

MUST_FIX_COUNT: 1
