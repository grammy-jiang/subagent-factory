#!/usr/bin/env bash
# Generate ONE subagent package via GitHub Copilot CLI (Opus 4.8, separate billing
# pool from Claude Code). Mirrors generate-subagent.sh but drives `copilot -p` LOCALLY
# (no --remote: the cloud env can't see local staging/corpus). Authoring-only:
# drives /author-subagent end-to-end, validates, STOPS. No commits.
#
# Usage: campaign/generate-subagent-copilot.sh --slug SLUG --topic "TOPIC" \
#            [--sources-file F] [--model M] [--effort E] [--timeout SECS] [--dry-run] [--fg]
set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CAMP="$REPO/campaign"; LOGS="$CAMP/logs"
TMPL="$CAMP/generate-prompt.tmpl"
# Model resolution mirrors generate-subagent.sh: prefer this machine's Opus 4.8 1M
# Bedrock inference-profile ARN ($ANTHROPIC_DEFAULT_OPUS_MODEL, else $ANTHROPIC_MODEL),
# falling back to copilot's dotted opus id. (The dotted form is copilot's id; the dashed
# 'claude-opus-4-8' is the Claude-CLI fallback — keep the dotted one as the last resort.)
MODEL="${MODEL:-${ANTHROPIC_DEFAULT_OPUS_MODEL:-${ANTHROPIC_MODEL:-claude-opus-4.8}}}"
EFFORT="${EFFORT:-max}"
RUN_TIMEOUT="${RUN_TIMEOUT:-9000}"
SLUG=""; TOPIC=""; SRCFILE=""; DRYRUN=0; FG=0

while [ $# -gt 0 ]; do
  case "$1" in
    --slug) SLUG="$2"; shift 2;;
    --topic) TOPIC="$2"; shift 2;;
    --sources-file) SRCFILE="$2"; shift 2;;
    --model) MODEL="$2"; shift 2;;
    --effort) EFFORT="$2"; shift 2;;
    --timeout) RUN_TIMEOUT="$2"; shift 2;;
    --dry-run) DRYRUN=1; shift;;
    --fg) FG=1; shift;;
    -h|--help) grep -E '^# ' "${BASH_SOURCE[0]}" | sed 's/^# //'; exit 0;;
    *) echo "unknown arg: $1" >&2; exit 2;;
  esac
done

[ -n "$SLUG" ]  || { echo "--slug required" >&2; exit 2; }
[ -n "$TOPIC" ] || { echo "--topic required" >&2; exit 2; }
SRCFILE="${SRCFILE:-$CAMP/$SLUG.sources}"
[ -f "$SRCFILE" ] || { echo "sources file not found: $SRCFILE" >&2; exit 3; }
command -v copilot >/dev/null 2>&1 || { echo "copilot CLI not found on PATH" >&2; exit 3; }
mkdir -p "$LOGS"

# Resolve + validate every source; build an ARRAY (paths may contain spaces — a
# space-joined string would word-split and mis-bind sources).
SOURCES=(); n=0; missing=0
while IFS= read -r line; do
  line="${line%$'\r'}"; [ -z "$line" ] && continue
  case "$line" in \#*) continue;; esac
  abs="$line"; case "$abs" in /*) ;; *) abs="$REPO/$line";; esac
  if [ -r "$abs" ]; then SOURCES+=("$abs"); n=$((n+1))
  else echo "  MISSING source: $abs" >&2; missing=$((missing+1)); fi
done < "$SRCFILE"
[ "$missing" -eq 0 ] || { echo "$missing source(s) unreadable — aborting." >&2; exit 3; }
[ "$n" -gt 0 ] || { echo "no sources listed in $SRCFILE" >&2; exit 3; }

# --add-dir for each distinct source directory (deduped) so Copilot may read them.
# Build a flat ARRAY of `--add-dir D` tokens (each dir may contain spaces — a
# space-joined string would word-split). Starts with $REPO, then each unique dir.
declare -A _seen=(); ADDDIRS=(--add-dir "$REPO")
for s in "${SOURCES[@]}"; do
  d="$(dirname "$s")"; [ -n "${_seen[$d]:-}" ] && continue; _seen[$d]=1; ADDDIRS+=(--add-dir "$d")
done

run="gen-$SLUG.copilot"
log="$LOGS/$run.log"
promptfile="$LOGS/$run.prompt.txt"
# render-prompt.py consumes SOURCES as a single env string; join the array with
# newlines (one source per line) so multi-source prompts list cleanly.
SOURCES_STR="$(printf '%s\n' "${SOURCES[@]}")"
REPO="$REPO" SLUG="$SLUG" TOPIC="$TOPIC" SOURCES="$SOURCES_STR" \
    python3 "$CAMP/render-prompt.py" "$TMPL" > "$promptfile"

# Build the copilot argv ONCE as an ARRAY (no generated heredoc, no two-level quoting).
# The copilot invocation is genuinely different from `claude -p`, so it is its own array
# rather than going through build_claude_argv. "${ADDDIRS[@]}" expands to the deduped
# --add-dir tokens; "${copilot_argv[@]}" is shared by the dry-run preview and the real run.
copilot_argv=(copilot -p "$(cat "$promptfile")"
  --model "$MODEL" --effort "$EFFORT"
  --allow-all-tools --allow-all-paths -C "$REPO" "${ADDDIRS[@]}" --context long_context)

echo "[copilot-gen] slug=$SLUG  sources=$n  model=$MODEL  effort=$EFFORT  timeout=${RUN_TIMEOUT}s"
echo "[copilot-gen] sources:"; for s in "${SOURCES[@]}"; do echo "    - $s"; done

if [ "$DRYRUN" -eq 1 ]; then
  echo "[copilot-gen] DRY-RUN — command:"
  echo "  copilot -p <prompt> --model $MODEL --effort $EFFORT --allow-all-tools --allow-all-paths -C $REPO ${ADDDIRS[*]} --context long_context"
  echo "[copilot-gen] prompt rendered to: $promptfile"; exit 0
fi

# Driver function: run copilot, then validate. Defined as a function (not a generated
# heredoc script) so the copilot_argv array and $REPO/$promptfile/$log survive without a
# second round of re-quoting (the old heredoc word-split $ADDDIRS and masked the rc).
# Propagates BOTH stages' rc: a clean copilot run with a FAILING validate must not look
# like success. Final rc written to a sentinel file so background runs are checkable.
rcfile="$LOGS/$run.rc"
run_driver() {
  cd "$REPO" || return 1
  local rc=0
  timeout "$RUN_TIMEOUT" "${copilot_argv[@]}" > "$log" 2>&1 || rc=$?
  echo "[copilot-gen] copilot exited rc=$rc — validating $SLUG ..."
  local venv_py="$REPO/.venv/bin/python"; [ -x "$venv_py" ] || venv_py=python3
  # `| tail` would mask the validate rc under pipefail, so capture PIPESTATUS[0].
  SUBAGENT_FACTORY_USE_VENV=1 "$venv_py" -m tools.subagent_factory.cli validate "$SLUG" 2>&1 | tail -8
  local vrc="${PIPESTATUS[0]}"
  # copilot rc wins if set, else the validate rc.
  [ "$rc" -ne 0 ] || rc="$vrc"
  echo "$rc" > "$rcfile"
  return "$rc"
}

if [ "$FG" -eq 1 ]; then
  # --fg path: run_driver writes the real rc to $rcfile on completion, exactly as before.
  # No sentinel reset here — the foreground caller sees run_driver's own exit status.
  run_driver
else
  # Stamp the sentinel EMPTY before backgrounding. run_driver only writes $rcfile when it
  # completes normally; if the detached subshell is SIGKILLed (OOM, kill -9, reboot) before
  # that write, a stale "0" from a PRIOR run would be misread as this run passing. Truncating
  # to empty first makes "unknown/running" (empty) distinct from a written "0" — a crashed run
  # that never writes its rc reads as empty, not a false pass. run_driver still writes the real
  # rc on normal completion (it does not reset $rcfile itself, so there is no double-reset).
  : > "$rcfile"
  # Background the driver in a SUBSHELL (not a fresh `bash -c`) so the run_driver
  # function and the copilot_argv array are inherited intact — no re-quoting, no
  # generated script. `trap '' HUP` + redirected fds + disown give nohup-like
  # detachment so the driver outlives this shell.
  ( trap '' HUP; run_driver ) >"$LOGS/$run.driver.log" 2>&1 &
  disown
  echo "[copilot-gen] launched in background (pid $!)."
  echo "[copilot-gen] transcript:  $log"
  echo "[copilot-gen] driver log:  $LOGS/$run.driver.log"
  echo "[copilot-gen] exit rc ->   $rcfile (empty = still running/crashed; real rc written when the driver finishes)"
  echo "[copilot-gen] watch:    tail -f $log"
fi
