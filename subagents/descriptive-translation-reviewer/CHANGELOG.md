# Changelog — descriptive-translation-reviewer

All notable changes to this generated subagent package are recorded here. Versions follow the
`agent_version` field in `profile.yaml`.

## [1.10.0] — 2026-07-12

Review-loop round r2 (`reports/review-loop/descriptive-translation-reviewer.r2.review.md`): applied both
must-fixes (M1, M2) and the high-value should-fixes (SF-2, SF-3, SF-4, SF-6, SF-7, SF-9), staying grounded in
the existing 180-principle spine — no new claim introduced; every added sentence is either sibling-routing
(no principle content) or failure-mode detail already present in the same skill's own anti-patterns.

### Fixed
- **M1 — sibling-routing boundary missing from `translation-quality-and-applied-studies` trigger surface** —
  added to that skill's `description` and a new `## When to use` bullet: requests to run corpus-based quality
  metrics / QA scoring and return the scores route to the sibling `translation-quality-reviewer`; this skill
  reviews only whether the evaluation method itself is sound.
- **M2 — Procedure step 15 (GILT/localization) invited scope creep** — added a boundary clause: terminology
  risk or scientific/technical target-text correctness in a localization deliverable routes to
  `technical-translation-advisor`; the step is scoped to whether the localization/internationalization
  framing (fixed-source vs. locale-functionality) is sound.
- **SF-2 — `inputs.required` unconditionally demanded source+target** — made the source/target pair
  conditionally required (only when reviewing an actual rendering); a translation-studies analysis or 'norm'
  claim may omit it, matching the `when_to_use[1]` analysis path.
- **SF-3 — `when_to_use[5]` bundled 4 triggers into one run-on bullet** — split the V&D/Catford/TQA-method
  soundness trigger onto its own bullet and merged the equivalence-orientation and axis-placement triggers,
  keeping the list at 6 (the deterministic gate hard-FAILs above 6).
- **SF-4 — profile body word-count margin thin (~989w vs 1000w FAIL)** — kept the review-only boundary at full
  strength once (`forbidden_behaviours[0]`) and shortened the `role` and `when_not_to_use[0]` restatements to
  cross-references; body now ~985w.
- **SF-6 — missing reciprocal tie-breaker between `hermeneutics-and-the-limits-of-translatability` and
  `meaning-signification-and-equivalence-critique`** — added a reciprocal routing clause to each skill's
  `description` (indeterminacy-of-reference / hermeneutic-motion vs. word/sign-level signification).
- **SF-7 — `text-type-skopos-and-the-brief` Procedure under-specified vs its own anti-patterns** — folded the
  concrete failure-mode detail already in this skill's anti-patterns back into the thin Procedure steps
  (2, 3, 6, 8, 9, 10, 14, 15); no new principle or claim.
- **SF-9 — Blum-Kulka explicitation mislabelled a "discourse type" (P047)** — reworded to "a proposed
  translating-specific process tendency (or 'universal')", keeping it distinct from Frawley's third-code thesis.

### Deferred
- **SF-1** — the router-visible adapter `description` is auto-composed by `export_claude_agent` from
  `role` + `when_to_use[:2]` + `when_not_to_use[:1]` under a 320-char / 85-char-per-clause budget; the primary
  sibling routing (→`translation-quality-reviewer`) already surfaces via `role`, and M1/M2 close the same root
  defect at the per-skill trigger surface. Forcing all three exclusions into the budgeted exclusion clause
  would truncate mid-list.
- **SF-5, SF-8, and NICE items** — SF-5 (repeat reviewer-only reframing in the generated adapter body) is
  template-rendered, not hand-editable; SF-8 is `owner-decide`, blocked pending a reciprocal fix on the sibling
  `translation-quality-reviewer` package.

## [1.9.0] — 2026-07-12

Review-loop round r1 (`reports/review-loop/descriptive-translation-reviewer.r1.review.md`): applied all three
must-fixes and the high-value should-fixes (SF-1..SF-6), staying grounded in the existing 180-principle spine
(no new claim introduced). Deferred SF-7 (per-skill anti-pattern trimming, a token-economy refinement across
all 12 skills) and the NICE items as lower-value polish, since trimming grounded per-principle coverage risks
losing skill-level grounding.

### Fixed
- **MF-1 — operating invariants read as translation-production instructions** — the invariants are rendered
  from the faithfulness-reviewed principle statements (shared adapter template), so the boundary was
  strengthened at the point of highest salience: `role` now ends "read every operating invariant below as a
  criterion for judging someone else's translation, never a step to perform yourself", which renders
  immediately before the `## Operating invariants` heading. No principle text touched.
- **MF-2 — `when_to_use` covered only 7 of 12 skills** — added two charter-level triggers routing to the
  five uncovered skills: (a) ideology / institutional rewriting / patronage / reception and
  hermeneutic/untranslatability grounding, (b) Vinay–Darbelnet procedure / Catford shift disputes and
  translation-quality-assessment / applied-TS method soundness.
- **MF-3 / SF-3 — stale version stamps** — re-stamped `tests/golden-tests.yaml` `profile_version` and the
  `tests/test-results.md` self-check verdict to the new `agent_version` (were `1.8.0`).

### Changed
- **SF-1 — P020 applied as an unscoped universal criterion** — added `applies_when`
  (literary/poetic/philosophical/experimental-deconstructive translation where the mode of signification, not
  propositional content, is the object of fidelity) to P020, mirroring P034; rewrote
  `domestication-foreignization-and-visibility` step 1 and its anti-pattern to keep "fluency is not proof of
  quality" general while gating "reject reproduction of meaning" behind that text-type condition.
- **SF-2 — worked example conflated Nida "dynamic equivalence" with Reiss/Newmark** — the operative-text
  advise example now names Reiss's adaptive method and Newmark's communicative translation, with Nida's
  "dynamic equivalence" marked as a parallel-but-distinct analogue.
- **SF-4 — `outputs.primary_format` overstated per-mode uniformity** — reworded to the mode-agnostic common
  thread (names the governing principle(s) + a residual trade-off, never a bare verdict), deferring shape to
  the modes list.
- **SF-5 — ledger orphan-field list omitted `handoff_rules[2]`** — added the sibling-routing bullet to the
  intentionally-uncited enumeration.
- **SF-6 — no temporal-currency boundary** — added a `when_not_to_use` note that the grounding is
  foundational/classical theory (through ~2016) and post-2016 corpus methodology, NMT-era norm shifts, and
  MQM/DQF typologies are out of scope.
- Tightened uncited descriptive prose (`role`, `when_to_use`, `when_not_to_use`, `minimum_useful_output`) to
  keep the profile body within the 1000-word FAIL budget after the additive fixes above.

## [1.8.1] — 2026-07-12

Adversarial-verify round 2 (`reports/review-loop/descriptive-translation-reviewer.verify2.md`): fixed the one
surviving must-fix (SCOPE_BROADENED). The liturgical-verse example's formal-orientation clause cited P104 and
P162 (P162 is scoped to legal documents / multilingual treaties; P104 to obligatorily-forced grammatical
categories) — regrounded to P105 (formal equivalence matches source form and content closely) for the
form-preservation part and P036 (word-for-word rendering produces opaque target text; sacred-text exception)
for the opacity risk. No claim changed; no new claim introduced. must-fix now 0.



Review-loop round r4 (`reports/review-loop/descriptive-translation-reviewer.r4.review.md`): applied all three
must-fixes and the high-value should-fixes, staying grounded in the existing 180-principle spine (no new claim
introduced).

### Fixed
- **MF-1 — register apparatus owned by two skills with no tie-breaker** — `translation-procedures-and-shifts`
  step 10 (P168) built a full Field/Tenor/Mode register profile that `register-discourse-and-audiovisual-constraints`
  (P064) already owns. Added reciprocal boundary sentences: the procedures skill now reads a marked
  Field/Tenor/Mode feature only far enough to name the procedure/shift it motivates and routes the full
  register profile to the register skill; the register skill's step 5 states it owns the full field/tenor/mode
  register-and-cohesion analysis while naming the specific V&D/Catford procedure a marked feature motivates
  routes back to the procedures skill. Cites P168 / P064 respectively; no claim changed.
- **MF-2 — skopos/brief territory overlapped `text-type-skopos-and-the-brief`** — `translation-quality-and-applied-studies`
  step 13 (P112) reviewed whether a commentary grounded itself in purpose/skopos, method, readership, and a
  translation specification. Added a boundary clause: whether the brief/skopos hierarchy was the right one and
  was followed routes to `text-type-skopos-and-the-brief`; this skill reviews only whether the evaluation
  **method** documented that specification before scoring. Added the reciprocal pointer to
  `text-type-skopos-and-the-brief` step 1 (P009).
- **MF-3 — router `description` collided with `translation-quality-reviewer`** — reworded the `profile.yaml`
  `role` opener so the distinguishing lens leads the exported dispatch string: "A reviewer of translation
  strategy and descriptive method — not corpus-based quality scoring, which routes to
  translation-quality-reviewer …". The exported `description` opener now reads distinguishing-first and names
  the corpus-quality-scoring contrast (the sibling's territory) instead of the generic
  "reviewer of translations…" opener. Re-exported.

### Changed
- **SF (golden-tests coverage)** — added **NR-004** (corpus-based quality metrics / QA scoring →
  `do_not_invoke`, `translation-quality-reviewer`) and **NR-005** (scientific/technical terminology risk →
  `do_not_invoke`, `technical-translation-advisor`), the two load-bearing `when_not_to_use` routes previously
  asserted but never behaviourally verified (matching the NR-003 pattern).
- **SF (`handoff_rules` internal consistency)** — added a `handoff_rules` bullet listing the three sibling
  routes (`translation-equivalence-advisor` / `translation-quality-reviewer` / `technical-translation-advisor`),
  mirroring `when_not_to_use`, so the section is self-sufficient; added the matching `handoff_rules[2]`
  `faithfulness-report.yaml` entry (routing directive, uncited by design).
- **SF (`test-results.md` drift)** — corrected the negative-routing count (now 5) and inlined the actual
  v1.8.0 self-check verdict (PASS with the non-blocking `body-size` WARNING) instead of pointing only at CLI
  output.
- `agent_version` 1.7.0 → 1.8.0; `tests/golden-tests.yaml` re-stamped `profile_version: 1.8.0`. Adapter
  re-exported; skill digests re-stamped after the skill-body edits.

### Deferred
- **SF (Nord function-plus-loyalty)** — deferred: promoting C00155 would introduce a new principle into the
  spine, outside this grounded fix pass (no new claim introduced).
- **SF (P105 formal/dynamic continuum), SF (per-skill Provenance-body dedup across all 12 skills), and
  NICE N-items** — polish/faithfulness-nuance on a passing package, left to a dedicated pass to avoid
  regression risk.

## [1.7.0] — 2026-07-12

Review-loop round r3 (`reports/review-loop/descriptive-translation-reviewer.r3.review.md`): independent
re-verify after the v1.6.0 fixes; applied the must-fix and the high-value should-fixes, staying grounded in the
existing 180-principle spine (no new claim introduced).

### Fixed
- **MF-1 — stale golden-tests version stamp** — `tests/golden-tests.yaml` still read `profile_version: 1.5.0`
  (the v1.6.0 bump re-exported the adapter but skipped the golden re-stamp). Set to `1.7.0`, matching
  `agent_version` and the exported adapter.

### Changed
- **SF-2 — `when_not_to_use[0]` run-on split** — the review-vs-produce boundary now stands alone in `[0]` (still
  the clause the exporter surfaces in the router `description`) and the three sibling routes become three
  separate bullets, one per sibling (`translation-equivalence-advisor` / `translation-quality-reviewer` /
  `technical-translation-advisor`); `faithfulness-report.yaml` `when_not_to_use` entries remapped to `[0..6]`.
- **SF-3 — `handoff_rules[1]` citation scope** — split into two sentences so `(P029)` scopes only the publisher's
  commercial/economic clause; the subject-matter/legal/typesetting clause is a separate uncited-by-design scope
  boundary. The ledger opening enumeration and the faithfulness note now say the *scope clause* is uncited, not
  the whole rule.
- **SF-5 — P047 Frawley/Blum-Kulka de-linked** — the **P047 statement** now marks Frawley's semiotic third-code
  thesis and Blum-Kulka's empirical explicitation hypothesis as two independent lines (corpus findings on
  explicitation neither confirm nor refute the third-code claim of relative autonomy); the matching
  `domestication-foreignization-and-visibility` step 4 no longer cites explicitation as evidence of relative
  autonomy. Cites P047 only; no claim strengthened.
- **SF-7 — P053 Camus disambiguation** — the camp/register worked example in the **P053 statement** is now
  attributed to *Renaud* Camus (author of *Tricks*), not Albert Camus.
- **SF-9 — lens-specific ranking heuristics** — added a lens-anchored ranking criterion to the two skills that
  closed on a bare "highest-impact first" (`descriptive-method-and-translational-norms` step 22;
  `culture-ideology-power-and-rewriting` step 21), matching the other ten skills.
- **SF-4** — recorded the converged independent re-verify (`MUST_FIX_COUNT: 0` after fixes) in the ledger
  v1.7.0 entry.
- `agent_version` 1.6.0 → 1.7.0. Adapter re-exported; skill/reference digests re-stamped.

### Deferred / rejected
- **SF-1** (name three sibling boundaries in the exported router `description`) — deferred: the exporter clips
  the exclusion at its first sentence / ~85 chars, so with the review-vs-produce boundary correctly leading
  `when_not_to_use[0]` the sibling names do not fit; the body carries the full routing (same disposition as the
  v1.6.0 SF-6 defer — an exporter constraint, not a defect).
- **SF-6** — rejected: the source (Munday, C00071) states formal equivalence "suits academic or legal settings",
  so P105/P124's Nida/legal pairing is faithful; no change.
- **SF-8** — verified, no change: P111's four Chesterman approaches faithfully paraphrase Munday (C00346).
- NICE N1–N14 — polish on a passing package, left to a dedicated pass.

## [1.6.0] — 2026-07-12

Consolidated review-loop round r2: applied all three must-fixes and the high-value should-fixes, staying
grounded in the existing 180-principle spine (no new claim introduced).

### Fixed
- **MF-1 — Koller's five relations inverted into a "fixed-order ladder"** — replaced the
  "escalate through … trying denotative" framing (which contradicts P106's own body) in all three condensed
  restatements: the `references/descriptive-translation-principles-index.md` P106 summary, the
  `equivalence-orientations-and-effect` Purpose sentence, and the PB-P106 `expected_behaviour` in
  `tests/principle-behaviour-tests.yaml` — now "weigh Koller's five equivalence relations against each other
  by the needs of the communicative situation, as simultaneous competing frames rather than a fixed-order
  ladder"; reframed the matching P106 anti-pattern to match. Cites P106 only.
- **MF-2 — two same-package skills overlapped with no tie-breaker** — added a boundary sentence to
  `domestication-foreignization-and-visibility` (owns the fluency-illusion + domesticating/foreignizing-axis
  judgment) and `culture-ideology-power-and-rewriting` (owns the institutional/agent, reception, and ideology
  judgment; on overlap each leads with its own), mirrored into each skill's frontmatter `description` and into
  `profile.yaml` `knowledge_partition.always_on[6]`/`[7]`. The prior v1.5.0 ledger's "already carries
  tie-breaker/boundary language" claim was false and is corrected in the ledger.
- **MF-3 — ~20 truncated / ungrammatical index summaries** — hand-repaired every one-line summary in
  `references/descriptive-translation-principles-index.md` that ended on an article/conjunction/preposition or
  a bare possessive (P003, P024, P029, P033, P034, P037, P040, P050, P061, P064, P066, P069, P093, P106, P111,
  P112, P113, P121, P128, P139, P172, P174, P175, P180), snapping each to a clause boundary and grounded in the
  full principle statement.
- **SF-1 — AVT skill invited a "dubbing script" it had no criteria for** — narrowed the
  `register-discourse-and-audiovisual-constraints` `description` and Inputs to audiovisual signifying-code
  analysis + subtitling-specific shortening constraints (states it carries no dubbing isochrony/lip-sync or
  voice-over criteria); removed "or dubbing script" from Inputs, matching `profile.yaml`.
- **SF-2 — House error taxonomy mischaracterised as a severity gradient** — reworded the same skill's Purpose
  from "grades an error's severity (P065)" to "classifies an error's type/origin … not its severity", grounded
  in P065's covertly-erroneous (dimensional) vs overtly-erroneous (denotative/target-system) distinction.
- **SF-3 — P121 omitted Koller's fifth (formal/expressive) relation** — added "formal (formal-aesthetic/
  expressive)" to P121's Koller enumeration, matching P106's five relations and its dependent adapter invariant.
- **SF-5 — three same-package equivalence skills had no cross-cue** — added a one-line same-package routing cue
  to the `equivalence-orientations-and-effect`, `meaning-signification-and-equivalence-critique`, and
  `translation-procedures-and-shifts` descriptions (orientation/effect → the first; theory-of-meaning premise →
  the second; procedure/shift naming → the third).

### Changed
- **N1** — dropped the unsourced "1960s-70s" date qualifier from the P121 index gloss.
- **N3** — dropped "always" from P047 (Blum-Kulka explicitation *tendency*, not an absolute).
- **N4** — normalised the `Literal-Free …` index heading en-dash to a hyphen to match the slug.

### Deferred
- **SF-4 (partial), SF-6, SF-7, SF-8, SF-9, N2, N5, N7, N8, N9, N10, N11**, and the MF-3 generator-lint —
  see the provenance-ledger v1.6.0 Deferred list for the per-item reason. These are structural/stylistic or
  factory-level items on a passing package, left to a dedicated pass.

## [1.5.0] — 2026-07-12

Consolidated review-loop round: applied the must-fix and the high-value should-fixes, staying grounded in
the existing 180-principle spine (no new claim introduced). Supersedes the open `r5.review.md` round (its
two must-fixes were re-triaged to should/nice and downgraded), resolving the `status: ready`-vs-open-round
contradiction.

### Fixed
- **M1 — `text-type-skopos-and-the-brief` written in translate-it-yourself voice** — rewrote every
  Procedure step (1–15) from production-imperative voice ("Make/Drive/Adjust/Orient/Take/Apply/Treat…") into
  reviewer voice ("Check/Verify/Confirm that…"), matching the other 11 skills and the no-production boundary.
  Same principle citations; no claim changed.
- **S2 — `meaning-signification-and-equivalence-critique` step 6 leaked into equivalence-mechanism territory**
  — reworded to stay on the theory-of-meaning side (which descriptive level a claim rests on) and cross-reference
  the sibling `translation-equivalence-advisor` for the mechanism it must not evaluate (still cites P109).
- **S13 — `literal-free-strategy-history-and-retranslation` steps 4 & 15 in imperative voice** — reworded
  step 4 (P036) and step 15 (P173) into review checks ("Check that the translator defaulted…/chose…").

### Changed
- **S1 / S6 — `when_not_to_use`** — `[0]` now leads with the highest-stakes boundary ("does not translate or
  certify a rendering correct"), which the exporter surfaces in the router `description`, followed by three
  **parallel** `route … to \`sibling\`` clauses; folded the redundant "produced end to end" bullet into the
  guaranteed-correct-rendering bullet.
- **S8 — `when_to_use[0]`** — split the garden-path clause ("…by descriptive method — reviewing losses against
  the source and the brief, not scored against a fixed quality metric").
- **S3 — `knowledge_partition.always_on[11]`** — added a sibling differentiator (evaluation-method soundness
  stays here; corpus/QA scoring output routes to `translation-quality-reviewer`); always-on tier is free of the
  body budget.
- **S11 — skill `description` lead-ins** — standardized the four "Use when…" descriptions (deforming,
  descriptive-method, hermeneutics, text-type) to the third-person "Reviews…" pattern.
- **S12 — `register-discourse-and-audiovisual-constraints` description** — front-loaded distinctive trigger
  vocabulary (Hallidayan field/tenor/mode, House's overt/covert axes, subtitling/AVT), dropped the generic
  "flagging violations of the cited principles" boilerplate.
- **S10 — `examples`** — added one `advise` (operative-text orientation) and one `compare` (formal vs dynamic
  liturgical verse) worked example (examples are outside the body-word budget).
- **S5 / S7 / S9 — body trims** — split `forbidden_behaviours[3]` into two singly-cited bullets (P075; P062/P038),
  deleted the `handoff_rules[1]` authoring meta-sentence, keeping the body under the 1000-word hard cap.
- **S4 — `source_of_truth_policy.precedence`** — dropped the mis-cited **P114**, replaced with **P107**
  (Vermeer's skopos grounds "the brief's purpose governs").
- **N6 — `quality_bar[3]`** — added **P052** (re-coding, not omission).
- **S14 — P014** — restored Berman's canonical pairing "ennoblement and popularization" (grounded in P081),
  echoed in `deforming-tendencies-and-translation-loss` step 1.
- **S15 — P010** — named the term "initial norm" (adequacy vs acceptability), cross-referencing P023's
  adequacy-acceptability axis, so Toury's initial→preliminary→operational structure is named whole.
- **`tests/golden-tests.yaml`** re-stamped `profile_version: 1.4.0 → 1.5.0`.
- `agent_version` 1.4.0 → 1.5.0.

### Deferred
- NICE N1–N5, N7–N9 (principle-annotation hedges and cross-references) — polish on a passing package, left to
  a dedicated pass to avoid regression risk.

## [1.4.0] — 2026-07-12

Review-loop round 4 (`reports/review-loop/descriptive-translation-reviewer.r4.review.md`): applied the
must-fix and the high-value should-fixes, staying grounded in the existing 180-principle spine (no new claim
introduced).

### Fixed
- **M1 — truncated router `description` "Not for" clause** — the exported frontmatter `description` (the
  dispatch field) ended on a bare noun: `…Route to \`translation-equivalence-advisor\` when the
  linguistic-equivalence mechanism`. Root cause: `_clean_clause`'s 85-char clip landed on a word boundary
  because `when_not_to_use[0]`'s first comma fell past the clip. Front-loaded `when_not_to_use[0]` so a
  complete self-contained clause ("…for the equivalence mechanism itself") sits before its first comma
  within ~85 chars; the dispatch clause now reads as a finished thought. Meaning preserved (mechanism →
  sibling; orientation-fit → here). Re-exported.

### Changed
- **S — `inputs.required`** — split the single omnibus bullet (5 bundled asks) into 5 discrete list items
  (artifact under review, source+target, orientation/strategy, brief/function, quality claim) so
  missing-context detection has per-item checks.
- **S — `knowledge_partition.always_on[5]` (register/discourse/AV)** — restored the P090 caveats dropped at
  profile level: a source-target register/cohesion mismatch may be a legitimate strategy (explicitation,
  compensation) rather than automatically an error, and the Hallidayan/Gricean apparatus is applied with
  caution outside English-oriented language pairs. Grounded in P090 (already cited); always-on tier is free
  of the body-size budget.
- **S — `tests/golden-tests.yaml`** — re-stamped `profile_version: 1.2.0 → 1.4.0` (stale since v1.3.0) and
  added **NR-003**, the missing negative-routing test for the thrice-reworked `when_not_to_use[0]` sibling
  clause (a word/idiom-level equivalence-mechanism prompt routes to `translation-equivalence-advisor`).
- `agent_version` 1.3.0 → 1.4.0.

### Deferred
- Skill-body polish (level-1 `description` trims on 2 skills, compound-step splits on 4 dense skills, one
  worked example per skill's Output) and principles-annotation notes (House secondary-grounding note on
  P021/P065/P168, P023-vs-P165 adequacy-homonym note, P111 Chesterman three-vs-four recount) — should/nice
  polish on a converged, passing package; left to a dedicated pass to avoid regression risk, consistent with
  the S7 deferral in v1.2.0/v1.3.0.

## [1.3.0] — 2026-07-12

Review-loop round 3 (`reports/review-loop/descriptive-translation-reviewer.r3.review.md`): applied the
must-fix and the high-value should-fixes, staying grounded in the existing 180-principle spine.

### Fixed
- **M1 — stale citation in `examples[1]`** — the never-translate/never-sign-off note cited
  `(forbidden behaviours, P070, P100)`, but v1.2.0 had dropped P070/P100 from the matching
  `forbidden_behaviours[0]` as an uncited-by-design product-scope boundary. P100 appeared nowhere else,
  making it a dangling citation. Changed to `(forbidden behaviours)` so the example matches the rule.
- **S3 — `minimum_useful_output`** — the bar was phrased only in review-mode "flaw" terms; broadened to
  gate `advise` (recommendation + orientation) and `compare` (brief-weighted side-by-side) as well.
- **S4 — `when_to_use[2]`** — reworded the garden-path/comma-spliced fluency-and-visibility trigger into
  a single unambiguous sentence (it seeds the exported routing description).
- **S5 / S6 — `when_not_to_use[0]`** — narrowed the routed-away scope to the linguistic-equivalence
  **mechanism** (disjoint from this package's orientation-fit judgment in P106/P109), and reordered so the
  exported `description` surfaces the `translation-equivalence-advisor` sibling cue within the router's
  character budget.
- **S8 — House's two same-named axes** — `register-discourse-and-audiovisual-constraints` Purpose now
  states the overt/covert translation-**type** typology (P021) and the overtly-/covertly-**erroneous**
  error taxonomy (P065) name different judgments and are not to be conflated.
- **S9 — theorist attribution** — named the originators at point of use: Lefevere (refraction/rewriting,
  P001/P050), Even-Zohar/polysystem (P002), Vermeer (Auftrag/skopos, P009/P062), with the echoing skill
  steps updated to match. Attribution only; no claim strengthened.

### Changed
- **S1 — faithfulness coverage** — `faithfulness-report.yaml` extended from 20 to 35 findings, adding the
  12 `knowledge_partition.always_on` bullets, `minimum_useful_output`, and `when_not_to_use[0..4]`
  (all WITHIN_SCOPE, no over-claim).
- **S2 — provenance accounting** — the ledger's citation-accounting sentence now lists `examples` and
  declares example citations audited + re-checked on every version bump (M1's root cause).

### Deferred
- **S7 — skill-body footprint** — an optimization on a passing package; all 12 skills already sit under
  the 500-line factory limit. Left to a dedicated pass to avoid regression risk. NICE items N1-N14 not applied.

## [1.2.0] — 2026-07-12

Review-loop round 2 (`reports/review-loop/descriptive-translation-reviewer.r2.review.md`): applied
the 3 must-fixes and the high-value should-fixes, staying grounded in the existing 180-principle spine.

### Fixed
- **M1 — Chaume signifying-code count** — P019 said "ten" but broke into 1+4+6 = 11. Corrected to
  "one linguistic, three acoustic and six visual" (= 10) in P019, and reworded the matching
  `register-discourse-and-audiovisual-constraints` Procedure step to "one linguistic code, three
  further acoustic codes, and six visual codes" so principle and skill agree on one reading.
- **M2 — `quality_bar[2]` over-claim** — "Translation **is** driven by an explicit brief and the
  text's predominant function" stated a functionalist/skopos prescription as settled fact (the exact
  anti-pattern `forbidden_behaviours[2]` forbids). Hedged to "Where a brief and predominant function
  apply, translation is judged against them; a fulfilled skopos never excuses micro-level neglect".
- **M3 — Adapter routing `description`** — the exported `description` truncated mid-clause
  ("…wants its equivalence — Not for:") and dropped the sibling-routing disambiguator. Reworded
  `when_to_use[0]` so its clipped clause reads as a complete sentence, and reordered `when_not_to_use`
  so the sibling-axis routing bullet leads (surfacing it in the routing description); re-exported.
  The v1.1.0 ledger claim that the description had already been repaired is corrected below.

### Changed
- **S1 — Profile body trimmed** from ~931 to ~851 words: dropped the duplicated sibling-routing
  `handoff_rules[2]` (routing now stated once, in `when_not_to_use`) and tightened role, modes,
  `quality_bar`, and `when_*` prose. Residual (~851w) is above the 800-word soft budget, so the
  `body-size` self-check still emits a non-blocking WARNING (FAIL threshold is 1000).
- **S4** — `quality_bar[1]` gains P059 (illusory equivalent effect), matching `knowledge_partition`.
- **S5** — `forbidden_behaviours[0]` citations (P070, P100) dropped; the "never translate / never
  sign off" boundary is a product-scope decision, left as an uncited scope boundary.
- **S7** — P106 and `equivalence-orientations-and-effect` step 6 reworded: Koller's five relations
  weighed against each other as simultaneous competing frames, not a fixed-order escalation ladder.
- **S8** — P121 no longer mis-dates Newmark's semantic/communicative pair as "1960s-70s" theory;
  the decade qualifier is dropped.
- **S9(a)** — `meaning-signification-and-equivalence-critique` description no longer repeats the same
  clause verbatim twice.
- **S2** — `tests/golden-tests.yaml` re-stamped `profile_version: 1.2.0`, `tier: 2`.
- `agent_version` 1.1.0 → 1.2.0.

## [1.1.0] — 2026-07-12

Review-loop round 1 (`reports/review-loop/descriptive-translation-reviewer.r1.review.md`): applied
all must-fixes and the high-value should-fixes, staying grounded in the existing 180-principle spine.

### Fixed
- **Adapter invariant layer truncation** — the installed/canonical adapter had 101 `…`-severed
  invariant lines and a mid-clause frontmatter `description`. Re-exported through the current
  `compile_invariants`/`export_claude_agent` path so each invariant renders its full principle
  sentence and the routing description ends at a clause boundary.
- **Skill bodies re-authored to the GOLD shape** — all 12 `skills/*/SKILL.md` rewritten so every
  Procedure and Anti-patterns bullet is a complete, self-contained sentence before its `(Pxxx)` cite
  (removing the mid-clause truncations such as "Surface a translation's (P113)."), Anti-patterns now
  cover every principle in the skill (not a silent 7-item cap) as concrete bad-finding symptoms, and
  each gains a `description:` frontmatter field for routing. Frontmatter provenance preserved.
- **Faithfulness re-grounding** — `handoff_rules[0]` re-anchored to P029 (publisher holds the publish
  decision) + P070 (macro/micro split), dropping the mis-grounded P009/P162/P080; `handoff_rules[1]`
  re-anchored to P029 for commercial/economic constraints. `faithfulness-report.yaml` gains entries
  for `handoff_rules[0..2]` and `canonical_owner`.
- **Cross-sibling routing** — `when_not_to_use` + `handoff_rules` now name `translation-equivalence-advisor`,
  `translation-quality-reviewer`, and `technical-translation-advisor` by slug/axis; `when_to_use[0]`
  differentiated from the quality-reviewer sibling.
- **Faithfulness weakening** — P047 no longer states Blum-Kulka's explicitation hypothesis as
  "confirmed by corpus study" (now a proposed, contested tendency with varying support); P115 frames
  the technical-texts-easier point as Ortega's comparative observation and marks technical/scientific
  subject-matter risk out of remit.

### Changed
- `tier: 1` → `tier: 2` (3-source manifest; matches siblings and the build record).
- Profile body trimmed (removed quality_bar/forbidden redundancy) toward the word budget.
- `agent_version` 1.0.0 → 1.1.0.

## [1.0.0] — 2026-07-12

### Added
- Initial release of the **descriptive-translation-reviewer** subagent (Tier 1), authoring the LLM layer over the
  already-assembled, deterministically-valid distilled spine (180 principles P001-P180 /
  984 claims from three distillation-only sources).
- `profile.yaml` derived from the 180 promoted principles: role, when/when-not-to-use, three modes
  (review / advise / compare), quality bar, forbidden behaviours, handoff rules, and a
  12-skill / 2-reference `knowledge_partition` covering every principle exactly
  once.
- 12 authored skills partitioning all 180 principles; 2 references
  (principles index + evidence notes).
- `reports/faithfulness-report.yaml` — every load-bearing profile rule graded WITHIN_SCOPE against
  its principles (no rule stronger than its evidence).
- `tests/golden-tests.yaml` (6 golden, 2 negative-routing,
  2 missing-context) and `tests/principle-behaviour-tests.yaml` (one behaviour test per
  principle, 180 total).
- Claude Code adapter exported to `adapters/claude-code/` and installed under
  `.claude/agents/generated/`.

### Grounding
- Three distillation-only sources: Jeremy Munday, *Introducing Translation Studies* (2016);
  Lawrence Venuti, ed., *The Translation Studies Reader* (2012); Gideon Toury, *The Nature and Role
  of Norms in Translation* (1995).
