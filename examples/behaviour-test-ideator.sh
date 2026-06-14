#!/usr/bin/env bash
# Live ideator for the Step-11 behaviour-test generator (E follow-on). Given a self-contained ideate
# prompt on stdin (principle + cell type), returns ONE realistic user message on stdout — a natural
# golden prompt, a hard-negative out-of-scope request, or an underspecified missing-context message.
#
# gen_behaviour_tests.shell_ideator() pipes the prompt; the generator uses the reply as the test
# prompt, falling back to its deterministic template on any empty/error reply.
#
#   printf '%s' "$IDEATE_PROMPT" | examples/behaviour-test-ideator.sh
set -uo pipefail
CLAUDE="${CLAUDE_BIN:-$HOME/.local/bin/claude}"
prompt="$(cat)"
[ -n "$prompt" ] || { echo "empty prompt" >&2; exit 2; }
timeout "${IDEATE_TIMEOUT:-120}" "$CLAUDE" -p \
  --model "${IDEATE_MODEL:-claude-opus-4-8}" \
  --dangerously-skip-permissions \
  "$prompt" 2>/dev/null
