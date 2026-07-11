# Review-loop report — translation-equivalence-advisor (r1)

**Date:** 2026-07-12
**Package:** `subagents/translation-equivalence-advisor/` (agent_version 1.2.5, Tier 2)
**Lenses run:** deterministic gates + 4 factory lenses (agent-skills, profile, faithfulness,
ai-agent-engineering) + 3 domain cross-checks (descriptive-translation, translation-quality,
technical-translation).

## Deterministic gates (STEP 1)

| Gate | Result |
|------|--------|
| `validate_generated_package` | **PASS** (0 FAIL; phase8 self-check WARNING only) |
| `quote_scan` | PASS — no verbatim quotation |
| truncation `…` ellipsis grep | clean |
| adapter invariant-severance grep | clean |

Deterministic FAIL count = **0**. (Note: validate only checks the self-check/test artifacts
*exist*, not that they match `agent_version` — see MF1, caught by the profile lens, not by the gate.)

---

## Findings (most-severe first, deduped across lenses)

### MUST-FIX

**MF1 — Self-check / test artifacts are stale relative to shipped `agent_version` 1.2.5**
- **Where:** `tests/golden-tests.yaml:4` (`profile_version: 1.2.4`) and `tests/test-results.md:3`
  (`Generated: 2026-07-11T19:46:38`, pre-v1.2.5 body-size row) vs `profile.yaml:4`
  (`agent_version: 1.2.5`); `CHANGELOG.md` `[1.2.5]` omits the "Test hygiene" regeneration line
  that every prior version entry (1.2.0/1.2.2/1.2.3/1.2.4) carried.
- **Severity:** must-fix (release-readiness). **Verified independently** by direct file read.
- **Problem:** v1.2.5 changed `_compose_description` and trimmed the profile body — exactly what
  Phase 8 self-check + Phase 10 golden tests re-verify — but those artifacts were never
  regenerated. `validate PASS` does not certify freshness. Same issue as the package's own
  r5 MF2, never fixed.
- **Fix:** Re-run Phase 8 self-check against current v1.2.5 `profile.yaml`; regenerate
  `tests/test-results.md`; bump `golden-tests.yaml` `profile_version` → `1.2.5`; add the matching
  "Test hygiene" CHANGELOG/ledger line; re-confirm the body-word-count WARNING against the fresh
  number.

---

### SHOULD-FIX

**SF1 — Gender/pronoun guidance omits gender-neutral / inclusive-language rendering**
*(dedup: descriptive-TS + translation-quality both raised P015 independently)*
- **Where:** `principles/principles.yaml` P015 (and P026); `skills/grammatical-equivalence/SKILL.md`
  procedure step 3.
- **Problem:** Guidance covers masculine-as-unmarked and "restructure to avoid specifying gender,"
  but never names gender-neutral/inclusive strategies (singular *they*, epicene forms, neologism,
  translator's note, EU/UN & style-guide inclusive-language norms) — a live mainstream problem in
  professional translation, and squarely in this skill's stated scope, so a real gap not an
  out-of-scope deferral.
- **Fix:** Add an explicit branch: when source referent gender is genuinely unspecified and the
  target has an established neutral device, offer that device as a primary option *before*
  defaulting to masculine-as-unmarked or restructuring away.

**SF2 — Grice's fourth maxim mislabeled "Relevance" (should be "Relation")**
- **Where:** `principles/principles.yaml` P032 (lines 674–694);
  `skills/pragmatic-equivalence-coherence-and-implicature/SKILL.md` line 99.
- **Problem:** Grice's (1975) canonical maxim is **Relation** ("Be relevant"). "Relevance" names a
  distinct later rival framework (Sperber & Wilson Relevance Theory); labeling Grice's maxim
  "Relevance" conflates two theoretical accounts — a pragmatics reviewer would dispute it.
- **Fix:** Reword both loci to "Quantity, Quality, Relation (often glossed as Relevance), and
  Manner."

**SF3 — Back-translation framed as "only pedagogical," eliding recognized professional QA use**
- **Where:** `principles/principles.yaml` P100; `skills/dynamic-and-formal-equivalence/SKILL.md`
  procedure step 7.
- **Problem:** States back-translation is "only a pedagogical illustration… not by itself a general
  test of translation quality." Omits that it is an established (if contested, insufficient-alone)
  professional QA step in regulated domains — clinical-trial/PRO (ISPOR/ISO), informed consent,
  legal, market research. "Only pedagogical" over-narrows.
- **Fix:** Note back-translation also functions as one recognized professional QA technique in
  regulated domains, while keeping the caution that it must never be the sole quality test.
  *(Cross-check: this is the r4 SF1 narrowing; may have over-corrected — reconcile with that history.)*

**SF4 — Contrastive-rhetoric claims stated as settled fact, not a contested hypothesis**
- **Where:** `principles/principles.yaml` P033 (lines 695–716);
  `skills/pragmatic-equivalence-coherence-and-implicature/SKILL.md` procedure step 3.
- **Problem:** Asserts national/cultural discourse patterns (German digression, Arabic
  repetition-by-assertion, Japanese linkless anecdote) as established facts. This is Kaplan's 1966
  contrastive-rhetoric hypothesis, substantially critiqued (Connor 1996, Kubota 1999) as
  essentializing. Stating as flat fact overreaches.
- **Fix:** Hedge to "loose tendencies to verify against the actual target readership, not fixed
  national patterns"; keep the well-supported underlying point (maxims are culture-relative).

**SF5 — when_not_to_use boundary vs descriptive-translation-reviewer names theory-topics, not the real overlap**
- **Where:** `profile.yaml:24-27` (`when_not_to_use` bullet 1); adapter lines 48-51.
- **Problem:** Redirect sends "generic review my translation" to descriptive-translation-reviewer
  for "norms, retranslation, translator (in)visibility" — but the actual overlap is *linguistic-level
  equivalence review itself* (descriptive's own when_to_use claims equivalence/register/cohesion at
  the same levels). A caller can't disambiguate from either package's text.
- **Fix:** Name the real axis: equivalence-as-evidence-for-a-norm / domestication-foreignization /
  translator-visibility → descriptive; the linguistic mechanism itself (is this collocation typical,
  does this cohesive tie fit target convention) → here. Flag as symmetric handoff note for the
  descriptive-reviewer package too.

**SF6 — "register profile" redirect conflicts with this package's own register quality-bar item**
- **Where:** `profile.yaml:27` (redirect to translation-quality-reviewer) vs `profile.yaml:73-75`
  (`quality_bar` register-by-field/tenor/mode) + `register-style-and-literary-form` skill.
- **Problem:** Excludes "a register profile" yet keeps a standing quality bar judging register by
  field/tenor/mode (same House categories the sibling uses). Distinction plausibly exists (local
  factor vs systematic ST/TT profile comparison) but is never stated.
- **Fix:** Make redirect specific: systematic ST-vs-TT register *profile* comparison (House
  field/tenor/mode, overt/covert) → translation-quality-reviewer; register as one local factor in a
  rendering-strategy decision → stays here.

**SF7 — `handoff_rules[1]` wording doesn't carry the v1.2.5 P094 scope-narrowing**
- **Where:** `profile.yaml:95-97`.
- **Problem:** P094 (principles.yaml:1773-1777) was narrowed in v1.2.5 to "stylistic concordance,
  not subject-matter terminology consistency." But handoff_rules[1]'s unqualified "terminology
  consistency," sitting right after "subject-matter terminology," can be read as re-claiming the
  narrowed-away scope.
- **Fix:** Reword: "…flags where source-term concordance (stylistic/study tracking, not
  subject-matter glossary consistency) or the receptor community's faithfulness expectations bear
  (P094, P115)."

**SF8 — No worked `compare`-mode example in the profile example gallery**
- **Where:** `profile.yaml:176-214` (`examples:`), cf. `outputs.modes[2]` (`profile.yaml:52-56`).
- **Problem:** All 3 example entries cover advise/review/decline; compare mode's distinct contract
  (side-by-side of two options → purpose-weighted recommendation) is exercised only by golden test
  GT-004, never in the gallery that most concretely teaches response shape.
- **Fix:** Add a fourth `examples` entry (`kind: happy-path`) with a compare-mode `ideal_response`
  (e.g. formal-vs-dynamic for one segment under a stated brief).

**SF9 — No worked example in any of the 9 SKILL.md files**
- **Where:** all `skills/*/SKILL.md` (esp. cohesion, thematic/information-structure, pragmatics,
  register/form — the most abstract lenses).
- **Problem:** Each skill's Output section describes finding *shape* abstractly; none shows a concrete
  before/after instance. Falls short of the operational-recipe bar (procedure + I/O example).
- **Fix:** Add one short worked example per skill (1–2 sentence source snippet → flaw named at that
  lens → strategy/correction → residual loss), prioritizing the four hardest-to-picture lenses.

**SF10 — Procedure steps overload a full decision table into one run-on sentence**
- **Where:** `word-level-nonequivalence-and-strategies/SKILL.md` step 5;
  `dynamic-and-formal-equivalence/SKILL.md` steps 2/5/8; `collocation-idiom-and-fixed-expression/SKILL.md`
  step 5.
- **Problem:** Full strategy set + citations crammed into one dense clause — reduces scannability at
  live-review time, the moment the step must work as a checklist.
- **Fix:** Reformat as a short nested bullet list (one option/strategy + citation per line), keeping
  the step's opening sentence as header.

**SF11 — Body-size WARNING has near-zero headroom and is currently unverifiable**
- **Where:** `profile.yaml` body budget (~968/1000 words claimed at v1.2.5, `CHANGELOG.md:38-39`).
- **Problem:** 800-word PASS already exceeded; ~3% headroom to the 1000-word hard-fail; the artifact
  that would confirm the count is stale (MF1), so true count unverified.
- **Fix:** After regenerating test-results (MF1), if confirmed count >900, trim further (collapse
  remaining `quality_bar` per-clause citation lists) or move detail into
  `knowledge_partition.always_on` (exempt from body budget).

---

### NICE

- **N1 — `dynamic → functional equivalence (1986)` succession not noted.** `skills/dynamic-and-formal-equivalence/SKILL.md` Purpose / P034. Nida & de Waard (1986) renamed "dynamic" to "functional equivalence" precisely because "dynamic" was misread as "free/emotive"; readers hitting the later term elsewhere will want the mapping. Add one sentence. *(descriptive + quality both flagged the terminology-succession area.)*
- **N2 — `quality_bar[2]` conflates obligatory-category compliance with function-over-form choices.** `profile.yaml`. Gender/number/tense are obligatory categories (P025/P057); voice (P009) and modality (P085) are function-over-form, not obligatory slots. Reword: "render voice and modality by function, and gender/number/tense-aspect by the target's obligatory categories."
- **N3 — P009 scientific-English passive example lacks a currency caveat.** `principles/principles.yaml` P009; `grammatical-equivalence/SKILL.md`. Current STEM style guidance (Nature/ACS/IEEE/CSE) has moved toward active voice; add "(a convention increasingly displaced by active-voice style guidance in current STEM writing)."
- **N4 — P009 Chinese adversative-passive claim slightly overconfident at "high".** `principles/principles.yaml` P009. 被-passive has broadened to neutral use in contemporary/translated Chinese; downgrade to medium or add a diachronic caveat (check register/period).
- **N5 — P015 "masculine as unmarked" hedge lives only in the skill, not the principle.** `principles/principles.yaml` P015. Fold the descriptive-not-prescriptive clause (already in `grammatical-equivalence` step 3) into the principle text so direct principles.yaml readers get it too.
- **N6 — Compensation scoped only to idioms (P014), not surfaced as Baker's general text-level strategy.** Cross-reference P014 from `register-style-and-literary-form` sound-effects guidance (P099), or add a cross-cutting principle.
- **N7 — "Explanatory vs supplemental coherence" (P070) terminology unverified against source wording.** `principles/principles.yaml` P070; pragmatics skill step 1. Spot-check against Baker's actual coherence chapter next faithfulness pass; soften if it's the distillation's own paraphrase.
- **N8 — `always_on[6]` citation list includes P100 though its prose never mentions back-translation.** `profile.yaml`. Citation noise, no over-claim; drop P100 or add a short back-translation clause if touched.
- **N9 — Skopos-theory convergence unnoted.** Brief-driven tactic selection (P021/P097) parallels Reiss & Vermeer Skopos; optional one-line "see also," or explicitly leave out-of-scope given two-source grounding.
- **N10 — H1 heading drift.** `dynamic-and-formal-equivalence/SKILL.md` H1 adds "and Receptor Response" not in the slug/description. Match slug or fold into frontmatter description.
- **N11 — Frontmatter `description` is a dense semicolon/dash run-on** (adapter line 3 + all 9 skill descriptions). Router/scan parse speed; consider clause-broken phrasing. Adapter-export-template concern, not profile authoring.
- **N12 — Redundant restatement of the advisory-boundary precedence rule** (adapter lines 19 & 23). Consolidate to one statement + cross-reference.
- **N13 — Single-sentence Role guard against 5 imperative must-hold invariants.** `profile.yaml:9-14` vs compiled `## Operating invariants`. Reword invariant surface forms to be self-evidently advisory ("Flag a draft that renders X mechanically…") rather than relying solely on the Role disclaimer. Future cycle.
- **N14 — Ledger version-history now 13 entries in one file** (`provenance-ledger.md:52-238`). Consider archiving entries older than N versions to `provenance-ledger-history.md`.

---

## Out-of-scope note (not counted)

`reports/review-loop/translation-equivalence-advisor.r5.review.md` MF1 reports
`references/translation-equivalence-principles-index.md` still carries pre-round-4 P094/P100 wording
(drifted from `principles.yaml`). Reference-file/domain-content drift — resolve in the same pass as
MF1, since both stem from round-5 fixes never applied.

MUST_FIX_COUNT: 1
