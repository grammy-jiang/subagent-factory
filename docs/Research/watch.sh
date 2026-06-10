#!/usr/bin/env bash
# Poll the 3 research folders. Exit on: all SUMMARY.md present | spend-limit in any
# run.log | global artifact staleness. Runs under bash (array word-split is correct).
set -u
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TOPICS=("$@")
[ "${#TOPICS[@]}" -eq 0 ] && TOPICS=(prompt-injection-defense argument-mining-claim-extraction factual-consistency-faithfulness)
echo "watch start $(date +%T)  root=$ROOT"
for i in $(seq 1 120); do
  done=0; capped=""
  for t in "${TOPICS[@]}"; do
    [ -f "$ROOT/$t/SUMMARY.md" ] && done=$((done+1))
    grep -qi "spend limit" "$ROOT/$t/run.log" 2>/dev/null && capped="$capped $t"
  done
  [ "$done" -eq "${#TOPICS[@]}" ] && { echo "ALL_DONE@iter$i $(date +%T)"; break; }
  [ -n "$capped" ] && { echo "SPEND_LIMIT@iter$i:$capped $(date +%T)"; break; }
  newest=$(find "$ROOT" -type f -not -path '*/.llm-sca/*' -not -name run.log -printf '%T@\n' 2>/dev/null | sort -n | tail -1 | cut -d. -f1)
  now=$(date +%s); age=$(( now - ${newest:-now} ))
  [ "$age" -gt 2400 ] && { echo "STALE@iter$i done=$done/${#TOPICS[@]} age=${age}s $(date +%T)"; break; }
  sleep 120
done
echo "==== per-topic ===="
for t in "${TOPICS[@]}"; do
  s=no; [ -f "$ROOT/$t/SUMMARY.md" ] && s=YES
  rep=$(ls "$ROOT/$t"/*-research-report.md 2>/dev/null | wc -l | tr -d ' ')
  cap=$(grep -qi "spend limit" "$ROOT/$t/run.log" 2>/dev/null && echo CAPPED || echo ok)
  echo "$t : SUMMARY=$s report=$rep run=$cap"
  echo "   ws: $(grep -oE '"status"[[:space:]]*:[[:space:]]*"[^"]*"' "$ROOT/$t/workflow_state.json" 2>/dev/null | sort | uniq -c | tr '\n' ' ')"
done
