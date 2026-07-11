# Review R1 — subagent `deception-detection-reviewer`

**Package:** `subagents/deception-detection-reviewer/`
**Pass:** single review pass, REVIEW ONLY (no edits applied)
**Date:** 2026-07-11

## Gate (deterministic — blocking)

| Gate | Result |
|------|--------|
| `validate_generated_package` | **PASS** (0 FAIL; 1 informational "phase8 self-check WARNING" inside an OK line — body ≈931w > 800 soft budget, < 1000 hard fail → not release-blocking) |
| `quote_scan` | **PASS** — no verbatim quotation |

No gate FAILs. All must-fix items below come from the four scoped reviewers, not the gate.

## Reviewers run (parallel)

agent-skills-advisor (skills) · profile-reviewer (release-readiness) · faithfulness-reviewer (over-claim) · ai-agent-engineering-reviewer (agent design).

---

## MUST-FIX (BLOCKER / HIGH) — severe first

**M1 [HIGH · faithfulness] Fabricated clause with no source — `profile.yaml` `knowledge_partition.always_on` bullet 5 ("Govern and organize").**
Clause "watch the champion who is slow to see undermining evidence" cited `(P006,P016,P017,P025,P027,P028,P033,P042,P049,P056,P076,P079,P092)`. grep of `principles.yaml`, `claims.jsonl`, `evidence-records.yaml` for "champion"/"undermin" → **nothing**. Invented content wearing a citation list. Worse than SCOPE_BROADENED.
Fix: remove, or replace with genuinely-grounded content (e.g. P056 "members subordinate their department's interest to the common goal"). Action = `reject`/`remove`, never `accept_with_note`.

**M2 [HIGH · faithfulness] Fabricated clause with no source — `always_on` bullet 8 ("Detect deception / mirror").**
Clause "cap certainty short of the endpoints so evidence can still move you" cited `(P011,P045,P048,P050,P059,P070,P074,P077,P078)`. grep-confirmed absent from all three source files. Reads like calibration boilerplate carried from a sibling package, not from Masterman.
Fix: remove or replace; P070's mirror discipline already covers the epistemic-humility intent without an invented numeric-certainty frame.

**M3 [HIGH/BLOCKER · faithfulness] Faithfulness-report coverage gap let M1/M2 hide — `reports/faithfulness-report.yaml`.**
Report reviews only `role`, `when_to_use`, `when_not_to_use`, `quality_bar`, `forbidden_behaviours`, `minimum_useful_output`, `outputs.primary_format`, `handoff_rules` (22 findings). **Zero** findings for `knowledge_partition.always_on` (8 dense per-invocation bullets — the actual applied content), `source_of_truth_policy.precedence`, or `outputs.modes` triggers. Exactly where M1/M2/M5 live, unreviewed.
Fix: add rule_ref entries for each `always_on` bullet, `source_of_truth_policy`, and each mode trigger before this is treated as faithfulness-reviewed. (Cross-check: all 22 *existing* findings are genuine WITHIN_SCOPE/EXACT_SUPPORT — no accept_with_note/SCOPE_BROADENED mislabels among reviewed rules. Risk is entirely the unreviewed block.)

**M4 [HIGH · agent-design] Garbled router description — `.claude/agents/generated/deception-detection-reviewer.md:3`.**
Description cut mid-word: `"...grounded in J — Use when: ..."`; drops "C. Masterman's history of Britain's WWII double-agent system." This is the one field the Task-tool router reads to route to this subagent.
Root cause traced: `profile.yaml:11` role = "...grounded in J. C. Masterman's history..."; exporter `_clean_clause` (`tools/subagent_factory/export_claude_agent.py:207`, `text.split(". ")[0]`) treats the `"J. C."` abbreviation as the first-sentence boundary.
Fix: reword `profile.yaml` role so no internal `". "` precedes the intended sentence end (e.g. lead with the WWII double-agent system; write "J.C. Masterman" or "the Masterman history"), then re-export. Generator-owner flag (out of package scope): make `_clean_clause` abbreviation-aware — recurs for any author with a middle initial.

**M5 [HIGH · profile] Orphan field value — `profile.yaml:142-146` `source_of_truth_policy.precedence`.**
Substantive tradecraft priority rule ("network security governs unless specific evidence justifies the risk; ... never endorse a control/trust claim more confident than the source supports") carries **no `(Pxxx)` citation**, unlike every other load-bearing field. Violates evidence-protocol / rights-and-quotation hard rule ("every profile field traceable to a source + QID").
Fix: cite grounding principle ID(s) (e.g. from `network-security-and-compartmentation` or `strategic-stewardship-and-timing`), or move uncited half into meta-language that asserts no specific tradecraft ranking.

**M6 [HIGH · skills] Systemic triple-restatement of the flaw taxonomy — all 8 `SKILL.md`.**
Each skill enumerates the same 7-10 flaw types three times (numbered Procedure w/ Pxxx → parenthetical list in `## Output` → bullets in `## Anti-patterns`) then a 4th principle-id list in `## Provenance`. Exactly the triple-redundancy the quality bar forbids (P088/P114); inflates each body to ~150-210 lines. E.g. `assessing-enemy-trust-and-belief/SKILL.md:67-106` vs `:125-139` vs `:141-161`.
Fix: keep `## Output` a short generic contract (name flaw / apply correction / state residual uncertainty / next step); let `## Anti-patterns` be the single canonical concrete list; drop the flaw-name parenthetical from Output.

---

## SHOULD-FIX (MEDIUM)

**S1 [profile] `physical-and-technical-deception-craft` skill has zero quality-bar/forbidden coverage** — none of 5 `quality_bar` items, `forbidden_behaviours`, or `handoff_rules` cite its principles (P018,P037,P041,P044,P046,P081,P082,P084,P085). 1 of 8 skills / 9 of 94 principles untested by any profile-level check — a review could pass without ever checking planted-personality / site-selection / sabotage-staging. Fix: add/extend one `quality_bar` bullet citing that skill.

**S2 [agent-design] Dangling citation `P089`** — `.claude/agents/generated/deception-detection-reviewer.md:221,231` (quality-bar + forbidden) cite P089, but in-file "Operating invariants" defines only P001–P044, P049–P070. Agent reading only its own prompt cannot resolve P089. Fix: promote P089 into invariants block, or replace with a defined invariant, or note that citations may reference the broader corpus via linked skills. (Note: profile-reviewer confirms P089 *does* resolve in `provenance-ledger.md` — so this is an adapter-rendering gap, not an orphan.)

**S3 [faithfulness] Block-citation drift** — `knowledge_partition` bullets cite 9-13 principle IDs per whole bullet, misaligned with text: P001 (controlled-sabotage) cited under "Turn/run controlled agent" but its content belongs under bullet 7 (physical craft); P076 cited under governance but text sits in the mirror bullet. This block granularity is *how* M1/M2 escaped. Fix: tighten to clause-level citations.

**S4 [skills] Frontmatter description voice — all 8 `SKILL.md:3-5`** — open imperative/2nd-person ("Review X..."; one drifts to "whether **you** are...") not conventional 3rd-person ("Reviews X..."); all 8 close with identical non-discriminating tail "use when reviewing this facet of a deception or counter-deception case" (zero added trigger signal). Fix: 3rd-person + skill-specific trigger clause (draw from each skill's own "When to use" bullets).

**S5 [skills] No worked input/output example in any skill body — all 8** (`## Inputs`/`## Output`, abstract only). P014 expects per-skill input/output examples; profile carries examples only at whole-subagent altitude. Fix: add one short 2-4 sentence worked example per skill instantiating the Output contract on a toy case.

**S6 [profile] Body ≈931 words > 800 soft budget** (`profile.yaml`; heaviest `quality_bar` :88-108 ~183w, `when_to_use` :20-35 ~112w, `role` :10-18 ~107w). Not release-blocking (<1000 hard fail) but is the source of the phase8 WARNING. Fix: trim `quality_bar`/`when_to_use` prose into skills.

---

## NICE-TO-HAVE (LOW)

- **L1 [faithfulness] Hedge dropped** — `always_on` bullet 8 uses "measured by the absence of enemy activity"; P059 says "measure success **partly** by the absence...". Mild HEDGING_REMOVED. Restore "in part".
- **L2 [skills] Body verbosity** — bodies long for single facets (e.g. `physical-and-technical-deception-craft/SKILL.md:1-197`); mostly resolves as side-effect of M6.
- **L3 [skills] `advise`/`compare` modes have no skill-level procedure** — `profile.yaml:66-86` promises both, but all 8 `## Procedure` are review/audit-only. Add a mode-adaptation note to the skills most likely invoked in those modes.
- **L4 [agent-design] Invariants numbering gap P044→P049** (`.md:112-114`) skips P045-P048 with no marker — reads as generation error. Add one-line "curated subset" note or omit numbering.
- **L5 [profile] Ledger auditability** — `provenance-ledger.md` documents coverage at skill granularity only; doesn't list which claim/evidence IDs back each `quality_bar`/`forbidden` bullet (had to hand-verify). Tighten for auditability.

## Confirmed-clean (no action)

- Tool boundary correct: adapter `tools: Read, Grep, Glob` — exactly the read-only set, no Write/Edit/Bash over-reach.
- Authority scope correct: role + `when_not_to_use[0]` + `forbidden_behaviours[0]` + `handoff_rules[0]` all deny running the operation / making the command decision / certifying a channel. Required "does not run the op" exclusion present and reinforced 4×.
- All 8 `knowledge_partition.skills` entries match the 8 skill dirs; all 2 references authored. No truncation, no orphan skill/reference names.
- Skills consistently hold review altitude — every procedure step phrased "check/test/confirm", never "perform the deception"; every `## Output` hands go/no-go back to case owner.
- Scope caveat (wartime-conditions, medium-confidence = guidance) documented in ledger — resolved, not open conflict.

## Not verified (out of scope this pass)

- `tests/golden-tests.yaml` counts (Phase-8 check 18: 3+ golden, 1+ negative-routing) — confirm before final release sign-off.

MUST_FIX_COUNT: 6
