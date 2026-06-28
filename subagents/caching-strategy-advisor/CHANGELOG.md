# Changelog — caching-strategy-advisor

## 0.5.2 — 2026-06-28

### Added

- **`provenance-ledger.md`** and **`CHANGELOG.md`**, restoring the package bookkeeping layer that
  was lost when a fresh per-book map→reduce rebuild overwrote `subagents/caching-strategy-advisor/`.

### Changed

- Bumped `agent_version` `0.5.1 → 0.5.2` and re-exported the Claude Code adapter to carry the new
  version. The distilled spine (123 claims, 10 principles `P001–P010`), profile rules, five skills,
  three references, tests, and faithfulness report are unchanged; grounding verified unchanged by
  the package validator.

## 0.5.1 — 2026-06-28

### Added

- **Map→reduce rebuilt baseline** grounded in *Caching at Scale With Redis* (Lee Atchison, 2021;
  `caching-at-scale-wit-11ebbc81`, distillation-only).
- **Distilled spine** assembled deterministically by the per-book map→reduce build: 123 claims
  (`C#####`), evidence records, and 10 principles (`P001–P010`; 6 high-confidence, 4 medium), with
  chunk anchors (`<sha12>-cNNNN`). The spine was not hand-edited.
- **Profile** with `advise` / `compare` / `validate` modes, quality bar, and forbidden behaviours,
  each rule citing the principles it is grounded in. Source-of-truth precedence: official Redis
  docs supersede the book for `maxmemory-policy` names, module availability, and cloud tiers; the
  book governs architectural reasoning and the cache-performance formula.
- **Skills (5)** — `cache-performance-break-even`, `eviction-policy-selection`,
  `cache-invalidation-design`, `ttl-selection`, `active-active-conflict-assessment` — and
  **references (3)** — `redis-maxmemory-policy-cheatsheet`, `scaling-technique-summary-table`,
  `cache-performance-formula-sheet` — each grounded in real principle / claim / chunk-anchor IDs.
- **Tests** — `golden-tests.yaml` (positive + negative routing) and
  `principle-behaviour-tests.yaml` covering every high-confidence principle.
- **Faithfulness report** grading each gradable profile rule against the evidence and chunk
  anchors; no rule stronger than its source. Distillation-only source — no verbatim quotation.
- **Claude Code adapter** exported from the profile.

> The 0.x line predating this rebuild is not itemised: its per-version history was not preserved
> when the map→reduce rebuild overwrote the package directory.
