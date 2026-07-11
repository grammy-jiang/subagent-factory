# Review — `calibrated-forecasting/SKILL.md` (r3)

**Target:** `/home/grammy-jiang/projects/intelligence-analysis-agent/.claude/skills/calibrated-forecasting/SKILL.md`
**Grounded against:** `docs/intelligence-analysis/PIPELINE-grounded.md` (Step 9 row + loop-back / human-gate section)
**Reviewers:** `agent-skills-advisor` (authoring quality) + `ai-agent-engineering-reviewer` (method design)
**Verdict:** Sound METHOD skill. Well-formed imperative Procedure, correctly scoped to draft-Judgment-only, correctly defers audit/gate/commit to `structured-analysis`. ONE MUST_FIX — the frontmatter description contradicts that scope. Both reviewers flagged it independently (highest confidence).

---

## MUST_FIX

### M1 — `description` (line 3) says "committed", body says draft-only — the one place that inverts the skill's load-bearing invariant

> `"...This is the sole entry point for producing a committed probability."`

The description is the **only** surface a routing agent reads before deciding whether this skill already finalizes the number. Every other section says the opposite:
- Purpose (~L14): *"The independent audit, the human gate, and the commit are **not this skill's**"*
- Procedure intro (~L40–41): *"produces the **draft** Judgment and stops... does **not**... call `log_forecast`"*
- Output (~L95–96): *"The number is a draft until the orchestrator's audit, human gate, and commit run — this skill does not lock it."*
- Persistence (~L105): required order *draft → reviewer audit → human gate → `log_forecast` lock*

Failure mode: a description-only router routes straight to this skill as the *final* number-producer and skips Steps 9a/10/10a — a silently unreviewed, uncommitted-but-treated-as-committed probability. This is exactly the over-reach the method must not permit.

**Fix:** drop "committed" — e.g. *"...the sole entry point for producing the draft probability the pipeline commits only after the orchestrator's Step 9a audit, Step 10 human gate, and Step 10a `log_forecast` commit."*

---

## SHOULD_FIX

### S1 — Procedure step 4 (L56–59) has no branch for the "no `ReviewFinding[]`" low-stakes path the skill itself allows
Step 4 reads as unconditionally mandatory (*"Read the `ReviewFinding[]` handed in... For each flagged bias or D&D risk, discount or re-anchor"*), but When-to-use bullet 3 (L33–36) sanctions a low-stakes path with no prior bias/deception workflow, and Inputs (L85–86) marks `ReviewFinding[]` "**required** on the Step-9 path" (⇒ absent otherwise). An executing agent has no instruction for the empty/absent case.
**Fix:** add a conditional — Step-9 path: findings required, fold in before proceeding; low-stakes shortcut with no findings: skip step 4 and note in the draft that no bias/deception review was performed.

### S2 — Case-artifact write (step 9, L76–77) names no tool/mechanism; `allowed-tools` grants only one read-only MCP tool
`allowed-tools: calibration-tracker:get_calibration_report` (L4) is the sole grant, and Persistence (L100–101) reaffirms *"its only calibration-tracker access."* Step 9 instructs *"Write the draft forecast into the case artifact"* — the pipeline's distinct `case-workspace` store (`PIPELINE-grounded.md:47`) — but no write mechanism is declared. Agent may either invent an out-of-surface call or silently fail to persist where Step 9a expects the draft.
**Fix:** state that the case-artifact write uses ordinary file-write capability (not an MCP tool), so the `allowed-tools` restriction isn't misread as blocking step 9.

### S3 — draft/audit/gate/commit boundary restated ~7× across the body (duplicated-content anti-pattern)
Purpose, two When-to-use bullets, Procedure intro, Procedure step 9, Output, all of Persistence, and Grounding each re-explain that Steps 9a/10/10a belong to the orchestrator. Beyond the first authoritative statement + the one operational (tool-signature/ordering) statement, each restatement costs body tokens on every trigger with no new information.
**Fix:** state the boundary once in Purpose, keep operational detail once in Persistence, shorten the other ~5 to a one-clause cross-reference.

### S4 — `## Grounding` block (L120–132) is always-loaded audit metadata that belongs in a reference file
Principle/claim IDs + book citations are human-facing traceability, not runtime behaviour; per progressive disclosure they belong in `references/grounding.md` linked from SKILL.md, not the always-loaded body.

### S5 — When-not-to-use (L32) disambiguates only against the *subagent* `calibration-forecasting-reviewer`, not co-installed reviewer skills
Flat `.claude/skills/` also holds `base-rates-outside-view-and-regression`, `calibration-and-probability-hygiene`, `forecasting-judgment-foxes-and-track-record` — all describe an "audit a forecast" job using this skill's own trigger vocabulary ("outside view", "base rate", "confidence"). A description-matching router has real producer-vs-auditor ambiguity this file doesn't address.
**Fix:** broaden L32 to note any "Audit…/Review…" skill in this namespace owns critique — or (deployment concern) don't flatten reviewer skill folders into the top-level namespace of a repo that also runs the producer.

---

## NICE

- **N1 — step 7 heading "pre-commit self-check" (L65)** collides with reserved commit vocabulary (Step 10a `log_forecast`) the file insists this skill never does. Rename → "final self-check before stating the number".
- **N2 — step 2 "before finalizing" + `get_calibration_report()` (L49–51)** is locally ambiguous (finalizing the anchor vs the whole forecast at step 8); reader may wonder if the tool is called twice. Reword → "before moving off this base-rate anchor, read your calibration history".
- **N3 — no Step-9a re-entry note.** Clean forward hand-off (L76–79) never says what happens if the audit returns the draft for revision. Not a grounding gap (loop-back plumbing is quarantined in `PIPELINE-grounded.md:52,60`), but one sentence — "if the Step 9a audit returns the draft, re-enter at the relevant Procedure step" — closes the readability gap without owning the plumbing.
- **N4 — description length (~150 words).** Precise and trigger-oriented, but carries the full Step-9a/10/10a ownership explanation also restated in the body; after S3 consolidation it can end with a short pointer instead of the full enumeration.

---

MUST_FIX_COUNT: 1
