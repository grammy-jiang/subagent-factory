# Review Loop — descriptive-translation-reviewer — Round 4

Consolidated single-pass review of profile **v1.7.0**. Deterministic gates + 7 reviewer lenses
(agent-skills, profile, faithfulness, ai-agent-engineering, translation-equivalence,
translation-quality, technical-translation). Findings deduped across lenses; most-severe first.

## Deterministic gates (all PASS)

- `validate_generated_package` → **VALIDATION PASSED** (0 fail; 12 skills + 2 refs authored,
  adapter-quality OK, all tier-artifacts + stale-maintenance grounding unchanged).
- `quote_scan` → **PASS** (no verbatim quotation).
- Ellipsis truncation grep (skills + adapter) → **no hits**.
- Adapter invariant severed-parenthetical grep → **no hits**.

No deterministic FAILs → 0 must-fix from gates.

---

## must-fix

| # | Where | Problem | Fix |
|---|-------|---------|-----|
| 1 | `skills/translation-procedures-and-shifts/SKILL.md` (step 10, P168) vs `skills/register-discourse-and-audiovisual-constraints/SKILL.md` (Purpose, step 5, P064) | Both skills independently own the Field/Tenor/Mode (Hallidayan) register-profiling apparatus; step 10 builds a full register profile that the register skill exists for. Neither carries a reciprocal boundary sentence — a lens-fit / no-redundancy violation. The fix pattern is already applied elsewhere in this package (equivalence trio, domestication/culture pair). | Add reciprocal boundary sentences: in `translation-procedures-and-shifts` limit register use to naming the procedure/shift the profile motivates and route full field/tenor/mode discourse + cohesion analysis to `register-discourse-and-audiovisual-constraints`; add the reciprocal pointer there. |
| 2 | `skills/translation-quality-and-applied-studies/SKILL.md` (step 13, P112) vs `skills/text-type-skopos-and-the-brief/SKILL.md` (whole skill, P009/P038/P062/P070) | Step 13 reviews whether a commentary grounds itself in purpose/skopos, method, readership and a translation specification — the skopos/brief/commissioner territory `text-type-skopos-and-the-brief` owns. No cross-reference either way; same unresolved-overlap class as MF-1. | Add a boundary clause to `translation-quality-and-applied-studies`: whether a brief/skopos hierarchy was followed routes to `text-type-skopos-and-the-brief`; this skill reviews only whether the evaluation method documented that specification before scoring. Add the reciprocal pointer. |
| 3 | `.claude/agents/generated/descriptive-translation-reviewer.md:3` (frontmatter `description`) vs `.claude/agents/generated/translation-quality-reviewer.md:3`; source `profile.yaml` `description`/`when_to_use[0]` | Router-facing description collides with sibling `translation-quality-reviewer`: near-identical opener ("A reviewer of translations, translation choices…" vs "…translation-quality claims, and corpus-based…") and both "Use when" clauses begin "A translation or draft is…", diverging only in the last clause. This is the dispatch string; the body `when_not_to_use` disambiguation is invisible at selection time, so a generic "review my translation" risks the wrong lens. Compounded by the truncated "Not for" clause picking the generic "does not translate/certify" line over a sibling-differentiating one (SF-4 of agent-design lens). | Rewrite the terse description opener so the distinguishing lens is first (e.g. "A reviewer of translation strategy and descriptive method — not corpus-based quality scoring; see translation-quality-reviewer"); prefer a `when_not_to_use` entry that names a sibling for the "Not for" clause. Apply the distinguishing-first fix across all four corpus-split siblings, then re-run `cli export`. |

---

## should-fix

| Where | Problem | Fix |
|-------|---------|-----|
| `tests/golden-tests.yaml` (coverage gap) | `when_not_to_use` names three load-bearing sibling routes but only equivalence has a negative-routing test (NR-003). Corpus/QA-scoring → `translation-quality-reviewer` and technical/scientific → `technical-translation-advisor` are asserted but never behaviourally verified. | Add NR-004 (corpus/QA-metric scoring → `do_not_invoke`, refs `translation-quality-reviewer`) and NR-005 (scientific/technical terminology-risk → `do_not_invoke`, refs `technical-translation-advisor`), matching the NR-003 pattern. |
| `profile.yaml` `handoff_rules` (L91-97) | `when_not_to_use` names three sibling destinations; `handoff_rules` — the authoritative "who owns what next" section — names only translator/commissioner + a generic "owning specialist," omitting all three siblings. Internal inconsistency between the two sections that jointly define scope. | Add a `handoff_rules` bullet listing the three sibling routes, mirroring `when_not_to_use`, so the section is self-sufficient without cross-reference. |
| `tests/test-results.md` (L11 count; L7 self-check) | States "2 negative-routing" tests; `golden-tests.yaml` has carried 3 since v1.4.0 (drift across 3 bumps). The Phase-8 self-check section points at CLI output rather than recording the actual PASS/WARNING verdict for v1.7.0. | Correct count to 3; regenerate mechanically on each bump or drop the hand-count; inline the self-check verdict per version. |
| `principles/principles.yaml` (missing); `skills/text-type-skopos-and-the-brief/SKILL.md` | Nord's "function plus loyalty" was extracted (`analysis/claims.jsonl` C00155, confidence high) but never promoted or wired in. The skopos cluster (P009/P062/P078/P079/P107/P108) stresses purpose-driven freedom with no counterbalancing loyalty check — yet loyalty is the field's safeguard against skopos "anything goes," missing from exactly the skill meant to review skopos choices. | Promote a principle from C00155 and wire it into `text-type-skopos-and-the-brief`'s procedure/anti-patterns alongside P108, so a skopos-serving-but-source-disloyal rendering can be caught. |
| `principles/principles.yaml` P105; `skills/equivalence-orientations-and-effect/SKILL.md` (step 5) | P105 frames the formal/dynamic-equivalence choice as a near-binary switch ("formal for academic/legal, dynamic elsewhere"). Nida's account is a continuum of degree; the package already treats overt/covert (P021) and domestication/foreignization (P024) as clines — asymmetric. | Add a "matter of degree / continuum, not a binary rule" clause to P105 and the skill step, mirroring the cline language used for P021/P024. |
| all 12 `skills/*/SKILL.md` (Provenance H2) | Each file restates its full principle-ID list in prose immediately below the identical list in the YAML frontmatter — pure per-file duplication, token cost with no new signal. | Replace the body enumeration with a pointer to the frontmatter `provenance` block. |

---

## nice

| Where | Problem | Fix |
|-------|---------|-----|
| all 12 skills | No body "When NOT to use" section; negative scope is packed into the dense `description`. | Add a short negative-scope subsection per skill and trim the description to primary triggers. |
| `skills/meaning-signification-and-equivalence-critique/SKILL.md` vs `skills/hermeneutics-and-the-limits-of-translatability/SKILL.md` | Shared surface vocabulary (meaning/reference/signification) with no disambiguating sentence (lower risk — semiotics vs analytic-philosophy indeterminacy). | Add one clarifying routing line each: semiotic sign/code critique stays here; indeterminacy/philosophical-warrant claims route to hermeneutics. |
| `profile.yaml` `quality_bar[0]` citation `(P010,P011,P039,P046,P110)` | P110 is Toury's probabilistic laws (standardization/interference), not the "graded and mobile norms" claim; the exact-match principle P102 is uncited — over-stated grounding (substantive claim still backed by P046). | Swap P110→P102, or drop P110 from this bullet and reserve it for a standardization/interference rule. |
| `profile.yaml` body size | ~900-950 words vs 800-word soft budget (WARNING, non-blocking; under the 1000 FAIL). Known deferred item since v1.2.0; recent splits added prose without a compensating trim. | Word-count pass: share a lead-in for `when_not_to_use` route bullets; trim `handoff_rules` restatement of `canonical_owner`. |
| `profile.yaml` worked example "formal vs dynamic liturgical verse" | Opacity-risk clause cited to (P104,P162), which don't state it. | Re-cite the opacity-risk clause to P124/P180. |
| `principles/principles.yaml` P107 (Holz-Mänttäri) and P109/P121 (Baker six-level taxonomy) | Both described accurately but unnamed, unlike every other named theorist in the package (source claims C00146/C00155 carry the names) — weakens traceability and name-matching on caller references. | Restore "Holz-Mänttäri" to P107 and "(Baker)" to P109/P121 and the corresponding skill lines. |
| `principles/principles.yaml` P021 (House overt/covert), register skill step 2 | Presented as a "cline"; House's model is a forced per-text categorical choice. | Soften to a categorical judgement noting hybrid/borderline STs exist, reserving cline language for the domestication/documentary axes. |
| `principles/principles.yaml` P090 (register skill) | Bundles two separable critiques (Gricean maxims' cross-cultural bias; discourse frameworks fitting narrow-field over literary texts) into one causal-sounding sentence. | Decouple the two claims so "suits technical/legal" isn't read as a corollary of the cultural-bias claim. |
| `profile.yaml` `role` field | Uses build-internal jargon ("operating invariants" / compile_invariants) in the portable, platform-neutral field. | Reword to "The quality bar and forbidden behaviours below are review criteria, not instructions to translate…". |
| adapter operating-invariants block | Many of the 180 quoted invariants are translator-imperative ("Work the V&D ladder…"); only the Role-paragraph caveat keeps them review-only — a single point of failure if truncated. | Add a one-line reminder immediately above the "Operating invariants" heading: read every "do X" as "check whether X was done." |
| all 12 skills | Several procedure steps run 60-90+ words bundling 2-4 checks; a "step" isn't one executable action. No per-skill worked before/after example (only profile-level scenarios). | Split compound steps into lettered sub-bullets; add one compact worked example per skill (densest first). |

---

MUST_FIX_COUNT: 3
