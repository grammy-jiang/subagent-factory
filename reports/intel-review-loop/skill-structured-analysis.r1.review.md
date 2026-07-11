# Review — `structured-analysis` SKILL.md (round 1)

**Target:** `/home/grammy-jiang/projects/intelligence-analysis-agent/.claude/skills/structured-analysis/SKILL.md`
**Grounding:** `docs/intelligence-analysis/PIPELINE-grounded.md`
**Reviewers:** `agent-skills-advisor` (authoring quality) · `ai-agent-engineering-reviewer` (method design)
**Verdict:** The method is sound and faithful step-by-step — all Step 1–11 citations trace correctly to the pipeline, no fabricated sources. The failures are all **phase-framing contradictions**: the Purpose/Deferred sections describe an old zero-MCP MVP while the procedure body actively invokes three MCP servers and a "deferred" subagent. An executing agent gets conflicting instructions about what tools/authority it has.

---

## MUST-FIX

### M1 — Purpose "no MCP" claim contradicts Steps 3/4/9 (both reviewers)
`SKILL.md:16-18` — Purpose declares "**MVP (Phase 1)** … the whole case runs in-context as prose — no persistent store, no MCP." But the procedure gives load-bearing MCP calls: Step 3 (`:77-79`) `evidence-ledger` (`add_evidence`/`grade_evidence`/`get_source_history`); Step 4 (`:86-88`) `ach-engine` (`create_matrix`/`rate_cell`/`score_matrix`); Step 9 (`:134-137`) `calibration-tracker` (`log_forecast`) with the explicit line "All three MCPs … are now available." An agent that enters via the Purpose section (the natural progressive-disclosure entry) believes no MCP exists, then hits three MCP-invoking steps. Live tool-scope/authority ambiguity.
**Fix:** Rewrite `:16-18` to state the *current* phase truthfully (which MCPs are live and used at which steps) and delete the "no persistent store, no MCP" claim. If a true zero-MCP variant must coexist, hedge each call site with prose-only fallback language instead.

### M2 — Deferred section is stale against Steps 7 and 9 (both reviewers)
Two flat contradictions inside the "Deferred (not in this MVP)" block:
- `SKILL.md:166` marks `deception-detection-reviewer` as "Phase 4, gated on a security review" — but Step 7 (`:106-118`) lists it as one of four subagents actively `Run:` with a fully specified trigger ("when the evidence chain includes ingested/OSINT material…"). Agent gets two conflicting orders on whether to call it. (Note: `PIPELINE-grounded.md` itself marks the deception-reviewer deferred at step 8, so Step 7's active listing also drifts from grounding.)
- `SKILL.md:161-163` says `calibration-tracker` is deferred and forecasts are "un-scored" at MVP — but Step 9 (`:134-137`) actively commits the number via `log_forecast` "so it can be Brier-scored when the outcome resolves." Opposite of "un-scored."
**Fix:** Reconcile the two sections. Either remove `deception-detection-reviewer` + `calibration-tracker` from Deferred (if live), or gate them explicitly in the step bodies ("skip in MVP — see Deferred"). Leave in Deferred only genuinely-unbuilt items (`source-trust-registry`, Step 12 Brier scoring, raw OSINT collection). If the deception-reviewer security gate is genuinely still open, move that caveat *into* Step 7 rather than leaving a section-vs-section contradiction.

### M3 — Step 3 conflates `evidence-ledger` (per-case) with `source-trust-registry` (cross-case) (eng reviewer)
`SKILL.md:77-79` folds `get_source_history` ("reads a source's cross-case grade record") under the `evidence-ledger` bullet. But `PIPELINE-grounded.md` explicitly defines two separate stores — `evidence-ledger` (per-case) and `source-trust-registry` (cross-case, Masterman C044) — and names `source-trust-registry` as the ⟲ store-read for step 3. Meanwhile the Deferred section (`:161-163`) says cross-case source history isn't available at MVP ("grade from present reasoning"). So Step 3 tells the agent to read cross-case history now, while Deferred says that store isn't built — direct contradiction **and** an architecture drift that erases the pipeline's two-store split.
**Fix:** Either drop `get_source_history` from Step 3 and state "source-trust-registry deferred — grade from present evidence alone" (consistent with Deferred), or, if live, name `source-trust-registry` as its own MCP matching the pipeline's per-case/cross-case split and remove it from Deferred.

---

## SHOULD-FIX

### S1 — `calibration-forecasting-reviewer` audit can silently never run (both reviewers)
Step 7 (`:114-115`) conditions this reviewer on "once a probability exists (Step 9), or now if the ranking already implies confidence" — but it lives only in Step 7's `Run:` block, and Step 9 (`:128-138`, where the probability is actually produced) never re-invokes it, nor does Step 10's gate check for it. In the common case (no confidence implied at Step 7), the pipeline-required audit (pipeline row 9: "calibrated-forecasting + subagent audits") never gets scheduled.
**Fix:** Add an explicit sub-step at end of Step 9 (e.g. "Step 9a"): invoke `calibration-forecasting-reviewer` on the completed Judgment, loop back to Step 8 on any material finding — mirroring the Step 10 human-gate loop-back pattern.

### S2 — Post-approval `log_forecast` commit is described but never scheduled as a step (eng reviewer)
Step 9's parenthetical (`:134-137`) says the probability is committed via `log_forecast` "after the human gate approves it" (i.e. after Step 10) — but this action is only an aside inside Step 9's prose; no step after Step 10 performs it. The instruction is stranded and easy to miss.
**Fix:** When `calibration-tracker` write access is on, add an explicit post-approval step (e.g. "Step 10a — after approval, `log_forecast(...)`") rather than embedding it in Step 9.

### S3 — MCP tool calls not server-qualified (skills-advisor, P056)
`:77-79`, `:86-88`, `:134-137` name bare tool ids (`add_evidence`, `score_matrix`, `log_forecast`, …). Three MCP servers are active in one workflow — exactly the ambiguity case.
**Fix:** Qualify each: `evidence-ledger:add_evidence`, `ach-engine:score_matrix`, `calibration-tracker:log_forecast`.

### S4 — Missing `## Inputs` section (skills-advisor, family-template drift)
Sibling doing-skills (`source-evaluation`, `calibrated-forecasting`) carry an explicit `## Inputs` block; this file has none. Prerequisites (existing case workspace? access to the four reviewer subagents + three MCP servers?) are never front-loaded.
**Fix:** Add a short `## Inputs` section for family consistency and to state prerequisites up front.

---

## NICE

- **N1 — Trailing Grounding recap (`:168-176`) duplicates inline per-step citations.** Family-wide habit, but this file is ~2.5× its siblings' word count (~1900 vs ~700), making it the best trim candidate — replace the recap with a one-line pointer to `PIPELINE-grounded.md`. (skills-advisor)
- **N2 — Name proximity with sibling `structured-analytic-techniques`.** Descriptions differentiate on verb (run vs review), so not a confirmed false-trigger, but near-identical names in the same `.claude/skills/` dir invite matcher/operator confusion — consider a disambiguating note or rename. (skills-advisor)
- **N3 — No `allowed-tools` frontmatter (P048).** This orchestrator calls Task + three MCP servers every run; declaring `allowed-tools` pre-approves them. Systemic across the family, low priority. (skills-advisor)
- **N4 — Citation looseness.** Step 2 (`:65`) cites Heuer C241, which the pipeline attributes to the HypothesisSet artifact-format/loop-back note, not the enumerate row (defensible, tighten). Step 9 (`:129`) allows "a numeric range"; pipeline Judgment format + Tetlock C076/C077 specify "an explicit number" — mild scope broadening. (eng reviewer)

---

MUST_FIX_COUNT: 3
