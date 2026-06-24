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
CLAUDE_BIN="${CLAUDE_BIN:-$HOME/.local/bin/claude}"
COPILOT_BIN="${COPILOT_BIN:-$HOME/.local/bin/copilot}"
COPILOT_MODEL="${COPILOT_MODEL:-claude-opus-4.8}"   # Copilot's opus id (dot, not dash)
COPILOT_EFFORT="${COPILOT_EFFORT:-high}"            # Copilot max effort is "high"
MODEL="${MODEL:-${ANTHROPIC_DEFAULT_OPUS_MODEL:-${ANTHROPIC_MODEL:-claude-opus-4-8}}}"
EFFORT="${EFFORT:-max}"; RUN_TIMEOUT="${RUN_TIMEOUT:-7200}"
CACHE="$REPO/cache/book-extracts"
ENGINE="claude"; TAG=""
BOOK=""; DRYRUN=0; FG=0; FORCE=0; MAX_ATTEMPTS=1
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

if [ "$DRYRUN" -eq 1 ]; then echo "[map] DRY-RUN; prompt: $promptfile"; exit 0; fi

driver="$LOGS/$run.driver.sh"
{
  echo '#!/usr/bin/env bash'
  echo "cd \"$REPO\" || exit 1"
  echo 'sleep $((RANDOM % 4))  # jitter: avoid simultaneous-launch empty-log collision'
  if [ "$ENGINE" = "copilot" ]; then
    echo "timeout \"$RUN_TIMEOUT\" \"$COPILOT_BIN\" -p \"\$(cat '$promptfile')\" --model \"$COPILOT_MODEL\" --effort \"$COPILOT_EFFORT\" --allow-all > \"$log\" 2>&1"
  else
    echo "timeout \"$RUN_TIMEOUT\" \"$CLAUDE_BIN\" -p --model \"$MODEL\" --effort \"$EFFORT\" --add-dir \"$REPO\" \\"
    echo "    --dangerously-skip-permissions --output-format stream-json --verbose \\"
    echo "    < \"$promptfile\" > \"$log\" 2>&1"
  fi
  # Capture + propagate the engine's real exit code: a 429/cap kill must NOT look like success
  # (the bare `echo` returned 0, masking cap failures so empty modules read as "done").
  echo "rc=\$?; echo \"[map] $SOURCE_ID $ENGINE rc=\$rc\"; exit \$rc"
} > "$driver"
chmod +x "$driver"

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
    bash "$driver" || true
    [ -f "$MODULE/principles.yaml" ] && { echo "[map] $SOURCE_ID complete after attempt $attempt"; return 0; }
    attempt=$((attempt + 1))
  done
  echo "[map] $SOURCE_ID still incomplete after $MAX_ATTEMPTS attempt(s) — re-run to continue (partials kept)"
  return 1
}

if [ "$FG" -eq 1 ]; then run_with_resume; else
  nohup bash -c "$(declare -f run_with_resume); MODULE='$MODULE' SOURCE_ID='$SOURCE_ID' MAX_ATTEMPTS='$MAX_ATTEMPTS' driver='$driver' run_with_resume" \
    >"$LOGS/$run.driver.log" 2>&1 &
  echo "[map] launched bg pid $!  transcript: $log"
fi
