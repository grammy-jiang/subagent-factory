# Review Loop — translation-quality-reviewer — Round 5

Date: 2026-07-12
Package: `subagents/translation-quality-reviewer/` (v1.4.0, status: ready)

## Deterministic gates (STEP 1)

| Gate | Result |
|------|--------|
| `validate_generated_package` | **PASS** (0 FAIL; 1 accepted WARNING: phase8 body-size ~950/1000w, disclosed in CHANGELOG + ledger) |
| `quote_scan` | **PASS** — no verbatim quotation |
| Ellipsis-truncation grep (skills + adapter) | clean |
| Severed-invariant grep (adapter) | clean |

No deterministic FAILs.

## LLM reviewer panel (STEP 2)

All 7 reviewers returned MUST_FIX_COUNT: 0.

| Lens | Reviewer | must-fix |
|------|----------|----------|
| Skill authoring | agent-skills-advisor | 0 |
| Profile release-readiness | profile-reviewer | 0 |
| Faithfulness / over-claim | faithfulness-reviewer | 0 |
| Agent design | ai-agent-engineering-reviewer | 0 |
| Domain — equivalence | translation-equivalence-advisor | 0 |
| Domain — descriptive TS | descriptive-translation-reviewer | 0 |
| Domain — technical/QA | technical-translation-advisor | 0 |

## Consolidated findings (deduped, most-severe first)

No must-fix. All findings below are should-fix / nice — advisory, non-blocking. Dedup note: the P042 House-model Participation-placement issue was raised by three lenses (faithfulness, descriptive, technical) and is consolidated as S1; the Yu Guangzhong 的/被 coverage gap by two lenses (descriptive, technical) as S6.

### should-fix

| # | Where | Problem | Fix |
|---|-------|---------|-----|
| S1 | `profile.yaml` `always_on[3]`; `principles.yaml` P042/P075; `skills/register-field-tenor-mode-analysis/SKILL.md` steps 5/13 | House model-history claim: revised (1997/2015) model "repositions Participation from Mode into Tenor" is (a) stated as settled and drives a corrective anti-pattern rule, and (b) the `always_on[3]` prose drops P042's explicit "establish which model is in force first" caveat (HEDGING_REMOVED). technical-translation-advisor further disputes the *direction* — recalls Participation stays under Mode in both schemes; not fully verifiable from scoped files. | Re-verify the Participation-placement claim directly against House 2015 (cited source) before it keeps gating the anti-pattern. Restore the "establish which House model is in force before flagging a Tenor/Mode placement" caveat into `always_on[3]`. |
| S2 | `.claude/agents/generated/translation-quality-reviewer.md` frontmatter `description`; `profile.yaml` `when_not_to_use[1]` | Adapter frontmatter (primary routing signal) carries only one "Not for" clause. The routing-critical sibling boundary — qualitative/single-text-norm / domestication-vs-foreignization → `descriptive-translation-reviewer` — never surfaces in the always-visible description, risking cross-agent misrouting at the seam the profile itself flags as important. | Add a second "Not for" clause to the frontmatter description: quantitative/corpus-based vs qualitative/single-text-norm boundary, naming `descriptive-translation-reviewer`. |
| S3 | `skills/error-analysis-and-evaluation-discipline/SKILL.md` (whole); `profile.yaml` role/when_to_use ("error typologies, evaluation discipline") | Evaluation-discipline skill is built solely on House's academic dimensional typology; never acknowledges industry-standard frameworks (MQM / ISO 5060:2024, LISA QA, SAE J2450, DQF) that dominate professional TQA. Users judging "error typologies" remit against these will see a gap. | Add a principle/step: House's dimensional model is one rigorous academic framework among several; for professional/LSP QA, point to MQM/ISO 5060 and map House categories onto MQM Accuracy/Fluency/Terminology/Style. |
| S4 | `principles.yaml` P076; `skills/descriptive-studies-and-translational-norms/SKILL.md` step 8 + "Norm-level conflation" anti-pattern | Matricial norms glossed to include "substitutions." In Toury, matricial norms govern existence/location/segmentation of TL material; lexical/stylistic substitution belongs to textual-linguistic norms — the exact boundary this section polices. | Narrow matricial gloss to existence/location/segmentation (omission/addition/relocation/segmentation); move "substitution" examples into the textual-norm gloss. Verify vs source claims C00506–C00509. |
| S5 | `skills/translation-universals-and-the-third-code/SKILL.md` step 7; `principles.yaml` P139 | P139 restricts "translationese" to translator incompetence only. Much corpus/computational TS (Gellerstam, Teich shining-through, translationese classifiers) uses the term competence-neutrally. Rigid application could mis-flag a caller's legitimate neutral usage. | Soften P139: note term's scope varies (competence-restricted in some prescriptive traditions; neutral/descriptive in corpus-TS/computational). Reviewer's job = identify which sense is meant + whether evidence supports a competence claim. |
| S6 | `skills/chinese-prose-and-europeanization/SKILL.md` Purpose caveat; P119/P120/P149/P150 | Skill self-discloses it omits 的-stacking ("的的不休") and 被-passive overuse — the two most iconic diagnostic markers of Europeanized Chinese in Yu Guangzhong's actual essay. Disclosed, but a real coverage gap in a core diagnostic area. | If the underlying Yu Guangzhong claims exist, extract principles for 的-stacking and 被-passive overuse and add to the skill so coverage matches source emphasis; else keep disclosed caveat. |
| S7 | `skills/chinese-prose-and-europeanization/SKILL.md` (whole) vs P114 | Chinese-prose skill applies Yu Guangzhong's prescriptive stylistic-purist criteria as direct findings, while P114 (and the rest of the package) demands a non-evaluative descriptive stance. Double standard risks mislabeling stylistic-quality findings as corpus-validated third-code findings. | Add a note (skill purpose or profile precedence): Yu's Europeanization criteria are a prescriptive stylistic lens distinct from the descriptive/corpus-empirical stance; label its findings as stylistic-quality, not corpus-validated. |
| S8 | `skills/overt-covert-translation-and-equivalence/SKILL.md` step 18 (P136) vs `cognition-pragmatics-and-contrastive-evidence` (P004/P015) | P136 presents House's cognitive-load hypothesis (overt co-activates source+target pragmatics; covert target-only) as operational fact; the package's own cognition skill (P015) insists cognitive-process claims need evidence and are limited. P136 uncrossed-referenced. | Cross-reference P136 to P015's evidentiary caution — treat it as a theoretical expectation to test, not a settled processing fact. |
| S9 | Long-procedure skills: `error-analysis-and-evaluation-discipline`, `overt-covert-translation-and-equivalence`, `cultural-filtering-ideology-and-globalization`, `register-field-tenor-mode-analysis`, `corpus-design-and-methodology` | 14–19 flat procedure steps + anti-patterns sit entirely in always-loaded SKILL.md (~1000–1100w each); shared references not used to defer procedural depth — runs against 3-tier progressive-disclosure (P001/P005/P029) + concision invariant (P088/P114). | Keep SKILL.md to triage grouping + one-line step summaries; move granular per-step elaboration into a per-skill/per-cluster reference loaded lazily. |
| S10 | `provenance-ledger.md` | Ledger (canonical release record) never records that `quote_scan` was run/its result (mandated "before release" by rights-and-quotation-policy for the 5 distillation-only sources), nor a consolidated Phase-8 self-check verdict (only CHANGELOG mentions the accepted WARNING). | Add to ledger: a `quote_scan` result line (date + 0 findings ≥40 words) and a Phase-8 self-check subsection stating per-check verdict count + the one accepted body-size WARNING with rationale. |

### nice

| # | Where | Problem | Fix |
|---|-------|---------|-----|
| N1 | `russian-corpus-and-interpreting-research`, `genre-childrens-literature-and-accessibility` SKILL.md | 11/12-step procedures lack the opening triage/grouping sentence used by the other 10 long skills (P012 scannability pattern). | Add a one-line triage/grouping sentence at top of each Procedure section. |
| N2 | `profile.yaml` name/description + adapter frontmatter | Distinctive niches (Russian-field multifactorial modelling; Chinese Europeanization) are full `when_to_use` triggers but invisible in name/description → discoverability gap for exactly those callers. | Surface the two niches as keywords in frontmatter description, or flag for a future split decision. |
| N3 | `translation-universals-and-the-third-code` step 5; P115 | Rival-explanation space framed binary (universal vs language-pair/culture norm); omits the well-established cognitive/processing-effort account (risk-aversion, processing-load) which the package covers elsewhere (P004/P009/P015) but doesn't cross-reference here. | Cross-reference step 5 → cognition skill, naming cognitive/processing-effort as a third rival explanation. |
| N4 | `register-field-tenor-mode-analysis`; P042 vs P075 | P042 glosses Field as "subject matter and lexical granularity" — narrower than Hallidayan Field (social activity/process type); fuller transitivity content only in P075 (step 13). Read at step 5 in isolation → overly lexis-centric Field. | Fold process-type/transitivity into P042, or forward-pointer step 5 → step 13. |
| N5 | `russian-corpus-and-interpreting-research` step 7 (P057); `corpus-design-and-methodology` | P057 scopes human-vs-MT comparison but package never names automatic MT metrics (BLEU/COMET/chrF/TER) or their known limited correlation with human judgment. | Add a brief note: when comparing human/MT output, name the automatic metric + flag correlation limits, paired with existing significance/effect-size discipline. |
| N6 | `quality_bar[1]`; P118 | P118 cited generically but its `applies_when` is Bible-translation-specific; P050 already grounds the metadata/comparability requirement generically (redundant over-narrow citation, SCOPE_BROADENED minor). | Drop P118 from `quality_bar[1]`, or add a scoping clause. |
| N7 | `examples[1]` | "equivalence stays close to formal (P005, P059)" — neither principle states overt equivalence defaults formal; closest is P030 (case-by-case demands). Borderline HEDGING_REMOVED. | Cite P030 + soften to "weighed case by case across formal/denotative/pragmatic demands," or drop the clause. |
| N8 | `descriptive-studies-and-translational-norms` / package-wide | Toury's "laws" (growing standardization, interference) — the norms↔universals bridge — never named, though normalization≈standardization and P033 shining-through≈interference. Likely intentional (sibling `descriptive-translation-reviewer` owns Toury's laws). | If underlying source claims reference the "laws" terminology, name it for completeness; else no action given deliberate cross-package split. |
| N9 | `register-field-tenor-mode-analysis`; P010/P070–P074 | 6/16 principles tuned to one genre (institutional "mission statements"); risks over-indexing register findings to that genre. | Broaden `applies_when` to "persuasive/exhortative institutional genres (mission statements, codes of conduct, CSR, etc.)". |
| N10 | `register-field-tenor-mode-analysis`; `handoff_rules` | Cross-package pointer ("defer to technical-translation-advisor") visible only inside this one skill body. | Surface once at profile level in `handoff_rules`. |
| N11 | `profile.yaml` `handoff_rules` (+ adapter mirror) | Handoff for out-of-scope concerns (subject-matter accuracy, statistical/software model impl) names no concrete owner ("the owning specialist"). | Name a concrete sibling/specialist if one exists in the catalog; else leave generic. |
| N12 | `chinese-prose-and-europeanization/SKILL.md` | Markedly smaller than siblings (4 principles / 1 source). Not a defect; note only if team later wants fewer, denser skills. | No action; revisit if consolidating skills. |
| N13 | `profile.yaml` body length | ~950/1000w — ~50w headroom before hard-FAIL. Already accepted. | Budget word count against thin margin on future version bumps. |

## Notes for the fix pass

- S1 is the highest-value should-fix: it couples a possibly-wrong domain claim (P042 Participation placement) to a dropped source caveat AND drives an active anti-pattern rule. Needs source re-verification against House 2015, not just a prose tweak.
- S6/S7 both concern the Chinese-prose skill; a single fix pass can address the descriptive/prescriptive labeling (S7) and the 的/被 coverage gap (S6) together.
- S9 (progressive disclosure) and S10 (ledger traceability) are structural/documentation, independent of domain content.

MUST_FIX_COUNT: 0
