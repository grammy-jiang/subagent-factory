# Review Loop — descriptive-translation-reviewer — Round r2 (re-review)

Package: `subagents/descriptive-translation-reviewer/` · agent_version 1.9.0 · Tier 2.
Consolidated across deterministic gates + 7 reviewer lenses (agent-skills, profile,
faithfulness, ai-agent-engineering, translation-equivalence, translation-quality,
technical-translation). Deduped, most-severe first.

> Note: an earlier r2 report (against v1.5.0) raised 3 must-fix — MF-1 Koller "escalate
> through" ladder, MF-2 domestication/culture-ideology overlap, MF-3 truncated index
> summaries. All three are **verified resolved in v1.9.0**: no "escalate through/trying
> denotative" text remains in references/skills/tests; the P113 index summary is now a
> complete sentence; profile-reviewer confirms the two adjacent-skill boundaries carry
> explicit "leads with" tie-breaker language. This report supersedes that one.

## Deterministic gates — ALL PASS (0 FAIL)

- `validate_generated_package` → **VALIDATION PASSED** (0 FAIL; Phase 8 self-check WARN only — body ~978w, under 1000w FAIL line).
- `quote_scan` → **PASS** (no verbatim quotation).
- Truncation grep (ellipsis + severed adapter invariant parenthetical) → **clean**.

Deterministic FAILs = 0.

---

## MUST-FIX

### M1 — `translation-quality-and-applied-studies` skill omits the sibling-subagent routing boundary at its trigger surface
- **Where:** `skills/translation-quality-and-applied-studies/SKILL.md` — `description` (L3–6),
  `## When to use` (L54–60), `## Procedure` (L62–79).
- **Severity:** must-fix (agent-skills-advisor).
- **Problem:** `profile.yaml:184-187` (`always_on` for this skill) + `when_not_to_use` (L35–36)
  route "run corpus-based quality metrics / QA scoring and return the scores" to the sibling
  `translation-quality-reviewer`. The SKILL.md — the only artifact scanned at trigger time —
  never names that sibling anywhere. This is the skill most likely to catch a "score this
  translation" request, so the single disambiguation that matters most is invisible where
  triggering happens. Sibling skills (equivalence-orientations, meaning-signification,
  translation-procedures) correctly thread their external-package tie-breaker into `description`.
- **Fix:** add to `description` (mirror in a When-NOT bullet): "Requests to run corpus-based
  quality metrics or QA scoring and return the scores route to the sibling
  `translation-quality-reviewer`; this skill reviews only whether the evaluation method itself
  is sound."

### M2 — same skill, Procedure step 15 (GILT/localization) invites scope creep with no boundary to `technical-translation-advisor`
- **Where:** `skills/translation-quality-and-applied-studies/SKILL.md` `## Procedure` step 15 (L78).
- **Severity:** must-fix (agent-skills-advisor).
- **Problem:** `profile.yaml:37` routes "scientific/technical target text and terminology risk"
  to `technical-translation-advisor`, but step 15 is the one procedure step across all 12 skills
  that tells the reviewer to directly engage GILT/localization work — squarely technical-
  translation territory. No file in the package names `technical-translation-advisor`, so nothing
  redirects terminology-risk requests out of scope.
- **Fix:** add a boundary clause to step 15 (or the description): "Terminology risk or
  scientific/technical target-text correctness in a localization deliverable routes to
  `technical-translation-advisor`; this skill reviews only whether the localization/
  internationalization framing (fixed-source vs. locale-functionality) is sound."

> Dedup: the ai-agent-engineering should-fix on the adapter `description` omitting the three
> sibling exclusions (SF-1 below) is the **same root defect** as M1/M2 at a different location
> (adapter/profile frontmatter vs. per-skill frontmatter). Closing the sibling-routing gap
> should cover both surfaces.

---

## SHOULD-FIX

### SF-1 — adapter/profile `description` omits the three sibling-routing exclusions *(same root as M1/M2)*
- **Where:** `profile.yaml:1-6` → adapter line 3.
- **Severity:** should-fix (ai-agent-engineering-reviewer).
- **Problem:** the router-visible `description` surfaces only the first when_to/when_not bullet,
  dropping the →`translation-equivalence-advisor` / →`translation-quality-reviewer` /
  →`technical-translation-advisor` exclusions an orchestrator uses to keep the 4-way split
  non-overlapping. A corpus-QA or terminology task could mis-route here on description-match alone.
- **Fix:** compress the sibling-exclusion clauses into the `description` string (e.g. "Not for:
  corpus QA scoring (→translation-quality-reviewer), word/collocation equivalence
  (→translation-equivalence-advisor), technical terminology (→technical-translation-advisor)").

### SF-2 — `inputs.required` unconditionally demands source+target text, mismatching the analysis/norm-claim path
- **Where:** `profile.yaml:43-49`.
- **Severity:** should-fix (ai-agent-engineering-reviewer).
- **Problem:** `when_to_use[1]` covers reviewing a translation-studies analysis / "norm" claim,
  which may carry no source/target pair; `inputs.required` still lists both as required →
  input-contract mismatch between promised scope and required inputs.
- **Fix:** make source+target conditionally required (only for the rendering-critique path), or
  add a note that the pair is required only when reviewing an actual rendering.

### SF-3 — `when_to_use[5]` bundles 4 distinct triggers into one run-on bullet
- **Where:** `profile.yaml:27-29`.
- **Severity:** should-fix (profile-reviewer + ai-agent-engineering agree).
- **Problem:** ideology/institutional critique; hermeneutic/untranslatability claims; V&D/Catford
  shift soundness; TQA-method soundness — 4 scenarios joined by "or"/";" in ~32 words. Passes the
  3–6 count gate but hurts scannability; a caller likely misses that V&D/Catford or TQA-method
  checks are in scope.
- **Fix:** split into 2–3 single-scenario bullets (a documented excursion to 7–8 bullets is
  acceptable — the deterministic gate only FAILs outside 3–6).

### SF-4 — profile body word-count margin thin (~978w vs 1000w FAIL)
- **Where:** `profile.yaml:8-15, 30-32, 84-86`.
- **Severity:** should-fix (profile-reviewer).
- **Problem:** the review-only boundary is stated at full strength 3× (`role` ~46w,
  `when_not_to_use[0]` ~27w, `forbidden_behaviours[0]` ~23w); each additive review-loop round
  shrinks the margin toward hard FAIL.
- **Fix:** keep the full statement once (recommend `forbidden_behaviours[0]`), shorten the `role`
  and `when_not_to_use[0]` restatements to cross-references (~40–60w reclaimed); confirm exact
  count with `python -m tools.subagent_factory.profile_self_check`.

### SF-5 — reviewer-only reframing lives one section above the ~90 imperative invariants it governs
- **Where:** `profile.yaml:8-15` (role) vs adapter Operating Invariants (L26–306).
- **Severity:** should-fix (ai-agent-engineering-reviewer).
- **Problem:** many invariants are 2nd-person imperatives to a translator (P045, P009, P038); read
  in isolation they say "do this," not "check this." The single governing sentence is structurally
  distant. `forbidden_behaviours` already blocks producing a translation, so this is hardening, not
  a live contradiction.
- **Fix:** repeat a short "each rule below is a criterion to check in someone else's translation,
  not an action to perform" line directly under the "Operating invariants (must hold)" header.

### SF-6 — missing reciprocal tie-breaker: `hermeneutics-and-the-limits-of-translatability` ↔ `meaning-signification-and-equivalence-critique`
- **Where:** both files' `description` frontmatter.
- **Severity:** should-fix (agent-skills-advisor).
- **Problem:** both ground substantial Quine content (indeterminacy / inscrutability of reference);
  no "X stays here / Y routes there" sentence → ambiguous or duplicated triggering on Quine-flavoured
  meaning-theory questions.
- **Fix:** add a reciprocal clause to each description (e.g. in meaning-signification: "the
  indeterminacy-of-reference and hermeneutic-motion critique routes to
  `hermeneutics-and-the-limits-of-translatability`; this skill stays on the word/sign-level
  signification premise").

### SF-7 — `text-type-skopos-and-the-brief` Procedure under-specifies vs its own Anti-patterns and sibling skills
- **Where:** `skills/text-type-skopos-and-the-brief/SKILL.md` `## Procedure` steps 2,3,6,8–10,12–15 (L66–79).
- **Severity:** should-fix (agent-skills-advisor).
- **Problem:** one-line paraphrase steps with no failure-mode detail, while this file's own
  Anti-patterns bullets and every sibling Procedure carry that operational detail. An agent
  following the Procedure alone gets materially less actionable guidance here than for the other 11.
- **Fix:** fold the concrete failure-mode detail already in this file's Anti-patterns back into the
  corresponding Procedure steps, matching the density of `equivalence-orientations-and-effect`.

### SF-8 — `register-discourse-and-audiovisual-constraints` still lacks the House-TQA boundary to sibling `translation-quality-reviewer`
- **Where:** that SKILL.md `description` + Procedure step 6 (House overt/covert + field/tenor/mode, P021/P064/P065).
- **Severity:** should-fix (agent-skills-advisor).
- **Problem:** `reports/review-loop/…verify2.md` item B already flagged this overlap and deferred
  it "owner-decide" pending a reciprocal fix on the sibling package; still unresolved. Same class as M1.
- **Fix:** once the sibling package's reciprocal sentence lands, add the matching tie-breaker: a
  House TQA judgment used to produce/certify a corpus-based quality score routes to
  `translation-quality-reviewer`; this skill reviews only the register/discourse analysis method.

### SF-9 — Blum-Kulka explicitation mislabelled a "discourse type" (belongs to Frawley's third code)
- **Where:** `principles/principles.yaml` P047 (~L1146–1152) + `skills/domestication-foreignization-and-visibility/SKILL.md` Procedure step 4.
- **Severity:** should-fix (translation-equivalence-advisor).
- **Problem:** explicitation is a hypothesised *process tendency / translation universal* (increased
  cohesive explicitness), not a claim that translation is a distinct discourse type — that phrasing
  re-merges exactly the Blum-Kulka/Frawley boundary the principle is trying to keep separate.
- **Fix:** reword to "a proposed translating-specific process tendency (or 'universal')," not
  "discourse type."

---

## NICE

- **N1** — Redundant `## Provenance` body footer re-lists the full `provenance.principles` ID set
  (already in frontmatter) in all 12 SKILL.md bodies (loads on every trigger); replace ID list with
  a pointer to the frontmatter block. (agent-skills)
- **N2** — Skill H1 titles don't consistently mirror the `name:` slug (e.g. domestication file adds
  "Translator"); normalise or document a display-title convention. (agent-skills)
- **N3** — `Inputs`/`Output` boilerplate repeated near-verbatim 12×; consolidation candidate only if
  a future token-budget pass targets this package specifically. (agent-skills)
- **N4** — Subtitling figures P069 (38 Roman / 13–15 CJK chars / ~6 s) stated as "near-universal";
  house/platform style varies (cps-based reading-speed targets exist). Already disclosed via profile
  `when_not_to_use` ~2016 scope boundary; soften to "widely used convention (house-style/platform
  dependent)." (equivalence + quality + technical lenses concur — informational, no domain error)
- **N5** — `principles.yaml` P081: the "semblante/rostro/cara" quantitative-impoverishment example
  is attributed to "Arlt's" prose; spot-check the author against Berman's original if a page anchor
  exists (concept itself stated correctly regardless). (technical lens)
- **N6** — `always_on[11]` cites P089, the one principle flagged `operational_mapping.profile_rule:
  false` in the spine; the profile only names the methods as a topic (no claim-strength violation),
  but the owner should confirm why a `profile_rule:false` principle is cited in a profile rule.
  (faithfulness)
- **N7** — P147 GILT/internationalization framing ("interlingua replaces the source") is a narrower,
  minority reading vs industry-standard internationalization; spot-check against the Munday passage
  if the skill is ever extended. (technical + quality lenses)
- **N8** — provenance-ledger Version History now 10 dense entries (1.0.0→1.9.0); a current-state
  "Grounding Summary" (without deleting history) would aid maintainability. (profile-reviewer)
- **N9** — role's "operating invariant" wording references the exported-adapter section name, not a
  field in `profile.yaml`; a reader of the portable profile alone may find "below" ungrounded.
  Harmless, sibling-consistent. (profile-reviewer)

---

## Lens must-fix tally

| Lens | must-fix |
|---|---|
| deterministic gates | 0 |
| agent-skills-advisor | 2 (M1, M2) |
| profile-reviewer | 0 |
| faithfulness-reviewer | 0 |
| ai-agent-engineering-reviewer | 0 |
| translation-equivalence-advisor | 0 |
| translation-quality-reviewer | 0 |
| technical-translation-advisor | 0 |

Deduped must-fix = **M1, M2** — both are the sibling-routing boundary missing from the
`translation-quality-and-applied-studies` skill; the ai-agent adapter-description finding (SF-1) is
the same defect at a second surface and is filed as should-fix to avoid double-counting. All three
domain lenses PASS with no must-fix — theorist attributions verified correct across the full 180-
principle corpus (Vinay & Darbelnet, Catford, Nida, Newmark, Reiss/Vermeer, Toury, House, Berman,
Venuti, Steiner, Quine, Gutt, Chaume, Pedersen). Prior r2 must-fix (MF-1/2/3) verified resolved in
v1.9.0.

MUST_FIX_COUNT: 2
