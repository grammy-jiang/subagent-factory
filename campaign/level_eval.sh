#!/usr/bin/env bash
# Review-quality probe across --select levels (no LLM judge). For each level: assemble at that select
# (deterministic, cached) → p2b_finish (LLM regen adapter) → save the adapter → run it on ONE target
# file → save the review → grounding-check the review (deterministic). Records everything under
# campaign/logs/level-eval/ for side-by-side comparison.
#
# CLOBBERS subagents/<slug> AND the installed adapter .claude/agents/generated/<slug>.md per level
# (the latter is regenerated/removed per level during the probe). This script backs up the installed
# adapter at startup and restores it via an EXIT trap; the caller must still back up subagents/<slug>.
# Usage: bash campaign/level_eval.sh --slug python --sources campaign/python.sources \
#          --doc tools/subagent_factory/cli.py [--levels "0 0.75 0.5 0.25"]
set -euo pipefail
REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PY="$REPO/.venv/bin/python"; [ -x "$PY" ] || PY=python3
SLUG=""; SOURCES=""; DOC=""; LEVELS="0 0.75 0.5 0.25"
while [ $# -gt 0 ]; do
  case "$1" in
    --slug) SLUG="$2"; shift 2;;
    --sources) SOURCES="$2"; shift 2;;
    --doc) DOC="$2"; shift 2;;
    --levels) LEVELS="$2"; shift 2;;
    *) echo "unknown arg: $1" >&2; exit 2;;
  esac
done
[ -n "$SLUG" ] && [ -n "$SOURCES" ] && [ -n "$DOC" ] || { echo "--slug --sources --doc required" >&2; exit 2; }
# DOC may be an absolute path (external file) or repo-relative; resolve to an absolute path.
case "$DOC" in /*) DOCABS="$DOC";; *) DOCABS="$REPO/$DOC";; esac
[ -f "$DOCABS" ] || { echo "doc not found: $DOCABS" >&2; exit 3; }
PKG="$REPO/subagents/$SLUG"; ADP="$REPO/.claude/agents/generated/$SLUG.md"
# Slug-scope the output dir so two slugs don't clobber the same summary.tsv/adapters.
EVAL="$REPO/campaign/logs/level-eval/$SLUG"; mkdir -p "$EVAL"
TSV="$EVAL/summary.tsv"
printf "level\tprinciples\tadapter_bytes\treview_bytes\tgrounding_cov\tn_findings\n" > "$TSV"

# $ADP is the SHARED installed runtime adapter, not eval-scoped: the loop overwrites/removes it per
# level. Back it up once and restore on exit so the probe doesn't leave the real package install in
# a mutated/deleted state (e.g. if the last level fails, the rm -f in the loop would otherwise
# persist). Restore is best-effort (the install may legitimately not exist yet).
ADP_BAK=""
if [ -f "$ADP" ]; then ADP_BAK="$EVAL/.adapter-backup-$SLUG.md"; cp "$ADP" "$ADP_BAK"; fi
restore_adp() { [ -n "$ADP_BAK" ] && [ -f "$ADP_BAK" ] && cp "$ADP_BAK" "$ADP"; }
trap restore_adp EXIT

label() { [ "$1" = "0" ] && echo "all" || echo "$1"; }

for lv in $LEVELS; do
  lb="$(label "$lv")"
  echo "============================================================"
  # Adapter cache: building a level adapter = a deterministic assemble + an EXPENSIVE LLM p2b_finish.
  # Cache the finished adapter per (slug, level) so repeat experiments skip the LLM rebuild. (The
  # finish is non-deterministic prose, so a cached adapter isn't byte-identical to a fresh one, but is
  # the same select level — valid to reuse for level comparisons. Delete the cache file to force a rebuild.)
  CACHED="$REPO/cache/adapters/$SLUG/$lb.md"
  adapter_ok=0   # per-level: did we end up with a valid adapter for THIS level?
  if [ -f "$CACHED" ]; then
    echo "[level-eval] level=$lb — CACHE HIT ($CACHED), skipping assemble+finish"
    cp "$CACHED" "$ADP"
    [ -s "$ADP" ] && adapter_ok=1
  else
    echo "[level-eval] level=$lb — assemble + finish (no cache)"
    # Guard the assemble like every other fallible per-level step: an unguarded heredoc would
    # abort the WHOLE multi-level loop under set -e on one bad level (malformed decisions.json,
    # missing source, embedder failure), losing later levels. On failure, skip finish/snapshot
    # and let this level record a degraded row.
    arc=0
    "$PY" - "$SLUG" "$SOURCES" "$lv" <<'PY' || arc=$?
import json, sys
from pathlib import Path
sys.path.insert(0, ".")
from tools.subagent_factory import map_reduce_build as mr
slug, sources, lv = sys.argv[1], sys.argv[2], float(sys.argv[3])
REPO = Path(".").resolve()
dec = {int(k): v for k, v in json.loads((REPO/"subagents"/slug/".build"/"decisions.json").read_text()).items()}
srcs = [l.strip() for l in open(sources) if l.strip() and not l.startswith("#")]
print("[level-eval] assembled:", mr.assemble(slug, srcs, repo=REPO, embedder=mr._embed_minilm, decisions=dec, select=lv))
PY
    if [ "$arc" -ne 0 ]; then
      echo "[level-eval] level=$lb — assemble rc=$arc; skipping finish + snapshot" >&2
    else
      frc=0
      bash "$REPO/campaign/p2b_finish.sh" --slug "$SLUG" --fg >"$EVAL/finish-$lb.log" 2>&1 || frc=$?
      # Only cache a non-empty adapter from a SUCCESSFUL finish — caching a stale/empty
      # adapter would poison every future CACHE HIT for this (slug, level).
      if [ "$frc" -eq 0 ] && [ -s "$ADP" ]; then
        adapter_ok=1
        mkdir -p "$(dirname "$CACHED")"
        cp "$ADP" "$CACHED"   # populate cache for next time
      else
        echo "[level-eval] level=$lb — finish rc=$frc, adapter $( [ -s "$ADP" ] && echo present || echo empty/missing ); NOT caching" >&2
      fi
    fi
  fi
  # Snapshot THIS level's adapter only if this iteration produced/loaded a valid one. An
  # unconditional cp would (a) abort the whole loop under set -e if no adapter exists, or
  # (b) silently copy a STALE adapter left by a PRIOR level and mislabel it as this level's
  # ($ADP is a fixed path reused across iterations).
  if [ "$adapter_ok" -eq 1 ]; then
    cp "$ADP" "$EVAL/adapter-$lb.md"
  else
    # No valid adapter for THIS level. $ADP is a fixed path reused across iterations, so a prior
    # level's adapter is still sitting there — remove it so the review and the TSV metrics
    # (adapter_bytes/coverage/findings) below don't silently measure the PREVIOUS level's adapter
    # mislabeled as this one. The [ -f "$ADP" ] guards then correctly record "-".
    rm -f "$ADP"
    echo "[level-eval] level=$lb — no valid adapter to snapshot" >&2
  fi

  review="$EVAL/review-$lb.md"
  if [ "$adapter_ok" -eq 1 ]; then
    echo "[level-eval] level=$lb — review $DOC"
    RUN_TIMEOUT=1800 MODEL="${ANTHROPIC_DEFAULT_OPUS_MODEL:-claude-opus-4-8}" \
      bash "$REPO/examples/review-with-subagents.sh" "$DOCABS" --reviewers "$SLUG" --out "$review" \
      >"$EVAL/review-$lb.runlog" 2>&1 || true
  else
    echo "[level-eval] level=$lb — no adapter; skipping review" >&2
  fi

  # Record "-" when a file is MISSING vs a real count (incl. 0) when it is present,
  # so the table never conflates "no file" with "present, zero matches".
  if [ -f "$PKG/principles/principles.yaml" ]; then
    prin=$(grep -c 'statement:' "$PKG/principles/principles.yaml" 2>/dev/null || true); prin="${prin:-0}"
  else prin="-"; fi
  if [ -f "$ADP" ]; then abytes=$(wc -c < "$ADP"); else abytes="-"; fi
  cov="-"; nf="-"; rbytes="-"
  if [ -f "$review" ]; then
    rbytes=$(wc -c < "$review")
    g=$(SUBAGENT_FACTORY_USE_VENV=1 "$PY" -m tools.subagent_factory.cli grounding-check "$SLUG" "$review" "$DOCABS" 2>/dev/null | grep -oE 'coverage [0-9]+%|coverage n/a' | head -1) || g=""
    cov="${g:-?}"
    nf=$(grep -cE '^\s*[0-9]+\.' "$review" 2>/dev/null || true); nf="${nf:-0}"
  fi
  printf "%s\t%s\t%s\t%s\t%s\t%s\n" "$lb" "$prin" "$abytes" "$rbytes" "$cov" "$nf" | tee -a "$TSV"
done
echo "[level-eval] done -> $EVAL (adapters, reviews, $TSV)"
