# Review r3 — calibration-forecasting-reviewer

Package: `subagents/calibration-forecasting-reviewer/` (profile v1.0.2)
Pass: single review pass, 4 parallel reviewers (skills / profile-release / faithfulness / agent-design) + deterministic gates. REVIEW ONLY.

## Gate results (deterministic)

- `validate_generated_package` → **VALIDATION PASSED**. Only WARN-level output: prompt-injection scan hits on `sources/markdown/{superforecasting,thinking-fast-and-sl}.md` — all benign source prose (Bayesian/psychology passages), triage-not-block per `untrusted-source-policy`. No FAIL.
- `quote_scan` → **PASS** — no potential verbatim quotation. All 6 sources `distillation-only`, clean.

No gate FAIL → no gate-derived must-fix.

---

## MUST-FIX (blocks release — repo-rule violations)

### M1 — `forbidden_behaviours[2]` over-claims vs P025/P086 (HEDGING_REMOVED)
`profile.yaml` `forbidden_behaviours[2]` bans scoring "almost right"/"off on timing" as success as an **unqualified flat rule**. Source principles are graduated/proportional: P025 penalizes the "almost right" excuse *"in proportion to how rarely the same forecaster admits being merely lucky when right"*; P086 grants *"only a small fraction of the credit"* discounted by selective invocation. The sibling clause `knowledge_partition.always_on[7]` states this correctly ("discount... in proportion to how selectively it is invoked") — the two clauses contradict each other in-profile. Violates `evidence-protocol` faithfulness rule (rule stronger than source support).
**Fix:** reword to proportional/"never grant full credit" phrasing (reuse `always_on[7]` language); apply `add_condition` in the faithfulness report as already done for `forbidden_behaviours[3]`/P031.
*(faithfulness-reviewer #1; MED severity there, elevated — direct faithfulness-rule breach.)*

### M2 — `reports/faithfulness-report.yaml` grounding is templated + mis-attributed + truncated
Three compounding defects in the faithfulness report, independently found by profile-reviewer and faithfulness-reviewer. Violates `rights-and-quotation-policy` ("every profile field traceable to a source+QID; no orphan field values") and the ledger's own claim (`provenance-ledger.md:53-61`) that every rule was per-field verified.
- **Boilerplate:** ~14–17 findings (`role`, `when_to_use[0-4]`, `when_not_to_use[0-2]`, `inputs.required[0]`, `outputs.primary_format`, all three `outputs.modes[*].trigger`, `minimum_useful_output`, `source_of_truth_policy.precedence`) carry byte-identical citation `P015/P006/P022` regardless of field content.
- **Factually wrong citations:** `when_to_use[3]` (cognitive-trap trigger) has no relation to P015/P006/P022 (scoring/base-rate/Bayesian) — should cite the cognitive-bias family. `when_not_to_use[0]` / `forbidden_behaviours[0]` / `handoff_rules[0]` ("does not make the decision / supply the estimate") are grounded to **P039**, whose actual statement is about defining good judgment / measurement progress — no role-separation content. Correct grounding is P039→(replace); the identical-content `forbidden_behaviours[0]` two sections down cites the right principle.
- **Truncated grading:** multi-citation rules grade only the first 3 IDs. E.g. `quality_bar[3]` cites 8 (P008,P020,P038,P034,P057,P016,P045,P033), graded on 3; `forbidden_behaviours[2]` cites 6, graded on 3; all 8 `always_on` rules (one cites 14 IDs) graded on 3. Majority of cited support never independently checked, yet ledger asserts exhaustive coverage.
**Fix:** re-derive per-field citations content-specifically; for pure scope/role/IO-shape rules that aren't literal source claims, mark "design decision, not source-derived" instead of implying uniform principle grounding; extend each finding to cover every cited ID (or explicitly label sampled). Correct `provenance-ledger.md:53-61` coverage prose.
*(profile-reviewer BLOCKER+HIGH+MED; faithfulness-reviewer #2+#3.)*

---

## HIGH (strongly recommended; not gate-blocking)

### H1 — Cross-agent routing overlap with `analytic-method-reviewer`
Both siblings installed in `.claude/agents/generated/` claim the same calibration/outside-view/base-rate/coherence/aggregation territory and share 4 of 6 source books. `analytic-method-reviewer` frontmatter explicitly says "forecast" and covers calibration. Neither package's `when_not_to_use`/`handoff_rules` names the other or draws a boundary — auto-router has no reliable signal.
**Fix:** add reciprocal disambiguation (calibration-forecasting = probability/scoring discipline; analytic-method = hypothesis structuring / structured-technique choice) to both packages' `when_not_to_use`/`handoff_rules`. Cross-package change — needs user decision.
*(ai-agent-engineering-reviewer #1.)*

---

## MED

- **MED-1** `profile.yaml` always_on bullets drift from skills: "outside view" bullet omits **P023** taught by `base-rates-outside-view-and-regression`; "horizon/tail" bullet omits **P087** taught by `scenarios-horizon-and-tail-risk`. Both are `profile_rule:false` (correctly dropped from always_on runtime per ledger) and appear in the reference index — so this is a summary-digest drift, not a runtime bug. Confirm intended; if the always_on prose is meant to digest the skill, add them. *(skills-advisor ×2 — reclassified: these are the intentionally-dropped P023/P087 per profile-reviewer's clean-check, so LOWER than the reviewers rated.)*
- **MED-2** Operating-invariants section in adapter (`:21-188`, ~80 principles) marked "take precedence over softer guidance," but ~80 of ~91 principles are invariants vs 5 quality-bar bullets — invariant/guidance distinction loses signal. **Fix:** curate a small hard-invariant set (no default 0.5; cap certainty short of 1.0/0.0; multiply not average conjunctions; enforce coherence); push rest to quality-bar/skills. *(ai-agent #2.)*

## LOW

- **L1** `forecasting-accountability-and-communication/SKILL.md:3` description states disambiguation twice ("(not the math)" + "not the proper-scoring arithmetic... which forecast-scoring-and-evaluation owns"). Drop the redundant "(not the math)". *(skills #3.)*
- **L2** `role` prose (`profile.yaml:10-18`) names Tetlock without co-author Gardner though `sources` lists both. → "Tetlock (with Gardner)". *(profile-reviewer LOW.)*
- **L3** "accountability" used two ways: `when_to_use[5]` = forecast/tournament scorekeeping (in-scope) vs `handoff_rules` = organizational accountability design (out-of-scope); no distinguishing test. Qualify the handoff term. *(ai-agent #3.)*
- **L4** Adapter frontmatter "Not for" (`:3`) states only 1 of 3 exclusions; auto-router weights frontmatter heaviest. Consider adding "or a deterministic/non-uncertainty question." Note: pattern matches sibling adapter — likely template convention. *(ai-agent #4.)*
- **L5** `references/forecasting-evidence-notes` declared package-wide but only linked from `forecast-scoring-and-evaluation`; other 7 skills reach only the principles-index. Scope its declared name or link from skills whose principles it documents. *(skills #4.)*
- **L6** advise/compare mode-shaping spelled out only in `calibration-and-probability-hygiene/SKILL.md` Output; other 7 skills describe review-mode shape only. Add one line each or state once package-level. *(skills #5.)*
- **L7** "do not invent the missing input" boundary present only in `base-rates-outside-view-and-regression`; add matching one-liner to skills with real invent-vs-defer risk (forecast-scoring, cognitive-bias). *(skills #6.)*
- **L8** 3 longest skills (calibration-and-probability-hygiene 306L, cognitive-bias-and-mindset-control 272L, scenarios-horizon-and-tail-risk 261L) duplicate reference-index rationale inline; tighten Procedure to imperative+citation. *(skills #7.)*
- **INFO** No `self_check` profile field exists anywhere in schemas — repo-wide gap already noted r2 (#13); `quality_bar`+`minimum_useful_output` serve equivalent. Not a per-package blocker.

---

## Confirmed clean (cross-checked)

Tool boundary `Read,Grep,Glob` only (no Write/Edit/Bash/MCP), consistent adapter↔profile. Adapter version 1.0.2 = `agent_version` (no drift). DO-NOT-EDIT header present. Advisory stance enforced structurally (role + forbidden_behaviours + both worked examples decline to supply the forecast). All 8 skills present, 1:1 with profile, valid frontmatter names, uniform template, four-part finding shape matching `outputs.primary_format`. All P001–P091 cited IDs exist in principles.yaml. r2 fixes verified applied (P031 hedge, version history, golden-tests profile_version). All 6 sources `distillation-only` with well-formed sha256.

MUST_FIX_COUNT: 2
