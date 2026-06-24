#!/usr/bin/env bash
# Part-B full adapter-size measurement across --select levels. For each level: assemble the distilled
# layer at that select (deterministic, reuses cached MAP + .build/decisions.json) → p2b_finish (LLM:
# regenerate profile/faithfulness/skills/tests/adapter + validate) → record adapter bytes/lines/
# invariants/validate into campaign/logs/adapter-size-sweep.tsv. Serial (one finish at a time).
#
# CLOBBERS subagents/<slug> per level — caller must have backed it up; this restores nothing.
# Usage: bash campaign/adapter_size_sweep.sh --slug python --sources campaign/python.sources \
#          [--levels "0.25 0.5 0.75 0"]
set -euo pipefail
REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PY="$REPO/.venv/bin/python"; [ -x "$PY" ] || PY=python3
SLUG=""; SOURCES=""; LEVELS="0.25 0.5 0.75 0"
while [ $# -gt 0 ]; do
  case "$1" in
    --slug) SLUG="$2"; shift 2;;
    --sources) SOURCES="$2"; shift 2;;
    --levels) LEVELS="$2"; shift 2;;
    *) echo "unknown arg: $1" >&2; exit 2;;
  esac
done
[ -n "$SLUG" ] && [ -n "$SOURCES" ] || { echo "--slug and --sources required" >&2; exit 2; }
PKG="$REPO/subagents/$SLUG"; ADP="$REPO/.claude/agents/generated/$SLUG.md"
OUT="$REPO/campaign/logs/adapter-size-sweep.tsv"
printf "level\tprinciples\tadapter_lines\tadapter_bytes\tinvariants\tvalidate\n" > "$OUT"

for lv in $LEVELS; do
  echo "============================================================"
  echo "[size-sweep] level=$lv — assemble"
  # Assemble at this select (deterministic; reuses cached modules + decisions.json).
  "$PY" - "$SLUG" "$SOURCES" "$lv" <<'PY'
import json, sys
from pathlib import Path
sys.path.insert(0, ".")
from tools.subagent_factory import map_reduce_build as mr
slug, sources, lv = sys.argv[1], sys.argv[2], float(sys.argv[3])
REPO = Path(".").resolve()
dec_path = REPO / "subagents" / slug / ".build" / "decisions.json"
dec = {int(k): v for k, v in json.loads(dec_path.read_text()).items()}
srcs = [l.strip() for l in open(sources) if l.strip() and not l.startswith("#")]
summary = mr.assemble(slug, srcs, repo=REPO, embedder=mr._embed_minilm,
                      decisions=dec, select=lv)
print("[size-sweep] assembled:", summary)
PY
  echo "[size-sweep] level=$lv — p2b_finish (LLM) ..."
  bash "$REPO/campaign/p2b_finish.sh" --slug "$SLUG" --fg >"$REPO/campaign/logs/size-sweep-$lv.log" 2>&1 || true

  prin=$(grep -c 'statement:' "$PKG/principles/principles.yaml" 2>/dev/null || echo 0)
  lines=$(wc -l < "$ADP" 2>/dev/null || echo 0)
  bytes=$(wc -c < "$ADP" 2>/dev/null || echo 0)
  inv=$(grep -c '^- ' "$ADP" 2>/dev/null || echo 0)
  val=$(SUBAGENT_FACTORY_USE_VENV=1 "$PY" -m tools.subagent_factory.validate_generated_package "$PKG" 2>&1 | grep -oE 'VALIDATION (PASSED|FAILED)' | tail -1) || val=""
  printf "%s\t%s\t%s\t%s\t%s\t%s\n" "$lv" "$prin" "$lines" "$bytes" "$inv" "${val:-?}" | tee -a "$OUT"
done
echo "[size-sweep] done -> $OUT"
