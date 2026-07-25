# Changelog — product-blueprint-reviewer

All notable changes to this generated subagent package are recorded here. The canonical source of
truth is `profile.yaml`; the installed adapter is a derived artifact.

## [1.0.1] — 2026-07-25

### Added
- `router_description` in `profile.yaml`: the adapter frontmatter `description` is the string the
  runtime routes on, and without this field the exporter composes it from the role plus only the
  first two `when_to_use` triggers and the first `when_not_to_use` exclusion — silently dropping the
  remaining domains. The authored description names the full remit and boundary. Adapter
  re-exported; no principle, rule, or skill changed.

## [1.0.0] — 2026-07-06

### Added

- Initial authored layer over the deterministic map→reduce distilled spine (527 globally-renumbered
  claims, 520 evidence records, 191 principles — 63 high-confidence — and chunk/paragraph anchors
  across four sources).
- `profile.yaml` — product-blueprint-reviewer role synthesized from the 191 principles, with
  `when_to_use`/`when_not_to_use`, three modes (review/advise/compare), a five-check quality bar,
  forbidden behaviours, knowledge partition (six skills, two references), and two worked examples
  (happy-path + failure-recovery); `tier: 2`, `status: ready`, `multisource_synthesis: deferred`.
- `reports/faithfulness-report.yaml` — per-rule claim-strength review of every load-bearing profile
  rule against the principles/claims/evidence; no rule stronger than its evidence.
- Six authored skills under `skills/`, each grounded in a cluster of principles and their backing
  claims, evidence, and anchors: `blueprint-altitude-and-neutrality`,
  `outcomes-over-output-and-build-trap`, `lean-startup-hypothesis-discipline`,
  `research-to-blueprint-and-gap-classification`, `stage-routing-and-pipeline`, and
  `product-experience-and-ux-architecture-boundary`.
- Two authored references under `references/`: `blueprint-principles-index.md` (all 191 principles
  grouped by the six themes) and `stage-routing-decision-guide.md` (the RUN/SKIP/DEFER/ASK_USER
  vocabulary, the dependency-aware stage-recommendation record, per-stage routing signals, and the
  routing-complexity heuristic).
- `tests/principle-behaviour-tests.yaml` — one behaviour test per high-confidence principle (63
  tests); `tests/golden-tests.yaml` — eight golden, three negative-routing, and four missing-context
  routing tests.
- Stamped `provenance.authored_from_digest` drift baselines into all six skills and two references
  (Step 9 drift-tracking).
- Exported and installed the Claude Code adapter:
  `adapters/claude-code/product-blueprint-reviewer.md` and
  `.claude/agents/generated/product-blueprint-reviewer.md`.

### Fixed

- `sources/metadata/*.metadata.json`: corrected `source_type` from the non-schema token `md` to the
  schema enum value `markdown` (the sources were ingested as Markdown). Schema-compliance correction
  only — no distilled content, hash, or anchor changed.

### Sources

- Product Blueprint and Stage-Boundary Skill Contract — `distillation-only`.
- Architecture and UX Stage Boundaries — `distillation-only`.
- Escaping the Build Trap — Melissa Perri (2018), `distillation-only`.
- Lean Startup in Technology-Driven Teams — Katila et al. (2020), `distillation-only`.
