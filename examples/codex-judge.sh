#!/usr/bin/env bash
# Independent (non-Claude) judge for the Phase-10 A/B ensemble (B3).
# Reads the judge prompt on stdin, returns codex's verdict on stdout. Using a different model
# family (gpt-5.5) is what makes the ensemble's self-preference audit meaningful — a Claude judge
# scoring Claude-built subagents cannot. Read-only sandbox, no approval: the prompt is
# self-contained (both reviews inline) and only needs a one-line JSON verdict, no tools.
#
# Usage: printf '%s' "$PROMPT" | examples/codex-judge.sh
set -uo pipefail
CODEX="${CODEX_BIN:-$HOME/.local/bin/codex}"
prompt="$(cat)"
[ -n "$prompt" ] || { echo "empty prompt" >&2; exit 2; }
timeout "${JUDGE_TIMEOUT:-300}" "$CODEX" exec --model "${CODEX_MODEL:-gpt-5.5}" --sandbox read-only "$prompt" 2>/dev/null
