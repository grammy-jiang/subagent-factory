#!/usr/bin/env bash
# Faithfulness campaign — run faithfulness-review over ready packages that lack a
# valid faithfulness report, one fresh headless Claude session per package. Done =
# the package gains a reports/faithfulness-report.yaml that passes its validator.
# Packages are gitignored artifacts, so rounds produce no commits.
#
# Usage: campaign/faith-run.sh [-n N | --all] [--only s,s,...]
#                              [--model M] [--timeout SECS] [--dry-run] [--yes]
set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CAMP="$REPO/campaign"
# Single source of truth for the `claude -p` argv (shared with run.sh / generate-subagent.sh).
source "$CAMP/_claude_run.sh"
LOGS="$CAMP/logs"
TMPL="$CAMP/faith-prompt.tmpl"
MODEL="${MODEL:-claude-opus-4-8}"
RUN_TIMEOUT="${RUN_TIMEOUT:-3000}"
LABEL="${LABEL:-faith}"   # run-name prefix; set distinct per instance for parallel runs
COUNT=1
ONLY=""
DRYRUN=0
ASSUME_YES=0

while [ $# -gt 0 ]; do
  case "$1" in
    -n|--count) COUNT="$2"; shift 2;;
    --all) COUNT=100000; shift;;
    --only) ONLY="$2"; shift 2;;
    --model) MODEL="$2"; shift 2;;
    --timeout) RUN_TIMEOUT="$2"; shift 2;;
    --dry-run) DRYRUN=1; shift;;
    --yes) ASSUME_YES=1; shift;;
    -h|--help) grep -E '^# ' "${BASH_SOURCE[0]}" | sed 's/^# //'; exit 0;;
    *) echo "unknown arg: $1" >&2; exit 2;;
  esac
done

mkdir -p "$LOGS"
command -v claude >/dev/null 2>&1 || { echo "claude CLI not found on PATH" >&2; exit 3; }

queue(){ local a=(); [ -n "$ONLY" ] && a=(--only "$ONLY"); python3 "$CAMP/faith-queue.py" "${a[@]}"; }
next_target(){ queue | head -1; }

echo "[faith] repo=$REPO  model=$MODEL  count=$COUNT  only=${ONLY:-all}"
echo "[faith] packages needing a faithfulness report:"; queue | sed 's/^/  - /'

processed=0
while [ "$processed" -lt "$COUNT" ]; do
  SLUG="$(next_target)"
  [ -z "$SLUG" ] && { echo "[faith] no packages left needing a report."; break; }
  # Authoritative, monotonic, collision-safe run id (matches run.sh). The old
  # counter (count of *.summary.md + 1) collided whenever a summary was deleted
  # or two LABEL-tagged instances raced, silently overwriting $log/$summ. A
  # timestamp plus the PID suffix is unique across quick successive / parallel runs.
  run="$LABEL-$(date +%Y%m%d-%H%M%S)-$$"
  log="$LOGS/$run.log.jsonl"
  summ="$LOGS/$run.summary.md"

  echo "============================================================"
  echo "[faith] $run · package $SLUG"

  prompt="$(SLUG="$SLUG" python3 "$CAMP/render-prompt.py" "$TMPL")"

  if [ "$DRYRUN" -eq 1 ]; then
    # Same argv the real run uses (build_claude_argv with empty effort, no --add-dir).
    build_claude_argv claude_argv "$MODEL" ""
    echo "[faith] DRY-RUN — command that would run:"
    echo "    timeout $RUN_TIMEOUT $(claude_argv_str "${claude_argv[@]}") <<<\"\$prompt\""
    echo "[faith] log -> $log"
    echo "[faith] summary -> $summ"
    echo "------------------ rendered prompt ------------------"
    printf '%s\n' "$prompt"
    echo "---------------- end rendered prompt ----------------"
    break
  fi

  if [ "$ASSUME_YES" -eq 0 ]; then
    printf "[faith] proceed with %s? [y/N] " "$SLUG"
    read -r ans || ans=""; case "$ans" in y|Y) ;; *) echo "[faith] aborted."; exit 0;; esac
  fi

  start_ts="$(date -Is)"
  echo "[faith] launching claude (timeout ${RUN_TIMEOUT}s) ..."
  rc=0
  # Build the claude argv from the shared contract. This driver deliberately
  # passes NO --effort and NO --add-dir (empty effort arg, no trailing dirs) —
  # that omission is now a visible argument rather than a silent flag-set diff.
  build_claude_argv claude_argv "$MODEL" ""
  # Feed the prompt via here-string (not `printf | claude`): under `pipefail` a
  # SIGPIPE on the writer (claude draining early) would surface as rc 141 and be
  # misattributed to the gate. A redirect makes claude's rc the only rc.
  timeout "$RUN_TIMEOUT" "${claude_argv[@]}" <<<"$prompt" >"$log" 2>&1 || rc=$?

  if make -C "$REPO" verify >"$LOGS/$run.verify.log" 2>&1; then verify=green; else verify=red; fi

  gate="$(REPO="$REPO" LOG="$log" SUMM="$summ" RUN="$run" SLUG="$SLUG" RC="$rc" \
          START="$start_ts" VERIFY="$verify" python3 "$CAMP/faith-gate.py")"

  echo "[faith] $run gate=$gate verify=$verify rc=$rc  (summary: $summ)"
  case "$gate" in
    ok) processed=$(( processed + 1 ));;
    usage-limit) echo "[faith] >>> USAGE LIMIT — stopping. Re-run to resume."; exit 0;;
    *) echo "[faith] >>> gate=$gate — stopping for review. See $summ (and $log)."; exit 0;;
  esac
  sleep 2
done

echo "[faith] finished: $processed report(s) generated this invocation."
