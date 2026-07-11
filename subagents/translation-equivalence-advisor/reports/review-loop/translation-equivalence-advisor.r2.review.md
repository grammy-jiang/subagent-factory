# Review Loop — translation-equivalence-advisor — Round 2

Package: `subagents/translation-equivalence-advisor/` (v1.1.0, HEAD `e519936`)
Lenses: deterministic gates + 7 subagent reviewers (skill-authoring, profile-readiness,
faithfulness, agent-design, + 3 domain: descriptive-translation, translation-quality,
technical-translation). Findings deduped across lenses; most-severe first.

## Deterministic gates — ALL PASS (0 must-fix)

- `validate_generated_package` → VALIDATION PASSED (Phase 8 self-check WARNING only)
- `quote_scan` → PASS, no verbatim quotation
- ellipsis truncation grep → none
- adapter invariant severed-parenthetical grep → none

---

## MUST-FIX (2)

### MF-1 — Receptor-response over-claim (M2 fix from r1) still live in 4 non-profile artifacts + generator
- **Where:**
  - `skills/dynamic-and-formal-equivalence/SKILL.md:96` (Purpose: "adequacy is judged by receptor response, not by formal closeness alone")
  - same file `:129` (Anti-pattern: "Judging adequacy by formal closeness alone rather than receptor response (P035)")
  - `references/translation-equivalence-key-concepts.md:73` (Adequacy entry: "…not by formal closeness alone (P035)")
  - `tests/golden-tests.yaml:71` (GT-004 `must_do`: "Judge adequacy by receptor response, not formal closeness alone")
  - root cause: `.build/authoring/gen.py` (emits all four; regeneration reproduces the defect)
- **Problem:** r1's M2 corrected this over-claim in `profile.yaml` quality_bar[6] (brief-conditioned adequacy), but the same pre-fix wording remains verbatim in the skill, reference, and golden test. It is a genuine domain misstatement of Nida's dual-criterion model: when formal equivalence is the deliberate orientation (P022 — reader needs close access to source form/terminology/structure, e.g. legal/philosophical/scholarly-apparatus text), the correct adequacy test *is* closeness to source form, not receptor response. As written, the advisor would tell a caller doing a correct formal/gloss translation that they are judging adequacy wrong. GT-004 will also re-validate the very over-claim v1.1.0 fixed.
- **Fix:** Propagate the brief-conditioned wording from `profile.yaml` quality_bar into skill Purpose/anti-pattern (`:96`, `:129`), the glossary Adequacy entry (ref `:73`), and GT-004 (`must_do`/`minimum_output`). Fix `gen.py` so regeneration doesn't reintroduce it. Extend `faithfulness-report.yaml` to cover these loci, not just quality_bar[6].

### MF-2 — quality_bar[1] reverses P044's hedge (idiom equivalence)
- **Where:** `profile.yaml:60` — quality_bar[1]: "…assume no idiom has a target equivalent (P042, P058, P044, P013)."
- **Problem:** P044 (`principles.yaml:900-911`) says *"do not assume an idiom has a target equivalent"* — stay agnostic. The profile rewrites this as an affirmative "assume no idiom has an equivalent" (HEDGING_REMOVED): "don't presume yes" became "presume no." Contradicts P014 (`principles.yaml:294-315`), which lists "a target idiom of similar meaning and form" as a real strategy — the reversed wording biases the advisor away from ever recommending it. The package's own `knowledge_partition.always_on[1]` (`profile.yaml:116`) states P044 correctly ("do not assume an idiom or fixed expression has a target equivalent"), so the two P044-citing passages now contradict each other.
- **Fix:** Change quality_bar[1] to match always_on[1]: "…do not assume an idiom has a target equivalent…" (drop "assume no … has"). Re-run faithfulness pass on quality_bar[1] and correct `faithfulness-report.yaml:12-19` verdict/note (currently WITHIN_SCOPE/accept_with_note "no strengthening" — inaccurate for pre-fix text).

---

## SHOULD-FIX (14)

- **SF-1 — Router description under-represents scope (drops 3–5 of 9 domains).** `.claude/agents/generated/translation-equivalence-advisor.md:3` (root: `profile.yaml:9-24` role + when_to_use ordering). Composed `description` samples role clause + first 2 when_to_use bullets positionally, silently dropping collocation/idiom, register/style/literary form, and whole-text review from what a dispatcher sees → under-routes idiom/register/cohesion/whole-text requests. Fix: reorder when_to_use so the most distinctive triggers (idiom/marked-structure/poetic-form, currently 4th) sit in the first two slots, then re-export the adapter. *(profile-reviewer #6 + agent-design #1)*

- **SF-2 — "correction" ambiguity in `review` mode could reconstruct a finished translation.** `profile.yaml:46-50` (outputs.modes[review]) / adapter `:73-76`, tension with forbidden_behaviours[0] (`profile.yaml:80-82`). "Correction" is ambiguous between naming a strategy/device (in-scope) and supplying verbatim replacement wording; applied span-by-span the latter reconstructs the finished text the forbidden behaviour bars. Fix: state explicitly that "correction" names the strategy/target-language device, not verbatim replacement prose. *(agent-design #2)*

- **SF-3 — Skill `## Output` sections assume a draft always exists (breaks `advise` mode).** 7 skills: `word-level-…:112`, `collocation-idiom-…:107`, `grammatical-equivalence:104`, `thematic-and-information-structure:137`, `cohesion-and-texture:103`, `pragmatic-…:111`, `register-style-…:80`, `text-level-…:89`. Output says "the strategy the draft used" etc., but `advise` mode has no draft (profile's own worked example `:174-186` is exactly this case). Inputs already hedge "(if any)"; Output doesn't. Fix: add a no-draft branch to each Output ("if none exists yet, state the recommended strategy directly and its principle"); `dynamic-and-formal-equivalence:124` already does this — use as template. *(skill-authoring #1)*

- **SF-4 — No per-skill worked example.** All 9 `skills/*/SKILL.md`. Only two worked examples exist, at profile level; under progressive disclosure a skill loads in isolation with no concrete input→output anchor. Fix: add a short `## Example` (one input scenario → one ideal per-finding output) to each skill, scoped to its lens. *(skill-authoring #2)*

- **SF-5 — Nida source citation: fabricated subtitle + secondary extract cited as primary monograph.** `profile.yaml:205-210` (sources[1]). Title "Toward a Science of Translating: dynamic and formal equivalence" is wrong (real subtitle: "With Special Reference to Principles and Procedures Involved in Bible Translating"); `sources/metadata/dynamic-formal-equiv-e6872198.metadata.json:13` records `authority: secondary`, `word_count: 10406` — a derived extract, not the ~300pp primary text. Neither fixed nor logged as deferred (`provenance-ledger.md:67-69` lists only S3/S5/S6/S7). Fix: correct the title; if a secondary extract, say so at the profile citation level and log in the ledger. *(profile-reviewer #5 + technical #4 + translation-quality nice#2)*

- **SF-6 — Body-size ~984/1000w leaves no fold-in headroom.** `profile.yaml:56-76` quality_bar. r1's S2 "compression" reclaimed ~0 words; any 3rd-source fold-in hard-fails the 1000w body budget day one. Fix: real compression — the shared "judged by function, not form" clause repeats across quality_bar[2]/[3]/[4]/[7]; state once, then lead each bullet with only its distinguishing content. *(profile-reviewer #4)*

- **SF-7 — `test-results.md` Phase-8 self-check pre-dates the v1.1.0 fixes.** `tests/test-results.md:1-28` stamped `2026-07-11T13:45:24`, before M1/M2/S* landed 2026-07-12; still reports the pre-fix 984w WARNING. Not evidence of current state. Fix: regenerate against v1.1.0 profile. *(profile-reviewer #3)*

- **SF-8 — `golden-tests.yaml` `profile_version` stale.** `tests/golden-tests.yaml:4` = `1.0.0`; profile is `1.1.0`. Fix: bump / re-derive per generated-artifact-policy re-export rule. *(profile-reviewer #2)*

- **SF-9 — Back-translation framed only as "theoretically unsound," omits mandated QA role.** `principles.yaml:1863-1868` (P100); `skills/dynamic-and-formal-equivalence/SKILL.md:113`. One-sided vs current practice: back-translation is a mandated validation step in pharma/clinical linguistic-validation (ISPOR, FDA PRO guidance, WHO instrument protocols); sibling technical-translation-advisor already frames it as "a limited quality check." Fix: add that it is also a recognized (limited) checking/validation device in high-stakes/regulated domains. *(descriptive #3 + technical)*

- **SF-10 — "Dynamic equivalence" used without Nida's own later "functional equivalence" revision.** `principles.yaml:717-735` (P034); `skills/dynamic-and-formal-equivalence/SKILL.md:92-96`; `references/translation-equivalence-key-concepts.md:47-49`. Nida & de Waard (1986) renamed it "functional equivalence" precisely because "dynamic" was misread as licensing free/loose translation. Fix: one line noting the later preferred term. *(translation-quality #1 + descriptive #4 + technical)*

- **SF-11 — Adversative-passive rule overstated for contemporary Mandarin.** `principles.yaml:192-212` (P009); `skills/grammatical-equivalence/SKILL.md:89`; `profile.yaml:61-62` quality_bar[2]. Faithful to Baker 1992 but 被(bèi)'s unfavorable bias has weakened since the 1990s (neutral/positive uses now routine). Reliable for Japanese (迷惑受身), register/era-sensitive for Mandarin. Fix: qualify — strongest for Japanese; a tendency (not a rule) for Mandarin, check text type before inferring adversity. *(descriptive #2 + technical)*

- **SF-12 — Contrastive-rhetoric patterns stated as fixed national norms.** `principles.yaml:695-716` (P033); `skills/pragmatic-…:97`. "German digression / Arabic repetition / Japanese linkless anecdote" descends from Kaplan (1966), substantially critiqued as essentializing (Kubota 1997, Zamel 1997). Unhedged → advisor over-applies a stereotype to an individual text (also violates package's own P102). Fix: hedge as contested genre/text-type tendencies to check against the actual text, not fixed cultural rules. *(translation-quality #2 + descriptive N2 + technical)*

- **SF-13 — "Similar audience response" treated as a checkable test, not an argued judgment.** `principles.yaml:717-771` (P034–P036); `skills/dynamic-and-formal-equivalence/SKILL.md:114,122-124`. TS scholarship since van den Broeck (1978) treats equivalent effect as unmeasurable — an interpretive claim the translator argues for, not a pass/fail criterion. Fix: reframe as an informed approximation to reason about and defend. *(technical)*

- **SF-14 — Gender-neutral/inclusive-language check absent from grammatical-gender guidance.** `principles.yaml:316-336` (P015); `skills/grammatical-equivalence/SKILL.md:90`. Gives only "masculine-as-unmarked / restructure to avoid" but EU/UN/corporate/legal style guides now often mandate inclusive phrasing even into heavily-gendered targets (écriture inclusive, Gendersternchen). Fix: add a step to check the brief's inclusive-language policy before defaulting. *(technical + translation-quality nice#1 + descriptive N4)*

---

## NICE (11)

- **N-1** — Gricean maxim labeled "Relevance"; Grice's canonical term is "Relation" (invites conflation with Sperber & Wilson Relevance Theory). Add "(Grice's maxim of Relation)" once. `principles.yaml:674-716` (P032); `skills/pragmatic-…:97`. *(descriptive N1 + technical)*
- **N-2** — Passive-for-"objectivity in scientific English" dated; Nature/APA/CSE now push active voice. Reframe "was long associated with." `principles.yaml:192-212` (P009). *(descriptive N3 + technical)*
- **N-3** — `handoff_rules[1]` (`profile.yaml:93-95`) asserts ownership/delegation ("belongs to the domain expert and commissioner") with more certainty than cited P094/P115 establish; it's a design/governance inference. Soften or mark as boundary decision. *(faithfulness #3)*
- **N-4** — `when_not_to_use[3]` (`profile.yaml:30-31`) "guarantee of a single correct rendering" restates forbidden_behaviours[1] caveat, not a recognizable redirect trigger; near-dup of forbidden_behaviours[0] wording too. Drop or reframe as an actual trigger. *(agent-design #3 + profile-reviewer #7)*
- **N-5** — `forbidden_behaviours[0]` (`profile.yaml:80-82`) carries no principle citation (it's an advisory-scope boundary). Add "(advisory-scope boundary, not a source claim)" so it doesn't read as an orphan. *(profile-reviewer #8 + agent-design #4)*
- **N-6** — Operating invariants (`profile.yaml:26-34`) phrased as translator-imperatives ("render", "never assume") not advisor-diagnostic voice ("flag", "check"). Role preamble neutralizes the risk; optional wording pass. *(agent-design #4)*
- **N-7** — Densest skills (thematic `:121,:126`; dynamic-formal `:107-114`) pack 2–3 instructions+citations per numbered step. Split for scannability. *(skill-authoring #3)*
- **N-8** — Skill frontmatter carries factory-internal fields (`kind`/`status`/`provenance`) beside `name`/`description`; harmless on current adapter Read-pointer path, only matters if ever exported as literal standalone Agent Skills. *(skill-authoring #4)*
- **N-9** — Nida D-E/F-E framework's Bible-translation origin unstated in `skills/dynamic-and-formal-equivalence/SKILL.md:92-96`; expansion/decoding-rate advice transfers less directly to technical/legal text. One line of origin context. *(technical)*
- **N-10** — Adapter header `Generated: 2026-07-11T18:17:10` vs Profile version 1.1.0 (CHANGELOG dates 1.1.0 to 2026-07-12); content confirms re-export happened, so cosmetic date only. `adapter:14`. *(profile-reviewer #9)*
- **N-11** — Scope currency: no Skopos/functionalist (Reiss & Vermeer, Nord), Vinay & Darbelnet procedures, or error-typology QA (MQM/DQF). Legitimate disclosed 2-source scope; sibling packages own the broader terrain. Future fold-in candidate, not a current defect. *(technical + translation-quality nice#2)*

---

MUST_FIX_COUNT: 2
