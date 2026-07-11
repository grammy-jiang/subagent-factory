# Review Loop — translation-equivalence-advisor (r2, fresh pass)

Consolidated review of `subagents/translation-equivalence-advisor/` at profile agent_version **1.2.6**
(Tier 2; sources: Baker *In Other Words* 1992 + Nida *Toward a Science of Translating* 1964 extract).
Seven reviewer lenses (agent-skills, profile, faithfulness, ai-agent-engineering + 3 domain lenses:
descriptive-translation, translation-quality, technical-translation) plus deterministic gates.

> Supersedes the earlier r2 snapshot. That snapshot's M1 (`always_on[0]` P095 unconditional) and M2
> (`always_on[4]` P038 vs P091 contradiction), and S1 (`always_on[7]` P041 register exception), were
> **fixed in the v1.2.2→v1.2.6 rounds**. The faithfulness lens this pass independently re-verified all three
> loci now carry the correct default-with-exception / conditioned wording in the current profile text.

## Deterministic gates

| Gate | Result |
|------|--------|
| `validate_generated_package` | **PASS** (0 FAIL; only pre-existing Phase-8 body-size WARNING) |
| `quote_scan` | **PASS** (no verbatim quotation) |
| truncation `…` grep (skills + adapter) | clean |
| adapter severed-invariant grep | clean |

Deterministic FAILs: **0**.

## Panel outcome

All 7 spawned reviewers returned MUST_FIX_COUNT: 0. Package has absorbed 7 prior review-loop rounds
(v1.0.0 → v1.2.6); faithfulness and agent-design lenses independently confirmed prior over-claim fixes are
present. No must-fix from any lens. Findings below are should-fix / nice only.

---

## SHOULD-FIX

### S1 — P033 contrastive-rhetoric stereotypes stated as settled fact *(converged: 2 domain lenses)*
- **where**: `principles/principles.yaml` P033; echoed `references/translation-equivalence-principles-index.md`
  (~line 224); profile.yaml knowledge_partition pragmatic bullet.
- **problem**: "German digression, Arabic repetition-by-assertion, Japanese linkless anecdote" is Kaplan-1966
  contrastive-rhetoric, substantially revised/critiqued since (Connor; Kubota & Lehner) as essentialist. The
  corrective hedge exists **only** in `pragmatic-equivalence-coherence-and-implicature/SKILL.md` step 3; a
  consumer reading the principle, index, or profile directly (or the agent in `advise` mode not routed through
  that skill) gets the unhedged version.
- **fix**: Fold the skill-level caveat into P033's statement text (and the index entry): "…treat as broad,
  contested tendencies from older contrastive-rhetoric scholarship, not fixed per-language rules; verify
  against the actual target readership and genre." So the caveat travels with the claim.

### S2 — P015 "masculine is usually the unmarked term" — 1992 framing, no currency/inclusive-language hedge *(converged: 3 domain lenses)*
- **where**: `principles/principles.yaml` P015; `skills/grammatical-equivalence/SKILL.md` step 3.
- **problem**: Stated flatly as a stable synchronic fact carried from Baker 1992. Holds only for binary
  masc/fem grammatical-gender systems, and the masculine-generic default is now widely contested (singular
  "they", écriture inclusive, EU/UN style guides). Skill correctly warns against defaulting masculine in the
  *target* but neither locus flags (a) a modern *source* may not follow the convention, nor (b) the now-routine
  gender-neutral / non-binary source reference crossing into a target with obligatory grammatical gender. The
  two loci disagree in coverage.
- **fix**: Qualify P015: "in languages with a masculine/feminine grammatical-gender system, the masculine is
  traditionally the unmarked term"; name gender-neutral/non-binary source reference as a case the existing
  "restructure to avoid specifying" strategy covers; add a brief/house-style inclusive-language check; align
  principle and skill loci.

### S3 — P009 Chinese passive "signalling adversity" — outdated as synchronic default *(converged: 2 domain lenses)*
- **where**: `principles/principles.yaml` P009; restated `skills/grammatical-equivalence/SKILL.md`.
- **problem**: Japanese adversative passive (迷惑の受身) is solid; the Chinese 被 pairing is weaker —
  contemporary Mandarin uses 被 routinely in neutral/favourable contexts (被评为…). Presented as a stable
  fact it could lead a translator to over-read adversity into a neutral modern passive.
- **fix**: Narrow adversity to Japanese, or qualify: "historically adversative in Chinese, now substantially
  neutralized in modern/translated usage — check era and register." Optionally cross-ref sibling
  translation-quality-reviewer's Europeanization coverage.

### S4 — P012 "environmentally relevant distinctions" risks environmental-determinism framing
- **where**: `principles/principles.yaml` P012.
- **problem**: "languages encode only environmentally relevant distinctions" echoes the debunked strong
  "Eskimo words for snow" claim (Pullum 1991); lexical elaboration tracks cultural/communicative salience, not
  strict environmental necessity.
- **fix**: Soften "environmentally relevant" → "culturally or communicatively salient"; drop deterministic
  environment→lexicon phrasing.

### S5 — Profile release-process hardening (3 recurring items, profile-reviewer)
- **body-size headroom**: Phase-8 WARNING re-confirmed near the 1000-word hard-fail edge across ≥4 rounds with
  near-zero headroom → next principle-grounded edit risks a hard FAIL. Fix: one dedicated headroom pass (move
  per-clause citation clusters out of `quality_bar` into `always_on`/skills) until headroom >50 words.
- **when_not_to_use[0] disambiguator** vs `translation-quality-reviewer` rests on a single adjective
  ("systematic") in one dense compound bullet → fragile router signal. Fix: anchor each sibling redirect with
  one concrete caller-phrasing example.
- **golden-tests / test-results staleness**: `profile_version` / `test-results.md` sync re-flagged+re-fixed in
  5 separate rounds (recurring release-process defect). Fix: automate — wire the sync into the version-bump
  step or add a validator hard-fail when `golden-tests.yaml.profile_version != profile.yaml.agent_version`.

### S6 — `grammatical-equivalence` step 7 routes to sibling by description, not slug (agent-skills)
- **where**: `skills/grammatical-equivalence/SKILL.md` step 7 ("per the word-level skill").
- **problem**: The one inconsistent cross-skill routing reference; every other routing instance names the slug.
- **fix**: Change to "per word-level-nonequivalence-and-strategies".

### S7 — Adapter frontmatter "Not for" spends its clause on the sibling-axis redirect, not the end-to-end-translation exclusion (ai-agent-engineering)
- **where**: `.claude/agents/generated/translation-equivalence-advisor.md` line 3 (`description:`).
- **problem**: Sibling adapters surface the core prohibition ("caller wants the finished translation produced
  end to end") at the routing layer; this one puts a lower-stakes sibling-axis redirect there. A "just
  translate this" request has no frontmatter-level signal to steer away (body Forbidden-behaviours still
  catches it once invoked — routing-consistency gap, not a runtime failure).
- **fix**: Swap the frontmatter "Not for" to the end-to-end-translation exclusion (sibling convention); keep
  the sibling-axis redirect in the body `when_not_to_use` where it already lives in full.

---

## NICE

- N1 — **P100 back-translation** one-sidedly framed as an "unsound compromise"; omits its limited-but-legitimate
  QA role (SIL/Bible-translation checking; regulated clinical/PRO/legal). `principles.yaml` P100 /
  `dynamic-and-formal-equivalence/SKILL.md` step 7. Verify against source, then distinguish
  "back-translation as a *sufficient* test" (correctly rejected) from "one QA input among several" (legitimate).
  *(converged: 2 domain lenses)*
- N2 — **P066 "always-definite" topic** overstates the tendency; topics in topic-prominent languages are
  characteristically, not categorically, definite/generic (Li & Thompson). `principles.yaml` P066 / index line
  197. Soften → "characteristically definite or generic". *(converged: 2 domain lenses)*
- N3 — **Collocational typicality** rests on translator intuition with no nod to corpus verification.
  `collocation-idiom-and-fixed-expression/SKILL.md` step 2 / P043, P063. Add one line: check typicality against
  corpus / collocation dictionaries where available (not new binding doctrine).
- N4 — **Dynamic-equivalence** entry could note Nida's later "functional equivalence" relabel (Nida & de Waard
  1986) to curb the "dynamic = license for paraphrase" misreading. `references/translation-equivalence-key-
  concepts.md`. Purely additive; reinforces the anti-misreading point with its own history.
- N5 — **Profile citation-granularity / symmetry nits** (faithfulness + profile lenses): several `quality_bar`
  bullets cite one principle ID where content draws on 2–3 (traceability, not strength gap); P058 cited only in
  the `always_on[1]` cluster not on its specific quality_bar bullet; `handoff_rules` doesn't name the three
  sibling subagents explicitly. Optional provenance/symmetry improvements.
- N6 — **Skill readability / router nits** (agent-skills): worked-example closing sentences are near-identical
  boilerplate; `dynamic-and-formal-equivalence` vs `text-level-approach-and-limits-of-equivalence` descriptions
  both key on "literal" — could add a reciprocal-boundary clause to the text-level description.
- N7 — **Adapter precedence rule** (role + forbidden override invariants) stated twice in slightly different
  words (adapter lines ~19 and ~23); optional consolidation if body size becomes a concern.

---

## Non-findings (verified sound)

Tool boundary (Read/Grep/Glob only, `may_edit_canonical: false`, empty mcp/caller_supplied),
canonical-ownership assignment, and the advisory / no-final-text boundary are correctly and explicitly
engineered (ai-agent-engineering: 0 must-fix). All 116 principles' core content — non-equivalence types,
idiom/collocation strategy, theme/rheme & FSP, cohesion reworking, register field/tenor/mode, Gricean
pragmatics, and the formal/dynamic orientation — tracks Baker + Nida accurately; all three domain lenses
returned 0 must-fix. The prior r2 must-fix loci (`always_on[0]` P095, `always_on[4]` P038/P091, `always_on[7]`
P041) are confirmed fixed at v1.2.6. Skill lens confirmed a clean, zero-overlap principle-id partition
(P001–P116 each in exactly one skill).

MUST_FIX_COUNT: 0
