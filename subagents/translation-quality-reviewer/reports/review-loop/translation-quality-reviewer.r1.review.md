# translation-quality-reviewer — Review r1 (consolidated)

Scope: one review pass over `subagents/translation-quality-reviewer/`. Deterministic gates +
7 reviewer lenses (agent-skills, profile, faithfulness, agent-design, and 3 domain cross-checks:
translation-equivalence, descriptive-translation, technical-translation). Findings deduped across
lenses, most-severe first. REVIEW ONLY — nothing fixed.

## Deterministic gates (STEP 1)

- `validate_generated_package`: **1 FAIL** — `tier-artifact: principles/principles.yaml: adapter
  invariant layer truncates rule content` (trailing `…` on compiled invariants P001, P002, P012,
  P018, P020, P029, P055–P058, P121, P122). → folded into MUST-FIX 1.
- `quote_scan`: PASS (no verbatim quotation).
- ellipsis grep: hits confirm the adapter invariant truncation above (skill bodies clean of `…`).
- paren-sever grep: no hits.

---

## MUST-FIX

### 1. Stale adapter export truncates operating invariants (deterministic FAIL + profile lens)
- **Where:** `adapters/claude-code/translation-quality-reviewer.md` + installed copy
  `.claude/agents/generated/translation-quality-reviewer.md`, `## Operating invariants (must hold)`
  (lines ~26–62). Both stamped Generated 2026-07-11, generator 0.1.0 — exported *before*
  `compile_invariants.py` was fixed, never re-exported.
- **Problem:** Two truncation signatures in the must-hold section:
  (a) trailing-`…` cut (the deterministic FAIL) on P001/P002/P012/P018/P020/P029/P055–P058/P121/P122;
  (b) a **colon-boundary cut with no `…` and no unbalanced paren** on P003, P019, P035, P053, P054,
  P083, P084 — invisible to `validate_invariant_coverage`'s detector, so it reads as passing.
  e.g. P003 → "Choose the corpus type by the question" (drops the entire parallel-vs-comparable rule);
  P035 → "Preserve the strength of the evidence" (drops the never-upgrade-a-hedged-claim rule);
  P083/P084 lose their operative definitions. 7 of 19 non-negotiable rules gutted silently in the
  live installed adapter. Same bug class already fixed in sibling packages
  (technical-translation-advisor, translation-equivalence-advisor).
- **Fix:** Re-export the adapter with current `compile_invariants.py`; diff the regenerated
  `## Operating invariants` to confirm P003/P019/P035/P053/P054/P083/P084 render the full first
  sentence and no other invariant regresses; re-copy to `.claude/agents/generated/`; bump
  `agent_version`; add CHANGELOG entry. Do not mark `status: ready` until the diff confirms the fix.

### 2. All 12 SKILL.md omit the `description` frontmatter field (agent-skills lens)
- **Where:** every `skills/*/SKILL.md` frontmatter (verified: `corpus-design-and-methodology`
  and all 11 others carry only `name/kind/status/provenance`, no `description:`).
- **Problem:** `description` is the primary signal a surface/orchestrator uses to route to a skill
  without opening it; a valid SKILL.md requires name **and** description. Confirmed regression vs.
  this factory's own better pattern — sibling `translation-equivalence-advisor` writes rich,
  scope-bounded descriptions in every skill (e.g. `cohesion-and-texture`: "…owns the surface ties
  …, not the reader's coherence judgement, which pragmatic-equivalence-… owns. Use when…").
- **Fix:** Add a `description:` to each of the 12 files, front-loading the primary trigger + trigger
  words, and naming the neighbouring skill it defers to (mirrors the sibling boundary convention;
  also resolves should-fix S5).

### 3. Anti-pattern bullets truncated mid-clause across all 12 skills (agent-skills lens)
- **Where:** the "Anti-patterns to flag" list in every `skills/*/SKILL.md`. Verified examples:
  `corpus-design-and-methodology/SKILL.md:90` "…searched, counted, displayed, and (P077)." (cut
  before the verb); `genre-childrens-literature-and-accessibility/SKILL.md:84` "…conversational
  rituals, reassurance, and gentle socialization as core Tenor and (P044)." (dangling "and");
  `cultural-filtering-ideology-and-globalization/SKILL.md:91` "…indexical orders, and
  language-cultural (P045)."
- **Problem:** Hard character/length cutoff before the clause completes, ending in the `(Pxxx)`
  citation — so the `…` truncation gate misses it. The fast-scan checklist section is left
  uninterpretable (reader cannot tell what the flagged failure is). Distinct from MUST-FIX 1
  (adapter invariants) — this is the skill bodies.
- **Fix:** Regenerate each anti-pattern bullet from the complete imperative clause, not a
  fixed-length prefix, so every bullet is a grammatical, complete sentence.

### 4. P003 mis-defines "comparable corpus" — omits the monolingual sense the package depends on (equivalence + descriptive + technical lenses; 3-way convergence)
- **Where:** `principles/principles.yaml` P003 (lines 65–89); surfaced in
  `skills/corpus-design-and-methodology/SKILL.md` step 1; echoed by P068. Verified text: "use
  comparable corpora (comparable original texts across several languages) …".
- **Problem:** P003 defines "comparable corpus" only in the *multilingual/contrastive* sense
  (matched non-translated originals across languages) and mis-assigns it to equivalence testing.
  It omits the standard corpus-TS sense — a **monolingual** corpus of translated vs. non-translated
  texts in the *same* target language — which is the canonical tool for translation-universals /
  third-code detection and is exactly what the package's own P050/P078/P121/P135 and the
  `translation-universals-and-the-third-code` skill rely on. As *the* corpus-type definition
  (procedure step 1, referenced by several `applies_when`), P003 would misdirect a corpus-design
  review to the wrong design for a universals/explicitation study. Contradicts P121 internally.
- **Fix:** Rewrite P003 to state both constructs by name: (a) parallel corpus (ST+TT aligned) for
  shifts/equivalence/alignment; (b) monolingual comparable corpus (translated vs. non-translated,
  same target language, matched domain/register/period) for universals/translationese;
  (c) multilingual comparable corpus (matched originals across languages) for contrastive study.
  Cross-reference P121/P050/P135; revisit P068 for the same conflation.

### 5. Participation placement contradicts itself (Mode vs. Tenor) with no version label (descriptive lens)
- **Where:** `principles/principles.yaml` P042/P013/P040 vs. P075 — P042 and P075 are procedure
  steps 5 and 13 of the **same** `skills/register-field-tenor-mode-analysis/SKILL.md`. Verified:
  line 856 bundles "participation" under Mode/channel; line 1406 (P075) places Participation under
  Tenor as "the revised model".
- **Problem:** House's *Past and Present* revision moves Participation from Mode to Tenor; P042
  (Mode) is the superseded stage, P075 (Tenor) is current — but both sit unlabeled and co-equal in
  one skill. The agent has no signal which is authoritative and could flag a translator for moving
  participation into Tenor in one session and require it in the next.
- **Fix:** Either move "participation" to the Tenor bullet in P042/P013/P040 (where they describe
  current analysis), or explicitly label P042/P013/P040 as House's earlier model with a note that
  P075 supersedes them on this point.

### 6. P139 defines translationese as an incompetence artefact — contradicts P002/P147 (descriptive lens)
- **Where:** `principles/principles.yaml` P139 (lines 2382–2398). Verified: "translationese is an
  artefact of a translator's inexperience or lack of competence in the target language."
- **Problem:** Non-standard, disputable gloss. Since Gellerstam (1986), translationese denotes the
  corpus-detectable fingerprint distinguishing translated from non-translated target text —
  documented even in skilled professional translation (shining-through, universal tendencies,
  target-norm effects), not by definition an incompetence marker. Internally contradicts P002
  (translationese indicators are not an automatic quality proxy) and P147 (Russian translationese
  studies as legitimate corpus inquiry). Followed literally, the reviewer would wrongly equate any
  detected translationese with incompetence.
- **Fix:** Redefine translationese in P139 as the corpus-observable profile distinguishing
  translated from non-translated target text regardless of skill level; treat "caused by
  incompetence" as one testable hypothesis among several (source interference, target-norm
  conformity, the third code), decided empirically case by case, not by definition.

---

## SHOULD-FIX

- **S1. Anti-patterns silently capped at ~7 bullets regardless of principle count** (agent-skills).
  e.g. `overt-covert-translation-and-equivalence` has 19 procedure steps but 7 anti-patterns;
  later principles get no matching anti-pattern and read as less load-bearing. Extend to one bullet
  per principle, or explicitly curate a "highest-signal" subset and say so.
- **S2. Dense skills are flat, unordered principle-ID lists with no routing** (agent-skills).
  overt-covert (19), error-analysis (17), cultural-filtering (16), corpus-design (15). Add a top
  triage step or group steps by sub-case (e.g. overt / covert / classifying-which).
- **S3. Profile body ≈941 words — over the 800w Phase 8 WARN line** (profile; this IS the
  "phase8 WARNING"; 17/18 checks pass, only check 14 warns). Trim heaviest sections `quality_bar`
  (~175w) and `role` (~125w). Under the 1000w FAIL line, so not a blocker.
- **S4. No `reports/quote-scan*` artifact recorded** (profile). All 5 sources are
  `distillation-only`; the live scan passes but no report is persisted. Record the scan output
  before release.
- **S5. Adapter/frontmatter description carries only 1 of 5 triggers** (profile + agent-design).
  Routing misses corpus-method, translationese-as-proxy, and Russian/Chinese-specific requests.
  Re-generate the description with 2–3 triggers per the Phase 9 rule (refreshes on MUST-FIX 1 re-export).
- **S6. `when_to_use` (5 clusters) under-covers the 11-skill surface** (agent-design). No explicit
  trigger for error-analysis/evaluation-discipline, cognition/pragmatics, or
  genre/children's-literature/accessibility. Add 1–2 bullets or broaden existing wording.
- **S7. `source_of_truth_policy.precedence` SCOPE_BROADENED** (faithfulness). "treat a principle as
  an adaptable guide, not an absolute" cites P032/P047/P115, all narrow (cultural-filter reassessment
  / universal-tendency scoping) — generalized into a profile-wide precedence rule. Narrow the
  sentence to the domains those principles cover, or re-cite to a genuinely profile-wide principle.
- **S8. `knowledge_partition.always_on` register bullet SCOPE_BROADENED** (faithfulness).
  "persuasive and missionizing texts" cites P010/P070–P075, all specifically about *mission
  statements*. Replace with "mission statements and comparably exhortative institutional texts".
- **S9. `handoff_rules[1]` cites unrelated anchors** (faithfulness). The handoff to owning
  specialists cites P052/P077, neither of which discusses division of labour. Re-cite or mark as
  profile-level engineering judgement.
- **S10. P083 overstates norms as textual-evidence-*only*** (descriptive domain). Omits Toury's
  caveated extratextual source (translators'/editors'/critics' normative statements). Add a
  "corroborating-but-not-substituting" clause.
- **S11. No S-universal / T-universal split** (descriptive domain). P121's comparable-corpus method
  is presented as *the* universal-isolation method but only tests T-universals; explicitation-type
  S-universals need parallel (ST-TT) corpora. Add the Chesterman S/T distinction and route by it.
- **S12. C00167 tenet not promoted** (technical domain). "Functional equivalence is achievable only
  for covert translation" sits only as evidence under P008 (narrowly about titles/ads/signs); no
  principle explicitly flags a "functional equivalence" claim about an *overt* translation as a
  category error. Add/fold an explicit principle.

---

## NICE

- N1. `quality_bar[0]` cites P084 (universals-vs-norms) for a third-code-vs-translationese claim —
  spurious anchor; drop P084 (faithfulness).
- N2. `quality_bar[2]` cites P090 ("overt *error*") for House's overt/covert *translation-type*
  distinction — conflates two senses of "overt"; drop P090 (faithfulness).
- N3. `examples[1]` "a contract is typically an overt case" — no principle grounds contracts
  specifically; soften to "plausible candidate" (faithfulness).
- N4. `when_to_use[4]` bundles Russian-corpus + Chinese-Europeanization into one bullet (profile).
- N5. Generic "Inputs"/"Output" boilerplate copy-pasted verbatim across all 12 skills — could live
  once in a reference (agent-skills).
- N6. H1/name apostrophe mismatch in `genre-childrens-literature-and-accessibility` H1 heading
  (agent-skills).
- N7. P051 named Russian corpora (UN Web TV, SIREN, COINCOUT) will age past the 2023 source — add a
  currency caveat (descriptive domain).
- N8. P030 uses Koller's equivalence typology surveyed by House without labelling it as a separate
  lens from House's own dimensions — note it to avoid blending (technical domain).
- N9. Error-analysis grounded only in House's academic typology; no acknowledgement of industry
  frameworks (MQM/LISA QA) — note scope in role (technical domain).

---

## Process note (not a ranked finding)

`reports/faithfulness-report.yaml` covers only `quality_bar`, `forbidden_behaviours`, `when_to_use`,
`outputs.primary_format`, and `precedence` — it has **no** entries for `knowledge_partition.always_on`
(the 12 skill-scope paragraphs, the bulk of behavioural content), `handoff_rules`, `outputs.modes`,
or `examples`. Regenerate/extend it to cover those fields before treating the package as
faithfulness-reviewed at Tier 2 completeness. (S7–S9, N1–N3 were found in those uncovered fields.)

MUST_FIX_COUNT: 6
