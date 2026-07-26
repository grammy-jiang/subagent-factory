# Changelog — product-design-advisor

All notable changes to this generated subagent package are recorded here. The canonical source of
truth is `profile.yaml`; the installed adapter is a derived artifact.

## [0.2.1] — 2026-07-25

### Added
- `router_description` in `profile.yaml`: the adapter frontmatter `description` is the string the
  runtime routes on, and without this field the exporter composes it from the role plus only the
  first two `when_to_use` triggers and the first `when_not_to_use` exclusion — silently dropping the
  remaining domains. The authored description names the full remit and boundary. Adapter
  re-exported; no principle, rule, or skill changed.

## [0.2.0] — 2026-07-03

### Added

- Authored the two remaining stub skills, grounded in their principles, claims, evidence, and source
  anchors: `skills/empowered-product-teams-and-leadership/` (P021, P089, P042, P019, P082, P091,
  P045, P103, P098, P097, P006) and `skills/human-centered-ai-interaction-design/` (P001, P007,
  P017, P056, P026, P052, P110, P022, P015, P014, P005).
- Authored the two reference catalogues: `references/product-principles-index.md` (66
  product-management principles grouped by the seven product skills) and
  `references/human-ai-interaction-guidelines.md` (14 human-centered-AI guidelines grouped by
  control model, tool-not-teammate, user control, mixed-initiative, safety interlocks, evaluation,
  and governance).
- Stamped `provenance.authored_from_digest` drift baselines into all eight skills and two references
  (Step 9 drift-tracking).
- Exported and installed the Claude Code adapter: `adapters/claude-code/product-design-advisor.md`
  and `.claude/agents/generated/product-design-advisor.md`.

### Changed

- Promoted the package from `status: draft` to `status: ready`: every declared skill and reference
  is now authored, faithfulness-reviewed, quote-scanned, and validated.

## [0.1.0] — 2026-07-03

### Added

- Initial authored layer over the deterministic map→reduce distilled spine (globally-renumbered
  claims, 682 evidence records, 110 principles — 87 high-confidence — and chunk/paragraph anchors
  across 11 sources).
- `profile.yaml` — product-design advisor role synthesized from the 110 principles, with
  `when_to_use`/`when_not_to_use`, three modes (review/advise/compare), a five-check quality bar,
  forbidden behaviours, knowledge partition (eight skills, two references), and two worked examples
  (happy-path + failure-recovery); `tier: 2`, `multisource_synthesis: deferred`.
- `reports/faithfulness-report.yaml` — per-rule claim-strength review of every load-bearing profile
  rule against the principles/claims/evidence; no rule stronger than its evidence.
- Six authored skills under `skills/`, plus scaffolded stubs for the remaining two skills and two
  references; each authored body grounded in a cluster of principles and their backing claims,
  evidence, and anchors (the remaining stubs were authored in 0.2.0).
- `tests/principle-behaviour-tests.yaml` — one behaviour test per high-confidence principle (87
  tests); `tests/golden-tests.yaml` — eight golden, three negative-routing, and four missing-context
  routing tests.
- Claude Code adapter export and the `status: ready` promotion were deferred to 0.2.0 (see below);
  0.1.0 remained `status: draft`.

### Fixed

- `sources/metadata/*.metadata.json`: corrected `source_type` from the non-schema token `md` to the
  schema enum value `markdown` (the sources were ingested as Markdown). Schema-compliance correction
  only — no distilled content, hash, or anchor changed.

### Sources

- Inspired: How to Create Tech Products Customers Love — Marty Cagan (2017), `distillation-only`.
- Continuous Discovery Habits — Teresa Torres (2021), `distillation-only`.
- Escaping the Build Trap — Melissa Perri (2018), `distillation-only`.
- User Story Mapping — Jeff Patton (2014), `distillation-only`.
- Shape Up — Ryan Singer (2019), `distillation-only`.
- Lean UX — Jeff Gothelf, Josh Seiden (2016), `distillation-only`.
- Guidelines for Human-AI Interaction — Saleema Amershi et al. (2019), `distillation-only`.
- Principles of Mixed-Initiative User Interfaces — Eric Horvitz (1999), `distillation-only`.
- Human-Centered Artificial Intelligence: Reliable, Safe & Trustworthy — Ben Shneiderman (2020),
  `distillation-only`.
- Human-Centered AI: A New Synthesis — Ben Shneiderman (2021), `distillation-only`.
- Human-Centered AI: Three Fresh Ideas — Ben Shneiderman (2020), `distillation-only`.
