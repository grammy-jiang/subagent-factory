# descriptive-translation-reviewer — Review Loop r5 (rerun)

Package: `subagents/descriptive-translation-reviewer/` (profile v1.8.0).
Consolidated from deterministic gates + 7 parallel reviewer lenses (agent-skills, profile,
faithfulness, agent-design, and 3 domain cross-checks: equivalence / quality / technical).
Dedup applied across lenses; most-severe first.

> Note: this file previously held a v1.4.0 pass (M1 anti-pattern duplication, M2 missing
> tie-breaker). Both were addressed in rounds r2–r4 (tie-breakers now present; anti-pattern
> density downgraded to should-fix here). This rerun reflects the current v1.8.0 state.

## Deterministic gates (this pass)

| Gate | Result |
|------|--------|
| `validate_generated_package` | **PASS** — 0 fail, 0 warn |
| `quote_scan` | **PASS** — no verbatim quotation |
| truncation grep (ellipsis `…`) | clean |
| truncation grep (severed invariant paren) | clean |
| `profile_self_check` | **WARNING** — body ~992 words > 800 budget (under 1000 FAIL line) |

No deterministic FAIL. The self-check WARNING is carried below as SF-2 (real, deterministically
measured, but under the hard FAIL threshold).

## must-fix

None. (Agent-design raised the adapter-description collision as must-fix; on verification it
downgrades to should-fix — see SF-1, rationale recorded there.)

## should-fix

### SF-1 — adapter/profile — description "Use when" clause near-duplicates sibling
- Where: `.claude/agents/generated/descriptive-translation-reviewer.md:3` (from `profile.yaml` `when_to_use[0]`)
- Problem: exported "Use when:" clause = *"A translation or draft is assessed for its equivalence
  orientation and strategy"* — near-identical to `translation-quality-reviewer`'s *"A translation or
  draft is being assessed and the team wants its quality reviewed."* The disambiguating tail of the
  source bullet ("…not scored against a fixed quality metric") is dropped in truncation.
  **Verified downgrade from must-fix:** the description LEAD sentence *does* carry the disambiguator —
  descriptive reads *"…descriptive method, **not corpus-based quality scoring**"* vs quality's
  *"…**corpus-based** translation-studies analyses."* An orchestrator reading the full description can
  still distinguish them; routing is not broken, only the mid-clause is weaker than it could be.
- Fix: front-load the disambiguator into `profile.yaml` `when_to_use[0]` so it survives truncation, or
  adjust the export template to stop cutting the bullet at its first em-dash. Apply the same check to
  the three sibling adapters.

### SF-2 — profile.yaml — body ~992 words, 192 over the 800-word budget
- Where: `subagents/descriptive-translation-reviewer/profile.yaml` (deterministic `profile_self_check` check 14)
- Problem: v1.3.0–v1.8.0 added content (forbidden_behaviours split, new handoff_rules bullet, extra
  citations) on top of the v1.2.0 trim with no follow-up size check; budget eroded to ~992w. Heaviest:
  `quality_bar` 158w, `when_not_to_use` 126w, `role` 108w. Still under the 1000-word hard FAIL, so
  headroom is thin.
- Fix: trim the heaviest sections without dropping any principle citation; re-run `profile_self_check`
  to confirm ≤800.

### SF-3 — principles.yaml P069 + register-discourse skill — subtitling numerics stated as near-universal hard limits
- Where: `principles/principles.yaml` P069; `skills/register-discourse-and-audiovisual-constraints/SKILL.md` (Procedure step 10 + Anti-patterns). Flagged by equivalence (should-fix) + quality (nice) + technical.
- Problem: figures ("~38 Roman / 13–15 CJK chars, ~six seconds") are a defensible classic average, but
  the anti-pattern flags any subtitle exceeding "the character or six-second limit" as a finding. Real
  platform style guides differ materially (Netflix 42 CPL EN / 16 CJK / up to 7s; BBC ~37) — applied
  literally against a Netflix-spec file this yields false positives.
- Fix: soften to "typical convention (~35–42 Roman / ~13–16 CJK chars per line, several-second
  ceiling), but check the commissioning platform's own style guide before citing an exact figure."

### SF-4 — principles.yaml P111/P166 — Chesterman "four approaches" likely a misattribution
- Where: `principles/principles.yaml` P111, P166; restated in `culture-ideology-power-and-rewriting/SKILL.md` step 15 and `descriptive-method-and-translational-norms/SKILL.md` step 21. (technical lens)
- Problem: P111 attributes "four complementary approaches (textual, cognitive, sociological, cultural)"
  to Chesterman. Chesterman's Translator-Studies typology names **three** branches (cultural /
  cognitive / sociological); "textual" is not his fourth. The four-way product/process/participant/
  context split (used, unnamed, in P093) is commonly Saldanha & O'Brien — a different source. Risk: two
  frameworks conflated under one name.
- Fix: re-verify against the source anchor backing P111 (claims C00345–C00347). If "textual" is not in
  Chesterman's own typology, drop it or re-attribute the four-way split; keep Chesterman's name only on
  the three branches he proposed.

### SF-5 — functionalist/skopos cluster — missing Nord "function plus loyalty"
- Where: `principles/principles.yaml` P009/P062/P078/P108/P112; `skills/text-type-skopos-and-the-brief/SKILL.md`. (technical lens)
- Problem: skopos rules and "a fulfilled skopos does not excuse micro-level neglect" (P108) are covered
  well, but Nord's *function plus loyalty* — the standard functionalist corrective answering the
  "skopos could justify any liberty" objection by binding the translator to source-participants'
  intentions — is never stated. It is the actual mechanism for judging whether a brief-licensed
  departure has gone too far.
- Fix: add a principle (groundable in Munday's functionalism chapter, which covers Nord alongside
  Reiss/Vermeer/Holz-Mänttäri) and route it into `text-type-skopos-and-the-brief` next to P108.

### SF-6 — profile.yaml knowledge_partition.always_on — r4 ownership fixes not mirrored into the profile
- Where: `subagents/descriptive-translation-reviewer/profile.yaml` `knowledge_partition.always_on`. (profile lens)
- Problem: two cross-skill ownership overlaps resolved in r4 (register: procedures-and-shifts P168 ↔
  register-discourse P064; skopos vs eval-method: text-type-skopos P009 ↔ translation-quality-and-
  applied-studies P112) were applied only to the SKILL.md bodies, not mirrored into the profile's
  `always_on` summaries. The domestication/culture-ideology pair (always_on items 7/8) *does* carry
  reciprocal boundary language in the profile. Since profile.yaml is canonical, a profile-only reader
  cannot see these two overlaps are resolved.
- Fix: add short reciprocal boundary clauses to the two affected always_on item pairs, matching the
  item-7/8 pattern.

### SF-7 — all 12 SKILL.md — review-only boundary sentence restated ~3× per file
- Where: every `skills/*/SKILL.md` (frontmatter description + `## Purpose` + `## Output`). (agent-skills lens)
- Problem: ~36 near-verbatim repetitions of the "critiques X; does not produce the finished
  translation / make the publication decision" boundary across the pack — low-signal duplication in the
  always-loaded body.
- Fix: state it once (keep in `## Purpose` or the description tail); drop from `## Output`, which should
  carry only the findings-format mechanics.

### SF-8 — all 12 SKILL.md — Procedure and Anti-patterns restate each principle as positive + negation
- Where: every `skills/*/SKILL.md` `## Procedure` vs `## Anti-patterns to flag` (worst on the 19–21-principle skills: culture-ideology-power, hermeneutics). (agent-skills lens)
- Problem: each principle appears twice — positive instruction then voice-inverted negation — roughly
  doubling body token cost on the largest skills for marginal recognition value. (Prior round rated
  this must-fix at v1.4.0; now should-fix.)
- Fix: on the largest skills, collapse anti-patterns to a terse one-line "trap" per principle, or keep
  only anti-patterns that add a genuinely new failure mode.

### SF-9 — 5 SKILL.md descriptions — 60–100+ word frontmatter, sibling routing front-loaded into tier-1
- Where: `equivalence-orientations-and-effect`, `meaning-signification-and-equivalence-critique`, `register-discourse-and-audiovisual-constraints`, `domestication-foreignization-and-visibility`, `culture-ideology-power-and-rewriting` (description fields). (agent-skills lens)
- Problem: full sibling tie-breaker routing logic sits in `description` (tier-1, loaded for every skill
  at trigger-decision time) *and* again in the body — inflates the cheapest tier with detail that only
  matters post-selection.
- Fix: shorten to one primary-use-case sentence + a short routing pointer; keep the full tie-breaker
  reasoning in `## Procedure` where it already lives.

### SF-10 — 2 SKILL.md descriptions omit the review-only clause
- Where: `translation-procedures-and-shifts/SKILL.md` desc; `equivalence-orientations-and-effect/SKILL.md` desc. (agent-skills lens)
- Problem: these 2 of 12 descriptions omit any "review-only, does not produce the finished translation"
  clause; `description` is the sole scoping signal before the body loads — inconsistent within an
  otherwise disciplined family.
- Fix: add a short trailing clause ("Review-only.") matching the other 10.

## nice

- `principles.yaml` P141 (equivalence): Yan Fu example conflates direct translation with paratext —
  *Tianyanlun* is Huxley's *Evolution and Ethics* with commentary; the Spencerian framing came via Yan
  Fu's own annotations. Reword to preserve the text/paratext distinction (matters for P013 method).
- `principles.yaml` P026/P083 (equivalence, provenance): Baker-characteristic pragmatics examples
  (Pinter casserole, Heathcliff footnote, Hemingway lunchroom) — confirm they trace to Munday in
  `source-pack.manifest.yaml`/digest, not an unlisted source; re-cite or rephrase if not.
- `principles.yaml` P106 (technical): Koller's 5th relation labelled "formal or expressive"; his term
  is "formal-aesthetic equivalence." Align label or note intentional paraphrase.
- descriptive-method skill (technical): Toury's *pseudotranslation* not covered — optional add as the
  diagnostic limit case for translation-status-as-norm.
- 3 SKILL.md descriptions (agent-skills): comma splices ("…it reviews…, it does not produce…") — use
  semicolon/period.
- 12 SKILL.md H1 headings (agent-skills): title-case capitalizes function words ("And","The");
  normalize if touched.
- SKILL.md frontmatter (agent-skills): factory-internal keys (`kind`,`status`,`provenance`) fine
  internally; confirm target parser tolerance only if ever exported standalone.
- `reports/faithfulness-report.yaml` (faithfulness): no `rule_ref` entries for the `examples` block
  though example `ideal_response` text carries principle-cited claims (checked: all WITHIN_SCOPE). Add
  4 example rule_refs for full profile coverage.
- `profile.yaml` role (profile): ~106w, 3 dense sentences; a tighter first sentence improves human
  scanability. Not release-blocking.

## Lens summary (must-fix per lens)

| Lens | must-fix |
|------|----------|
| deterministic gates | 0 |
| agent-skills (skill authoring) | 0 |
| profile (release-readiness) | 0 |
| faithfulness (over-claim) | 0 |
| agent-design | 1 → **downgraded to SF-1 on verification** |
| domain: equivalence | 0 |
| domain: quality | 0 |
| domain: technical | 0 |

Faithfulness lens confirmed 0 over-claims across all strong-claim profile fields; prior-round
corrections (quality_bar[2] hedge, handoff_rules re-anchor, forbidden_behaviours split) verified intact.

MUST_FIX_COUNT: 0
