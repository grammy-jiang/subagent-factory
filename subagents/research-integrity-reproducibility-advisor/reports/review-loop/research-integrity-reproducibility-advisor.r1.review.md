# Review Loop r1 — research-integrity-reproducibility-advisor

Single review pass. Deterministic gates + 4-lens reviewer panel (agent-skills, profile,
faithfulness, ai-agent-engineering). Consolidated, deduped, most-severe first.

## Deterministic gates (STEP 1)

| Gate | Result |
|------|--------|
| `validate_generated_package` | **PASS** (0 FAIL) |
| `quote_scan` | **PASS** — no verbatim quotation |
| ellipsis truncation grep (`…`) | clean |
| adapter invariant-sever grep | clean |

0 deterministic FAILs. (Note: the ellipsis grep did NOT catch the body truncation in
must-fix #1 below — those cut-offs end mid-clause with a `.` and no `…`, so the grep is
blind to them. Manually confirmed via `grep`.)

---

## MUST-FIX

### M1 — Skill bodies truncated mid-clause (Procedure steps + Anti-patterns)
**Where:** all 7 `skills/*/SKILL.md`. Confirmed instances:
- `version-control-and-collaboration/SKILL.md:49` — "...only merge finished, tested work into it; **when a merge conflict occurs (P031).**" — trails off, no instruction attached.
- `research-software-engineering-and-testing/SKILL.md:48` — "...treat even one-off analysis scripts as software, **draft (P005).**" — missing object of "draft".
- `research-data-management-and-sharing/SKILL.md:49` — "...reuse and licensing, and costs; **ensure at least one (P017).**" — "at least one" *what*?
- `authorship-publication-and-attribution/SKILL.md:54` — "...all required editorial and rights-holder **consents are (P013).**" — missing "obtained".
- Anti-patterns are worse and near-universal: `reproducible-computational-pipelines/SKILL.md:72` "...rebuilds an output **whenever.**"; `research-integrity-and-misconduct/SKILL.md:68` "...report data so that... **examine.**"; `:69` "...preserving and inspecting **original.**"
**Severity:** must-fix (violates package's own quality bar "actionable, concrete steps, not vague prose"; several bullets are non-instructions).
**Fix:** Regenerate the body-summarization step to respect sentence/clause boundaries (or reuse full principle text, or hand-tighten each to one complete short sentence). Re-run stale-stamp + re-export after.

### M2 — No `description` in any skill frontmatter
**Where:** all 7 `skills/*/SKILL.md` frontmatter. Fields are limited to `name`/`kind`/`status`/`provenance`; no `description`.
**Severity:** must-fix. `description` is the sole triggering signal an Agent-Skills host reads at metadata-scan time; without it these skills cannot progressive-disclose or auto-trigger under the standard mechanism.
**Fix:** Add a ≤1024-char `description` per skill, front-loading concrete trigger phrases (synthesize from each body's Purpose + "When to use"). Trim the heavy `provenance` claim-id list out of frontmatter into the body's existing `## Provenance` section while there.

### M3 — Faithfulness report never checked `knowledge_partition.always_on` (7 skill-scope rules)
**Where:** `reports/faithfulness-report.yaml`. 18 findings cover `quality_bar`/`forbidden_behaviours`/`when_to_use`/`outputs`/`handoff_rules`/`source_of_truth_policy` — but **zero** findings for the 7 `always_on` bullets, which between them cite all 34 principles (more than the rest of the profile combined) and make per-skill behavioural claims. These are profile rules and were never over-claim-checked, so the faithfulness gate is not truly clean.
**Severity:** must-fix (audit-completeness gap on the load-bearing gate).
**Fix:** Add 7 findings (one per `always_on` bullet) to the faithfulness report. While doing so, resolve the SCOPE_BROADENED candidate in **S6** below.

---

## SHOULD-FIX

### S1 — Anti-patterns restate principles instead of being real anti-patterns
**Where:** all 7 `skills/*/SKILL.md`, `## Anti-patterns to flag`. Every bullet is "Overlooking P0xx: <restatement>", not a concrete red-flag symptom.
**Fix:** Rewrite as observable bad symptoms (e.g. P029 → "commit message reads 'fix stuff', five unrelated changes in one commit") contrasted with the fix.

### S2 — Lens mismatch: P016 (open-hardware) filed under software-eng-and-testing
**Where:** `skills/research-software-engineering-and-testing/SKILL.md` (P016). Its content is openness/community/discoverability, not testing; the skill's other principles are all SMP/test-layering.
**Fix:** Move P016 into `open-source-projects-and-licensing`, or broaden that skill's stated scope to cover hardware.

### S3 — `plan` mode has no worked example
**Where:** `profile.yaml` `examples` / `modes`. Both examples exercise only `review` and `advise`; `plan` (project setup / DMP / open-release planning, when_to_use #1 and #4) has zero example coverage.
**Fix:** Add a third example exercising `plan` end-to-end.

### S4 — Contribution scenario in skills but no matching `when_to_use` trigger
**Where:** `profile.yaml`. `always_on` skill 5 covers "contribute well to someone else's project," but no `when_to_use` bullet surfaces a contribution scenario (closest, #4, is about *releasing*, not *contributing*).
**Fix:** Add/extend a `when_to_use` trigger for "contribute to an existing open research project."

### S5 — Ledger omits faithfulness-review outcome
**Where:** `provenance-ledger.md`. Asserts a faithfulness report exists but never states its result (pass/fail, count of any SCOPE_BROADENED/HEDGING_REMOVED/CONTRADICTED and resolution).
**Fix:** Add a one-line Faithfulness note recording the outcome so the gate is auditable from the ledger.

### S6 — P027 documentation duties applied beyond source scope (SCOPE_BROADENED candidate)
**Where:** `profile.yaml` `always_on[0]` vs `principles/principles.yaml` P027. P027's `applies_when` is scoped to "reusing a dataset produced by others," but the bullet applies its documentation duties unconditionally to anyone planning/documenting/depositing data.
**Fix:** Verify P027's source scope; correct either the principle's `applies_when` or narrow the bullet's framing. Resolve as part of M3.

### S7 — Faithfulness report findings are boilerplate, no anchors
**Where:** `reports/faithfulness-report.yaml`. All 18 findings use one templated note ("Restates <Pxxx>; within the source's scope...") with no `source_anchors`; verdicts aren't independently auditable.
**Fix:** Re-run with per-finding anchor citations, or vary the notes to show the specific comparison made.

### S8 — `outputs.primary_format` guardrail dropped from exported adapter
**Where:** `.claude/agents/generated/research-integrity-reproducibility-advisor.md` vs `profile.yaml:42-45`. Profile's primary_format states "never a bare good/bad verdict or an institutional finding"; the adapter renders only per-mode Trigger/Output pairs and drops this sentence, so the runtime agent (loads adapter only) never sees it.
**Fix:** Render `outputs.primary_format` in the adapter, or fold its "never a bare verdict" clause into Forbidden behaviours. Likely a shared export-template fix — check sibling packages before fixing per-package.

### S9 — Adapter `description` under-surfaces triggers for routing
**Where:** `.claude/agents/generated/research-integrity-reproducibility-advisor.md:3`. Description surfaces only the first `when_to_use` + first `when_not_to_use` bullet; higher-signal discriminators (misconduct/authorship/human-subjects; "won't adjudicate / won't give legal advice") are absent from what Claude Code auto-routes on.
**Fix:** Compress a broader spread of when/when-not triggers into the description. Confirmed factory-wide template pattern — fix in the shared description-generation step.

---

## NICE

- **N1** — Identical boilerplate `## Inputs` / `## Output` sections repeated verbatim across all 7 skills; centralize the shared contract, keep only skill-specific Inputs local. (all `skills/*/SKILL.md`)
- **N2** — `always_on[1]` cites P026 but P026 is marked `operational_mapping.profile_rule: false` and its content (Make authoring conventions) isn't reflected in the bullet text (only P032 supports it); drop the P026 citation or reconcile the flag. (`profile.yaml`, `principles.yaml`)
- **N3** — `always_on[4]` correctly uses P020, but P020 is stale-flagged `profile_rule: false`; flip to `true`. (`principles.yaml`)
- **N4** — `sources` `year: null` for `gaoxiao-xueshu-guifa` with no ledger note on why; add a one-line note or fill it. (`profile.yaml`, `provenance-ledger.md`)
- **N5** — `when_to_use` #5 (manuscript authorship/citations) overlaps #2 (authorship/citation ethics); consider merging. (`profile.yaml`)
- **N6** — `golden-tests.yaml` mode/negative-routing coverage not independently re-verified this pass; confirm all 3 modes + the misconduct-adjudication decline case are exercised before release.

---

## Cross-lens dedup notes

- profile-reviewer and ai-agent reviewer both PASS with 0 must-fix; their findings land in should/nice above.
- M3 (faithfulness report incomplete) and S6/S7 are the same lens (faithfulness) — M3 is the blocking completeness gap, S6/S7 are quality issues resolved within the same re-run.
- S8/S9 are shared export-template issues, not package-unique — flagged here, fix upstream.

MUST_FIX_COUNT: 3
