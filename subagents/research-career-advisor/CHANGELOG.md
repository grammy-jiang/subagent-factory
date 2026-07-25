# Changelog — research-career-advisor

All notable changes to this generated subagent package are recorded here. Versions follow the
`agent_version` field in `profile.yaml`.

## [1.3.0] — 2026-07-25

### Changed
- **Review-loop round 1 fixes** (`reports/review-loop/research-career-advisor.r1.review.md`).
- **Adapter renderer (must-fix #1):** `tools/subagent_factory/export_claude_agent.py` now builds the
  frontmatter `description` from the profile's `router_description` when present, falling back to the
  mechanical composition only when it is absent. The old composition truncated to two `when_to_use`
  triggers + one `when_not_to_use` exclusion, silently dropping the empirical-study/metric soundness
  domain and both sibling-advisor exclusions from the string Claude Code routes on.
- `profile.yaml`: extended `router_description` to name all five `when_to_use` domains and the two
  sibling-advisor referrals; added an inline "structural house-policy, advice-only boundary" qualifier
  to `forbidden_behaviours[0-2]` (should-fix #2); tightened `when_not_to_use[4]` to separate reviewing a
  test procedure's statistical validity (in scope) from adjudicating p-hacking/misconduct (out of scope,
  should-fix #4); softened `role`'s absolute "condition of research survival (Cohen, Hamming)" clause to
  a descriptive register (#10); tightened `always_on[3]` "moving on" → "moving groups" to track P019 (#11).
- Skills (7 of 8, all except `evaluation-metrics-and-research-judgment`): replaced the filler `## Purpose`
  sentence + "carries the specific checks" pointer with a content-bearing purpose (should-fix #5); added a
  negative-scope "Not for …" clause to the `description:` frontmatter (should-fix #6); normalized the
  `presenting-…` and `early-career-…` descriptions from "Use when …" to "Guides …" (#8). `provenance:`
  blocks preserved verbatim; only bodies/descriptions changed.
- `reports/faithfulness-report.yaml`: added `WITHIN_SCOPE` coverage entries for `handoff_rules[2]`,
  `source_of_truth_policy.canonical_owner`, all 8 `always_on[i]` blocks, and all 3 `examples[i]`
  (should-fix #3 — the densest citation surface was previously unaudited).
- `provenance-ledger.md`: recorded `canonical_owner` as a descriptive no-tag field (#12) and added the
  1.3.0 Version History entry. No principle citation IDs on any surviving row changed; the distilled spine
  is unchanged.

## [1.2.0] — 2026-07-25

### Changed
- **Review-loop round 2 fixes** (`reports/review-loop/research-career-advisor.r2.review.md`).
- `skills/evaluation-metrics-and-research-judgment`: rewrote the `description:` frontmatter and every
  `## When to use` bullet to anchor each trigger to the research domain (research-group brainstorming,
  lab/publication metrics, screening PhD/postdoc applicants, expertise carried into a new subfield) and
  added an out-of-scope carve-out for purely generic corporate-metrics/HR/hiring questions, so the router
  can no longer fire this skill on a non-research judgment question (must-fix).
- All 8 skills: adopted the conditional load-on-demand `## References` phrasing (from the funding skill)
  so each reference load is gated by need, and trimmed each `## Purpose` to one sentence (the enumerated
  checks live in `## When to use`/`## Procedure`) for token discipline. `provenance:` blocks and
  `authored_from_digest` preserved verbatim.
- `skills/funding-grants-and-research-proposals`: shortened the over-long `description:` (was 1194 chars,
  over the 1024 frontmatter cap) to a single tight paragraph with the concrete trigger phrases.
- `profile.yaml`: added a `when_not_to_use` bullet routing research-integrity / reproducibility audits
  (misconduct, p-hacking, replication failure) to `research-integrity-reproducibility-advisor`; added a
  third `handoff_rules` entry carrying the sibling-advisor referrals (research-writing-advisor for
  craft-level writing; research-integrity-reproducibility-advisor for integrity/reproducibility); and
  extended `role` to state why empirical-methods/evaluation review belongs inside the career remit
  (methodological soundness as research survival, per Cohen/Hamming).
- `provenance-ledger.md`: relabelled the advice-only **boundary** rows (`forbidden_behaviours[0-2]`,
  `handoff_rules[0-2]`) as structural house-policy citing the topically-nearest principle for provenance
  rather than as literal source restatements of advisor-vs-researcher ownership.

## [1.1.0] — 2026-07-25

### Changed
- Re-authored all 8 skill bodies to the GOLD shape: added a trigger-oriented `description:`
  frontmatter field to each (progressive-disclosure routing signal), rewrote every
  "Anti-patterns to flag" bullet as a complete, standalone observable-failure-symptom sentence
  (one per provenance principle — replacing character-truncated substrings), and expanded the
  bare one-line Procedure steps to carry their concrete criteria. `provenance:` blocks (and
  `authored_from_digest`) preserved verbatim.
- `evaluation-metrics-and-research-judgment` and `writing-and-publishing-scientific-work`:
  restored the anti-pattern bullet for the previously-dropped principle (P038 and P046).
- `profile.yaml`: weakened `quality_bar[2]` to restore P010's tie-break hedge (established
  reputation used only when protection factors are comparable — was flattened to "not prestige");
  shortened the `role` closing to a pointer to remove ~40 words duplicating `forbidden_behaviours`;
  narrowed `when_to_use[3]` to the strategy slice this advisor owns and added a `when_not_to_use`
  handoff pointer to `research-writing-advisor` for craft-level writing.

### Added
- `profile.yaml` `router_description:` (≤320 chars) covering all five `when_to_use` domains plus the
  core advice-only exclusion, so the exported adapter description no longer under-covers scope.

## [1.0.0] — 2026-07-25

### Added
- Initial release of the **research-career-advisor** subagent (Tier 2), authoring the LLM layer over the
  already-assembled, deterministically-valid distilled spine (48 principles
  P001-P048 / 611 claims from four distillation-only sources).
- `profile.yaml` derived from the 48 promoted principles: role, when/when-not-to-use, three
  modes (advise / review / plan), quality bar, forbidden behaviours, handoff rules, and a
  8-skill / 2-reference `knowledge_partition` covering every principle exactly
  once.
- 8 authored skills partitioning all 48 principles; 2 references
  (principles index + evidence notes).
- `reports/faithfulness-report.yaml` — every load-bearing profile rule graded WITHIN_SCOPE against
  its principles (no rule stronger than its evidence).
- `tests/golden-tests.yaml` (7 golden, 2 negative-routing,
  2 missing-context) and `tests/principle-behaviour-tests.yaml` (one behaviour test per
  principle, 48 total).
- Claude Code adapter exported to `adapters/claude-code/` and installed under
  `.claude/agents/generated/`.

### Grounding
- Four distillation-only sources: *A PhD Is Not Enough! A Guide to Survival in Science* (Peter J.
  Feibelman, 2011); *The Art of Doing Science and Engineering* / *You and Your Research* (Richard W.
  Hamming, 1997); a Chinese guide to succeeding in academic research; and *Empirical Methods for
  Artificial Intelligence* (Paul R. Cohen, 1995).
