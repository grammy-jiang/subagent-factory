# Review — analytic-method-reviewer (r3, single pass)

Package: `subagents/analytic-method-reviewer/`
Date: 2026-07-11
Verdict: **RELEASE-READY.** Zero must-fix. All findings MEDIUM/LOW polish.

## Bash gate (must-fix source)

- `validate_generated_package` → **VALIDATION PASSED** (only WARNs: injection-scan on `sources/markdown/thinking-fast-and-sl-*.md`, benign source-content flags, not adapter defects).
- `quote_scan` → **PASS** — no verbatim quotation.
- `profile_self_check` (run to close two flagged items) → **PASS**: check-14 body-size ~800 words; check-18 golden = 6 golden + 4 negative routing.

No gate FAILs → **no must-fix**.

## Reviewer verdicts

| Lens | Result |
|------|--------|
| Agent design (tool boundary / scope / routing / self-containment) | **CLEAN — 0 findings** |
| Faithfulness (over-claim) | 2 MEDIUM + 1 LOW, no BLOCKER/HIGH |
| Skill authoring | 1 MEDIUM + 3 LOW, no BLOCKER/HIGH |
| Profile release-readiness | 1 MEDIUM (+ 2 items resolved by self-check) |

## Findings (severe-first, deduped)

### MEDIUM-1 — Faithfulness report coverage gap: `knowledge_partition.always_on[0–6]` never reviewed
`reports/faithfulness-report.yaml` has 21 findings covering role/when_to/quality_bar/forbidden/outputs/min-output but **zero** `rule_ref` for `knowledge_partition.always_on[0]–[6]`, `handoff_rules[0-1]`, `source_of_truth_policy.precedence`. `always_on` is imperative rule text → in scope. Principles cited there for the first-and-only time (P009, P015, P022, P026, P032, P035, P039, P050, P051, P053, P058, P064, P065) were never over-claim-checked.
**Fix:** add faithfulness findings for `always_on[0]–[6]` (+ handoff_rules, precedence); verify each newly-cited principle vs `principles.yaml`.

### MEDIUM-2 — Possible HEDGING_REMOVED in `always_on[1]`, uncaught because unreviewed (subset of MEDIUM-1)
`always_on[1]` restates the ACH rule but drops the "key issue where cost of error is high or deception a serious possibility" qualifier that `forbidden_behaviours[1]` correctly preserves (matches P010 `applies_when`). If `always_on` = "apply on every review," this is HEDGING_REMOVED vs P010 → needs `add_condition`. If it only means "knowledge stays loaded," it's naming semantics, not a violation. Ambiguity unresolved because the block was never reviewed.
**Fix:** resolve within MEDIUM-1; if apply-semantics, add the cost-of-error/deception condition.

### MEDIUM-3 — Skill Procedure ↔ Anti-patterns systemic redundancy (all 9 skills)
Every `## Anti-patterns to flag` bullet restates a flaw + same principle IDs already in a `## Procedure` step, reworded. E.g. `cognitive-biases-and-dual-process-reasoning/SKILL.md:77-81` vs `:143-145` (P009/P051); same in `assumptions-framing-and-analytic-writing/SKILL.md:64-89` vs `:115-122`; `mindsets-schemata-and-perception/SKILL.md:69-99` vs `:134-144`; + 6 more. ~2x token footprint per file, cuts against concise-skill bar (P088).
**Fix:** drop Anti-patterns and let numbered Procedure serve as scan list, OR compress Anti-patterns to a one-line-per-flaw table cross-referencing the procedure step number.

### MEDIUM-4 — provenance-ledger field→grounding table incomplete (orphan fields)
Ledger table (lines 28-38) grounds only role/quality_bar/forbidden/always_on. No row + no citation for: `when_to_use`, `when_not_to_use`, `inputs.required`, `outputs.primary_format`/`modes`, `minimum_useful_output`, `handoff_rules[1]`, `source_of_truth_policy.precedence`. Rights-policy requires every field traceable to source+QID. Likely structural/scope fields inheriting `role`'s grounding (P013/P052/P057), but implicit.
**Fix:** doc-only — add ledger note (same pattern as `handoff_rules[0]` self-declaration) stating these are scope/output-shape fields inheriting role grounding; or add citation rows if any embed a substantive claim.

### LOW-1 — Weak/mismatched citation in `forbidden_behaviours[2]`
Cites P052, P008, P046. P008 = devil's-advocate backfire, does NOT support "guarantee against error." WITHIN_SCOPE verdict fine (P052 carries it), but P008 mis-grounds.
**Fix:** drop P008 or replace (e.g. P065 formula-override caveat).

### LOW-2 — H1 title inconsistency
`perception-misperception-and-signaling/SKILL.md:34` uses commas ("Perception, Misperception, and Signaling"); other 8 comma-free Title Case.
**Fix:** drop commas.

### LOW-3 — Name lexical overlap `mindsets-schemata-and-perception` vs `perception-misperception-and-signaling`
Both contain "perception" → thinner routing margin for keyword/embedding matcher. Frontmatter prose disambiguates adequately ("analyst's own schemata" vs "how adversary reads our signals") → not a routing failure.
**Fix (optional):** rename one, e.g. `adversary-perception-and-signaling`.

### LOW-4 — Skill bodies lack "When NOT to use" heading
Disambiguation lives only in frontmatter description + References footer. Correct per tier-1-description routing (P002), but a one-line body bullet would help human skim.
**Fix (optional):** add short "When NOT to use" under each Purpose.

## Resolved during this pass (no action)
- Profile body-size margin (~800w) — self-check **PASS check-14**.
- Golden/negative-routing tests — self-check **PASS check-18** (6 golden, 4 negative).
- P080 quality_bar reference outside Operating-Invariants list — established factory pattern, defined in `references/analytic-method-principles-index.md:178`, not a broken ref.

MUST_FIX_COUNT: 0
