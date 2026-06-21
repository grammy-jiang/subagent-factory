#!/usr/bin/env bash
# map_book.sh — run ONE book's MAP step (deep per-chunk claim extraction + principle
# promotion) over a PRE-CHUNKED module from tools.subagent_factory.chunk_source, in a fresh
# headless Claude session. Writes claims.jsonl + principles.yaml + module.json into the module
# dir and STOPS. Top-level `claude -p` (can spawn sub-agents; no sub-agent stall).
#
# Usage: campaign/map_book.sh --book <staged.md> [--cache cache/book-extracts]
#                             [--model M] [--effort max] [--timeout SECS] [--dry-run] [--fg]
set -uo pipefail

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
BOOK=""; DRYRUN=0; FG=0; FORCE=0
while [ $# -gt 0 ]; do
  case "$1" in
    --book) BOOK="$2"; shift 2;;
    --cache) CACHE="$2"; shift 2;;
    --model) MODEL="$2"; shift 2;;
    --effort) EFFORT="$2"; shift 2;;
    --timeout) RUN_TIMEOUT="$2"; shift 2;;
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

# A prior run that died (cap/429, timeout) leaves a partial claims.jsonl but no principles.yaml;
# the MAP prompt APPENDS, so re-running would duplicate claims and collide C-ids. Reset the partial
# extraction outputs — but KEEP the deterministic chunks (chunks.jsonl, chunks/, source.md).
if [ -f "$MODULE/claims.jsonl" ] && [ ! -f "$MODULE/principles.yaml" ]; then
  echo "[map] $SOURCE_ID has a partial (incomplete) extraction — resetting before re-MAP"
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
  echo "cd \"$REPO\""
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

if [ "$FG" -eq 1 ]; then bash "$driver"; else
  nohup bash "$driver" >"$LOGS/$run.driver.log" 2>&1 &
  echo "[map] launched bg pid $!  transcript: $log"
fi
