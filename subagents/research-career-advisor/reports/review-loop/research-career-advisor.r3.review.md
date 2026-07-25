# research-career-advisor — Review Loop Round 3

Consolidated review of `subagents/research-career-advisor/` (v1.2.0). Four reviewer lenses
(agent-skills-advisor, profile-reviewer, faithfulness-reviewer, ai-agent-engineering-reviewer)
plus deterministic gates. Findings deduped, most-severe first.

## Deterministic gates

| Gate | Result |
|------|--------|
| `validate_generated_package` | **PASS** (0 FAIL) |
| `quote_scan` | PASS |
| truncation (`…` / severed invariant) | clean |
| `profile_self_check` body-size (check 14) | WARNING (992w > 800; FAIL threshold is >1000 — **not** a FAIL) |
| injection-scan | 7 WARN, all benign frozen-source Hamming prose ("you are now at the lower levels…") — correctly triaged, not must-fix |

Deterministic FAILs: **0**.

---

## MUST-FIX

### 1. `forbidden_behaviours[2]` cites P026 as false grounding
- **Where**: `profile.yaml` `forbidden_behaviours[2]` — "Giving binding legal, financial, contractual, visa or immigration, or HR advice… (P026)."
- **Problem**: P026 is entirely about negotiating a result-oriented start-up package (space, equipment, workload relief, costs, confirm in writing). It says nothing about refusing legal/immigration/HR advice. `reports/faithfulness-report.yaml` marks this `WITHIN_SCOPE` / "Restates P026" — it does not restate P026. Highest-stakes instance: a legal/immigration no-advice boundary presented as source-grounded when it is not. (Note: the boundary itself is correct and appropriately restrictive — the defect is the false citation/traceability, not the safety behaviour.)
- **Fix**: relabel as structural house-policy (as `handoff_rules` already labels its sibling-referral note "structural house-policy, not principle-derived") and drop the `(P026)` citation, or cite an actual grounding claim from the evidence records. Update the faithfulness-report entry to match.

### 2. `forbidden_behaviours[1]` cites P010/P021 as false grounding
- **Where**: `profile.yaml` `forbidden_behaviours[1]` — "Making or predicting a hiring, admission, funding, or tenure outcome… (P010, P021)."
- **Problem**: P010 is the adviser-selection tie-break (established reputation vs. protection factors); P021 is postdoc-position selection criteria. Neither grounds a rule about refusing to predict/guarantee outcomes. Faithfulness-report again marks `WITHIN_SCOPE`/"Restates P010/P021" incorrectly.
- **Fix**: same as #1 — relabel structural or correct the citation; sync the faithfulness-report entry.

---

## SHOULD-FIX

### 3. `forbidden_behaviours[0]` cites P017/P013 as false grounding (same pattern as #1/#2)
- **Where**: `profile.yaml` `forbidden_behaviours[0]` — "Producing the research output… (P017, P013)."
- **Problem**: P017 = milestone decomposition; P013 = dissertation coherence. Neither grounds "advisor must not do the work." The profile's own `role` states the advice-only boundary is structural and "take[s] precedence over every invariant" — so citing principles as its source is internally inconsistent. Lower severity than #1/#2 (not a legal/outcome boundary) but same defect family.
- **Fix**: relabel structural or correct citation.

### 4. `handoff_rules[1]` repeats the P026/P010 mis-citation
- **Where**: `profile.yaml` `handoff_rules[1]` — "…legal, financial, contractual, and immigration questions… (P026, P010)."
- **Problem**: duplicates the false grounding of #1/#2 in referral form.
- **Fix**: remove/correct citation, mark structural. Fix together with #1–#3.

### 5. `knowledge_partition.skills[2]` broadens P034 out of its scope (SCOPE_BROADENED)
- **Where**: `profile.yaml` `knowledge_partition` bullet for `choosing-advisers-groups-and-positions` — "…a laboratory's management of priorities, resources, performance… (P010, P011, P021, P024, P033, **P034**)."
- **Problem**: P034's `applies_when` is scoped to an **industrial or government laboratory** / managed research environment. The bullet presents it as a general adviser/group/postdoc-evaluation heuristic with no such qualifier. Never checked because the faithfulness-report does not review `knowledge_partition`.
- **Fix**: add the source qualifier (e.g. "particularly in an industrial or government lab") or split so the P034 claim is not blended with the academic-adviser claims.

### 6. Faithfulness-report coverage gap
- **Where**: `reports/faithfulness-report.yaml`.
- **Problem**: reviews only `quality_bar`, `forbidden_behaviours`, `when_to_use`, `outputs.primary_format`, `handoff_rules`, `precedence`. It never checks `knowledge_partition.always_on`/`skills[*]` (the 8 paragraphs that drive the skills), `examples`, `role`, `router_description`, or `when_not_to_use`. Finding #5 exists because that content was never checked. Current PASS certifies only a minority of substantive claims.
- **Fix**: extend the report to include `knowledge_partition.skills[*]` bullets as first-class `rule_ref` entries.

### 7. Profile body over the 800-word budget (WARNING, not FAIL)
- **Where**: `profile.yaml` body (992w; heaviest `quality_bar` 194w, `when_not_to_use` 137w, `when_to_use` 123w).
- **Problem**: v1.1.0/v1.2.0 added `when_not_to_use` + `handoff_rules` entries without a compensating trim; now 192w over the 800 WARNING budget (still under the 1000 FAIL threshold — non-blocking).
- **Fix**: trim while doing #1–#4 — dropping the false citations already removes words; also tighten `quality_bar[2]`'s run-on and the near-duplicative v1.1/1.2 sibling-routing bullets.

### 8. `quality_bar[1]` P046 citation not load-bearing
- **Where**: `profile.yaml` `quality_bar[1]` — cites `(P017, P012, P046)`.
- **Problem**: P046 does not ground the milestone-decomposition/promptness clause (P017+P012 do). Citation-hygiene, same family as #1–#4; also adds body words (#7). Carried over unaddressed from r2 nice-finding #10.
- **Fix**: drop `P046`, or add the specific clause it supports.

### 9. Stale `profile_version` in golden tests
- **Where**: `tests/golden-tests.yaml:4` — `profile_version: 1.0.0` vs. profile `agent_version: 1.2.0`.
- **Fix**: bump to `1.2.0` (do with #10).

### 10. Newest `when_not_to_use` exclusions have no negative-routing coverage
- **Where**: `tests/golden-tests.yaml` `negative_routing_tests` vs. `profile.yaml` `when_not_to_use[3]/[4]`.
- **Problem**: the v1.1.0 (craft writing → `research-writing-advisor`) and v1.2.0 (integrity/reproducibility → `research-integrity-reproducibility-advisor`) sibling-referral exclusions — the most routing-collision-prone — have zero negative tests. (≥1 negative test requirement is technically met by NR-001/002.)
- **Fix**: add NR-003 (craft-writing tighten → route to research-writing-advisor) and NR-004 (suspected data fabrication → route to research-integrity-reproducibility-advisor).

### 11. All 8 skills reference the bundled references via code-span, not Markdown link
- **Where**: every `skills/*/SKILL.md` References section — `` `../../references/research-career-principles-index.md` `` (backtick span).
- **Problem**: unreferenced-via-link resources are never loaded; the skill-authoring principle requires a relative Markdown link.
- **Fix**: convert to `[research-career-principles-index.md](../../references/research-career-principles-index.md)` and the evidence-notes equivalent in all 8 files.

### 12. `when_to_use` bullet 5 wording invites "produce the study design" misread
- **Where**: `profile.yaml` lines 28-29 / adapter lines 32-33 — "Designing or reviewing an empirical study, metric, or measurement for soundness."
- **Problem**: read literally, "Designing an empirical study" sits adjacent to forbidden "running the study… for the caller." Modes/examples show only critique/sequencing, but the trigger text can be misread as an offer to author the design.
- **Fix**: reword to "Advising on or reviewing the design of an empirical study, metric, or measurement for soundness."

### 13. 7 of 8 skills have empty-boilerplate Purpose sections
- **Where**: Purpose sections of all skills except `evaluation-metrics-and-research-judgment`.
- **Problem**: filler pattern "…`## When to use` and `## Procedure` carry the specific checks" names the next headers instead of stating what the skill accomplishes.
- **Fix**: rewrite each to a 2–3 sentence summary of the skill's actual operational content, matching the density `evaluation-metrics-and-research-judgment` already has.

### 14. Two skill descriptions lack a negative-scope guard
- **Where**: `early-career-positioning-and-negotiation` and `funding-grants-and-research-proposals` frontmatter `description`.
- **Problem**: generic trigger vocabulary ("job search", "negotiating an offer", "grant proposal") could false-trigger on non-research corporate/HR requests; only `evaluation-metrics-and-research-judgment` has a "Not for…" exclusion.
- **Fix**: append a trailing "Not for…" sentence scoping out the generic corporate/HR analogs.

---

## NICE

- **15.** `evaluation-metrics-and-research-judgment/SKILL.md` "When to use" bullet 7 (applicant ranking) sits ~50 lines from its Output-section no-decision reminder; add an inline qualifier "(never the agent's own hiring/admission call)".
- **16.** Description template inconsistent: 6/8 skills use "Guides X. Use when Y."; `presenting-and-engaging-with-research` and `early-career-positioning-and-negotiation` invert. Normalize.
- **17.** Identical ~100-word Provenance prose paragraph repeated verbatim in all 8 skill bodies (duplicates frontmatter `provenance`). Shorten to a one-line pointer.
- **18.** `research-program-and-problem-selection` skill description char-count never explicitly re-verified under the 1024 cap (r2 measured only the funding skill). Measure and record, or trim defensively.
- **19.** `provenance-ledger.md:14-15` asserts the "descriptive fields carry no inline tags" convention without pointing to where it is defined; add a pointer to the rule/sibling precedent.
- **20.** `role`/`router_description` bundles career coaching with statistical/empirical-methodology review — grounded (Cohen/Hamming) but one of the widest sibling remits; if a routing eval later shows misses for pure methodology queries, foreground the methodology half earlier. No change now.
- **21.** Adapter grants `Grep, Glob` though required inputs are pasted conversational text, not a corpus; confirm intentional (read-only, no risk).

---

MUST_FIX_COUNT: 2
