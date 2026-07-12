# Review Loop — translation-quality-reviewer — Round 4

Consolidated from deterministic gates + 7 reviewer lenses (agent-skills, profile,
faithfulness, ai-agent-engineering + 3 domain: equivalence, descriptive, technical).
Findings deduped across lenses, most-severe first.

## Deterministic gates — ALL PASS (0 must-fix)

- `validate_generated_package` → VALIDATION PASSED (Phase 8 = WARNING, non-blocking; see S2).
- `quote_scan` → PASS, no verbatim quotation.
- ellipsis-truncation grep → no hits.
- adapter parenthetical-severance grep → no hits.

---

## MUST-FIX (3)

### M1 — P042/P075 House model-version mapping is self-contradictory and likely misattributed
- **where:** `principles/principles.yaml:856-861` (P042); `:1409-1418` (P075); `skills/register-field-tenor-mode-analysis/SKILL.md:70,78,98` (steps 5/13 + anti-pattern); surfaces in `profile.yaml:74` quality_bar[3] (P042 cited).
- **severity:** must-fix (cross-corroborated by 3 independent domain reviewers: equivalence=must-fix, technical=should-fix, descriptive=should-fix).
- **problem:** P042's own Field/Tenor/Mode list already assigns "participant relations and stance" to **Tenor**, then claims this "reflects House's earlier model, which placed participation under Mode; her revised model reassigns Participation to Tenor." So the principle describes the *revised* split while calling it the *earlier* one, and **never states what the earlier model's Tenor/Mode split actually was** — the two "models" are indistinguishable, and the skill's own anti-pattern ("establish which model is in force before flagging") is unusable because the earlier mapping is never given. Independently, the migration claim itself is doubtful on domain grounds: standard TS descriptions (1977 + 1997 "Model Revisited") keep Participation under **Mode** in both versions; the reassignment, if real, is specific to House's 2015 integrative model (grounding anchor heading: "Towards a New Integrative Model of TQA"), not the "revised model" most callers assume. As written, a reviewer who correctly keeps Participation under Mode for a classic-House analysis would be told they are wrong.
- **fix:** Rewrite P042 to state the earlier-model split explicitly and separately from the revised split, and **name the specific editions** contrasted (e.g. "House 1997 revised" vs "House 2015 integrative"). Verify the Participation Mode→Tenor claim against the specific House 2015 page behind P075's claims (C00418–C00421) before finalizing; if the source does not support the migration, correct P042/P075 rather than just de-contradicting them. Align register-analysis skill step 5 + anti-pattern to the corrected mapping.

### M2 — P056 mis-grounded citation in quality_bar[3] (cultural-filtering clause)
- **where:** `profile.yaml:75` (quality_bar[3]); corroborated `reports/faithfulness-report.yaml:28-36`.
- **severity:** must-fix (profile lens; **verified by direct inspection** — `principles/principles.yaml:1107-1110`).
- **problem:** quality_bar[3] reads "…cultural filtering is likewise compared source-to-target (P056, P137)." P137 grounds cultural filtering correctly, but **P056 is about multifactorial modelling of complex variation**, not cultural filtering ("For complex variation… recommend multifactorial modelling when multiple explanatory variables are plausible"). P056 is absent from the cultural-filtering skill's own citation set (always_on[5]) and is correctly used elsewhere for multifactorial modelling (quality_bar[4] line 77, forbidden_behaviours, precedence). This is an orphan/mis-grounded citation — violates the provenance rule (every field traceable to a QID that actually supports it). It survived 3 review-loop rounds because the faithfulness-report note echoed the citation without checking the principle text.
- **fix:** Drop `P056` from the cultural-filtering clause of quality_bar[3] (P137 alone grounds it), or replace with a correct cultural-filtering ID; correct the matching faithfulness-report note; re-export adapter + bump `agent_version`.

### M3 — Anti-patterns sections are a 1:1 negated restatement of Procedure in all 12 skills
- **where:** every `skills/*/SKILL.md` (e.g. `corpus-design-and-methodology` Procedure L77-111 vs Anti-patterns L130-163; `error-analysis-and-evaluation-discipline` L71-93 vs L106-122; identical pattern in the other 10).
- **severity:** must-fix (agent-skills lens).
- **problem:** In every skill, "Anti-patterns to flag" is an essentially exhaustive negated paraphrase of "Procedure" (8-vs-8, 15-vs-15, 19-vs-19…) — no thresholds, no paired good/bad examples, no new decision content. This ~doubles every body's token cost with zero added signal, contradicting the package's own quality bar ("every line must earn its token cost") and progressive-disclosure invariants (P001/P005/P029/P088/P114). Duplication compounds when a single review loads multiple skills at once.
- **fix:** Drop the standalone Anti-patterns section and fold a short caution into the relevant Procedure step, OR make Anti-patterns earn distinct value — one paired good/bad example per cluster rather than a negated restatement of every step.

---

## SHOULD-FIX

### S1 — P116-grounded register-cluster rule is over-broadened (faithfulness)
- **where:** `profile.yaml:74` quality_bar[3] + `:130-135` always_on[3], grounded in P116.
- **problem:** Rule states as a blanket criterion "Register… compared from co-occurring feature clusters, not isolated frequencies." P116's statement scopes the cluster-over-counts method to "When adapting register-analysis tools to translation" (corpus/frequency tooling), not every qualitative Tenor/Mode critique. SCOPE_BROADENED candidate — "in this context prefer clusters" risks reading as "always require clusters."
- **fix:** Narrow to "where corpus/frequency evidence is used…", add a second grounding principle for purely qualitative register review, or soften to "prefer" matching P116's conditional framing.

### S2 — Body-size WARNING (~950 words) is an unaccepted regression
- **where:** `profile.yaml` body fields vs `provenance-ledger.md:44-89`.
- **problem:** This is the validator's Phase-8 WARNING. Ledger's 1.2.0 says the body was trimmed to 800w clearing the WARN; 1.3.0's MF1/MF3 added words back (~950w, over the 800 WARN, under the 1000 FAIL) without re-checking or documenting the regression.
- **fix:** Trim ~150w (heaviest: quality_bar ~168w, when_to_use ~157w, when_not_to_use ~120w) back under 800, OR explicitly accept the WARNING in the ledger with trade-off reasoning.

### S3 — golden-tests `profile_version` stale
- **where:** `tests/golden-tests.yaml:4` (`profile_version: 1.0.0`) vs `profile.yaml:4` (`agent_version: 1.3.0`).
- **problem:** Never bumped through 1.1.0→1.3.0; metadata drift vs generated-artifact-policy version discipline.
- **fix:** Bump `profile_version` to 1.3.0 on next export.

### S4 — chinese-prose skill omits Yu Guangzhong's two most-cited symptoms (的-stacking, 被-passive)
- **where:** `skills/chinese-prose-and-europeanization/SKILL.md` (P119-120, P149-150).
- **problem:** Covers concision/connectors/idiom-flattening/nominalization but omits attributive/possessive 的 over-stacking and 被-passive overuse — arguably the single most-identified diagnostics in Yu's essay. A reviewer applying only this skill misses them.
- **fix:** Check if these claims were distilled then dropped in clustering; if in source, add a principle/anti-pattern for each; if genuinely absent from the digest, note the coverage gap in the skill scope.

### S5 — P034 target-orientation vs House equivalence framing is unscoped (equivalence)
- **where:** `principles/principles.yaml` P034 vs P030/P038/P059/P006; `skills/descriptive-studies-and-translational-norms/SKILL.md:68` vs `skills/overt-covert-translation-and-equivalence/SKILL.md:80,82`.
- **problem:** House's TQA is source-profile/equivalence-centered by design; P034 (Toury/DTS target-orientation) is listed as a general unscoped principle that could be applied to a House-model overt/covert case where it directly clashes with P030/P038.
- **fix:** Add a scoping note (parallel to the existing triage note in overt-covert L69-73) that P034 applies within descriptive/corpus-norm reconstruction, not within a House-model equivalence assessment.

### S6 — Significance-testing discipline siloed to Russian-field skill (descriptive)
- **where:** `skills/russian-corpus-and-interpreting-research/SKILL.md:66` (P057) vs `skills/corpus-design-and-methodology` (P078, P135).
- **problem:** "pair descriptive indicators with significance testing + effect sizes before interpreting group differences" is stated only for Russian interpreting; a corpus-TS expert expects it as a general discipline for any quantitative comparable/parallel-corpus claim.
- **fix:** Promote a general "pair frequency/concordance differences with significance testing + effect sizes" rule into corpus-design-and-methodology; have P057/P058 read as a domain-specific instance.

### S7 — Provenance boilerplate cites all 5 sources in every skill
- **where:** each skill's `## Provenance` sentence (e.g. `chinese-prose-and-europeanization/SKILL.md:74`, `russian-corpus-and-interpreting-research/SKILL.md:101`).
- **problem:** Identical five-source list in all 12 regardless of the principles the skill owns. chinese-prose owns only Yu-Guangzhong principles; russian-corpus owns only Dayter & Grabowski. Citing all five weakens the audit trail.
- **fix:** Make the Provenance sentence per-skill — name only the source(s) actually grounding the listed principle IDs.

### S8 — Repeated verbatim scope-boundary in every skill's Inputs/Output
- **where:** Inputs bullet 2 + Output closing sentence, identical across all 12 (e.g. `translation-universals-and-the-third-code/SKILL.md:68-69,72-73`).
- **problem:** The "reviews… does not produce the finished translation/publication decision" boundary is already at profile level (forbidden_behaviours/handoff_rules); restating in full in every body is low-signal filler.
- **fix:** Shorten to a one-clause reminder or drop (profile boundary covers it).

### S9 — corpus-design procedure lacks the triage grouping used by sibling skills
- **where:** `skills/corpus-design-and-methodology/SKILL.md:77-111` (15 flat steps).
- **problem:** 5 comparable-length skills open with a "Triage first" grouping sentence; corpus-design (2nd-longest procedure) is a flat wall of 15 — inconsistent.
- **fix:** Add a triage preamble grouping the 15 steps (corpus-type selection / comparability+normalisation controls / evidence-integration).

### S10 — One-directional sibling routing to descriptive-translation-reviewer (cross-package)
- **where:** `profile.yaml:35-38` when_not_to_use[1] vs `subagents/descriptive-translation-reviewer/profile.yaml:17-35`.
- **problem:** This package routes qualitative/single-text norm claims to descriptive-translation-reviewer, but that sibling has no reciprocal bullet routing quantitative/corpus-empirical norm claims back here (translation-equivalence-advisor does carry the reciprocal). Not fixable inside this package.
- **fix:** Follow-up — add a reciprocal `when_not_to_use` bullet in `descriptive-translation-reviewer/profile.yaml`. Not release-blocking here.

---

## NICE

- **N1** (faithfulness): P118 is Bible-scoped but cited in quality_bar[1]/always_on[1] for a domain-general metadata-control claim already grounded by P050/P135 — grounding-precision nit; drop P118 or add a Bible qualifier.
- **N2** (faithfulness): P125 cited in forbidden_behaviours[3] but doesn't ground either half of the statement (P061/P134 already do) — stray citation; replace or drop.
- **N3** (technical): "iconic linkage" collides with sibling `technical-translation-advisor`'s Byrne sense (consistency-reuse) vs House's cohesion-device sense — add a one-line disambiguating gloss in the skill.
- **N4** (equivalence): "Corpus support for Genre" (P075) is vague on Genre's superordinate position over Register; clarify what "corpus support" means operationally.
- **N5** (descriptive): universals skill omits Chesterman's S-universal/T-universal distinction — naming it sharpens "wrong corpus type for this claim" diagnosis.
- **N6** (descriptive): P083's "only from a corpus of source texts and their translations" reads Toury's textual-primary requirement too strongly — add a one-clause caveat that extratextual evidence (prefaces, critical statements) is admissible-but-weaker corroboration.
- **N7** (descriptive): third-code-vs-translationese dichotomy (P139) is Baker's/House's framing, not field-wide consensus (Gellerstam uses "translationese" neutrally) — add a one-line note so a caller using the neutral sense isn't over-corrected.
- **N8** (agent-design): frontmatter `description` crams role+use+not-for into one ~300-char sentence (factory-wide template convention, not package-specific).
- **N9** (agent-design): when_not_to_use bullets 1 and 4 both express "doesn't produce/certify a final answer" — optional consolidation.
- **N10** (skills): `applied-corpus-tools-and-textual-devices` 10-step flat procedure — optional light triage grouping.
- **N11** (profile): quality_bar[3] fuses register-comparison + cultural-filtering checks (two citation sets) under one bullet — optional split for cleaner auditing (independent of M2).

---

MUST_FIX_COUNT: 3
