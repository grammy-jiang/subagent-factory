# software-design Rebuild — STATUS (DONE)

**Branch:** `rebuild/software-design` (pushed to origin; master untouched)
**Date:** 2026-06-24
**Outcome:** calibrated 0.25x rebuild shipped as **v1.0.0**, validate PASS, pushed.

## Headline numbers
- **0.25x principle count: 34** (down from 134 uncalibrated) — 886 claims → 34 principles → 291 evidence.
- `validate_generated_package`: **PASS (0 fail, 0 warn)** at every phase after P1.
- Faithfulness: 25 verdicts, all ≤ source support (6 EXACT_SUPPORT, 19 WITHIN_SCOPE, 0 over-claims). quote_scan PASS.

## COST GUARD — honored (zero re-MAP, zero LLM spend)
- All 5 cached books had `principles.yaml` present → MAP gate cache-hit. `decisions.json` present → filter gate satisfied.
- Build ran `--resume --select 0.25` end-to-end deterministically (route/chunk/map/anchors/reduce-emit all `[skip]`, only `assemble` ran). No `map_book.sh` / precision-filter LLM call triggered.
- Used `--sources campaign/software-design.sources` (sha-matched cache), never the anchor-injected package markdown.
- NOTE: cached clean-code MAP (5b1b9ca3) holds **0 principles** (a prior partial MAP); cost-guard forbids re-MAP so it was reused as-is. The other 4 books supplied the pool. Clean Code is still represented in claims/skills/refs via its claims.

## Phases / SHAs (all committed, pushed)
| Phase | SHA | What |
|---|---|---|
| P1 | `ba63738` | calibrated 0.25x spine (134→34 principles), cached MAP |
| P2 | `dc9963f` | reground authored layer (8 skills, 5 refs, profile, tests) onto new spine — survivors keep ids, 100 dropped ids → nearest survivor (MiniLM + curated overrides); bodies unchanged; digests re-stamped |
| P3 | `6aea651` | Step-16 GRADE blocks on all 34 (confidence == grade level, 0 mismatch) |
| P4 | `70fb779` | Step-13 ask-gate: applies_when cues on all 34 + behaviour-tests.yaml (68 golden incl 34 twins, 34 missing-context) |
| P5 | `25b6d97` | faithfulness verified (≤ source support) + quote_scan PASS; test-results.md refreshed |
| P6 | `68c138a` | Step-7 C-track: 4 cross-source clusters (each ≥2 sources), 18-edge graph, 1 resolved conflict, conflict-log.md |
| P7 | `94870d3` | ship v1.0.0: version bump, CHANGELOG + provenance, adapter re-exported (canonical+installed), complete rights-clean package tracked |

## Validation (final)
- `validate_generated_package subagents/software-design` → **VALIDATION PASSED** (0 fail, 0 warn).
- `validate_principle_clusters` → OK. `validate_principle_graph` → OK. `validate_confidence_grade` → OK.
- Adapter `Profile version: 1.0.0` synced; `DO NOT EDIT` header present.

## Reuse achieved
- Cached per-book MAP reused (no re-extraction).
- v0.3.1 authored layer regrounded, not re-authored — skill/reference **bodies unchanged**, only principle citations remapped.

## Remaining / open
- None blocking. Branch ready for review/merge to master (PR URL printed on push).
- Optional future: re-MAP clean-code (5b1b9ca3) once a cap window allows, to recover its dropped principles into the pool (would change ids → full re-reground).

SD REBUILD DONE: rebuild/software-design ba63738 dc9963f 6aea651 70fb779 25b6d97 68c138a 94870d3
