#!/usr/bin/env bash
# Iterative "dogfood" review of the FACTORY ITSELF by its own generated reviewer subagents — each
# round in a FRESH, INDEPENDENT headless `claude -p` instance (no context shared with the fixer
# session, so the review is unbiased by the implementation chat).
#
# Reuses campaign/render-prompt.py + the headless-instance pattern of
# examples/review-with-subagents.sh; ADDS: iterative rounds, STRUCTURED findings (JSON), and
# drop-converged state (a reviewer that reports nothing new drops out of later rounds).
#
# One round per invocation:
#   1. render the review prompt for the ACTIVE reviewers (campaign/dogfood/active-reviewers.txt),
#   2. run it in a fresh headless instance (root-safe: an --allowedTools allowlist, NOT
#      --dangerously-skip-permissions, which the CLI refuses under root),
#   3. the instance writes structured findings to campaign/dogfood/round-<N>/findings.json,
#   4. digest: print the NEW findings, record them, and DROP reviewers that found nothing new.
# Then YOU (the fixer session) read the digest, fix + commit, and run the next round.
#
# Usage:
#   campaign/dogfood-review.sh [--round N] [--reviewers a,b,c] [--model M] [--timeout S] [--dry-run]
# Reset the loop:  rm -rf campaign/dogfood/
set -euo pipefail
REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO" || { echo "dogfood-review: cannot cd to REPO=$REPO" >&2; exit 3; }

MODEL="${MODEL:-claude-opus-4-8}"
TIMEOUT="${RUN_TIMEOUT:-3000}"
ROUND=""; REVIEWERS_ARG=""; DRYRUN=0
while [ $# -gt 0 ]; do
  case "$1" in
    --round) ROUND="$2"; shift 2;;
    --reviewers) REVIEWERS_ARG="$2"; shift 2;;
    --model) MODEL="$2"; shift 2;;
    --timeout) TIMEOUT="$2"; shift 2;;
    --dry-run) DRYRUN=1; shift;;
    -h|--help) grep -E '^# ' "${BASH_SOURCE[0]}" | sed 's/^# //'; exit 0;;
    *) echo "unknown arg: $1" >&2; exit 2;;
  esac
done
command -v claude >/dev/null 2>&1 || { echo "claude CLI not found on PATH" >&2; exit 3; }

DOG="$REPO/campaign/dogfood"; STATE="$DOG/active-reviewers.txt"; SEEN="$DOG/seen.tsv"
mkdir -p "$DOG"

# Reviewer -> the factory subsystem it critiques. Seeds the default active set + prompt domain hints.
declare -A HINT=(
  [python-reviewer]="tools/subagent_factory/*.py — idiomatic Python, correctness, error handling, edge cases"
  [python-testing-advisor]="tests/ — coverage gaps, test design, missing/weak assertions, brittle mocks"
  [software-design]="tools/subagent_factory/ — module/function structure, complexity, coupling, duplication"
  [software-architecture]="the factory pipeline as a whole — stage boundaries, layering, data flow, source-of-truth"
  [bash-shell-scripting-advisor]="campaign/*.sh — quoting, word-splitting, error handling, portability, set -euo pitfalls"
  [harness-engineering-advisor]="campaign/ orchestration + campaign/_claude_run.sh — headless-session contract, gates, verify-before-commit, resume"
  [ai-agent-engineering-reviewer]=".claude/agents/ + the authoring/review agent design — delegation, tool grants, instruction/data separation"
  [documentation-as-code-advisor]="docs/ + CLAUDE.md + .claude/rules/ — accuracy vs code, structure, drift, discoverability"
  [application-security-reviewer]="tools/subagent_factory/*scan*.py + export/validate/redact — injection, quote, adapter-policy, fail-closed posture"
  [mcp-security-advisor]="the IPI / lethal-trifecta posture — _claude_run.sh profiles, prefetch/offline ingest, source-safety triage"
)
DEFAULT_REVIEWERS=(python-reviewer python-testing-advisor software-design software-architecture \
  bash-shell-scripting-advisor harness-engineering-advisor ai-agent-engineering-reviewer \
  documentation-as-code-advisor application-security-reviewer mcp-security-advisor)

# Active reviewers this round: --reviewers  >  state file  >  default seed (seeded on first run).
if [ -n "$REVIEWERS_ARG" ]; then
  IFS=',' read -ra ACTIVE <<< "$REVIEWERS_ARG"
elif [ -s "$STATE" ]; then
  mapfile -t ACTIVE < <(grep -vE '^[[:space:]]*(#|$)' "$STATE")
else
  ACTIVE=("${DEFAULT_REVIEWERS[@]}"); printf '%s\n' "${ACTIVE[@]}" > "$STATE"
fi
[ "${#ACTIVE[@]}" -gt 0 ] || { echo "[dogfood] no active reviewers left — the iteration has converged."; exit 0; }

# Round number: explicit, else max existing round + 1.
if [ -z "$ROUND" ]; then
  last=0
  for d in "$DOG"/round-*; do
    [ -d "$d" ] || continue; nn="${d##*/round-}"
    case "$nn" in ''|*[!0-9]*) ;; *) [ "$nn" -gt "$last" ] && last="$nn";; esac
  done
  ROUND=$((last + 1))
  # Claim the round dir atomically: mkdir (no -p) fails if a concurrent run already took it → bump
  # and retry, so two invocations can never clobber the same round's findings.
  while ! mkdir "$DOG/round-$ROUND" 2>/dev/null; do ROUND=$((ROUND + 1)); done
  RDIR="$DOG/round-$ROUND"
else
  RDIR="$DOG/round-$ROUND"; mkdir -p "$RDIR"  # explicit --round N: idempotent (allows re-run)
fi
FINDINGS="$RDIR/findings.json"

# Prompt inputs: per-reviewer domain block + the prior-titles the instance must not repeat.
REVIEWER_BLOCK=""
for r in "${ACTIVE[@]}"; do REVIEWER_BLOCK+="  - ${r}: ${HINT[$r]:-(general review of the factory)}"$'\n'; done
if [ -s "$SEEN" ]; then PRIOR_TITLES="$(awk -F'\t' 'NF>=3{print "  - "$2": "$3}' "$SEEN")"; else PRIOR_TITLES="  (none yet — first round)"; fi

promptfile="$RDIR/prompt.txt"
ROUND="$ROUND" REVIEWER_BLOCK="$REVIEWER_BLOCK" FINDINGS="$FINDINGS" PRIOR_TITLES="$PRIOR_TITLES" \
  python3 "$REPO/campaign/render-prompt.py" "$REPO/campaign/dogfood-review-prompt.tmpl" > "$promptfile"

echo "[dogfood] round=$ROUND  reviewers=${#ACTIVE[@]} (${ACTIVE[*]})"
echo "[dogfood] model=$MODEL  timeout=${TIMEOUT}s"
echo "[dogfood] findings -> $FINDINGS"

if [ "$DRYRUN" -eq 1 ]; then
  echo "------------------ rendered prompt ------------------"; cat "$promptfile"; exit 0
fi

# Read-only enforcement precondition: a CLEAN tree, so anything the review instance touches (it must
# not — it only Writes the findings JSON) is unambiguously a stray to revert. campaign/dogfood/ is
# gitignored, so round outputs never count as "dirty".
dirty="$(git status --porcelain)"
[ -z "$dirty" ] || { echo "[dogfood] working tree not clean — commit or stash first:" >&2; printf '%s\n' "$dirty" >&2; exit 3; }

log="$RDIR/session.log.jsonl"
echo "[dogfood] launching fresh headless instance…"
rc=0
# Root-safe: an explicit allowlist (Read/Grep/Glob to review, Task to spawn reviewer subagents, Write
# for the findings JSON) runs non-interactively WITHOUT --dangerously-skip-permissions, which the CLI
# refuses under root. Verified: subagent spawns complete with no permission denials.
timeout "$TIMEOUT" claude -p \
  --model "$MODEL" \
  --add-dir "$REPO" \
  --allowedTools "Read Grep Glob Task Write" \
  --output-format stream-json --verbose \
  < "$promptfile" > "$log" 2>&1 || rc=$?
echo "[dogfood] instance rc=$rc  log=$log"

# Safety net: the review instance is read-only-except-findings. Revert any stray change it made to
# the tracked tree and remove stray new (non-ignored) files. campaign/dogfood/ is gitignored → kept.
strays="$(git status --porcelain || true)"
if [ -n "$strays" ]; then
  echo "[dogfood] review instance modified files outside the findings dir — reverting (must be read-only):" >&2
  printf '%s\n' "$strays" >&2
  git checkout -- . 2>/dev/null || true
  git clean -fdq 2>/dev/null || true
fi

[ -f "$FINDINGS" ] || { echo "[dogfood] NO findings.json produced — inspect $log (rc=$rc)."; exit 4; }

# Digest: NEW vs prior, print the fix-list, record seen titles, drop converged reviewers from STATE.
python3 "$REPO/campaign/dogfood_digest.py" \
  --round "$ROUND" --findings "$FINDINGS" --seen "$SEEN" --state "$STATE" \
  --active "$(IFS=,; echo "${ACTIVE[*]}")"

echo "[dogfood] round $ROUND done. Fix the findings above, commit, then re-run for the next round."
