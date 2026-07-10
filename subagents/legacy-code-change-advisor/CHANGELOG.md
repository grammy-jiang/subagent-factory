# Changelog — Legacy Code Change Advisor

All notable changes to this generated subagent package are recorded here.

## [0.3.0] — 2026-07-11

### Changed
- Re-authored the whole LLM layer onto the map→reduce-rebuilt distilled spine: the
  principle set grew from 12 (P01–P12) to **145 principles (P001–P145)** derived from
  **582 globally-renumbered claims (C00001–C00582)** over source
  `robert-c-martin-seri-1d83dc6f`. The prior authored layer referenced the retired
  `P01–P12` / `C001–C024` / heading-anchor scheme and no longer resolved.
- `profile.yaml`: `sources[]` retargeted to `robert-c-martin-seri-1d83dc6f`
  (sha `1d83dc6f489c…`); every prose principle citation and the source-of-truth
  precedence remapped to current IDs; `agent_version 0.2.0 → 0.3.0`.
- All 7 skill bodies and both reference bodies re-grounded: `provenance` now carries
  real current principle/claim/chunk-anchor (`<sha12>-cNNNN`) IDs; inline citations
  remapped to the new scheme.
- `reports/faithfulness-report.yaml`: regenerated — 22 findings over the current
  gradable profile rules, each at/within source support (no over-claim);
  `source_anchors` omitted (notes carry provenance).
- `tests/principle-behaviour-tests.yaml`: regenerated to one test per principle
  (145), covering every high-confidence principle (115) for the principle→test gate.
  `tests/golden-tests.yaml`: `source_id`, `profile_version`, and `principle_coverage`
  refreshed to current IDs.
- Adapter re-exported; the `## Operating invariants (must hold)` layer now compiles
  all 115 high-confidence must-hold principles.

## [0.2.0] — 2026-06-15

### Added
- Authored all 7 skill bodies (cover-before-change, legacy-code-change-algorithm,
  sensing-and-separation, seam-model, characterization-testing, sprout-and-wrap,
  effect-reasoning) and both reference bodies (dependency-breaking-techniques,
  legacy-code-glossary) from the package's own principles/claims/evidence
  (Step 8 `author-skills`). Each body carries real `provenance` principle/claim/
  source-anchor IDs and a stamped `authored_from_digest` drift baseline.

### Changed
- `status: draft → ready`; all `STATUS: STUB` markers removed.
- Passes `validate_skill_authoring`, `quote_scan` (no verbatim), and `cli validate`.

## [0.1.0] — 2026-06-15

### Added
- Initial package authored from *Working Effectively with Legacy Code* (Michael
  C. Feathers, 2005, Prentice Hall PTR), rights `distillation-only`.
- Tier-1 evidence chain: 24 claims (C001–C024), 24 evidence records, importance
  scores (all keep), and 12 principles (P01–P12).
- `profile.yaml` with modes advise / review / extract / patch-suggest, grounded
  in principles P01–P12.
- `tests/golden-tests.yaml` (3 golden, 2 negative-routing, 1 missing-context) and
  `tests/principle-behaviour-tests.yaml` (one test per principle).
- `reports/faithfulness-report.yaml` (Tier-1, vs evidence records; no over-claim).
- `policy/patch-policy.yaml` (patch-suggest mode → suggest-only default).

### Status
- `status: draft` — knowledge-partition skills and references are stubs
  (`STATUS: STUB`). Re-run with `--author-skills` to author bodies and promote to
  `ready`.
