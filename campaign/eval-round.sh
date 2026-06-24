#!/usr/bin/env bash
# Output-quality eval for the new subagents (the RELIABLE half: run each reviewer on a real
# in-domain doc, then the deterministic grounding-check). Sequential (one headless review at a
# time — respects the usage cap, avoids nested-spawn concurrency). Inputs are the factory's own
# code/docs (real, in-domain).
set -euo pipefail
REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LOGS="$REPO/campaign/logs"; mkdir -p "$LOGS"
EVAL="$LOGS/eval-round-$(date +%Y%m%d-%H%M%S).log"
VENV_PY="$REPO/.venv/bin/python"; [ -x "$VENV_PY" ] || VENV_PY=python3

# slug : in-repo input doc (real, in-domain)
PAIRS=(
  "python-code-reviewer:tools/subagent_factory/convert_pdf.py"
  "software-design:tools/subagent_factory/export_claude_agent.py"
  "software-architecture:docs/state-of-the-factory.md"
  "devops-sre-advisor:Makefile"
)

echo "[eval] start $(date)  log: $EVAL" | tee -a "$EVAL"
for pair in "${PAIRS[@]}"; do
  slug="${pair%%:*}"; doc="${pair#*:}"
  review="/tmp/eval-$slug.md"
  echo "[eval] === $slug on $doc ===" | tee -a "$EVAL"
  RUN_TIMEOUT=1500 MODEL=claude-opus-4-8 bash "$REPO/examples/review-with-subagents.sh" \
    "$REPO/$doc" --reviewers "$slug" --out "$review" >>"$EVAL" 2>&1
  if [ -f "$review" ]; then
    echo "[eval] grounding-check $slug" | tee -a "$EVAL"
    SUBAGENT_FACTORY_USE_VENV=1 "$VENV_PY" -m tools.subagent_factory.cli grounding-check \
      "$slug" "$review" "$REPO/$doc" >"/tmp/grounding-$slug.txt" 2>&1 || true
    echo "[eval] grounding -> /tmp/grounding-$slug.txt  review -> $review" | tee -a "$EVAL"
  else
    echo "[eval] WARN: no review produced for $slug (timeout/stall?)" | tee -a "$EVAL"
  fi
done
echo "[eval] $(date) ALL DONE" | tee -a "$EVAL"
