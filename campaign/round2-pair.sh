#!/usr/bin/env bash
# Round 2 dual-engine launcher (staggered, single tracked process — no nested nohup).
#   chain P: python-code-reviewer  — Claude (2a generate + 2b finish-skills)
#   chain D: devops-sre-advisor     — Copilot (2a generate) + Claude (2b finish-skills backstop;
#            Copilot's ~27-req/session cap can't complete 2b)
# Both drive to status: ready. Blocks until both chains finish.
set -uo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CAMP="$REPO/campaign"; LOGS="$CAMP/logs"; mkdir -p "$LOGS"
PAIR="$LOGS/round2-$(date +%Y%m%d-%H%M%S).log"
STAGGER="${PAIR_STAGGER:-75}"

echo "[r2] start $(date)  log: $PAIR"

(
  echo "[chainP] $(date) GENERATE python-code-reviewer (claude)"
  bash "$CAMP/generate-subagent.sh" --fg --slug python-code-reviewer --topic "python code reviewer"
  echo "[chainP] $(date) FINISH-SKILLS python-code-reviewer (claude)"
  bash "$CAMP/finish-skills.sh" --engine claude --slug python-code-reviewer
  echo "[chainP] $(date) DONE"
) >>"$PAIR" 2>&1 &
PP=$!

echo "[r2] staggering chain D by ${STAGGER}s (collision avoidance)"
sleep "$STAGGER"

(
  echo "[chainD] $(date) GENERATE devops-sre-advisor (copilot 2a)"
  bash "$CAMP/generate-subagent-copilot.sh" --fg --slug devops-sre-advisor --topic "devops and SRE advisor"
  echo "[chainD] $(date) FINISH-SKILLS devops-sre-advisor (claude 2b backstop)"
  bash "$CAMP/finish-skills.sh" --engine claude --slug devops-sre-advisor
  echo "[chainD] $(date) DONE"
) >>"$PAIR" 2>&1 &
PD=$!

echo "[r2] python/claude pid=$PP  devops/copilot+claude pid=$PD"
wait "$PP"; rcP=$?
wait "$PD"; rcD=$?
echo "[r2] $(date) BOTH DONE  python rc=$rcP  devops rc=$rcD"
