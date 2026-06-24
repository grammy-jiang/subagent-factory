#!/usr/bin/env bash
# Review-quality probe across --select levels (no LLM judge). For each level: assemble at that select
# (deterministic, cached) → p2b_finish (LLM regen adapter) → save the adapter → run it on ONE target
# file → save the review → grounding-check the review (deterministic). Records everything under
# campaign/logs/level-eval/ for side-by-side comparison.
#
# CLOBBERS subagents/<slug> per level — caller must back it up + restore after.
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
EVAL="$REPO/campaign/logs/level-eval"; mkdir -p "$EVAL"
TSV="$EVAL/summary.tsv"
printf "level\tprinciples\tadapter_bytes\treview_bytes\tgrounding_cov\tn_findings\n" > "$TSV"

label() { [ "$1" = "0" ] && echo "all" || echo "$1"; }

for lv in $LEVELS; do
  lb="$(label "$lv")"
  echo "============================================================"
  # Adapter cache: building a level adapter = a deterministic assemble + an EXPENSIVE LLM p2b_finish.
  # Cache the finished adapter per (slug, level) so repeat experiments skip the LLM rebuild. (The
  # finish is non-deterministic prose, so a cached adapter isn't byte-identical to a fresh one, but is
  # the same select level — valid to reuse for level comparisons. Delete the cache file to force a rebuild.)
  CACHED="$REPO/cache/adapters/$SLUG/$lb.md"
  if [ -f "$CACHED" ]; then
    echo "[level-eval] level=$lb — CACHE HIT ($CACHED), skipping assemble+finish"
    cp "$CACHED" "$ADP"
  else
    echo "[level-eval] level=$lb — assemble + finish (no cache)"
    "$PY" - "$SLUG" "$SOURCES" "$lv" <<'PY'
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
    bash "$REPO/campaign/p2b_finish.sh" --slug "$SLUG" --fg >"$EVAL/finish-$lb.log" 2>&1 || true
    mkdir -p "$(dirname "$CACHED")"
    cp "$ADP" "$CACHED"   # populate cache for next time
  fi
  cp "$ADP" "$EVAL/adapter-$lb.md"

  echo "[level-eval] level=$lb — review $DOC"
  review="$EVAL/review-$lb.md"
  RUN_TIMEOUT=1800 MODEL="${ANTHROPIC_DEFAULT_OPUS_MODEL:-claude-opus-4-8}" \
    bash "$REPO/examples/review-with-subagents.sh" "$DOCABS" --reviewers "$SLUG" --out "$review" \
    >"$EVAL/review-$lb.runlog" 2>&1 || true

  prin=$(grep -c 'statement:' "$PKG/principles/principles.yaml" 2>/dev/null || echo 0)
  abytes=$(wc -c < "$ADP" 2>/dev/null || echo 0)
  rbytes=$(wc -c < "$review" 2>/dev/null || echo 0)
  cov="-"; nf="-"
  if [ -f "$review" ]; then
    g=$(SUBAGENT_FACTORY_USE_VENV=1 "$PY" -m tools.subagent_factory.cli grounding-check "$SLUG" "$review" "$DOCABS" 2>/dev/null | grep -oE 'coverage [0-9]+%|coverage n/a' | head -1) || g=""
    cov="${g:-?}"
    nf=$(grep -cE '^\s*[0-9]+\.' "$review" 2>/dev/null || echo 0)
  fi
  printf "%s\t%s\t%s\t%s\t%s\t%s\n" "$lb" "$prin" "$abytes" "$rbytes" "$cov" "$nf" | tee -a "$TSV"
done
echo "[level-eval] done -> $EVAL (adapters, reviews, $TSV)"
