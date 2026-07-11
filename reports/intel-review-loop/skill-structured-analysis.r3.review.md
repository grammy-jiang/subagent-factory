# Review — `structured-analysis` SKILL.md (r3)

**Target:** `intelligence-analysis-agent/.claude/skills/structured-analysis/SKILL.md`
**Grounding:** `subagent-factory/docs/intelligence-analysis/PIPELINE-grounded.md`
**Kind:** METHOD skill — the procedure the intel-analysis agent itself runs (not a reviewer subagent).
**Reviewers:** agent-skills-advisor (authoring quality) + ai-agent-engineering-reviewer (method design). One pass each, consolidated.

## Verdict

Skill is well-grounded and structurally sound. Both reviewers independently confirm: the 11 skill steps map faithfully onto the 12 grounded pipeline steps (Steps 7/8 legitimately consolidated, Step 12 Brier carried to Deferred, not dropped); the human-approval gate is real and structurally unskippable; invariant 2 correctly forces reviewer subagents to see raw state not narrative; failure/edge handling (MCP-write fallback, stale-grade refusal, reviewer-Task halt, bounded 3-iteration escalation) is explicit. **No over-reach** — never commits a judgment, publishes, or acts before the human gate; OSINT is read-only; every grade/probability stated as judgment not fact.

One real MUST-FIX, flagged by BOTH reviewers independently and verified in source.

---

## MUST-FIX

### M1 — Step 9 instructs a `calibration-tracker` read that frontmatter never grants
**Location:** line 4 (`allowed-tools`) vs. line 153 (Step 9).
**Verified:** line 4 grants only `calibration-tracker:log_forecast` (write, used Step 10a). Line 153 orders the agent to "query the `calibration-tracker` MCP for the analyst/model's own resolved track record." No read/query tool over `calibration-tracker` is declared anywhere in frontmatter, and — unlike `source-trust-registry`, Brier scoring, live OSINT — this read is NOT in the Deferred section. So Step 9 reads as a live capability the agent has no way to invoke: it will stall, silently skip, or fabricate the track-record check — the last directly undercutting invariant 4 (never fabricate a judgment). Defeats the purpose of pre-approving tools (no per-use prompt) and is an internal step-vs-frontmatter contradiction.
**Fix (pick one):**
- (a) If the read path exists: add the read tool (e.g. `calibration-tracker:get_calibration_report` / `query_history` — verify exact name against the MCP server) to both `allowed-tools` and the "Current phase" MCP list; **or**
- (b) If not built yet: move the track-record read into the Deferred section next to `source-trust-registry`, and rewrite Step 9 to state the check is deferred — proceed from stated base-rate reasoning alone, mirroring how Step 1 already handles the missing base-rate store (line 72).

---

## SHOULD-FIX

### S1 — Over-broad `Skill` grant vs. actual usage (least-privilege)
**Location:** line 4. Grants bare `Skill` (invoke ANY skill) but body only ever calls three: `source-evaluation` (Step 3), `osint-investigation` (Step 3), `calibrated-forecasting` (Step 9). Directory holds ~12 sibling audit skills with adjacent names this orchestrator should never invoke mid-run. **Fix:** scope to the three names actually used, e.g. `Skill(source-evaluation)`, `Skill(osint-investigation)`, `Skill(calibrated-forecasting)`.

### S2 — Ambiguous, ungrounded early invocation of `calibration-forecasting-reviewer` duplicates its guaranteed Step-9a run
**Location:** Step 7. Pipeline places this reviewer at row 9 (after a Judgment/number exists). Step 7 invites it "early... if the ranking already implies confidence" — but there is no probability to audit yet, only a qualitative ranking; the trigger is subjective with no operational test; and no dedup/precedence rule reconciles an early firing with the mandatory Step 9a run. **Fix:** drop the optional early path; make Step 9a the sole invocation point (matches pipeline row 9). If an early lopsided-ranking check is genuinely wanted, ground it as its own named check, not a reuse of this reviewer ahead of its designed input.

### S3 — Split grading instruction: who grades in Step 3?
**Location:** lines 84–89. First says the agent grades A–F / 1–6 directly; two sentences later says use the `source-evaluation` skill to grade. Read literally → two independent grading passes or ambiguity over which is authoritative. **Fix:** merge into one instruction — grading is performed by invoking `source-evaluation`; describe A–F/1–6 as that skill's output format, not a separate agent action.

### S4 — No progressive-disclosure tier; full ~2,900-word body loads every trigger
**Location:** whole file (~216 lines; `Glob` confirms directory holds only `SKILL.md`). The "Grounding" section and extended per-step rationale are reference material, not procedure. **Fix:** move citation/grounding detail + deferred-items rationale into `references/grounding.md`; keep `SKILL.md` to the operational skeleton (Purpose, invariants, When/When-not, numbered steps as terse imperatives, Output).

### S5 — Duplicated content (two instances)
- "Current phase" (lines 17–23) restates the four Deferred items (lines 196–205) verbatim in preview form. **Fix:** keep the Deferred section canonical; reduce "Current phase" to a one-line pointer.
- Per-step inline citations (in each `### Step` heading) are re-listed in prose by the closing "Grounding" section (lines 207–215), ~9 lines of pure restatement. **Fix:** trim "Grounding" to a single pointer sentence to `PIPELINE-grounded.md`. (Folds into S4.)

---

## NICE-TO-HAVE

- **N1 — Loop-back doesn't name the reviewer re-run.** Step 8's convergence ("until the reviewers raise nothing new material") depends on re-invoking the reviewers, but Step 8 only says "re-run the affected earlier steps" — the Task calls (Step 7) are left implicit; a careless run could revise and skip to Step 9, breaking the loop. Contrast Step 9a, which is explicit. **Fix:** add "then re-invoke the reviewer subagent(s) whose finding triggered the revision."
- **N2 — Deception-reviewer gate has no named signal.** Step 7's `deception-detection-reviewer` is "gated on a security review — skip unless that gate is cleared" (prose only), whereas live OSINT names `OSINT_LIVE=0`. No flag/config/tool for a deterministic decision. **Fix:** name the actual gating signal (env var / config flag / recorded out-of-band human decision), matching `OSINT_LIVE`.
- **N3 — Name proximity to sibling `structured-analytic-techniques`.** Orchestrator (`structured-analysis`) vs. the narrow technique-audit skill share the two most salient name words — collision risk for name-weighted routing. **Fix:** consider a more distinct name (e.g. `analytic-tradecraft-workflow`), or leave as-is if routing is empirically verified.
- **N4 — Trigger clause late in description.** Line 3 front-loads WHAT (good) but the WHEN clause sits at the end of a ~600-char string after two delegation sentences. **Fix:** pull a short trigger clause forward if this surface weights early text.

---

## Verified sound (not flagged)
Frontmatter valid/minimal (name lowercase-hyphenated, <64 chars); MCP refs use fully-qualified `server:tool` form throughout; invariants block (lines 40–58) is a good scannable pattern; failure/edge handling is a strength; human gate honored at Steps 9/9a/10/10a.

MUST_FIX_COUNT: 1
