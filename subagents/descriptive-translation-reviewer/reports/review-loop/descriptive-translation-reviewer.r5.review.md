# descriptive-translation-reviewer — Review Loop Round 5

Package: `subagents/descriptive-translation-reviewer/` (profile v1.4.0)
Lenses: deterministic gates + 7 subagent reviewers (agent-skills, profile, faithfulness,
ai-agent-engineering, translation-equivalence, translation-quality, technical-translation).

## Deterministic gates — ALL PASS

- `validate_generated_package` → **VALIDATION PASSED** (0 FAIL, 0 WARN)
- `quote_scan` → **PASS** (no verbatim quotation)
- ellipsis-truncation grep → clean
- severed-parenthetical grep → clean

## Per-lens must-fix counts

| Lens | MUST_FIX |
|------|----------|
| agent-skills-advisor (skill authoring) | 2 |
| profile-reviewer (release readiness) | 0 |
| faithfulness-reviewer (over-claim) | 0 |
| ai-agent-engineering-reviewer (agent design) | 0 |
| translation-equivalence-advisor (domain) | 0 |
| translation-quality-reviewer (domain) | 0 |
| technical-translation-advisor (domain) | 0 |
| **Deduped total** | **2** |

---

## MUST-FIX (2)

### M1 — Anti-patterns sections duplicate the Procedure ~1:1 in all 12 skills
- **where**: systemic — e.g. `skills/descriptive-method-and-translational-norms/SKILL.md:70-93` (Procedure) vs `:104-126` (Anti-patterns); `skills/culture-ideology-power-and-rewriting/SKILL.md:69-91` vs `:102-124`; same in all 10 others.
- **severity**: must-fix (skill-authoring)
- **problem**: Each Anti-pattern bullet restates its matching Procedure step in the negative — a mirrored restatement of the full principle set, not a distinct failure-mode catalogue. Doubles the on-trigger (level-2) load cost of every one of 12 skills for zero incremental signal; violates conciseness / progressive-disclosure doctrine (P001/P005/P029/P088/P114).
- **fix**: Drop Anti-patterns (fold a short "watch for" clause into each Procedure step), OR cut to only the 3–5 highest-impact failure modes per skill not already implied by the Procedure, moving exhaustive per-principle detail into `references/descriptive-translation-evidence-notes.md` for lazy load.

### M2 — Two Venuti-adjacent skills overlap with no tie-breaker
- **where**: `skills/domestication-foreignization-and-visibility/SKILL.md:1-8` (+`:68` P087) and `skills/culture-ideology-power-and-rewriting/SKILL.md:1-8` (+`:80` P050).
- **severity**: must-fix (skill-authoring)
- **problem**: Both cover fluency/invisibility, canonization, institutional/ideological shaping. Three other skills in the package carry an explicit "Tie-breaker" description sentence; these two do not, so a case like "a fluent translation domesticates the foreign because the publisher's ideology/canon demands it" has no deterministic route. Breaks the "distinct, non-overlapping lens" requirement.
- **fix**: Add a one-sentence tie-breaker to each description — domesticating/foreignizing axis + translator-invisibility stays in `domestication-foreignization-and-visibility`; institutional agents, patronage, feminist/postcolonial reading, reception/paratexts route to `culture-ideology-power-and-rewriting` (mirror sentence on the other).

---

## SHOULD-FIX (deduped)

### S1 — Frontmatter `description` under-represents the highest-stakes boundary
- **where**: `.claude/agents/generated/descriptive-translation-reviewer.md:3` (and `profile.yaml` description source).
- **lens**: ai-agent-engineering
- **problem**: Frontmatter "Not for" clause surfaces only the sibling-routing exclusion, omitting the higher-stakes `when_not_to_use` boundaries (`profile.yaml:33-34`: "wants the finished/revised translation end to end", "wants one guaranteed-correct rendering"). This terse line is what an orchestrator sees first, raising odds of routing a translate-and-certify request here before the body's `forbidden_behaviours` are read.
- **fix**: Compress the "does not translate / does not certify" boundary into the frontmatter description, alongside or in place of the sibling-routing clause.

### S2 — `advise` mode leans on one role sentence to reframe ~150 imperative invariants as review criteria
- **where**: `profile.yaml:19` (role) vs invariants phrased as translator instructions, e.g. adapter `:104` (P045), `:274` (P164), `:144` (P069).
- **lens**: ai-agent-engineering
- **problem**: Many operating invariants are first-person how-to-translate imperatives. Only a single role clause ("these are review criteria, not instructions to translate") + global forbidden_behaviours stops the `advise` mode reading them as license to draft. `advise`'s trigger ("which principle/strategy fits") invites a "so what should I write" pull.
- **fix**: Rephrase invariants in review-voice at generation ("check whether…", "flag if…"), OR reinforce the no-production boundary inside the `advise` mode trigger/output spec.

### S3 — `translation-quality-and-applied-studies` overlaps sibling `translation-quality-reviewer` with no in-skill boundary note
- **where**: `profile.yaml:31` vs `skills/translation-quality-and-applied-studies/SKILL.md:59-60,68`.
- **lens**: agent-skills
- **problem**: Skill trigger language (corpus, CAT/MT, process-research) sits inside territory the profile disclaims to a different subagent, yet the skill (unlike the equivalence cluster) restates no boundary in its own description.
- **fix**: Add a boundary clause: corpus/QA-scoring outputs → sibling `translation-quality-reviewer`; this skill reviews whether the *evaluation method itself* was sound.

### S4 — Procedure sections are flat unordered principle-checklists, not sequenced recipes
- **where**: e.g. `skills/culture-ideology-power-and-rewriting/SKILL.md:69-91` (21 steps), `skills/hermeneutics-and-the-limits-of-translatability/SKILL.md:68-89`, `skills/text-type-skopos-and-the-brief/SKILL.md:63-80`.
- **lens**: agent-skills
- **problem**: Each "step" is one principle restated as an imperative, ordered by principle ID, not grouped into execution phases (P014 asks for an operational recipe). Pushes the full principle catalogue into the always-on-trigger body.
- **fix**: Restructure each Procedure into 3–6 synthesized phases (locate claim → apply lens checks → rank & emit); move per-principle granularity to the reference doc, cited by ID.

### S5 — Koller's five equivalence relations enumerated inconsistently (four vs five)
- **where**: `principles/principles.yaml:2350-2366` (P106, five — correct) vs `:2603-2622` (P121, drops the fifth); propagated to `skills/meaning-signification-and-equivalence-critique/SKILL.md:71,95` (incomplete) vs `skills/equivalence-orientations-and-effect/SKILL.md:73` (correct).
- **lens**: technical-translation (domain)
- **problem**: P121 and the meaning/signification skill omit Koller's **formal/expressive** (formal-aesthetic) equivalence — exactly the category most relevant to literary/poetic equivalence critique, the skill's own subject. A reviewer following that skill would never be prompted to check wordplay/meter/rhetorical form.
- **fix**: Add "formal (formal-aesthetic/expressive)" to P121's list and to `meaning-signification-and-equivalence-critique` procedure step 8 + its anti-pattern, matching P106.

### S6 — House's overt/covert error taxonomy mischaracterized as a "severity" scale
- **where**: `skills/register-discourse-and-audiovisual-constraints/SKILL.md:51` (Purpose note).
- **lens**: technical-translation (domain)
- **problem**: House's covertly-/overtly-erroneous distinction is about error *type/detectability* (dimensional register/genre mismatch visible only via source comparison vs denotative/system-breach mismatch), not a severity gradient. Calling it "severity" risks a reviewer down-prioritizing covert errors — which are the harder-to-catch, often more consequential kind, cutting against the package's own P044 ("errors that pass silently").
- **fix**: Reword the note: the error taxonomy classifies error *type/origin*, not severity; drop the "grades severity" phrasing.

### S7 — P021 merges House's overt/covert cline with an unrelated "version vs translation" claim
- **where**: `principles/principles.yaml:553-573` (P021), used at `skills/register-discourse-and-audiovisual-constraints/SKILL.md:64`.
- **lens**: translation-equivalence (domain)
- **problem**: P021 states House's overt/covert typology (accurate) then appends "produce a version rather than a translation when the source genre has no equivalent target form" with an `applies_when` (unstable/oral source) that isn't part of House's theory; `derived_from_claims` mixes two distant claim ranges. A reviewer citing P021 could misattribute the version-vs-translation point to House.
- **fix**: Split into two principles — keep P021 strictly to House's cline; re-home the "version rather than translation" claim as its own principle with its own grounding + scope.

### S8 — P114 mis-cited for the equivalence/function precedence rule (dedup: faithfulness + profile)
- **where**: `profile.yaml:104-105` (`source_of_truth_policy.precedence`) and `:88` — "when equivalence orientation and function conflict, the brief's purpose governs (P062, P114)".
- **lens**: faithfulness + profile (deduped)
- **problem**: P062 (skopos hierarchy) grounds this fully; P114 is about selective-preservation trade-offs generally and does not establish that the brief governs over equivalence orientation.
- **fix**: Drop P114 from the citation or replace with a skopos-hierarchy principle (e.g. P107).

### S9 — Sibling-routing bullet mixes prose + arrow notation
- **where**: `profile.yaml:28-32` (`when_not_to_use[0]`).
- **lens**: profile
- **problem**: First sibling in prose ("Route to `translation-equivalence-advisor` for…"), other two in arrow shorthand ("→ `translation-quality-reviewer`"). This is the field that drove 4 rounds of router churn; internal inconsistency = maintainability risk.
- **fix**: Split into three parallel bullets, one per sibling, one consistent form.

### S10 — Body word-count headroom thin (~950–960 words vs 1000 hard-FAIL)
- **where**: body-counted fields collectively (`profile.yaml` role/when/modes/quality_bar/forbidden/handoff/precedence + inputs.required).
- **lens**: profile
- **problem**: Ledger tracked ~55 words/round growth toward the 1000 `_BODY_FAIL_WORDS` cap; round 4 added an `inputs.required` split without applying the deferred S7 trim. Still PASS but headroom is thin; any further broadening risks FAIL.
- **fix**: Apply the deferred trim now — deleting the S11 meta-sentence + tightening S12 both help.

### S11 — `handoff_rules[1]` ships authoring meta-commentary in a body-counted field
- **where**: `profile.yaml:97` — trailing "Sibling-axis routing is stated once under when_not_to_use."
- **lens**: profile
- **problem**: Doc-hygiene note about the profile's own authoring, not operational guidance, yet inside a body-counted, adapter-exported field.
- **fix**: Delete the sentence (end bullet at "…theirs to weigh (P029)."); keep the cross-reference in `provenance-ledger.md` only.

### S12 — Tangled `when_to_use[0]` trigger grammar
- **where**: `profile.yaml:17-18` — "…reviewing the losses against the source and the brief by descriptive method, not a quality metric."
- **lens**: profile
- **problem**: Ambiguous what "not a quality metric" negates; "by descriptive method" dangles. Release-critical routing field (most likely to seed the frontmatter description).
- **fix**: Reword into two clauses, e.g. "…assessed by descriptive method — reviewing losses against the source and brief, not scored against a fixed quality metric."

### S13 — `forbidden_behaviours[3]` bundles two prohibitions under one citation set
- **where**: `profile.yaml:89-90` — "prescribing a single correct rendering" + "ignoring the brief, audience, and function" (P075, P062, P038).
- **lens**: profile
- **problem**: P075 grounds only the first half; P062/P038 only the second.
- **fix**: Split into two bullets, each citing only its grounding principles.

---

## NICE (grouped)

- **N1** `principles.yaml:1133-1144` (P047): grammar folds Frawley's "third code" and Blum-Kulka's explicitation into one clause reading as if the hypothesis *is* a discourse type; reword to "…a proposed translating-specific *tendency*, contested by later corpus studies" (skill body already self-corrects). *(domain-quality)*
- **N2** P066 (`:1537-1553`) states explicitation flatly without the "contested tendency" hedge P047 carries; add the qualifier or cross-ref so the register/cohesion skill doesn't present it as settled. *(domain-equivalence)*
- **N3** P108 (`:2382-2396`) compresses Nord's instrumental translation as definitionally function-preserving; add "(equifunctional, heterofunctional, or homologous)". *(domain-equivalence)*
- **N4** P004 (`:113-124`) states the structuralist/relational theory of meaning as settled fact; treat as *this source's* argument against naive equivalence, optional one-clause hedge. *(domain-quality)*
- **N5** P119 (`:2567-2584`) attaches the false-friend (*faux amis*) caution to V&D "Borrowing"; classically a hazard of literal translation/calque — verify against V&D and move/duplicate if needed. *(domain-technical)*
- **N6** Role paragraph (`profile.yaml:8-15`) is one dense run-on covering four claims; split so the review-only boundary stands alone. *(agent-design)*
- **N7** Inconsistent trigger-phrasing style across the 12 skill descriptions ("Use when…" vs "Reviews…"); standardize one lead pattern. *(agent-skills)*
- **N8** Boilerplate "Inputs" bullet repeated verbatim in all 12 skills (e.g. `descriptive-method-and-translational-norms/SKILL.md:98`); drop or tailor per skill. *(agent-skills)*
- **N9** Reference-pointer sentence gives no signal of unique reference content; state what the reference adds (source anchors/quote-level grounding). *(agent-skills)*

MUST_FIX_COUNT: 2
