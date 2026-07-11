# Review Loop — descriptive-translation-reviewer — Round 4

Consolidated from deterministic gates + 7 reviewer lenses (agent-skills, profile, faithfulness,
ai-agent-engineering, translation-equivalence, translation-quality, technical-translation).
Findings deduped across lenses; most-severe first.

## Deterministic gates (all PASS)

- `validate_generated_package` → **VALIDATION PASSED** (0 fail, all tier-artifacts + adapter-quality + stale OK).
- `quote_scan` → **PASS** (no verbatim quotation).
- Ellipsis truncation grep (skills + adapter) → **no hits**.
- Adapter invariant severed-parenthetical grep → **no hits**.

No deterministic FAILs → 0 must-fix from gates.

---

## must-fix

| # | Where | Problem | Fix |
|---|-------|---------|-----|
| 1 | `.claude/agents/generated/descriptive-translation-reviewer.md:3` (frontmatter `description`); source `profile.yaml` `when_not_to_use[0]` L28 | Router-facing `description` "Not for" clause is truncated to a bare noun with no verb/resolution: `...Route to \`translation-equivalence-advisor\` when the linguistic-equivalence mechanism`. Sibling adapters end on complete clauses. This is the field Claude Code + operator use to dispatch, so a cut-off clause degrades when-to/when-not routing. Root cause: `_clean_clause` 85-char clip lands on a word boundary with no complete-thought check, and `when_not_to_use[0]`'s first comma falls past the clip. (agent-engineering=must-fix; profile-reviewer flagged same as nice — kept must-fix: it's the dispatch field and reads as an accidental cut.) | Front-load `when_not_to_use[0]` so a complete, self-contained clause sits within ~85 chars before its first comma (e.g. "Route to \`translation-equivalence-advisor\` for word/collocation/grammar equivalence mechanics"), then re-run `cli export`. Optionally harden `_clean_clause` to require a sentence-final boundary (comma/semicolon/dash) or drop the piece rather than emit a bare-noun fragment. |

---

## should-fix

| Where | Problem | Fix |
|-------|---------|-----|
| `tests/golden-tests.yaml` header | `profile_version: 1.2.0` stale — profile now v1.3.0; `when_to_use[2]` and `when_not_to_use[0]` reworded in v1.3.0, so version claim no longer proves re-check. | Bump header to 1.3.0, re-verify GT-001/NR-001/NR-002 vs reworded triggers, record re-stamp in ledger/CHANGELOG. |
| `tests/golden-tests.yaml` (coverage gap) | The 3-way sibling-routing clause `when_not_to_use[0]` — reworked across 3 straight rounds — has zero negative-routing test. NR-001/NR-002 cover `[1]`/`[2]` only. | Add negative-routing test where prompt is squarely a word/collocation/grammar equivalence question (routes to `translation-equivalence-advisor`, not here). |
| `profile.yaml` body size | ~906 words (role+when+inputs+outputs+modes+quality_bar+forbidden+handoff+precedence), up from ~851 at v1.2.0; ~55 words/round growth trends toward 1000-word FAIL. | Apply deferred S7 (trim heavy skills / profile prose) now; trim in the same round any field is broadened so net body size doesn't grow monotonically. |
| `profile.yaml` `inputs.required` | Single omnibus bullet bundling 5 asks (source+target, orientation, strategy, brief, quality claim) — satisfiable partially yet judged "input provided". | Split into discrete list items so missing-context detection has per-item checks. |
| `profile.yaml` `knowledge_partition.always_on[5]` (register/discourse/AV) | Cites P090 but drops its caveats: a source-target register/cohesion mismatch may be legitimate strategy (explicitation/compensation) not an error, and the Hallidayan/Gricean apparatus is Anglo-centric — apply with caution outside English-oriented pairs. Hedge dropped at profile level, not just deferred to skill. | Append clause: "…treating a source-target register mismatch as possibly a legitimate strategy (explicitation, compensation) rather than automatically an error, and applying the Hallidayan/Gricean apparatus with caution outside English-oriented language pairs (P090)." |
| `skills/translation-procedures-and-shifts/SKILL.md` desc L3-11; `skills/meaning-signification-and-equivalence-critique/SKILL.md` desc L3-9 | Level-1 frontmatter `description` (loaded for every request) embeds full V&D taxonomy + long tie-breaker paragraph — duplicates Purpose, inflates always-loaded tier. | Trim each description to ~1-2 sentences (review question + one routing clause); move taxonomy into Purpose. |
| `skills/{culture-ideology-power-and-rewriting, hermeneutics-and-the-limits-of-translatability, literal-free-strategy-history-and-retranslation, translation-quality-and-applied-studies}/SKILL.md` | Densest skills: procedure steps + anti-pattern bullets are 60-90-word sentences packing 2-4 sub-checks each; bodies well past ~2000 words; a "step" isn't one executable action. | Split compound steps into single-action bullets; push granular trailing clauses into the reference files. |
| all 12 `skills/*/SKILL.md` Output sections | No concrete worked example (flaw→correction instantiation of the Output template); only profile.yaml's 2 examples show finished format and can't exercise the other 10 skills. | Add one compact worked example per skill (or per cluster). |
| `principles.yaml` P021/P065/P168 (House model) | House's overt/covert + covertly/overtly-erroneous taxonomy is load-bearing but House is not a listed primary source (only Munday/Venuti/Toury) → Munday-mediated, risks subtle distortion (Genre dimension, cultural-filter operational content omitted). | Add a House source/citation note acknowledging secondary grounding, or cross-check P021/P065/P168 vs House's primary text (sibling `translation-quality-reviewer` has House primary — reuse). |
| `principles.yaml` P023 vs P165 (adequacy homonym) | Two unrelated senses of "adequacy" (Toury's norm-orientation pole vs Reiss's per-text-type quality criteria) left undisambiguated, though the package explicitly disambiguates the analogous House overt/covert homonym. | Add a one-line disambiguation note (parallel to the House note) in `text-type-skopos-and-the-brief` or `descriptive-method-and-translational-norms`. |
| `principles.yaml` P111 (Chesterman) | "Chesterman's four complementary approaches (textual, cognitive, sociological, cultural)" — Chesterman's own taxonomy is usually three research-models (comparative/process/causal), "cultural" folded in. Could not confirm as his own four-way split. | Re-check the Munday chunk behind C00345–C00347; attribute to "Munday's summary of Chesterman" or collapse to three. |

---

## nice

| Where | Problem | Fix |
|-------|---------|-----|
| `profile.yaml` `source_of_truth_policy.precedence` L100-102 | P114 cited for equivalence-vs-function precedence but P114 is about selective-preservation trade-offs generally; P062 alone supports the claim. | Drop P114 or replace with a principle addressing the equivalence/function trade-off mechanism. |
| `profile.yaml` `handoff_rules[1]` L94 / adapter Handoff L397 | "Sibling-axis routing is stated once under when_not_to_use." is an authoring note, not a runtime instruction — leaks doc-hygiene rationale into shipped adapter. | Remove; move to provenance-ledger if kept. End bullet after "...theirs to weigh (P029)." |
| `profile.yaml` `examples` L186-214 | Neither example models the subtle `translation-equivalence-advisor` boundary (orientation-fit-here vs mechanism-there) that needed its own prose clause. | Add/replace one example with an either-could-apply ask, response naming the resolving test. |
| `principles.yaml` P108 (Nord doc/instrumental) | Nord's documentary/instrumental distinction stated without attribution, unlike neighbouring named-theorist principles. | Prefix "Following Nord, …". |
| `principles.yaml` P115 + `deforming-tendencies` skill desc | "normalization" listed in one breath with Berman's twelve → risks being read as a 13th tendency (P014 list is correctly twelve). | In skill description set normalization off explicitly as distinct from Berman's twelve. |
| `principles.yaml` P061 / `text-type-skopos-and-the-brief` | "add a phatic function" — phatic is Jakobson's, not a Reiss text-type; reader may infer it's part of Reiss's typology. | Mark the phatic addition as a supplementary extension onto Reiss, not a fifth Reiss type. |
| `principles.yaml` P047 (explicitation) / `domestication-foreignization` step 4 | Omits Blum-Kulka's obligatory-vs-optional explicitation distinction — only optional shifts count as evidence for the hypothesis. | Add a clause: check cited explicitation is optional/non-obligatory before crediting it. |
| `principles.yaml` norms cluster (P010/P039/P046) | Toury's "pseudo-translations" (norm-reconstruction tool) absent despite otherwise-thorough Toury coverage. | Consider adding pseudo-translations to the norm-reconstruction kit. |
| `profile.yaml` sources (Toury `norms-in-translation`) | "The Nature and Role of Norms in Translation" listed year-1995 as if standalone monograph; it's an essay/chapter. | Confirm source-pack manifest scopes ingest to the essay, not implied monograph coverage. |
| `faithfulness-report.yaml` count | grep shows 38 `rule_ref` vs ledger's "35 findings" — likely prose matches, but recount. | Recount top-level `rule_ref:` entries; correct ledger arithmetic if off. |
| skill H1 headings (e.g. `meaning-signification…` L47, `text-type-skopos…` L49) | Naive title-casing capitalizes "And"/"The" mid-sentence. | Use sentence case in generated H1s. |
| all 12 skills Inputs/Output boilerplate | Shared Output-contract sentence copied verbatim across 12 files → 12-way edit on any change. | Optionally single-source in a reference; low priority (duplication aids portability). |

---

MUST_FIX_COUNT: 1
