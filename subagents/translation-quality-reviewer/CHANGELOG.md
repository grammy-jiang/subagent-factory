# Changelog — translation-quality-reviewer

All notable changes to this generated subagent package are recorded here. Versions follow the
`agent_version` field in `profile.yaml`.

## [1.4.0] — 2026-07-12

### Fixed (review loop r4)
- **P042 self-contradiction** (M1): P042 described the *revised* Field/Tenor/Mode split while calling it the
  *earlier* one and never stated the earlier split. Rewritten grounded in C00180/181/182 + P075 (C00418):
  House's **earlier** model keeps Participation under **Mode**; her **revised** model moves it to **Tenor**;
  establish which model is in force before flagging a placement. `register-field-tenor-mode-analysis` step 5
  and its anti-pattern aligned to the corrected principle.
- **P056 mis-grounded citation** (M2): `quality_bar[3]`'s cultural-filtering clause cited `(P056, P137)`, but
  P056 is about **multifactorial modelling of complex variation**, not cultural filtering. Dropped P056; P137
  alone grounds the clause. Faithfulness-report note for `quality_bar[3]` corrected accordingly.
- **Anti-patterns 1:1 negation** (M3): in all 12 skills the "Anti-patterns to flag" section was an exhaustive
  negated restatement of every Procedure step (8-vs-8, 15-vs-15…), doubling body token cost with zero new
  signal. Re-authored each to a short, skill-specific set (~4–6 bullets) adding thresholds, paired good/bad
  contrasts, and commonly-confused distinctions — grounded only in each skill's own principle IDs.

### Changed
- **P116 over-broadening** (S1): `quality_bar[3]` scoped the co-occurring-cluster rule to where corpus/frequency
  evidence is used and softened "not isolated frequencies" to "prefer … over isolated frequencies", matching
  P116's conditional framing ("When adapting register-analysis tools to translation").
- **Per-skill provenance** (S7): each skill's `## Provenance` sentence now names only the source(s) that
  actually ground its principles, not all five.
- **Scope-boundary boilerplate** (S8): each skill's `## Output` closing boundary shortened to a single clause
  (the full boundary lives at profile level).
- **corpus-design triage** (S9): added a "Triage first" preamble grouping the 15-step Procedure; light triage
  preamble also added to `applied-corpus-tools-and-textual-devices` (N10).
- **descriptive-norms scope note** (S5): P034 target-orientation scoped to descriptive/corpus-norm
  reconstruction, not House-model overt/covert equivalence.
- **chinese-prose coverage note** (S4): noted that 的-stacking and 被-passive overuse fall outside this skill's
  distilled principle set (P119/P120/P149/P150), so a reviewer treats them separately.
- **iconic-linkage gloss** (N3): genre skill keeps House's cohesion-device sense of "iconic linkage" distinct
  from a terminology-reuse sense.

### Known / accepted
- **Body-size WARNING** (S2): profile body sits ~950w (Phase-8 WARN, under the 1000w FAIL). Accepted rather
  than trimmed — the r3 MF1/MF3 grounding text (source-and-target-pairs precision, corpus/empirical routing)
  is load-bearing and cannot be cut without weakening grounding. Non-blocking.

## [1.3.0] — 2026-07-12

### Fixed (review loop r3)
- **Sibling routing** (MF1): `when_to_use[1]` reworded to front-load the quantitative/corpus-empirical
  boundary (frequency evidence, corpus design/comparability, source-and-target norm reconstruction,
  keyword/concordance/collocation); a new `when_not_to_use` bullet routes qualitative single-text norm /
  translator-visibility critique (domestication–foreignization, orientation read from one text) to
  `descriptive-translation-reviewer`. Re-exported so the adapter `description` carries the distinguishing
  corpus/empirical terms.
- **Faithfulness coverage** (MF2): added the missing `when_to_use[5]` verdict (P090/P061/P044/P116/P082) —
  every `when_to_use` bullet is now graded — and corrected the miscount: the 1.2.0 changelog/ledger said
  "40 findings" but the report held 36; it now holds 37.
- **P083 SCOPE_BROADENED** (MF3): `quality_bar[5]` and `always_on[7]` now state P083 precisely — norms
  reconstructed only from a corpus of **source-and-target text pairs**, never a generic or target-only
  collection. The faithfulness-report entries for both were corrected to describe the actual profile text
  (the prior "P083 as corrected" note graded a correction that was not in the text).
- **Toury norm levels** (MF4): `always_on[7]` now scopes P076 to operational (matricial/textual) norms and
  requires a norm claim to be placed at its level first, so an overall-orientation or translation-policy
  claim is not silently judged by operational criteria. A new principle for the initial/preliminary norm
  levels was **not** added — no promoted claim grounds that content; a scope guard was applied instead of
  an ungrounded principle.
- **Provenance ledger** (MF5): corrected the false "descriptive fields carry no inline tags" claim —
  `when_to_use` does carry inline principle tags and is graded in the faithfulness report; only `role`,
  `inputs`, `outputs` are untagged.

### Changed
- **P120** (SF1): restored the two-clause either/or with the "when natural" condition in `always_on[10]`
  ("stand by juxtaposition when natural, otherwise choose connectors matched to progression/contrast/
  adjustment rather than English-style and-linking") — the 1.2.0 wording had fused it to the
  near-contradictory "juxtaposition with connectors".
- **Register skill** (SF2): dropped the ungrounded "standard Hallidayan register split" excuse from the
  Participation-under-Mode anti-pattern; kept only House's earlier model (grounded in P042). Aligned the
  skill Purpose wording ("mission statements and comparably exhortative institutional texts") with its
  frontmatter (N9).
- **Trigger keywords** (SF8): added register (Field/Tenor/Mode) and applied-corpus-tools
  (keyword/concordance/collocation) triggers to `when_to_use[5]` (P116/P082).
- Re-exported the Claude Code adapter from the updated profile.

## [1.2.0] — 2026-07-12

### Fixed (review loop r2)
- **P083** (M3) rewritten to preserve Toury's coupled-pairs method: a norm is identified from a corpus
  of **source texts and their translations** (comparison across source–target pairs), not projected
  from the source text's own features alone, an idealised target system, or a generic target-text
  collection (grounded C00470 + C00472). The `descriptive-studies-and-translational-norms` step 10 and
  its anti-pattern updated to match, so the reviewer no longer rejects ST–TT comparison as evidence.
- **P076 procedure step** (M4) restored in `descriptive-studies-and-translational-norms` step 8: names
  the two levels — matricial (omissions, additions, substitutions, transpositions in distribution) and
  textual (collocation, speech treatment, title conventions) — inline, so the step is executable.
- **Register skill** (M1): the anti-pattern no longer flags Participation-under-Mode as a blanket error.
  Participation → Tenor is scoped to House's **revised** model (P042/P075); the standard/earlier
  Hallidayan split (Participation under Mode) is not penalised — the reviewer establishes which model is
  in force first.
- **Translationese senses** (M2): `translation-universals-and-the-third-code` (step 7 + anti-pattern),
  `profile.yaml` `examples[0]`, and `references/translation-quality-evidence-notes.md` now name which
  sense of "translationese" is in play — an automatic classifier/corpus "translationese score" measures
  the distinctive translated-vs-original profile (the third code / normal patterning, P139/P114), not a
  competence diagnosis (P139) and not a quality verdict (P002).
- **Faithfulness coverage** (M5): `faithfulness-report.yaml` extended from 17 to 36 findings — added a
  verdict per `knowledge_partition.always_on` paragraph (12), each `handoff_rules` item (2), each
  `outputs.modes` mode (3), and both `examples` (2). The ledger's full-coverage claim is now true at the
  artifact level.

### Changed
- Restored P082's hedge "treat limited findings as hypotheses for further testing" in the applied-corpus
  `always_on` paragraph (S4); scoped the metadata-rich-corpora sentence to multifactorial studies such as
  Polish-Russian/Russian-Polish pairs (P058, S4).
- Split `quality_bar[3]` (S5) so the co-occurring-feature-cluster method attaches to register only (P116);
  cultural filtering is stated as source-to-target comparison (P056/P137) without borrowing that method.
- Added `translation-universals` step-6 note (S6) routing explicitation-type (source-relative) claims to
  parallel-corpus evidence, distinct from the monolingual-comparable design (P121) used for
  simplification/normalisation.
- Added a corpus-design-vs-engineering boundary to `handoff_rules[1]` (S11): choosing corpus type/controls
  is in scope, building the pipeline/implementation is not (P003/P078).
- `when_to_use[2]` now also routes cognitive-process / contrastive-pragmatic evidence claims (P132, S3);
  `when_to_use[0]` broadened to a multi-surface trigger (quality / corpus-method / translationese-as-proxy)
  so the exported adapter description carries more routing signal (S2).
- Trimmed profile body fields to 800 words (S1), clearing the Phase-8 body-size WARNING.
- Added triage/grouping lead-ins to `descriptive-studies-and-translational-norms` and
  `register-field-tenor-mode-analysis` procedures (S15), a sci-tech Field defer to
  `technical-translation-advisor` (S9), and folded operative nouns back into thin procedure steps (S14).
- Corrected the 1.1.0 changelog wording below: v1.1.0 did **not** split the Russian/Chinese `when_to_use`
  trigger (S3).
- Re-exported the Claude Code adapter from the updated profile.

## [1.1.0] — 2026-07-12

### Fixed (review loop r1)
- Re-exported the Claude Code adapter with the corrected `compile_invariants`, restoring the full
  operating invariants (the earlier export truncated P001/P002/P012/P018/P020/P029/P055-P058/P121/P122
  with a trailing `…` and silently colon-cut P003/P019/P035/P053/P054/P083/P084).
- **P003** rewritten to name all three corpus types — parallel (equivalence/shifts/alignment),
  monolingual comparable (translated vs non-translated, same target language, for
  universals/translationese, grounded in P121), and multilingual comparable (cross-linguistic
  contrast) — instead of defining "comparable" only in the multilingual sense.
- **P042** now notes that participation sat under Mode in House's earlier model and is reassigned to
  Tenor in her revised model (P075 governs), removing the Mode-vs-Tenor contradiction within the
  register skill.
- **P139** weakened to match its source (Baker C00515): the label *translationese* applies only when
  an unusual distribution is clearly the result of translator inexperience/incompetence, not as a
  blanket definition — resolving the contradiction with P002/P147.

### Changed
- All 12 skills re-authored to gold shape: added a `description:` frontmatter line (routing signal +
  neighbouring-skill boundary), and rewrote `## Anti-patterns to flag` as complete, skill-specific
  sentences (one per load-bearing principle) instead of truncated generic principle echoes.
- Profile faithfulness tightened: dropped spurious anchors (P084 from quality_bar[0], P090 from
  quality_bar[2]); narrowed the `precedence` rule (P032/P047/P115) to its cultural-filter /
  universal-tendency scope; scoped the register `always_on` bullet to "mission statements and
  comparably exhortative institutional texts" (P010/P070-P075); re-marked `handoff_rules[1]` as a
  profile-level scoping judgement (dropped unrelated P052/P077); softened the contract-as-overt
  example to "plausible candidate". Added `when_to_use` coverage for error-discipline and
  genre/accessibility triggers.

## [1.0.0] — 2026-07-12

### Added
- Initial release of the **translation-quality-reviewer** subagent (Tier 2), authoring the LLM layer over the
  already-assembled, deterministically-valid distilled spine (150 principles
  P001-P150 / 713 claims from five distillation-only sources).
- `profile.yaml` derived from the 150 promoted principles: role, when/when-not-to-use,
  three modes (review / advise / compare), quality bar, forbidden behaviours, handoff rules, and a
  12-skill / 2-reference `knowledge_partition` covering every principle exactly
  once.
- 12 authored skills partitioning all 150 principles; 2 references
  (principles index + evidence notes).
- `reports/faithfulness-report.yaml` — every load-bearing profile rule graded WITHIN_SCOPE against
  its principles (no rule stronger than its evidence).
- `tests/golden-tests.yaml` (6 golden, 2 negative-routing,
  2 missing-context) and `tests/principle-behaviour-tests.yaml` (one behaviour test per
  principle, 150 total).
- Claude Code adapter exported to `adapters/claude-code/` and installed under
  `.claude/agents/generated/`.

### Grounding
- Five distillation-only sources: Juliane House, *Translation Quality Assessment: Past and Present*
  (2015); Mona Baker, *Corpus Linguistics and Translation Studies* (1993); Haidee Kruger et al.,
  *Corpus-Based Translation Studies* (2011); Daria Dayter & Łukasz Grabowski, eds., corpus-based
  translation and interpreting studies in the Russian field (2023); Yu Guangzhong on the normal and
  distorted states of Chinese prose (1987).
