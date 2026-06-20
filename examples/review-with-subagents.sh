#!/usr/bin/env bash
# Review any document with this repo's GENERATED reviewer subagents, in a FRESH headless
# Claude Code instance (separate from any interactive session — no context pollution).
#
# The headless instance runs from the factory repo (so .claude/agents/generated/ adapters are
# discoverable), reads the target doc, spawns the named reviewer subagents to critique it, and
# writes a synthesized review next to the doc.
#
# Usage:
#   examples/review-with-subagents.sh <doc-path> [--reviewers a,b,c] [--out PATH]
#                                     [--model M] [--timeout SECS] [--dry-run]
#
# Defaults: reviewers = software-design,software-architecture,microservice-patterns-advisor
#           out       = <doc-dir>/reviews/<doc-name>.subagent-review.<date>.md
#
# List available reviewers:  python -m tools.subagent_factory.cli catalog
set -uo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MODEL="${MODEL:-claude-opus-4-8}"
RUN_TIMEOUT="${RUN_TIMEOUT:-3600}"
REVIEWERS="software-design,software-architecture,microservice-patterns-advisor"
OUT=""
DRYRUN=0
DOC=""

while [ $# -gt 0 ]; do
  case "$1" in
    --reviewers) REVIEWERS="$2"; shift 2;;
    --out) OUT="$2"; shift 2;;
    --model) MODEL="$2"; shift 2;;
    --timeout) RUN_TIMEOUT="$2"; shift 2;;
    --dry-run) DRYRUN=1; shift;;
    -h|--help) grep -E '^# ' "${BASH_SOURCE[0]}" | sed 's/^# //'; exit 0;;
    -*) echo "unknown arg: $1" >&2; exit 2;;
    *) DOC="$1"; shift;;
  esac
done

[ -n "$DOC" ] || { echo "usage: review-with-subagents.sh <doc-path> [--reviewers ..] [--out ..]" >&2; exit 2; }
DOC="$(cd "$(dirname "$DOC")" && pwd)/$(basename "$DOC")"   # absolutize
[ -f "$DOC" ] || { echo "doc not found: $DOC" >&2; exit 2; }
command -v claude >/dev/null 2>&1 || { echo "claude CLI not found on PATH" >&2; exit 3; }

DOCDIR="$(dirname "$DOC")"
if [ -z "$OUT" ]; then
  base="$(basename "$DOC")"; base="${base%.md}"
  OUT="$DOCDIR/reviews/${base}.subagent-review.$(date +%Y%m%d).md"
fi
mkdir -p "$(dirname "$OUT")"
LOGS="$REPO/campaign/logs"; mkdir -p "$LOGS"
log="$LOGS/review-$(date +%Y%m%d-%H%M%S).log.jsonl"

prompt="$(DOC="$DOC" REVIEWERS="$REVIEWERS" OUT="$OUT" \
          python3 "$REPO/campaign/render-prompt.py" "$REPO/examples/review-prompt.tmpl")"

echo "[review] doc=$DOC"
echo "[review] reviewers=$REVIEWERS"
echo "[review] out=$OUT"
echo "[review] model=$MODEL  (headless, fresh instance)"

if [ "$DRYRUN" -eq 1 ]; then
  echo "------------------ rendered prompt ------------------"; printf '%s\n' "$prompt"; exit 0
fi

echo "[review] launching claude (timeout ${RUN_TIMEOUT}s) ..."
( cd "$REPO" && printf '%s' "$prompt" | timeout "$RUN_TIMEOUT" claude -p \
    --model "$MODEL" \
    --add-dir "$DOCDIR" \
    --dangerously-skip-permissions \
    --output-format stream-json --verbose ) >"$log" 2>&1
rc=$?

echo "[review] rc=$rc  log=$log"
if [ -f "$OUT" ]; then
  echo "[review] review written: $OUT  ($(wc -l <"$OUT") lines)"
else
  echo "[review] NO review file produced — inspect $log (rc=$rc)."
fi
