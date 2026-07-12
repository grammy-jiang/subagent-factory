# Review Loop — descriptive-translation-reviewer — r3

One review pass. 7 reviewer lenses + 3 deterministic gates. Findings consolidated,
deduped, most-severe first. Each: where | severity | problem | fix.

## Deterministic gates (STEP 1)

- `validate_generated_package` → **VALIDATION PASSED** (0 FAIL). Tier 2, 12 skills + 2 refs authored, adapter-quality OK, stale-maintenance all "grounding unchanged".
- `quote_scan` → **PASS** (no verbatim quotation).
- Truncation grep (`…` in skills/adapter; severed invariant parentheticals) → **0 hits** (clean).

Deterministic FAIL count = 0.

---

## MUST-FIX

### MF-1 — golden-tests version stamp stale (release-blocker)
- **Where:** `tests/golden-tests.yaml:4` (`profile_version: 1.5.0`) vs `profile.yaml:4` (`agent_version: 1.6.0`).
- **Severity:** must-fix.
- **Problem:** Package convention re-stamps `golden-tests.yaml` `profile_version` on every version bump (ledger v1.2.0/v1.4.0/v1.5.0 each record it). The v1.6.0 bump re-exported the adapter (adapter correctly shows `Profile version: 1.6.0`) but skipped the golden-tests re-stamp — file still reads 1.5.0. Verified real drift. (Checked: no stale inverted-Koller framing present in golden-tests — `grep denotative|Koller|escalate through` = 0 hits, so re-stamp is the only edit needed.)
- **Fix:** Set `tests/golden-tests.yaml` `profile_version: 1.6.0`; note the re-stamp in the ledger v1.6.0 entry.

---

## REJECTED must-fix (verified false — recorded so it is not re-raised)

### RJ-1 — "truncate operating invariants to one-liners like the sibling" — REJECTED
- **Raised by:** agent-design lens (as its sole must-fix).
- **Claim:** This adapter's invariants block has 141 full-paragraph principle statements vs sibling `translation-quality-reviewer` at 19 truncated one-liners ending `…`; fix = re-run compile to truncate.
- **Why rejected — direction is INVERTED.** Verified: this adapter = 141 full invariants, **0** ellipsis (passes the STEP 1 truncation gate). Sibling = 19 entries, **12** ellipsis-truncated. Adapter-invariant *truncation* is the known factory SAFETY bug (compile_invariants gutting must-hold rules, incl. safety P145/P146; only translation-quality-reviewer caught it — i.e. the SIBLING is the bug victim). The STEP 1 gate explicitly treats `…` truncation as a must-fix. Applying the proposed remedy would re-introduce the bug and FAIL the gate. This package's full, untruncated invariants block is the CORRECT state. Not counted.

---

## SHOULD-FIX

### SF-1 — adapter `description` under-represents sibling routing
- **Where:** `.claude/agents/generated/descriptive-translation-reviewer.md:3` (derived from profile).
- **Problem:** The one-line front-matter `description` — what an orchestrator matches for auto-invocation — omits the sibling-routing boundaries the body carefully states. With 4 near-identically-named translation reviewers, a caller matching only the short line has no signal to route equivalence-mechanics / corpus-QA-scoring / technical-terminology elsewhere.
- **Fix:** Extend the generated description's `Not for:` to name the boundaries, e.g. `Not for: word/collocation equivalence mechanics (→ translation-equivalence-advisor), corpus-based QA scoring (→ translation-quality-reviewer), technical/scientific terminology risk (→ technical-translation-advisor)`.

### SF-2 — `when_not_to_use` packs three sibling hand-offs into one run-on
- **Where:** `profile.yaml:28-32` (mirrored adapter ~L325); same shape flagged in `handoff_rules[1]` (see SF-3).
- **Problem:** Three distinct routing rules (equivalence-mechanism → equivalence-advisor, with carve-out; corpus/QA metrics → quality-reviewer; technical terminology → technical-advisor) compressed into one dense sentence with an inline parenthetical exception. Ambiguity concentrated exactly where mis-routing between the 4 siblings would occur.
- **Fix:** Split into three bullets, one per sibling, each stating what stays here vs. routes away.

### SF-3 — `handoff_rules[1]` trailing `(P029)` reads as grounding an uncited clause; ledger compounds it
- **Where:** `profile.yaml:93-95`; `provenance-ledger.md:9-10`.
- **Problem:** A single trailing `(P029)` on a multi-clause sentence reads (by this doc's own clause-level citation convention) as grounding the whole sentence — including the subject-matter/legal/typesetting scope boundary that CHANGELOG v1.1.0 says is deliberately uncited (P029 grounds only the commercial/economic clause). The ledger opening paragraph then lists `handoff_rules[1]` wholesale among fields "left uncited by design" — inconsistent with it carrying a citation.
- **Fix:** Split into an uncited scope-boundary clause + a `(P029)`-cited commercial/economic clause (or move `(P029)` to the clause it grounds); correct the ledger enumeration to match.

### SF-4 — record an independent re-verify after v1.6.0 fixes
- **Where:** `reports/review-loop/*.r2.review.md` ends `MUST_FIX_COUNT: 3`; no later report records a fresh `0` after the fixes landed.
- **Problem:** Repo workflow is "panel → fix → independent re-verify → converge to 0". v1.6.0 ledger logs the fixes as applied but no independent re-verify report confirms `MUST_FIX_COUNT: 0`. (This r3 pass partially closes it, but MF-1 above shows the loop had not in fact converged.)
- **Fix:** After MF-1 is applied, record this pass's converged result in the ledger before calling the loop done.

### SF-5 — split Frawley "third code" from Blum-Kulka explicitation (two research traditions)
- **Where:** `principles/principles.yaml` P047; `skills/domestication-foreignization-and-visibility/SKILL.md` step 4.
- **Problem:** P047 fuses a theoretical/semiotic thesis (Frawley's "third code") with an empirical corpus claim (Blum-Kulka's explicitation hypothesis). A domain expert would not treat explicitation evidence as support for the third-code thesis; as written a reviewer could cite corpus findings as proof of "relative autonomy".
- **Fix:** Split into two principles, or explicitly mark the two claims as independent and not evidentially linked.

### SF-6 — Nida formal-equivalence over-extended to "legal texts"
- **Where:** `principles/principles.yaml` P105/P124; `skills/equivalence-orientations-and-effect/SKILL.md` steps 5, 8.
- **Problem:** Pairing Nida's formal equivalence specifically with "academic or legal texts" over-extends Nida — his own F-E case is the gloss translation (readers studying source form/culture). Legal/treaty gravitation to formal-equivalence-like technique is a separate legal-TS strand (Šarčević), already covered correctly by P162.
- **Fix:** Soften P105/P124 so the Nida attribution names the gloss case; keep the legal-genre point as the separate, independently-grounded claim (P162).

### SF-7 — verify "Camus" attribution in the camp/register example
- **Where:** `principles/principles.yaml` P053 (claim C00880, Harvey "Camp Talk"); `skills/register-discourse-and-audiovisual-constraints/SKILL.md` step 4.
- **Problem:** "Camus's ... 'vous vous dévergondez' → 'you whore'" asserts an author association that is unusual for camp-discourse case material; likely a character named in the discussed fiction rather than Albert Camus, or a distillation slip. Asserted verbatim as a worked example.
- **Fix:** Re-check anchor `45ee8f34c41b-c0048` against Harvey's text; disambiguate (character vs author) or correct the name.

### SF-8 — Chesterman "four approaches (…cultural)" — verify count/wording
- **Where:** `principles/principles.yaml` P111; `skills/culture-ideology-power-and-rewriting/SKILL.md` step 15.
- **Problem:** Attributes to Chesterman "four complementary approaches (textual, cognitive, sociological, cultural)". Chesterman's own taxonomies are more standardly three (comparative/process/causal, or textual/cognitive/sociological); "cultural" as a co-equal fourth branch is not consistent with his own terminology. May be a faithful paraphrase of a Munday passage — verify.
- **Fix:** Check `derived_from_claims` C00345–C00347 against the Munday source; narrow wording or reframe "cultural" as an extension if the source doesn't support four co-equal branches.

### SF-9 — two skills lack a lens-specific ranking heuristic
- **Where:** `skills/descriptive-method-and-translational-norms/SKILL.md` step 22; `skills/culture-ideology-power-and-rewriting/SKILL.md` step 21.
- **Problem:** The other 10 skills close with a lens-anchored ranking criterion; these two just repeat the generic "highest-impact first", giving an agent no concrete rule for what counts as high-impact within *this* lens.
- **Fix:** Add a one-clause heuristic per sibling pattern (e.g. method skill: "an unreplicable coupled-pair method or an asserted-not-reconstructed norm claim outranks a mis-weighted frequency count"; culture skill: "a flattened institutional/ideology account that erases agency/power outranks an isolated paratext-reading slip").

---

## NICE

- **N1 — skill body bloat / progressive disclosure.** Each of 12 skills is near one-paragraph-per-principle Procedure + inverted restatement in Anti-patterns (94–134 lines). Consider shrinking each to a ~6–10 step recipe and moving the exhaustive per-principle checklist into a reference file. (`skills/*/SKILL.md`)
- **N2 — no triage step for which lenses fire.** Neither profile `review` mode nor the skills state how the agent picks the applicable subset of 12 lenses before loading them; combined with N1 a full-coverage review could load all 12 dense bodies. Add a triage clause to `review` mode. (`profile.yaml:49-54`)
- **N3 — Provenance prose duplicates frontmatter id list.** The closing `## Provenance` paragraph in each skill restates the frontmatter `provenance.principles` ids verbatim. Shorten to one pointer line. (all 12 `SKILL.md`)
- **N4 — Toury source bibliographic label.** `profile.yaml` sources lists "The Nature and Role of Norms in Translation" (Toury 1995) as a book title; it is an anthologized chapter — Toury's 1995 monograph is *Descriptive Translation Studies and Beyond*. Relabel as chapter/excerpt.
- **N5 — Procházka/Nida four-requirement double attribution.** Same four-part formula attributed to Procházka (P125) and Nida (P160) with no disambiguator that these are independent convergent formulations. Add a one-clause note or verify attribution. (`principles.yaml` P125/P160)
- **N6 — Quine "neutrinos lack mass" is period example.** P056 uses Quine's now-outdated illustration (neutrino oscillation confirmed nonzero mass, 1998). Point about translatability is unaffected; add a parenthetical that it is Quine's own historical example. (`principles.yaml` P056; hermeneutics skill step 4)
- **N7 — quality_bar[0] cites P110 imprecisely.** P110 = Toury's standardization/interference laws, not the "norms reconstructed / graded & mobile" claim the bullet makes. Drop P110 from that citation or move it to a standardization bullet. (`profile.yaml` quality_bar[0])
- **N8 — Toury DTS founding postulates + "assumed translation" missing.** Descriptive-method skill grounds Toury's norms/coupled-pairs thoroughly but omits the three founding postulates and the "assumed translation" premise. Consider adding if source supports. (`principles.yaml` P039; descriptive-method skill)
- **N9 — verify "systeme d'antan" (P002)** is genuine Even-Zohar/polysystem terminology, not an invented gloss. (`principles.yaml` P002)
- **N10 — Berman twelve tendencies not self-evidently enumerable to 12** in P014's comma-spliced prose. Consider a numbered 1–12 list in the reference index. (`principles.yaml` P014; deforming-tendencies skill)
- **N11 — profile body word count ~790-800w**, at the 800 WARN line; trim for firmer margin.
- **N12 — review-loop filenames reused** (r1/r2 overwritten with new content); number restarts monotonically to keep a complete audit trail.
- **N13 — ledger SF-4 carries "partial"** with no closing disposition; give it a final status on next bump.
- **N14 — audiovisual re-coding quality_bar[3]** reads categorical vs P052's "can actively re-code" hedge; reword to keep the modal ("possible re-coding, not assumed omission").

---

## Tally

- Deterministic FAILs: 0
- LLM must-fix (deduped, verified): 1 (MF-1). Agent-design's 1 rejected as inverted (RJ-1). Faithfulness / skill-authoring / all 3 domain lenses: 0 must-fix each.

MUST_FIX_COUNT: 1
