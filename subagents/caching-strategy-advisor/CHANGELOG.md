# Changelog — caching-strategy-advisor

## 0.6.0 — 2026-06-28

### Changed

- **Deeper map→reduce spine.** The distilled spine was rebuilt from *Caching at Scale With Redis*
  (Lee Atchison, 2021; `caching-at-scale-wit-11ebbc81`, distillation-only) to **123 claims** and
  **38 principles** (`P001–P038`; 22 high-confidence, 16 medium) with **119 evidence records**,
  superseding the earlier 10-principle (`P001–P010`) spine. The spine was assembled
  deterministically and not hand-edited.

### Added

- **Re-authored LLM layer over the new spine:**
  - `tests/behaviour-tests.yaml` regenerated so every high-confidence principle has a golden test
    (76 golden + 38 missing-context cells across the 38 principles).
  - `tests/principle-behaviour-tests.yaml` rewritten — one behaviour test citing each of the 22
    high-confidence principles, plus side-effect negatives.
  - `tests/golden-tests.yaml` scenario tests re-aligned to cite the correct new principle IDs.
  - `provenance-ledger.md` and this `CHANGELOG.md` re-authored for the 38-principle build.

### Fixed

- **Adapter invariant layer.** Re-exported the Claude Code adapter so its must-hold invariant layer
  covers all 22 high-confidence, profile-rule principles (previously only `P001–P010`'s six
  high-confidence rules were enforced). `agent_version` bumped `0.5.2 → 0.6.0`.
- Profile rules, the five skills, three references, and the faithfulness report were verified
  consistent with the new spine; grounding verified unchanged by the package validator.

## 0.5.x — 2026-06-28

- Earlier map→reduce baseline over the same source with a 10-principle (`P001–P010`) spine.
  Its per-version history was not preserved across the rebuild that produced the current
  38-principle spine.
