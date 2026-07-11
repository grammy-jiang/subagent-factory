# Review — subagent package `calibration-forecasting-reviewer` (r2)

Scope: ONE review pass, REVIEW ONLY. cwd = `/home/grammy-jiang/projects/subagent-factory`.

## Gate (deterministic)

- `validate_generated_package` → **VALIDATION PASSED** (0 FAIL). Only WARNs: injection-scan on `sources/markdown/thinking-fast-and-sl-d88ef771.md` (fake-completion / role-override, dewrapped+unescaped) — source-side triage WARN per untrusted-source-policy, not a package defect.
- `quote_scan` → **PASS** — no verbatim quotation.

No gate FAILs. Must-fix below are reviewer-found release-readiness / faithfulness defects.

## Findings (deduped, severe-first)

### CRITICAL

1. **Faithfulness report skips the load-bearing rules.** `reports/faithfulness-report.yaml` has **zero findings for `knowledge_partition.always_on[0..7]`** — the 8 dense runtime rules (`profile.yaml:154–212`, 5–14 principle cites each). Report only covers peripheral fields (role/when_to/inputs/outputs/quality_bar/forbidden/handoff). The `always_on` set is what drives behavior; it was not reviewed. → Re-run faithfulness review to add per-rule findings for `always_on[0..7]` before release.

### HIGH

2. **`forbidden_behaviours[3]` removes hedging from a medium-confidence principle.** `profile.yaml:126–129` folds P031 (rated `confidence: medium` in `principles.yaml`) into an unqualified *forbidden* prohibition ("unvalidated granularity as precision") alongside high-confidence P059/P035. Verdict should be **HEDGING_REMOVED**, not the report's `WITHIN_SCOPE`/`accept_with_note`. → `add_condition`: qualify (e.g. "when granularity is asserted without validation evidence") or downgrade severity.

3. **Provenance ledger missing v1.0.1 Version History entry.** `provenance-ledger.md:54–59` stops at v1.0.0, but `profile.yaml:5` = `1.0.1` and `CHANGELOG.md:6–23` documents a substantive v1.0.1 release. Violates supersession rule in `.claude/rules/generated-artifact-policy.md`. → Append `### v1.0.1 — 2026-07-11` mirroring the CHANGELOG fixes.

4. **Provenance ledger mapping table stale vs shipped profile.** `provenance-ledger.md:40,44` still lists **P023** (base-rates) and **P087** (scenarios) as profile-level cites, but v1.0.1 removed both from `profile.yaml` `always_on` (confirmed absent via grep). Table implies grounding that no longer exists. → Update table or annotate P023/P087 as skill-only, not profile-restated.

5. **golden-tests version metadata not bumped.** `tests/golden-tests.yaml:4` = `profile_version: 1.0.0` while profile + adapter are `1.0.1`. Breaks release version consistency. → Bump to `1.0.1` and re-verify the 5 golden / 2 negative / 2 missing-context tests hold (spot-check: none reference P023/P087, so likely still pass).

6. **Skill descriptions in wrong point-of-view (all 8 SKILL.md).** Every `skills/*/SKILL.md:3` frontmatter `description` is imperative ("Audit whether…", "Review a single…", "Make a forecast…") not third person. This package's own agent-skills corpus mandates third person (injected into system prompt → discovery problems); sibling packages `analytic-method-reviewer` and `bias-perception-reviewer` correctly use third person. Systemic, package-wide. → Rewrite all 8 to third person ("Audits…", "Reviews…", "Makes…"), keep scope/trigger text otherwise unchanged.

### MEDIUM

7. **Faithfulness report is templated, not per-rule.** 12+ distinct `rule_ref`s share identical note text + identical P015/P006/P022 citation triple; every finding uses `support_granularity: section`, never claim/sentence. WITHIN_SCOPE verdicts are boilerplate, not verified evidence. → Re-run with rule-specific citations at finer granularity (couples with finding #1).

8. **Adjacent skills lack frontmatter disambiguation.** `forecast-scoring-and-evaluation` vs `forecasting-accountability-and-communication` (the "almost right" P025 vs "it almost happened" P086 excuses) — disambiguation lives only in body `## References`, not the trigger-gating description. Sibling packages put "not X — see sibling" clauses in the description line. → Fold a short disambiguation clause into both descriptions.

9. **Profile's advise/compare modes implemented in only 1 of 8 skills.** `profile.yaml:64–85` declares review/advise/compare; only `calibration-and-probability-hygiene/SKILL.md:255–259` states advise/compare collapse. Other 7 skill bodies describe only the review-findings shape. → Add advise/compare collapse note to each `## Output`, or scope mode routing in profile to name which skills advise/compare use.

### LOW

10. **Medium-confidence principles voiced in flat imperative (systemic nuance).** `always_on[6]` (P056/P079/P089 all medium), `always_on[5]` (P088), `always_on[2]`/`quality_bar[1]` (P090/P091) never modulate claim strength by source confidence tier. No individual SCOPE_BROADENED, but confidence tiering is invisible. Lower risk where the wording keeps its own hedge.
11. **quality_bar[3]/always_on[4] drops P034's "offsetting errors" caveat** — hindsight + unpacking are two errors to *manage*, not eliminate; compressed to "surfaced and corrected."
12. **Body verbosity.** `calibration-and-probability-hygiene` (306 lines) and `scenarios-horizon-and-tail-risk` (261 lines) run long vs the concise-skill guidance (P059/P088/P114); both well inside the 500-line validator cap — stylistic only.
13. **No `self_check` field in profile** — confirmed systemic factory-schema gap (zero hits repo-wide; `quality_bar`+`minimum_useful_output` serve the role). Not package-specific; flag to schema owner, not a per-package blocker.

## Clean

- **Agent design (adapter + profile): 0 findings.** Tools = `Read, Grep, Glob` only — no Edit/Write/Bash/mutating/network grant. Reviewer-vs-doer boundary stated explicitly and consistently across role / when-NOT / forbidden / handoff / worked example; all 3 modes stay at critique/recommend level, no forecast value emitted. Frontmatter gating present. Matches sibling `analytic-method-reviewer` pattern.
- Skill `name` fields all match dir names + `profile.yaml` `knowledge_partition.skills`; no collisions; consistent Purpose→When→Procedure→Inputs→Output→Anti-patterns→References→Provenance structure; altitude correct (skills = procedure, profile = trigger summary); sibling cross-refs point to real files.
- Profile role scoped; when_to (5) / when_not (3) precise, non-overlapping; quality_bar (5) + forbidden (4) concrete, enforceable; 6 sources `distillation-only` with well-formed sha256; 91 principles match ledger; cited P-ids in range; CHANGELOG internally consistent with profile v1.0.1.

MUST_FIX_COUNT: 6
