#!/usr/bin/env bash
# Campaign driver — run /author-subagent over the PDF queue, one fresh headless
# Claude session per PDF (smallest-first). Deterministic orchestration only; the
# LLM does the skill test / review / change / commit. See campaign/README.md.
# NOTE: authors ONE single-source package per PDF (batch path). For a MULTI-book package use the
#   per-book map->reduce path instead: campaign/build_map_reduce.py (+ map_books.sh, p2b_finish.sh)
#   — see docs/per-book-authoring-upgrade.md. Multi-book batch authoring under-extracts (dilution).
#
# Usage: campaign/run.sh [-n N | --all] [--prompt-file F] [--collection DIR]
#                        [--model M] [--timeout SECS] [--dry-run] [--yes]
#                        [--pdf ABS_PATH]
#
# --pdf ABS_PATH: skip the queue and author this one specific PDF (a create-new /
#   targeted test, vs the default smallest-pending queue selection). Runs exactly once.
set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CAMP="$REPO/campaign"
# Single source of truth for the `claude -p` argv (shared with generate-subagent.sh).
source "$CAMP/_claude_run.sh"
LOGS="$CAMP/logs"
QUEUE="$CAMP/pdf-queue.tsv"
TMPL="$CAMP/prompt.tmpl"
COLLECTION="${COLLECTION:-$HOME/projects/awesome-book-collection}"
MODEL="${MODEL:-claude-opus-4-8}"
RUN_TIMEOUT="${RUN_TIMEOUT:-2400}"   # per-round wall-clock cap (seconds)
COUNT=1
DRYRUN=0
ASSUME_YES=0
PDF_OVERRIDE=""

while [ $# -gt 0 ]; do
  case "$1" in
    -n|--count) COUNT="$2"; shift 2;;
    --all) COUNT=100000; shift;;
    --prompt-file) TMPL="$2"; shift 2;;
    --collection) COLLECTION="$2"; shift 2;;
    --model) MODEL="$2"; shift 2;;
    --timeout) RUN_TIMEOUT="$2"; shift 2;;
    --pdf) PDF_OVERRIDE="$2"; shift 2;;
    --dry-run) DRYRUN=1; shift;;
    --yes) ASSUME_YES=1; shift;;
    -h|--help) grep -E '^# ' "${BASH_SOURCE[0]}" | sed 's/^# //'; exit 0;;
    *) echo "unknown arg: $1" >&2; exit 2;;
  esac
done
[ -n "$PDF_OVERRIDE" ] && COUNT=1   # --pdf authors exactly one source

mkdir -p "$LOGS"
command -v claude >/dev/null 2>&1 || { echo "claude CLI not found on PATH" >&2; exit 3; }
[ -d "$COLLECTION" ] || { echo "collection not found: $COLLECTION" >&2; exit 3; }

refresh_queue(){ python3 "$CAMP/build-queue.py" "$COLLECTION" >/dev/null; }
# Queue TSV schema (must match build-queue.py HEADER):
#   $1=idx  $2=size_bytes  $3=status  $4=slug  $5=sha256  $6=relpath
# Emit (idx, size, sha, relpath) for the first pending row. If build-queue.py
# reorders columns, update this projection and the `read` binding below in lockstep.
next_pending(){ awk -F'\t' 'NR>1 && $3=="pending"{print $1"\t"$2"\t"$5"\t"$6; exit}' "$QUEUE"; }
done_slugs(){ ls -d "$REPO"/subagents/*/ 2>/dev/null | xargs -n1 basename 2>/dev/null | paste -sd, -; }

echo "[campaign] repo=$REPO  model=$MODEL  count=$COUNT  collection=$COLLECTION"
# A targeted --pdf run does not select from the queue, so skip the upfront full-collection
# rebuild (sha256 over every PDF). The post-run refresh_queue still normalizes the queue and
# marks this PDF's row done if it belongs to the collection.
[ -n "$PDF_OVERRIDE" ] || refresh_queue

processed=0
while [ "$processed" -lt "$COUNT" ]; do
  if [ -n "$PDF_OVERRIDE" ]; then
    pdf_abs="$PDF_OVERRIDE"
    relpath="$(basename "$PDF_OVERRIDE")"
    size="$(stat -c%s "$pdf_abs" 2>/dev/null || echo 0)"; idx="-"
    # real sha256 (matches build-queue.py) so summarize.py marks this PDF's queue row done if
    # it is part of the collection — keeps the queue consistent after a targeted --pdf run.
    sha="$(sha256sum "$pdf_abs" 2>/dev/null | cut -d' ' -f1)" || sha=""
  else
    line="$(next_pending)"
    [ -z "$line" ] && { echo "[campaign] no pending PDFs left — campaign complete."; break; }
    # Columns here mirror next_pending()'s projection: idx, size_bytes, sha256, relpath.
    IFS=$'\t' read -r idx size sha relpath <<<"$line"
    relpath="${relpath%$'\r'}"   # defensive: strip any stray CR from the queue
    pdf_abs="$COLLECTION/$relpath"
  fi
  # Authoritative, monotonic, collision-safe run id. The old counter
  # (count of *.summary.md + 1) collided whenever a summary was deleted or two
  # invocations raced, silently overwriting $log/$summ. A timestamp plus the
  # PID suffix is unique across two quick successive runs (even within the same
  # second / same wall-clock from parallel processes).
  run="$(date +%Y%m%d-%H%M%S)-$$"
  log="$LOGS/run-$run.log.jsonl"
  summ="$LOGS/run-$run.summary.md"

  echo "============================================================"
  echo "[campaign] Run $run · queue #$idx · $(( size/1024 )) KB"
  echo "[campaign] PDF: $relpath"

  if [ ! -f "$pdf_abs" ]; then
    echo "[campaign] file missing on disk — skipping. Re-run build-queue if the collection moved."
    break
  fi

  prompt="$(REPO="$REPO" TMPL="$TMPL" PDF="$pdf_abs" RUN="$run" \
            DONE_SLUGS="$(done_slugs)" RECENT_COMMITS="$(git -C "$REPO" log --oneline -15)" \
            python3 -c 'import os,sys
t=open(os.environ["TMPL"],encoding="utf-8").read()
for k in ("REPO","PDF","RUN","DONE_SLUGS","RECENT_COMMITS"):
    t=t.replace("{{"+k+"}}",os.environ.get(k,""))
sys.stdout.write(t)')"

  # Build the claude argv ONCE so the --dry-run preview and the real run are
  # the same command. Both --add-dir flags (collection + the PDF's own dir)
  # are part of this single array — the preview cannot drift from reality.
  build_claude_argv claude_argv "$MODEL" "" "$COLLECTION" "$(dirname "$pdf_abs")"

  if [ "$DRYRUN" -eq 1 ]; then
    echo "[campaign] DRY-RUN — command that would run:"
    echo "    printf '%s' \"\$prompt\" | timeout $RUN_TIMEOUT $(claude_argv_str "${claude_argv[@]}")"
    echo "[campaign] log -> $log"
    echo "[campaign] summary -> $summ"
    echo "------------------ rendered prompt ------------------"
    printf '%s\n' "$prompt"
    echo "---------------- end rendered prompt ----------------"
    break
  fi

  if [ "$ASSUME_YES" -eq 0 ]; then
    printf "[campaign] proceed with Run %s? [y/N] " "$run"
    read -r ans || ans=""; case "$ans" in y|Y) ;; *) echo "[campaign] aborted."; exit 0;; esac
  fi

  head_before="$(git -C "$REPO" rev-parse HEAD)"
  start_ts="$(date -Is)"
  echo "[campaign] launching claude (timeout ${RUN_TIMEOUT}s) ..."

  rc=0
  # Same argv array previewed by --dry-run above (both --add-dir flags included).
  # Feed the prompt via here-string (not `printf | claude`): under `pipefail` a
  # SIGPIPE on the writer (claude draining early) would surface as rc 141 and be
  # misattributed to the run. A redirect makes claude's rc the only rc.
  timeout "$RUN_TIMEOUT" "${claude_argv[@]}" <<<"$prompt" >"$log" 2>&1 || rc=$?

  head_after="$(git -C "$REPO" rev-parse HEAD)"
  if make -C "$REPO" verify >"$LOGS/run-$run.verify.log" 2>&1; then verify=green; else verify=red; fi

  gate="$(REPO="$REPO" LOG="$log" SUMM="$summ" RUN="$run" RELPATH="$relpath" SHA="$sha" \
          SIZE="$size" HEAD_BEFORE="$head_before" HEAD_AFTER="$head_after" VERIFY="$verify" \
          RC="$rc" START="$start_ts" python3 "$CAMP/summarize.py")"

  refresh_queue   # normalize queue + regenerate inventory (preserves terminal status)

  echo "[campaign] Run $run gate=$gate verify=$verify rc=$rc  (summary: $summ)"
  case "$gate" in
    ok)
      processed=$(( processed + 1 ))
      ;;
    usage-limit)
      echo "[campaign] >>> USAGE LIMIT reached — stopping. PDF left pending; re-run campaign/run.sh to resume."
      exit 0
      ;;
    *)
      echo "[campaign] >>> gate=$gate — stopping for review. Inspect $summ (and $log for detail)."
      exit 0
      ;;
  esac
  sleep 2
done

echo "[campaign] finished: $processed round(s) ok this invocation."
