#!/usr/bin/env bash
# Live runner for the behaviour-test replay engine (A1/A2). Runs ONE behaviour-test prompt against
# an adapter and returns the model's response, so behaviour_replay can score it.
#
# The adapter body is fed as an appended system prompt (an approximation of "this subagent" — it
# exercises the adapter's behavioural instructions, which is what A1/A2 measure). The test prompt
# arrives on stdin; the response goes to stdout.
#
#   ADAPTER_TEXT="$(cat adapters/claude-code/<slug>.md)" printf '%s' "$PROMPT" | examples/replay-runner.sh
#
# behaviour_replay.shell_runner() wires this up automatically (sets ADAPTER_TEXT, pipes the prompt).
set -euo pipefail
CLAUDE="${CLAUDE_BIN:-$HOME/.local/bin/claude}"
prompt="$(cat)"
[ -n "$prompt" ] || { echo "empty prompt" >&2; exit 2; }
[ -n "${ADAPTER_TEXT:-}" ] || { echo "ADAPTER_TEXT (adapter/system text) not set" >&2; exit 2; }
timeout "${REPLAY_TIMEOUT:-300}" "$CLAUDE" -p \
  --model "${REPLAY_MODEL:-claude-opus-4-8}" \
  --append-system-prompt "$ADAPTER_TEXT" \
  --dangerously-skip-permissions \
  "$prompt" 2>/dev/null
