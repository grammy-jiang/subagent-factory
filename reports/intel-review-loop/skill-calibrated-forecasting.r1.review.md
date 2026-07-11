# Review — `calibrated-forecasting` SKILL.md (r1)

**Target:** `/home/grammy-jiang/projects/intelligence-analysis-agent/.claude/skills/calibrated-forecasting/SKILL.md`
**Grounding:** `docs/intelligence-analysis/PIPELINE-grounded.md` Step 9
**Reviewers:** `agent-skills-advisor` (authoring), `ai-agent-engineering-reviewer` (method/orchestration)
**Scope:** REVIEW ONLY — no edits. Method + authoring altitude, not prose nits.

This skill is the *method the intel-analysis agent runs* to turn an ACH ranking into a
calibrated number at Step 9. The Procedure math (outside view → Fermi → moderate inside-view
adjust → explicit number → update plan) is sound and correctly ordered. The defects below are
all in **orchestration wiring** — how the method connects to its inputs, its reviewer audit,
the human gate, and the irreversible `log_forecast` lock. Both reviewers converged
independently on the same three core problems.

---

## MUST-FIX

### M1. Step 7 "log now" contradicts Persistence "log after the human gate" — and can lock a number before any check. (BOTH reviewers)
`SKILL.md:50` step 7: "Log the forecast verbatim now so it can be scored later."
`SKILL.md:65-67` Persistence: "After the human gate, **commit** the number with `log_forecast(...)`" — which the same lines say **locks** the question+probability (only the outcome appended later).
Opposite timing for the same action. A runner cannot tell whether to call `log_forecast` at
step 7 or hold it. **Failure:** runner calls `log_forecast` at step 7, locking an unapproved,
un-audited number into the cross-case `calibration-tracker`; the lock is irreversible except
for outcome-append, so there is no correction path if the reviewer or human later finds a
skipped base rate / hedge word / uncorrected bias.
**Fix:** step 7's "log verbatim" must mean *write into the case artifact* only; state once,
explicitly, that the `log_forecast` MCP call happens **only after** reviewer audit + human
gate. Disambiguate the word "log" from the tool literally named `log_forecast`.

### M2. The `calibration-forecasting-reviewer` audit is not an executable step — it lives only in frontmatter prose. (eng-reviewer)
Pipeline row 9 = "skill: calibrated-forecasting **+ subagent audits**" — the audit is part of
the step. In the file the pairing appears only in `description:` (`:3`) and Purpose (`:12-13`).
The numbered Procedure 1–7 (`:28-50`) — the part actually executed — never says "invoke
`calibration-forecasting-reviewer` via Task with the draft forecast."
**Failure:** an orchestrator executes Procedure verbatim, emits a number, marks the skill done;
the review leg of Step 9 silently never fires.
**Fix:** add an explicit Procedure step invoking `calibration-forecasting-reviewer` via the
Task tool on the draft, before persistence.

### M3. The "human gate" is invoked as a precondition but never defined in this skill's Procedure. (BOTH)
`SKILL.md:66` presupposes a "human gate"; `:71` ties `judgment_source="analyst_confirmed"` to
"a human read-back." Neither appears in Procedure steps 1–7. Because "When to use" (`:17`)
permits standalone invocation, a runner following only this file has no defined gate to
satisfy, and "human read-back" is a weak, unspecified proxy for the pipeline's Step 10
human-decides gate (the decisionmaker owning the Assessment).
**Failure:** an orchestrating agent implements "read-back" as an internal echo turn with no real
human, then records `analyst_confirmed` — corrupting the calibration-tracker institutional
record. **Fix:** define the gate inside the Procedure (or restrict "When to use" so this skill
runs only as a substep of `structured-analysis`, which owns the gate), and tie
`analyst_confirmed` to the actual Step 10 human approval, not a bare read-back.

### M4. Audit-and-approval-before-lock is not sequenced. (eng-reviewer)
Given `log_forecast` is an irreversible lock (`:67`), the reviewer audit (M2) and human gate
(M3) must both complete **before** the lock. Nothing in Procedure or Persistence enforces this
order — it is left to chance which of audit / gate / lock fires first.
**Fix:** state the required sequence explicitly: draft → reviewer audit → human gate →
`log_forecast`.

### M5. Skill never ingests `ReviewFinding[]`, though Step 9's input contract requires it. (eng-reviewer)
Pipeline row 9 upstream-in = `Ranking + ReviewFinding[]` (bias-perception-reviewer from Step 7
+ method/deception-reviewer from Step 8). "When to use" (`:18`) and "Inputs" (`:54`) name only
"an ACH ranking" — `ReviewFinding[]` is never an input, and no step folds flagged
bias/deception into the number before it is set.
**Failure:** bias-perception-reviewer flagged mirror-imaging on the lead hypothesis; the
forecast never sees it and is calibrated around an unflagged-bias anchor — confidently wrong,
not merely imprecise. **Fix:** add `ReviewFinding[]` as a required input and a step that
discounts/addresses flagged findings before finalizing.

---

## SHOULD-FIX

### S1. Trigger overlap with `structured-analysis`; missing anti-trigger lets the full pipeline's safeguards be bypassed. (authoring)
`:17` ("a question needs a probability… over-/under-confident is costly") near-duplicates
`structured-analysis`'s trigger. "When not to use" (`:21-24`) excludes only near-certain and
review-of-existing cases — not contested, multi-hypothesis, high-stakes questions that should
reach this skill only *after* Steps 1–8.
**Failure:** "probability Country X strikes this month, high-stakes" fires `calibrated-forecasting`
directly, producing a bare base-rate number with no hypothesis set, no evidence grading, no
independent bias/deception critique. **Fix:** add an anti-trigger routing contested/multi-hypothesis
high-stakes questions to `structured-analysis` first.

### S2. Output drops `dissent`, a field the pipeline's Judgment artifact requires. (eng-reviewer)
Pipeline Judgment artifact = "probability… + confidence, dissent." Output (`:59-61`) lists
probability, base rate, Fermi, confidence — no dissent. Step 10's decisionmaker never sees
recorded disagreement. **Fix:** add dissent to Output.

---

## NICE-TO-HAVE

- **N1.** `calibration-tracker` used only retrospectively. Pipeline row 9 store-read lists own
  track record as an *input to the current judgment* (check personal calibration bias before
  finalizing). `get_calibration_report()` is described (`:69`) only for post-hoc scoring, never
  invoked in Procedure to shade the estimate. (eng-reviewer)
- **N2.** No tie to evidence reliability/credibility grades (A–F / 1–6) from Step 3. Step 5
  (`:42-43`) handles *probability* of an item but ignores its FM C428 reliability grade — an
  F/6 and a high-reliability item at equal likelihood are treated identically. (eng-reviewer)
- **N3.** No loop-back/revision branch if the reviewer or human gate rejects the forecast; the
  pipeline's iterate principle (Heuer C249) is never operationalized. (eng-reviewer)
- **N4.** Grounding cite `docs/intelligence-analysis/PIPELINE-grounded.md` (`:79`) is unqualified
  and not resolvable from within `intelligence-analysis-agent`; sibling `structured-analysis`
  qualifies the identical path "in the factory repo." (authoring)
- **N5.** No `allowed-tools` frontmatter despite naming three MCP calls; consistent with sibling
  leaf skills (orchestrator pre-approves tools) so likely deliberate — but if standalone
  invocation is intended, each call triggers a confirmation prompt breaking the "now" flow. (authoring)
- **N6.** Description (`:3`) uses second person ("you need"), breaking the third-person trigger
  convention of sibling skills (`structured-analysis`, `source-evaluation`, `osint-investigation`). (authoring)

---

## Note on non-findings
The many `Audits…` calibration/forecast skills in `.claude/skills/` (e.g.
`calibration-and-probability-hygiene`, `base-rates-outside-view-and-regression`) are scoped to
reviewer subagents via each agent's `skills:` allowlist, not globally selectable — so they are
**not** a live trigger-collision risk for this method skill and are excluded above.

MUST_FIX_COUNT: 5
