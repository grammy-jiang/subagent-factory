#!/usr/bin/env bash
# precision_filter.sh — headless LLM precision filter over a package's candidate clusters: reads
# subagents/<slug>/.build/clusters.json (emitted by build_map_reduce's reduce-emit step) and writes
# subagents/<slug>/.build/decisions.json (group-keyed confirm/split/conflict), then stops. This is
# the automated alternative to authoring decisions.json by hand at the build_map_reduce filter gate.
# Usage: campaign/precision_filter.sh --slug SLUG [--fg]
set -uo pipefail
REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CAMP="$REPO/campaign"; LOGS="$CAMP/logs"; TMPL="$CAMP/precision-filter-prompt.tmpl"
CLAUDE_BIN="${CLAUDE_BIN:-$HOME/.local/bin/claude}"
MODEL="${MODEL:-${ANTHROPIC_DEFAULT_OPUS_MODEL:-${ANTHROPIC_MODEL:-claude-opus-4-8}}}"
EFFORT="${EFFORT:-max}"; RUN_TIMEOUT="${RUN_TIMEOUT:-3600}"
SLUG=""; FG=0
while [ $# -gt 0 ]; do
  case "$1" in
    --slug) SLUG="$2"; shift 2;;
    --fg) FG=1; shift;;
    -h|--help) grep -E '^# ' "${BASH_SOURCE[0]}" | sed 's/^# //'; exit 0;;
    *) echo "unknown arg: $1" >&2; exit 2;;
  esac
done
[ -n "$SLUG" ] || { echo "--slug required" >&2; exit 2; }
WORK="$REPO/subagents/$SLUG/.build"
[ -f "$WORK/clusters.json" ] || {
  echo "no $WORK/clusters.json — run build_map_reduce.py $SLUG ... to the filter gate first" >&2; exit 3; }
mkdir -p "$LOGS"
run="precision-filter-$SLUG"; log="$LOGS/$run.log.jsonl"; promptfile="$LOGS/$run.prompt.txt"
REPO="$REPO" WORK="$WORK" python3 "$CAMP/render-prompt.py" "$TMPL" > "$promptfile"
echo "[filter] slug=$SLUG  clusters=$(python3 -c "import json;print(len(json.load(open('$WORK/clusters.json'))))")  model=$MODEL effort=$EFFORT"
driver="$LOGS/$run.driver.sh"
{
  echo '#!/usr/bin/env bash'
  echo "cd \"$REPO\""
  echo "timeout \"$RUN_TIMEOUT\" \"$CLAUDE_BIN\" -p --model \"$MODEL\" --effort \"$EFFORT\" --add-dir \"$REPO\" \\"
  echo "    --dangerously-skip-permissions --output-format stream-json --verbose \\"
  echo "    < \"$promptfile\" > \"$log\" 2>&1"
  # Propagate the engine's real exit code so a cap/429 kill is not masked as success.
  echo "rc=\$?; echo \"[filter] $SLUG rc=\$rc\"; exit \$rc"
} > "$driver"
chmod +x "$driver"
if [ "$FG" -eq 1 ]; then bash "$driver"; else
  nohup bash "$driver" >"$LOGS/$run.driver.log" 2>&1 &
  echo "[filter] launched bg pid $!  transcript: $log"
fi
