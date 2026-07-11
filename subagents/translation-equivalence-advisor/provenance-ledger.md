# Provenance Ledger — translation-equivalence-advisor

Canonical record of what grounds this subagent. The profile, skills, references, faithfulness
report, and tests are all derived from the distilled spine in this package
(`principles/principles.yaml` → `analysis/claims.jsonl` → `evidence/evidence-records.yaml` →
`sources/anchors/*.anchors.jsonl`), which was assembled by the map→reduce build. No load-bearing
profile rule field is an orphan: every `quality_bar`, `forbidden_behaviours`, `handoff_rules`,
`knowledge_partition.always_on`, and `source_of_truth_policy` value cites the promoted principle(s)
it restates. (Descriptive fields — `role`, `when_to_use`, `inputs`, `outputs` — carry no inline
tags, per repo convention.)

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
