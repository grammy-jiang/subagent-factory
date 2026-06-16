#!/usr/bin/env bash
# Run Step-7 multi-source synthesis (principle-clusters.json + principle-graph.json)
# on one package, in a fresh headless Claude session. Synthesis-only; no status change.
#
# Usage: campaign/step7-run.sh --slug SLUG [--model M] [--effort E] [--timeout S] [--dry-run] [--fg]
set -uo pipefail
REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CAMP="$REPO/campaign"; LOGS="$CAMP/logs"; TMPL="$CAMP/step7-prompt.tmpl"
MODEL="${MODEL:-${ANTHROPIC_DEFAULT_OPUS_MODEL:-${ANTHROPIC_MODEL:-claude-opus-4-8}}}"
EFFORT="${EFFORT:-max}"; RUN_TIMEOUT="${RUN_TIMEOUT:-3600}"
SLUG=""; DRYRUN=0; FG=0
while [ $# -gt 0 ]; do case "$1" in
  --slug) SLUG="$2"; shift 2;;
  --model) MODEL="$2"; shift 2;;
  --effort) EFFORT="$2"; shift 2;;
  --timeout) RUN_TIMEOUT="$2"; shift 2;;
  --dry-run) DRYRUN=1; shift;;
  --fg) FG=1; shift;;
  *) echo "unknown arg: $1" >&2; exit 2;;
esac; done
[ -n "$SLUG" ] || { echo "--slug required" >&2; exit 2; }
[ -d "$REPO/subagents/$SLUG" ] || { echo "package not found: subagents/$SLUG" >&2; exit 3; }
command -v claude >/dev/null 2>&1 || { echo "claude CLI not found" >&2; exit 3; }
mkdir -p "$LOGS"

MODELFLAG=""; [ -n "$MODEL" ] && MODELFLAG="--model $MODEL"
EFFORTFLAG=""; [ -n "$EFFORT" ] && EFFORTFLAG="--effort $EFFORT"
run="step7-$SLUG"; log="$LOGS/$run.log.jsonl"; promptfile="$LOGS/$run.prompt.txt"
REPO="$REPO" SLUG="$SLUG" python3 "$CAMP/render-prompt.py" "$TMPL" > "$promptfile"

echo "[step7] slug=$SLUG model=${MODEL:-<env>} effort=$EFFORT timeout=${RUN_TIMEOUT}s"
if [ "$DRYRUN" -eq 1 ]; then echo "[step7] DRY-RUN prompt:"; cat "$promptfile"; exit 0; fi

driver="$LOGS/$run.driver.sh"
cat > "$driver" <<DRIVER
#!/usr/bin/env bash
cd "$REPO"
timeout "$RUN_TIMEOUT" claude -p $MODELFLAG $EFFORTFLAG --add-dir "$REPO" \\
    --dangerously-skip-permissions --output-format stream-json --verbose \\
    < "$promptfile" > "$log" 2>&1
echo "[step7] claude exited rc=\$? — validating $SLUG ..."
VENV_PY="$REPO/.venv/bin/python"; [ -x "\$VENV_PY" ] || VENV_PY=python3
SUBAGENT_FACTORY_USE_VENV=1 "\$VENV_PY" -m tools.subagent_factory.cli validate "$SLUG" 2>&1 | grep -iE "synthesis|cluster|graph|PASSED|FAILED" | tail -8
DRIVER
chmod +x "$driver"
if [ "$FG" -eq 1 ]; then bash "$driver"; else
  nohup bash "$driver" >"$LOGS/$run.driver.log" 2>&1 &
  echo "[step7] launched pid $! · transcript: $log"
fi
