# Review Loop — translation-equivalence-advisor — Round 4

Consolidated review across 4 factory lenses + 3 domain-expert cross-checks. Deterministic
gates run first; their FAILs are must-fix. LLM findings deduped across lenses, most-severe first.

## Deterministic gates (STEP 1)

| Gate | Result |
|------|--------|
| `validate_generated_package` | **PASS** (0 FAIL; 1 non-blocking phase8 self-check WARNING) |
| `quote_scan` | **PASS** — no verbatim quotation |
| ellipsis-truncation grep | clean (no hits) |
| severed-invariant grep | clean (no hits) |

No deterministic FAILs → 0 deterministic must-fix.

## Reviewer must-fix tallies

| Lens | MUST_FIX |
|------|----------|
| agent-skills-advisor | 0 |
| profile-reviewer | 0 |
| faithfulness-reviewer | 0 |
| ai-agent-engineering-reviewer | 1 |
| descriptive-translation-reviewer | 0 |
| translation-quality-reviewer | 0 |
| technical-translation-advisor | 0 |

---

## MUST-FIX

### MF1 — adapter frontmatter description drops review-mode trigger + sibling-redirect clause
- **where:** `.claude/agents/generated/translation-equivalence-advisor.md` frontmatter `description` (line 3), compiled from `when_to_use` / `when_not_to_use` in `profile.yaml`
- **severity:** must-fix
- **problem:** The frontmatter description — the only pre-dispatch signal an orchestrator sees before loading the body — keeps only bullet #1 of each list. It drops (a) the `review`-mode trigger ("a draft translation or rendering decision needs review"), likely the modal real-world request ("review my translation"), and (b) the single most load-bearing disambiguation: the sibling-redirect routing generic review asks to `descriptive-translation-reviewer` (norms/retranslation), `translation-quality-reviewer` (corpus metrics/register profile), and `technical-translation-advisor` (terminology/usability). With 4 near-identical "translation review" siblings, losing that clause from the pre-dispatch signal is a real misrouting risk — same class as the adapter-truncation bug that previously gutted must-hold rules in a sibling package.
- **fix:** Fix the description compiler so it does not always take only bullet #1 of each list; fold the sibling-redirect clause and the review trigger into the frontmatter description. Prefer a general compiler fix over a one-off hand-edit (check whether description-compilation truncates other packages too). Re-export the adapter + version bump + changelog entry after.

---

## SHOULD-FIX

### SF1 — back-translation framing too narrow (regulated-domain QA role omitted)  *[domain, 2 reviewers]*
- **where:** `principles/principles.yaml` P100; `skills/dynamic-and-formal-equivalence/SKILL.md` step 7; `skills/text-level-approach-and-limits-of-equivalence/SKILL.md`
- **problem:** P100 ("back-translation only to expose structure... theoretically unsound... never reproduces meaning") faithfully reflects Baker's pedagogical illustration but as a general rule undersells back-translation's recognized bounded role as a QA/compliance check in regulated medical/legal/technical translation (ISPOR/COA, pharma, survey-instrument localization). Sibling `technical-translation-advisor` frames it correctly as "a limited quality check."
- **fix:** Scope P100 explicitly to its pedagogical origin, or add a caveat that some regulated domains still require back-translation as one QA check among several (not a sole test).

### SF2 — P094 concordance relaxation over-generalized for technical register  *[domain]*
- **where:** `principles/principles.yaml` P094; `skills/dynamic-and-formal-equivalence/SKILL.md` step 6
- **problem:** P094 generalizes Nida's narrow literary "concordance" point into an unqualified step. As written it could license relaxing terminology consistency for naturalness — which contradicts near-universal technical/scientific practice (terminology consistency near-mandatory in manuals/patents/standards; sibling states this as mandated-terminology).
- **fix:** Narrow to the literary/rhetorical concordance sense; add caveat that for technical/scientific terminology the default reverses (relax only for stylistic concordance, never domain terminology) and route terminology decisions to `technical-translation-advisor`.

### SF3 — "dynamic equivalence" terminology-currency note missing  *[domain, 2 reviewers]*
- **where:** `skills/dynamic-and-formal-equivalence/SKILL.md`; `references/translation-equivalence-key-concepts.md`
- **problem:** "Dynamic equivalence" used throughout as stable current terminology, but Nida himself later reframed it as "functional equivalence" (Nida & de Waard 1986; Nida 1993) precisely to correct the misread as license for free paraphrase. No signal the term evolved.
- **fix:** Add a one-line note that "dynamic equivalence" is Nida's original (1964) term, later reframed by Nida as "functional equivalence." No operational-rule change.

### SF4 — "adequacy" collides with Toury's technical sense across siblings  *[domain]*
- **where:** `principles/principles.yaml` P035; `references/translation-equivalence-key-concepts.md` "Adequacy" entry
- **problem:** Package uses "adequacy" in Nida's everyday fitness-for-brief sense. In descriptive TS (the `descriptive-translation-reviewer` sibling's framework) "adequate" is Toury's technical *source-oriented* term, antonym of "acceptable." The profile's own handoff rules invite movement between siblings → a reader could import the opposite technical sense, inverting meaning.
- **fix:** Add a disambiguating clause to the glossary entry distinguishing Nida's sense from Toury's adequate/acceptable dichotomy.

### SF5 — repeated advise/review/compare Output boilerplate (9× duplication)  *[skill-authoring]*
- **where:** all 9 `skills/*/SKILL.md` `Output` sections
- **problem:** Near-verbatim 2–3 sentence advise/review/compare scaffold repeated in every skill body with only a noun swapped — non-differentiating token weight against the "every line earns its cost" bar.
- **fix:** Move the shared response-shape protocol into `references/translation-equivalence-key-concepts.md` once; each skill's `Output` states only its domain-specific finding fields + a pointer.

### SF6 — inconsistent caller-trigger concreteness across 9 descriptions  *[skill-authoring]*
- **where:** 8 of 9 skill descriptions (only `text-level-approach-and-limits-of-equivalence` gives a quoted caller trigger)
- **problem:** 8 descriptions rely on technical-vocabulary enumeration with no example of the words a caller would actually use → ambiguous auto-selection on borderline requests among 9 adjacent lenses.
- **fix:** Add a short "Use when a caller says/asks…" clause to the other 8; prioritize confusable pairs (thematic-and-information-structure vs cohesion-and-texture; pragmatic-equivalence vs cohesion-and-texture).

### SF7 — thematic vs cohesion reference-tracking overlap  *[skill-authoring]*
- **where:** `skills/thematic-and-information-structure/SKILL.md` step 5 vs `skills/cohesion-and-texture/SKILL.md` step 5
- **problem:** Both claim "tracing participants through reference" in near-identical language despite frontmatter boundary; a "track a participant across a passage" query could fire either.
- **fix:** Add a clause to thematic-and-information-structure noting reference-tracking mechanics belong to cohesion-and-texture; this skill only reads given/new status of a referenced participant.

### SF8 — no worked example demonstrates review or compare mode  *[agent-design, profile]*
- **where:** `profile.yaml` `examples:` (mirrored in adapter)
- **problem:** 3 modes declared (advise/review/compare) but both examples are advise-flavored (one advise, one decline-and-offer-review). The package's key differentiator — the review findings-list output keyed to equivalence level, and the compare side-by-side — is never exemplified.
- **fix:** Swap one example for an actual `review` execution (short draft, 2–3 findings across equivalence levels) or a `compare` execution (formal-vs-dynamic for one segment).

### SF9 — CHANGELOG.md entries per version bump not evidenced  *[profile]*
- **where:** `provenance-ledger.md` version history (v1.0.0→v1.2.4, 7 bumps)
- **problem:** `generated-artifact-policy.md` rule 5 requires a CHANGELOG.md entry per bump; ledger never references CHANGELOG.md.
- **fix:** Confirm CHANGELOG.md has one entry per bump v1.0.0–v1.2.4; backfill from the ledger's per-version bullets (already changelog-shaped) if absent.

### SF10 — profile body ~26 words under the 1000-word hard-fail limit  *[profile]*
- **where:** `provenance-ledger.md` line 70; `profile.yaml` body
- **problem:** v1.2.4 self-reports ~26 words of headroom under the hard-fail; the very next faithfulness/routing fix risks tripping FAIL. Any MF1/SFn edit that touches the body must reclaim headroom.
- **fix:** When applying fixes, restructure one of the heaviest quality_bar/always_on clauses to buy back headroom; re-run body-size validator before export.

---

## NICE

- **N1 — dated-source caveats:** P015 "masculine as unmarked term" stated as flat cross-linguistic default (flag as source-era descriptive, check house style — raised by 3 domain reviewers); P066 topic "always-definite" → soften to "typically definite or generic" (Li & Thompson); P009 Chinese 被-passive adversity weakened in modern neutral register + scientific-English passive norm shifting active (Nature/AMA/ACS). All are hedge-tightening, not errors.
- **N2 — inline citations under-represent aggregate grounding:** quality_bar[2]/[3]/[7] cite one principle ID inline though the faithfulness report notes 3–4 aggregated; optionally widen inline citations for profile-only traceability.
- **N3 — Baker pinned to 1st ed. (1992):** 3rd ed. (2018) revised collocation/pragmatics chapters; optional future fold-in note, source transparently declared + sha-pinned.
- **N4 — provenance-ledger readability:** add a top-of-history "current state" summary; dense em-dash descriptions could split for scanning; uneven anti-pattern bullet counts (3 vs 4). Polish only.

---

MUST_FIX_COUNT: 1
