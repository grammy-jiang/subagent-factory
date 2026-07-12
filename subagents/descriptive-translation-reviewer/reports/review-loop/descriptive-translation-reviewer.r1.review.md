# Review — descriptive-translation-reviewer (round r1)

Package: `subagents/descriptive-translation-reviewer/` · profile `agent_version: 1.8.1` · Tier 2 · 180 principles / 12 skills / 2 references.

## Deterministic gates (STEP 1)

| Gate | Result |
|------|--------|
| `validate_generated_package` | **VALIDATION PASSED** (0 FAIL) |
| `quote_scan` | PASS — no verbatim quotation |
| truncation `…` grep (skills + adapter) | no hits |
| adapter invariant severed-parenthetical grep | no hits |

No deterministic FAILs.

## Consolidated findings (deduped, most-severe first)

### MUST-FIX

**MF-1 — Operating invariants phrased as translation-PRODUCTION instructions, in tension with the review-only role** (agent design)
- Where: `.claude/agents/generated/descriptive-translation-reviewer.md` lines 21–306 (`## Operating invariants`); canonical source is `profile.yaml` (principle renderings, e.g. P045, P069, P063, P015, P036, P037, P072, P119, P120).
- Problem: The highest-authority "must-hold" section reads item-by-item like a translator's playbook ("Prepare a verse translation by…", "Subtitle within… following…", "Adjust for the audience…"), not a reviewer's checklist. ~280 lines of production-imperative content are held in check only by the single Role-paragraph disclaimer and the Forbidden-behaviours list that bracket them. Over-reach / authority-creep risk against the declared read-only reviewer boundary.
- Fix: In `profile.yaml` / the generator, prefix each principle rendered into a review-type agent with a review-framing verb ("Check whether the translation…", "Verify that the rendering…") instead of the raw imperative; OR at minimum add a salient boundary reminder immediately before the `## Operating invariants` heading ("Apply every invariant below as a criterion for judging someone else's translation — never as a step to perform yourself"). Re-export the adapter. Template/rendering-level fix — does not touch faithfulness-reviewed principle text.

**MF-2 — `when_to_use` covers only 7 of 12 skills (~42% of corpus has no charter-level trigger)** (skill authoring)
- Where: `profile.yaml` lines 17–40 (`when_to_use`).
- Problem: No top-level trigger phrase points to `meaning-signification-and-equivalence-critique` (11 princ), `culture-ideology-power-and-rewriting` (20), `hermeneutics-and-the-limits-of-translatability` (19), `translation-procedures-and-shifts` (10), `translation-quality-and-applied-studies` (15) — ~75/180 principles. A caller wanting ideology/institutional critique, hermeneutic/untranslatability reasoning, Vinay–Darbelnet procedure-label disputes, or QA-method soundness finds no charter-level route, though dedicated skills exist.
- Fix: Add 2–3 `when_to_use` bullets covering (a) ideology/institutional/reception critique, (b) hermeneutic grounding / untranslatability claims, (c) Vinay–Darbelnet procedure/shift naming disputes, (d) soundness of a translation-quality-assessment method or applied/empirical TS study — mirroring vocabulary already in those skills' descriptions.

**MF-3 — `tests/golden-tests.yaml` `profile_version` stale vs `agent_version` (recurrence of a previously-fixed defect)** (release readiness)
- Where: `tests/golden-tests.yaml:4` (`profile_version: 1.8.0`) vs `profile.yaml:4` (`agent_version: 1.8.1`).
- Problem: The v1.8.1 adversarial-verify fix bumped `agent_version` + CHANGELOG but did not re-stamp `golden-tests.yaml`. Exact defect class already fixed once at v1.7.0 (ledger MF-1, stale 1.5.0→1.7.0). No validator checks this drift, so it is silent. `tests/test-results.md:7` verdict is likewise still stamped v1.8.0 (see SF-3).
- Fix: Re-stamp `golden-tests.yaml` `profile_version` to `1.8.1`; add a review-loop checklist item (or validator) so every version bump re-stamps all versioned test/report artifacts.

### SHOULD-FIX

**SF-1 — P020 applied as an unscoped universal review criterion but states a contested minority stance** (domain: quality)
- Where: `principles/principles.yaml` P020 (`applies_when: []`); operationalized in `skills/domestication-foreignization-and-visibility/SKILL.md` Procedure step 1 + matching anti-pattern.
- Problem: P020's second clause ("reject reproduction of meaning as its aim") is Benjamin/de Man's avant-garde position, not domain consensus, and conflicts with the meaning-reproduction goal the rest of the package treats as normal (P044, P125, P160, P179). Sibling P034 is correctly scoped to literary/poetic/philosophical texts; P020 is not, yet the skill runs it as a check on any reviewed translation — a "prefer X here → always X" overclaim the package's own forbidden-behaviours warn against.
- Fix: Add `applies_when: [literary/poetic/philosophical/experimental-deconstructive translation where mode of signification, not propositional content, is the object of fidelity]` to P020 (match P034); rewrite skill step 1 to keep "fluency is not proof of quality" general but gate "reject reproduction of meaning" behind a text-type condition.

**SF-2 — Worked example conflates Nida "dynamic equivalence" with Newmark/Reiss frameworks** (domain: equivalence)
- Where: `profile.yaml` operative-text worked example (~lines 234–245), cites P059/P129/P062 alongside "dynamic."
- Problem: "Dynamic equivalence" is specifically Nida's term; Newmark's communicative and Reiss's operative-adaptive methods are parallel-but-distinct. Example risks reading as if the three are interchangeable, though the principles layer (P121/P167) carefully treats them as a family.
- Fix: Name the operative orientation in Reiss/Newmark's own vocabulary ("adaptive method"/"communicative translation") and cite "dynamic equivalence" only as the Nida-family analogue, or add a one-clause "parallel frameworks, not one shared term" caveat.

**SF-3 — `tests/test-results.md` self-check verdict still stamped v1.8.0** (release readiness)
- Where: `tests/test-results.md:7`.
- Problem: Same root cause as MF-3 — v1.8.1 fix did not re-verify/re-stamp the recorded self-check verdict.
- Fix: Re-stamp to v1.8.1 or note it was superseded by `reports/review-loop/…verify2.md` and is unchanged.

**SF-4 — `outputs.primary_format` worded as review-mode-specific but presented for all three modes** (release readiness)
- Where: `profile.yaml` lines 48–50.
- Problem: "per finding… correction… next step" matches `review` mode but not `advise` (single recommendation) or `compare` (side-by-side, brief-weighted recommendation). `minimum_useful_output` already distinguishes per-mode; `primary_format` overstates uniformity.
- Fix: Reword to the genuinely mode-agnostic common thread ("a structured critique that names the governing principle(s) and states a residual trade-off, never a bare verdict"); leave mode-specific shape in the `modes` list.

**SF-5 — `provenance-ledger.md` orphan-field exception list omits `handoff_rules[2]`** (release readiness)
- Where: `provenance-ledger.md` lines 8–16.
- Problem: The enumeration of intentionally-uncited fields omits `handoff_rules[2]` (sibling-routing bullet), whose uncited-by-design status is documented only in the faithfulness report. An auditor reading the ledger alone would flag it as an orphan.
- Fix: Add `handoff_rules[2]` to the ledger's opening enumeration.

**SF-6 — No explicit temporal-currency boundary for the classical/pre-2016 grounding** (domain: technical)
- Where: `profile.yaml` role / `source_of_truth_policy`; package-wide (sources Munday 2016, Venuti ed. 2012, Toury 1995).
- Problem: Grounding stops ~2016 and largely anthologizes 1980s–2000s essays; nothing flags that post-2016 corpus methodology, NMT-era norm shifts, and MQM/DQF error typologies are out of scope. Bears on the "current" prong.
- Fix: Add one sentence noting the corpus is foundational/classical theory (through ~2016) and post-2016 developments are out of grounding.

**SF-7 — Review-only disclaimer + full Anti-patterns mirror inflate every SKILL.md body** (skill authoring)
- Where: all 12 `skills/*/SKILL.md` — disclaimer repeated in Purpose + Output (+ sometimes Anti-patterns lead); Anti-patterns is a near-1:1 negation of every Procedure step (bodies ~1200–1900 words); closing Provenance prose re-enumerates IDs already in frontmatter.
- Problem: Each principle stated ~3× per file; real reference layer (`references/*.md`) exists but bodies don't defer the long tail to it — works against progressive-disclosure guidance.
- Fix: State the review-only boundary once (Purpose); trim Anti-patterns to the 5–8 highest-impact/most-confusable failure modes and push exhaustive per-principle coverage into the reference index; shorten closing Provenance to a one-line source citation.

### NICE

- **N-1** (agent design): ~100 dense must-hold invariants sit between the two boundary-defining sections, diluting them; consider demoting some to skill-level guidance. Folds into MF-1 remediation. — adapter lines 21–306.
- **N-2** (skill authoring): 4 profile worked examples never exercise the two largest skills (`culture-ideology-power-and-rewriting` 20 princ, `descriptive-method-and-translational-norms` 21). Add a norms/method example and an ideology-critique example. — `profile.yaml` lines 205–256.
- **N-3** (skill authoring): large flat procedures (hermeneutics 19 steps, culture-ideology 21 steps) lack a triage/decision-tree entry point; add a 3–5 line "if X-type text → steps …" note.
- **N-4** (skill authoring): `translation-procedures-and-shifts` + `equivalence-orientations-and-effect` omit the review-only clause from the frontmatter `description` (other 10 include it); add for consistency.
- **N-5** (domain: equivalence): P059 skill step 1 compresses Newmark's causal chain — "illusory equivalent effect" is his reason to *reserve* semantic translation, not the reason communicative translation fits the majority; split the "because" clause per branch. `skills/equivalence-orientations-and-effect/SKILL.md` step 1.
- **N-6** (domain: equivalence): P105 `applies_when` reads as a fixed either/or recipe in isolation, mild tension with the "open set, not fixed recipe" quality bar; soften with "typically… weighed against the brief, not by rule."
- **N-7** (domain: quality): functionalist cluster omits Nord's "function plus loyalty" principle (the standard ethical safeguard on skopos freedom); add if Munday's chapter covers it, else a follow-up MAP pass. `skills/text-type-skopos-and-the-brief`.
- **N-8** (domain: quality): Toury source cited as if "The Nature and Role of Norms in Translation" were a standalone 1995 book — it is ch.1 of *Descriptive Translation Studies and Beyond* (1995), also anthologized in the Venuti Reader (possible overlap). Correct citation / check duplication. `profile.yaml` sources.
- **N-9** (faithfulness): `examples[0]` generalizes P176 (scoped to *verse* translation) to any literary review; cushioned by co-cited P088/P020 so not should-fix. Add "verse" qualifier or drop P176 from that sentence's citations.
- **N-10** (domain: technical): P056 uses Quine's period example "Neutrinos lack mass" — neutrinos now known to have nonzero mass; add a parenthetical marking it as Quine's illustrative case, not current physics. `principles.yaml` P056 + hermeneutics skill step 4.
- **N-11** (domain: technical): P069 subtitling figures (38 CPL, ~6s) stated more precisely than the field standardizes (Netflix ~42 CPL etc.); already hedged, optionally soften to a range. `principles.yaml` P069 + register skill step 10.
- **N-12** (release readiness): `role` is one dense em-dash-heavy paragraph; splitting risks regressing exporter-clip tuning — polish only with adapter re-export verification. `profile.yaml` lines 8–16.
- **N-13** (release readiness): `when_to_use[2]` phrased around caller intent rather than a concrete scenario; minor wording tighten. `profile.yaml` lines 22–23.

MUST_FIX_COUNT: 3
