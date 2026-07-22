#!/usr/bin/env bash
# map_book.sh — run ONE book's MAP step (deep per-chunk claim extraction + principle
# promotion) over a PRE-CHUNKED module from tools.subagent_factory.chunk_source, in a fresh
# headless Claude session. Writes claims.jsonl + principles.yaml + module.json into the module
# dir and STOPS. Top-level `claude -p` (can spawn sub-agents; no sub-agent stall).
#
# Usage: campaign/map_book.sh --book <staged.md> [--cache cache/book-extracts]
#                             [--model M] [--effort max] [--timeout SECS] [--max-attempts N]
#                             [--dry-run] [--fg]
#   --max-attempts N: auto-resume this book across up to N runs (default 1) until principles.yaml
#     exists. Each attempt resumes from persisted partials, so a per-request timeout on a big book
#     costs one more attempt instead of a manual re-launch. Requires --fg (the loop blocks per run).
set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CAMP="$REPO/campaign"; LOGS="$CAMP/logs"; TMPL="$CAMP/map-book-prompt.tmpl"
# Single source of truth for the claude `claude -p` argv (shared with run.sh / generate-subagent.sh).
source "$CAMP/_claude_run.sh"
CLAUDE_BIN="${CLAUDE_BIN:-$HOME/.local/bin/claude}"
COPILOT_BIN="${COPILOT_BIN:-$HOME/.local/bin/copilot}"
COPILOT_MODEL="${COPILOT_MODEL:-claude-opus-4.8}"   # Copilot's opus id (dot, not dash)
COPILOT_EFFORT="${COPILOT_EFFORT:-high}"            # Copilot max effort is "high"
CODEX_BIN="${CODEX_BIN:-$HOME/.local/bin/codex}"
CODEX_MODEL="${CODEX_MODEL:-gpt-5.5}"               # Codex (OpenAI); SMALL 5h budget — small books only
MODEL="${MODEL:-${ANTHROPIC_DEFAULT_OPUS_MODEL:-${ANTHROPIC_MODEL:-claude-opus-4-8}}}"
EFFORT="${EFFORT:-max}"; RUN_TIMEOUT="${RUN_TIMEOUT:-7200}"
CACHE="$REPO/cache/book-extracts"
ENGINE="claude"; TAG=""
BOOK=""; DRYRUN=0; FG=0; FORCE=0; MAX_ATTEMPTS=1
BLOCK_ON_INJECTION="${MAP_BLOCK_ON_INJECTION:-0}"
while [ $# -gt 0 ]; do
  case "$1" in
    --book) BOOK="$2"; shift 2;;
    --cache) CACHE="$2"; shift 2;;
    --model) MODEL="$2"; shift 2;;
    --effort) EFFORT="$2"; shift 2;;
    --timeout) RUN_TIMEOUT="$2"; shift 2;;
    --max-attempts) MAX_ATTEMPTS="$2"; shift 2;;  # auto-resume a big book across N runs until principles.yaml
    --dry-run) DRYRUN=1; shift;;
    --fg) FG=1; shift;;
    --force) FORCE=1; shift;;
    --engine) ENGINE="$2"; shift 2;;
    --tag) TAG="$2"; shift 2;;
    --block-on-injection) BLOCK_ON_INJECTION=1; shift;;  # fail closed on un-triaged injection findings
    *) echo "unknown arg: $1" >&2; exit 2;;
  esac
done
[ -n "$BOOK" ] || { echo "--book <staged.md> required" >&2; exit 2; }
[ -f "$BOOK" ] || { echo "book not found: $BOOK" >&2; exit 3; }
mkdir -p "$LOGS"

# Content-address the module (must match chunk_source.write_book_module: sha256 of file bytes).
SHA="$(sha256sum "$BOOK" | cut -d' ' -f1)"
MODULE="$CACHE/${SHA}${TAG}"
# A/B (--tag): seed the tagged module with the SAME deterministic chunks (so engine is the only
# variable), leaving the canonical <sha> module untouched for comparison.
if [ -n "$TAG" ] && [ ! -f "$MODULE/chunks.jsonl" ] && [ -f "$CACHE/$SHA/chunks.jsonl" ]; then
  mkdir -p "$MODULE"; cp -r "$CACHE/$SHA/chunks" "$CACHE/$SHA/chunks.jsonl" "$CACHE/$SHA/source.md" "$MODULE/"
fi
[ -f "$MODULE/chunks.jsonl" ] || { echo "module not chunked yet: $MODULE (run chunk_source first)" >&2; exit 3; }
# source_id = <title-slug truncated 20>-<sha8>  (matches the factory's existing source_id style).
STEM="$(basename "$BOOK" .md)"
SLUG="$(printf '%s' "$STEM" | tr '[:upper:]' '[:lower:]' | tr -c 'a-z0-9' '-' | sed 's/-\{2,\}/-/g; s/^-//; s/-$//' | cut -c1-20 | sed 's/-$//')"
SOURCE_ID="${SLUG}-${SHA:0:8}"
TITLE="$STEM"

# Parallel-safe (multiple drain loops): skip a completed module; else atomically claim it (mkdir is
# atomic) and release the claim on exit so a crashed book can be retried. Requires --fg (the claim is
# held for the lifetime of this process, which blocks on the claude run only in --fg mode).
if [ "$FORCE" -eq 0 ] && [ -f "$MODULE/principles.yaml" ] && [ -f "$MODULE/module.json" ]; then
  echo "[map] $SOURCE_ID already complete — skip"; exit 0
fi
if ! mkdir "$MODULE/.claim" 2>/dev/null; then
  echo "[map] $SOURCE_ID claimed by another worker — skip"; exit 0
fi
trap 'rmdir "$MODULE/.claim" 2>/dev/null' EXIT

# A prior run that died (cap/429, timeout) before promoting principles leaves per-chunk partials
# under partials/ and possibly a stale merged claims.jsonl. KEEP partials/ (the MAP prompt resumes
# from them — completed chunks are skipped); only clear the post-merge artifacts so the re-run
# re-merges cleanly. KEEP the deterministic chunks (chunks.jsonl, chunks/, source.md).
if [ ! -f "$MODULE/principles.yaml" ] && { [ -f "$MODULE/claims.jsonl" ] || [ -d "$MODULE/partials" ]; }; then
  echo "[map] $SOURCE_ID has an incomplete extraction — keeping partials/, clearing merged outputs before resume"
  rm -f "$MODULE/claims.jsonl" "$MODULE/anchors.jsonl" "$MODULE/module.json"
  rm -rf "$MODULE/_map" "$MODULE/_work"
fi

run="map-$SOURCE_ID${TAG}"; log="$LOGS/$run.log.jsonl"; promptfile="$LOGS/$run.prompt.txt"
REPO="$REPO" MODULE="$MODULE" SOURCE_ID="$SOURCE_ID" TITLE="$TITLE" \
  python3 "$CAMP/render-prompt.py" "$TMPL" > "$promptfile"
echo "[map] book=$STEM  source_id=$SOURCE_ID  module=$MODULE  engine=$ENGINE"
echo "[map] chunks=$(grep -c . "$MODULE/chunks.jsonl")"

# IPI pre-flight (approach A): the injection scan runs at chunk time (chunk_source writes
# injection-scan.jsonl). Surface findings BEFORE this untrusted book reaches the MAP session. Advisory
# by default (the ~225:1 benign:attack base rate makes hard-blocking raw hits flood legit content);
# --block-on-injection (or MAP_BLOCK_ON_INJECTION=1) fails closed until the module is triaged. The
# presence of source-safety-verdicts.yaml is the "triaged" signal that clears the warning/block.
INJ="$MODULE/injection-scan.jsonl"
if [ -s "$INJ" ] && [ ! -f "$MODULE/source-safety-verdicts.yaml" ]; then
  n_inj="$(grep -c . "$INJ" 2>/dev/null || echo 0)"
  echo "[map] ⚠ IPI: $n_inj un-triaged injection finding(s) in this book (see $INJ)." >&2
  echo "[map]   Triage before distillation — record verdicts in $MODULE/source-safety-verdicts.yaml" >&2
  echo "[map]   and redact suspicious spans, then re-run." >&2
  if [ "$BLOCK_ON_INJECTION" -eq 1 ] && [ "$DRYRUN" -eq 0 ]; then
    echo "[map]   --block-on-injection: refusing to launch MAP on un-triaged untrusted content." >&2
    exit 5
  fi
fi

# Build the engine argv ONCE as an ARRAY (no generated script, no two-level quoting). The
# claude case uses the shared build_claude_argv contract — with --effort and a single
# --add-dir "$REPO" — then overrides argv[0] to honour the CLAUDE_BIN path. The copilot
# case is a genuinely different invocation, so it is its own small array.
if [ "$ENGINE" = "copilot" ]; then
  engine_argv=("$COPILOT_BIN" -p "$(cat "$promptfile")" --model "$COPILOT_MODEL" --effort "$COPILOT_EFFORT" --allow-all)
elif [ "$ENGINE" = "codex" ]; then
  # Codex non-interactive: prompt as arg (like copilot). workspace-write lets it write the
  # module dir under $REPO (cache/book-extracts/...); never prompts for approval.
  engine_argv=("$CODEX_BIN" exec --model "$CODEX_MODEL" --sandbox workspace-write --skip-git-repo-check "$(cat "$promptfile")")
else
  build_claude_argv engine_argv "$MODEL" "$EFFORT" "$REPO"
  engine_argv[0]="$CLAUDE_BIN"   # contract is `claude -p ...`; use the configured binary path
fi

if [ "$DRYRUN" -eq 1 ]; then
  echo "[map] DRY-RUN; prompt: $promptfile"
  echo "[map] command that would run (cwd=$REPO):"
  if [ "$ENGINE" = "copilot" ] || [ "$ENGINE" = "codex" ]; then
    echo "    timeout $RUN_TIMEOUT $(claude_argv_str "${engine_argv[@]}") > $log 2>&1"
  else
    echo "    timeout $RUN_TIMEOUT $(claude_argv_str "${engine_argv[@]}") < $promptfile > $log 2>&1"
  fi
  exit 0
fi

run_driver() {
  # Run the engine ONCE. Defined as a function (not a generated heredoc script) so the
  # engine_argv array + $REPO/$promptfile/$log survive without a second round of re-quoting.
  # Capture + propagate the engine's real exit code: a 429/cap kill must NOT look like success
  # (a bare success rc would mask cap failures, so empty modules read as "done").
  cd "$REPO" || return 1
  sleep $((RANDOM % 4))  # jitter: avoid simultaneous-launch empty-log collision
  local rc=0
  if [ "$ENGINE" = "copilot" ] || [ "$ENGINE" = "codex" ]; then
    timeout "$RUN_TIMEOUT" "${engine_argv[@]}" > "$log" 2>&1 || rc=$?
  else
    timeout "$RUN_TIMEOUT" "${engine_argv[@]}" < "$promptfile" > "$log" 2>&1 || rc=$?
  fi
  echo "[map] $SOURCE_ID $ENGINE rc=$rc"
  return "$rc"
}

run_with_resume() {
  # Run the driver up to MAX_ATTEMPTS times. Each attempt resumes from persisted partials (the prompt
  # skips done chunks/batches); a per-request timeout/cap kill on a big book then just costs one more
  # attempt instead of a manual re-launch. Stop early once principles.yaml exists (real success).
  local attempt=1
  while [ "$attempt" -le "$MAX_ATTEMPTS" ]; do
    [ "$MAX_ATTEMPTS" -gt 1 ] && echo "[map] $SOURCE_ID attempt $attempt/$MAX_ATTEMPTS"
    # Between attempts, clear only the post-merge artifacts (keep partials/ + chunks) so the re-run
    # re-merges cleanly — same reset the script does once at the top.
    if [ "$attempt" -gt 1 ] && [ ! -f "$MODULE/principles.yaml" ]; then
      rm -f "$MODULE/claims.jsonl" "$MODULE/anchors.jsonl" "$MODULE/module.json"
    fi
    run_driver || true
    [ -f "$MODULE/principles.yaml" ] && { echo "[map] $SOURCE_ID complete after attempt $attempt"; return 0; }
    attempt=$((attempt + 1))
  done
  echo "[map] $SOURCE_ID still incomplete after $MAX_ATTEMPTS attempt(s) — re-run to continue (partials kept)"
  return 1
}

if [ "$FG" -eq 1 ]; then
  # Foreground: this process blocks on the run, so the parent EXIT trap (set at the top)
  # releases $MODULE/.claim only after the work finishes — claim held for the run's lifetime.
  run_with_resume
else
  # Background in a SUBSHELL (not `bash -c "$(declare -f ...) VAR='$VAR' ..."`): the old form
  # string-interpolated user-supplied vars (MODULE/SOURCE_ID from --tag/--cache) into single-quoted
  # assignments — a single quote in them broke the command. The subshell inherits the functions and
  # the engine_argv array intact, so no re-serialization is needed.
  #
  # Claim semantics: bash does NOT run the parent's EXIT trap inside a `( )` subshell, and the parent
  # exits immediately after launching — so the OLD code released $MODULE/.claim while the bg child was
  # still running (another worker could re-claim and double-process). Fix: clear the parent trap for
  # the bg path (so the parent's exit no longer touches the claim) and OWN the release inside the
  # subshell, where it fires when the actual work finishes — including on a crash. `trap '' HUP`
  # + redirected fds + disown give nohup-like detachment so the driver outlives this shell.
  trap - EXIT
  ( trap 'rmdir "$MODULE/.claim" 2>/dev/null' EXIT; trap '' HUP; run_with_resume ) \
    >"$LOGS/$run.driver.log" 2>&1 &
  disown
  echo "[map] launched bg pid $!  transcript: $log  driver log: $LOGS/$run.driver.log"
fi
