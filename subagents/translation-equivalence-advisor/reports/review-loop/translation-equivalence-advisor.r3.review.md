# Review Loop — round 3 — `translation-equivalence-advisor`

**Date:** 2026-07-12
**Profile version reviewed:** 1.2.0
**Method:** deterministic gates (validate, quote-scan, truncation) + 7 parallel reviewer lenses
(agent-skills, profile-readiness, faithfulness/over-claim, agent-design, and 3 domain
cross-checks: descriptive-translation-reviewer, translation-quality-reviewer,
technical-translation-advisor). Findings deduped across lenses; deterministic FAILs count as must-fix.

## Deterministic gates — ALL PASS

- `validate_generated_package` → **VALIDATION PASSED** (Phase 8 WARNING only: body 992w, under 1000w hard limit; all skill/reference authoring OK; all grounding unchanged).
- `quote_scan` → **PASS** — no potential verbatim quotation.
- ellipsis truncation grep → **no hits**.
- adapter invariant-truncation grep → **no hits**.

No deterministic FAILs. No round-3 must-fix from any lens. This round confirms round-2's v1.2.0
fixes (MF-1 receptor-response over-claim, MF-2 reversed P044 idiom hedge) are genuinely closed at
every locus — independently re-verified, not merely trusted from the ledger.

---

## Findings (all should-fix / nice; none must-fix)

### SHOULD-FIX

**S1 — P015 "masculine as unmarked" stated as flat cross-linguistic fact** *(domain — flagged independently by all 3 domain reviewers; highest cross-lens agreement)*
- Where: `principles/principles.yaml` P015; `skills/grammatical-equivalence/SKILL.md` step 3.
- Problem: "the masculine is usually the unmarked term" is unqualified. Only holds for binary masculine/feminine gender systems (chiefly Indo-European); many languages have no grammatical gender, and "masculine-as-default" is not universal. Also omits contemporary inclusive/non-binary strategies now standard practice (singular "they"; French point médian / "-e"; Spanish "elle"; noun repetition) and increasingly mandated by client/EU/corporate style guides — a brief-dependent choice, not a settled linguistic fact.
- Fix: Qualify P015 to "in languages with a masculine/feminine grammatical-gender system, the masculine is traditionally the unmarked term"; add that inclusive/gender-neutral conventions frequently override this and the translator should check brief/style guide before defaulting, treating it as a deliberate flagged choice.

**S2 — "similar audience response" / "equivalent effect" presented as a verifiable test** *(domain — flagged independently by descriptive-translation-reviewer AND translation-quality-reviewer)*
- Where: `principles/principles.yaml` P035, P036; `skills/dynamic-and-formal-equivalence/SKILL.md` step 8 + Output (line ~114, ~124); `references/translation-equivalence-key-concepts.md` "Dynamic equivalence" entry.
- Problem: Package treats "similar audience response" / "naturalness tested across the receptor culture" as a checkable adequacy criterion. This is the best-known durable critique of Nida's model (per Munday's survey): a source audience's original response is not independently measurable, so equivalent effect can only be inferred by analogy, never empirically verified. Risks the advisor certifying a rendering "adequate" on an unobservable criterion. Currency note: Nida & de Waard (1986) relabeled "dynamic" → "functional equivalence" to strip the emotive connotation; the glossary presents "dynamic equivalence" as settled final terminology.
- Fix: Add a caveat to P035/P036 (and the skill Output + glossary entry): treat "similar audience response" as an aspirational/regulative heuristic to argue from, not a verifiable success criterion; evidence for it is necessarily indirect (informant reaction, back-translation, comprehension trials). Note the later "functional equivalence" relabeling for currency.

**S3 — `always_on[0]` drops P095's conditional ("never erase" is absolute)** *(faithfulness — HEDGING_REMOVED)*
- Where: `profile.yaml` `knowledge_partition.always_on[0]`.
- Problem: "never erase a culturally embedded item merely to sound natural" is unconditional. Grounding P095 is explicitly conditional — retain/describe/annotate *when the foreign setting is part of the message*. The profile's own `examples[0].ideal_response` already gets this right ("where its foreignness carries meaning (P095)"), so the always_on line is internally inconsistent with its own example.
- Fix: Restore the conditional: "…never erase a culturally embedded item merely to sound natural when its foreignness carries meaning for the text (P095)" — matching the example wording.

**S4 — `always_on[4]` internally contradictory: absolute "do not transfer" vs purpose-driven P091** *(faithfulness)*
- Where: `profile.yaml` `knowledge_partition.always_on[4]`.
- Problem: Opens with an absolute prohibition ("Do not transfer the source text's cohesive devices") from P038, but the same sentence cites P091, which frames this as a purpose-dependent judgment ("following source norms minimizes meaning change"). The compound rule reads more absolute than its own cited grounding (P091) supports and is internally contradictory.
- Fix: Reframe as default-with-exception: "As a default, rework rather than transfer source cohesive devices to the target's own preferences/frequencies, but decide whether to follow source cohesion or approximate target norms by the translation's purpose (P038 as default; P091 as the purpose-driven exception)."

**S5 — `compare` mode declared in profile has no matching Output contract in any skill** *(skill-authoring)*
- Where: `profile.yaml` outputs.modes `compare` (lines ~53-57); all 9 `skills/*/SKILL.md` `## Output` sections.
- Problem: Profile declares a `compare` mode whose output is a side-by-side of what each option favours/costs ending in a weighted recommendation. No skill Output section describes a side-by-side shape; all are single-recommendation formats. Closest owner `dynamic-and-formal-equivalence` still doesn't produce the declared layout, and cross-strategy "A vs B" for a segment is owned by no skill — the declared mode contract is not executable from skill guidance.
- Fix: Add an explicit compare-mode output clause to `dynamic-and-formal-equivalence/SKILL.md` Output (side-by-side favours/costs → purpose-weighted call), plus a one-line "lay out side-by-side before recommending" note to the level-specific skills whose Procedure already weighs options (word-level, collocation-idiom).

**S6 — P100 scopes back-translation too narrowly; omits its legitimate QA role** *(domain — translation-quality-reviewer)*
- Where: `principles/principles.yaml` P100; `skills/dynamic-and-formal-equivalence/SKILL.md` step 7.
- Problem: Back-translation framed only as exposing target structure to a monolingual reader, "a theoretically unsound compromise that never reproduces meaning." Omits its most common real-world use: a standard QA check in regulated/high-stakes translation (pharma, medical, legal, patient-facing) routinely required by clients/regulators to catch meaning-distorting errors. Sibling `technical-translation-advisor` already treats it as a limited quality check; this narrower framing could mislead a caller into dismissing a legitimate technique.
- Fix: Broaden P100 to acknowledge back-translation's limited-but-legitimate QA role (while keeping the caution that it cannot itself certify semantic equivalence).

**S7 — Description omits concrete trigger phrasing for text-level skill** *(skill-authoring)*
- Where: `skills/text-level-approach-and-limits-of-equivalence/SKILL.md` frontmatter `description`.
- Problem: The one skill whose natural trigger is a *generic* caller phrasing ("is this translation 'right' / 'literal enough' / 'faithful'?"). That phrasing lives only in the body "When to use" (line ~67) — after the skill would already need selecting. The frontmatter (the sole routing signal) uses only academic vocabulary, a weaker lexical match to how callers actually phrase this → under-triggers.
- Fix: Fold the concrete trigger phrase into the description, e.g. "Reviews whether a translation is 'right,' 'literal enough,' or 'faithful' overall against a relative, whole-text standard… for calls that don't name a single equivalence level."

**S8 — Adapter frontmatter `description` truncates role + when-to-use mid-clause** *(agent-design)*
- Where: `.claude/agents/generated/translation-equivalence-advisor.md` line 3 (auto-generated router description).
- Problem: The dispatcher-matched one-liner stops at "…grammar, information structure" (drops cohesion, pragmatics, register/form, whole-text) and stops when-to-use at "marked structure" (drops the form-bound / receptor-language clause). A caller asking about register, cohesion, pragmatics, or whole-text equivalence has no routing-layer signal for those in-scope capabilities. NOTE: regenerate via export, do NOT hand-edit the adapter.
- Fix: Regenerate the description to preserve complete clauses for domain scope + at least one full when-to-use item + the not-for item. If the generator truncates at a fixed char count, truncate at clause boundaries (or raise the budget) in the export template.

**S9 — Untracked should-fix from round 2 (SF-4 per-skill example) + no recorded independent round-3 verification** *(profile-readiness / process)*
- Where: `reports/review-loop/` (only r1/r2 artifacts); `provenance-ledger.md` + `CHANGELOG.md` v1.2.0.
- Problem: Round-2 SF-4 ("add a short `## Example` to each of the 9 skills") was neither implemented (zero `## Example` hits) nor logged in the v1.2.0 "Deferred" list — it fell through the resolve-or-defer discipline. Separately, v1.2.0's own MF-1/MF-2 fixes were bundled into the round-2 commit with no independent post-fix pass recorded in the package (this r3 review now fills that gap and finds both fixes sound).
- Fix: Either add per-skill worked examples (cheap — restate existing profile-level examples at skill scope) or add an explicit SF-4 deferred-with-reasoning line to the ledger/CHANGELOG. Record this r3 review as the independent must-fix=0 verification consistent with the driver's merge-gating rule.

### NICE

- **N1** — `quality_bar[0]` extends "no one-to-one match" to "phrase level" while cited P037 is word-scoped. Drop "or phrase" or add a phrase-level citation. *(faithfulness)*
- **N2** — P009 Chinese adversative passive (被 bèi): accurate as traditional/classical default but connotation has weakened in modern/technical Mandarin (translationese influence). Add a currency note to check frequency-in-context rather than assume adversative reading. *(domain ×2)*
- **N3** — P110 "let a translation pass for an original" presented as unqualified good; brushes the domestication/fluency critique (Venuti). Sibling `descriptive-translation-reviewer` owns that lens and package carries the P022/P074 counterweight, so low priority. Optional: note naturalness is register/brief-dependent. *(domain)*
- **N4** — P033 states Gricean maxims "reflect English-culture values" as settled fact; soften to "have been criticized by some scholars as reflecting Anglo-communicative norms." *(domain)*
- **N5** — Coverage: Baker's componential/semantic-feature analysis is a distinct word-level diagnostic not quite covered by the semantic-field treatment (P012). Optional: add a brief principle/procedure line. *(domain)*
- **N6** — Near-identical surface wording "trace participants… through reference" in `thematic-and-information-structure` step 5 and `cohesion-and-texture` step 5 (different principles: givenness vs anaphora). Reword one to disambiguate lens. *(skill-authoring)*
- **N7** — Identical advise/review boilerplate sentence repeated verbatim across all 9 `## Output` sections; optional DRY hoist into the key-concepts reference. *(skill-authoring)*
- **N8** — Role sentence lists only advise+review, omits the third declared `compare` mode; add "recommends or compares" for role/mode coherence. *(agent-design)*
- **N9** — Provenance currency: package distills Baker (1992, 1st ed.); a one-line "reflects the 1992 first edition" note pre-empts an edition-agnostic assumption (2011/2018 eds. add corpus/ethics). *(domain)*
- **N10** — `golden-tests.yaml:3` `generated_at: 2026-07-11` not bumped with profile_version 1.2.0; cosmetic. *(profile-readiness)*
- **N11** — Optional: point Skopos/House/DTS-norms questions to sibling packages via a `handoff_rules`/`when_not_to_use` line, so the two-source scope boundary is explicit not silent. *(domain)*

---

## Verified clean (no issue)

Tool boundary Read/Grep/Glob only (no Write/Bash/MCP) — correct read-only advisor; DO-NOT-EDIT
adapter header present; principle→skill partition complete P001–P116, zero duplicates/orphans;
progressive disclosure intact (references linked not inlined); no authority creep (never delivers
final text, never certifies one answer); faithfulness report all 29 rule_refs
EXACT_SUPPORT/WITHIN_SCOPE, none CONTRADICTED; both round-2 must-fixes genuinely closed;
116 principle-behaviour tests + 5 golden + 4 routing/missing-context, schema-valid.

MUST_FIX_COUNT: 0
