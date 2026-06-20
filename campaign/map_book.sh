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
MODEL="${MODEL:-${ANTHROPIC_DEFAULT_OPUS_MODEL:-${ANTHROPIC_MODEL:-claude-opus-4-8}}}"
EFFORT="${EFFORT:-max}"; RUN_TIMEOUT="${RUN_TIMEOUT:-7200}"
CACHE="$REPO/cache/book-extracts"
BOOK=""; DRYRUN=0; FG=0
while [ $# -gt 0 ]; do
  case "$1" in
    --book) BOOK="$2"; shift 2;;
    --cache) CACHE="$2"; shift 2;;
    --model) MODEL="$2"; shift 2;;
    --effort) EFFORT="$2"; shift 2;;
    --timeout) RUN_TIMEOUT="$2"; shift 2;;
    --dry-run) DRYRUN=1; shift;;
    --fg) FG=1; shift;;
    *) echo "unknown arg: $1" >&2; exit 2;;
  esac
done
[ -n "$BOOK" ] || { echo "--book <staged.md> required" >&2; exit 2; }
[ -f "$BOOK" ] || { echo "book not found: $BOOK" >&2; exit 3; }
mkdir -p "$LOGS"

# Content-address the module (must match chunk_source.write_book_module: sha256 of file bytes).
SHA="$(sha256sum "$BOOK" | cut -d' ' -f1)"
MODULE="$CACHE/$SHA"
[ -f "$MODULE/chunks.jsonl" ] || { echo "module not chunked yet: $MODULE (run chunk_source first)" >&2; exit 3; }
# source_id = <title-slug truncated 20>-<sha8>  (matches the factory's existing source_id style).
STEM="$(basename "$BOOK" .md)"
SLUG="$(printf '%s' "$STEM" | tr '[:upper:]' '[:lower:]' | tr -c 'a-z0-9' '-' | sed 's/-\{2,\}/-/g; s/^-//; s/-$//' | cut -c1-20 | sed 's/-$//')"
SOURCE_ID="${SLUG}-${SHA:0:8}"
TITLE="$STEM"

run="map-$SOURCE_ID"; log="$LOGS/$run.log.jsonl"; promptfile="$LOGS/$run.prompt.txt"
REPO="$REPO" MODULE="$MODULE" SOURCE_ID="$SOURCE_ID" TITLE="$TITLE" \
  python3 "$CAMP/render-prompt.py" "$TMPL" > "$promptfile"
echo "[map] book=$STEM  source_id=$SOURCE_ID  module=$MODULE  model=$MODEL effort=$EFFORT"
echo "[map] chunks=$(grep -c . "$MODULE/chunks.jsonl")"

if [ "$DRYRUN" -eq 1 ]; then echo "[map] DRY-RUN; prompt: $promptfile"; exit 0; fi

driver="$LOGS/$run.driver.sh"
{
  echo '#!/usr/bin/env bash'
  echo "cd \"$REPO\""
  echo "timeout \"$RUN_TIMEOUT\" \"$CLAUDE_BIN\" -p --model \"$MODEL\" --effort \"$EFFORT\" --add-dir \"$REPO\" \\"
  echo "    --dangerously-skip-permissions --output-format stream-json --verbose \\"
  echo "    < \"$promptfile\" > \"$log\" 2>&1"
  echo "echo \"[map] $SOURCE_ID claude rc=\$?\""
} > "$driver"
chmod +x "$driver"

if [ "$FG" -eq 1 ]; then bash "$driver"; else
  nohup bash "$driver" >"$LOGS/$run.driver.log" 2>&1 &
  echo "[map] launched bg pid $!  transcript: $log"
fi
