#!/usr/bin/env bash
# Dual-engine pair launcher: author TWO subagent packages to status: ready, one per
# billing pool, concurrently. Each chain = generate (2a) -> finish-skills (2b).
#   chain A: software-architecture  on Claude Code (claude -p, Opus 4.8)
#   chain B: software-design        on GitHub Copilot (copilot -p, Opus 4.8)
# Blocks until BOTH chains finish (run this with the Bash tool in background).
set -uo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CAMP="$REPO/campaign"; LOGS="$CAMP/logs"; mkdir -p "$LOGS"
STAMP="$(date +%Y%m%d-%H%M%S)"
PAIR="$LOGS/pair-$STAMP.log"

echo "[pair] start $(date)  combined log: $PAIR"

(
  echo "[pairA] $(date) GENERATE software-architecture (claude / Opus 4.8)"
  bash "$CAMP/generate-subagent.sh" --fg --slug software-architecture --topic "software architecture reviewer"
  echo "[pairA] $(date) FINISH-SKILLS software-architecture (claude)"
  bash "$CAMP/finish-skills.sh" --engine claude --slug software-architecture
  echo "[pairA] $(date) DONE software-architecture"
) >>"$PAIR" 2>&1 &
PA=$!

# Stagger the second engine: launching two headless agent CLIs at the same instant caused a
# transient `claude -p` startup collision (empty log, rc=1). Let chain A pass session init first.
STAGGER="${PAIR_STAGGER:-75}"
echo "[pair] staggering chain B start by ${STAGGER}s (collision avoidance)"
sleep "$STAGGER"

(
  echo "[pairB] $(date) GENERATE software-design (copilot / Opus 4.8)"
  bash "$CAMP/generate-subagent-copilot.sh" --fg --slug software-design --topic "software design reviewer"
  echo "[pairB] $(date) FINISH-SKILLS software-design (copilot)"
  bash "$CAMP/finish-skills.sh" --engine copilot --slug software-design
  echo "[pairB] $(date) DONE software-design"
) >>"$PAIR" 2>&1 &
PB=$!

echo "[pair] architecture/claude pid=$PA   design/copilot pid=$PB"
echo "[pair] tail -f $PAIR"
wait "$PA"; rcA=$?
wait "$PB"; rcB=$?
echo "[pair] $(date) BOTH DONE  architecture rc=$rcA  design rc=$rcB"
echo "[pair] verify: python -m tools.subagent_factory.cli validate software-architecture / software-design"
