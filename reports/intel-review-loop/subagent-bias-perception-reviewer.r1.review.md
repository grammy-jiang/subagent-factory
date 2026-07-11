# Review — subagents/bias-perception-reviewer (round 1)

Package: `subagents/bias-perception-reviewer/` · profile v1.0.0 · 200 principles / 10 skills / 2 refs / 6 sources
Reviewers: agent-skills-advisor, profile-reviewer, faithfulness-reviewer, ai-agent-engineering-reviewer

## Bash gate (authoritative — FAILs = must-fix)

- `validate_generated_package` → **VALIDATION PASSED** (exit 0). Only 2 `[WARN] injection-scan` on
  `sources/markdown/thinking-fast-and-sl-*.md` (fake-completion / role-override) — triage-level, expected
  where Kahneman's text quotes prompt-style examples; policy = quarantine/escalate, not hard-block. Not a FAIL.
- `quote_scan` → **PASS** — no potential verbatim quotation.

**No gate FAILs.** All findings below are quality nits, none blocking release.

## Findings (severe-first)

### MED

1. **Faithfulness report has a coverage gap on the load-bearing rules** — `reports/faithfulness-report.yaml`
   verifies `role`, `when_to_use`, `when_not_to_use`, `quality_bar`, `forbidden_behaviours`,
   `minimum_useful_output`, `outputs.primary_format`, but has **zero entries for
   `knowledge_partition.always_on[0-9]`, `handoff_rules`, `source_of_truth_policy.precedence`, and
   `examples[].ideal_response`** — roughly a third of the rule surface, and the always_on bullets are what
   actually drive the always-on skill layer. Independent hand-check found these clean (hedges preserved: "only",
   "can", "may"; no SCOPE_BROADENED/HEDGING_REMOVED/CONTRADICTED), so the report's "no rule stronger than its
   evidence" claim is *true but unverified* for that third. Fix: extend the report with explicit verdicts for
   those fields. (faithfulness-reviewer)

2. **`outputs.modes[compare].output` wording is ambiguous against the no-substantive-judgment guardrail** —
   "…ending in a recommendation and the residual uncertainty" doesn't state *what* the recommendation is *of*;
   read in isolation it can be misread as recommending which interpretation is *true*, which `role` /
   `forbidden_behaviours` forbid. Behaviorally mitigated (forbidden_behaviours + both examples + 66 compare PB
   tests all constrain it), so wording gap only. Fix: qualify like `advise` does, e.g. "…a recommendation on
   which interpretation's reasoning holds up better, not which is true, and the residual uncertainty."
   (profile-reviewer)

3. **Profile body word count near WARN threshold** — manual sum of the fields `profile_self_check.py` counts
   (~840w) is over the 800w WARN line (under the 1000w FAIL line; gate did not FAIL). Verify with
   `python -m tools.subagent_factory.profile_self_check subagents/bias-perception-reviewer`; if confirmed, trim
   `quality_bar` / `outputs.modes` (heaviest sections). (profile-reviewer)

4. **Three high-principle skills overload individual Procedure steps** —
   `deterrence-spiral-and-strategic-interaction`, `perception-attribution-of-intent-and-signaling`,
   `motivated-reasoning-and-belief-perseverance` (25/37/25 principles) compress 3–4 distinct principle-cited
   checks into single dense numbered steps (e.g. deterrence step 6, perception-attribution step 6), hurting
   scannability vs the one-check-per-step pattern in the other 7 skills. Content accurate/grounded. Fix: split
   overloaded steps into one sub-step (or sub-bullet) per mechanism. (agent-skills-advisor)

### LOW

5. **Adapter router `description` is truncation-clipped, loses sibling-disambiguation terms** — export's
   per-clause `max_chars` cap drops the back half of the Use-when/Not-for clauses (e.g. "…perceptual" cut before
   "distortion") and omits the calibration `when_to_use` bullet — the one that overlaps
   `calibration-forecasting-reviewer` — so the one-line router signal doesn't show where the two subagents
   diverge. Body's full When-to-use/When-NOT sections are complete/correct; this is generator behavior shared by
   sibling adapters, not a profile defect. Fix (optional): raise the clause cap or reorder `when_to_use` so
   differentiating terms land before the cut. (ai-agent-engineering-reviewer)

6. **`compare` mode has no golden-test coverage** — all 6 `golden-tests.yaml` entries use `expected_mode:
   review`/`advise`; `compare` has principle-level PB coverage but no end-to-end routing test. Fix: add one
   `golden_tests` entry with `expected_mode: compare` (adapt an existing compare PB prompt). (profile-reviewer)

7. **`provenance-ledger.md` grounding table omits `handoff_rules`** — the "Field → grounding" table lists role /
   quality_bar / forbidden_behaviours / always_on but not `handoff_rules`, though the profile cites P008/P086
   inline for it (not an orphan — citation exists). Fix: add a `handoff_rules | P008, P086` row. (profile-reviewer)

8. **Citation padding in two always_on bullets (traceability, not strength)** — always_on bullet 4 cites P078/
   P086/P122/P152/P156/P197 but its text only paraphrases P083/P085/P155/P192; `handoff_rules[1]` cites P008
   (thorough collection doesn't improve accuracy) for a data-handoff claim P008 doesn't literally support. No
   over-claim; loosely-matched IDs just aren't traceable to the specific assertion. Fix: drop the unused IDs or
   add a supporting excerpt when the faithfulness report is extended (finding 1). (faithfulness-reviewer)

9. **Three skill descriptions drift from the sibling "Audits X; invoke when Y" pattern** —
   `mind-sets-and-structured-techniques` opens imperative-first ("Invoke to audit…");
   `dual-process-heuristics-and-cognitive-ease` and `judgment-anchoring-and-base-rates` omit the explicit
   "invoke when…" trigger clause the other skills carry. Still third-person, no first-person. Fix: reword to
   match sibling shape / append a short trigger clause. (agent-skills-advisor)

## Verdict

No BLOCKER/HIGH, no gate FAIL. Release not blocked. Highest-value pre-export fixes: #1 (close the faithfulness
coverage gap on always_on/handoff) and #2 (tighten compare-mode output wording). Rest are cosmetic/consistency.

MUST_FIX_COUNT: 0
