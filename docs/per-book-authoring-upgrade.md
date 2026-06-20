# Per-book authoring upgrade (map → reduce, checkpointed)

**Status:** proposed design (refined 2026-06-20). Motivated by the **confirmed** per-run
extraction-dilution finding (`docs/output-quality-eval.md`): one author pass over N books extracts
far fewer claims **per book** than per-book passes (software-architecture batch 1/3/5 →
34 / 12.3 / 9.0 claims/book). Incremental `add-source` already beats full re-author (devops 72→101,
arch 24→42). So the factory should **extract each book on its own, persist it, then merge** — for
*creation*, not just updates — and the whole pipeline should be **resumable, portable, cap-tolerant**.

## Architecture — deep MAP, light REDUCE
The dilution lives in **claim extraction from raw book text**; promotion over already-extracted
**claims** is light. And `add-source` already proves "extract one book → promote → merge". So push
the deep work per-book; keep the global step thin.

```
per book → claims → evidence → principles → faith-check        ← MAP  (deep, cached by sha, parallel)
all books → merge/dedup principles → conflicts → renumber
          → global faithfulness → profile → skills              ← REDUCE (light, global)
```

**MAP (per book — a self-contained "book module", content-addressed by sha):**
claims → evidence records → principle promotion → per-book faithfulness pre-check → behaviour-test
seeds. Deep per book (no dilution), cached, parallelizable, reusable across packages/machines.

**REDUCE (global, light):** merge/dedup principles across books (same principle from 2 books → one
**multi-anchor** principle = strengthened), conflict resolution (Phase-7 classes), ID renumber,
global faithfulness re-check, profile, skills. Claims stay **per-book** (cleaner provenance); the
deduped layer is **principles** — so measure grounding-richness by **principles** + per-book claims.

### What moved to per-book (vs the first draft) and why it's safe
| step | now | why |
|------|-----|-----|
| evidence records | per-book | per-claim → belongs to its book |
| principle promotion | per-book | deeper per book, cached, parallel; `add-source` already does it |
| faithfulness pre-check | per-book (+ global re-check) | each book's principles vs its own evidence |
| test seeds | per-book | one principle → one test |

**Stays global (genuinely cross-book):** principle dedup/merge, conflict resolution, ID renumber,
profile, skills, final faithfulness.

### The one trade-off
Promoting per-book means an **emergent cross-source principle** (one that exists in *no* single book,
only by combining A+B claims) won't form. But the common case (same principle in multiple books) is
captured by the **dedup→multi-anchor** merge, and the emergent case *is* Step-7 synthesis, which we
**defer anyway**. So little lost; much gained (fully cached/parallel per-book modules; thin REDUCE).
→ The merge **subsumes** Step 7: global principle promotion/merge over per-book principles is the
cross-source synthesis; `principle-clusters/graph` become its byproduct (no longer "deferred").

## Checkpoint / resume / portability
Every step persists its output + an atomic completion marker, so a failure (e.g. monthly cap / 429)
resumes from where it stopped, and a full copy resumes on another machine.

```
cache/book-extracts/<book-sha>/        # MAP — content-addressed (reusable across packages AND machines)
  source.md
  claims.jsonl  +claims.done    evidence.yaml +evidence.done
  principles.yaml +principles.done    faith.yaml +faith.done
  module.json    # {sha, title, per-step status@ts, engine, machine, schema_ver}

subagents/<slug>/.build/               # REDUCE — per package
  inputs.json    # ordered book-sha set this package is built from
  merged-principles.yaml +.done    conflicts.yaml +.done
  faithfulness.yaml +.done    profile.yaml +.done    skills/ +.done
  build.json     # per-step status, engine, machine, timestamps
  steps.log.jsonl  # append-only: one line per step-attempt
```

**Resume semantics (idempotent, skip-done):** a `build <slug> --resume` runner reads `inputs.json`
+ `.done` markers → runs only missing/failed steps.
- MAP: per book sha, run only module steps lacking `.done`; a fully-done book is skipped (never recomputed).
- REDUCE: resume from the first step without `.done`.
- **Cap-hit example:** `merged-principles` 429s → no `.done` → next `--resume` restarts *at*
  `merged-principles` (claims-merge skipped, all book modules skipped). No lost work.

**Portability:** `cache/book-extracts/` is content-addressed by sha → identical on any machine. Copy
`cache/` + `subagents/<slug>/.build/` (or the whole repo) → another machine resumes exactly. Maps can
run on machine A, REDUCE on B.

**Two correctness rules so resume is safe:**
1. **Atomic completion** — write output to `*.tmp` → fsync → rename → *then* write `.done`. A killed
   step leaves `*.tmp`, never a false `.done`.
2. **Input fingerprinting** — each `.done` records its inputs' sha; if an upstream output changed,
   downstream `.done` is invalidated → re-runs (no stale resume).

**Logging:** `steps.log.jsonl` (`{ts, step, sha-or-slug, status, engine, machine, rc, output_count,
error}`) = audit + run ledger; plus existing per-step transcripts under `campaign/logs/`.

## Resolved open questions
| Question | Answer |
|----------|--------|
| Avoid bloat? | REDUCE dedups (multi-anchor) + merges globally → synthesize, not accumulate |
| Subsume Step 7? | Yes — global principle merge is the cross-source synthesis |
| ID scheme? | faithfulness anchors are (sha+offset) — stable; merge renumbers CL/PR with an old→new map |
| Cost? | extraction cached by sha → never re-run; only the lighter REDUCE re-runs on add; maps parallel |
| Cap/restart? | per-step `.done` checkpoints + `--resume` + content-addressed modules → cap-tolerant, portable |
| Net-new code? | REDUCE largely orchestrates existing tools (`claim_recall` dedup, `principle-promotion`, `seed_principle_clusters`/`principle-graph`, `faithfulness-review`, `profile-deriver`) over the merged set |

## Plan (phased — prototype, don't big-bang)
- **P0 — prototype (first):** minimal per-book module + N-way principle merge; rebuild ONE package
  (software-architecture, 9 books) via map→reduce; compare `grounding-richness` (principles) to the
  current batch v0.3.0. Adopt only if it clearly wins.
- **P1 — per-book module + content-addressed cache** (`cache/book-extracts/<sha>/`, per-step `.done`).
- **P2 — N-way merge/assemble** (dedup→multi-anchor principles, conflicts, IDs, faithfulness, profile, skills) under `subagents/<slug>/.build/` with `.done` checkpoints.
- **P3 — switch + gate + resume:** `author-subagent` create = map→reduce; update = add book→cache +
  re-merge; `build --resume`; gate every assembly on grounding-richness growing.

## Residual risks
- **Dedup threshold tuning** — too aggressive merges distinct principles; too loose keeps redundancy. Calibrate on real data.
- **Global principle merge is one pass** — lighter than extraction, but if it dilutes too it may need chunking; the P0 prototype will show.
- Still **grounding-not-advice** — richer grounding; advice gain unproven (merge coherence is the lever).
- Core-pipeline change → P0 prototype + richness comparison de-risks before adoption.
