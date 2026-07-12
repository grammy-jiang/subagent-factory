# Review Loop — descriptive-translation-reviewer — r3 (profile v1.10.0)

One review pass. 4 lens reviewers + 3 domain reviewers + 3 deterministic gates. Findings
consolidated, deduped, most-severe first. Each: where | severity | problem | fix.
(Supersedes the earlier v1.6.0 content that previously occupied this filename.)

## Deterministic gates (STEP 1)
- `validate_generated_package` → **VALIDATION PASSED** (0 FAIL; phase8 body-size WARNING only). Tier 2, 12 skills + 2 refs authored, adapter-sync OK, stale-maintenance all "grounding unchanged".
- `quote_scan` → **PASS** (no verbatim quotation).
- Truncation greps (`…` in skills/adapter; severed invariant parentheticals) → **0 hits** (clean).

Deterministic FAIL count = 0.

---

## MUST-FIX

### MF-1 — Test artifacts stale against shipped `agent_version` (release-blocker)
- **Where:** `tests/golden-tests.yaml:4` (`profile_version: 1.9.0`) and `tests/test-results.md:7` (`Verdict (v1.9.0)`) vs `profile.yaml:4` (`agent_version: 1.10.0`). Deterministically confirmed by grep.
- **Problem:** the v1.10.0 bump (M1/M2 fixes per ledger) re-exported the adapter but skipped re-stamping the test artifacts. This package's own history treats a stale `profile_version` as must-fix (v1.7.0 MF-1, v1.9.0 MF-3; the earlier v1.6.0 review-loop caught the identical drift). `generated-artifact-policy` requires version consistency + validation before release.
- **Fix:** re-stamp `tests/golden-tests.yaml` `profile_version: 1.10.0`; regenerate `tests/test-results.md` with the current verdict (fresh body word-count — see SF-6); note the re-stamp in the ledger v1.10.0 entry.

---

## REJECTED must-fix (verified false — recorded so it is not re-raised)

### RJ-1 — "adapter silently drops 36 of 180 principles / compile_invariants truncation" — REJECTED
- **Raised by:** ai-agent-engineering-reviewer (its sole must-fix).
- **Claim:** the adapter references only 144 unique principle IDs; 36 (`P023, P033–035, P054–057, P089–090, P092–101, P103, P142–156`, incl. "safety" P145/P146) are absent from the "Operating invariants" section, matching the known sibling `compile_invariants` truncation SAFETY bug.
- **Why rejected — the invariant layer is a DELIBERATE must-hold subset, not all 180.** `tools/subagent_factory/compile_invariants.py` selects must-hold = `confidence: high` AND `operational_mapping.profile_rule: true`, and renders each as a full-first-sentence bullet. Verified deterministically: **compile yields exactly 141 must-hold invariants; all 141 appear in the adapter (0 missing); and none of the 36 "absent" IDs are must-hold** (they are lower-confidence / non-profile-rule principles that correctly live in the on-demand skill files, reachable via progressive disclosure). `validate_invariant_coverage` passed (0 stale/missing). The 36 are not dropped — they were never must-hold. P145/P146 carry no safety weight in THIS package (no safety axis; they concern skopos/descriptive method). The known SAFETY bug is *truncation of a must-hold rule to a `…` one-liner* — this adapter has 0 ellipsis and full-sentence invariants, i.e. the correct (non-bug) state. Not counted.

---

## SHOULD-FIX

- **SF-1 — No independent re-verify recorded for v1.10.0.** `provenance-ledger.md` self-narrates the M1/M2 fixes in the same entry that closes the version; no independent round confirms `MUST_FIX_COUNT:0` at 1.10.0. *(This r3 pass is that check.)* Record this round's converged result in the ledger before treating the package as shipped. (profile-reviewer.)

- **SF-2 — Frontmatter `description` under-specifies the closest sibling boundary.** `.claude/agents/generated/descriptive-translation-reviewer.md:3` names only the `translation-quality-reviewer` exclusion; omits `translation-equivalence-advisor`, though the body's own when-not-to-use calls that (mechanism vs orientation) the most confusable split in the 4-sibling family. The one-line description is the primary auto-routing signal. **Fix:** name both, e.g. "…not the equivalence mechanism itself (→ translation-equivalence-advisor) and not corpus QA scoring (→ translation-quality-reviewer)." (ai-agent.)

- **SF-3 — Invariant P058 worded as an action for someone *producing* a translation.** Adapter line 122: "Before assessing or **producing a translation**, fix its type…" — pulls against the review-only authority boundary (only the Role's blanket reinterpretation defends it). Siblings share the imperative-to-a-translator voice (P015, P045). **Fix:** reword P058 (audit siblings) into reviewer-voice: "Check whether the translation fixed its type/vocabulary before…". (ai-agent.)

- **SF-4 — Skill Output sections cover only `review` mode.** Every skill's Output states a flaw-finding shape; none maps to `advise` / `compare`, though 2 of 4 profile worked examples are advise/compare. A reader of one SKILL.md would infer post-hoc critique only. **Fix:** add one clause per skill Output mapping the same checks to advise (recommendation + trade-off) and compare (side-by-side). (agent-skills.)

- **SF-5 — Anti-patterns ~1:1 restate Procedure across all 12 skills**, doubling already-dense bodies against the package's own concision bar / progressive disclosure. **Fix:** collapse Anti-patterns to compact red-flag clauses, or move the prose to `references/descriptive-translation-evidence-notes.md` with a pointer. (agent-skills.)

- **SF-6 — Profile body word-count margin critically thin (~985w vs 1000-word hard-FAIL).** The review-only boundary is restated at near-full strength in `role`, `when_not_to_use[0]`, and `forbidden_behaviours[0]`; the next additive fix will hit FAIL. **Fix:** consolidate to one full statement + cross-refs to buy durable margin. (profile-reviewer.)

- **SF-7 — Worked example over-cites P062.** `profile.yaml` liturgical formal-vs-dynamic compare example (~lines 249–259) cites `(P062, P036)`; the "sacred text warrants closer word/syntax attention" claim is P036's content — P062 is skopos *ordering* (purpose > coherence > fidelity). **Fix:** cite P036 alone; reserve P062 for an ordering claim. (translation-quality-reviewer.)

- **SF-8 — Missing sibling tie-breaker on the free/literal axis.** `literal-free-strategy-history-and-retranslation` (Dryden triad) and `domestication-foreignization-and-visibility` (Venuti free/literal) both stake the free-vs-literal axis with no routing statement between them, unlike the rest of the package's disambiguation discipline. **Fix:** add a one-clause tie-breaker to both descriptions (classical rhetoric-based literal/free stays in the former; modern ideological domestication/fluency routes to the latter). (agent-skills.)

- **SF-9 — Missing Nord "function plus loyalty."** The skopos hierarchy (P062) + "skopos does not excuse micro-neglect" (P108) are covered, but Nord's loyalty check on skopos-driven liberties — the mechanism `text-type-skopos-and-the-brief` needs to judge whether a brief-licensed departure went too far — is absent from all 180 principles. Previously surfaced (r5 SF-5) and deferred (CHANGELOG v1.4.0) as spine-expansion; still open on domain completeness. **Fix:** promote C00155 into a principle routed to that skill, or record a durable deferral rationale. (technical-translation-advisor.)

- **SF-10 — Cross-package register boundary (register-discourse skill vs `translation-quality-reviewer`) open across ≥2 cycles** with no tracking reference. **Fix:** add an issue / sibling-ledger pointer so it doesn't go stale. (profile-reviewer.)

---

## NICE
- **N1** — Frontmatter descriptions long; four-way disambiguation clause strains the always-loaded trigger tier (`meaning-signification-…`, `translation-procedures-…`, `register-discourse-…`). Keep the single load-bearing tie-breaker; move secondary sibling pointers into the body. (agent-skills.)
- **N2** — Body "Purpose" ≈ verbatim restatement of the frontmatter description across all 12 skills; give Purpose new information (scope cue) instead. (agent-skills.)
- **N3** — Adapter description "Not for" restates the role rather than naming an exclusion; replace with a concrete route-elsewhere clause. (ai-agent.)
- **N4** — Role paragraph bundles 5 ideas into one subordinated sentence; split so the invariant-reframing safety instruction stands alone for salience. (ai-agent.)
- **N5** — Subtitle "38 Roman characters / ~6s" (P069 + register skill) stated near-hard; AVT guides vary ~35–42 — already hedged "about/near-universal"; spot-check against Munday's cited figure. (equivalence + quality + technical reviewers.)
- **N6** — P010 "chronological precedence" of preliminary norms could soften to "usually chronological" per Toury (logical precedence firm, chronological typical). (equivalence-advisor.)
- **N7** — Name Baker's 1993 universals alongside Chesterman's T-universals (P041/P054); name Toury's three "assumed translation" postulates (P039); add a one-line P047↔P054 cross-ref on the shared contested-generalization caveat. (quality + technical reviewers.)
- **N8** — Provenance ledger now 11 dense entries — add a top "current grounding state" summary block without deleting history. (profile-reviewer.)
- **N9** — No worked example exercises the `when_to_use[1]` no-source-target norm-claim path; add a 5th example. (profile-reviewer.)

---

## Tally
- Deterministic FAILs: 0.
- LLM must-fix (deduped, re-verified): 1 (MF-1, version-stamp drift, deterministically confirmed).
- Rejected as verified-false: 1 (RJ-1, adapter "truncation" — the 141-bullet invariant layer is a correct deliberate must-hold subset; 0 must-hold missing).
- Faithfulness: 0 over-claim (56 findings all WITHIN_SCOPE). Domain reviewers ×3: 0 domain errors / 0 must-fix.

MUST_FIX_COUNT: 1
