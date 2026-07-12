# Provenance Ledger — descriptive-translation-reviewer

Canonical record of what grounds this subagent. The profile, skills, references, faithfulness
report, and tests are all derived from the distilled spine in this package
(`principles/principles.yaml` -> `analysis/claims.jsonl` -> `evidence/evidence-records.yaml` ->
`sources/anchors/*.anchors.jsonl`), assembled by the map->reduce build. No load-bearing profile rule
field is an orphan: every `quality_bar`, `forbidden_behaviours`, `handoff_rules`,
`knowledge_partition.always_on`, `source_of_truth_policy`, and `examples` value cites the promoted
principle(s) it restates — except a small number of product-scope boundaries (`forbidden_behaviours[0]`,
the never-translate/never-sign-off note in `examples[1]`, and the subject-matter/legal/typesetting scope
clause of `handoff_rules[1]`) that state a review-vs-produce decision rather than a source claim and are left
uncited by design; note that `handoff_rules[1]`'s other clause (the publisher's commercial/economic
constraints) does carry a `(P029)` citation. Inline `examples` citations are audited
on the same footing as rule fields and are re-checked whenever a cited field's grounding changes on a
version bump. (Descriptive fields — `role`, `when_to_use`, `inputs`, `outputs` — carry no inline tags, per
repo convention.)

## Sources

| source_id | title | author | year | rights |
|-----------|-------|--------|------|--------|
| introducing-translat-4a29c5ca | Introducing Translation Studies: Theories and Applications | Jeremy Munday | 2016 | distillation-only |
| translation-studies-45ee8f34 | The Translation Studies Reader | Lawrence Venuti (ed.) | 2012 | distillation-only |
| norms-in-translation-ad249b8d | The Nature and Role of Norms in Translation | Gideon Toury | 1995 | distillation-only |

All three sources are **distillation-only**: paraphrase and restructure only, no verbatim quotation
(see `.claude/rules/rights-and-quotation-policy.md`; enforced by `quote_scan`). They are canonical
descriptive-translation-studies works: Munday's survey of the discipline, Venuti's reader of primary
essays, and Toury's statement of the norms programme.

## Distillation

Spine: 180 promoted principles (P001-P180; 141 high-confidence) over
984 atomic claims, with evidence records and chunk anchors. The 180 principles are
partitioned across 12 skills, each principle owned by exactly one skill; the two
references index and ground them.

## Version History

- **1.7.0** (2026-07-12) — Review-loop round r3
  (`reports/review-loop/descriptive-translation-reviewer.r3.review.md`; no prior decision silently
  overwritten). Independent re-verify after the v1.6.0 fixes: deterministic gates (validate / quote_scan /
  truncation grep) all clean, one must-fix and three should-fixes applied, staying grounded in the existing
  180-principle spine (no new claim introduced). **Must-fix:** **MF-1** — re-stamped
  `tests/golden-tests.yaml` `profile_version` (stale `1.5.0`, skipped by the v1.6.0 bump) to `1.7.0`, matching
  `agent_version` and the exported adapter. **Should-fix:** **SF-2** — split `when_not_to_use[0]`'s run-on:
  the review-vs-produce boundary now stands alone in `[0]` (still the clause surfaced in the exported router
  `description`), and the three sibling routes are three separate bullets `[1..3]`
  (`translation-equivalence-advisor` / `translation-quality-reviewer` / `technical-translation-advisor`);
  faithfulness entries remapped to `[0..6]`. **SF-4** — this entry records the independent re-verify converging
  to `MUST_FIX_COUNT: 0` after fixes (closing the v1.6.0 "SF-4 partial" item). **Field→grounding changes:**
  **SF-3** — split `handoff_rules[1]` into two sentences so the `(P029)` citation scopes only the publisher's
  commercial/economic clause; the subject-matter/legal-validity/typesetting clause is a separate
  uncited-by-design scope boundary. The ledger opening enumeration and the `faithfulness-report.yaml` note are
  corrected to say the *scope clause* (not the whole rule) is uncited. **SF-5** — **P047 statement** now marks
  Frawley's semiotic third-code thesis and Blum-Kulka's empirical explicitation hypothesis as two independent
  lines within the shared 1980s relative-autonomy assumption, not as evidence for one another (corpus findings
  on explicitation neither confirm nor refute the third-code claim); the matching
  `domestication-foreignization-and-visibility` step 4 no longer treats explicitation as evidence of relative
  autonomy. Reduces over-linkage; cites P047 only; no claim strengthened. **SF-7** — **P053 statement** now
  attributes the camp/register worked example to *Renaud* Camus (author of *Tricks*, the text Harvey's camp-talk
  essay analyses), disambiguating from Albert Camus. **SF-9** — added a lens-anchored ranking heuristic to the
  two skills that closed on a bare "highest-impact first"
  (`descriptive-method-and-translational-norms` step 22 and `culture-ideology-power-and-rewriting` step 21),
  matching the other ten skills' sibling pattern (uncited synthesis-ordering step). Adapter re-exported;
  skill/reference digests re-stamped after the principle-statement + skill-body edits. **Deferred / rejected:**
  **SF-1** (name the three sibling boundaries in the exported router `description` "Not for") — the exporter
  clips the exclusion at its first sentence and ~85 chars, so with the highest-stakes review-vs-produce boundary
  correctly leading `when_not_to_use[0]`, the sibling names do not fit; the body `when_not_to_use` carries the
  full three-way routing (same disposition as the v1.6.0 SF-6 defer — a factory-level exporter constraint, not a
  package defect). **SF-6 — rejected:** pairing Nida formal-equivalence with "academic or legal texts" is *not*
  an over-claim: the source (Munday, claim C00071) states formal equivalence "suits academic or legal settings",
  so P105/P124 are faithful; the gloss-translation case already leads both. **SF-8 — verified, no change:**
  P111's "Chesterman's four approaches (textual, cognitive, sociological, cultural)" is a faithful paraphrase of
  Munday (claim C00346, which attributes exactly those four to Chesterman); keeping it is correct under the
  faithfulness rule. **NICE N1–N14** — structural/stylistic polish on a passing package, left to a dedicated
  pass.
- **1.6.0** (2026-07-12) — Consolidated review-loop round r2 (no prior decision silently overwritten).
  Applied all three must-fixes and the high-value should-fixes on the existing 180-principle spine; no new
  claim introduced. **Must-fix:** **MF-1** — corrected the inverted Koller framing ("escalate through … trying
  denotative", which contradicts P106's own body) in the `principles-index` P106 summary, the
  `equivalence-orientations-and-effect` Purpose sentence, and the PB-P106 test `expected_behaviour`, and
  reframed the matching P106 anti-pattern, to P106's own "simultaneous competing frames, not a fixed-order
  ladder" language (cites P106 only; no claim changed). **MF-2** — added a same-package boundary/tie-breaker to
  `domestication-foreignization-and-visibility` (owns fluency-illusion + domesticating/foreignizing-axis
  judgment) and `culture-ideology-power-and-rewriting` (owns institutional/agent, reception, ideology
  judgment), mirrored into each skill `description` and `knowledge_partition.always_on[6]`/`[7]`. **This
  corrects the v1.5.0 entry's claim that the overlap "already carries tie-breaker/boundary language": grep of
  both SKILL.md files and the profile confirmed no such text existed before this round; the tie-breaker is
  added here, not re-triaged away.** **MF-3** — hand-repaired ~24 truncated/ungrammatical one-line summaries
  in `references/descriptive-translation-principles-index.md` (P003, P024, P029, P033, P034, P037, P040, P050,
  P061, P064, P066, P069, P093, P106, P111, P112, P113, P121, P128, P139, P172, P174, P175, P180), each snapped
  to a clause boundary and grounded in the full principle statement. **Should-fix:** **SF-1** — narrowed the
  `register-discourse-and-audiovisual-constraints` `description`/Inputs to subtitling-specific shortening
  constraints (no dubbing isochrony/lip-sync/voice-over criteria), removing the "dubbing script" input to match
  `profile.yaml`. **SF-2** — reworded that skill's Purpose so House's overtly-/covertly-erroneous taxonomy
  "classifies an error's type/origin, not its severity" (grounded in P065). **SF-5** — added a same-package
  routing cue to the three equivalence-adjacent skill descriptions (`equivalence-orientations-and-effect`,
  `meaning-signification-and-equivalence-critique`, `translation-procedures-and-shifts`).
  **Field→grounding / statement changes:** **SF-3** — **P121 statement** now enumerates Koller's fifth relation,
  "formal (formal-aesthetic/expressive)", matching P106's five and its dependent adapter invariant (grounded in
  the same Munday/Koller basis as P106; citing fields — `always_on[2]`, `source_of_truth_policy.precedence` —
  keep the P121 id unchanged). **N3** — **P047 statement** drops "always" (Blum-Kulka explicitation is a
  contested *tendency*, not an absolute; reduces claim strength, no field-citation change). **N1** — dropped the
  unsourced "1960s-70s" date from the P121 index gloss. **N4** — normalised the `Literal-Free` index heading
  en-dash to a hyphen. Adapter re-exported; skill/reference digests re-stamped after the principle-statement
  edits. **Deferred:** **SF-4** (partial — the open r4/r5 items are now named in this Deferred list),
  **SF-6** (frontmatter "Not for" sibling clause — the exporter clips the router `description` at ~85 chars
  before the first comma, so three sibling names do not fit; the body `when_not_to_use` already carries the
  full three-way routing), **SF-7**/**SF-8** (procedure-step scannability and anti-pattern-as-smell rewrites
  across all 12 skills — a broad structural pass with faithfulness-regression risk, not a defect), **SF-9**
  (imperative-voice adapter invariants — the preamble/handoff already state the review-only boundary), **N2**
  (P010 "at the base by" wording), **N5** (worked mini-examples), **N7**/**N9**/**N10** (profile
  scan-ability/word-count polish), **N8** (load-on-demand partition), **N11** (uncited-by-design exception
  pointer), and the MF-3 generator-lint (a factory-level tooling change outside this package).
- **1.5.0** (2026-07-12) — Consolidated review-loop fixes (no prior decision silently overwritten).
  **Supersession of the open round:** the earlier `r5.review.md` (which ended `MUST_FIX_COUNT: 2`) is
  **superseded by this consolidated round** — its two must-fixes were re-triaged (the Anti-pattern↔Procedure
  mirroring is justified reviewer redundancy at tier-2 cost, not a defect; the Venuti-adjacent skill overlap
  already carries tie-breaker/boundary language) and downgraded, so no orphan open-must-fix report survives
  this release. **[Corrected in 1.6.0 MF-2: the "already carries tie-breaker/boundary language" claim was
  false — no such text existed in either skill or the profile; the tie-breaker was actually added in 1.6.0.]**
  **Must-fix:** **M1** — rewrote every `text-type-skopos-and-the-brief` Procedure step from
  translate-it-yourself imperative voice ("Make/Drive/Adjust/Orient/Take/Apply/Treat…") into reviewer voice
  ("Check/Verify/Confirm that…"), matching the other 11 skills and the profile's no-production boundary
  (same principle citations; no claim changed). **Should-fix:** **S1/S6** — restructured `when_not_to_use`
  so `[0]` leads with the highest-stakes boundary ("does not translate or certify a rendering correct" — now
  surfaced in the exported router `description`) followed by three **parallel** `route … to \`sibling\``
  clauses (`translation-equivalence-advisor`, `translation-quality-reviewer`, `technical-translation-advisor`);
  folded the redundant "produced end to end" bullet into the guaranteed-correct-rendering bullet.
  **S2** — reworded `meaning-signification-and-equivalence-critique` Procedure step 6 to stay on the theory-of-
  meaning side (which descriptive level a claim rests on) and cross-reference `translation-equivalence-advisor`
  for the equivalence **mechanism** it must not evaluate. **S3** — added a sibling differentiator to
  `knowledge_partition.always_on[11]` (evaluation-method soundness stays here; corpus/QA scoring output routes
  to `translation-quality-reviewer`) — always-on tier is free of the body budget. **S8** — split the garden-path
  `when_to_use[0]`. **S13** — reworded `literal-free-strategy-history-and-retranslation` Procedure steps 4 (P036)
  and 15 (P173) into review voice. **S11** — standardized the four "Use when…" skill `description` lead-ins to
  the third-person "Reviews…" pattern (deforming, descriptive-method, hermeneutics, text-type) and fixed the
  imperative literal-free description. **S12** — front-loaded distinctive trigger vocabulary in the
  `register-discourse-and-audiovisual-constraints` description, dropping the generic "flagging violations"
  boilerplate. **S10** — added one `advise` and one `compare` worked example (examples are outside the body
  budget). **S5/S7/S9** — split `forbidden_behaviours[3]` into two singly-cited bullets, deleted the
  `handoff_rules[1]` authoring meta-sentence, and applied these trims to keep the body under budget.
  **Field→grounding changes:** `source_of_truth_policy.precedence` **P114 → P107** (S4 — P107 grounds
  "brief's purpose governs" via Vermeer's skopos; P114 was selective-preservation, mis-cited); `quality_bar[3]`
  **+P052** (N6 — re-coding-not-omission most precisely grounded by P052); `forbidden_behaviours` now `[3]`
  cites P075 alone and `[4]` cites P062/P038 (S5 — split, citations unchanged); **P010** statement gains the
  term "initial norm" (adequacy vs acceptability; grounded in Toury, cross-referencing P023's adequacy-
  acceptability axis) (S15); **P014** statement pairs "ennoblement and popularization" (S14 — restoring Berman's
  canonical pairing already grounded in P081), echoed in `deforming-tendencies-and-translation-loss` step 1;
  two new `examples` cite P059/P129/P062/P108 (advise) and P104/P162/P059/P105/P118/P062/P036 (compare), all
  already-promoted principles. Adapter re-exported. **Deferred:** NICE N1-N5, N7-N9 (principle-annotation
  hedges and cross-references) — polish on a passing package, left to a dedicated pass.
- **1.4.0** (2026-07-12) — Review-loop round 4 fixes (no prior decision silently overwritten). (1)
  **M1** — repaired the truncated router `description` "Not for" clause at its root: front-loaded
  `when_not_to_use[0]` so a complete self-contained clause ("Route to `translation-equivalence-advisor` for
  the equivalence mechanism itself") lands within the exporter's ~85-char `_clean_clause` budget before its
  first comma, instead of clipping to the bare noun "…the linguistic-equivalence mechanism". Routing meaning
  unchanged (equivalence mechanism → sibling; orientation-fit → here); adapter re-exported. (2) **S** — split
  `inputs.required` into 5 discrete asks for per-item missing-context detection. (3) **S** — restored the
  **P090** caveats to `knowledge_partition.always_on[5]` (register/cohesion mismatch may be a legitimate
  explicitation/compensation strategy, not automatically an error; Hallidayan/Gricean apparatus applied with
  caution outside English-oriented pairs) — grounded in the already-cited P090, no claim strengthened.
  (4) **S** — `tests/golden-tests.yaml` re-stamped `profile_version: 1.2.0 → 1.4.0` and gained **NR-003**, the
  negative-routing test for the `when_not_to_use[0]` sibling clause. **Field→grounding changes:** none —
  `when_not_to_use[0]` and `inputs` are descriptive/routing fields (uncited by convention); `always_on[5]`
  keeps its existing P090 citation. **Deferred:** skill-body polish (2 description trims, 4 dense-skill step
  splits, per-skill Output worked examples) and principles-annotation notes (House P021/P065/P168 secondary
  grounding, P023-vs-P165 adequacy homonym, P111 Chesterman recount) — polish on a converged package, left to
  a dedicated pass (as with S7 in v1.2.0/v1.3.0).
- **1.3.0** (2026-07-12) — Review-loop round 3 fixes (no prior decision silently overwritten). (1)
  **M1** — dropped the stale `P070, P100` citation from `examples[1].ideal_response`'s never-translate/
  never-sign-off note so it matches the uncited-by-design `forbidden_behaviours[0]` (the v1.2.0 decision
  that dropped those two citations); this removes the last dangling `P100` reference in the profile.
  (2) **S2** — the citation-accounting sentence above now lists `examples` and declares example citations
  audited + re-checked on every version bump (M1's root cause). (3) **S3** — broadened
  `minimum_useful_output` to gate all three modes (advise/compare, not review alone). (4) **S4** — reworded
  the garden-path `when_to_use[2]` fluency/visibility trigger. (5) **S5 + S6** — reworded `when_not_to_use[0]`
  so the routed-away scope is the linguistic-equivalence **mechanism** (disjoint from this package's
  orientation-fit judgment in P106/P109) and the exported routing `description` now surfaces the
  `translation-equivalence-advisor` sibling cue. (6) **S8** — `register-discourse-and-audiovisual-constraints`
  Purpose now states House's overt/covert translation-**type** (P021) and overtly-/covertly-**erroneous**
  error taxonomy (P065) are distinct axes, not one judgment. (7) **S9** — named the originating theorists at
  point of use: **Lefevere** in P001/P050 (refraction/rewriting), **Even-Zohar/polysystem** in P002,
  **Vermeer** (Auftrag/skopos) in P009/P062, with the echoing steps in
  `culture-ideology-power-and-rewriting`, `descriptive-method-and-translational-norms`, and
  `text-type-skopos-and-the-brief` updated to match — attribution only, no claim strengthened.
  (8) **S1** — `faithfulness-report.yaml` extended with the 12 `knowledge_partition.always_on` bullets,
  `minimum_useful_output`, and `when_not_to_use[0..4]` (all WITHIN_SCOPE, no over-claim). Adapter
  re-exported; digests re-stamped. **Field→grounding changes:** `examples[1]` P070/P100 dropped (now
  uncited by design). **Deferred:** S7 (skill-body footprint) — an optimization on a passing package; all
  12 skills already sit under the 500-line factory limit, so trimming is left to a dedicated pass to avoid
  regression risk. NICE items N1-N14 not applied.
- **1.2.0** (2026-07-12) — Review-loop round 2 fixes (no prior decision silently overwritten). (1)
  **M1** — corrected the Chaume signifying-code count in **P019** (1+4+6 = 11 → "one linguistic,
  three acoustic and six visual" = 10) and the matching `register-discourse-and-audiovisual-constraints`
  Procedure step. (2) **M2** — hedged `quality_bar[2]`: functionalist skopos no longer stated as
  settled fact ("Translation **is** driven by…" → "Where a brief and predominant function apply,
  translation is judged against them…"). (3) **M3** — repaired the routing **`description`** for real
  (see the v1.1.0 correction note below): reworded `when_to_use[0]` so its clipped clause is a complete
  sentence and reordered `when_not_to_use` so the sibling-routing bullet leads and surfaces in the
  exported description; adapter re-exported. (4) **Field→grounding changes:** `quality_bar[1]` **+P059**
  (illusory equivalent effect, matching `knowledge_partition`); `forbidden_behaviours[0]` citations
  **P070, P100 dropped** (never-translate/never-sign-off is a product-scope boundary, left uncited like
  `handoff_rules[1]`); removed `handoff_rules[2]` (the v1.1.0 sibling-routing directive) as a duplicate
  of the `when_not_to_use` routing bullet — routing is now stated once. (5) Weakened two principle
  statements to match source support: **P106** (Koller's five relations are simultaneous competing
  frames, not a fixed-order escalation ladder; skill `equivalence-orientations-and-effect` step 6 to
  match) and **P121** (dropped the "1960s-70s" mis-dating of Newmark's semantic/communicative pair).
  (6) Trimmed `meaning-signification-and-equivalence-critique` description (verbatim-duplicated clause).
  (7) Profile body trimmed ~931 → ~851 words; `tests/golden-tests.yaml` re-stamped to 1.2.0 / tier 2.
- **1.1.0** (2026-07-12) — Review-loop round 1 fixes (no prior decision silently overwritten; the
  spine is unchanged except two faithfulness re-wordings below). (1) Re-exported the adapter to
  repair the truncated invariant layer + frontmatter description. *(Correction, recorded in v1.2.0:
  the invariant-layer repair shipped, but the frontmatter `description` remained truncated mid-clause
  and missing the sibling-routing cue in the shipped v1.1.0 adapter — actually repaired in v1.2.0 via
  the profile rewording above.)* (2) Re-authored all 12 skills to the
  GOLD shape (complete Procedure/Anti-pattern sentences before each `(Pxxx)`; Anti-patterns cover
  every principle in the skill; added `description:` frontmatter). (3) **Field→grounding changes:**
  `handoff_rules[0]` re-anchored **P070, P009 → P029, P070** (publication authority now grounded in
  P029; macro/micro split in P070); `handoff_rules[1]` re-anchored **P162, P080 → P029** (commercial/
  economic constraints in P029; legal-validity/typesetting left as an uncited scope boundary); added
  `handoff_rules[2]` (sibling-routing directive, no principle cite — routing only). (4) Weakened two
  principle statements to match source support: **P047** (Blum-Kulka explicitation hypothesis: "later
  confirmed by corpus study" → proposed, contested tendency with varying support) and **P115** (frames
  the technical-texts-easier point as Ortega's comparative observation, marks technical/scientific
  subject-matter risk out of remit). (5) `tier: 1 → 2`; profile body trimmed. `faithfulness-report.yaml`
  extended with `handoff_rules[0..2]` and `canonical_owner` entries.
- **1.0.0** (2026-07-12) — Initial LLM-authored layer over the pre-built distilled spine: profile
  (role, three modes, quality bar, forbidden behaviours, 12-skill / 2-reference
  knowledge partition), faithfulness report, 12 skills, 2 references, golden +
  principle-behaviour tests, and the exported Claude Code adapter. No prior profile decisions
  superseded.
