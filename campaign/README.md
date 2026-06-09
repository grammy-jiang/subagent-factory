# Campaign driver

Automates the factory-hardening campaign: run `/author-subagent` over the
`awesome-book-collection` PDFs, **one fresh headless Claude session per PDF**,
smallest-first. Each session tests the skill, finds a factory defect, fixes it,
and commits locally. Bash owns all mechanics; the LLM owns only judgment.

## Files (committed)
| File | Role |
|------|------|
| `run.sh` | driver: pick next PDF → render prompt → run `claude -p` → gate → record → loop/stop |
| `build-queue.py` | scan collection, size-sort, sha256 done-detection → `pdf-queue.tsv` + `pdf-inventory.md` |
| `summarize.py` | parse the `claude` stream-json log → `summary.md` + `runs.md` row + queue update + gate verdict |
| `prompt.tmpl` | the per-PDF LLM prompt (`{{PDF}} {{RUN}} {{DONE_SLUGS}} {{RECENT_COMMITS}}`) |

## Generated (gitignored)
`pdf-queue.tsv` (source of truth) · `pdf-inventory.md` (human view) · `runs.md`
(one row per round) · `logs/run-NNN-<slug>.{log.jsonl,summary.md,verify.log}`.

## Usage
```bash
campaign/run.sh --dry-run          # show the exact command + rendered prompt, run nothing
campaign/run.sh -n 5 --yes         # run up to 5 rounds unattended
campaign/run.sh --all              # churn the whole queue
```
Flags: `-n N | --all`, `--prompt-file F`, `--collection DIR`, `--model M`
(default `claude-opus-4-8`), `--timeout SECS` (per-round cap, default 2400),
`--dry-run`, `--yes`.

## Behaviour
- **One PDF at a time**, sequential (git index + queue forbid parallel).
- **Skip done** via sha256 match against `subagents/*/source-pack.manifest.yaml`.
- **Markdown cache** (`inputs/markdown-cache/`) is reused automatically — no re-conversion.
- **Commit local only, never push** (so no CI trigger). The LLM commits just the factory fix.
- **Post-run gate** (deterministic): a round is `ok` only if the agent reports
  `status: ok`, `make verify` is green, and `HEAD` advanced (a fix was committed).
- **Stops** on the first non-`ok` round (for review) or on a usage limit (PDF left
  pending). **Resume** by re-running — the queue remembers progress.

## Context tiers for review
`runs.md` (whole campaign) → `logs/run-NNN.summary.md` (one round) →
`logs/run-NNN.log.jsonl` (full transcript, only when debugging).
