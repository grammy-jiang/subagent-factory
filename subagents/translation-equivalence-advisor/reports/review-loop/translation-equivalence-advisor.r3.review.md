# Review Loop — round 3 — `translation-equivalence-advisor`

Consolidated one-pass review. 7 reviewer lenses (skill-authoring, profile-readiness,
faithfulness, agent-design, + 3 domain: descriptive / quality / technical) plus deterministic gates.
Findings deduped across lenses, most-severe first.

## Deterministic gates

| Gate | Result |
|------|--------|
| `validate_generated_package` | PASSED (Phase-8 self-check verdict: **WARNING** — body-size) |
| `quote_scan` | PASS — no verbatim quotation |
| ellipsis-truncation grep (skills + adapter) | clean |
| adapter severed-invariant grep | clean |

0 deterministic FAILs (the self-check body-size WARNING is surfaced as MF-3 below by profile-reviewer judgment).

---

## MUST-FIX

### MF-1 — forbidden_behaviours[3] cohesion clause is an absolute; omits P091 purpose-driven exception
- **Where:** `profile.yaml` `forbidden_behaviours[3]` ("Transferring the source text's cohesive devices, thematic markedness, voice, or tense/aspect unchanged ... (P038, P024, P009, P046).")
- **Severity:** must-fix (faithfulness — HEDGING_REMOVED / internal inconsistency)
- **Problem:** The *cohesive-devices* clause restates P038 ("rework, don't transfer cohesion") as a hard-forbidden absolute with no citation of **P091**, which explicitly licenses following source cohesion when the translation's purpose calls for it. The same P038-vs-P091 conflict was already reconciled in `knowledge_partition.always_on[4]` ("default P038 … but purpose-driven exception P091") but that fix was **not** propagated here. The faithfulness-report entry for `forbidden_behaviours[3]` (`EXACT_SUPPORT`) is therefore stale. Confirmed: current text cites `P038, P024, P009, P046`, no P091.
- **Fix:** Split the cohesion clause out and condition it — keep thematic-markedness/voice/tense-aspect absolute (P024, P009, P046), reword cohesion to "transferring cohesive devices unchanged **where the translation's purpose does not call for following source cohesion**, instead of reworking them to the target's own preferences by default (P038, P091)." Update the faithfulness-report finding from `EXACT_SUPPORT` to reflect the correction (mirror the note on `always_on[4]`).

### MF-2 — stale QA artifacts: test-results + adapter never regenerated for v1.2.1→v1.2.3; golden `profile_version` mismatch
- **Where:** `tests/test-results.md:3` (`Generated: 2026-07-11T19:21:40`), `adapters/claude-code/translation-equivalence-advisor.md:14` (`Generated: 2026-07-11T19:21:22`), `tests/golden-tests.yaml:4` (`profile_version: 1.2.2`), vs `profile.yaml:4` `agent_version: 1.2.3` and ledger/CHANGELOG v1.2.0/v1.2.2/v1.2.3 entries dated 2026-07-12 claiming regen + re-export.
- **Severity:** must-fix (release-readiness — orphan claim; violates generated-artifact-policy "Validation before release")
- **Problem:** `run_tests.write_test_results` stamps `datetime.now(UTC)` at write time; a genuine 2026-07-12 regen would show a 2026-07-12 timestamp. Both artifacts still read **2026-07-11**, and `golden-tests.yaml` still declares **1.2.2** (never bumped to 1.2.3) — so the Phase-8 verdict and golden run are not verified against the current v1.2.3 profile, yet ledger/CHANGELOG assert they were. Same defect flagged in r1 (MF-2) and r2 (S10) and marked fixed — it was not. Confirmed by direct inspection.
- **Fix:** Re-run self-check + `write_test_results` (or `cli validate`) against current `profile.yaml`; confirm `Generated:` ≥ 2026-07-12; bump `golden-tests.yaml` `profile_version` to `1.2.3`; re-export adapter so its `Generated:` matches; correct/annotate the v1.2.0/v1.2.2/v1.2.3 ledger + CHANGELOG entries that overstate what was done.

### MF-3 — Phase-8 body-size WARNING unresolved, sitting at the hard-fail edge
- **Where:** `profile.yaml` counted body fields; heaviest `quality_bar` 274w, `modes` 115w, `forbidden_behaviours` 106w. Self-check: `body ~1000 words (> 800); 200 over budget` (hard-FAIL line = 1000).
- **Severity:** must-fix (release-readiness — WARNING at ~0 headroom below hard-fail, unimproved across v1.1.0 S2 + v1.2.0 SF-6 "trim" fixes, and v1.2.1–v1.2.3 added text).
- **Problem:** Two prior dedicated size-reduction fixes netted no measurable reduction; later versions added counted text. Body is at the edge of the 1000-word hard-FAIL and cannot be safely called WARNING-not-FAIL until MF-2 regen confirms it.
- **Fix:** After MF-2 regen, if still WARNING, trim for real headroom — collapse citation lists, tighten the two heaviest compound `quality_bar` clauses and/or `forbidden_behaviours` — rather than deferring a 4th time.

---

## SHOULD-FIX

### SF-1 — quality_bar[4] cohesion categorical omits P091 (same defect as MF-1)
- **Where:** `profile.yaml` `quality_bar[4]` ("Cohesion is reworked, not transferred ... (P038, P004, P069, P017)"). Reword to "reworked by default, not transferred, unless the translation's purpose favours following source patterns …" and add P091. (Faithfulness.)

### SF-2 — P009 passive-adversity marked confidence: high overstates Mandarin evidence
- **Where:** `principles/principles.yaml` P009; echoed `skills/grammatical-equivalence/SKILL.md` step 2.
- **Problem:** Japanese adversative passive is settled; the Mandarin 被 (bèi) claim is much weaker (adversative bias eroded in modern usage). P009 is the only voice/grammar principle at `confidence: high` — overstates the Chinese half. (Quality-reviewer should-fix; descriptive nice — deduped.)
- **Fix:** Downgrade to `medium`, or narrow: "signalling adversity in Japanese, and historically in Chinese though weaker in modern usage."

### SF-3 — P066 "always-definite" topic overstates topic typology
- **Where:** `principles/principles.yaml` P066; `skills/thematic-and-information-structure/SKILL.md`.
- **Problem:** Topic-prominent languages have *characteristically* (not categorically) definite topics; indefinite topics occur in licensed constructions. "Always" risks faulting a legitimate indefinite-topic rendering. (Quality-reviewer.)
- **Fix:** Soften to "characteristically/typically definite," consistent with P069's "likely near-universal" hedging.

### SF-4 — key-concepts glossary under-covers terms skills claim it defines
- **Where:** every skill's `## References` line vs `references/translation-equivalence-key-concepts.md` (~10 entries).
- **Problem:** `grammatical-equivalence`, `thematic-and-information-structure`, `pragmatic-equivalence-coherence-and-implicature`, `register-style-and-literary-form` lean on undefined terms (obligatory grammatical categories, T/V distinction, FSP/communicative dynamism, markedness, speech-act force, Gricean maxims, register field/tenor/mode, concordant terminology, back-translation). Blanket pointer over-claims. (Skill-authoring.)
- **Fix:** Add the missing entries, or reword the per-skill pointer to "concepts shared across skills" for skills whose core vocabulary isn't in the glossary.

### SF-5 — no per-lens worked example in any of the 9 skill bodies
- **Where:** all 9 `SKILL.md` `## Procedure`/`## Anti-patterns`. Only package-wide `profile.yaml examples:` (2) exist.
- **Problem:** Dense 6–8-step procedures cite principles abstractly with no source-item→diagnosis→strategy→residual-loss walkthrough to pattern-match against. (Skill-authoring.)
- **Fix:** Add a short `## Example` to each skill, or at least the three densest/most-confusable (`collocation-idiom-and-fixed-expression`, `thematic-and-information-structure`, `register-style-and-literary-form`).

### SF-6 — multi-principle procedure steps compressed into run-on sentences
- **Where:** e.g. `grammatical-equivalence` step 3 (~70w, P015+P064); `thematic-and-information-structure` step 6 (P028+P088+P090); `dynamic-and-formal-equivalence` step 6.
- **Problem:** Rules buried mid-sentence get under-applied by a skimming agent; hurts the scannable/actionable bar. (Skill-authoring.)
- **Fix:** Split into one-decision-per-line sub-bullets, principle citation attached to its own clause.

### SF-7 — sibling-routing disambiguator missing from when_not_to_use
- **Where:** `profile.yaml` `when_to_use[1]` + adapter mirror; 4 corpus-siblings expose near-identical "review my translation" triggers.
- **Problem:** A generic "review my translation" request has no explicit routing signal to pick equivalence-advisor over the 3 siblings; disambiguation lives only in the dense `role` grounding clause. (Agent-design.)
- **Fix:** Add one `when_not_to_use` disambiguator naming the siblings' distinct lenses (norms/visibility → descriptive; corpus-QA/register-profile → quality; technical-doc usability/terminology → technical) and stating this advisor works at word/collocation/grammar/info-structure/cohesion/pragmatics/register equivalence levels.

### SF-8 — review-loop artifact traceability ambiguous (r2 S9 still open)
- **Where:** `reports/review-loop/` r1/r2/r3 filenames reused across two passes; 5 post-1.0.0 versions can't be mapped to artifacts.
- **Fix:** Version-scope historical report filenames (e.g. `<slug>.v1.2.2.review.md`) or add a round→version index to the ledger (Supersession rule). (Profile-reviewer.)

### SF-9 — Nida "dynamic equivalence" currency note absent (dedup: 3 domain reviewers)
- **Where:** `references/translation-equivalence-key-concepts.md` "Dynamic equivalence"; `skills/dynamic-and-formal-equivalence/SKILL.md`.
- **Problem:** Nida later renamed "dynamic" → "functional equivalence" (with de Waard, 1986) to stop the free-rewrite misreading. Absent note may confuse a reader comparing to modern TS vocabulary. Faithful to the cited 1964 extract, so completeness not correctness. (Descriptive + quality + technical — deduped.)
- **Fix:** One clause in the glossary entry + skill Purpose noting the 1986 "functional equivalence" relabel denotes the same orientation.

---

## NICE

- **N1** `inputs.required` is one compound entry; golden MC-001 enumerates 3 → split into 3 items for consistency. (Profile.)
- **N2** Collocation typicality (P043/P058/P063, `collocation-idiom-and-fixed-expression`) relies on intuition; Baker's later editions + corpus-TS recommend corpus consultation. Add a corpus-check step; flag 1992-edition grounding in role text. (Descriptive.)
- **N3** P069 explicitation "likely near-universal" is dated; later corpus studies show it's genre/register-dependent. Add a one-clause caveat. (Descriptive.)
- **N4** P015 masculine-as-unmarked: note inclusive/gender-neutral brief requirements override the default; cross-linguistic limit (non-IE noun-class systems). (Descriptive + technical.)
- **N5** `dynamic-and-formal-equivalence` "similar audience response" is an unfalsifiable heuristic goal, not a measurable target — add an anti-pattern line. (Quality.)
- **N6** Pragmatics skill is purely Gricean; relevance theory (Gutt/Sperber & Wilson) is the natural refinement if a 3rd source is ever added. No change within 2-source scope. (Technical.)
- **N7** `grammatical-equivalence` step 7 says "per the word-level skill" unnamed → name `word-level-nonequivalence-and-strategies`. (Skill-authoring.)
- **N8** `dynamic-and-formal-equivalence` H1 "…and Receptor Response" drifts from frontmatter `name`; align, or reflect "receptor response" in the description. (Skill-authoring.)
- **N9** 9× near-identical advise/review/compare `## Output` boilerplate — could live once in a reference for maintainability (no runtime cost). (Skill-authoring.)
- **N10** No worked example exercises the granted Read/Grep/Glob tools (caller-supplies-a-file path). Optional. (Agent-design.)
- **N11** r2 S5 (P015 gender caveat) / S6 (P100 back-translation) deferred as out-of-grounding-scope — carry to a future source-addition cycle. (Profile.)

MUST_FIX_COUNT: 3
