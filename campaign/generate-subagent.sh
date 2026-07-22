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
# Single source of truth for the `claude -p` argv (shared with run.sh).
source "$CAMP/_claude_run.sh"
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

# Resolve + validate every source (follow symlinks); build an ARRAY (paths may
# contain spaces — a space-joined string would word-split and mis-bind sources).
SOURCES=(); n=0; missing=0
while IFS= read -r line; do
  line="${line%$'\r'}"; [ -z "$line" ] && continue
  case "$line" in \#*) continue;; esac
  # URL sources pass through unresolved: they are prefetched (below) into the cache before the
  # network-denied author session, which then ingests them offline (SUBAGENT_FACTORY_OFFLINE).
  case "$line" in http://*|https://*) SOURCES+=("$line"); n=$((n+1)); continue;; esac
  abs="$line"; case "$abs" in /*) ;; *) abs="$REPO/$line";; esac
  if [ -r "$abs" ]; then SOURCES+=("$abs"); n=$((n+1))
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
# Build a deduped ARRAY of dirs (dirs may repeat across sources; a path may
# contain spaces). build_claude_argv() turns each into its own --add-dir D.
declare -A _seen=(); ADDDIRS=()
for s in "${SOURCES[@]}"; do
  case "$s" in http://*|https://*) continue;; esac  # URLs have no local dir to grant
  d="$(dirname "$s")"; [ -n "${_seen[$d]:-}" ] && continue; _seen[$d]=1; ADDDIRS+=("$d")
done

run="gen-$SLUG"
log="$LOGS/$run.log.jsonl"
promptfile="$LOGS/$run.prompt.txt"
# render-prompt.py consumes SOURCES as a single env string; join the array with
# newlines (one source per line) so multi-source prompts list cleanly.
SOURCES_STR="$(printf '%s\n' "${SOURCES[@]}")"
REPO="$REPO" SLUG="$SLUG" TOPIC="$TOPIC" SOURCES="$SOURCES_STR" \
    python3 "$CAMP/render-prompt.py" "$TMPL" > "$promptfile"

# Build the claude argv ONCE; the --dry-run preview and the real run share it.
build_claude_argv claude_argv "$MODEL" "$EFFORT" "${ADDDIRS[@]}"

echo "[generate] slug=$SLUG  sources=$n  effort=${EFFORT:-<default>}  timeout=${RUN_TIMEOUT}s"
echo "[generate] model=${MODEL:-<env default>}"
echo "[generate] sources:"; for s in "${SOURCES[@]}"; do echo "    - $s"; done

if [ "$DRYRUN" -eq 1 ]; then
  echo "[generate] DRY-RUN — command:"
  echo "  timeout $RUN_TIMEOUT $(claude_argv_str "${claude_argv[@]}") < $promptfile"
  echo "[generate] prompt rendered to: $promptfile"
  echo "------------------ rendered prompt ------------------"
  cat "$promptfile"
  echo "---------------- end rendered prompt ----------------"
  exit 0
fi

# Driver function: feed prompt from file (robust), run claude, then validate.
# Defined as a function (not a generated heredoc script) so the claude_argv
# array and $REPO/$promptfile/$log survive without a second round of re-quoting.
# It propagates claude's rc as its own exit status (was previously only logged).
rcfile="$LOGS/$run.rc"
run_driver() {
  cd "$REPO" || return 1
  # Prefetch URL sources over the network HERE (in the manager, real runs only — never --dry-run),
  # BEFORE the network-denied author session. The session then serves them from the warmed cache, so
  # the trifecta's network leg is removed from the session that reads untrusted content.
  local _urls=() _s
  for _s in "${SOURCES[@]}"; do case "$_s" in http://*|https://*) _urls+=("$_s");; esac; done
  if [ "${#_urls[@]}" -gt 0 ]; then
    echo "[generate] prefetching ${#_urls[@]} URL source(s) into the cache (network-allowed, pre-session)…"
    python3 -m tools.subagent_factory.prefetch_url_sources "${_urls[@]}" \
      || { echo "[generate] prefetch failed — aborting before the offline author session." >&2; return 3; }
  fi
  local rc=0
  # SUBAGENT_FACTORY_OFFLINE=1 scopes to the claude session (and its ingest children): URL sources
  # are served from the prefetched cache, and any un-prefetched URL fails closed rather than fetching
  # — enforcing the network-free author session (pairs with --disallowedTools WebFetch WebSearch).
  SUBAGENT_FACTORY_OFFLINE=1 timeout "$RUN_TIMEOUT" "${claude_argv[@]}" < "$promptfile" > "$log" 2>&1 || rc=$?
  echo "[generate] claude exited rc=$rc — validating $SLUG ..."
  local venv_py="$REPO/.venv/bin/python"; [ -x "$venv_py" ] || venv_py=python3
  # `| tail` would mask the validate rc under pipefail, so capture PIPESTATUS[0].
  SUBAGENT_FACTORY_USE_VENV=1 "$venv_py" -m tools.subagent_factory.cli validate "$SLUG" 2>&1 | tail -8
  local vrc="${PIPESTATUS[0]}"
  # Final rc reflects BOTH stages: a clean claude run with a failing validate must
  # not look like success. claude rc wins if set, else the validate rc.
  [ "$rc" -ne 0 ] || rc="$vrc"
  echo "$rc" > "$rcfile"
  return "$rc"
}

if [ "$FG" -eq 1 ]; then
  run_driver
else
  # Background the driver in a SUBSHELL (not a fresh `bash -c`) so the run_driver
  # function and the claude_argv array are inherited intact — no re-quoting, no
  # generated script. `trap '' HUP` + redirected fds + disown give nohup-like
  # detachment so the driver outlives this shell.
  ( trap '' HUP; run_driver ) >"$LOGS/$run.driver.log" 2>&1 &
  disown
  echo "[generate] launched in background (pid $!)."
  echo "[generate] transcript:  $log"
  echo "[generate] driver log:  $LOGS/$run.driver.log"
  echo "[generate] exit rc ->   $rcfile (written when the driver finishes)"
  echo "[generate] watch:    tail -f $log"
  echo "[generate] validate: python -m tools.subagent_factory.cli validate $SLUG"
fi
