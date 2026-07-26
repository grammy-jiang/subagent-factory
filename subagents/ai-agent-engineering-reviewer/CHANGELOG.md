# Changelog

## [0.3.1] — 2026-07-25

### Added
- `router_description` in `profile.yaml`: the adapter frontmatter `description` is the string the
  runtime routes on, and without this field the exporter composes it from the role plus only the
  first two `when_to_use` triggers and the first `when_not_to_use` exclusion — silently dropping the
  remaining domains. The authored description names the full remit and boundary. Adapter
  re-exported; no principle, rule, or skill changed.

## [0.3.0] - 2026-07-03

- Rebuilt the LLM-authored layer to match the current 60-principle spine after it was left missing/stale by the map→reduce assemble: reconstructed `source-pack.manifest.yaml` from the eight source metadata records, hand-derived `profile.yaml` (role, scope, five principle-cited quality bars, eight always-on knowledge buckets covering all 60 principles), and regenerated the faithfulness report and test suites.
- Authored eight thematic knowledge skills (memory/reflection, reasoning-and-acting loops, tool use/augmentation, RAG, safety evaluation, evaluation methods, model cards, design strategy) plus two references (principles index, safety/evaluation evidence notes), each grounded in its principle subset.
- Generated `tests/golden-tests.yaml` (6 golden + 3 negative-routing + 2 missing-context) and `tests/principle-behaviour-tests.yaml` (one behaviour test per principle; all 40 high-confidence principles covered). Faithfulness report omits `source_anchors` (provenance carried in each note via principle + claim IDs).
- Re-exported the Claude Code adapter; package validates clean.

## [0.2.1] - 2026-07-03

- P2B finish pass: verified the authored layer (profile, faithfulness report, tests, adapter) is consistent with the current 60-principle spine — all 27 profile principle references resolve, all 40 high-confidence principles carry a behaviour test (0 dangling), and every faithfulness `source_anchors` entry is a valid chunk anchor.
- Ran deterministic `repair-faithfulness` (clean: no invalid anchor refs) and re-exported the Claude Code adapter.

## [0.2.0] - 2026-07-03

- Regenerated the profile, faithfulness report, tests, and adapter-facing authored layer from the current principle/evidence spine.
- Set Tier 2 profile metadata and source provenance for the eight-source package.
- Normalized markdown source metadata to the current schema vocabulary.
