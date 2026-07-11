# Review R1 — analytic-method-reviewer

Package: `subagents/analytic-method-reviewer/` (v1.0.0, status: ready)
Date: 2026-07-11 · One review pass, 4 parallel scopes (skills / profile / faithfulness / agent-design)

## Bash gate (authoritative)

- `validate_generated_package` → **VALIDATION PASSED** (0 FAIL). Injection-scan WARNs only,
  all on `sources/markdown/*.md` (Superforecasting, Thinking-Fast-and-Slow book prose) —
  benign source content, not adapter/profile; non-blocking per untrusted-source triage policy.
- `quote_scan` → **PASS** (no verbatim quotation).

Gate FAILs = 0. The must-fix items below are release blockers found by the review scopes,
one of which (body-size) is a documented FAIL in the package's OWN Phase-8 record that the
release validator does not enforce.

---

## MUST-FIX (release blockers)

### 1. [CRITICAL] Profile body-size FAIL — package marked `ready` over its own failing self-check
`subagents/analytic-method-reviewer/profile.yaml` (whole body) · `tests/test-results.md:14`
- The package's Phase-8 `profile_self_check` records **Verdict: FAIL**, check 14 body-size:
  body ~1134 words (>1000 hard cap; 334 over the 800 budget). Heaviest: `quality_bar` 203w,
  `when_to_use` 158w, `modes` 140w. Adapter was exported and `status: ready` set anyway —
  violates "do not export until self-check gate passes."
- Note the discrepancy: `validate_generated_package` PASSES (it does not enforce the 1000-word
  cap that `profile_self_check` does). Both are real; the self-check FAIL governs release.
- Fix: trim the body (start `quality_bar` + `when_to_use`; push detail into the matching
  skills), re-run `profile_self_check` to PASS, re-export adapter, then confirm `ready`.

### 2. [HIGH] Over-claim — `quality_bar[4]` strips stakes/cost hedges (HEDGING_REMOVED)
`profile.yaml:quality_bar[4]`
- Rule states Red Team / Alternative Futures / "no hypothesis without a competitor" as an
  **unconditional** quality bar applied to every reviewed judgment. Sources hedge on
  stakes/cost: P006 "reserve … for high-consequence problems given its cost"; P004 "when at
  least two strong competing views exist and the stakes justify the cost"; P020 scoped to
  "high-stakes … especially a confident" conclusion; P080 "set no fixed number of hypotheses;
  scale … to uncertainty and policy impact" (directly contradicts a blanket
  no-hypothesis-without-competitor rule). Violates evidence-protocol faithfulness rule.
- Fix: qualify — "…where stakes and cost justify it… number/rigor scaled to uncertainty and
  policy impact (P004, P006, P020, P058, P080)." (Also shortens the body → helps #1.)

### 3. [HIGH] Adapter routing description truncated — drops the operational/HUMINT scope boundary
`.claude/agents/generated/analytic-method-reviewer.md:3` (frontmatter `description`)
- Auto-generated `description` is an incomplete fragment ("…the estimate, forecast") and omits
  the profile's most important exclusion — operational/collection/HUMINT/targeting tradecraft
  (present in `profile.yaml` `when_not_to_use:43-45` and the adapter body:195-197). Claude Code
  routes on `name`+`description`; an operational/HUMINT request could mis-route to this
  read-only analytic-method reviewer.
- Fix: regenerate a complete-sentence `description` that keeps the operational/HUMINT/targeting
  exclusion, not just the "substantive judgment" one.

---

## SHOULD-FIX

### 4. [MEDIUM] Over-claim — `forbidden_behaviours[1]` forbids single-outcome universally (SCOPE_BROADENED)
`profile.yaml:forbidden_behaviours[1]` — Forbids "single-outcome assessment with no competing
hypothesis" unconditionally, cited only to P013 (general ACH def). The governing principle P010
gates rejection on "most single-outcome analysis … on key issues … when cost of error is high
or deception is a serious possibility." Fix: cite P010 and inherit its "key/high-stakes issue"
qualifier.

### 5. [MEDIUM] Skill descriptions lack negative boundary → weak routing between near-siblings
All 9 `skills/*/SKILL.md:3` except `analytic-collaboration-training-and-process` (which models
the pattern with "…not the judgment itself"). Sibling skills share symptoms (e.g.
`competing-hypotheses-and-diagnostic-evidence` vs `structured-analytic-techniques`, both fire on
"single hypothesis/single-outcome"). Fix: append a short "; not X" clause naming the adjacent
skill's territory.

### 6. [MEDIUM] `references/analytic-method-evidence-notes.md` is orphaned from progressive disclosure
Declared in `profile.yaml` `knowledge_partition.references` but no SKILL.md links it (skills
only cite `analytic-method-principles-index.md` + siblings). Undiscoverable skill-by-skill.
Fix: add a pointer in each relevant skill's `## References`.

### 7. [MEDIUM] Procedure ↔ Anti-patterns duplication doubles skill body length
All 9 skills restate each principle twice ("check whether X" then "X is a flaw") in near-dup
language (files 150–235 lines), against the package's own conciseness principles P088/P114.
Fix: compress Anti-patterns to flaw-name + principle-ID bullets referencing the Procedure step.

---

## LOW / polish

- [LOW] `provenance-ledger.md:28-37` grounding table covers only role/quality_bar/
  forbidden/always_on; blanket "no orphan value" claim not verifiable from the ledger for
  `when_to_use`, `when_not_to_use`, `inputs`, `outputs`/`modes`, `handoff_rules`,
  `source_of_truth_policy` (they ARE grounded in `faithfulness-report.yaml`). Fix: extend table
  or point to the report as the authoritative per-field index.
- [LOW] `profile.yaml:forbidden_behaviours[3]` (operational/HUMINT) is the only forbidden bullet
  with no P-ID (grounded by scope/absence). Add a one-line note so it isn't read as orphan.
- [LOW] Finding-ordering phrased 3 ways across skills ("highest-impact" / "highest-risk-to-the-
  judgment" / "highest-impact-to-the-judgment") — standardize one phrase.
- [LOW] Trigger-clause style split: 6/9 skills use "invoke…", 3/9 use bare "before X is
  finalized" — standardize.
- [LOW] No per-skill worked example (only 2 aggregate examples at `profile.yaml:200-234`).
  Optional: add one short worked example per skill.
- [OK] Tool grant correct: `Read, Grep, Glob` only; `mcp: []`. No over-reach; role is REVIEW not
  DO (forbidden_behaviours + both worked examples confirm). DO-NOT-EDIT header present, adapter
  1:1 mirrors profile. Principle-ID coverage clean (every cited principle used, none duplicated
  across skills); version/CHANGELOG/ledger coherent (1.0.0 ↔ 1.0.0 ↔ 1.0.0).

---

MUST_FIX_COUNT: 3
