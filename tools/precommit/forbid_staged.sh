#!/usr/bin/env bash
# Tier-1 pre-commit guard: copyrighted / distillation-only source trees.
#
# pre-commit invokes this with the staged files that matched the hook's
# `files:` regex (sources/{original,markdown,assets}). If this script is
# called at all, a forbidden file is staged — fail and list them.
#
# Rationale: .claude/rules/rights-and-quotation-policy.md — original source
# bytes are distillation-only; only sources/{anchors,metadata,reports} may be
# committed. This automates the manual leak-check run before every package commit.
set -euo pipefail

if [ "$#" -eq 0 ]; then
  exit 0
fi

{
  echo "ERROR: copyrighted / distillation-only source files are staged."
  echo "These must NOT be committed (rights-and-quotation-policy):"
  for f in "$@"; do
    echo "  $f"
  done
  echo
  echo "Only sources/{anchors,metadata,reports} are tracked. Unstage with:"
  echo "  git reset -q HEAD -- 'subagents/*/sources/original' 'subagents/*/sources/markdown' 'subagents/*/sources/assets'"
  echo
  echo "Emergency bypass (discouraged): git commit --no-verify"
} >&2

exit 1
