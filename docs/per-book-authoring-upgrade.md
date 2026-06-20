# Per-book authoring upgrade (map → reduce, checkpointed)

**Status:** proposed design (refined 2026-06-20 — added engine routing, context-window budgeting, determinism boundary). Motivated by the **confirmed** per-run
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

## Determinism boundary (factory invariant)
**Anything deterministic is a script — Python or bash under `tools/subagent_factory/` or `campaign/` —
never an LLM prompt.** The LLM is spent only on *irreducible judgment*: reading a book into claims,
promoting claims into principles, resolving a semantic conflict, authoring a skill body. Everything
else is code:

- staging (pymupdf4llm md), tokenizing, **book routing** (`route_books.py`), input fingerprinting;
- dedup (token-F1 `claim_recall`), ID renumber, old→new ID maps;
- checkpoint / `.done` management, atomic write (`*.tmp`→fsync→rename), resume selection;
- manifest / `steps.log.jsonl` assembly, profile assembly from chosen fields, all validation.

Why it is a hard rule: **cost** (no premium-requests or tokens burned on mechanical work),
**reproducibility** (same input → same output; re-runs are free and identical), **auditability**
(a script's logic is reviewable; an LLM's is not), and **context economy** — scripts pass compact
artifacts between steps instead of dragging transcripts, which is exactly what keeps each LLM prompt
inside the 200k window (see *Engine assignment & context routing*). Each pipeline step is therefore
tagged **DET** (script) or **LLM** (judgment); DET steps never consume an engine budget.

## Checkpoint / resume / portability
Every step persists its output + an atomic completion marker, so a failure (e.g. monthly cap / 429)
resumes from where it stopped, and a full copy resumes on another machine.

```
cache/book-extracts/<book-sha>/        # MAP — content-addressed (reusable across packages AND machines)
  source.md
  claims.jsonl  +claims.done    evidence.yaml +evidence.done
  principles.yaml +principles.done    faith.yaml +faith.done
  module.json    # {sha, title, per-step status@ts, engine, machine, ctx_tokens_in, cost, compacted, schema_ver}

subagents/<slug>/.build/               # REDUCE — per package
  inputs.json    # ordered book-sha set this package is built from
  merged-principles.yaml +.done    conflicts.yaml +.done
  faithfulness.yaml +.done    profile.yaml +.done    skills/ +.done
  build.json     # per-step status, engine, machine, ctx_tokens_in, cost, compacted, timestamps
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

**Logging:** `steps.log.jsonl` (`{ts, step, sha-or-slug, status, engine, machine, ctx_tokens_in,
compacted, cost, rc, output_count, error}`) = audit + run ledger; plus existing per-step transcripts
under `campaign/logs/`.

## Engine assignment & context routing
Two engines, two cost models, two context windows. Three forces decide where each step runs.

| Force | Pull |
|-------|------|
| extraction dilution (engine-independent — measured all-Claude) | **one book per unit** — never batch books into a prompt |
| Copilot cost = **premium requests** (one opus-4.8 prompt ≈ 27, regardless of work inside; real cap = 5h / weekly window, like Claude Code) | **whole MAP per prompt** — fewest, biggest prompts win |
| context window (Copilot ~200k vs Claude ~1M; **compaction degrades output**) | prompt input must fit **with headroom — no compaction** |

Cost wants big prompts; context caps prompt size. Resolution: **size each Copilot prompt to the
largest that still fits 200k uncompacted = one *small* book's whole MAP.** The context window becomes
the router.

**Routing rule** — measure each book's staged-markdown token count:
- **Small book (md ≤ ~100k tok)** → **Copilot**, whole MAP in one prompt (claims → evidence →
  principles → faith → test-seeds). Fits 200k with output headroom; cost-optimal (one premium-request
  unit buys the whole book).
- **Large book (md > ~100k tok)** → **Claude** (~1M), whole MAP in one prompt. No chunking, no compaction.
- **REDUCE + global faithfulness** run on **distilled principles + evidence records** (never raw book
  text) → compact (tens of k tokens) → fit either engine; default Claude (serial critical path), or
  Copilot to balance windows.

The three forces align: small books are *both* cheap and fitting on Copilot; large books need Claude
regardless; REDUCE is light in cost *and* context — the deep-MAP / light-REDUCE split pays off again.

**Stateless artifact-passing — the linchpin that makes 200k viable.** Every step reads its declared
input *artifacts from disk*, never the conversation transcript. Per-prompt context = system prompt +
that step's inputs + its output — bounded and *computable*, never the accumulated history.
- The faith step reads `claims.jsonl` + `evidence.yaml`, not the claims-extraction transcript.
- Only the raw-claims step ever loads a whole book — so it is the only context-binding step, and the
  only one the size-router gates.
- Each step records a **context budget** (`ctx_tokens_in`); the router proves the step fits the target
  engine *before* dispatch. **Compaction is a hard gate, not a soft preference** — no step runs on an
  engine where input + output won't fit with headroom.

This is the same stateless contract that already gives resume + portability: a step depends only on
on-disk artifacts, so it can run on any engine, any machine, at any time.

**Step → input artifact → engine (with determinism tag):**

| Step (phase) | Input artifact (size) | LLM / DET | Engine |
|------|------|------|------|
| claims (MAP) | book md (**variable**) | LLM | **size-routed** (≤ ~100k → Copilot, else Claude) |
| evidence (MAP) | claims.jsonl (small) | LLM | either |
| principle promotion (MAP) | claims + evidence (small) | LLM | either |
| faith pre-check (MAP) | principles + evidence (small) | LLM | either |
| test seeds (MAP) | principles (small) | LLM | either |
| dedup / merge principles | all principles (small) | **DET** (`claim_recall` token-F1) | script — no LLM |
| conflict resolution | merged principles (small) | LLM | Claude (serial) |
| ID renumber | merged (small) | **DET** | pure script |
| global faithfulness | merged + evidence (small) | LLM | **opposite engine** (independent judge; one prompt, all books) |
| profile assembly | merged + decisions (small) | **DET** (`profile-deriver`) | script |
| skills authoring | merged (small) | LLM | Claude (or Copilot per-skill) |

Whole-book-MAP-in-one-prompt (small book): the claims row loads the md once; the later MAP rows reuse
it in-context — it fits because md ≤ ~100k leaves room for the accumulating output.

**Window-drain handoff.** Copilot runs its small-book queue until its 5h / weekly window nears
exhaustion; Claude then drains the remainder (any size), starting each book from its `.done` markers.
The content-addressed cache *is* the handoff — a window-truncated book resumes exactly where it
stopped, on either engine.

**Independent judge, cheaply.** Per-book faith folded into the book-MAP prompt is the same engine
reviewing its own claims (free, but not independent). Buy independence once, at the merge layer: run
**global faithfulness on the opposite engine** from whoever did most of the MAP — one prompt, all
books, a cross-family judge.

**Logged for both cost models.** `ctx_tokens_in`, `cost` (premium-requests for Copilot / tokens for
Claude), and `compacted` are recorded per step (see *Logging* above), so a run is auditable against
*either* billing model and any compaction event — a quality risk — is visible after the fact.

## Resolved open questions
| Question | Answer |
|----------|--------|
| Avoid bloat? | REDUCE dedups (multi-anchor) + merges globally → synthesize, not accumulate |
| Subsume Step 7? | Yes — global principle merge is the cross-source synthesis |
| ID scheme? | faithfulness anchors are (sha+offset) — stable; merge renumbers CL/PR with an old→new map |
| Cost? | extraction cached by sha → never re-run; only the lighter REDUCE re-runs on add; maps parallel |
| Cap/restart? | per-step `.done` checkpoints + `--resume` + content-addressed modules → cap-tolerant, portable |
| Net-new code? | REDUCE largely orchestrates existing tools (`claim_recall` dedup, `principle-promotion`, `seed_principle_clusters`/`principle-graph`, `faithfulness-review`, `profile-deriver`) over the merged set |
| Which engine? | size-route per book: md ≤ ~100k → Copilot (whole MAP, 1 prompt); larger → Claude (1M); REDUCE on distilled artifacts → either |
| Context limits? | stateless steps read compact input artifacts, not transcripts → per-prompt context bounded + computed; compaction is a hard routing gate |
| Deterministic work? | every deterministic step is a script (Python/bash); LLM only for irreducible judgment — see *Determinism boundary* |

## Plan (phased — prototype, don't big-bang)
**Determinism-first throughout:** each phase ships its mechanical work as a script
(`tools/subagent_factory/` or `campaign/`) before any LLM step wraps it (see *Determinism boundary*).

- **P0 — prototype (first):** minimal per-book module + N-way principle merge; rebuild ONE package
  (software-architecture, 9 books) via map → reduce. Measure: (1) `grounding-richness` (principles)
  vs the current batch v0.3.0 — adopt only if it clearly wins; (2) same *small* book, Copilot-MAP vs
  Claude-MAP richness — equal ⇒ Copilot is a full MAP worker; (3) **zero `compacted=true`** on any
  Copilot prompt; (4) REDUCE distilled-artifact input stays < 200k.
- **P1 — per-book module + content-addressed cache** (`cache/book-extracts/<sha>/`, per-step `.done`)
  + `route_books.py` (deterministic: tokenize staged md → small/large → per-book engine assignment).
- **P2 — N-way merge/assemble** (dedup→multi-anchor principles, conflicts, IDs, faithfulness, profile,
  skills) under `subagents/<slug>/.build/` with `.done` checkpoints — every deterministic step a script.
- **P3 — switch + gate + resume:** `author-subagent` create = map→reduce; update = add book→cache +
  re-merge; `build --resume`; window-drain handoff (Copilot small-book queue, Claude drains the rest);
  gate every assembly on grounding-richness growing.

## Residual risks
- **Dedup threshold tuning** — too aggressive merges distinct principles; too loose keeps redundancy. Calibrate on real data.
- **Global principle merge is one pass** — lighter than extraction, but if it dilutes too it may need chunking; the P0 prototype will show.
- Still **grounding-not-advice** — richer grounding; advice gain unproven (merge coherence is the lever).
- Core-pipeline change → P0 prototype + richness comparison de-risks before adoption.
- **Routing threshold (~100k tok)** — too high → Copilot compaction (silent quality loss); too low → Copilot underused. Tune from measured staged-md sizes; the `compacted` flag catches misses.
- **Copilot MAP depth unverified** — assumed equal to Claude on small books; P0 measures it before the split is trusted.
