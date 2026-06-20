#!/usr/bin/env bash
# precision_filter.sh — run the LLM precision filter over emitted candidate clusters in a fresh
# headless Claude session: reads reduce/clusters.json, writes reduce/decisions.json, then stops.
# Usage: campaign/precision_filter.sh [--fg]   (run `precision_filter_p0.py emit` first)
set -uo pipefail
REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CAMP="$REPO/campaign"; LOGS="$CAMP/logs"; TMPL="$CAMP/precision-filter-prompt.tmpl"
CLAUDE_BIN="${CLAUDE_BIN:-$HOME/.local/bin/claude}"
MODEL="${MODEL:-${ANTHROPIC_DEFAULT_OPUS_MODEL:-${ANTHROPIC_MODEL:-claude-opus-4-8}}}"
EFFORT="${EFFORT:-max}"; RUN_TIMEOUT="${RUN_TIMEOUT:-3600}"
WORK="$REPO/cache/p0-build/software-architecture-p0/reduce"
FG=0; [ "${1:-}" = "--fg" ] && FG=1
[ -f "$WORK/clusters.json" ] || { echo "no clusters.json — run precision_filter_p0.py emit first" >&2; exit 3; }
mkdir -p "$LOGS"
run="precision-filter"; log="$LOGS/$run.log.jsonl"; promptfile="$LOGS/$run.prompt.txt"
REPO="$REPO" WORK="$WORK" python3 "$CAMP/render-prompt.py" "$TMPL" > "$promptfile"
echo "[filter] clusters=$(python3 -c "import json;print(len(json.load(open('$WORK/clusters.json'))))")  model=$MODEL effort=$EFFORT"
driver="$LOGS/$run.driver.sh"
{
  echo '#!/usr/bin/env bash'
  echo "cd \"$REPO\""
  echo "timeout \"$RUN_TIMEOUT\" \"$CLAUDE_BIN\" -p --model \"$MODEL\" --effort \"$EFFORT\" --add-dir \"$REPO\" \\"
  echo "    --dangerously-skip-permissions --output-format stream-json --verbose \\"
  echo "    < \"$promptfile\" > \"$log\" 2>&1"
  echo "echo \"[filter] rc=\$?\""
} > "$driver"
chmod +x "$driver"
if [ "$FG" -eq 1 ]; then bash "$driver"; else
  nohup bash "$driver" >"$LOGS/$run.driver.log" 2>&1 &
  echo "[filter] launched bg pid $!  transcript: $log"
fi
