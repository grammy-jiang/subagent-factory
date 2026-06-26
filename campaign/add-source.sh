#!/usr/bin/env bash
# Incrementally add source(s) to an EXISTING package via the subagent-maintenance flow, in a
# fresh headless Claude session (no Copilot — its 2a cap under-extracts). Preserves existing
# claims/principles, appends only the new source(s). Authoring-only; validates; STOPS.
#
# Usage: campaign/add-source.sh --slug SLUG --sources-file F [--timeout SECS] [--dry-run] [--fg]
set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CAMP="$REPO/campaign"; LOGS="$CAMP/logs"; TMPL="$CAMP/maintenance-prompt.tmpl"
# Single source of truth for the `claude -p` argv (shared with generate-subagent.sh/run.sh).
source "$CAMP/_claude_run.sh"
MODEL="${ANTHROPIC_DEFAULT_OPUS_MODEL:-${ANTHROPIC_MODEL:-claude-opus-4-8}}"
EFFORT="${EFFORT:-max}"; RUN_TIMEOUT="${RUN_TIMEOUT:-7200}"
SLUG=""; SRCFILE=""; DRYRUN=0; FG=0
while [ $# -gt 0 ]; do
  case "$1" in
    --slug) SLUG="$2"; shift 2;;
    --sources-file) SRCFILE="$2"; shift 2;;
    --timeout) RUN_TIMEOUT="$2"; shift 2;;
    --dry-run) DRYRUN=1; shift;;
    --fg) FG=1; shift;;
    *) echo "unknown arg: $1" >&2; exit 2;;
  esac
done
[ -n "$SLUG" ] || { echo "--slug required" >&2; exit 2; }
[ -d "$REPO/subagents/$SLUG" ] || { echo "package subagents/$SLUG must already exist" >&2; exit 3; }
SRCFILE="${SRCFILE:-$CAMP/$SLUG-new.sources}"
[ -f "$SRCFILE" ] || { echo "new-sources file not found: $SRCFILE" >&2; exit 3; }
mkdir -p "$LOGS"

# Resolve + validate every new source; build an ARRAY (paths may contain spaces —
# a space-joined string would word-split and mis-bind sources / --add-dir flags).
SOURCES=(); n=0
while IFS= read -r line; do
  line="${line%$'\r'}"; [ -z "$line" ] && continue; case "$line" in \#*) continue;; esac
  abs="$line"; case "$abs" in /*) ;; *) abs="$REPO/$line";; esac
  [ -r "$abs" ] || { echo "MISSING new source: $abs" >&2; exit 3; }
  SOURCES+=("$abs"); n=$((n+1))
done < "$SRCFILE"
[ "$n" -gt 0 ] || { echo "no new sources in $SRCFILE" >&2; exit 3; }

# add-dir for the repo plus each distinct source directory (dirs may repeat across
# sources; a path may contain spaces). build_claude_argv() turns each into its own
# --add-dir D.
declare -A _seen=(); ADDDIRS=("$REPO")
for s in "${SOURCES[@]}"; do d="$(dirname "$s")"; [ -n "${_seen[$d]:-}" ] && continue; _seen[$d]=1; ADDDIRS+=("$d"); done

# Timestamp the run name so concurrent or repeat runs don't clobber each other's
# log/prompt/driver files (this script backgrounds itself via nohup).
run="addsrc-$SLUG-$(date +%s)"; log="$LOGS/$run.log.jsonl"; promptfile="$LOGS/$run.prompt.txt"
# render-prompt.py consumes SOURCES as a single env string; join the array with
# newlines (one source per line) so multi-source prompts list cleanly.
SOURCES_STR="$(printf '%s\n' "${SOURCES[@]}")"
REPO="$REPO" SLUG="$SLUG" SOURCES="$SOURCES_STR" python3 "$CAMP/render-prompt.py" "$TMPL" > "$promptfile"
# Guard against a multi-hour claude run on an empty prompt (render failure).
[ -s "$promptfile" ] || { echo "render-prompt produced empty prompt" >&2; exit 4; }

# Build the claude argv ONCE; the --dry-run preview and the real run share it.
build_claude_argv claude_argv "$MODEL" "$EFFORT" "${ADDDIRS[@]}"

echo "[add-source] slug=$SLUG  new-sources=$n  model=$MODEL  effort=$EFFORT"
for s in "${SOURCES[@]}"; do echo "    + $s"; done

if [ "$DRYRUN" -eq 1 ]; then
  echo "[add-source] DRY-RUN — command:"
  echo "  timeout $RUN_TIMEOUT $(claude_argv_str "${claude_argv[@]}") < $promptfile"
  echo "[add-source] prompt rendered to: $promptfile"
  exit 0
fi

# Driver function: feed prompt from file, run claude, then validate. Defined as a
# function (not a generated heredoc script) so the claude_argv array and
# $REPO/$promptfile/$log survive without a second round of re-quoting. It propagates
# the combined claude+validate rc as its own exit status (a backgrounded run writes it
# to $rcfile) — a `| tail` alone would mask the failure as success.
rcfile="$LOGS/$run.rc"
run_driver() {
  cd "$REPO" || return 1
  local rc=0
  timeout "$RUN_TIMEOUT" "${claude_argv[@]}" < "$promptfile" > "$log" 2>&1 || rc=$?
  echo "[add-source] claude rc=$rc — validating $SLUG"
  local venv_py="$REPO/.venv/bin/python"; [ -x "$venv_py" ] || venv_py=python3
  # `| tail` would mask the validate rc under pipefail, so capture PIPESTATUS[0].
  SUBAGENT_FACTORY_USE_VENV=1 "$venv_py" -m tools.subagent_factory.cli validate "$SLUG" 2>&1 | tail -6
  local vrc="${PIPESTATUS[0]}"
  # Final rc reflects BOTH stages: a clean claude run with a failing validate must not
  # look like success. claude rc wins if set, else the validate rc.
  [ "$rc" -ne 0 ] || rc="$vrc"
  echo "$rc" > "$rcfile"
  return "$rc"
}

if [ "$FG" -eq 1 ]; then
  run_driver
else
  ( trap '' HUP; run_driver ) >"$LOGS/$run.driver.log" 2>&1 &
  disown
  echo "[add-source] launched bg pid $!  transcript: $log"
  echo "[add-source] exit rc -> $rcfile (written when the driver finishes)"
fi
