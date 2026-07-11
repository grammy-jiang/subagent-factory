# Review — calibrated-forecasting SKILL.md (r2)

**Target:** `/home/grammy-jiang/projects/intelligence-analysis-agent/.claude/skills/calibrated-forecasting/SKILL.md`
**Grounding:** `docs/intelligence-analysis/PIPELINE-grounded.md` (Step 9 row), cross-checked vs `structured-analysis/SKILL.md` orchestrator + `DESIGN-SPEC-intel-analysis-agent.md`.
**Lens:** METHOD skill (the method the agent RUNS, Step 9), not a reviewer. Two parallel passes: agent-skills-advisor (authoring) + ai-agent-engineering-reviewer (method design).
**Scope:** REVIEW ONLY. No edits.

Core forecasting logic is sound and well-grounded (outside-view-first, own-track-record check, Fermi with correct multiply-not-average conjunction, fold in bias/deception `ReviewFinding[]`, explicit numeric probability + separate confidence, named dissent; Tetlock/EPJ citations track). Findings are at the **delegation boundary** and **tool governance**, not the math.

---

## MUST_FIX

### M1. Steps 9–10 collide with the orchestrator's Step 9a/10/10a and can premature-lock the forecast
The pipeline Step 9 is split in `structured-analysis/SKILL.md` into: Step 9 (this skill produces *the number* — scope ends there), Step 9a (**orchestrator** invokes `calibration-forecasting-reviewer` via Task, handed the RAW case state per invariant 2), Step 10 (orchestrator assembles the full Assessment + human approval), Step 10a (orchestrator calls `log_forecast` **only after** approval).

But this skill's own Procedure steps 9–10 instruct it to *itself* invoke the Task audit, run a human gate, and commit via `log_forecast` — duplicating those actions. Result is either (a) the reviewer subagent runs twice (wasted Task call, two possibly-divergent audits) or (b) this skill commits on its own **truncated** gate (just the number) before the full Assessment exists and is approved — the exact premature-lock the "Human before commit" / Step-10a "only after Assessment approved" guard prevents. Compounding: its Step 9 hands the reviewer only "the draft forecast (number, base rate, Fermi, confidence, dissent)", not the raw hypotheses/evidence/matrix/assumptions that invariant 2 ("critique reads the RAW case state, not your narrative") mandates.

**Fix:** Bound this skill's procedure to steps 1–8 (produce the draft Judgment) when nested as the Step-9 delegate, and explicitly return control to the orchestrator for audit/gate/commit. If a standalone low-stakes mode is intended, fork that path explicitly instead of one linear 10-step sequence that collides when nested.
*Violates:* `PIPELINE-grounded.md` row 9 + "Human before commit" loop-back; `structured-analysis/SKILL.md` invariants 1–2, Step 9/9a/10/10a ownership.

### M2. No `allowed-tools` frontmatter, yet prose calls Task + MCP writes
Frontmatter declares only `name`/`description`. Prose invokes `get_calibration_report()`, the Task tool (step 9), and `log_forecast(...)` (Persistence) — none scoped. Sibling `structured-analysis/SKILL.md` sets the precedent with an explicit `allowed-tools:` line; `DESIGN-SPEC` Layer-1 says calibrated-forecasting's tool access is "likely none" (pure-reasoning skill). Undeclared authority → per-use confirmation prompts and a governance gap.

**Fix — resolve jointly with M1** (the two interact — do not fix in isolation):
- If M1 is fixed by handing Task/commit back to the orchestrator (design intent): declare read-only only — `allowed-tools: calibration-tracker:get_calibration_report` (or none) — and drop the Task-invoke + `log_forecast` instructions from this skill's procedure.
- If a standalone mode keeps them: declare `allowed-tools: Task, calibration-tracker:get_calibration_report, calibration-tracker:log_forecast, calibration-tracker:resolve_forecast`.
*Violates:* `DESIGN-SPEC` Layer-1 governance note; least-privilege precedent in `structured-analysis` frontmatter.

---

## SHOULD

### S1. Reviewer-voice / redundant restatement bloats an always-loaded body
Nearly every Procedure `(P0xx)` citation is duplicated verbatim in the closing `## Grounding` (P006/P007/P023, P036/P018, P005/P043, P014, P015/P010, P012), and "draft ≠ commit; order draft→audit→gate→lock" is stated 3× (step 8, step 10, Persistence intro). Citations are factually correct — problem is inflated tier-1 content reading like an audit trail on an operational recipe.
**Fix:** Strip inline `(P0xx)` tags from the numbered steps (agent needs the instruction, not the ID); keep the citation trail only in Grounding, or move Grounding to `references/grounding.md` (progressive disclosure). State the required order once (Persistence); step 10 points to it.

### S2. Description doubles as a procedure summary
Description restates the full sequence the Procedure already spells out. It's loaded for every skill at all times (~38 skill dirs here) → real cumulative tier-1 cost.
**Fix:** Trim to scope + trigger conditions (what question, when to invoke / not). Let Purpose/Procedure carry the "how."

### S3. Triggering collision with finely-sliced sibling skills
`.claude/skills/` also holds reviewer-internal reference slices (`calibration-and-probability-hygiene`, `forecast-scoring-and-evaluation`, `base-rates-outside-view-and-regression`, `forecasting-judgment-foxes-and-track-record`, ...). Auto-selection is description-only → a forecasting request may fire a reference slice instead of `calibrated-forecasting`, the intended sole "produce a number" entry point.
**Fix:** Scope those slices out of the main-agent-visible pool (they belong to the reviewer subagent's own skill path), OR add one disambiguating line stating `calibrated-forecasting` is the sole entry point for producing a committed probability and the slices are reviewer-internal reference.

### S4. Conjunctive-probability arithmetic not offloaded to a deterministic tool
`DESIGN-SPEC` item 2: "bundle a small deterministic script for compound-probability arithmetic (don't do that math via token generation)." Step 3 states the conjunction rule ("multiply, do not average") but performs the arithmetic in prose.
**Fix:** Reference a small deterministic calculator for the Fermi multiplication step.

### S5. No first-person anchoring/availability/overconfidence self-check
`DESIGN-SPEC` item 2: this skill should "absorb the anchoring/availability/overconfidence checklist as a pre-commit self-check." Current procedure only folds in *externally supplied* `ReviewFinding[]` (step 4) + track-record read (step 2); no own self-check.
**Fix:** Add a short self-check before finalize (step 7): anchored on first estimate? vivid/recent case over-weighted? track record justify this confidence?

---

## NICE

- **N1.** `get_calibration_report()` (step 2) has no "MCP — see Persistence" forward-pointer, unlike step 8. Add one.
- **N2.** `## Output` folds "indicators for updating" into the Judgment artifact, but `PIPELINE-grounded.md` (line 41) defines Judgment as "probability + confidence, dissent" and assigns indicators to the Step-11 `Indicator[]` artifact (SAT skill). Add a line clarifying these are the forecaster's own revision triggers, distinct from Step 11's formal watch-list.
- **N3.** Step-number drift: Grounding cites "Step 7"(bias)/"Step 8"(contrarian+deception) per the original 12-row table, but the orchestrator merged those into one Step 7 and renumbered forward. Align citations or note they track the pipeline doc's original table.

---

## Consolidation notes
- **M2 both passes agreed** (missing `allowed-tools`); its correct resolution depends on M1's design decision — fix together.
- M1 is the load-bearing method finding: this skill claims audit/gate/commit authority that the orchestrator already owns. Everything else is authoring hygiene.

MUST_FIX_COUNT: 2
