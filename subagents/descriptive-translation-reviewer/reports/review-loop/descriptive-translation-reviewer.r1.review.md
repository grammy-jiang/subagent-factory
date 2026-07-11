# Review — descriptive-translation-reviewer (r1)

One review pass over `subagents/descriptive-translation-reviewer/` (profile v1.4.0, `status: ready`, Tier 2, 180 principles / 12 skills / 2 references).

## Deterministic gates (STEP 1)

| Gate | Result |
|------|--------|
| `validate_generated_package` | **PASSED** — 0 FAIL (phase8 = WARNING only, within budget) |
| `quote_scan` | PASS — no verbatim quotation |
| truncation grep (`…` / severed invariant) | clean — 0 hits |

No deterministic FAILs.

## LLM reviewer panel (STEP 2)

7 reviewers: agent-skills-advisor (must=1), profile-reviewer (must=1), faithfulness-reviewer (must=0),
ai-agent-engineering-reviewer (must=0), + 3 domain reviewers translation-equivalence / translation-quality /
technical-translation (must=0 each). Findings deduped below, most-severe first.

---

## MUST-FIX

### M1 — `text-type-skopos-and-the-brief` skill written in translate-it-yourself voice
- **where:** `skills/text-type-skopos-and-the-brief/SKILL.md` — Procedure steps 1–4, 6, 9, 12–14
- **problem:** ~half this skill's Procedure section uses first-person production-imperative voice ("make," "drive," "work," "adjust," "orient," "take," "apply," "treat") instead of the reviewer "Check that / Verify / Confirm" pattern used consistently by all 11 sibling skills. The Procedure is the recipe the agent executes step-by-step, so this phrasing reads as an instruction to *construct* a commission/brief rather than to *review whether one exists and is sound* — directly at odds with the profile's `forbidden_behaviours` no-production boundary.
- **fix:** Rewrite steps 1–4, 6, 9, 12–14 into "Check/Verify/Confirm that …" review voice matching the other 11 skills (e.g. "Check that the translation commission … was made an explicit instruction stating both the goal and the conditions for attaining it (P009)").

### M2 — package declares `status: ready` with an open, unresolved review round
- **where:** `reports/review-loop/descriptive-translation-reviewer.r5.review.md` (present) vs `profile.yaml` (`status: ready`, `agent_version: 1.4.0`), `CHANGELOG.md`, `provenance-ledger.md`
- **problem:** `r5.review.md` ends `MUST_FIX_COUNT: 2` but has **no** matching `r5.fix.done` marker (rounds 1–4 each have one), no v1.5.0 CHANGELOG/ledger entry, and no version bump. The package still declares `ready` at v1.4.0 as if the loop had converged to zero must-fix, but the last recorded round left 2 must-fix open — contradicts the repo's converge-to-zero release rule. (Note: this r1 pass downgrades r5's two must-fixes — anti-pattern/Procedure duplication is now NICE N8, the skill-overlap is now should-fix S2 — so a fresh convergence assessment is warranted, but the open-round-vs-`ready` contradiction must be resolved either way.)
- **fix:** Either (a) run the fix cycle, write `r5.fix.done` (or supersede it with this r1 loop), bump version, add CHANGELOG/ledger entries before calling ready; or (b) if r5 is stale, explicitly supersede it in the ledger Version History so no orphan open-must-fix report survives release.

---

## SHOULD-FIX

- **S1 — router `description` under-specifies boundary & sibling routes** *(profile-reviewer + ai-agent-engineering, deduped)*
  - **where:** `.claude/agents/generated/descriptive-translation-reviewer.md` frontmatter `description` (line 3); source `profile.yaml` `when_not_to_use`.
  - **problem:** The exported description (the only string the auto-router reads) collapses 5+5 bullet lists to one item each; it omits the highest-stakes boundary ("critiques, does not translate or certify") and 2 of the 3 sibling routes (`translation-quality-reviewer`, `technical-translation-advisor`). A translate-and-certify request could route here and be declined only mid-session.
  - **fix:** Compress each list into one comprehensive sentence including the "does not translate/certify" boundary and all three sibling routes.

- **S2 — `meaning-signification-and-equivalence-critique` step 6 leaks into equivalence-mechanism territory**
  - **where:** `skills/meaning-signification-and-equivalence-critique/SKILL.md` Procedure step 6 (P109).
  - **problem:** Step 6 instructs analysing/preserving equivalence "across word, above-word, grammar, thematic-structure, cohesion, pragmatic levels" — Baker's equivalence-levels mechanism the skill's own description assigns to sibling `translation-equivalence-advisor`. Crosses the stated theory-vs-mechanism line.
  - **fix:** Reword to stay on the theory side (name which level the meaning claim rests on, without selecting/evaluating a target rendering) and cross-reference the sibling by name.

- **S3 — quality-territory boundary vs `translation-quality-reviewer` under-differentiated**
  - **where:** `profile.yaml` `knowledge_partition.always_on` (`translation-quality-and-applied-studies`) vs `when_not_to_use` ("corpus-based quality metrics/QA scoring → `translation-quality-reviewer`").
  - **problem:** The only differentiator (corpus/QA scoring routes away) doesn't obviously exclude this reviewer's own quality content (Holmes map, process research, source-comparison quality judgement).
  - **fix:** Add one worked contrast showing a quality question that stays here vs one that routes to the sibling.

- **S4 — precedence miscite P114**
  - **where:** `profile.yaml` `source_of_truth_policy.precedence` (~L103–105).
  - **problem:** "brief's purpose governs (P062, P114)" — P062 (skopos hierarchy) grounds it; P114 (selective-preservation trade-offs) does not. (Also flagged r5 S8, still open.)
  - **fix:** Drop P114 or replace with a skopos-hierarchy principle (e.g. P107).

- **S5 — `forbidden_behaviours[3]` bundles two prohibitions under one citation set**
  - **where:** `profile.yaml` `forbidden_behaviours[3]` (~L89–90).
  - **problem:** "prescribing a single correct rendering" (grounded by P075) and "ignoring the brief/audience/function" (grounded by P062/P038) share one citation list. (r5 S13, open.)
  - **fix:** Split into two bullets, each citing only its grounding principles.

- **S6 — `when_not_to_use[0]` mixes citation styles**
  - **where:** `profile.yaml` `when_not_to_use[0]` (~L28–32).
  - **problem:** Full prose for one sibling route, arrow-shorthand for the other two — inconsistent in the field that already drove 4 rounds of router churn. (r5 S9, open.)
  - **fix:** Make all three sibling routes parallel in form.

- **S7 — `handoff_rules[1]` carries authoring meta-commentary in a body-counted field**
  - **where:** `profile.yaml` `handoff_rules[1]` trailing sentence (~L96–97).
  - **problem:** "Sibling-axis routing is stated once under when_not_to_use." is documentation about the profile's own structure, not runtime guidance — spends ~9 words of a thin budget. (r5 S11, open.)
  - **fix:** Delete the sentence; keep the note only in the ledger.

- **S8 — `when_to_use[0]` garden-path clause**
  - **where:** `profile.yaml` `when_to_use[0]` (~L17–18).
  - **problem:** "…reviewing the losses against the source and the brief by descriptive method, not a quality metric" — ambiguous attachment; this field seeds the exported routing description. (r5 S12, open.)
  - **fix:** Split into two clauses, e.g. "…assessed by descriptive method — reviewing losses against source and brief, not scored against a fixed quality metric."

- **S9 — body word budget near hard-FAIL**
  - **where:** `profile.yaml` body-counted fields collectively.
  - **problem:** ~946 words vs 800 soft-WARN / 1000 hard-FAIL — ~54 words headroom; last three bumps added net words without applying deferred trims. One more addition risks a check-14 FAIL.
  - **fix:** Apply the deferred trims (S7 delete, S8 tighten, S5 split without net add) now.

- **S10 — examples cover only `review` mode** *(profile-reviewer + ai-agent-engineering, deduped)*
  - **where:** `profile.yaml` `examples`.
  - **problem:** Both examples exercise `review`; neither `advise` nor `compare` (2 of 3 declared modes) has a worked example, including the advise-vs-equivalence-advisor routing line.
  - **fix:** Add one example each for `advise` and `compare`, or explicitly defer with owner/timeline in the ledger.

- **S11 — inconsistent skill `description` lead-in mood across the 12 skills**
  - **where:** all 12 `skills/*/SKILL.md` frontmatter `description`.
  - **problem:** 4 open "Use when…", 7 open "Reviews…", 1 (`literal-free-strategy-history-and-retranslation`) opens with imperative "Review a translation's placement…". Mixed convention hurts scanning/maintenance of the sole load-time trigger signal.
  - **fix:** Standardize on one lead-in pattern; fix the literal-free description to third person.

- **S12 — `register-discourse-and-audiovisual-constraints` description spends budget on generic boilerplate**
  - **where:** `skills/register-discourse-and-audiovisual-constraints/SKILL.md` frontmatter `description`.
  - **problem:** "flagging violations of the cited principles" is true of all 12 skills — no differentiating trigger signal.
  - **fix:** Drop the generic clause; front-load distinctive trigger vocabulary (register, discourse, subtitling/AVT, House's two axes).

- **S13 — `literal-free-strategy-history-and-retranslation` steps 4 & 15 in imperative voice**
  - **where:** `skills/literal-free-strategy-history-and-retranslation/SKILL.md` Procedure steps 4 (P036) & 15 (P173).
  - **problem:** "Default to sense-for-sense…", "Choose the target register…" read as translation commands, not review checks (same drift as M1, isolated to 2 steps).
  - **fix:** Reword to "Check that the translator defaulted to… / Check that the target register was chosen by…".

- **S14 — Berman's twelve deforming tendencies: "popularization" dropped from the enumerated list** *(technical-translation should-fix; translation-equivalence nice — deduped, higher severity taken)*
  - **where:** `principles/principles.yaml` P014; restated `skills/deforming-tendencies-and-translation-loss/SKILL.md` step 1.
  - **problem:** Berman pairs "ennoblement and popularization" as one tendency; P014's list names only "ennoblement". A reviewer checking "the twelve" via P014 alone misses the popularizing pole (it appears only later, separately, in P081).
  - **fix:** Amend P014 to "ennoblement and popularization" so the canonical pairing is visible where the twelve are enumerated.

- **S15 — Toury's norm structure names only two of three terms**
  - **where:** `principles/principles.yaml` P010 (with P023).
  - **problem:** P010 names "preliminary" and "operational" norms but never the foundational "initial norm" (adequacy-vs-acceptability orientation) that governs both; P023 has the concept without the term.
  - **fix:** Add the term "initial norm" to P010 or cross-reference from P023 so the initial→preliminary→operational structure is named whole.

---

## NICE

- **N1** — `principles.yaml` P047 (explicitation): "tends **always** to increase…" reads more absolute than Blum-Kulka's hedged original and pulls against the sentence's own "contested support" qualifier. Drop "always" → "tends to increase". *(translation-quality + technical, deduped.)*
- **N2** — `principles.yaml` P069 subtitling limit "38 Roman" chars used as a hard pass/fail; Díaz Cintas & Remael commonly cite ~37 (35–42 by convention). Verify against Munday's cited source. *(technical.)*
- **N3** — `principles.yaml` P150 / `hermeneutics…/SKILL.md` step 19: "principle of charity" is Wilson/Davidson's named label; Quine argues the substance without that tag. Drop the label or note "(later formalized by Davidson…)". *(translation-quality.)*
- **N4** — `principles.yaml` P056: distinctive Quine phrasing ("cantilever fashion", "Neutrinos lack mass" example) worth a source-anchor spot-check. *(translation-equivalence, low-confidence.)*
- **N5** — `reports/faithfulness-report.yaml` has no `rule_ref` for `examples[*].ideal_response`, `outputs.modes[*]`, `role`, `inputs` — all principle-cited but outside the 38 reviewed refs. Today's content checks out; add coverage next faithfulness pass. *(faithfulness.)*
- **N6** — `profile.yaml` `quality_bar[3]` ("re-coding, not omission") is most precisely grounded by P052; add it to the citation list. *(faithfulness.)*
- **N7** — `profile.yaml` `role` is one dense run-on bundling four claims; split so the review-only boundary stands alone. *(profile-reviewer / r5 N6.)*
- **N8** — two largest skills (`culture-ideology-power-and-rewriting` 20 princ, `hermeneutics-and-the-limits-of-translatability` 19) restate each principle as a Procedure check + mirrored Anti-pattern; consider merging a few closely related anti-patterns to trim length (justified redundancy for a reviewer, tier-2 cost only). *(agent-skills.)*
- **N9** — `descriptive-method-and-translational-norms` (P011/P101) and `translation-quality-and-applied-studies` (P007) both carry the "reconstruct-norm-from-behaviour-not-self-report" check; add a one-line cross-reference so the overlap reads as intentional. *(agent-skills.)*

---

## Positive notes

- All deterministic gates pass; no truncation, no verbatim quotation, adapter in sync, tier-consistency OK.
- 12 skills share a consistent template (Purpose / When / Procedure / Inputs / Output / Anti-patterns / References / Provenance), valid frontmatter, correct progressive-disclosure reference links, uniform Output contract.
- Domain grounding is unusually strong: three independent domain reviewers found **zero** theorist misattributions, garbled terms, or reversed claims across Jakobson/Catford/Vinay-Darbelnet/Nida/Newmark/Koller/Reiss/Vermeer/Nord/Toury/Even-Zohar/Chesterman/Venuti/House/Berman/Lefevere/Quine/Steiner/Spivak/Chaume/Pedersen. The register skill correctly disambiguates House's two same-named overt/covert axes.
- Tool boundary correct (Read/Grep/Glob only); no authority creep — forbidden_behaviours + handoff_rules correctly prevent producing translations or certifying.

MUST_FIX_COUNT: 2
