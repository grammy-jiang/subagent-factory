# Provenance Ledger — translation-quality-reviewer

Canonical record of what grounds this subagent. The profile, skills, references, faithfulness
report, and tests are all derived from the distilled spine in this package
(`principles/principles.yaml` -> `analysis/claims.jsonl` -> `evidence/evidence-records.yaml` ->
`sources/anchors/*.anchors.jsonl`), assembled by the map->reduce build. No load-bearing profile rule
field is an orphan: every `quality_bar`, `forbidden_behaviours`, `handoff_rules`,
`knowledge_partition.always_on`, and `source_of_truth_policy` value cites the promoted principle(s)
it restates. `when_to_use` also carries inline principle tags on every bullet, and each bullet is
graded in `reports/faithfulness-report.yaml`. (The remaining descriptive fields — `role`, `inputs`,
`outputs` — carry no inline tags, per repo convention.)

## Sources

| source_id | title | author | year | rights |
|-----------|-------|--------|------|--------|
| translation-quality-c0dd203d | Translation Quality Assessment: Past and Present | Juliane House | 2015 | distillation-only |
| corpus-linguistics-t-ceffdb40 | Corpus Linguistics and Translation Studies: Implications and Applications | Mona Baker | 1993 | distillation-only |
| corpus-based-transla-98c56c2d | Corpus-Based Translation Studies: Research and Applications | Haidee Kruger, Kim Wallmach and Jeremy Munday (eds.) | 2011 | distillation-only |
| corpus-translation-r-b10b2ead | Corpus-Based Translation and Interpreting Studies (the Russian field) | Daria Dayter and Łukasz Grabowski (eds.) | 2023 | distillation-only |
| chinglish-europeaniz-5798beb7 | On the Normal and Distorted States of Chinese (Europeanized Chinese / Chinglish) | Yu Guangzhong | 1987 | distillation-only |

All five sources are **distillation-only**: paraphrase and restructure only, no verbatim quotation
(see `.claude/rules/rights-and-quotation-policy.md`; enforced by `quote_scan`). They are canonical
translation-quality and corpus-translation-studies works: House's functional-pragmatic quality
model, Baker's and Kruger et al.'s corpus programme and universals, the Dayter & Grabowski Russian-
field volume, and Yu Guangzhong on Europeanized Chinese prose.

## Distillation

Spine: 150 promoted principles (P001-P150; 19 high-confidence) over
713 atomic claims, with evidence records and chunk anchors. The 150
principles are partitioned across 12 skills, each principle owned by exactly one skill;
the two references index and ground them.

## Version History

- **v1.5.0** (2026-07-12) — In-session finish after the auto-merge driver triage-stopped: an independent
  adversarial faithfulness verify found 11 citation-integrity over-claims the loop's rubber-stamp
  faithfulness-report missed. Dropped the manufactured P059/P134 citation from four ownership/sign-off
  clauses (now labelled advice-only role boundaries); removed text-type-scoped P118/P081 (Bible) and P044
  (children's books) from general clauses; restored P042's House-model hedge; removed the ungrounded
  Toury norm-level clause; restated examples[1]'s Nida "formal equivalence" bleed in the package's own
  Koller terms (P030). No spine (principles) change; adapter re-exported.

- **1.4.0** (2026-07-12) — Review-loop r4 fixes (supersedes 1.3.0 on the points below; earlier decisions
  remain visible). **M1** P042 self-contradiction: P042 described the revised Field/Tenor/Mode split while
  labelling it the earlier one and never stated the earlier split, making the register skill's
  "establish which model is in force" anti-pattern unusable. Rewritten grounded in C00180/C00181/C00182
  (earlier model: Field = subject matter/lexis; Tenor = participant roles/power/distance/stance;
  **Mode = channel + participation**) and P075/C00418 (revised model repositions Participation into Tenor);
  `register-field-tenor-mode-analysis` step 5 + its anti-pattern realigned. **M2** P056 mis-grounded citation:
  `quality_bar[3]`'s cultural-filtering clause cited `(P056, P137)`, but P056 concerns multifactorial modelling
  of complex variation, not cultural filtering — dropped P056 (P137 alone grounds it), corrected the matching
  faithfulness-report note. **M3** anti-pattern 1:1 negation: in all 12 skills the "Anti-patterns to flag"
  section was an exhaustive negated restatement of every Procedure step (doubling body token cost with zero new
  signal, against the package's own progressive-disclosure bar P001/P005/P029/P088/P114); re-authored each to a
  short skill-specific set (~4–6 bullets) adding thresholds, paired good/bad contrasts, and commonly-confused
  distinctions, grounded only in each skill's own principle IDs. Also: **S1** scoped `quality_bar[3]`'s
  co-occurring-cluster rule to corpus/frequency evidence and softened to "prefer", matching P116's conditional
  framing; **S5** scoped P034 target-orientation to descriptive/corpus-norm reconstruction (not House-model
  equivalence) in `descriptive-studies-and-translational-norms`; **S4** noted 的-stacking and 被-passive overuse
  fall outside `chinese-prose-and-europeanization`'s distilled principle set (P119/P120/P149/P150); **S7** made
  each skill's `## Provenance` name only the source(s) grounding its principles; **S8** shortened the repeated
  scope-boundary in each skill's `## Output` to one clause; **S9/N10** added triage-grouping preambles to
  `corpus-design-and-methodology` and `applied-corpus-tools-and-textual-devices`; **N3** kept House's
  cohesion-device sense of "iconic linkage" distinct in the genre skill. **S2** body-size WARNING (~950w, under
  the 1000w FAIL) accepted rather than trimmed — the r3 grounding text is load-bearing. No new principle added.
  Re-exported the adapter.

  Field→grounding rows affected: `quality_bar[3]` grounding changed from `(P042, P069, P116; P056, P137)` to
  `(P042, P069, P116; P137)` — cultural-filtering half now grounded by P137 only (P056 removed as mis-grounded).
  All other profile field→grounding rows unchanged.
- **1.3.0** (2026-07-12) — Review-loop r3 fixes (supersedes 1.2.0 on the points below; earlier decisions
  remain visible). **MF1** sibling-routing collision: `when_to_use[1]` reworded to front-load the
  quantitative/corpus-empirical boundary (frequency evidence, corpus design/comparability,
  source-and-target norm reconstruction, keyword/concordance/collocation), and a new `when_not_to_use`
  bullet routes qualitative single-text norm / translator-visibility critique (domestication–foreignization,
  orientation-from-one-text) to `descriptive-translation-reviewer`; re-exported so the adapter description
  front-loads the distinguishing corpus/empirical terms. **MF2** faithfulness coverage: added the missing
  `when_to_use[5]` verdict (P090/P061/P044/P116/P082) — the report now grades every `when_to_use` bullet —
  and corrected the miscounted finding total (the 1.2.0 "40" was actually 36; now 37 with `when_to_use[5]`).
  **MF3** P083 SCOPE_BROADENED: `quality_bar[5]` and `always_on[7]` now state the restriction precisely —
  norms reconstructed only from a corpus of source-and-target text pairs, never a generic or target-only
  collection (P083) — and the faithfulness-report entries were corrected to describe the actual profile text
  (the earlier "P083 as corrected" note graded a correction not present in the text). **MF4** Toury norm
  levels: `always_on[7]` now scopes P076 to operational (matricial/textual) norms and requires a norm claim
  to be placed at its level first, so an overall-orientation or translation-policy claim is not judged by
  the operational criteria; a new principle for the initial/preliminary norm levels was **not** added —
  no promoted claim in the spine grounds that content, so a scope guard was applied instead of an ungrounded
  principle. **MF5** ledger corrected: `when_to_use` does carry inline principle tags (graded in the
  faithfulness report); only `role`, `inputs`, `outputs` are untagged. Also: **SF1** restored P120's
  two-clause either/or with the "when natural" condition in `always_on[10]`; **SF2** dropped the ungrounded
  "standard Hallidayan register split" excuse from the register skill's Participation-under-Mode anti-pattern
  (kept only House's earlier model, which is grounded in P042); **SF8** added register (Field/Tenor/Mode) and
  applied-corpus-tools trigger keywords to `when_to_use[5]`; **N9** aligned the register skill Purpose wording
  with its frontmatter. Re-exported the adapter.
- **1.2.0** (2026-07-12) — Review-loop r2 fixes (supersedes 1.1.0 on the points below; earlier decisions
  remain visible). Grounded principle/skill rewrites: **P083** now identifies norms from a corpus of
  source texts and their translations — comparison across source–target pairs — rather than "a
  representative body of translated texts" alone (grounded C00470 + C00472), preserving Toury's
  coupled-pairs method; the `descriptive-studies` skill (step 8 restores the matricial/textual two levels
  of **P076**; step 10 and its anti-pattern track the corrected P083). Register skill anti-pattern scoped
  Participation→Tenor to House's **revised** model (P042/P075), no longer flagging the earlier/standard
  Mode placement as an error. Translationese senses disambiguated across `translation-universals` skill,
  `examples[0]`, and evidence-notes: a classifier/corpus "translationese score" measures the distinctive
  translated-vs-original profile (third code / patterning, P139/P114), not competence-translationese and
  not a quality verdict (P002). Faithfulness coverage extended 17→36 findings (every `always_on`
  paragraph, `handoff_rules`, `outputs.modes`, and `examples` now graded WITHIN_SCOPE) — the full-coverage
  claim above is now accurate at the artifact level. Profile faithfulness tightened: restored P082's hedge
  in the applied-corpus paragraph; scoped the P058 metadata-rich-corpora sentence to multifactorial
  Polish-Russian/Russian-Polish studies; split `quality_bar[3]` so the feature-cluster method (P116)
  attaches to register only. Added a corpus-design/engineering boundary to `handoff_rules[1]` (P003/P078),
  a cognition/pragmatics `when_to_use` trigger (P132), an explicitation→parallel-corpus routing note
  (P121/P001), procedure triage lead-ins and a sci-tech Field defer; trimmed the profile body to 800 words.
  Re-exported the adapter.
- **1.1.0** (2026-07-12) — Review-loop r1 fixes (supersedes 1.0.0 on the points below; earlier
  decisions remain visible above). Re-exported the adapter to restore truncated operating invariants.
  Grounded principle rewrites: **P003** now names parallel / monolingual comparable / multilingual
  comparable corpus types (monolingual-comparable sense grounded in P121); **P042** labels
  participation-under-Mode as House's earlier model, superseded by **P075** (Tenor) in the revised
  model; **P139** restores Baker's conditional framing (translationese only when a distribution is
  clearly incompetence-driven), resolving the P002/P147 contradiction. All 12 skills re-authored to
  gold shape (added `description:` frontmatter, complete skill-specific anti-patterns). Profile
  faithfulness tightened: dropped spurious anchors P084 (quality_bar[0]) and P090 (quality_bar[2]);
  narrowed `precedence` (P032/P047/P115) to its cultural-filter/universal-tendency scope; scoped the
  register `always_on` bullet to mission statements and comparably exhortative institutional texts
  (P010/P070-P075); re-marked `handoff_rules[1]` as profile-level scoping judgement (dropped
  unrelated P052/P077); added `when_to_use` coverage for error-discipline and genre/accessibility.
- **1.0.0** (2026-07-12) — Initial LLM-authored layer over the pre-built distilled spine: profile
  (role, three modes, quality bar, forbidden behaviours, 12-skill / 2-reference
  knowledge partition), faithfulness report, 12 skills, 2 references, golden +
  principle-behaviour tests, and the exported Claude Code adapter. No prior profile decisions
  superseded.
