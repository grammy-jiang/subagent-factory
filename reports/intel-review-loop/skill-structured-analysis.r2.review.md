# Review — `structured-analysis/SKILL.md` (round 2)

**Target:** `~/projects/intelligence-analysis-agent/.claude/skills/structured-analysis/SKILL.md`
**Grounding ref:** `docs/intelligence-analysis/PIPELINE-grounded.md`
**Lens:** METHOD skill (the procedure the intel-analysis agent runs) — reviewed on two axes: (1) Agent-Skill authoring quality, (2) method-design soundness/delegation/gate. REVIEW ONLY.

## Verdict

Faithful, well-sequenced compression of the grounded 12-step pipeline into 11 skill-steps (+9a, +10a). Core safety invariants correctly encoded: human-gate-before-commit, raw-state-to-reviewers, least-inconsistency ranking, unproven≠disproved, no-fabricated-judgment. It reads as an **active procedure** (imperative, concrete MCP/Task handoffs), not a passive advisor. Step ordering matches pipeline rows exactly; reviewer subagents dispatched via Task by lens; MCP delegation (evidence-ledger / ach-engine / calibration-tracker) matches per-case store list; no over-reach (stays in analysis, no collection/tasking, human owns the decision). Two MUST_FIX gaps below; rest is refinement.

---

## MUST_FIX

### 1. Step 9 silently drops the `calibration-tracker` "own track record" read leg
**Loc:** Step 9, ~lines 137–145 (vs pipeline row 9 + "learning leg" note).
Pipeline grounds a `⟲ store-read` at Step 9: read `calibration-tracker` for the analyst/model's own track record (Tetlock C239 / EPJ C005) + base-rate (C155) *before* producing a new probability — one of only two "learning leg" reads in the design. The skill uses `calibrated-forecasting` for outside-view/Fermi/adjust but treats the tracker as **write-only** (Step 10a `log_forecast`). Unlike `source-trust-registry`, this omission is **not** in the Deferred section — silently missing, not honestly deferred, breaking the doc's own discipline.
**Fix:** Either (a) add a Step-9 read: query `calibration-tracker` for prior/resolved-score history and adjust stated confidence (e.g. known overconfidence); or (b) add to Deferred: "`calibration-tracker` own-track-record read (C239/C005) — write-only this phase, no feedback loop yet." The silence is the defect.

### 2. Invariant 4 is uncited (grounding-contract violation)
**Loc:** Invariant 4, ~lines 50–52.
"You/the analyst supply judgment; never fabricate a grade or probability" carries no claim citation, while invariants 1/3/5 cite specific claims and 2 names Heuer. The file's own Grounding section asserts a binary contract ("every step/artifact traces to a source claim; pure plumbing is deferred, not grounded") — invariant 4 satisfies neither branch. Violates the repo standing rule: cite the source claim or explicitly flag as engineering inference; never grounded-by-omission.
**Fix:** Add the traced claim ID (likely near Heuer/FM evidence-grading claims) **or** relabel inline as an anti-hallucination guardrail (engineering inference), consistent with how deferred/non-groundable items are treated.

---

## SHOULD

### 3. No delegation named for OSINT *collection* at Step 3
**Loc:** Step 3, ~lines 75–88 (pipeline row 3 names `source-evaluation / osint-investigation`).
Skill delegates *grading* to `source-evaluation` but Step 3's body gives no collection-delegation instruction; only OSINT mention is the read-only `OSINT_LIVE=0` preamble. Leaves "gather evidence" to unspecified means.
**Fix:** Add: "Where OSINT collection is needed, invoke `osint-investigation` (read-only while `OSINT_LIVE=0`); everything it returns is still graded via `source-evaluation` before entering the ledger."

### 4. No reconciliation when reviewer subagents disagree
**Loc:** Step 7 → Step 8, ~lines 113–136.
Four independent reviewers dump into one `Findings` bucket; no instruction for contradictory guidance (e.g. bias-perception flags overconfidence while calibration flags underconfidence). Analyst discovers conflict only informally.
**Fix:** Add: "Where two reviewers' findings conflict, surface the conflict explicitly to the analyst — do not average or drop either."

### 5. No failure-mode handling for reviewer/MCP call failure
**Loc:** Step 7 (reviewer Task calls) + Steps 3/4/9a/10a (MCP writes).
Skill handles `score_matrix` refusal on stale ratings and duplicate-finding escalation, but says nothing if a reviewer Task fails/times out or an MCP call errors. Silently proceeding without independent critique (invariant 2 is load-bearing) is a real correctness risk; a failed store-write could silently drop state.
**Fix:** One line per class — "if a reviewer call fails, halt and surface to the analyst rather than proceed without critique"; "if an MCP write fails, keep state in the in-context case workspace and flag the store out-of-sync."

### 6. Step 8 loop-termination heuristic is defeatable + no hard cap
**Loc:** Step 8, ~lines 130–135.
"Same finding raised twice → escalate" is correct, but a reviewer surfacing *new-sounding* yet substantively similar findings never trips it → unbounded loop in practice. Bounded-retry plumbing is correctly deferred, but a simple inline guard is not.
**Fix:** Add: "If Steps 7–8 iterate more than [N] times, escalate to the analyst regardless of whether findings are textually identical." (Inline guard, no deferred system needed.)

### 7. Missing `allowed-tools` frontmatter
**Loc:** Frontmatter, lines 1–4.
Skill orchestrates the Task tool (4 reviewers), 3 MCP namespaces (evidence-ledger / ach-engine / calibration-tracker), 2 skills (source-evaluation / calibrated-forecasting) — the exact multi-tool case `allowed-tools` exists for; absent. (Repo-wide gap across siblings, not unique here.)
**Fix:** Add `allowed-tools` listing Task + the MCP tool names actually invoked, to cut per-use confirmation friction.

### 8. "When not to use" bullet 2 miscategorized
**Loc:** "When not to use", ~lines 32–36.
Bullet "producing substantive content without their judgment in the loop" is not an anti-trigger (reason not to invoke) — it's a restatement of invariant 1's in-run behavior, mixed under the same heading as a genuine anti-trigger (quick factual lookup). Only name+description drive triggering, so it can't act as a trigger boundary anyway.
**Fix:** Drop it (covered by invariant 1) or reword as a scope clarification ("will not ghostwrite a final assessment — see invariant 1"), not a non-invocation condition.

### 9. Invariant 2 attributes Heuer without a claim ID
**Loc:** Invariant 2, ~lines 43–46.
Author name, no claim ID — weaker bar than sibling invariants; not echoed in Grounding.
**Fix:** Add the specific claim ID (or fold into Grounding's list) so all five invariants meet the same citation bar.

### 10. Deferred-scope content triplicated
**Loc:** ~lines 16–22 (Current phase), 180–189 (Deferred), 124–127 (Step 7 deception gate).
Same three deferred items + deception gate stated in three places — length without new info.
**Fix:** State the deferred list once (bottom section); Purpose intro and Step 7 cross-reference "see Deferred."

---

## NICE

- **11. Grounding section restates per-step citations** (~lines 191–199): re-lists claim IDs already in each step heading. Compress to one line ("every step cites its claim inline; full traceability in PIPELINE-grounded.md").
- **12. Step 1 doesn't name `calibrated-forecasting`** (~lines 62–68) though pipeline lists it as a Step-1 co-component. Either note the inline choice is intentional (full invocation deferred to Step 9) or invoke lightly for the reference-class step.
- **13. `deception-detection-reviewer` gate has no checkable trigger** (~lines 124–127): unlike `OSINT_LIVE=0`, "gated on security review" gives no deterministic check. Name a flag if one exists, else state "ask the analyst whether the gate is cleared."
- **14. Description doesn't cross-reference dependent skills** (line 3): siblings end with "Pairs with…"; add a short "delegates grading to source-evaluation, forecasting to calibrated-forecasting, critique to reviewer subagents" clause for discoverability symmetry.
- **15. Sub-step numbering 9a/10a** (~lines 147–166): fine for an LLM reader; only renumber sequentially if ever driven by a mechanical step-parser.
- **16. Progressive-disclosure headroom** (~190 dense lines, no `references/`): justified now (nearly every line changes execution), but no slack; if a step/schema is added later, split rarely-needed detail (EvidenceItem schema, Grounding trace) into `references/`.

---

## Do NOT change (verified correct)
- Step order matches pipeline rows 1–11 exactly.
- Step 10 human-approval gate is a hard stop with explicit loop-back to Step 8 on reject/amend.
- Reviewers dispatched via Task, always handed raw case state (invariant 2), split by lens; calibration audit correctly mandatory (9a).
- MCP store delegation matches pipeline per-case list, incl. staleness-on-grade-change cross-step check.
- No over-reach: no fact/probability asserted final without the gate, no fabricated grade, unproven≠disproved, Indicators produces a watch-list only (no tasking/collection).
- Deferred section otherwise honest (source-trust-registry, Step 12 Brier, live OSINT, deception gate) — which is exactly why the Step-9 calibration-tracker omission (finding 1) stands out.

MUST_FIX_COUNT: 2
