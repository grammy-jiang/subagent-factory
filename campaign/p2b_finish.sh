#!/usr/bin/env bash
# p2b_finish.sh — regenerate the LLM-authored layer (profile/faithfulness/skills/tests/adapter) of an
# already-assembled P0 package so validate_generated_package PASSES, in a fresh headless Claude session.
# Usage: campaign/p2b_finish.sh [--slug software-architecture-p0] [--fg]
set -uo pipefail
REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CAMP="$REPO/campaign"; LOGS="$CAMP/logs"; TMPL="$CAMP/p2b-finish-prompt.tmpl"
CLAUDE_BIN="${CLAUDE_BIN:-$HOME/.local/bin/claude}"
MODEL="${MODEL:-${ANTHROPIC_DEFAULT_OPUS_MODEL:-${ANTHROPIC_MODEL:-claude-opus-4-8}}}"
EFFORT="${EFFORT:-max}"; RUN_TIMEOUT="${RUN_TIMEOUT:-14400}"
SLUG="software-architecture-p0"; FG=0
while [ $# -gt 0 ]; do
  case "$1" in
    --slug) SLUG="$2"; shift 2;;
    --fg) FG=1; shift;;
    *) echo "unknown arg: $1" >&2; exit 2;;
  esac
done
PKG="$REPO/subagents/$SLUG"
[ -d "$PKG" ] || { echo "package not found: $PKG (assemble its distilled layer via build_map_reduce.py first)" >&2; exit 3; }
mkdir -p "$LOGS"
run="p2b-$SLUG"; log="$LOGS/$run.log.jsonl"; promptfile="$LOGS/$run.prompt.txt"
REPO="$REPO" PKG="$PKG" SLUG="$SLUG" python3 "$CAMP/render-prompt.py" "$TMPL" > "$promptfile"
echo "[p2b] slug=$SLUG  pkg=$PKG  model=$MODEL effort=$EFFORT timeout=${RUN_TIMEOUT}s"
driver="$LOGS/$run.driver.sh"
{
  echo '#!/usr/bin/env bash'
  echo "cd \"$REPO\""
  echo "timeout \"$RUN_TIMEOUT\" \"$CLAUDE_BIN\" -p --model \"$MODEL\" --effort \"$EFFORT\" --add-dir \"$REPO\" \\"
  echo "    --dangerously-skip-permissions --output-format stream-json --verbose \\"
  echo "    < \"$promptfile\" > \"$log\" 2>&1"
  echo "rc=\$?; echo \"[p2b] $SLUG claude rc=\$rc\""
  # Deterministic safety net + gate, baked into the driver so it runs for BOTH --fg and background:
  # strip any invalid faithfulness anchors the LLM emitted (e.g. heading anchors absent from the
  # chunk index), then validate BY PATH (passing a slug to validate_generated_package gives a false
  # 'missing required file'). The driver still exits with the engine rc so a cap kill is detectable.
  echo "PY=\"$REPO/.venv/bin/python\"; [ -x \"\$PY\" ] || PY=python3"
  echo "\"\$PY\" -m tools.subagent_factory.cli repair-faithfulness \"$SLUG\" 2>&1 | grep -vE 'Requests|warnings.warn' | tail -1"
  echo "\"\$PY\" -m tools.subagent_factory.validate_generated_package \"$PKG\" 2>&1 | grep -E 'VALIDATION (PASSED|FAILED)' | tail -1"
  echo "exit \$rc"
} > "$driver"
chmod +x "$driver"
if [ "$FG" -eq 1 ]; then bash "$driver"; else
  nohup bash "$driver" >"$LOGS/$run.driver.log" 2>&1 &
  echo "[p2b] launched bg pid $!  transcript: $log"
fi
