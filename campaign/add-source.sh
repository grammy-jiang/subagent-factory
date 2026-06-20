#!/usr/bin/env bash
# Incrementally add source(s) to an EXISTING package via the subagent-maintenance flow, in a
# fresh headless Claude session (no Copilot — its 2a cap under-extracts). Preserves existing
# claims/principles, appends only the new source(s). Authoring-only; validates; STOPS.
#
# Usage: campaign/add-source.sh --slug SLUG --sources-file F [--timeout SECS] [--dry-run] [--fg]
set -uo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CAMP="$REPO/campaign"; LOGS="$CAMP/logs"; TMPL="$CAMP/maintenance-prompt.tmpl"
MODEL="${ANTHROPIC_DEFAULT_OPUS_MODEL:-${ANTHROPIC_MODEL:-claude-opus-4-8}}"
EFFORT="${EFFORT:-max}"; RUN_TIMEOUT="${RUN_TIMEOUT:-7200}"
SLUG=""; SRCFILE=""; DRYRUN=0; FG=0
while [ $# -gt 0 ]; do
  case "$1" in
    --slug) SLUG="$2"; shift 2;;
    --sources-file) SRCFILE="$2"; shift 2;;
    --timeout) RUN_TIMEOUT="$2"; shift 2;;
    --dry-run) DRYRUN=1; shift;;
    --fg) FG=1; shift;;
    *) echo "unknown arg: $1" >&2; exit 2;;
  esac
done
[ -n "$SLUG" ] || { echo "--slug required" >&2; exit 2; }
[ -d "$REPO/subagents/$SLUG" ] || { echo "package subagents/$SLUG must already exist" >&2; exit 3; }
SRCFILE="${SRCFILE:-$CAMP/$SLUG-new.sources}"
[ -f "$SRCFILE" ] || { echo "new-sources file not found: $SRCFILE" >&2; exit 3; }
mkdir -p "$LOGS"

SOURCES=""; n=0
while IFS= read -r line; do
  line="${line%$'\r'}"; [ -z "$line" ] && continue; case "$line" in \#*) continue;; esac
  abs="$line"; case "$abs" in /*) ;; *) abs="$REPO/$line";; esac
  [ -r "$abs" ] || { echo "MISSING new source: $abs" >&2; exit 3; }
  SOURCES="${SOURCES:+$SOURCES }$abs"; n=$((n+1))
done < "$SRCFILE"
[ "$n" -gt 0 ] || { echo "no new sources in $SRCFILE" >&2; exit 3; }

declare -A _seen=(); ADDDIRS="--add-dir $REPO"
for s in $SOURCES; do d="$(dirname "$s")"; [ -n "${_seen[$d]:-}" ] && continue; _seen[$d]=1; ADDDIRS="$ADDDIRS --add-dir $d"; done

run="addsrc-$SLUG"; log="$LOGS/$run.log.jsonl"; promptfile="$LOGS/$run.prompt.txt"
REPO="$REPO" SLUG="$SLUG" SOURCES="$SOURCES" python3 "$CAMP/render-prompt.py" "$TMPL" > "$promptfile"
echo "[add-source] slug=$SLUG  new-sources=$n  model=$MODEL  effort=$EFFORT"
for s in $SOURCES; do echo "    + $s"; done

if [ "$DRYRUN" -eq 1 ]; then echo "[add-source] DRY-RUN; prompt: $promptfile"; exit 0; fi

driver="$LOGS/$run.driver.sh"
{
  echo '#!/usr/bin/env bash'
  echo "cd \"$REPO\""
  echo "timeout \"$RUN_TIMEOUT\" claude -p --model \"$MODEL\" --effort \"$EFFORT\" $ADDDIRS \\"
  echo "    --dangerously-skip-permissions --output-format stream-json --verbose \\"
  echo "    < \"$promptfile\" > \"$log\" 2>&1"
  echo "echo \"[add-source] claude rc=\$? — validating $SLUG\""
  echo "VENV_PY=\"$REPO/.venv/bin/python\"; [ -x \"\$VENV_PY\" ] || VENV_PY=python3"
  echo "SUBAGENT_FACTORY_USE_VENV=1 \"\$VENV_PY\" -m tools.subagent_factory.cli validate \"$SLUG\" 2>&1 | tail -6"
} > "$driver"
chmod +x "$driver"

if [ "$FG" -eq 1 ]; then bash "$driver"; else
  nohup bash "$driver" >"$LOGS/$run.driver.log" 2>&1 &
  echo "[add-source] launched bg pid $!  transcript: $log"
fi
