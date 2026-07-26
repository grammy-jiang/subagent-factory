# Review — research-career-advisor (round r2)

Single review pass over `subagents/research-career-advisor/` (v1.3.0). Four reviewer lenses
(agent-skills, profile, faithfulness, ai-agent-engineering) + deterministic gates. Review-only;
no package files edited. Findings deduped across lenses, most-severe first.

## Deterministic gates (STEP 1)

| Gate | Result |
|------|--------|
| `validate_generated_package` | **VALIDATION PASSED** (0 FAIL). `phase8` WARN; `injection-scan` 7 WARN — all benign frozen-source Hamming prose ("you are now at the lower levels…"), triage-not-block per untrusted-source-policy. NOT must-fix |
| `quote_scan` | PASS — no verbatim quotation |
| ellipsis / severed-invariant truncation grep | clean — no hits |

Deterministic must-fix = **0**.

---

## MUST-FIX

### 1. `forbidden_behaviours[1]` — false principle citation on hiring/tenure no-advice boundary
- **Where:** `profile.yaml:90` — "Making or predicting a hiring, admission, funding, or tenure outcome… (structural house-policy; P010, P021)"; `reports/faithfulness-report.yaml:61-67`.
- **Problem:** P010 is the adviser-selection tie-break (reputation vs. protection factors); P021 is postdoc-position selection criteria. Neither grounds a rule about refusing to predict/guarantee outcomes. v1.3.0 added the "structural house-policy" label but **kept** the false `(P010, P021)` citation — `reports/review-loop/*.r3.review.md` MUST-FIX #2 explicitly ruled the label alone insufficient (must *drop* the citation or cite a real grounding claim). `faithfulness-report.yaml:61-67` still asserts "Restates P010/P021… no strengthening" — factually false. Confirmed independently by profile + faithfulness lenses against `principles.yaml`. Highest-stakes instance: a boundary presented as source-derived when it is not (the boundary behaviour itself is correct).
- **Fix:** Drop the `(P010, P021)` citation (house-policy alone suffices per `source_of_truth_policy`), or cite an actual grounding claim from `claims.jsonl`. Sync `faithfulness-report.yaml:61-67` to the disclosed-house-policy framing (not "Restates…").

### 2. `forbidden_behaviours[2]` — false principle citation on legal/immigration no-advice boundary
- **Where:** `profile.yaml:92` — "Giving binding legal, financial, contractual, visa or immigration, or HR advice… (structural house-policy; P026)"; `reports/faithfulness-report.yaml:68-74`.
- **Problem:** P026 is entirely about negotiating a result-oriented start-up package (space, equipment, confirm in writing). It says nothing about refusing legal/immigration/HR advice. Same defect family as #1 — label added, false citation kept; `r3.review.md` MUST-FIX #1. `faithfulness-report.yaml:68-74` still says "Restates P026… no strengthening" — factually false.
- **Fix:** Same as #1 — drop or correct `(P026)`; sync `faithfulness-report.yaml:68-74`.

### 3. Skill `## Output` contract implements only the `review` mode — `advise` and `plan` undocumented in every SKILL.md
- **Where:** all 8 `skills/*/SKILL.md` `## Output` (byte-identical text, e.g. `skills/research-program-and-problem-selection/SKILL.md:80-82`).
- **Problem:** `profile.yaml` `outputs.modes` defines three shapes — `advise` (one recommendation + trade-off/referral), `review` (findings list, highest-impact first), `plan` (ordered horizon-scoped steps). Every SKILL.md carries only the `review` shape ("Per finding: name the gap and the principle…, order findings highest-impact first"). A caller invoking `advise`/`plan` gets steered toward a findings-list critique. The Claude Code adapter compensates at top level (`adapters/claude-code/research-career-advisor.md:57-76`), so runtime is not broken — but `schema_version: portable-profile-v1` is meant to export to platforms that load SKILL.md standalone, where the two missing modes have no other source.
- **Fix:** Replace the single hard-coded review-shape sentence in each `## Output` with a 3-line mapping to the profile's `advise` / `review` / `plan` shapes so each skill is self-sufficient off-adapter.

---

## SHOULD-FIX

### 4. `forbidden_behaviours[0]` — same false-citation pattern (lower stakes)
- **Where:** `profile.yaml:88` "(structural house-policy; P017, P013)"; `faithfulness-report.yaml:57-60`.
- **Problem:** P017 is milestone decomposition; P013 dissertation coherence. Neither grounds "advisor must not produce the output." `r3.review.md` #3 (should-fix — not a legal/outcome boundary).
- **Fix:** Drop/correct the citation; sync `faithfulness-report.yaml:57-60`.

### 5. `handoff_rules[0]` and `[1]` — false citations, and missing the house-policy label their sibling carries
- **Where:** `profile.yaml:100` (`(P015, P017)`) and `:103` (`(P026, P010)`); `faithfulness-report.yaml:137-151`.
- **Problem:** P015 (orient program around consequential questions) / P017 (milestone decomposition) do not establish study/data/writing ownership; P026/P010 repeat the #1/#2 mis-citation. `handoff_rules[2]` already carries "(structural house-policy, not principle-derived)"; `[0]`/`[1]` do not. Confirmed by both profile + faithfulness lenses. `r3.review.md` #4 flagged `[1]`; `[0]` has the identical defect.
- **Fix:** Add the same "structural house-policy" qualifier and drop/correct the citations on both; sync `faithfulness-report.yaml:137-151`.

### 6. `knowledge_partition` (choosing-advisers bullet) broadens P034 out of scope
- **Where:** `profile.yaml:149` — "…a laboratory's management of priorities, resources, performance, collaboration, and internal mobility… (P010, P011, P021, P024, P033, **P034**)".
- **Problem:** P034's `applies_when` scopes it to an industrial or government laboratory; the bullet presents it as a general adviser/group heuristic with no qualifier (SCOPE_BROADENED). `r3.review.md` #5; the faithfulness report audits whole blocks so it did not catch this bullet-level claim.
- **Fix:** Add the industrial/government-lab qualifier or split the claim.

### 7. `quality_bar[1]` carries a non-load-bearing P046 citation
- **Where:** `profile.yaml:72` — "…a few strong papers preferred over many weak (P017, P012, **P046**)".
- **Problem:** P046 is about honestly generalizing a result's scope, not dissemination cadence (P017/P012 cover the clause). Loose thematic tag, not strengthening. Flagged by profile + faithfulness; `r3.review.md` #8.
- **Fix:** Drop P046 here (already correctly cited in the writing-and-publishing `always_on` block).

### 8. `tests/golden-tests.yaml` `profile_version` stale
- **Where:** `tests/golden-tests.yaml:4` `profile_version: 1.0.0` vs `profile.yaml` `agent_version: 1.3.0`.
- **Problem:** three versions stale. `r3.review.md` #9.
- **Fix:** Bump to `1.3.0` (or the next release version).

### 9. `provenance-ledger.md` Version History omits round 3
- **Where:** `provenance-ledger.md` Version History.
- **Problem:** Ledger records round-2 → 1.2.0 and round-1 → 1.3.0 but never records that round 3 ran against v1.2.0 and found 2 unresolved MUST-FIX (items #1/#2). A reader relying on the ledger alone sees a clean history over known-open defects — a traceability gap distinct from the citations themselves.
- **Fix:** After #1–#5, add a Version-History entry citing `r3.review.md`; if releasing sooner, at minimum note the open must-fix items.

### 10. `presenting-and-engaging-with-research` omits its nearest sibling-advisor boundary
- **Where:** `skills/presenting-and-engaging-with-research/SKILL.md:3-14` (description).
- **Problem:** Skill vets slide *content* (Procedure step 3), sitting right next to `when_not_to_use`'s "figure or slide design → research-writing-advisor". The sibling `writing-and-publishing` skill states that boundary; this one only excludes "generic business presentation." A slide-layout/visual-design request risks firing here instead of routing to research-writing-advisor.
- **Fix:** Add a clause: covers *what content* belongs on a slide and argument-fit, not slide layout/typography/visual design (→ research-writing-advisor).

### 11. No SKILL.md carries a worked example despite 3 profile examples mapping onto skills
- **Where:** all 8 `skills/*/SKILL.md` (no `## Example`); examples live only in `profile.yaml:224-266` + adapter.
- **Problem:** For judgment-heavy advisory skills a concrete input/output example disambiguates the target shape. Profile example 1 ↔ research-program-and-problem-selection, 2 ↔ experimental-design-and-measurement, 3 ↔ choosing-advisers / early-career-negotiation — but none are embedded/linked. Off-adapter (standalone SKILL.md load) there are zero worked examples.
- **Fix:** Add a short `## Example` to at least the three skills with a ready match (embed a trimmed profile example or link `references/research-career-evidence-notes.md`).

### 12. Role bundling justification thin for a two-concern charter
- **Where:** `profile.yaml` role / adapter line 19.
- **Problem:** Role welds research-career/positioning strategy and empirical-methods/measurement review with one justificatory sentence. Coherence risk at frontmatter-skim altitude — reads as two advisors bundled. Design is intentional (dedicated `experimental-design-and-measurement` + `evaluation-metrics-and-research-judgment` skills keep the sides separately triggerable), so this is presentation, not scope creep.
- **Fix:** Strengthen the one-line justification to name the shared discipline concretely (career judgment and empirical judgment are exercised on the same decisions — worth persisting on? worth publishing?), or confirm the bundling as deliberate.

---

## NICE

- **13.** `evaluation-metrics-and-research-judgment` description lacks an explicit "reviews how a selection/ranking process is built, not who is selected" clause — a marginal "should we admit X?" is stopped only by the shared Output boilerplate, not the trigger. (`skills/evaluation-metrics-and-research-judgment/SKILL.md:3-13`)
- **14.** Identical ~130-word `## Output`/`## References` boilerplate duplicated byte-for-byte across all 8 SKILL.md — drift risk if the contract changes and only 7 are updated. Fine if generator-templated from one source; verify that on next regen.
- **15.** Redundancy: "producing the research output" appears as both `forbidden_behaviours[0]` and a `handoff_rules[0]` ownership fact — change both together or they drift.
- **16.** `when_to_use[5]`/`when_not_to_use[5]` empirical-vs-integrity boundary ("statistical validity in scope; judging p-hacking out") is fine-grained but no worked example exercises it — a 4th example (suspiciously significant result → statistical-validity review + handoff to research-integrity-reproducibility-advisor) would make it self-evident.
- **17.** `provenance-ledger.md:17-18` asserts the "descriptive fields carry no inline tags" convention without pointing to where it is defined. (`r3.review.md` #19)
- **18.** Round-numbering is confusing to a later auditor: round-2 (PR#97) merged before round-1 fixes; round-3 (most recent, most substantive) has no fix branch/PR. A one-line ledger note on sequencing would prevent "rounds 1&2 done ⇒ round 3 done" misreads.

MUST_FIX_COUNT: 3
