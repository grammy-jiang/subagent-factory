# Review Loop — translation-equivalence-advisor (r2)

Consolidated review pass. Seven reviewer lenses (agent-skills, profile, faithfulness,
ai-agent-engineering) + three domain lenses (descriptive-translation, translation-quality,
technical-translation) plus deterministic gates.

## Deterministic gates

| Gate | Result |
|------|--------|
| `validate_generated_package` | PASS (0 FAIL; Phase-8 self-check WARNING only) |
| `quote_scan` | PASS (no verbatim quotation) |
| truncation grep (`…` / severed invariant) | clean |

Deterministic FAILs: **0**.

---

## MUST-FIX

### M1 — `always_on[0]` hardens conditional P095 into an unconditional prohibition
- **where**: `profile.yaml:109-115` (`knowledge_partition.always_on[0]`)
- **severity**: must-fix (faithfulness HEDGING_REMOVED; Phase-8 check 17)
- **problem**: Clause ends "…never erase a culturally embedded item merely to sound natural
  (…P095…)" — unconditional. P095 is conditional: retain/describe/annotate *when the
  foreignness carries meaning*. The package's own `word-level-nonequivalence-and-strategies/
  SKILL.md:101` and `profile.yaml examples[0].ideal_response` already carry the correct
  conditional wording, so this field is internally inconsistent. Flagged as S3 in
  `r3.review.md:37-40`, never fixed nor logged deferred in the v1.2.2 CHANGELOG.
  `faithfulness-report.yaml:134-141` still grades it WITHIN_SCOPE / no distortion.
- **fix**: Reword to "…never erase a culturally embedded item merely to sound natural when its
  foreignness carries meaning for the text (P095)"; update the faithfulness-report finding.

### M2 — `always_on[4]` is internally contradictory (absolute P038 vs. purpose-conditioned P091)
- **where**: `profile.yaml:132-136` (`knowledge_partition.always_on[4]`)
- **severity**: must-fix (faithfulness internal contradiction; Phase-8 check 17)
- **problem**: Opens "Do not transfer the source text's cohesive devices…" (absolute, P038) then
  in the same sentence "…decide whether to follow source cohesion or approximate target norms by
  the translation's purpose (…P091…)" — a purpose-conditioned exception that contradicts the
  absolute opener. Flagged as S4 in `r3.review.md:42-45`; not fixed nor logged deferred.
  `faithfulness-report.yaml:166-173` still grades it WITHIN_SCOPE / no distortion.
- **fix**: Reframe as default-with-exception, e.g. "As a default, rework rather than transfer
  source cohesive devices to the target's own preferences/frequencies, but decide whether to
  follow source cohesion or approximate target norms by the translation's purpose (P038 as
  default; P091 as the purpose-driven exception)"; update the faithfulness-report finding.

---

## SHOULD-FIX

### S1 — `quality_bar[7]` / `always_on[7]` drop P041's foreignization exception (register)
- **where**: `profile.yaml:75-76` (`quality_bar[7]`) and `profile.yaml:150-154`
  (`always_on[7]`); mis-assessed at `faithfulness-report.yaml:75-82` and `:190-197` (both
  WITHIN_SCOPE / distortion:none).
- **problem**: Both restate P041 as unconditional register-matching. P041
  (`principles.yaml:846-850`) is conditional: "…**unless the purpose is deliberately to give the
  reader a flavour of the source culture**." Same HEDGING_REMOVED shape already corrected for
  P021/P034/P035/P022 in `quality_bar[6]`. An advisor following it literally would flag a
  deliberate foreignizing rendering as a register error. Same drop propagated to
  `register-style-and-literary-form/SKILL.md:66,85` and `.build/authoring/gen.py:621/644`.
- **fix**: Append "…unless the brief calls for preserving source-culture flavour (P041)" to both
  clauses; re-grade the two faithfulness-report findings to HEDGING_REMOVED with an active fix.
  (Borderline must-fix — same class as M1/M2; kept should-fix because the faithfulness lens graded
  it so.)

### S2 — `examples[1].ideal_response` still asserts a genre default it tells the advisor not to assume
- **where**: `profile.yaml:198-200`
- **problem**: v1.2.2 SF-6 fix left "…a marketing brief typically prioritizes the receptor's
  response, so ask what this brief's purpose and audience favour…" — asserts a genre default
  ("typically prioritizes") while instructing the advisor to ask rather than assume. Partially
  undoes its own fix.
- **fix**: Drop the genre-default clause: "…ask what this brief's purpose and audience favour
  before setting the orientation, without defaulting by genre (P034, P041, P021)."

### S3 — Faithfulness-report stale on M1/M2 loci
- **where**: `reports/faithfulness-report.yaml:134-141,166-173` (and :75-82,:190-197 per S1)
- **problem**: `always_on[0]`, `always_on[4]` (and the S1 register loci) graded clean despite the
  distortions above; should be re-graded to accept_with_note / HEDGING_REMOVED once fixed, not
  left silently marked clean.
- **fix**: Re-grade after M1/M2/S1 fixes land.

### S4 — Compare-mode output shape absent from 7 of 9 skills
- **where**: `word-level-nonequivalence-and-strategies/SKILL.md:110-112`,
  `collocation-idiom-and-fixed-expression/SKILL.md:105-107`,
  `thematic-and-information-structure/SKILL.md:135-137`, `cohesion-and-texture/SKILL.md:101-103`,
  `pragmatic-equivalence-coherence-and-implicature/SKILL.md:109-111`,
  `register-style-and-literary-form/SKILL.md:78-80`, `grammatical-equivalence/SKILL.md:102-104`
- **problem**: `profile.yaml:53-57` makes `compare` a first-class mode triggered generically
  ("strategy A versus B"), but only `dynamic-and-formal-equivalence` and
  `text-level-approach-and-limits-of-equivalence` describe a compare-mode output shape. The other
  7 Output sections cover only review/advise, though comparisons routinely happen at their level.
- **fix**: Add one compare-mode output sentence to each of the 7, mirroring the two skills that
  already have it.

### S5 — P015 (masculine-as-unmarked) stated without inclusive-language / gender-system caveat
- **where**: `principles.yaml:316-321` (P015); `grammatical-equivalence/SKILL.md:90`
  (3 domain lenses flagged independently)
- **problem**: P015 states flatly "the masculine is usually the unmarked term" and restructures
  (passive) only "when neither marked nor unmarked gender fits." Reproduces Baker's 1992 framing
  with no caveat that (a) it holds only for binary masc/fem grammatical-gender systems, not
  universally, and (b) the masculine-generic default is now widely contested (singular "they,"
  écriture inclusive, EU/UN style guides). Applied literally in 2026, risks a rendering that
  clashes with house style or a non-binary referent. Skill step 3 has a partial note; the
  principle text itself (the reused locus) does not — the two loci disagree.
- **fix**: Qualify P015: "in languages with a masculine/feminine grammatical-gender system, the
  masculine is traditionally the unmarked term"; add a brief/house-style inclusive-language check
  and singular-they recasting as a live option to P015 and the skill step; align both loci.

### S6 — P100 (back-translation) one-sidedly framed as an "unsound compromise"
- **where**: `principles.yaml:1862-1868` (P100); `dynamic-and-formal-equivalence/SKILL.md:113`
  (2 domain lenses flagged independently)
- **problem**: P100 says back-translation is used "only to expose … structure" and is "a
  theoretically unsound compromise." Omits its legitimate, still-mandated QA role in regulated
  domains (clinical/PRO instruments, pharmacovigilance, legal). Sibling
  `technical-translation-advisor` treats it as "a limited quality check," which P100 contradicts
  in tone — could steer a reviewer away from a sometimes-required check.
- **fix**: Broaden P100 to acknowledge the limited-but-legitimate QA use (keeping the valid
  caution that a matching back-translation doesn't certify equivalence — a shared error survives).

### S7 — Adapter frontmatter description under-represents review/compare modes
- **where**: `.claude/agents/generated/translation-equivalence-advisor.md:3` (routing line) vs.
  `profile.yaml:16-25` (when_to_use) — ai-agent-engineering + agent-skills lenses concur
- **problem**: One-line description compresses to only the first when_to_use bullet
  (culture-specific item / idiom), never surfacing the review-mode trigger ("review a draft
  translation…") or compare-mode. Two of three modes — and arguably the most common invocation
  (submitting a draft for critique) — are invisible at routing time.
- **fix**: Extend the frontmatter description to cover review (and compare) explicitly, e.g.
  append "; reviews a draft translation or rendering decision against equivalence principles."

### S8 — `text-level-approach-and-limits-of-equivalence` description lacks concrete caller phrasing
- **where**: `skills/text-level-approach-and-limits-of-equivalence/SKILL.md` frontmatter
  `description` (concrete phrasing only in body `When to use`, line 67)
- **problem**: The "is this translation 'right,' 'literal enough,' or 'faithful'?" caller phrasing
  that most naturally selects this skill lives only in the body; the frontmatter description is
  the sole routing-time signal, so the skill under-triggers. (r3 S7, unaddressed.)
- **fix**: Fold the concrete caller phrasing into the frontmatter description.

### S9 — Missing review-loop artifact for the v1.2.2 fix round
- **where**: `reports/review-loop/` (has r1/r2/r3/verify1 + `.done`, none for the SF-1…SF-13
  v1.2.2 round the CHANGELOG/ledger attribute fixes to)
- **problem**: Audit trail for the latest, currently-shipping round is absent from the package
  though the ledger describes it in detail.
- **fix**: Add the corresponding review report for traceability.

### S10 — Stale generation timestamps on test-results + adapter
- **where**: `tests/test-results.md:3`, `adapters/claude-code/translation-equivalence-advisor.md:14`
- **problem**: Both show `Generated: 2026-07-11T19:03…` though ledger/CHANGELOG claim v1.2.2
  (2026-07-12) regenerated both. Adapter *content* matches v1.2.2 (re-stamp quirk), but
  `test-results.md` still reports the pre-r3 self-check and was not re-run against M1/M2.
- **fix**: Regenerate both after M1/M2 land.

---

## NICE

- N1 — Profile body ~992/800 words (`tests/test-results.md:24`): WARNING band, under 1000-word
  hard limit, but no headroom after additive fixes. Trim before next revision.
- N2 — word-level vs. dynamic-formal skills give overlapping open strategy sets for a
  culture-specific single item with different taxonomies and no cross-reference
  (`word-level-nonequivalence-and-strategies/SKILL.md:100` vs.
  `dynamic-and-formal-equivalence/SKILL.md:110`). Add a one-line disambiguator.
- N3 — `grammatical-equivalence/SKILL.md:94` introduces a 3-way taxonomy (ordinary parallels /
  functional cultural analogues / culture-specific items) not defined in the key-concepts
  reference — progressive-disclosure dead-end. Add a glossary entry or inline definition.
- N4 — Advise vs. compare mode triggers overlap in wording ("which strategy fits" vs. "strategy
  A vs. B"); distinguished only by output shape (`profile.yaml:43-46` vs. `:53-57`). Tighten the
  trigger text (advise = no candidate options named yet; compare = ≥2 named).
- N5 — P009 passive "adversity in Japanese and Chinese" stated without a modern-Mandarin
  currency qualifier (被 broadened beyond adversative) (`principles.yaml:192-197`). Add
  "traditionally/historically" framing. (3 domain lenses concur.)
- N6 — P033 contrastive-rhetoric national-style claims (German digression / Arabic repetition /
  Japanese linkless anecdote) presented as settled fact rather than a contested (Kaplan-style)
  tradition (`principles.yaml:695-702`). Soften to "criticized by some scholars…".
- N7 — Dynamic-equivalence terminology not noted as later relabeled "functional equivalence"
  (Nida & de Waard 1986) to curb the "dynamic = license for paraphrase" misreading
  (`dynamic-and-formal-equivalence/SKILL.md`). Add a one-line currency note.
- N8 — P001 bundles "loan word" and "false friend" in one non-equivalence-type bullet; false
  friend is a mistranslation risk, a different failure mode (`principles.yaml:4-9`,
  `word-level-nonequivalence-and-strategies/SKILL.md:98`). Split into two clauses.
- N9 — Nida coverage intentionally partial (secondary ~10k-word extract; kernel-sentence /
  componential-analysis / analysis-transfer-restructuring absent). Note in provenance ledger so a
  future reviewer doesn't assume they were considered and excluded (`profile.yaml:208-214`).
- N10 — Consider a `when_not_to_use` / `handoff_rules` pointer to sibling packages covering
  Catford / House / Koller / Vinay-Darbelnet equivalence frameworks, so callers wanting broader
  equivalence-theory coverage route correctly.
- N11 — Adapter router `description` truncates domain scope mid-clause (shared factory-template
  concern, correctly deferred in ledger) — not a package-specific fix.
- N12 — Precedence rule (role + forbidden override invariants) stated twice in slightly different
  words (adapter lines 19 and 23); optional consolidation if body size becomes a concern.

---

## Non-findings (verified sound)

Tool boundary (Read/Grep/Glob only, `may_edit_canonical: false`, empty mcp/caller_supplied),
canonical-ownership assignment, and the advisory / no-final-text boundary are correctly and
explicitly engineered (ai-agent-engineering: 0 must-fix). Domain coverage of non-equivalence
types, idiom/collocation strategy, theme/rheme & FSP, cohesion, Gricean pragmatics, and the
formal/dynamic orientation tracks Baker + Nida accurately — all three domain lenses returned 0
must-fix. Absence of MQM/LISA/ISO-17100 and CAT/MT tooling is intentional and in-scope-excluded.

MUST_FIX_COUNT: 2
