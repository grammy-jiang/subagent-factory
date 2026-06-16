#!/usr/bin/env bash
# Authoring campaign — run author-skills over draft packages to fill stub bodies
# and promote draft -> ready, one fresh headless Claude session per package.
# Queue = draft packages that currently validate, tier >= TIER_MIN (grounded
# first, richest authoring). Done = package becomes status: ready and still
# validates. Packages are gitignored artifacts, so rounds produce no commits.
# Deterministic orchestration only; the LLM authors the bodies. See author-gate.py.
#
# Usage: campaign/author-run.sh [-n N | --all] [--tier-min T] [--only s,s,...]
#                               [--model M] [--timeout SECS] [--dry-run] [--yes]
set -uo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CAMP="$REPO/campaign"
LOGS="$CAMP/logs"
TMPL="$CAMP/author-prompt.tmpl"
# Default to this machine's Opus 4.8 1M Bedrock ARN; public ids 400 here. See GENERATE-REVIEW.md.
MODEL="${MODEL:-${ANTHROPIC_DEFAULT_OPUS_MODEL:-${ANTHROPIC_MODEL:-claude-opus-4-8}}}"
EFFORT="${EFFORT:-max}"
RUN_TIMEOUT="${RUN_TIMEOUT:-3000}"
LABEL="${LABEL:-author}"   # run-name prefix; set distinct per instance for parallel runs
COUNT=1
TIER_MIN=1
ONLY=""
DRYRUN=0
ASSUME_YES=0

while [ $# -gt 0 ]; do
  case "$1" in
    -n|--count) COUNT="$2"; shift 2;;
    --all) COUNT=100000; shift;;
    --tier-min) TIER_MIN="$2"; shift 2;;
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

# Helper scripts import tools.subagent_factory (needs slugify etc.) — use the managed
# .venv interpreter when present so they don't fail on a bare system python3.
PY="python3"; [ -x "$REPO/.venv/bin/python" ] && PY="$REPO/.venv/bin/python"

queue(){ "$PY" "$CAMP/author-queue.py" "$TIER_MIN" ${ONLY:+--only "$ONLY"}; }
next_target(){ queue | head -1; }

echo "[author] repo=$REPO  model=$MODEL  count=$COUNT  tier_min=$TIER_MIN  only=${ONLY:-all}"
echo "[author] eligible draft packages:"; queue | sed 's/^/  - /'

processed=0
while [ "$processed" -lt "$COUNT" ]; do
  SLUG="$(next_target)"
  [ -z "$SLUG" ] && { echo "[author] no eligible draft packages left."; break; }
  n=$(ls "$LOGS/$LABEL"-*.summary.md 2>/dev/null | wc -l)
  run="$(printf '%s-%03d' "$LABEL" "$(( n + 1 ))")"
  log="$LOGS/$run.log.jsonl"
  summ="$LOGS/$run.summary.md"

  echo "============================================================"
  echo "[author] $run · package $SLUG"

  prompt="$(SLUG="$SLUG" RECENT_COMMITS="$(git -C "$REPO" log --oneline -8)" \
            "$PY" "$CAMP/render-prompt.py" "$TMPL")"

  if [ "$DRYRUN" -eq 1 ]; then
    echo "[author] DRY-RUN — rendered prompt for $SLUG:"
    printf '%s\n' "$prompt"
    break
  fi

  if [ "$ASSUME_YES" -eq 0 ]; then
    printf "[author] proceed with %s? [y/N] " "$SLUG"
    read -r ans; case "$ans" in y|Y) ;; *) echo "[author] aborted."; exit 0;; esac
  fi

  start_ts="$(date -Is)"
  MODELFLAG=""; [ -n "$MODEL" ] && MODELFLAG="--model $MODEL"
  EFFORTFLAG=""; [ -n "$EFFORT" ] && EFFORTFLAG="--effort $EFFORT"
  echo "[author] launching claude (model=${MODEL:-<env>} effort=${EFFORT:-<def>} timeout=${RUN_TIMEOUT}s) ..."
  printf '%s' "$prompt" | timeout "$RUN_TIMEOUT" claude -p \
      $MODELFLAG $EFFORTFLAG \
      --dangerously-skip-permissions \
      --output-format stream-json --verbose >"$log" 2>&1
  rc=$?

  if make -C "$REPO" verify >"$LOGS/$run.verify.log" 2>&1; then verify=green; else verify=red; fi

  gate="$(REPO="$REPO" LOG="$log" SUMM="$summ" RUN="$run" SLUG="$SLUG" RC="$rc" \
          START="$start_ts" VERIFY="$verify" "$PY" "$CAMP/author-gate.py")"

  echo "[author] $run gate=$gate verify=$verify rc=$rc  (summary: $summ)"
  case "$gate" in
    ok) processed=$(( processed + 1 ));;
    usage-limit) echo "[author] >>> USAGE LIMIT — stopping. Re-run to resume."; exit 0;;
    *) echo "[author] >>> gate=$gate — stopping for review. See $summ (and $log)."; exit 0;;
  esac
  sleep 2
done

echo "[author] finished: $processed package(s) authored this invocation."
