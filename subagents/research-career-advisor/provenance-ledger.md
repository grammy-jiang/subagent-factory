# Provenance Ledger — research-career-advisor

Canonical record of what grounds this subagent. The profile, skills, references, faithfulness
report, and tests are all derived from the distilled spine in this package
(`principles/principles.yaml` -> `analysis/claims.jsonl` -> `evidence/evidence-records.yaml` ->
`sources/anchors/*.anchors.jsonl`), assembled by the map->reduce build. Most load-bearing profile
rule fields cite the promoted principle(s) they restate: `quality_bar`, `knowledge_partition.always_on`,
the `precedence` clause, and the substantive `forbidden_behaviours` (faithfulness and empirical-overstatement
rules `[3]`/`[4]`). The advice-only **boundary** rules, however, are **structural house-policy**, not
principle restatements: advisor-vs-researcher ownership and no-prediction-of-outcomes in
`forbidden_behaviours[0]`, `[1]`, `[2]`, `handoff_rules[0]`, `[1]`, and the sibling-referral
`handoff_rules[2]` all carry the inline "(structural house-policy…)" qualifier and **no principle tag** —
they derive from the advice-only boundary and the repository rules, since no source claim establishes
advisor-vs-researcher ownership, no-outcome-prediction, or no-legal/immigration-advice as a literal
statement. (v1.4.0 dropped the topically-nearest principle tags these six boundary rules previously carried:
the r2 review found them misread as source grounding — a boundary presented as source-derived when it is
not.) `source_of_truth_policy.canonical_owner`
is likewise a **descriptive authority statement** (advice-only boundary, structural house-policy): it carries
no inline principle tag, and its closing sentence grounds the advisory criteria in the four sources' distilled
principles. (Descriptive fields — `role`, `when_to_use`, `when_not_to_use`, `inputs`, `outputs`, and
`source_of_truth_policy.canonical_owner` — carry no inline tags, per repo convention.)

## Sources

| source_id | title | author | year | rights |
|-----------|-------|--------|------|--------|
| a-phd-is-not-enough-9a264724 | A PhD Is Not Enough! A Guide to Survival in Science | Peter J. Feibelman | 2011 | distillation-only |
| hamming-meta-5bf0ea64 | The Art of Doing Science and Engineering: Learning to Learn / You and Your Research | Richard W. Hamming | 1997 | distillation-only |
| xueshu-yanjiu-chengg-ff70b27e | The Road to Success in Academic Research (学术研究成功之道) | Academic-research success guide (Chinese) | None | distillation-only |
| empirical-methods-co-de09d1d7 | Empirical Methods for Artificial Intelligence | Paul R. Cohen | 1995 | distillation-only |

All four sources are **distillation-only**: paraphrase and restructure only, no verbatim quotation
(see `.claude/rules/rights-and-quotation-policy.md`; enforced by `quote_scan`). They are canonical
works on the scientific research career and empirical method: Feibelman's survival guide for a
career in science, Hamming's essays on doing high-impact research and learning to learn, a Chinese
guide to succeeding in academic research, and Cohen's textbook on empirical methods for AI.

## Distillation

Spine: 48 promoted principles (P001-P048; 0 high-confidence) over
611 atomic claims, with evidence records and chunk anchors. The 48 principles are
partitioned across 8 skills, each principle owned by exactly one skill; the two
references index and ground them.

## Cross-source conflict check

`multisource_synthesis` is `deferred` (no automated Step-7 synthesis / principle-graph run). A manual
cross-source conflict pass was made over the four sources, which span different eras and settings
(Hamming's 1997 Bell-Labs industrial perspective vs. present-day academic-job-market guidance in
Feibelman and the Chinese success guide; Cohen's empirical-method text is orthogonal). No contradictory
principles were found: the sources emphasize different facets (importance-and-attackability of problems,
protection factors in mentoring, communication, funding, empirical soundness) rather than opposing rules.
The one latent tension — how much to weight institutional prestige — is resolved by P010's own hedge
(established reputation is a tie-breaker only when protection factors are comparable), which `quality_bar`
and `knowledge_partition.always_on` both preserve, and by the `precedence` rule that treats purpose-tied
practices as adaptable guides rather than absolutes.

## Version History

- **1.4.0** (2026-07-25) — Review-loop round r2 (consolidated) fixes
  (`reports/review-loop/research-career-advisor.r2.review.md`). **Sequencing note:** round r2 (PR#97) and
  round r1 both landed before this pass; round r3 (`r3.review.md`) ran against v1.2.0 and flagged two
  unresolved MUST-FIX — the false `(P010, P021)` and `(P026)` citations on the hiring/tenure and
  legal/immigration boundary rules — which the v1.3.0 label-only fix did not close. This release closes
  them. **Profile:** dropped the false principle citations from `forbidden_behaviours[0]` (was P017/P013),
  `[1]` (P010/P021), `[2]` (P026), `handoff_rules[0]` (P015/P017), and `[1]` (P026/P010) — none grounded
  the boundary, and the inline "(structural house-policy…)" qualifier alone suffices per
  `source_of_truth_policy`; `handoff_rules[0]`/`[1]` gained the same qualifier `[2]` already carried.
  Scoped the choosing-advisers `always_on[2]` lab-management clause to "an industrial or government
  laboratory" to track P034's `applies_when` (was SCOPE_BROADENED). Dropped the non-load-bearing P046 tag
  from `quality_bar[1]` (P017/P012 carry the clause). Strengthened the `role` two-concern bundling
  justification to name the shared publish/persist decision surface. **Skills (all 8):** replaced the
  review-only `## Output` sentence with a three-line advise/review/plan mapping to `outputs.modes`, so each
  SKILL.md is self-sufficient off-adapter; `presenting-and-engaging-with-research` `description:` gained a
  slide-content-vs-visual-design boundary clause (→ research-writing-advisor). Skill `provenance:` blocks
  preserved verbatim; only bodies/descriptions changed. **Faithfulness report:** synced the six affected
  rule notes to the disclosed-house-policy framing. **Tests:** bumped stale `golden-tests.yaml`
  `profile_version` 1.0.0 → 1.4.0. **Ledger:** the grounding paragraph now records the six boundary rules
  as carrying no principle tag (the topically-nearest tags were dropped this release). The distilled spine
  (48 principles) is unchanged. Supersedes the 1.3.0 boundary-citation decisions.
- **1.3.0** (2026-07-25) — Review-loop round 1 (r1) fixes. **Adapter routing (must-fix):** the adapter
  renderer (`export_claude_agent.py`) now builds the frontmatter `description` from the profile's
  purpose-built `router_description` when present, instead of the mechanical `role — Use when — Not for`
  concatenation that truncated to two triggers + one exclusion and silently dropped the empirical-study/metric
  soundness domain and both sibling-advisor exclusions; `router_description` was extended to name all five
  `when_to_use` domains and the two sibling referrals. **Profile:** `forbidden_behaviours[0-2]` now carry an
  inline "structural house-policy, advice-only boundary" qualifier for self-disclosure (matching
  `handoff_rules[2]`); `when_not_to_use[4]` distinguishes reviewing a stated test procedure's statistical
  validity (in scope) from adjudicating whether p-hacking/misconduct occurred (out of scope); `role`'s
  absolute author-attributed "condition of research survival (Cohen, Hamming)" clause softened to a descriptive
  register; `always_on[3]` tightened "moving on" → "moving groups" to track P019 exactly. **Skills:** the 7
  filler `## Purpose` sections (all except `evaluation-metrics-and-research-judgment`) replaced with
  content-bearing purposes naming the actual checks (pointer sentence dropped); a negative-scope "Not for …"
  clause added to those 7 `description:` frontmatters; `presenting-and-engaging-with-research` and
  `early-career-positioning-and-negotiation` descriptions normalized from "Use when …" to "Guides …". Skill
  `provenance:` blocks preserved verbatim; only bodies/descriptions changed. **Faithfulness report:** added
  coverage entries for `handoff_rules[2]`, `source_of_truth_policy.canonical_owner`, all 8
  `knowledge_partition.always_on[i]` blocks, and all 3 `examples[i]` (previously unaudited; independent walk
  found each within scope). **Ledger:** `canonical_owner` recorded as a descriptive no-tag field. No principle
  **citation IDs** on any surviving field→grounding row changed and the distilled spine is unchanged.
  Supersedes the 1.2.0 skill-purpose, profile-boundary, and adapter-description-composition decisions.
- **1.2.0** (2026-07-25) — Review-loop round 2 fixes. `evaluation-metrics-and-research-judgment`:
  re-anchored `description:` + every `## When to use` bullet to the research domain and added an
  out-of-scope carve-out (must-fix — trigger scope drifted outside the advisor boundary). All 8 skills:
  conditional load-on-demand `## References` phrasing and one-sentence `## Purpose` (token discipline);
  `funding-grants-and-research-proposals` `description:` trimmed under the 1024-char cap. Profile: added
  `when_not_to_use` + `handoff_rules` routing to `research-integrity-reproducibility-advisor` (sibling
  scope overlap on empirical-integrity) and `research-writing-advisor`, and extended `role` to justify
  the empirical-methods/evaluation remit. This ledger's grounding paragraph relabelled the advice-only
  boundary rows (`forbidden_behaviours[0-2]`, `handoff_rules[0-2]`) as structural house-policy rather than
  literal principle restatements — no principle **citation IDs** on any surviving row changed (the new
  `handoff_rules[2]` sibling-referral is intentionally uncited house-policy), so no field→grounding row
  required re-mapping. Skill `provenance:` blocks and digests preserved verbatim; the distilled spine is
  unchanged. Supersedes the 1.1.0 skill-trigger and profile-boundary decisions.
- **1.1.0** (2026-07-25) — Re-authored all 8 skill bodies to the GOLD shape (added trigger-oriented
  `description:` frontmatter; rewrote every anti-pattern bullet as a complete observable-failure-symptom
  sentence, one per provenance principle — restoring the dropped P038 and P046 bullets and replacing
  truncated substrings; expanded stub Procedure steps), preserving `provenance:` blocks and digests
  verbatim. Profile: weakened `quality_bar[2]` to restore P010's tie-break hedge (was flattened to "not
  prestige"), shortened `role` to stop duplicating `forbidden_behaviours`, narrowed `when_to_use[3]` to
  the strategy slice and added a `when_not_to_use` handoff to `research-writing-advisor`, and added a
  `router_description` covering all five when-to-use domains. Recorded the manual cross-source conflict
  check above. No principle citations were changed for any surviving `quality_bar` /
  `forbidden_behaviours` / `handoff_rules` row, so no field→grounding row required re-mapping.
  Supersedes the 1.0.0 skill-body and profile-copy decisions; the distilled spine is unchanged.
- **1.0.0** (2026-07-25) — Initial LLM-authored layer over the pre-built distilled spine: profile
  (role, three modes, quality bar, forbidden behaviours, 8-skill / 2-reference
  knowledge partition), faithfulness report, 8 skills, 2 references, golden +
  principle-behaviour tests, and the exported Claude Code adapter. No prior profile decisions
  superseded.
