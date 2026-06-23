#!/usr/bin/env bash
# Serial, resumable multi-reviewer sweep over a list of files. Wraps the existing
# examples/review-with-subagents.sh (one fresh headless session per file) — skip-if-done so a
# flaky-endpoint timeout just re-runs the remaining files. Reviewers: python +
# software-engineering-practices (code-quality lenses). Reviews land in <dir>/reviews/.
#
# Usage: bash campaign/review_scripts.sh <listfile> [--reviewers a,b] [--timeout SECS]
set -uo pipefail
REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LIST="${1:?usage: review_scripts.sh <listfile> [--reviewers a,b] [--timeout S]}"; shift || true
REVIEWERS="python,software-engineering-practices"; TIMEOUT=2400
while [ $# -gt 0 ]; do
  case "$1" in
    --reviewers) REVIEWERS="$2"; shift 2;;
    --timeout) TIMEOUT="$2"; shift 2;;
    *) echo "unknown arg: $1" >&2; exit 2;;
  esac
done
export MODEL="${ANTHROPIC_DEFAULT_OPUS_MODEL:-${ANTHROPIC_MODEL:-claude-opus-4-8}}"
date="$(date +%Y%m%d)"; ok=0; skip=0; bad=0
while IFS= read -r f; do
  f="${f%$'\r'}"; [ -z "$f" ] && continue; case "$f" in \#*) continue;; esac
  base="$(basename "$f")"; base="${base%.md}"
  out="$REPO/$(dirname "$f")/reviews/${base}.subagent-review.${date}.md"
  if [ -f "$out" ]; then echo "[sweep] skip (done): $f"; skip=$((skip+1)); continue; fi
  echo "[sweep] review: $f"
  RUN_TIMEOUT="$TIMEOUT" bash "$REPO/examples/review-with-subagents.sh" "$REPO/$f" \
    --reviewers "$REVIEWERS" >/dev/null 2>&1
  if [ -f "$out" ]; then echo "  ok -> $out"; ok=$((ok+1)); else echo "  FAIL (no review, timeout?)"; bad=$((bad+1)); fi
done < "$LIST"
echo "[sweep] done: $ok reviewed, $skip skipped, $bad failed"
[ "$bad" -eq 0 ]
