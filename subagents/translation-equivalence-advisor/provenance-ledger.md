# Provenance Ledger — translation-equivalence-advisor

Canonical record of what grounds this subagent. The profile, skills, references, faithfulness
report, and tests are all derived from the distilled spine in this package
(`principles/principles.yaml` → `analysis/claims.jsonl` → `evidence/evidence-records.yaml` →
`sources/anchors/*.anchors.jsonl`), which was assembled by the map→reduce build. No load-bearing
profile rule field is an orphan: every `quality_bar`, `forbidden_behaviours`, `handoff_rules`,
`knowledge_partition.always_on`, and `source_of_truth_policy` value cites the promoted principle(s)
it restates, or is marked as declared advisory-boundary policy in the faithfulness report — as with
`forbidden_behaviours[0]` (the "do not deliver the finished translation" boundary), which is a
declared scope, not a distillation claim, and so carries no inline citation. (Descriptive fields —
`role`, `when_to_use`, `inputs`, `outputs` — carry no inline tags, per repo convention.)

## Sources

| source_id | title | author | year | rights |
|-----------|-------|--------|------|--------|
| in-other-words-baker-8e6c3cb1 | In Other Words: A Coursebook on Translation | Mona Baker | 1992 | distillation-only |
| dynamic-formal-equiv-e6872198 | Toward a Science of Translating (secondary extract on dynamic and formal equivalence; a derived ~10k-word extract, not the primary monograph) | Eugene A. Nida | 1964 | distillation-only |

Both sources are **distillation-only**: paraphrase and restructure only, no verbatim quotation
(see `.claude/rules/rights-and-quotation-policy.md`; enforced by `quote_scan`).

## Distilled spine

- **116 promoted principles** (`principles/principles.yaml`, P001–P116; 5 high-confidence, 111
  medium).
- **415 atomic claims** (`analysis/claims.jsonl`, C-ids), each source-anchored.
- **Evidence records** (`evidence/evidence-records.yaml`, keyed by `claim_id`).
- **28 chunk anchors** across the two sources (`sources/anchors/*.anchors.jsonl`, `<sha12>-cNNNN`).

## Profile → principle mapping

The `knowledge_partition.skills` list partitions all 116 principles across nine skills, each
principle appearing in exactly one skill:

| skill | principles |
|-------|-----------|
| Word-Level Non-Equivalence and Strategies (`word-level-nonequivalence-and-strategies`) | P001, P011, P012, P037, P059, P060, P080, P081, P082, P095, P102, P103, P104, P105, P106 |
| Collocation, Idiom, and Fixed Expression (`collocation-idiom-and-fixed-expression`) | P013, P014, P040, P042, P043, P044, P058, P061, P063, P083, P107, P108, P109, P110 |
| Grammatical Equivalence (`grammatical-equivalence`) | P009, P015, P025, P026, P045, P046, P055, P057, P064, P084, P085 |
| Thematic and Information Structure (`thematic-and-information-structure`) | P002, P003, P016, P024, P027, P028, P029, P030, P047, P048, P065, P066, P067, P086, P088, P089, P090 |
| Cohesion and Texture (`cohesion-and-texture`) | P004, P017, P018, P031, P038, P049, P068, P069, P087, P091, P112 |
| Pragmatic Equivalence, Coherence, and Implicature (`pragmatic-equivalence-coherence-and-implicature`) | P007, P019, P020, P032, P033, P050, P070, P071, P072, P073, P092, P093, P113 |
| Dynamic and Formal Equivalence and Receptor Response (`dynamic-and-formal-equivalence`) | P008, P021, P022, P023, P034, P035, P036, P052, P053, P054, P056, P074, P094, P097, P098, P100, P115 |
| Register, Style, and Literary Form (`register-style-and-literary-form`) | P005, P041, P075, P076, P077, P099, P114, P116 |
| Text-Level Approach and the Limits of Equivalence (`text-level-approach-and-limits-of-equivalence`) | P006, P010, P039, P051, P062, P078, P079, P096, P101, P111 |

The five high-confidence principles (P009, P024, P037, P038, P058) are compiled into the adapter's
`## Operating invariants (must hold)` layer at export and each carries a behaviour test.

## Version history

- **v1.2.3** (2026-07-12) — review-loop r2 consolidated-panel fixes (no spine change; every edited rule
  still restates principles already in the spine, no new claim; supersedes the r3-flagged S3/S4 loci left
  unlogged at v1.2.2):
  - M1 (faithfulness): `knowledge_partition.always_on[0]` — the closing "never erase a culturally embedded
    item merely to sound natural" (unconditional, HEDGING_REMOVED against P095) reworded to "…when its
    foreignness carries meaning for the text (P095)"; citations unchanged.
  - M2 (faithfulness): `knowledge_partition.always_on[4]` — the absolute P038 opener contradicted its own
    P091 purpose-conditioned close; reframed default-with-exception ("As a default (P038)… but, as a
    purpose-driven exception (P091)…"); citations unchanged.
  - S1 (faithfulness): `quality_bar[7]` and `always_on[7]` restored P041's "unless the brief calls for
    preserving source-culture flavour" exception; `register-style-and-literary-form` step 2 + anti-pattern
    carry the same exception; citations unchanged (P041, P005, P076, P099).
  - S2 (faithfulness): `examples[1].ideal_response` dropped the "typically prioritizes the receptor's
    response" genre default it instructs the advisor not to assume; now "…without defaulting by genre
    (P034, P041, P021)".
  - S4 (mode coverage): the remaining seven skills' `## Output` gained a `compare`-mode branch — P106
    (word-level), P044 (collocation-idiom), P024 (thematic), P091 (cohesion), P050 (pragmatic), P005
    (register), P046 (grammatical) — each citing a principle already in that skill's partition.
  - S7 (routing): `when_to_use[1]` tightened so the exported router `description` surfaces the review-mode
    trigger; wording only, no citation.
  - S8 (routing): `text-level-approach-and-limits-of-equivalence` frontmatter `description` folds in the
    concrete caller phrasing ("right"/"literal enough"/"faithful"); wording only.
  - S3 (faithfulness-report): `always_on[0]`, `always_on[4]`, `quality_bar[7]`, `always_on[7]` notes
    re-graded from silently-clean to documented "Corrected in v1.2.3" entries.
  - S10 (test hygiene): `tests/test-results.md` regenerated and adapter re-exported against v1.2.3.
  - Deferred (out of grounding scope): S5 (P015 inclusive-language / singular-they options) and S6 (P100
    regulated-domain back-translation QA role) require claims absent from the two grounded sources; S9
    (missing v1.2.2 review-loop artifact) and NICE items are non-blocking.

- **v1.2.2** (2026-07-12) — review-loop r1 independent re-verify fixes (no spine change; every edited
  rule still restates principles already in the spine, no new claim):
  - SF-1 (routing): seven skill `description` openers broadened from "Reviews …" to "Diagnoses and
    reviews …" so the sole load-time trigger covers the pre-draft advise/diagnose path the bodies already
    build (mirrors the `word-level` skill; scope statement, no principle grounding).
  - SF-2 (mode coverage): `dynamic-and-formal-equivalence` and `text-level-approach-and-limits-of-equivalence`
    `## Output` gained a `compare`-mode branch (side-by-side favours/costs before a purpose-weighted
    recommendation) — P021 for the orientation compare, P079 for the whole-text compare.
  - SF-3 (faithfulness): `profile.yaml` `quality_bar[0]` headline "No one-to-one match at word level" →
    "Don't assume a one-to-one match at word level" to restore P037's hedge ("never *assume* a
    one-to-one correspondence"); citations unchanged (P037, P001, P103, P106).
  - SF-5 (grammatical, grounded subset): `grammatical-equivalence` step 3 adds that "masculine as
    unmarked" describes the source system, not a target default, and to restructure (e.g. passive) where
    the distinction is arbitrary or need not be specified — the grounded part of P015 only (no
    inclusive-language *policy* claim, which stays deferred as out of spine scope).
  - SF-6 (faithfulness): `profile.yaml` `examples[1].ideal_response` de-genre-defaulted — "a marketing
    text usually calls for dynamic equivalence" → "a marketing brief typically prioritizes the receptor's
    response, so ask what this brief's purpose and audience favour before setting the orientation"
    (P034, P041, P021), consistent with the brief-governs precedence and `forbidden_behaviours[2]`. Root
    cause `.build/authoring/gen.py` fixed so regeneration will not reintroduce it.
  - SF-8 (dynamic-formal, grounded subset): anti-pattern added that a fluent receptor read is not proof
    of equivalent effect and "similar audience response" is a directional target tested across audience
    and context, not a single pass/fail — grounded in P035 (multiple valid solutions) and P036
    (naturalness that preserves meaning). Does not assert the ungrounded unmeasurability critique, which
    stays deferred.
  - SF-9 (grammatical): step 6 relabelled from "Distinguish morphology from syntax" to P084's load-bearing
    contrast — grammar (morphology and syntax together, a closed, largely obligatory system) vs lexis (an
    open, largely optional system); citation unchanged (P084).
  - SF-10 (test hygiene): `golden-tests.yaml` `profile_version` → 1.2.2 (metadata only; GT-004 content
    unaffected).
  - SF-12 (ledger): the per-field citation claim above qualified to note `forbidden_behaviours[0]` is a
    declared advisory-boundary policy carrying no inline citation by design.
  - SF-13 (faithfulness-report): `quality_bar[0]` note extended to record the SF-3 hedge restoration.
  - MF-2 / Phase 8: `tests/test-results.md` regenerated against the v1.2.2 profile.
  - Deferred again (out of grounding scope): SF-4/prior-SF-9 back-translation QA role and SF-7/prior-SF-10
    Nida-1986 "functional equivalence" rename — both require claims absent from this spine; SF-11 adapter
    description-synthesis is a shared factory-template concern, not a package-grounding fix.

- **v1.2.1** (2026-07-12) — adversarial-verify (verify1) fixes (no spine change; every edited rule still
  restates principles already in the spine, no new claim):
  - MF-1 (faithfulness): `skills/grammatical-equivalence/SKILL.md` step 7 conflated a term-TYPE with a
    STRATEGY — classified terms as "ordinary parallels, functional equivalents, or borrowings", swapping
    P055's diagnostic third category "culture-specific items" for the strategy "borrowings" and dropping
    "cultural" from the second. Restated to P055's exact sense (ordinary parallels / functional cultural
    analogues / culture-specific items) with strategy choice deferred to the word-level skill, restoring
    the no-map-type-to-strategy discipline.
  - MF-2 (faithfulness): `profile.yaml` `quality_bar[0]` broadened word-scoped P037/P001 to "word or
    phrase level" (SCOPE_BROADENED — phrase/collocation is governed by P042/P043 typicality). Narrowed to
    "word level"; phrase/collocation/idiom coverage remains in `quality_bar[1]`.

- **v1.2.0** (2026-07-12) — review-loop r2 fixes (supersession, no spine change; every edited rule still
  restates principles already in the spine, no new claim):
  - MF-1 (faithfulness): the receptor-response over-claim fixed in `quality_bar[6]` at v1.1.0 was still
    live verbatim in four non-profile artifacts — the `dynamic-and-formal-equivalence` skill Purpose and
    anti-pattern, the key-concepts Adequacy entry, and golden test GT-004. All propagated to the
    brief-conditioned wording (P021, P034, P035, P022 — P022 grounds closeness-to-source-form for readers
    who need that access). `.build/authoring/gen.py` corrected so regeneration will not reintroduce it.
    Faithfulness-report `quality_bar[6]` note extended to record the propagated loci.
  - MF-2 (faithfulness): `quality_bar[1]` reversed P044's hedge ("assume no idiom has a target
    equivalent" = presume none) → restored to P044's agnostic "do not assume an idiom has a target
    equivalent", matching `always_on[1]` and unblocking P014's similar-meaning-and-form idiom strategy.
    Faithfulness-report `quality_bar[1]` note corrected (was inaccurately "no strengthening").
  - SF-1 (routing): `when_to_use` reordered so the most distinctive triggers (culture-specific
    item/idiom/collocation/marked-structure/poetic-form; whole-text review) fill the first two slots the
    router `description` samples (no principle grounding — scope statement).
  - SF-2 (scope): `review` mode output now states "correction" = strategy/target-language device, not
    verbatim replacement prose (consistent with `forbidden_behaviours[0]`; no new citation).
  - SF-3 (advise-mode fit): eight skill `## Output` sections gained a no-draft branch (state the
    recommended strategy and its principle directly when no draft is supplied). No grounding change.
  - SF-5 (provenance): Nida citation corrected — fabricated subtitle dropped; recorded as a derived
    secondary extract, not the primary monograph (Sources table above updated).
  - SF-6 (size): `quality_bar` clauses trimmed to hold the body under the 1000-word limit; all principle
    citations preserved.
  - SF-7/SF-8 (test hygiene): `golden-tests.yaml` `profile_version` → 1.2.0; GT-004 `principle_coverage`
    gains P022; Phase-8 `test-results.md` regenerated against the v1.2.0 profile.
  - Deferred (out of grounding scope — would need claims absent from this spine): SF-9 back-translation
    QA/validation role, SF-10 Nida-1986 "functional equivalence" rename, SF-11 Mandarin 被 era-drift,
    SF-12 contrastive-rhetoric critique, SF-13 equivalent-effect unmeasurability, SF-14 inclusive-language
    policy, and the N-tier nice-to-haves that import outside sources.
- **v1.1.0** (2026-07-12) — review-loop r1 fixes (supersession, no spine change; every edited rule still
  restates principles already in the spine, no new claim):
  - M2 (faithfulness): `quality_bar[6]` over-claim removed — the universal negation "adequacy is judged
    by receptor response, **not** formal closeness" exceeded its cites (P022 endorses formal-equivalence/gloss
    for close source access; P035 gives four adequacy criteria). Reworded brief-conditioned; grounding
    unchanged (P021, P034, P035, P022). Faithfulness-report `quality_bar[6]` note updated.
  - S9 (faithfulness): `source_of_truth_policy.precedence` regraded "preserve it only where…" →
    "preserving it more strongly where…" to match P005's graded wording (grounding P005, P021, P078,
    P051 unchanged). Faithfulness-report `precedence` note updated.
  - S1 (routing): `when_to_use[0]` split into two sentences so the exported router `description` gets a
    complete, scope-signalling first clause (no principle grounding — scope statement).
  - S2 (size): `quality_bar` compressed for body-word headroom; all principle citations preserved.
  - S8 (lens-fit): `text-level-approach-and-limits-of-equivalence` "When to use" narrowed to its distinct
    whole-text/relative-standard trigger (P006, P051, P078; no new citation).
  - M1 (adapter): re-exported so P038/P058 invariants emit whole (stale adapter had a mid-clause `…`).
  - Deferred (out of grounding scope — would need claims absent from this spine): S3 back-translation
    QA role, S5 equivalent-effect unverifiability, S6 Mandarin 被 era-drift, S7 Nida-1986 "functional
    equivalence" rename, and the N-tier nice-to-haves.
- **v1.0.0** (2026-07-11) — initial LLM-authored layer (profile, nine skills, two references,
  faithfulness report, golden + principle-behaviour tests, adapter) generated over the pre-built
  distilled spine. Distilled spine unchanged.
