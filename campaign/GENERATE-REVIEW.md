# Review — `generate-subagent.sh` authoring launcher

> **Portability / environment note.** This review was written on an AWS-Bedrock machine
> (`/scratch` workspace) where the model is an inference-profile ARN and the public id
> `claude-opus-4-8` 400s. On a **public-API** machine `claude-opus-4-8` is valid — the launcher
> model default falls back to it (`…:-${ANTHROPIC_MODEL:-claude-opus-4-8}`). Repo paths in the
> prompt templates are now the portable `{{REPO}}` placeholder (filled at render time from the
> script-computed repo root), so the launchers run unchanged after copying the repo to any path.

Critical review of the independent (headless) authoring launcher before first run.
Scope: produce ONE valid subagent package via `/author-subagent`; no factory hardening,
no commits. Reviewed 2026-06-15.

## Files
| File | Role |
|------|------|
| `generate-subagent.sh` | driver: resolve sources → render prompt → headless `claude -p` → auto-`validate` |
| `generate-prompt.tmpl` | authoring-only prompt (multi-source, distillation-only, Tier-1 pipeline, machine summary) |
| `software-architecture.sources` | the 7 canonical-core source paths (4 books + 3 papers, markdown) |

---

## Findings

### FIXED — blockers / bugs

1. **Invalid hardcoded model (`claude-opus-4-8`) — would 400 every run.**
   This environment runs on **AWS Bedrock**: the model is set via `ANTHROPIC_MODEL`
   (an `arn:aws:bedrock:...application-inference-profile/...` ARN), not a public id.
   Passing `--model claude-opus-4-8` returns `400 The provided model identifier is
   invalid`.
   **Fix:** `--model` now **defaults to this machine's Opus 4.8 (1M-context) ARN** —
   `$ANTHROPIC_DEFAULT_OPUS_MODEL` (`…application-inference-profile/awrex5qkjz05`,
   the `[1m]` profile this session itself runs on), falling back to `$ANTHROPIC_MODEL`.
   The 1M context window is **baked into the inference profile** — no beta header needed.
   Verified: explicit ARN + `--effort max` runs headless and returns the expected token.
   *NB: the existing `campaign/run.sh` and `author-run.sh` hardcode the same invalid
   `claude-opus-4-8` — same latent bug, out of scope to change here.*

   **Effort:** added `--effort` (low|medium|high|xhigh|max), **default `max`** for the
   deepest reasoning on this multi-source Tier-1 authoring run. (Session/global default
   is only `medium`.) Overridable via `--effort` or the `EFFORT` env var.

2. **`--model` previously always injected** even when empty → would have passed
   `--model ""`. Now gated behind a non-empty check.

3. **Cosmetic: leading space in the rendered `{{SOURCES}}` block.** Harmless to the
   LLM, fixed anyway (`${SOURCES:+...}` accumulator).

### VERIFIED — correct as written

- **stdin redirect (`< promptfile`) works** with `claude -p` (tested) — robust against the
  heredoc/ANSI-`cat` corruption gotcha the prompt itself warns about.
- **`ingest` is variadic** (`SOURCE...`) — passing all 7 sources under one `--slug`
  grounds a single multi-source package, as intended.
- **`--add-dir` per source dir, deduped** — the headless session can read both
  `markdown/` and `papers/markdown/`; duplicate dirs collapsed via an assoc-array set.
- **Auto-`validate` after the run** surfaces PASS/FAIL without a human watching.
- **Backgrounded by default** (`nohup`) with transcript + driver logs under
  `campaign/logs/gen-<slug>.*`; `--fg` for foreground.
- **Disk**: ~12 GB free — adequate for a generated package (small text artifacts; the
  markdown cache is reused, no re-conversion).

---

## Residual risks / caveats (not bugs — know before running)

1. **`--dangerously-skip-permissions`** — required for unattended headless; the session
   has full tool access in the repo. Same posture as the existing campaign scripts.
2. **Source fidelity is uneven.** 3 of 4 books + all papers came via Docling (good
   headings); **`software-architecture-in-practice-3rd` came via the markitdown fallback**
   (flat, `headings=0`). Claim extraction still works on flat text, but anchoring is
   coarser for that one source — expect weaker provenance anchors from it specifically.
3. **Cost/time.** 7 substantial Tier-1 sources through every gated LLM step is a real
   multi-hour, high-token run. Default timeout 7200s (2h) may be tight; raise with
   `--timeout` if a run is `timeout`-killed mid-pipeline.
4. **No resume.** Unlike the queue-based campaign, this is one-shot. If it dies partway,
   the package may be half-built; re-running re-ingests (sha256 skip avoids dup work, but
   verify the package state). A future improvement could checkpoint per pipeline step.
5. **Rights are asserted in the prompt, not detected.** The prompt tells the session these
   are `distillation-only`. That is the correct floor for authored books, but it bypasses
   the skill's Step-2a detection. Acceptable (we know what these are), just explicit.

---

## Possible improvements (future, not blocking)

- **Fix the model bug in `run.sh` / `author-run.sh` too** (same invalid `claude-opus-4-8`).
- **Add `--resume`/checkpointing** so a killed run continues from the last completed step.
- **Emit a gate verdict** (parse `===GENERATE_SUMMARY===` like `summarize.py` does for the
  campaign) instead of only running `validate` — gives one-line ok/blocked/fail.
- **Pre-flight fidelity warning**: detect markitdown-converted (`headings=0`) sources in the
  `.sources` list and warn, so the operator can choose to re-Docling them first.
- **Parameterize `--add-dir`** to also include the repo root if a future source list spans
  more trees.

---

## How to run (after this review)

```bash
# dry-run (no LLM): show resolved sources + command + rendered prompt
campaign/generate-subagent.sh --slug software-architecture \
    --topic "software architecture reviewer" --dry-run

# real run (backgrounded; inherits env Bedrock model; auto-validates on finish)
campaign/generate-subagent.sh --slug software-architecture \
    --topic "software architecture reviewer"

# watch / check
tail -f campaign/logs/gen-software-architecture.log.jsonl
python -m tools.subagent_factory.cli validate software-architecture
```

To author another category later: add `campaign/<slug>.sources` and run with
`--slug <slug> --topic "..."`.
