# Per-book authoring upgrade (map → reduce)

**Status:** proposed (draft — to be refined). Motivated by the confirmed per-run extraction-dilution
finding (`docs/output-quality-eval.md`): a single author pass over N books extracts far fewer
claims **per book** than per-book passes (software-architecture batch 1/3/5 → 34 / 12.3 / 9.0
claims/book). Strengthening via incremental add-source already beats full re-author (devops 72→101,
arch 24→42). So the factory should **extract each book on its own, persist that, and merge** — for
*creation*, not just updates.

## Idea
A **map → reduce** authoring pipeline:
- **map:** extract each book's claims/principles/evidence in its own full pass (no dilution),
  persist content-addressed (by sha) so it is reusable, resumable, and incremental-for-free.
- **reduce:** merge a *set* of per-book extracts into one package — dedup, cross-source principle
  promotion, Phase-7 conflict resolution, faithfulness, ID renumbering, profile build.

The hard, valuable part is the **reduce (merge)**, not the map. Merge must *synthesize and prune*,
not just accumulate — piling claims yields a bloated, incoherent package (more claims ≠ better
advice; advice quality is judge-dependent — see output-quality-eval).

## Current vs vision
| | Current | Vision |
|--|--|--|
| Create | **batch** — extract all N in one pass → dilutes | per-book map → merge |
| Update | `add-source` (incremental) — already a 1-book map + merge (proven) | same, generalized to N |
| Source attribution | ✅ claims carry `source_id` | ✅ |
| Ingest cache | ✅ sha-keyed markdown | extend to per-book *extract* cache |
| Merge logic | partial — `add-source`/`subagent-maintenance` append-one + Phase-7 conflicts | **N-way merge** |
| Per-book extract store | ❌ extracts live inside a package | **new:** `cache/book-extracts/<sha>/` |
| Gate | ✅ `cli grounding-richness` (deterministic) | reuse |

Key: the incremental `add-source` path is **already** "process a book separately + merge" and works
— the upgrade makes that the default for creation, with a persistent per-book cache + N-way merge.

## Plan (phased — prototype, don't big-bang)
- **P0 — prototype (do first):** minimal P1+P2; rebuild ONE existing package (software-architecture)
  via map→merge; compare grounding-richness to its current batch v0.3.0. Adopt only if it clearly
  wins (it should, per the experiment).
- **P1 — per-book extract cache:** extract each book in its own pass → persist
  `cache/book-extracts/<sha>/{claims.jsonl, principles.yaml, evidence-records.yaml}`. Keyed by book
  sha → reused across packages, resumable, incremental adds become free.
- **P2 — N-way merge/assemble:** compose a package from a set of cached extracts (dedup,
  cross-source principle promotion, conflict resolution, faithfulness, ID renumber, profile). Reuse
  + generalize the existing `add-source`/maintenance merge from append-one → merge-N.
- **P3 — switch + gate:** `author-subagent` create = map → reduce; update = add book→cache +
  re-merge; gate every assembly on `grounding-richness` growing.

## Caveats / open questions (to resolve in refinement, step (c))
- **Merge is the real engineering + risk** (dedup / conflict / cross-source / IDs / faithfulness).
- Maximizes grounding *richness*, not proven advice quality → merge MUST prune/synthesize or the
  package bloats and may advise worse. How does merge decide what to keep/drop?
- Cost: N extraction passes vs 1 — but cached + reusable + parallelizable (incremental adds free).
- Cross-source synthesis: currently `multisource_synthesis: deferred`. Does the merge subsume Step 7,
  or stay separate?
- Big change to the core pipeline → P0 prototype + richness comparison de-risks before adoption.
- ID scheme: per-book extracts need stable local IDs that the merge renumbers without breaking
  provenance/faithfulness anchors.
