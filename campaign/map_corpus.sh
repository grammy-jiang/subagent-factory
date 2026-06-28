#!/usr/bin/env bash
# map_corpus.sh — thin wrapper over the cap-resilient cross-engine MAP orchestrator
# (tools/subagent_factory/map_corpus.py). Drains every book for a package, failing over across
# claude / copilot / codex when an engine hits its usage cap, so a single pool's limit never blocks
# generation. Resumes from per-chunk partials; safe to Ctrl-C and re-run.
#
# Usage: campaign/map_corpus.sh --sources campaign/<slug>.sources [--engines claude,copilot,codex]
#                               [--cache cache/book-extracts] [--state campaign/.engine-state.json]
#                               [--timeout SECS]
#        campaign/map_corpus.sh --book A.md --book B.md [...]
#
# Engine binaries are found on PATH; put ~/.local/bin first if that is where claude/copilot/codex live.
set -euo pipefail
REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
export PATH="$HOME/.local/bin:$PATH"
cd "$REPO"
exec python3 -m tools.subagent_factory.map_corpus --repo "$REPO" "$@"
