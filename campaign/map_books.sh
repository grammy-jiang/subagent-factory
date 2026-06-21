#!/usr/bin/env bash
# map_books.sh — cap-aware batch MAP over many books for ONE package. Chunks each book (idempotent)
# then MAPs it via map_book.sh, which self-resets a partial/cap-killed module and propagates the
# engine's real exit code. Reports REAL success by principles.yaml (a 429/cap kill must not read as
# done). Written as a bash file + bash arrays — the Claude Bash tool runs zsh, where ${arr[@]} /
# ${!arr[@]} misbehave, so inline launchers break; run this with `bash`.
#
# Usage: campaign/map_books.sh --sources campaign/<slug>.sources [--engine claude|copilot]
#                              [--parallel N] [--timeout SECS]
#        campaign/map_books.sh --book A.md --book B.md [...]
#
# Default is SERIAL (--parallel 1): concurrent heavy MAP runs split one spend-cap top-up and all
# fail partial. Serialize; raise --parallel only when the cap has headroom. Re-running is safe —
# completed modules skip, incomplete (cap-killed) modules are auto-reset by map_book.sh.
set -uo pipefail
REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CACHE="$REPO/cache/book-extracts"
ENGINE="claude"; PAR=1; TIMEOUT=""; SRCFILE=""; BOOKS=()
while [ $# -gt 0 ]; do
  case "$1" in
    --sources) SRCFILE="$2"; shift 2;;
    --book) BOOKS+=("$2"); shift 2;;
    --engine) ENGINE="$2"; shift 2;;
    --parallel) PAR="$2"; shift 2;;
    --timeout) TIMEOUT="$2"; shift 2;;
    -h|--help) grep -E '^# ' "${BASH_SOURCE[0]}" | sed 's/^# //'; exit 0;;
    *) echo "unknown arg: $1" >&2; exit 2;;
  esac
done
if [ -n "$SRCFILE" ]; then
  [ -f "$SRCFILE" ] || { echo "sources file not found: $SRCFILE" >&2; exit 3; }
  while IFS= read -r line; do
    line="${line%$'\r'}"; [ -z "$line" ] && continue
    case "$line" in \#*) continue;; esac
    case "$line" in /*) BOOKS+=("$line");; *) BOOKS+=("$REPO/$line");; esac
  done < "$SRCFILE"
fi
[ "${#BOOKS[@]}" -gt 0 ] || { echo "no books (use --sources or --book)" >&2; exit 2; }

TFLAG=(); [ -n "$TIMEOUT" ] && TFLAG=(--timeout "$TIMEOUT")
echo "[map-books] ${#BOOKS[@]} books  engine=$ENGINE  parallel=$PAR"

run_one() {
  local b="$1"
  # Chunk first (deterministic, idempotent) so map_book has a module to MAP.
  python3 -c "from tools.subagent_factory.chunk_source import write_book_module; from pathlib import Path; write_book_module(Path('$b'), Path('$CACHE'))" 2>/dev/null
  bash "$REPO/campaign/map_book.sh" --book "$b" --engine "$ENGINE" "${TFLAG[@]}" --fg \
    > "/tmp/mapbooks-$(basename "$b" .md).out" 2>&1
}

cd "$REPO"
if [ "$PAR" -le 1 ]; then
  for b in "${BOOKS[@]}"; do echo "[map-books] -> $(basename "$b")"; run_one "$b" || true; done
else
  i=0; pids=()
  for b in "${BOOKS[@]}"; do
    run_one "$b" & pids+=($!); i=$((i+1))
    if [ "$((i % PAR))" -eq 0 ]; then for p in "${pids[@]}"; do wait "$p" || true; done; pids=(); fi
  done
  for p in "${pids[@]}"; do wait "$p" || true; done
fi

echo "=== MAP results (real success = principles.yaml present) ==="
ok=0; bad=0
for b in "${BOOKS[@]}"; do
  sha=$(sha256sum "$b" | cut -d' ' -f1); m="$CACHE/$sha"
  if [ -f "$m/principles.yaml" ]; then
    echo "  OK   $(basename "$b" .md): $(grep -c . "$m/claims.jsonl" 2>/dev/null) claims"; ok=$((ok+1))
  else
    echo "  FAIL $(basename "$b" .md): no principles.yaml (cap/429? see /tmp/mapbooks-$(basename "$b" .md).out)"; bad=$((bad+1))
  fi
done
echo "[map-books] $ok ok, $bad incomplete"
[ "$bad" -eq 0 ]
