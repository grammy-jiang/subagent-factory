# Review Loop — translation-equivalence-advisor (round r1)

Consolidated single-pass review. Deterministic gates + 4 lens reviewers (agent-skills,
profile, faithfulness, agent-engineering) + 3 domain reviewers (descriptive-translation,
translation-quality, technical-translation). Findings deduped across lenses, most-severe first.

## Deterministic gates (STEP 1)

| Gate | Result |
|------|--------|
| `validate_generated_package` | **PASS** (0 FAIL; phase8 WARNING only — see MF-2) |
| `quote_scan` | PASS — no verbatim quotation |
| truncation `…` grep (skills + adapter) | clean |
| adapter invariant severed-parenthetical grep | clean |

No deterministic FAILs.

---

## MUST-FIX

### MF-1 — No independent re-verify (verify2) confirming v1.2.1 converged to zero must-fix
- **Where**: `reports/review-loop/` — has `verify1.md` (found MF-1, MF-2) + `vfix.done`, no `verify2.md`.
- **Problem**: `verify1.md` documents that a prior self-reported `must-fix=0` ("CLEAN") was **wrong** — the independent panel found 2 real must-fix defects the loop missed. v1.2.1 records fixes for both, and the fixes are textually present, but this is the exact self-reported-clean pattern already proven unreliable once for this package. CLAUDE.md's process ("domain-reviewer panel → grounded fix → independent re-verify → converge to zero must-fix") requires an independent re-verify round on the v1.2.1 state before release. (This r1 pass is that round.)
- **Fix**: Treat this r1 report as the independent re-verify of v1.2.1; apply the fixes below then run one more converge pass. No new domain/skill/agent defect surfaced here that blocks — the only must-fix items are this process gate and MF-2.

### MF-2 — Phase 8 self-check artifact (`tests/test-results.md`) is stale / not tied to v1.2.1
- **Where**: `tests/test-results.md` (`Generated: 2026-07-11T18:33:14`) vs `profile.yaml` v1.2.1 (2026-07-12).
- **Problem**: Timestamp predates all three post-1.0.0 bumps (v1.1.0/1.2.0/1.2.1) that touched body word count near the Phase 8 hard limits. v1.2.0 SF-6 records the body was trimmed "to keep under the 1000-word hard limit after the MF-1 propagation" (implies transient FAIL mid-fix). Recorded check-14 = ~992w (WARNING), ~8w under the 1000w FAIL cutoff = no headroom, and the file carries no `profile_version` tag proving which revision it measured. Plausibly still accurate, but plausibility ≠ verification; validate's `phase8: WARNING` is the same soft signal.
- **Fix**: Re-run `python -m tools.subagent_factory.profile_self_check subagents/translation-equivalence-advisor` (or `cli validate`) against current `profile.yaml`; regenerate `tests/test-results.md` with a fresh timestamp so check-14 body-size is verifiably tied to v1.2.1.

---

## SHOULD-FIX

### SF-1 — 7 of 9 skill descriptions frame with "Reviews" only, under-triggering pre-draft advise mode
- **Where**: SKILL.md frontmatter `description` in `collocation-idiom-and-fixed-expression`, `grammatical-equivalence`, `thematic-and-information-structure`, `cohesion-and-texture`, `pragmatic-equivalence-coherence-and-implicature`, `register-style-and-literary-form`, `text-level-approach-and-limits-of-equivalence`.
- **Problem**: Every body builds a first-class advise-mode path and the profile charter treats pre-draft advice as core, but the description (sole load-time trigger) opens with "Reviews," skewing matches to draft-exists requests. `word-level-nonequivalence-and-strategies` already models the better "Diagnoses…and reviews…" pattern.
- **Fix**: Broaden each opening verb to cover diagnose/advise + review, mirroring the word-level skill.

### SF-2 — `compare` mode has no body-level output support in any skill
- **Where**: `## Output` in all 9 skills; most acute in `dynamic-and-formal-equivalence` and `text-level-approach-and-limits-of-equivalence`.
- **Problem**: Profile advertises a `compare` mode (side-by-side of what each option favours/costs → weighted recommendation), but no skill Output section describes that shape — only advise (single rec) or review (per-finding). The two skills most likely to get compare requests lack the format the charter promises.
- **Fix**: Add a compare-mode output branch to at least those two skills: "If comparing two options for one segment, lay out what each favours and costs side by side before recommending."

### SF-3 — `quality_bar[0]` drops the hedge on one-to-one word matching (HEDGING_REMOVED)
- **Where**: `profile.yaml` `quality_bar[0]`.
- **Problem**: "No one-to-one match at word level…" states categorically that no match exists; cited P037 only cautions against *assuming* one-to-one correspondence (a match may hold). As a governing review criterion this could flag an accurate one-to-one rendering as a defect. Every sibling formulation (`always_on[0]`, the example, `forbidden_behaviours[1]`) correctly hedges as "don't assume/assert." This outlier is a fresh finding (not the earlier quality_bar[1]/[6] fixes).
- **Fix**: Reword headline to "Don't assume a one-to-one match at word level: diagnose the non-equivalence, weigh its significance in context, and choose from an open set (P037, P001, P103, P106)."

### SF-4 — Back-translation characterized too narrowly + too skeptically (raised by 2 domain reviewers)
- **Where**: `principles/principles.yaml` P100; `skills/dynamic-and-formal-equivalence/SKILL.md` Procedure step 7.
- **Problem**: Frames back-translation only as exposing morphological/syntactic/lexical structure and brands it flatly "theoretically unsound…never reproduces meaning." Nida's own methodology uses it as a *semantic-equivalence testing* technique, and it remains a mandated QA step in regulated domains (clinical/PRO, pharmacovigilance, legal — ISPOR/FDA-style). Narrowed scope + unqualified "never" understates its real role.
- **Fix**: Reframe to reflect its meaning-check purpose and current QA role, while keeping the legitimate caution that a matching back-translation doesn't *guarantee* equivalence (a shared error survives the round trip). NOTE: verify the reframe stays within P100's source support; keep the caveat.

### SF-5 — "Masculine as unmarked" stated without inclusive-language currency caveat (raised by 2 domain reviewers)
- **Where**: `principles/principles.yaml` P015; `skills/grammatical-equivalence/SKILL.md` step 3.
- **Problem**: Accurate as a structural-linguistic description, but as unqualified advice it reads as license to default to generic masculine. Current institutional/legal/publisher style guides (EU/UN, corporate) and non-binary source-language handling increasingly treat generic-masculine defaults as contested.
- **Fix**: Add a caveat: "masculine-as-unmarked" is a structural fact, not a translator default; check the brief/style guide, which often now mandates gender-neutral resolution (singular they, paired forms, restructuring). Existing restructure clause already points this way.

### SF-6 — `examples[1].ideal_response` genre-defaults marketing→dynamic equivalence (SCOPE_BROADENED)
- **Where**: `profile.yaml` `examples[1].ideal_response` ("marketing text usually calls for dynamic equivalence", P034/P041). Same pattern in `tests/golden-tests.yaml` GT-004 (root cause `.build/authoring/gen.py`).
- **Problem**: P034/P041 are task/purpose-conditioned, not genre-defaulted; no source states a genre-level default. Contradicts the package's own precedence rule (brief governs) and `forbidden_behaviours[2]` (mechanical type→strategy mapping). "usually" hedge + illustrative context keep it below must-fix.
- **Fix**: Reframe as brief-conditioned: "a marketing brief typically prioritizes receptor response, so ask what this brief's purpose favours before defaulting the orientation (P034, P041, P021)." Fix GT-004 at the generator too.

### SF-7 — Nida "dynamic equivalence" presented as live term without the "functional equivalence" reframing (raised by 2 domain reviewers)
- **Where**: `skills/dynamic-and-formal-equivalence/SKILL.md`; `references/translation-equivalence-key-concepts.md`; P021/P034/P035/P036.
- **Problem**: Nida (with de Waard, 1986, *From One Language to Another*) replaced "dynamic equivalence" with "functional equivalence" specifically to curb misreading "dynamic" as license for loose paraphrase. Package's own source disclosure notes it's a derived extract of the 1964 monograph. Currency gap for a package meant to reflect current practice.
- **Fix**: Add one line in the skill Purpose + key-concepts entry: "Nida's 1964 term; later reframed as 'functional equivalence' (1986) to curb over-reading 'dynamic' as license for paraphrase." No strategy change.

### SF-8 — Adequacy defined only by Nida's criteria; no note on unfalsifiability of "equivalent response"
- **Where**: `skills/dynamic-and-formal-equivalence/SKILL.md` step 8; P035/P036; key-concepts "Adequacy".
- **Problem**: "Similar receptor response" is empirically unverifiable (can't measure against the unavailable original audience) — a central translation-studies critique. `quality_bar` softens generally but nothing flags the specific unfalsifiability of equivalent-response testing.
- **Fix**: Add caveat/anti-pattern: treat "similar audience response" as a directional target, not a measurable outcome; a fluent read is not proof of equivalent effect.

### SF-9 — P084 mislabels the grammar/lexis contrast as "morphology vs syntax"
- **Where**: `principles/principles.yaml` P084; `skills/grammatical-equivalence/SKILL.md` step 6.
- **Problem**: Header says "Distinguish morphology from syntax," but the substance (and Baker Ch.3) contrasts grammar (morphology+syntax, closed/obligatory) vs lexis (open/optional). Mislabel could send a reader hunting a morphology-vs-syntax distinction that isn't the point.
- **Fix**: Rephrase to "Distinguish grammar (morphology and syntax together, a closed, largely obligatory system) from lexis (an open, largely optional system)" in principle + skill step. NOTE: verify against P084's actual claim text before editing.

### SF-10 — `golden-tests.yaml` profile_version one revision behind
- **Where**: `tests/golden-tests.yaml:4` (`1.2.0`) vs `profile.yaml:4` (`1.2.1`).
- **Problem**: Dependent artifact should track version bumps; reader can't tell if GT-004 etc. were validated against current text.
- **Fix**: Bump `profile_version` to `1.2.1` (content appears unaffected by v1.2.1 fixes — metadata-only), or record the intentional lag.

### SF-11 — Adapter `description` compresses to 1 of 3 modes + 1 of 3 exclusions
- **Where**: adapter `description` (line 3) vs profile `when_to_use`/`when_not_to_use`.
- **Problem**: Drops the `review` and `compare` triggers (half the modes) and 2 of 3 exclusions from the orchestrator's discovery signal, narrowing selection for review/compare use cases. Shared generator-template pattern (same truncation in sibling adapters) → fix belongs in the adapter-export description-synthesis step.
- **Fix**: Have description-synthesis sample across modes/bullets or name the three mode triggers.

### SF-12 — Provenance ledger overclaims universal per-field citation
- **Where**: `provenance-ledger.md:8-9`.
- **Problem**: States every quality_bar/forbidden_behaviours/handoff/always_on/source_of_truth value cites its principle, but `forbidden_behaviours[0]` (profile:83-84) has no inline citation — correct by design (faithfulness-report marks it declared scope, not a distillation claim). Blanket sentence reads like an orphan-field violation.
- **Fix**: Qualify: "…cites the promoted principle(s) it restates, or is marked as declared advisory-boundary policy in the faithfulness report (see forbidden_behaviours[0])."

### SF-13 — faithfulness-report `quality_bar[0]` note not updated for v1.2.1 correction
- **Where**: `reports/faithfulness-report.yaml:4-11`; `CHANGELOG.md` v1.2.1.
- **Problem**: v1.1.0/v1.2.0 changelog entries each record "Faithfulness-report note updated"; v1.2.1 (MF-2 narrowing "word or phrase"→"word level") does not, and the note text is unchanged. Audit trail inconsistent with prior practice at the same rule_ref.
- **Fix**: Add a short note to the `quality_bar[0]` entry recording the MF-2 scope correction.

### SF-14 — faithfulness-report coverage gap on uncited profile sections
- **Where**: `reports/faithfulness-report.yaml`.
- **Problem**: Report covers 27 rule_refs but has no entries for `role`, `when_to_use[*]`, `when_not_to_use[*]`, `inputs.required`, `minimum_useful_output`, `examples[*].ideal_response` — yet its scope claims "every profile rule." SF-6 (in examples[1]) is exactly the kind of over-claim this gap misses.
- **Fix**: Add rule_ref entries for those sections, including the SF-6 SCOPE_BROADENED finding.

---

## NICE

- **N-1** — Body word count at edge of 1000w hard FAIL with no durable headroom; `quality_bar` carries 9 bullets (registry expects 3–5), the structural reason for repeated ceiling bumps. Consolidate into fewer denser bullets to reclaim headroom. (`profile.yaml` quality_bar)
- **N-2** — Gricean third maxim labeled "Relevance" (faithful to Baker) risks conflation with Sperber & Wilson Relevance Theory. Add parenthetical: "Relevance (Grice's Maxim of Relation, 'be relevant' — distinct from Relevance Theory)." (P032/P033/P073; pragmatic skill)
- **N-3** — Chinese "bei" passive-as-adversity stated as flat fact; modern journalistic/internet Mandarin (post-2008 "被XX") has broadened it to neutral/satirical. Note the association is register/era-dependent. (P009)
- **N-4** — `dynamic-and-formal-equivalence` H1 "…and Receptor Response" diverges from the title-cased-name pattern of the other 8 skills. Rename H1 or fold into Purpose.
- **N-5** — Only 2 of 9 skill Output sections carry a "never hand back X as final" closing clause, and they reinforce different boundaries. Standardize or accept redundant-elsewhere coverage.
- **N-6** — Skill descriptions assume translation-studies vocabulary ("unlexicalized", "false friend", "FSP"); a plain-language trigger phrase per description would widen matching.
- **N-7** — `cohesion-and-texture` uses "coherence" (P112, lexical sense) while its boundary hands reader-coherence to the pragmatic sibling; term overlap could blur routing. Phrase as "lexical continuity/lexical coherence".
- **N-8** — Baker 1st ed. (1992) grounding; 2nd (2011)/3rd (2018) editions exist with corpus-informed collocation refinements. Optionally note later editions in source-of-truth for cross-check.
- **N-9** — `inputs.required` bundles 3 distinct inputs (source segment / draft / brief) into one compound sentence; split into three bullets.
- **N-10** — Role paragraph names adapter-specific mechanic ("the invariants below"); soften to platform-neutral phrasing so it holds across future adapters.
- **N-11** — `when_to_use[2]` / adapter line 43 grammatically broken: "They want which strategy fits" → "and wants to know which strategy fits."
- **N-12** — Adapter role narrative never names `compare` mode explicitly though it's 1 of 3 modes; add an explicit clause.

---

MUST_FIX_COUNT: 2
