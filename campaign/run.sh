#!/usr/bin/env bash
# Campaign driver — run /author-subagent over the PDF queue, one fresh headless
# Claude session per PDF (smallest-first). Deterministic orchestration only; the
# LLM does the skill test / review / change / commit. See campaign/README.md.
#
# Usage: campaign/run.sh [-n N | --all] [--prompt-file F] [--collection DIR]
#                        [--model M] [--timeout SECS] [--dry-run] [--yes]
#                        [--pdf ABS_PATH]
#
# --pdf ABS_PATH: skip the queue and author this one specific PDF (a create-new /
#   targeted test, vs the default smallest-pending queue selection). Runs exactly once.
set -uo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CAMP="$REPO/campaign"
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
    sha="$(sha256sum "$pdf_abs" 2>/dev/null | cut -d' ' -f1)"
  else
    line="$(next_pending)"
    [ -z "$line" ] && { echo "[campaign] no pending PDFs left — campaign complete."; break; }
    IFS=$'\t' read -r idx size sha relpath <<<"$line"
    relpath="${relpath%$'\r'}"   # defensive: strip any stray CR from the queue
    pdf_abs="$COLLECTION/$relpath"
  fi
  run="$(printf '%03d' "$(( $(ls "$LOGS"/*.summary.md 2>/dev/null | wc -l) + 1 ))")"
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

  if [ "$DRYRUN" -eq 1 ]; then
    echo "[campaign] DRY-RUN — command that would run:"
    echo "    printf '%s' \"\$prompt\" | timeout $RUN_TIMEOUT claude -p \\"
    echo "        --model $MODEL --add-dir \"$COLLECTION\" --dangerously-skip-permissions \\"
    echo "        --output-format stream-json --verbose"
    echo "[campaign] log -> $log"
    echo "[campaign] summary -> $summ"
    echo "------------------ rendered prompt ------------------"
    printf '%s\n' "$prompt"
    echo "---------------- end rendered prompt ----------------"
    break
  fi

  if [ "$ASSUME_YES" -eq 0 ]; then
    printf "[campaign] proceed with Run %s? [y/N] " "$run"
    read -r ans; case "$ans" in y|Y) ;; *) echo "[campaign] aborted."; exit 0;; esac
  fi

  head_before="$(git -C "$REPO" rev-parse HEAD)"
  start_ts="$(date -Is)"
  echo "[campaign] launching claude (timeout ${RUN_TIMEOUT}s) ..."

  printf '%s' "$prompt" | timeout "$RUN_TIMEOUT" claude -p \
      --model "$MODEL" \
      --add-dir "$COLLECTION" \
      --add-dir "$(dirname "$pdf_abs")" \
      --dangerously-skip-permissions \
      --output-format stream-json --verbose >"$log" 2>&1
  rc=$?

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
