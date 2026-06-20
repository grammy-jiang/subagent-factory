#!/usr/bin/env bash
# Generate ONE subagent package via GitHub Copilot CLI (Opus 4.8, separate billing
# pool from Claude Code). Mirrors generate-subagent.sh but drives `copilot -p` LOCALLY
# (no --remote: the cloud env can't see local staging/corpus). Authoring-only:
# drives /author-subagent end-to-end, validates, STOPS. No commits.
#
# Usage: campaign/generate-subagent-copilot.sh --slug SLUG --topic "TOPIC" \
#            [--sources-file F] [--model M] [--effort E] [--timeout SECS] [--dry-run] [--fg]
set -uo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CAMP="$REPO/campaign"; LOGS="$CAMP/logs"
TMPL="$CAMP/generate-prompt.tmpl"
MODEL="${MODEL:-claude-opus-4.8}"
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

SOURCES=""; n=0; missing=0
while IFS= read -r line; do
  line="${line%$'\r'}"; [ -z "$line" ] && continue
  case "$line" in \#*) continue;; esac
  abs="$line"; case "$abs" in /*) ;; *) abs="$REPO/$line";; esac
  if [ -r "$abs" ]; then SOURCES="${SOURCES:+$SOURCES }$abs"; n=$((n+1))
  else echo "  MISSING source: $abs" >&2; missing=$((missing+1)); fi
done < "$SRCFILE"
[ "$missing" -eq 0 ] || { echo "$missing source(s) unreadable — aborting." >&2; exit 3; }
[ "$n" -gt 0 ] || { echo "no sources listed in $SRCFILE" >&2; exit 3; }

# --add-dir for each distinct source directory (deduped) so Copilot may read them.
declare -A _seen=(); ADDDIRS="--add-dir $REPO"
for s in $SOURCES; do d="$(dirname "$s")"; [ -n "${_seen[$d]:-}" ] && continue; _seen[$d]=1; ADDDIRS="$ADDDIRS --add-dir $d"; done

run="gen-$SLUG.copilot"
log="$LOGS/$run.log"
promptfile="$LOGS/$run.prompt.txt"
REPO="$REPO" SLUG="$SLUG" TOPIC="$TOPIC" SOURCES="$SOURCES" \
    python3 "$CAMP/render-prompt.py" "$TMPL" > "$promptfile"

echo "[copilot-gen] slug=$SLUG  sources=$n  model=$MODEL  effort=$EFFORT  timeout=${RUN_TIMEOUT}s"
echo "[copilot-gen] sources:"; for s in $SOURCES; do echo "    - $s"; done

if [ "$DRYRUN" -eq 1 ]; then
  echo "[copilot-gen] DRY-RUN — command:"
  echo "  copilot -p <prompt> --model $MODEL --effort $EFFORT --allow-all-tools --allow-all-paths -C $REPO $ADDDIRS --context long_context"
  echo "[copilot-gen] prompt rendered to: $promptfile"; exit 0
fi

driver="$LOGS/$run.driver.sh"
{
  echo '#!/usr/bin/env bash'
  echo "cd \"$REPO\""
  echo "timeout \"$RUN_TIMEOUT\" copilot -p \"\$(cat '$promptfile')\" \\"
  echo "    --model \"$MODEL\" --effort \"$EFFORT\" \\"
  echo "    --allow-all-tools --allow-all-paths -C \"$REPO\" $ADDDIRS --context long_context \\"
  echo "    > \"$log\" 2>&1"
  echo 'rc=$?'
  echo "echo \"[copilot-gen] copilot exited rc=\$rc — validating $SLUG ...\""
  echo "VENV_PY=\"$REPO/.venv/bin/python\"; [ -x \"\$VENV_PY\" ] || VENV_PY=python3"
  echo "SUBAGENT_FACTORY_USE_VENV=1 \"\$VENV_PY\" -m tools.subagent_factory.cli validate \"$SLUG\" 2>&1 | tail -8"
} > "$driver"
chmod +x "$driver"

if [ "$FG" -eq 1 ]; then
  bash "$driver"
else
  nohup bash "$driver" >"$LOGS/$run.driver.log" 2>&1 &
  echo "[copilot-gen] launched in background (pid $!)."
  echo "[copilot-gen] transcript:  $log"
  echo "[copilot-gen] watch:    tail -f $log"
fi
