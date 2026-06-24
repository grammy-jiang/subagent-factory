#!/usr/bin/env bash
# Round-4 batch: run level_eval (cached adapters → no LLM finish) over 3 external files, 0.25x vs all,
# each into its own results dir; restore shipped python after. Run with `bash` (zsh mangles PATH in
# the Claude Bash tool's compound blocks).
set -euo pipefail
REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO" || exit 1
BK="$(ls -d subagents/.backups/python-shipped-* 2>/dev/null | tail -1)" || BK=""
[ -n "$BK" ] || { echo "no python-shipped backup found; refusing to restore (would corrupt subagents/python)" >&2; exit 3; }
ADP="$(ls subagents/.backups/python-adapter-shipped-*.md 2>/dev/null | tail -1)" || ADP=""
[ -n "$ADP" ] || { echo "no python-adapter backup found; refusing to restore" >&2; exit 3; }

FILES=(
  "uitypes:/scratch/workspaces/mts-explorer/src/mts_explorer/hoops/uitypes.py"
  "simm:/scratch/workspaces/mts-explorer/src/mts_explorer/hoops/SimmCommands.py"
  "dealchanges:/scratch/workspaces/mts-explorer/src/mts_explorer/hoops/deal_changes.py"
)
for entry in "${FILES[@]}"; do
  tag="${entry%%:*}"; path="${entry#*:}"
  echo "######## ROUND4 file=$tag ########"
  rm -rf campaign/logs/level-eval
  bash campaign/level_eval.sh --slug python --sources campaign/python.sources --doc "$path" --levels "0.25 0"
  mv campaign/logs/level-eval "campaign/logs/level-eval-$tag"
done
rm -rf subagents/python && cp -a "$BK" subagents/python && cp "$ADP" .claude/agents/generated/python.md
echo "ROUND4_ALL_DONE; shipped restored: $(grep -c statement: subagents/python/principles/principles.yaml) principles"
