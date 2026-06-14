#!/usr/bin/env bash
# Live variant proposer for the Step-12 optimize-adapter loop (D8). Given the current adapter (as an
# appended system prompt) and a proposer prompt listing the failing behaviour-tests, returns
# ===VARIANT===-delimited ADDITIVE guidance blocks to append to the adapter.
#
# The driver (optimize_adapter.shell_proposer) sets ADAPTER_TEXT and pipes the prompt; it parses the
# delimited blocks, appends each to the adapter, and scores/gates the candidates. The model only
# writes the new blocks — it never rewrites the adapter (cheap + safe; v1 is additive-only).
#
#   ADAPTER_TEXT="$(cat adapters/claude-code/<slug>.md)" printf '%s' "$PROMPT" | examples/optimize-proposer.sh
set -uo pipefail
CLAUDE="${CLAUDE_BIN:-$HOME/.local/bin/claude}"
prompt="$(cat)"
[ -n "$prompt" ] || { echo "empty prompt" >&2; exit 2; }
[ -n "${ADAPTER_TEXT:-}" ] || { echo "ADAPTER_TEXT (adapter/system text) not set" >&2; exit 2; }
timeout "${PROPOSE_TIMEOUT:-300}" "$CLAUDE" -p \
  --model "${PROPOSE_MODEL:-claude-opus-4-8}" \
  --append-system-prompt "$ADAPTER_TEXT" \
  --dangerously-skip-permissions \
  "$prompt" 2>/dev/null
