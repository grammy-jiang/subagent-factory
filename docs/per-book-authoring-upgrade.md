# Per-book authoring upgrade (map → reduce, checkpointed)

**Status:** proposed design (refined 2026-06-20 — engine routing, context-window budgeting, determinism boundary; **research-grounded** against 4 prior research reports — see *Research grounding*). Motivated by the **confirmed** per-run
extraction-dilution finding (`docs/output-quality-eval.md`): one author pass over N books extracts
far fewer claims **per book** than per-book passes (software-architecture batch 1/3/5 →
34 / 12.3 / 9.0 claims/book). Incremental `add-source` already beats full re-author (devops 72→101,
arch 24→42). So the factory should **extract each book on its own, persist it, then merge** — for
*creation*, not just updates — and the whole pipeline should be **resumable, portable, cap-tolerant**.

## Architecture — chunk → book → corpus (deep MAP, light REDUCE)
The dilution lives in **claim extraction**; promotion over already-extracted **claims** is light. But
"one book = one prompt" is infeasible for the real corpus (most staged books are 200k–880k tok — over
Copilot's 200k, several over Claude's 1M) **and** degrades extraction even where it fits (flat reading
loses recall past ~800 tok — *long-document-structure-mapping*). So the deep unit is the **chunk** (a
source-map section), not the book: **three levels, not two.**

```
per chunk  → typed claims (+condition/exception/certainty)              ← MAP-inner (deep, structure-aware)
per book   → aggregate claims → evidence → principles → faith-check      ← MAP   (cached by sha, parallel)
all books  → recall-then-filter dedup → split-by-nature reconcile
           → select → renumber → global faithfulness → profile → skills  ← REDUCE (light, global)
```

**MAP (per book — a self-contained "book module", content-addressed by sha).** The claims step is
itself **chunked**: build a part→chapter→section map (`source-structure-mapper`, already in the
factory), extract **with neighbour-context overlap + a global salience pass** (chunk-local extraction
misses boundary-spanning + scattered claims — *long-document*), and emit **typed atomic claims**
(fact / value / policy, provenance-anchored, with nullable `condition`/`exception` and a `certainty`
flag — *argument-mining*). Then per book: evidence records → principle promotion → faithfulness
pre-check → behaviour-test seeds. Deep per book (no dilution), cached, parallel, reusable.

**REDUCE (global, light).** Merge is **recall-then-filter**: deterministic recall (token-F1
`claim_recall` + embedding centroid) proposes equivalence candidates, an LLM **precision filter**
confirms (never invents) — same principle from 2 books → one **multi-anchor** principle. Then
**split-by-nature reconcile** (factual → accuracy-weighted + copy-discounted + multi-truth; **normative
(value/policy) → social-choice, keep multiple co-valid principles** — *knowledge-fusion*), **importance
selection** (independent selection breeds redundancy → rank + keep the best = anti-bloat), ID renumber,
global faithfulness re-check, profile, skills. Claims stay **per-book** (cleaner provenance); the
deduped layer is **principles** — measure richness by **principles** + per-book claim-**recall**
(coverage vs a reference set, not raw count). Citations in *Research grounding*.

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

## Research grounding (2026-06-20)
Four prior research reports (`docs/Research/`) were reviewed against this design; each refinement above
is cited here. (The knowledge-fusion report was **regenerated this day** — PASS 1.00, 8 foundational
papers injected by verified arXiv-ID — before being used.)

| design decision | report | key finding (arXiv) |
|---|---|---|
| **chunk** (not whole book) is the extraction unit | long-document | flat/fixed-window is the wrong baseline; degrades past ~800 tok [1905.13164, 2505.06862] |
| neighbour-context + global salience pass | long-document | chunk-local under-recalls boundary-spanning + scattered units [2606.10716, 2502.00448, 2305.14806] |
| provenance-anchored atomic units | long-document | bullet ↔ source span — the granularity claim-extraction consumes [2406.10370] |
| **typed claims** (fact/value/policy) route the reconcile handler | argument-mining | validated 3-way taxonomy [2510.16363]; value/policy = normative |
| **condition/exception** fields (anti-over-broad) | argument-mining | undercutting "unless X" qualifiers; surface-cue bootstrap [Pollock via s2-a2ae7155d9] |
| **certainty** field (preserve hedging) | argument-mining | hedged ≠ asserted [2606.10471] — guards faithfulness `HEDGING_REMOVED` |
| coverage is a capability ceiling → gate on claim-**recall** | argument-mining, long-document | precision-only rewards abstention; recall vs reference set [2606.09376, 2305.14251, 2502.10855] |
| LLM + JSON schema + delayed-structure extraction | argument-mining | ~95% vs 75–80% classifiers; schema cost ≈ 0 for capable models [2606.09251, 2606.09410] |
| REDUCE merge = **recall-then-filter** (det recall → LLM precision) | knowledge-fusion, rag-graphrag | dominant cross-doc architecture; recall stage must be recall-tuned [2109.07401, 2104.08413, 2004.04906] |
| **dedup-before-voting + copy-detection** | knowledge-fusion | N near-duplicate books can't outvote one authority; our own distillation can manufacture false corroboration [1503.00310, 1708.02018] |
| **split reconcile by nature** (factual vs normative) | knowledge-fusion | accuracy-weighting a normative conflict is a category error; social-choice + keep-both [2404.10271, 1404.6445, 2112.13557] |
| contradiction = 3-way stance head, **not a bare LLM** | knowledge-fusion | off-the-shelf LLMs near chance on subtle conflicts [DocNLI 2106.09449, 2403.08319, 2103.08541] |
| claim-**conditional** dedup (not raw paraphrase) | knowledge-fusion | equivalence is claim-conditional [PERSPECTRUM 1906.03538] |
| principle store **aids retrieval of real passages, not LLM summaries** | rag-graphrag | summary-replacement collapses + hallucinates [2502.14802, 2605.20815] |
| knowledge_partition = routed mix (distill stable / retrieve volatile) | rag-graphrag | distill + retrieve are complementary [2407.16833, 2401.08406] — grounds the existing Step-14 rule |
| keep dedup/rank/retrieval DETERMINISTIC; LLM only for judgment/synthesis | rag-graphrag | cross-validates the *Determinism boundary* [2004.04906, 2405.14831, 2304.09542] |

**Three cautions the research forces:**
- **Chunking trades book-dilution for chunk-localism** — per-chunk extraction *must* add neighbour
  overlap + a global salience pass, or it just relocates the dilution. Chunking alone is not the win.
- **Cross-source contradiction detection is genuinely hard** (even GPT-4 near chance). REDUCE's
  conflict step is **best-effort + surfaced for review**, never a guarantee — and "merge subsumes
  Step 7" means *dedup + strengthen*, not reliable emergent synthesis.
- **Do NOT import rag-graphrag's "fixed-size chunking is fine"** into the MAP — that is a *runtime
  retrieval* result; *extraction recall* needs structure-aware chunks (a different objective).

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
| Avoid bloat? | REDUCE dedups (multi-anchor) + **ranks & selects** by importance → synthesize, not accumulate (*long-document*: independent selection breeds redundancy) |
| Subsume Step 7? | **Partly** — merge = dedup + strengthen via recall-then-filter; true emergent synthesis + reliable cross-source contradiction stay hard (*knowledge-fusion*) |
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

- **P0 — prototype (first):** minimal **chunk-level** per-book module (source-map → typed claims with
  neighbour-context + global salience) + N-way recall-then-filter merge; rebuild ONE package
  (software-architecture, 9 books) via map → reduce. Measure: (1) `grounding-richness` (principles)
  vs the current batch v0.3.0 — adopt only if it clearly wins; (2) same *small* book, Copilot-MAP vs
  Claude-MAP richness — equal ⇒ Copilot is a full MAP worker; (3) **zero `compacted=true`** on any
  Copilot prompt; (4) REDUCE distilled-artifact input stays < 200k; (5) **claim-recall coverage** vs a
  reference atomic-claim set rises (not just raw count); (6) **advice no-regression** on a small
  behaviour-replay A/B (semantic grader) — guards the bloat risk.
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
- **Chunk-local salience loss** — per-chunk extraction under-recalls boundary-spanning/scattered claims; mitigate with neighbour-context overlap + a global salience pass (*long-document*), else chunking just relocates the dilution.
- **Bloat (mirror of dilution)** — more claims can yield a worse, unfocused reviewer; REDUCE must rank-and-**select**, not accumulate. Anti-dilution (deep MAP) + anti-bloat (selection) together.
- **Normative conflicts have no settled algorithm** (*knowledge-fusion* G1) — don't auto-resolve value/policy conflicts; preserve both with scope/condition. Cross-source contradiction detection is near-chance for bare LLMs → surface, don't trust.
- **Count ≠ recall** — gate on claim-**recall** coverage vs a reference set + advice (semantic grader), not raw claim count (which can be padded/trivia).
