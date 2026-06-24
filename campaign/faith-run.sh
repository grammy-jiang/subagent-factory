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

queue(){ python3 "$CAMP/faith-queue.py" ${ONLY:+--only "$ONLY"}; }
next_target(){ queue | head -1; }

echo "[faith] repo=$REPO  model=$MODEL  count=$COUNT  only=${ONLY:-all}"
echo "[faith] packages needing a faithfulness report:"; queue | sed 's/^/  - /'

processed=0
while [ "$processed" -lt "$COUNT" ]; do
  SLUG="$(next_target)" || SLUG=""
  [ -z "$SLUG" ] && { echo "[faith] no packages left needing a report."; break; }
  n=$(ls "$LOGS/$LABEL"-*.summary.md 2>/dev/null | wc -l) || n=0
  run="$(printf '%s-%03d' "$LABEL" "$(( n + 1 ))")"
  log="$LOGS/$run.log.jsonl"
  summ="$LOGS/$run.summary.md"

  echo "============================================================"
  echo "[faith] $run · package $SLUG"

  prompt="$(SLUG="$SLUG" python3 "$CAMP/render-prompt.py" "$TMPL")"

  if [ "$DRYRUN" -eq 1 ]; then
    echo "[faith] DRY-RUN — rendered prompt for $SLUG:"
    printf '%s\n' "$prompt"
    break
  fi

  if [ "$ASSUME_YES" -eq 0 ]; then
    printf "[faith] proceed with %s? [y/N] " "$SLUG"
    read -r ans || ans=""; case "$ans" in y|Y) ;; *) echo "[faith] aborted."; exit 0;; esac
  fi

  start_ts="$(date -Is)"
  echo "[faith] launching claude (timeout ${RUN_TIMEOUT}s) ..."
  rc=0
  printf '%s' "$prompt" | timeout "$RUN_TIMEOUT" claude -p \
      --model "$MODEL" \
      --dangerously-skip-permissions \
      --output-format stream-json --verbose >"$log" 2>&1 || rc=$?

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
