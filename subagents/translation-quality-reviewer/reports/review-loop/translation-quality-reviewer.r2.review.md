# Review Loop — translation-quality-reviewer — Round 2

Scope: one review pass over `subagents/translation-quality-reviewer/`. Deterministic gates +
7 reviewer lenses (4 factory lenses + 3 domain cross-checks). Findings deduped across lenses,
most-severe first.

## Deterministic gates — ALL PASS (0 must-fix)

- `validate_generated_package` → **VALIDATION PASSED** (phase8 self-check WARNING only — see M5/S1).
- `quote_scan` → PASS, no verbatim quotation.
- truncation greps (ellipsis / severed parenthetical) → no hits.

## must-fix

### M1 — P042/P075 likely misstate House's Register model (Participation Mode→Tenor)
- Where: `principles/principles.yaml` P042, P075; `skills/register-field-tenor-mode-analysis/SKILL.md` (Purpose, step 5, step 13, anti-pattern).
- Problem: P042/P075 assert House "reassigned Participation from Mode to Tenor" and an anti-pattern *flags placing Participation under Mode as an outdated error*. In House's model Mode has always had two sub-categories **Medium + Participation** (monologue/dialogue, addressee involvement); Tenor's sub-category is **Participant Relationship** (a distinct construct). This reads as a claim-extraction conflation of "Participation" (Mode) with "Participant Relationship" (Tenor), not a real model revision. As written the reviewer would *penalize the textbook-correct classification* on any text — including sci-tech instructional prose where Mode/Participation (imperatives/questions) is load-bearing.
- Fix: verify House 2015 page behind claim C00418 (`c0dd203dbe43-c0013`). If it describes Participant Relationship elaborated under Tenor (not Participation *moving*), correct P042/P075 to keep Participation under Mode and delete/rewrite the anti-pattern so it no longer flags the standard classification as error.

### M2 — P139 "translationese" definition internally inconsistent with package's own flagship example
- Where: `principles/principles.yaml` P139; `skills/translation-universals-and-the-third-code/SKILL.md` step 7 (L63), anti-pattern (L83); `references/translation-quality-evidence-notes.md:174`; collides with P002, P147, `profile.yaml` `examples[0]`.
- Problem: P139 defines translationese narrowly/exclusively as deviation "clearly the result of a translator's inexperience or lack of competence" (source-faithful to Baker C00515). But P002/P147 and the flagship worked example ("review a translation graded by its translationese score") use the broad corpus-linguistics sense that automatic classifiers actually detect (statistical divergence, no competence finding). Under P139's literal definition a classifier's "translationese score" isn't measuring translationese at all → the reviewer has no coherent principle for the very scenario the package designed as its headline example. (r1 recorded P139 as "fixed"; both domain reviewers independently re-flag it as still substantively unresolved.)
- Fix: split the concept — keep Baker's narrow sense relabeled + `applies_when`-scoped to competence-caused deviation; add/fold the broader corpus sense (statistically distinct translated-vs-original profile, skill-independent) that P002/P147/the example rely on, cross-referenced to the third code (P139's other half) rather than opposed to it. Name which sense the example is in.

### M3 — P083 overstates that norms are "never deduced from the source text"
- Where: `principles/principles.yaml` P083; `skills/descriptive-studies-and-translational-norms/SKILL.md` step 10 (L72), anti-pattern (L98). Grounding C00470 vs C00472.
- Problem: P083 follows only C00472's absolute phrasing ("norms do not emerge from a source text") and drops sibling C00470 (same source/section): norms are identified "only by reference to **a corpus of source and target texts**" — Toury's actual coupled-pairs method is ST–TT *comparative*. As written P083 would misdirect the reviewer to reject any norm claim that uses ST–TT comparison as evidence, which is the core Toury methodology.
- Fix: rewrite P083 to "identified from a representative corpus of source-and-target text pairs (not projected from the source text's own features, an idealized target system, or a generic target-text collection)" — preserving the real distinction without denying ST–TT comparison as the evidentiary base.

### M4 — P076 procedure step silently truncated (unexecutable as written)
- Where: `skills/descriptive-studies-and-translational-norms/SKILL.md:70`.
- Problem: step 8 reads "Investigate operational norms through the corpus at two levels (P076)" but never names the two levels; the matricial/textual detail only appears 26 lines later in the anti-pattern (L96). An agent running the Procedure top-to-bottom cannot perform the step — "two levels" names nothing.
- Fix: restore the split into the procedure line: "…at two levels: matricial (omissions, additions, substitutions, transpositions in distribution) and textual (collocation, speech treatment, title conventions) (P076)."

### M5 — faithfulness-report does not cover `knowledge_partition.always_on`; real over-claims live there, and ledger/changelog claim full coverage
- Where: `reports/faithfulness-report.yaml` (17 entries: only quality_bar/forbidden_behaviours/when_to_use/outputs.primary_format/precedence) vs `provenance-ledger.md:6-10` + `CHANGELOG.md:47-48`.
- Problem: zero faithfulness entries for `knowledge_partition.always_on` (the 12 skill-scope paragraphs = the bulk of behavioural content, all 150 principles), `handoff_rules`, `outputs.modes`, `examples`. The ledger/changelog assert "every load-bearing rule graded WITHIN_SCOPE" and "no orphan field" — untrue at the artifact level. Independent review of that unreviewed section surfaced actual strength issues (see S5/S6/S7 below), confirming the gap is not cosmetic. A reader trusting the ledger would wrongly believe Tier-2 faithfulness coverage occurred.
- Fix: extend `faithfulness-report.yaml` with a verdict per `always_on` paragraph, each `handoff_rules` item, `outputs.modes`, and the 2 `examples`; correct ledger/changelog wording for any entry not WITHIN_SCOPE.

## should-fix

### S1 — profile body-size Phase-8 WARNING is real (~947w vs 800 WARN / 1000 FAIL)
- Where: `profile.yaml` body fields (role/when_to_use/quality_bar/…).
- Problem: confirmed genuine overage; r1's fix added a `when_to_use` bullet without trimming, moving 941→947w — only ~53w headroom before hard FAIL. Fix: trim `quality_bar` (~156w, heaviest) and `role` (~123w) to land under 800w.

### S2 — adapter frontmatter `description` carries only 1 of 6 `when_to_use` triggers
- Where: `.claude/agents/generated/translation-quality-reviewer.md:3` (and `adapters/claude-code/…`). [profile-reviewer + ai-agent-eng]
- Problem: the routing signal an orchestrator reads before opening the file names only "a translation/draft assessed for quality," omitting corpus-method rigour, translationese-as-proxy, overt/covert-equivalence, Russian-field/Chinese-Europeanization, error-discipline/genre. Narrow requests risk under-invocation. Fix: front-load 2–3 highest-frequency triggers, mirroring the role's opening clause; re-export.

### S3 — `when_to_use` under-covers the 12-skill surface; CHANGELOG overclaims a split that didn't happen
- Where: `profile.yaml:18-31`; `CHANGELOG.md:32-33`. [profile-reviewer + ai-agent-eng nice]
- Problem: (a) no trigger routes to `cognition-pragmatics-and-contrastive-evidence`. (b) bullet 5 still fuses "Russian-field multifactorial … or Chinese Europeanization," and bullet 6 fuses error-discipline + genre/accessibility, despite the changelog claiming v1.1.0 "split the Russian/Chinese trigger." Fix: consolidate a weak trigger to add a cognition/pragmatics bullet, or split bundled bullets; correct the CHANGELOG to stop claiming a split that wasn't done.

### S4 — over-claims inside the un-faithfulness-reviewed `always_on` section (corroborate M5)
- Where: `profile.yaml` `knowledge_partition.always_on`. [faithfulness-reviewer]
  - P082 (applied-corpus-tools): HEDGING_REMOVED — drops "treat limited findings as hypotheses for further testing," contradicting the package's own `quality_bar[4]`. Fix: restore the hedge.
  - P058 (Russian-corpus): SCOPE_BROADENED — "metadata-rich corpora recording direction/mode/delivery" applied package-wide, but P058 `applies_when` is Polish-Russian/Russian-Polish only. Fix: scope the sentence or re-cite.

### S5 — `quality_bar[3]` extends register feature-cluster method onto cultural filtering
- Where: `profile.yaml` `quality_bar[3]` (P042/P069/P056/P116/P137). [faithfulness-reviewer] SCOPE_BROADENED.
- Problem: P116's "co-occurring feature clusters against a baseline" is scoped to register/orality/involvement, not cultural filtering; no cited principle states a feature-cluster method for cultural filtering. Fix: split the clause so the cluster requirement attaches only to register.

### S6 — no S-universal/T-universal distinction; P121 isolation method presented as universal for all of P001
- Where: `principles/principles.yaml` P001, P121; `skills/translation-universals-and-the-third-code/SKILL.md` step 6. [descriptive]
- Problem: P121's monolingual-comparable design tests T-universals (simplification, normalization), but P001 lists explicitation (an S-universal, evidenced via parallel ST–TT corpora). Presenting P121 as the general method risks demanding the wrong corpus type for explicitation claims. Fix: add the S/T split and route explicitation-type claims to parallel-corpus evidence.

### S7 — House source-comparative equivalence (P006/P030/P038/P059) vs Toury target-orientation (P034): no scoping rule
- Where: `overt-covert-translation-and-equivalence` vs `descriptive-studies-and-translational-norms`. [equivalence]
- Problem: two opposed theory commitments presented flatly as criteria the same reviewer applies, with no principle saying which frame governs which task. A quality claim resting on a corpus-descriptive norm argument straddles both. Fix: add a scoping note — House's ST-comparative model governs adequacy/quality-assessment against a brief; Toury's target-orientation governs descriptive norm-reconstruction and is not licence to drop the P006/P059 ST-profile comparison when a quality claim is adjudicated.

### S8 — House genre→translation-type heuristic missing (sci-tech = default covert)
- Where: `overt-covert-translation-and-equivalence` skill; P005–P011, P062, P093. [technical]
- Problem: House treats scientific/technical/instructional/journalistic/tourist genres as prototypical **covert** candidates (function domestically, cultural-filter units/formality/imperatives), overt reserved for source-event-anchored texts. The package captures classification *criteria* but never this genre default → a technical manual could be misclassified overt (over-preserving source markedness per P005). Fix: add/extend P062/P093 to state the genre default (portable-function genres → covert absent a specific reason to go overt).

### S9 — register skill Field-thin for sci-tech; heavily skewed to institutional/persuasive Tenor
- Where: `skills/register-field-tenor-mode-analysis/SKILL.md`. [technical + agent-skills nice]
- Problem: 6 of 16 procedure steps are mission-statement/exhortation-specific (P010, P070–P074); only P129 briefly names "technical terminology," with no nominalization density, passive ratio, hedging/modality, or technicality gradient — the standard Field markers for sci-tech register. Fix: add a Field-specific technical-marker step-cluster, or scope it out with an explicit defer to `technical-translation-advisor`.

### S10 — P020 phrased as first-person action directive ("Prioritize corpus construction …")
- Where: `.claude/agents/generated/translation-quality-reviewer.md:38`; `profile.yaml` (P020 always_on). [ai-agent-eng]
- Problem: reads as an action the agent takes rather than a review criterion/recommendation. Read/Grep/Glob makes literal execution impossible, so the risk is a misleading self-description. Fix: rephrase advisory ("When advising on Russian-field corpus design, recommend prioritizing …"), matching adjacent P019/P029 phrasing.

### S11 — handoff: corpus design (in-scope) vs corpus engineering (handed off) boundary unstated
- Where: `.claude/agents/generated/…:148-153`; `profile.yaml:93-97` handoff_rules. [ai-agent-eng]
- Problem: reviewer has deep in-scope authority over corpus *design* (P003/P050/P078/P056) but hands off "corpus engineering," with no rule separating the two; a borderline request (raw vs normalized frequency) has nothing to route by. Fix: add a clause — in scope: which corpus type/controls fit the question; out of scope: building the pipeline or its statistical/software implementation.

### S12 — "leveling out"/convergence candidate universal absent from P001
- Where: `principles/principles.yaml` P001. [descriptive + equivalence nice]
- Problem: standard Baker-associated set is simplification/explicitation/normalization/**leveling out**; convergence appears nowhere in the package. May be source-faithful (Baker formalized it in 1996, not the 1993 paper distilled here). Fix: check Baker 1993 / Kruger et al. 2011; add if present, else note in the reference index that P001's list is non-exhaustive.

### S13 — repeated boilerplate inflates all 12 skills
- Where: every `skills/*/SKILL.md` `## Output` / `## References` / `## Provenance` / second `## Inputs` bullet. [agent-skills]
- Problem: the Output disclaimer, References sentence, Provenance framing, and one Inputs bullet are copy-pasted verbatim across 12 skills with zero skill-specific signal (only principle-id lists differ). Fix: collapse to a one-line-per-skill reminder + pointer to a shared note.

### S14 — procedure steps thinner than their own anti-patterns (pattern beyond M4)
- Where: `descriptive-studies…` L66/L67; `error-analysis…` L81/L87; `corpus-design…` L81. [agent-skills]
- Problem: bare-headline procedure steps whose checkable specifics only surface in the anti-pattern bullet. Fix: fold the operative nouns back into each numbered step so it's independently actionable.

### S15 — uneven triage/grouping lead-in on large procedure lists
- Where: `corpus-design-and-methodology` (15 steps), `register-field-tenor-mode-analysis` (16), `descriptive-studies-and-translational-norms` (14) lack the routing lead-in that 3 comparably large siblings have. [agent-skills]
- Fix: add a one-sentence triage/grouping lead-in, consistent with the proven siblings.

## nice

- **N1** No persisted quote-scan artifact under `reports/` for a 5/5 `distillation-only` package (scan passes inline, but not archived). [profile-reviewer] Fix: persist `quote_scan` output under `reports/`.
- **N2** P002 vs P139: add a one-line cross-ref that an automatic "translationese" classifier flag ≠ diagnosed translationese under P139 — may be third code (P139) or normal translated-language patterning (P114). [equivalence] (folds into M2.)
- **N3** No dedicated terminology-consistency error class in the error typology (P090); industry LQA (MQM/DQF/SAE J2450) treats it separately. Add a one-line defer to `technical-translation-advisor`. [technical]
- **N4** Contract-as-overt worked example under-hedged: a contract meant to be legally operative in the target jurisdiction is a strong *covert* candidate. Add "…unless the contract must remain legally tied to its foreign jurisdiction." [technical]
- **N5** P051 names Russian interpreting corpora (UN Web TV, SIREN, COINCOUT) with no currency caveat; will age past the 2023 source. Add "verify current availability/access." [descriptive]
- **N6** `register-field-tenor-mode-analysis` when-to-use triggers are institution-text-specific; add one general-case bullet so general register questions match. [agent-skills] (overlaps S9.)
- **N7** `references/translation-quality-principles-index.md` frontmatter `claims:` truncates at C00019 while the body groups ~713; sibling evidence-notes uses `claims: []`. Reader following a skill's reference pointer lands on an apparently-truncated manifest. [agent-skills]

MUST_FIX_COUNT: 5
