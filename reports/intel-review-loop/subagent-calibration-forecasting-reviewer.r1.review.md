# Review — calibration-forecasting-reviewer (r1)

Package: `subagents/calibration-forecasting-reviewer/` · Profile v1.0.0 · Tier 2 · 91 principles / 8 skills / 2 refs

## Gate (must-fix = FAILs)

- `validate_generated_package` → **VALIDATION PASSED** (0 FAIL). Injection-scan WARNs on `sources/markdown/*` are triage-only per untrusted-source policy, not FAILs (source text is data; benign lab-study prose).
- `quote_scan` → **PASS** (no verbatim quotation).

Gate FAILs: **0**.

## Findings (severe-first, deduped across 4 reviewers)

### HIGH-1 — over-claim: P023 promoted into always-on despite `profile_rule: false`
`profile.yaml` `knowledge_partition.always_on[2]` cites **P023** ("use causal base rates" / outside-view anchor). In `principles.yaml`, P023 has `operational_mapping.profile_rule: false` — deriver excluded it from profile content — and carries a load-bearing moral caveat ("statistically valid stereotype … discarding it has an accuracy cost even when there are good moral reasons to do so"). Profile folds it into an unqualified always-on instruction, caveat stripped → **SCOPE_BROADENED**.
Fix: drop the P023 citation + "use causal base rates" clause (P006/P007 already ground the uncaveated base-rate content); or re-derive P023 with caveat and route through profile-deriver.

### HIGH-2 — broken dispatch: adapter `description` truncated mid-clause
`.claude/agents/generated/calibration-forecasting-reviewer.md:3` — description is raw char-truncation of `when_to_use` bullets, not a summary: (1) "A team has a probability judgment, forecast;" cuts before "…or estimate and wants it reviewed for calibration…", dangling comma+semicolon; (2) "the right proper scoring" drops its noun "rule" ("…proper scoring rule, baseline, and calibration/resolution decomposition"). Router reads this string → ambiguous clause degrades routing precision. Sibling `analytic-method-reviewer.md:3` condenses cleanly.
Fix: regenerate description by summarizing 2–3 `when_to_use` bullets into short complete phrases (re-export adapter after profile edit).

### MED-1 — P025/P083 timing-excuse trap double-owned (skill + faithfulness agree)
`skills/forecast-scoring-and-evaluation/SKILL.md:114` anti-pattern cites **P025** for "off only on timing," but the timing-excuse check is owned by `forecasting-accountability-and-communication` (step 5 + anti-patterns, **P083**; `SKILL.md:66,95`), and profile `forbidden_behaviours` attributes "off on timing" to P083 (not P025). Two skills flag the same trap under different IDs → duplicate/ambiguous findings at review time. P025's actual content ("almost right" excuse) is separately mis-cited in profile.
Fix: drop "off only on timing" from the P025 bullet in `forecast-scoring-and-evaluation` (leave to P083); add a cross-ref. In `forbidden_behaviours[2]` add the correct **P025** cite for the "almost right" clause.

### MED-2 — citation-integrity slips in profile (faithfulness)
- `always_on[6]` cites **P087** (loss-aversion/golf-putting, `profile_rule: false`) with no connection to horizon/tail-risk; content grounded in P085 alone. → drop P087.
- `forbidden_behaviours[1]` cites **P003** ("more info raises confidence not accuracy") for "confidence untethered from a track record" — wrong support; actual is **P021**. → cite P021.
These are citation-integrity (SCOPE_BROADENED by mis-cite), not fabricated content.

### LOW findings
- `quality_bar[3]`: omits **P033** (motivated counterfactual selection) from cite set — content grounded elsewhere; add P033.
- `forbidden_behaviours[3]` granularity-theatre clause folds `confidence: medium` **P031** into absolute "forbidden" force — borderline HEDGING_REMOVED; consider softer phrasing.
- `forecast-scoring-and-evaluation/SKILL.md:126` References: only skill not naming sibling skills explicitly; add `forecasting-accountability-and-communication` (ties to MED-1).
- All 8 skills reference only `calibration-forecasting-principles-index.md`; second declared ref `forecasting-evidence-notes` (`profile.yaml:222-224`) is unreachable via progressive disclosure — add one pointer.
- Provenance ledger documents traceability only for load-bearing fields (`role`/`when_to_use`/`inputs`/`outputs`/`source_of_truth_policy` untagged) — matches repo convention across siblings; flag only if factory tightens repo-wide.

### Process note (not a package defect)
`reports/faithfulness-report.yaml` grounds 15 framing rules (`role`, all `when_to_use`/`when_not_to_use`, outputs, `minimum_useful_output`, `source_of_truth_policy`) to the **identical** 3 principles (P015/P006/P022) with identical boilerplate notes → those rules were not independently checked. Treat their WITHIN_SCOPE verdicts as unverified; re-run a genuine per-rule pass before relying on the report for sign-off.

## Cross-reviewer agreement
- Skill partition clean: 8 skills = exact mutually-exclusive partition of P001–P091, no gaps/dupes (skill + profile reviewers concur).
- Tool boundary clean: adapter `tools: Read, Grep, Glob`; `may_edit_canonical: false`; no escalation/scope-creep (agent reviewer).
- Version coherent: profile 1.0.0 = adapter header = ledger v1.0.0.

## Verdict
Gate green, structurally sound package. Two HIGH defects are genuine and cheap: one faithfulness over-claim (P023) + one broken dispatch string. Both warrant fix before release; MED/LOW are citation-integrity cleanups (batch with the HIGH-1 profile edit + re-export).

MUST_FIX_COUNT: 2
