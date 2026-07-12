# translation-quality-reviewer — review loop round 3

Consolidated review of `subagents/translation-quality-reviewer/`. Sources: 3 deterministic gates
(all PASS) + 7 reviewer lenses (4 factory: agent-skills, profile, faithfulness, ai-agent-engineering;
3 domain: translation-equivalence, descriptive-translation, technical-translation). Findings deduped
across lenses, most-severe first.

## Deterministic gates (all PASS — 0 must-fix)

- `validate_generated_package`: VALIDATION PASSED (Phase-8 self-check WARNING only; all 12 skills + 2
  refs authored; adapter in sync; tier 2 consistent).
- `quote_scan`: PASS — no verbatim quotation.
- Truncation gates (`…` ellipsis, severed invariant parenthetical): no hits.

## must-fix

### MF1 — Sibling routing collision with `descriptive-translation-reviewer` (unresolved)
- **Where:** `profile.yaml` `when_to_use[1]` / `when_not_to_use[0-2]`; installed adapter frontmatter
  `description` (`.claude/agents/generated/translation-quality-reviewer.md:3`); mirror in
  `descriptive-translation-reviewer`.
- **Severity:** must-fix. **Lenses:** profile-reviewer (MF#1) + ai-agent-engineering (F1) — deduped.
- **Problem:** Both siblings' frontmatter `description` opens "A reviewer of translations…" and ends with
  the **verbatim-identical** "Not for: …the finished or revised translation produced end to end."
  `when_not_to_use[0-2]` are word-for-word identical between the two profiles, and `when_to_use[1]`
  ("corpus-based analysis, universals, or norm claim needs checking for method rigour and faithfulness")
  collides with descriptive-reviewer's own `when_to_use[2]`. A router/caller cannot tell which reviewer
  owns "review this norm claim" / "review this translation." The third sibling
  `translation-equivalence-advisor` already solves this — its `when_not_to_use[0]` names all three siblings
  and routes by axis; this package does not reciprocate.
- **Fix:** Add an explicit disambiguating bullet naming the boundary — quantitative/corpus-empirical
  norm & universal review (frequency evidence, corpus design, comparability controls, ST-vs-TT register
  profiling) → here; qualitative translator-visibility / domestication-foreignization / single-text norm
  critique → `descriptive-translation-reviewer` — matching the `translation-equivalence-advisor` pattern,
  and add the mirror redirect to descriptive-reviewer. Re-export so the adapter `description` front-loads
  the distinguishing corpus/empirical terms instead of the generic clause.

### MF2 — Faithfulness-report coverage: miscount + orphaned `when_to_use[5]`
- **Where:** `reports/faithfulness-report.yaml`; `provenance-ledger.md:47`; `CHANGELOG.md:26-29`.
- **Severity:** must-fix. **Lens:** profile-reviewer (MF#2).
- **Problem:** Ledger + CHANGELOG claim "40 findings"; `rule_ref:` count in the report is **36**. Worse,
  `profile.yaml` has 6 `when_to_use` bullets but the report grades only `when_to_use[0..4]` —
  **`when_to_use[5]` has no faithfulness verdict at all** (orphaned load-bearing field, violates the
  every-field-traceable rule in rights-and-quotation-policy).
- **Fix:** Add `rule_ref: when_to_use[5]` with a source-grounded verdict; correct the count in ledger +
  CHANGELOG to the true value; re-verify no other `rule_ref` is missing before re-asserting full coverage.

### MF3 — P083 norm-reconstruction safeguard dropped in profile rules (SCOPE_BROADENED)
- **Where:** `profile.yaml` `quality_bar[5]` ("norms reconstructed from the corpus") and
  `knowledge_partition.always_on[7]` ("norms reconstructed from recurrent corpus regularities"); cross-ref
  `reports/faithfulness-report.yaml` entry for `always_on[7]`.
- **Severity:** must-fix. **Lens:** faithfulness-reviewer (MF, SCOPE_BROADENED).
- **Problem:** P083 (confidence high) is restrictive: a norm is observable **only through comparison across
  source-and-target text pairs — not from the source alone, an idealised target system, or a generic
  target-only collection.** Both profile rules drop the source-and-target-pairing requirement, saying only
  "from the corpus" — broad enough to license exactly the malpractice P083 forbids (deriving a "norm" from
  a target-only/generic corpus). Compounding: the faithfulness-report entry claims the rule reads
  "source-and-target corpus (P083 as corrected)" — but that phrase is **not in the profile text**; the
  report grades a correction that was never applied, so its accept_with_note verdict is not valid evidence.
- **Fix:** Reword both rules to state the constraint precisely, e.g. "norms reconstructed only from a corpus
  of source-and-target text pairs, never from a generic or target-only collection (P083)." Then re-verify
  and correct the faithfulness-report entry to reflect the actual profile text.

### MF4 — Toury norm taxonomy incomplete: initial + preliminary norms entirely absent
- **Where:** `principles/principles.yaml` P076 (only norms-structure principle);
  `skills/descriptive-studies-and-translational-norms/SKILL.md` step 8.
- **Severity:** must-fix. **Lens:** descriptive-translation-reviewer (MF#1).
- **Problem:** Toury's framework has three levels — **initial norm** (adequacy-toward-source vs
  acceptability-toward-target orientation), **preliminary norms** (translation policy + directness/relay),
  and **operational norms** (matricial + textual). P076 captures only the operational level. No principle
  in the 150 addresses adequacy/acceptability orientation or policy/directness. A caller presenting a norm
  claim at either missing level gets no principle — the reviewer silently drops the category or wrongly
  applies the operational (matricial/textual) lens to a claim that isn't about distribution or formulation.
- **Fix:** Extend P076 (or add a sibling principle) naming the initial norm and preliminary norms explicitly,
  reconstructed by the same evidentiary discipline P083 requires (patterned corpus/paratextual behaviour,
  not asserted), so a claim is first placed at the correct level before operational criteria apply.

### MF5 — Provenance ledger factually false about `when_to_use` tagging
- **Where:** `provenance-ledger.md:9-10` vs `profile.yaml:17-29`.
- **Severity:** must-fix. **Lens:** profile-reviewer (MF#3).
- **Problem:** Ledger states "Descriptive fields — `role`, `when_to_use`, `inputs`, `outputs` — carry no
  inline tags, per repo convention." False for the shipped profile: every `when_to_use` bullet carries
  inline principle citations (e.g. `(P006, P001, P002)`). The ledger misrepresents the actual provenance
  mechanism, undermining it as an accurate record.
- **Fix:** Correct the ledger to state `when_to_use` does carry inline principle tags (and confirm the tags
  resolve against `principles.yaml`), or strip the tags for consistency if "no inline tags" is meant to hold.

## should-fix

- **SF1 — P120 conflation (HEDGING_REMOVED).** `knowledge_partition.always_on[10]` fuses P120's two
  conditional alternatives ("stand by juxtaposition **when natural**" OR "choose connectors matched to
  progression/contrast/adjustment instead of English-style and-linking") into the near-contradictory "stand
  by juxtaposition with connectors," dropping the "when natural" condition. *(faithfulness)* Fix: restore the
  two-clause either/or structure with the condition.
- **SF2 — House Mode/Participation mischaracterized as "standard Hallidayan register split."**
  `skills/register-field-tenor-mode-analysis/SKILL.md` anti-patterns bullet excuses Participation-under-Mode
  as valid under "a standard Hallidayan register split" — but in canonical SFL, Tenor covers participant
  relations; House's Participation-under-Mode traces to the Crystal & Davy / Gregory & Carroll stylistics
  tradition, not standard Halliday. Risks excusing a genuine misclassification. *(technical-translation)* Fix:
  replace with "or House's original (1977) model, adapted from the Crystal & Davy/Gregory & Carroll framework."
- **SF3 — Anti-pattern sections are mechanical 1:1 negations of every Procedure step.** All 12 SKILL.md files
  restate each procedure step as a negated anti-pattern, ~doubling body length for no new signal (works
  against concise/moderate-detail guidance P088/P059 and selective good/bad pairing P046). *(agent-skills)* Fix:
  collapse each step+anti-pattern into one line, or trim to the most-often-misapplied subset.
- **SF4 — Missing DTS-vs-TQA reconciliation rule.** Package blends Toury's non-evaluative DTS (source = "fact
  of departure") with House's evaluative TQA; the two can license opposite verdicts on the same shift with no
  routing/reconciliation rule. *(translation-equivalence)* Fix: add a `precedence` / skill line stating the norms
  lens governs descriptive/corpus tasks (not single-text evaluative TQA), and surface disagreement explicitly
  when both apply.
- **SF5 — Missing candidate universals & refinements.** P001 omits Baker's "leveling out"/convergence with no
  non-exhaustiveness caveat; the "unique items hypothesis" (Tirkkonen-Condit) is absent from the universals
  cluster. *(descriptive-translation)* Fix: verify against Baker 1993 / Kruger et al. 2011 source pack; add named
  principles/steps if covered, else add explicit non-exhaustiveness caveat + reference-index note.
- **SF6 — P083 omits Toury's extratextual/paratextual corroboration.** P083 requires ST–TT textual comparison
  but gives no principle for weighing prefaces/editorial statements as (lower-reliability) corroboration.
  *(descriptive-translation)* Fix: add a clause — extratextual statements may corroborate but never substitute for
  textual/corpus regularity evidence.
- **SF7 — Missing industry-metric scope boundary.** Error-analysis skill is entirely House's academic
  overt/covert model; no note distinguishing it from severity-scored industry frameworks (MQM, ISO 17100/18587,
  LISA QA, SAE J2450) a caller may assume are covered. *(technical-translation + translation-equivalence)* Fix: add
  a `when_not_to_use` / role note that industry MQM/DQF-style severity scoring and MT quality-estimation metrics
  (COMET/BLEURT/GEMBA) are out of scope.
- **SF8 — Duplicated / thin `when_to_use` triggers.** `when_to_use[1]` duplicates `[2]` ("corpus-based analysis…
  checked for quality/rigour"); no bullet carries trigger keywords for the register (Field/Tenor/Mode) or
  applied-corpus-tools (keyword/concordance/collocation) skills. *(profile-reviewer)* Fix: merge the duplicate
  (freeing a slot for MF1's disambiguation) and add explicit register + corpus-tools trigger language.
- **SF9 — Adapter `description` truncated mid-clause.** The broadened `when_to_use[0]` ("…is assessed for
  quality") drops the "corpus-method rigour, or translationese-as-proxy" terms that were the point of the S2 fix;
  the router never sees them. *(profile-reviewer)* Fix: inspect the description-generation length budget /
  fragment-selection in the export template so the broadened trigger reaches the frontmatter; re-export.
- **SF10 — Body trimmed exactly to 800-word WARN threshold.** `provenance-ledger.md:54` states the body was
  trimmed "to 800 words" = the exact WARN floor; zero headroom risks re-tripping the Phase-8 WARNING on next edit.
  *(profile-reviewer)* Fix: re-run validate, confirm safely below 800, trim further if at/over.
- **SF11 — Duplicated cross-skill rule (P002) risks drift.** `translation-universals-and-the-third-code` step 7
  and `error-analysis-and-evaluation-discipline` step 10 both independently restate "a translationese
  classifier flag is not a quality proxy" in near-identical wording with no cross-reference. *(agent-skills)* Fix:
  keep the canonical treatment in the universals skill; shorten the error-discipline copy to a pointer.

## nice

- **N1** — Chesterman's S-universal/T-universal split is functionally implemented in
  `translation-universals-and-the-third-code` step 6 but never named; add the term.
  *(descriptive + equivalence)*
- **N2** — P116 register-cluster analysis is Biber-style Multi-Dimensional Analysis but MDA is unnamed; add a
  one-clause pointer. *(equivalence)*
- **N3** — Core concepts (Frawley's third code, Toury's norms, Baker/Blum-Kulka universals, Chesterman) lack
  scholar attribution in the reference index; add attributions to enable citation cross-check. *(descriptive)*
- **N4** — `quality_bar[3]` cites P056 (Russian-field multifactorial modelling) to ground a cultural-filter
  source-to-target claim; P056 doesn't support it. Replace with P032/P047/P007/P137. *(faithfulness + technical)*
- **N5** — `when_not_to_use[2]` "translation quality is probabilistic and brief-dependent" is stronger than
  P061's "non-absolute and subjective"; soften "probabilistic." *(faithfulness)*
- **N6** — Verify "superstructural" three-level split (P021) is House's own term vs a van Dijk & Kintsch source
  cited within House; attribute explicitly at next faithfulness pass. *(technical)*
- **N7** — Adapter frontmatter `Not for:` carries only 1 of 4 `when_not_to_use` exclusions (template-wide, not
  package-specific); compress a second clause if budget allows. *(ai-agent-engineering)*
- **N8** — Larger skills (overt-covert, error-analysis, cultural-filtering, register) keep full per-principle
  prose inline instead of offloading detail to the two existing reference files via specific in-body pointers.
  *(agent-skills)*
- **N9** — `register-field-tenor-mode-analysis` frontmatter ("mission statements…") vs body Purpose
  ("persuasive and missionizing texts") word the same referent two ways; align. *(agent-skills)*

MUST_FIX_COUNT: 5
