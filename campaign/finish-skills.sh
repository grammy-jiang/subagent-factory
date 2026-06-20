#!/usr/bin/env bash
# Phase 2b: author all stub skill/reference bodies of an EXISTING draft package and
# promote it to status: ready, on a chosen engine. Run after generate (2a) succeeds.
#
# Usage: campaign/finish-skills.sh --engine claude|copilot --slug SLUG [--timeout SECS] [--dry-run]
set -uo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CAMP="$REPO/campaign"; LOGS="$CAMP/logs"
TMPL="$CAMP/finish-skills-prompt.tmpl"
ENGINE=""; SLUG=""; RUN_TIMEOUT="${RUN_TIMEOUT:-5400}"; DRYRUN=0

while [ $# -gt 0 ]; do
  case "$1" in
    --engine) ENGINE="$2"; shift 2;;
    --slug) SLUG="$2"; shift 2;;
    --timeout) RUN_TIMEOUT="$2"; shift 2;;
    --dry-run) DRYRUN=1; shift;;
    *) echo "unknown arg: $1" >&2; exit 2;;
  esac
done
[ -n "$ENGINE" ] || { echo "--engine claude|copilot required" >&2; exit 2; }
[ -n "$SLUG" ]   || { echo "--slug required" >&2; exit 2; }
[ -d "$REPO/subagents/$SLUG" ] || { echo "package subagents/$SLUG not found — run generate (2a) first" >&2; exit 3; }
mkdir -p "$LOGS"

# Phase gate: 2b (skill authoring -> ready) only runs on a VALID 2a draft. If generate (2a)
# failed or left an invalid/incomplete draft, do NOT author skills on top of it — abort loudly
# so the broken 2a surfaces instead of being papered over.
_GATE_PY="$REPO/.venv/bin/python"; [ -x "$_GATE_PY" ] || _GATE_PY=python3
if ! SUBAGENT_FACTORY_USE_VENV=1 "$_GATE_PY" -m tools.subagent_factory.cli validate "$SLUG" >/dev/null 2>&1; then
  echo "[finish:$ENGINE] ABORT — $SLUG draft fails validate (2a incomplete/failed); not running 2b." >&2
  exit 4
fi

run="finish-$SLUG.$ENGINE"
log="$LOGS/$run.log"
promptfile="$LOGS/$run.prompt.txt"
REPO="$REPO" SLUG="$SLUG" python3 "$CAMP/render-prompt.py" "$TMPL" > "$promptfile"

case "$ENGINE" in
  claude)
    MODEL="${ANTHROPIC_DEFAULT_OPUS_MODEL:-${ANTHROPIC_MODEL:-claude-opus-4-8}}"
    CMD="timeout \"$RUN_TIMEOUT\" claude -p --model \"$MODEL\" --effort max --add-dir \"$REPO\" --dangerously-skip-permissions --output-format stream-json --verbose < \"$promptfile\" > \"$log\" 2>&1" ;;
  copilot)
    MODEL="${MODEL:-claude-opus-4.8}"
    CMD="timeout \"$RUN_TIMEOUT\" copilot -p \"\$(cat '$promptfile')\" --model \"$MODEL\" --effort max --allow-all-tools --allow-all-paths -C \"$REPO\" --add-dir \"$REPO\" --context long_context > \"$log\" 2>&1" ;;
  *) echo "unknown engine: $ENGINE (claude|copilot)" >&2; exit 2;;
esac

echo "[finish:$ENGINE] slug=$SLUG  model=$MODEL  timeout=${RUN_TIMEOUT}s"
if [ "$DRYRUN" -eq 1 ]; then echo "[finish:$ENGINE] CMD: $CMD"; echo "[finish:$ENGINE] prompt: $promptfile"; exit 0; fi

cd "$REPO"
eval "$CMD"; rc=$?
echo "[finish:$ENGINE] $ENGINE exited rc=$rc — validating $SLUG ..."
VENV_PY="$REPO/.venv/bin/python"; [ -x "$VENV_PY" ] || VENV_PY=python3
SUBAGENT_FACTORY_USE_VENV=1 "$VENV_PY" -m tools.subagent_factory.cli validate "$SLUG" 2>&1 | tail -10
