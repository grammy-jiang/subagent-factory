#!/usr/bin/env bash
# map_books.sh — cap-aware batch MAP over many books for ONE package. Chunks each book (idempotent)
# then MAPs it via map_book.sh, which self-resets a partial/cap-killed module and propagates the
# engine's real exit code. Reports REAL success by principles.yaml (a 429/cap kill must not read as
# done). Written as a bash file + bash arrays — the Claude Bash tool runs zsh, where ${arr[@]} /
# ${!arr[@]} misbehave, so inline launchers break; run this with `bash`.
#
# Usage: campaign/map_books.sh --sources campaign/<slug>.sources [--engine claude|copilot]
#                              [--parallel N] [--timeout SECS] [--max-attempts N]
#        campaign/map_books.sh --book A.md --book B.md [...]
#
# --max-attempts N (default 1): per-book auto-resume — retry each book up to N runs until its
#   principles.yaml exists. A big book that times out per-request mid-session then finishes
#   unattended instead of needing a manual re-run. Resumes from persisted partials each attempt.
#
# Default is SERIAL (--parallel 1): concurrent heavy MAP runs split one spend-cap top-up and all
# fail partial. Serialize; raise --parallel only when the cap has headroom. Re-running is safe —
# completed modules skip, incomplete (cap-killed) modules are auto-reset by map_book.sh.
set -euo pipefail
REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CACHE="$REPO/cache/book-extracts"
ENGINE="claude"; PAR=1; TIMEOUT=""; SRCFILE=""; BOOKS=(); MAX_ATTEMPTS=1
while [ $# -gt 0 ]; do
  case "$1" in
    --sources) SRCFILE="$2"; shift 2;;
    --book) BOOKS+=("$2"); shift 2;;
    --engine) ENGINE="$2"; shift 2;;
    --parallel) PAR="$2"; shift 2;;
    --timeout) TIMEOUT="$2"; shift 2;;
    --max-attempts) MAX_ATTEMPTS="$2"; shift 2;;  # per-book auto-resume across N runs (big-book timeouts)
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
  # Per-book out file keyed on the book's sha (not basename): two books sharing a
  # basename would otherwise clobber each other's log under --parallel.
  local bsha; bsha="$(sha256sum "$b" 2>/dev/null | cut -d' ' -f1)" || bsha=""
  local out="/tmp/mapbooks-${bsha:-$(basename "$b" .md)}.out"
  # Chunk first (deterministic, idempotent) so map_book has a module to MAP.
  # Pass the paths as ARGV (sys.argv), never interpolated into the Python source:
  # a path with a quote/$/backtick/newline would otherwise break out of the literal
  # and execute, and a space would silently mis-bind. Keep stderr visible (into the
  # per-book out file) so a chunk failure surfaces here, not as a downstream map error.
  # Gate the MAP launch on the chunk step's rc EXPLICITLY: run_one is always invoked
  # as `run_one ... || true` (serial) or `run_one ... &` (parallel), which disables
  # set -e inside this function body — so a bare chained command would NOT abort on a
  # chunk crash. If chunking fails (import error, unwritable cache) there is no module
  # to MAP; emit a DISTINCT CHUNK-FAIL marker and return non-zero so the failure is
  # attributable here, instead of being misreported downstream as a generic cap/429 kill.
  python3 -c 'import sys; from pathlib import Path; from tools.subagent_factory.chunk_source import write_book_module as w; w(Path(sys.argv[1]), Path(sys.argv[2]))' "$b" "$CACHE" \
    > "$out" 2>&1 || { echo "CHUNK-FAIL $b" >> "$out"; return 1; }
  bash "$REPO/campaign/map_book.sh" --book "$b" --engine "$ENGINE" "${TFLAG[@]}" \
    --max-attempts "$MAX_ATTEMPTS" --fg \
    >> "$out" 2>&1
}

cd "$REPO" || exit 1
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
  sha=$(sha256sum "$b" 2>/dev/null | cut -d' ' -f1) || sha=""
  if [ -z "$sha" ]; then echo "  FAIL $(basename "$b" .md): cannot hash (missing/unreadable)"; bad=$((bad+1)); continue; fi
  m="$CACHE/$sha"
  if [ -f "$m/principles.yaml" ]; then
    echo "  OK   $(basename "$b" .md): $(grep -c . "$m/claims.jsonl" 2>/dev/null) claims"; ok=$((ok+1))
  elif grep -q "^CHUNK-FAIL " "/tmp/mapbooks-$sha.out" 2>/dev/null; then
    echo "  FAIL $(basename "$b" .md): chunk step failed before MAP (CHUNK-FAIL, see /tmp/mapbooks-$sha.out)"; bad=$((bad+1))
  else
    echo "  FAIL $(basename "$b" .md): no principles.yaml (cap/429? see /tmp/mapbooks-$sha.out)"; bad=$((bad+1))
  fi
done
echo "[map-books] $ok ok, $bad incomplete"
[ "$bad" -eq 0 ]
