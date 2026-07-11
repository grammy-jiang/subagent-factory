# Factory operations guide

Practical commands for running and maintaining the factory. Generated packages under
`subagents/<slug>/` and adapters under `.claude/agents/generated/` are **gitignored regenerable
output**; the factory *code* is tracked.

## Corpus health — start here

```bash
python -m tools.subagent_factory.cli corpus-health          # table
python -m tools.subagent_factory.cli corpus-health --json    # machine-readable
```

Per package: converter, anchor count + dominant type, tier/status, claims, dangling refs, and a
health flag. Flags:

- `empty-anchors` — conversion produced no anchors (old MarkItDown flatten / never re-authored).
- `no-headings` — paragraph-only anchors (MarkItDown fallback); a Docling re-author upgrades these.
- `junk-anchors` — paragraph anchors dominated by PDF noise.
- `dead-refs` — claims cite anchors not in the index (inconsistent package).
- `ok` — heading anchors, no dead refs.

## PDF conversion (Docling)

Docling is the preferred converter (semantic headings); MarkItDown is the fallback (flattens).
Install CPU-only (see `enhancement-steps/step-20-document-ai-pdf-parsing.md`):

```bash
python -m pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
python -m pip install docling
```

The markdown cache is **converter-keyed** (`inputs/markdown-cache/<sha>.<converter>.md`), so
installing Docling over a MarkItDown-cached corpus auto-invalidates the old entries — a re-author
re-converts with Docling automatically, **no manual cache purge needed**.

## Re-author a package on clean anchors

```bash
# /author-subagent <pdf...> --update <slug>   (run via a Claude Code session / headless `claude -p`)
python -m tools.subagent_factory.cli validate <slug>
```

- `source_id` is content-addressed (`<stem>-<sha8>`): re-authoring the same source reuses the id
  and overwrites artifacts in place — no orphaned references, even if a run is interrupted.
- Multi-source packages: pass every source PDF; clear/let the converter-keyed cache invalidate each.
- After a re-author, confirm with `cli validate <slug>` and `cli corpus-health`.

## Faithfulness report flaky? Repair it

The faithfulness step occasionally emits free-text `source_anchors` instead of ids, failing
validation. Repair deterministically (quarantines the bad entries, keeps verdicts):

```bash
python -m tools.subagent_factory.cli repair-faithfulness <slug>   # writes reports/faithfulness-repair.yaml
python -m tools.subagent_factory.cli validate <slug>
```

**Stale line/slug anchors (older packages).** If the `source_anchors` are line references
(`<source_id>:L148`, `kafka-best-practices L753-757`) rather than free text, `remap` *recovers*
them instead of dropping: it regenerates an empty anchor index from the surviving markdown, then
line-maps each reference to the anchor covering that line (routing by source hint; a finding's bare
`L<n>` inherits the source its hinted siblings agree on). Refs with no line — conceptual section
slugs (`ch6-never-split`) — are quarantined, **never** fuzzy-matched (that would fabricate
provenance):

```bash
python -m tools.subagent_factory.remap_faithfulness_anchors subagents/<slug>/reports/faithfulness-report.yaml
```

This fixes only the **faithfulness** report.

**Skill / reference provenance with bare source-ids (Tier-0 packages).** A Tier-0 package can ship
skills/references whose `provenance.source_anchors` is the *whole source id* (no claim→anchor chain to
rebuild from). Because a skill/reference is a *broad* artifact, "which spans does it draw on" is
answerable by **content overlap** — and that is appropriate for a coarse "draws-on" provenance (it is
not the atomic-claim *support* judgement). `reground_skill_anchors` replaces each bare source-id with
the top content-matched real anchors of that source (requiring a real shared-token signal, never
guessing):

```bash
python -m tools.subagent_factory.reground_skill_anchors subagents/<slug>   # skills + references
```

**Claim/evidence anchors that are concept slugs (`ch1-tactical-empathy`).** These name a *section*,
not a span. Two cases:

1. *Source has (or can recover) headings.* A slug is a slugified section title, so map it back to the
   heading it names — faithful **recovery**, not a guess. If the package was converted by the old
   markitdown path (no headings, tab/table-noise prose — check `sources/reports/*.conversion-report.md`),
   first **re-convert with Docling in place** (keeps the source_id stable, so claims still resolve),
   regenerate anchors, then `reanchor_by_heading` maps each slug to its source's best-matching heading
   (≥1 shared concept token; no match ⇒ left empty, never forced):
   ```bash
   python - <<'PY'   # re-convert in place + regenerate anchors (Docling, local CPU, no model cost)
   from pathlib import Path
   from tools.subagent_factory.convert_pdf import convert_pdf
   from tools.subagent_factory.inject_anchors import inject_anchors
   b = Path("subagents/<slug>"); sid = "<source_id>"
   md = b/f"sources/markdown/{sid}.md"
   convert_pdf(b/f"sources/original/{sid}/original.pdf", md)
   inject_anchors(md, md, b/f"sources/anchors/{sid}.anchors.jsonl", sid)
   PY
   python -m tools.subagent_factory.reanchor_by_heading subagents/<slug>   # slug -> heading; evidence inherits
   ```
   (Run any `python -` heredoc with **stdin** as above, not `python /tmp/x.py` — a stray `/tmp/struct.py`
   shadows the stdlib and breaks the converters.)
2. *A claim's concept has no heading* (a sub-point) — `reanchor_by_heading` leaves it empty (valid,
   honest). To anchor it to a prose span, `reanchor_claims` (surgical LLM: content-narrow candidates →
   LLM picks the supporting span) works **once the source is clean** — it cannot find a faithful span in
   markitdown-corrupted prose.

**Worked example — the 4 bulk-re-export failures, all fixed:** advertising + startup-ceo by `remap`
(`:L<n>` line refs); kafka by `reground` (Tier-0 skills/references, bare source-ids); negotiation by
**Docling re-convert + `reanchor_by_heading`** (markitdown→Docling recovered 166 headings, 55/64 claim
slugs resolved to them, 9 headingless concepts left empty) — zero model cost.

## Evaluate extraction (claim recall)

Compare two claim sets on content (no ML) — e.g. structure-mapped units vs flat claims:

```bash
python -m tools.subagent_factory.claim_recall <reference> <candidate> [threshold]
#   each path: analysis/claims.jsonl OR sources/maps/<id>.source-map.yaml
```

Reports recall / precision / f1 and the unmatched reference statements (the recall gaps). Lexical
lower bound — use for relative arm comparison, not as absolute truth.

## Evaluate output quality (does the expert give good advice?)

Structural `validate` proves the package is consistent; it does not prove the generated expert gives
good advice on a real task. To measure that — and the **eval-driven multi-source grounding** recipe
that turns a grounding leak into a stronger, more faithful subagent — see
[`output-quality-eval.md`](output-quality-eval.md). Harness: `examples/review-with-subagents.sh`
(read-only, headless). Deterministic grounding-leak scorer:

```bash
python -m tools.subagent_factory.cli grounding-check <slug> <review.md> <reviewed-doc.md>
#   coverage + cross-source borrows (names the source to add for multi-source grounding)
```

## Baseline-gate the invariant layer

The operating-invariant layer (A3/A5) helps a package whose behaviour-test baseline is **weak** and
can mildly *hurt* an already-strong one (measured, package-dependent ≈ inverse to baseline — see
`output-quality-eval.md`). To decide per package: replay it **without** invariants, then apply the
rule (attach iff baseline < 0.80). Use a semantic grader for a trustworthy baseline:

```python
from tools.subagent_factory.invariant_policy import recommend_invariants
from tools.subagent_factory.behaviour_replay import shell_runner, make_llm_grader
# llm = a Callable[[str],str] judge, e.g. wrapping examples/codex-judge.sh
rec = recommend_invariants("subagents/<slug>", shell_runner("examples/replay-runner.sh"),
                           make_llm_grader(llm))
# rec = {"attach": bool, "baseline": float, "threshold": 0.8, ...}
```

Then set `attach_invariants: <rec.attach>` in `subagents/<slug>/profile.yaml` and re-`export`.
`export_claude_agent` honours the flag (default `true`); `attach_invariants: false` omits the layer.

## Validate before release

```bash
python -m tools.subagent_factory.cli validate <slug>     # per package
make verify                                               # factory code: lint + type + tests + secrets
```

## Run and improve the factory (two layers)

Two layers cooperate. **Layer 1 — the skill (`/author-subagent`)** is the recipe: one
agent runs the whole pipeline in-thread (source → ingest → interrogate → claims →
evidence → principles → profile → faithfulness → adapter → validate). Engine-agnostic
instructions. **Layer 2 — the `campaign/` bash scripts** are the manager around the
skill — they do NOT replace it. They drive the skill inside fresh, independent headless
`claude -p` sessions and add the discipline a single skill call can't: per-session
budgets (anti-dilution), resumability, deterministic gates, and offline logs.

```text
bash script ──render prompt──▶ claude -p (fresh session RUNS the skill) ──▶ log.jsonl
     │                                                                        │
     └──── deterministic gate (parse log, check artifact, make verify) ◀──────┘
                  ok → next   |   fail/missing-artifact → STOP for review
```

Three-role loop (the intended way to test + improve this repo):

- **Manager** = bash (`build_map_reduce.py`, `map_books.sh`, `p2b_finish.sh`): orchestrate, gate, log, resume.
- **Worker** = fresh `claude -p` per step: runs one skill step on its own budget.
- **Reviewer** = a separate claude reading the logs: `review-run.py` → diagnose → fix factory code/prompts → re-run only the affected phase.

### Single book vs multi-book

- **Single source** → `campaign/generate-subagent.sh --slug S --topic "..."`: ONE session
  runs the whole skill end-to-end, auto-validates, stops.
- **Multi-book (≥2 sources)** → `generate-subagent.sh` REFUSES (exit 4) because one
  session over many books under-extracts (dilution — see
  `docs/per-book-authoring-upgrade.md`). Use the per-book map→reduce path:

```bash
# Phase 1 — MAP (one fresh session per book; chunks + claims + principles cached by sha256)
bash campaign/map_books.sh --sources campaign/<slug>.sources          # serial, cap-aware
# Phase 2 — REDUCE to filter gate (deterministic: anchors → clusters.json, then STOPS)
python3 campaign/build_map_reduce.py <slug> --sources campaign/<slug>.sources --resume
# Phase 3 — precision filter (1 session → .build/decisions.json; or hand-author it)
bash campaign/precision_filter.sh --slug <slug> --fg
# Phase 4 — assemble (--select 50 focused / 150 comprehensive / 0 all)
python3 campaign/build_map_reduce.py <slug> --sources campaign/<slug>.sources --resume --select 50
# Phase 5 — finish LLM layer + validate (1 session)
bash campaign/p2b_finish.sh --slug <slug> --fg
```

`build_map_reduce.py` is checkpointed (`subagents/<slug>/.build/*.done` +
`steps.log.jsonl`) and resumable; its two LLM steps (MAP, precision filter) are **gates**
that print the next command and stop — they never auto-spend.

### Engine assignment, caps, and the p2b self-drive

Which engine runs which LLM step (claude / GitHub Copilot / codex — **one session per engine
at a time**; concurrent same-pool sessions corrupt a build):

- **p2b (`p2b_finish.sh`) = opus only** (`--engine claude|copilot`). codex UNDER-authors — it
  skips the skills layer (`skills: []`) even though `validate` passes. Never p2b on codex.
- **precision filter = any structured engine**, but codex caps fast on large cluster sets
  (rc=1 on the first call). Prefer the free opus pool; fail over on cap.
- **MAP = any engine.** A giant book's final promotion (≥~45 chunks — e.g. xUnit 59ch,
  Continuous Delivery 43ch) needs 1M context → route it to **claude**, which lands it in one
  round where codex/copilot cap.
- **Cap failover order: codex → copilot → claude.** codex has the smallest window; claude is
  the last-resort recovery pool. codex, once capped in a session, tends to stay capped.

**`p2b_finish` self-drives to green** — its session runs the whole validate→fix loop internally
and prints `===P2B_SUMMARY=== validate: PASS` when done. Therefore:

- **Do NOT `validate` a package mid-p2b** — you will see transient failures (stale behaviour
  tests / adapter-invariant layer for the new spine) that the p2b is still fixing. Wait for the summary.
- `P2B_SUMMARY` lands in the **transcript** `campaign/logs/p2b-<slug>.log.jsonl`, NOT the shell
  launcher log (which only records "launched bg pid …").
- **A dead headless session ≠ unfinished work.** A capped/crashed engine may have already reached
  a valid state before the session ended (only the completion signal is lost). When a p2b looks
  "stuck" (engine gone, transcript frozen), **check the package's `validate` state** — if it
  PASSES, the work is done; bump the version, re-export, commit. Don't blindly re-run.

Detached (`setsid`) campaign jobs are reparented to `systemd --user`, so they **survive a
`claude` CLI restart** — they die only on logout/reboot. Gate any waiter on a **completion
marker** (`principles.yaml` / installed adapter), never on engine-absence (an engine idles
between p2b phases and a premature fire spawns a second same-pool session). Put `pkill` lines in
a `.sh` file — an inline `pkill -f '<pattern>'` self-matches the running command's cmdline (exit 1).

#### Always `setsid`-detach a forked engine session (never a bare child of a background task)

**Rule:** any independent engine session (`claude -p` / `codex exec` / `copilot -p`) that must outlive
the thing that launched it — a p2b, precision filter, MAP, faithfulness run — **must be started under
`setsid`**, so it gets its own session + process group reparented to `init`/`systemd`.

**Why (a real failure, 2026-07-10):** a `p2b_finish.sh --fg` started as a child of a Claude Code
Bash-tool *background task* was **SIGKILLed mid-authoring** when that task was reaped — abrupt (transcript
stops mid-message, no `rc=` line), **not** OOM and **not** a usage cap. `nohup` / `trap '' HUP` + `disown`
do **not** protect against this: they only ignore SIGHUP, and the process stays in the caller's process
group, so a group-targeted kill takes it down. Only `setsid` (new session, no shared group, reparented to
PID 1) survives. MAP/filter escaped this earlier only because a long-lived `--fg` manager held them alive.

**How:**
- `precision_filter.sh` and `p2b_finish.sh` **self-`setsid`** in their non-`--fg` bg mode — so just omit
  `--fg` to get a survivable launch, or wrap `--fg`.
- `map_book.sh` / `map_books.sh` / `generate-subagent.sh` / `faith-run.sh` background a subshell that
  inherits an argv **array** and so cannot self-`setsid` internally (re-serializing via `bash -c
  "$(declare -f …)"` drops the array and reintroduces a fixed quoting bug). Launch them through
  **`campaign/detach.sh`**: `bash campaign/detach.sh bash campaign/<script> … --fg`.
- Equivalently, wrap any launcher yourself: `setsid bash campaign/<script> … --fg </dev/null &`.
- A detached session sends **no** task-notification — **gate on a completion marker**
  (`principles.yaml` / `===P2B_SUMMARY===` / installed adapter), and put the poll-waiter in a `.sh` FILE
  written with the Write tool (a `cat <<EOF` heredoc gets ANSI-corrupted under the rtk shell hook).
- Verify detachment once: `ps -o pid,ppid,sid,cmd -p <engine-pid>` → the parent chain must reach PID 1.

### Caching (reuse MAP outputs)

- MAP output is cached at `cache/book-extracts/<sha256-of-book-bytes>/`
  (`chunks.jsonl`, `claims.jsonl`, `principles.yaml`, `anchors.jsonl`, `module.json`).
- Key = file bytes → identical markdown is a guaranteed cache hit; re-converting a PDF
  changes the sha → re-MAP. **Real success = `principles.yaml` present**, not exit-0:
  a cap/429 kill leaves a partial `claims.jsonl` with no `principles.yaml`; re-running
  auto-resets that book (keeps chunks, re-MAPs). Engine exit codes are propagated so a
  kill never marks the cache "done".
- Cache is slug-independent → a book MAPped once is reused by every package that includes it.
- UPDATE (add a book): chunk + MAP only the new book, then re-run REDUCE. Never re-MAP unchanged books.
- FOLD-IN (rebuild an existing package with a new source): **clear the stale
  `subagents/<slug>/.build/` first** — old `decisions.json`/`clusters.json`/`*.done` gates are
  keyed to the previous cluster set and would misapply to the new one. Then REDUCE → filter →
  assemble → p2b. Notes: (a) assemble re-synthesises the new source's metadata to a slug title
  with null author/year — that is consistent with the md-sourced siblings, leave it; (b) a new
  source + a principle-count change is a **MINOR** version bump (not patch), and after bumping
  `agent_version` you must **re-export the adapter** (`python -m tools.subagent_factory.cli export
  <slug>`) or the `adapter-sync` gate fails; (c) tune `--select` to the corpus tier — do not
  under-select (50 was too thin for the 2-book DDD domain, raised to 110 = the software-architecture
  tier; the pool after the filter is usually far larger than the cluster count).

### Review → fix → improve loop

> **Two different reviews.** The log-tier table below is for a *generation run's health* (did it
> validate?). To review a generated package's *quality* — domain-reviewer panel → grounded fix →
> **independent adversarial re-verify** → converge to zero must-fix — use the
> **`/review-subagent <slug>`** skill (`.claude/skills/review-subagent/`, driver
> `campaign/review-subagent-loop.sh`).

| Tier | Artifact | Use for |
| --- | --- | --- |
| 1 | `campaign/logs/review-<slug>.md` (`python3 campaign/review-run.py <slug>`) | READY y/n, validate verdict, FAIL/WARN lines, real over-claims, log failure signatures |
| 2 | `subagents/<slug>/.build/steps.log.jsonl` + the `===*_SUMMARY===` blocks in logs | which step gated/failed |
| 3 | `campaign/logs/<run>.log.jsonl` | full transcript — only when debugging a specific failure |

Other campaign loops: `run.sh` (factory-hardening campaign over the PDF queue, one
session/PDF, agent finds+fixes a defect + commits; `summarize.py` gates each round),
`faith-run.sh` (per-package faithfulness-report campaign), `prep-round.py` (spec-YAML →
resolve titles → stage → launch staggered chains → auto-review), `eval-round.sh`
(output-quality eval + grounding-check).

Cautions: per-book MAP can take ~1h (default `RUN_TIMEOUT=7200`; raise via env for big
books). A fresh map→reduce OVERWRITES an existing package on assemble/finish — back up
`subagents/<slug>/` (e.g. to `subagents/.backups/<slug>-<ts>`) first if comparing old vs
new. Headless runs author in-thread (no-spawner branch); spawn worker agents only in an
interactive session where you can watch and recover.
