#!/usr/bin/env bash
# Generate ONE subagent package from a fixed set of sources, in a fresh headless
# Claude session. Authoring-only: drives /author-subagent end-to-end, validates,
# and STOPS. No factory-hardening, no bug-hunt, no commits (unlike campaign/run.sh).
#
# Usage: campaign/generate-subagent.sh --slug SLUG --topic "TOPIC" \
#            [--sources-file F] [--model M] [--timeout SECS] [--dry-run] [--fg] [--batch]
#
# NOTE: best for SINGLE-source packages. For >1 source this prints the per-book map->reduce
#   pipeline and STOPS (single-session multi-book batch under-extracts — see docs/per-book-
#   authoring-upgrade.md); pass --batch to force the legacy single-session path anyway.
#
#   --slug         kebab-case package slug (e.g. software-architecture)
#   --topic        expert role/topic passed to /author-subagent
#   --sources-file newline-separated list of source paths (default: campaign/<slug>.sources)
#   --model        OPTIONAL. Defaults to this machine's Opus 4.8 (1M-context) Bedrock
#                  inference-profile ARN (from $ANTHROPIC_DEFAULT_OPUS_MODEL, else
#                  $ANTHROPIC_MODEL). This env runs on AWS Bedrock — public ids like
#                  'claude-opus-4-8' are INVALID here and 400 the API. The 1M context
#                  is baked into the ARN profile (no beta header needed).
#   --effort       OPTIONAL. low|medium|high|xhigh|max. Default: max.
#   --timeout      per-run wall-clock cap, seconds (default 7200 — large multi-source run)
#   --dry-run      print the rendered prompt + command, run nothing
#   --fg           run in foreground (default backgrounds via nohup, prints log path)
set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CAMP="$REPO/campaign"; LOGS="$CAMP/logs"
TMPL="$CAMP/generate-prompt.tmpl"
# Default to Opus 4.8 1M (the machine's Bedrock ARN); fall back to ANTHROPIC_MODEL.
MODEL="${MODEL:-${ANTHROPIC_DEFAULT_OPUS_MODEL:-${ANTHROPIC_MODEL:-claude-opus-4-8}}}"
EFFORT="${EFFORT:-max}"
RUN_TIMEOUT="${RUN_TIMEOUT:-7200}"
SLUG=""; TOPIC=""; SRCFILE=""; DRYRUN=0; FG=0; BATCH=0

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
    --batch) BATCH=1; shift;;
    -h|--help) grep -E '^# ' "${BASH_SOURCE[0]}" | sed 's/^# //'; exit 0;;
    *) echo "unknown arg: $1" >&2; exit 2;;
  esac
done

[ -n "$SLUG" ]  || { echo "--slug required" >&2; exit 2; }
[ -n "$TOPIC" ] || { echo "--topic required" >&2; exit 2; }
SRCFILE="${SRCFILE:-$CAMP/$SLUG.sources}"
[ -f "$SRCFILE" ] || { echo "sources file not found: $SRCFILE" >&2; exit 3; }
command -v claude >/dev/null 2>&1 || { echo "claude CLI not found on PATH" >&2; exit 3; }
mkdir -p "$LOGS"

# Resolve + validate every source (follow symlinks); build a space-joined list.
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

# Refinery routing: authoring >1 source in ONE headless /author-subagent session suffers per-run
# extraction dilution — the reason the per-book map->reduce path exists. For multi-source, steer to
# the map->reduce turnkey (richer grounding, no dilution) unless --batch forces the legacy path.
if [ "$n" -gt 1 ] && [ "$BATCH" -eq 0 ]; then
  echo "[generate] $n sources — the single-session batch path under-extracts multi-book packages." >&2
  echo "[generate] Use the per-book map->reduce path instead:" >&2
  echo "    python3 campaign/build_map_reduce.py $SLUG --sources $SRCFILE --resume     # route->chunk->MAP gate" >&2
  echo "    bash    campaign/map_books.sh        --sources $SRCFILE                    # MAP all books (cap-aware, serial)" >&2
  echo "    python3 campaign/build_map_reduce.py $SLUG --sources $SRCFILE --resume     # anchors->reduce-emit->filter gate" >&2
  echo "    bash    campaign/precision_filter.sh --slug $SLUG --fg                     # (or author .build/decisions.json by hand)" >&2
  echo "    python3 campaign/build_map_reduce.py $SLUG --sources $SRCFILE --resume --select 150   # assemble" >&2
  echo "    bash    campaign/p2b_finish.sh       --slug $SLUG --fg                     # finish LLM layer + validate" >&2
  echo "[generate] To force the legacy single-session batch anyway, re-run with --batch." >&2
  exit 4
fi

# add-dir for each distinct source directory so the headless session can read them.
# Build a deduped list of -add-dir flags (dirs may repeat across sources).
declare -A _seen=(); ADDDIRS=""
for s in $SOURCES; do d="$(dirname "$s")"; [ -n "${_seen[$d]:-}" ] && continue; _seen[$d]=1; ADDDIRS="$ADDDIRS --add-dir $d"; done

# Only pass --model when set (defaulted to Opus ARN above; empty only if env is unset).
MODELFLAG=""; [ -n "$MODEL" ] && MODELFLAG="--model $MODEL"
EFFORTFLAG=""; [ -n "$EFFORT" ] && EFFORTFLAG="--effort $EFFORT"

run="gen-$SLUG"
log="$LOGS/$run.log.jsonl"
promptfile="$LOGS/$run.prompt.txt"
REPO="$REPO" SLUG="$SLUG" TOPIC="$TOPIC" SOURCES="$SOURCES" \
    python3 "$CAMP/render-prompt.py" "$TMPL" > "$promptfile"

echo "[generate] slug=$SLUG  sources=$n  effort=${EFFORT:-<default>}  timeout=${RUN_TIMEOUT}s"
echo "[generate] model=${MODEL:-<env default>}"
echo "[generate] sources:"; for s in $SOURCES; do echo "    - $s"; done

if [ "$DRYRUN" -eq 1 ]; then
  echo "[generate] DRY-RUN — command:"
  echo "  claude -p $MODELFLAG $EFFORTFLAG $ADDDIRS --dangerously-skip-permissions --output-format stream-json --verbose < <prompt>"
  echo "[generate] prompt rendered to: $promptfile"
  echo "------------------ rendered prompt ------------------"
  cat "$promptfile"
  echo "---------------- end rendered prompt ----------------"
  exit 0
fi

# Driver: feed prompt from file (robust), run claude, then validate. Reads $promptfile,
# $log, $ADDDIRS, $MODEL, $RUN_TIMEOUT, $SLUG, $REPO from the environment.
driver="$LOGS/$run.driver.sh"
cat > "$driver" <<DRIVER
#!/usr/bin/env bash
cd "$REPO" || exit 1
timeout "$RUN_TIMEOUT" claude -p $MODELFLAG $EFFORTFLAG $ADDDIRS \\
    --dangerously-skip-permissions --output-format stream-json --verbose \\
    < "$promptfile" > "$log" 2>&1
echo "[generate] claude exited rc=\$? — validating $SLUG ..."
VENV_PY="$REPO/.venv/bin/python"; [ -x "\$VENV_PY" ] || VENV_PY=python3
SUBAGENT_FACTORY_USE_VENV=1 "\$VENV_PY" -m tools.subagent_factory.cli validate "$SLUG" 2>&1 | tail -8
DRIVER
chmod +x "$driver"

if [ "$FG" -eq 1 ]; then
  bash "$driver"
else
  nohup bash "$driver" >"$LOGS/$run.driver.log" 2>&1 &
  echo "[generate] launched in background (pid $!)."
  echo "[generate] transcript:  $log"
  echo "[generate] driver log:  $LOGS/$run.driver.log"
  echo "[generate] watch:    tail -f $log"
  echo "[generate] validate: python -m tools.subagent_factory.cli validate $SLUG"
fi
