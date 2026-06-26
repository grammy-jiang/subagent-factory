#!/usr/bin/env bash
# Sourceable helper that owns the single source of truth for the headless
# `claude -p` invocation contract used by campaign/run.sh and
# campaign/generate-subagent.sh.
#
# It is meant to be SOURCED, not executed:
#     source "$(dirname "${BASH_SOURCE[0]}")/_claude_run.sh"
#
# It exposes one function, build_claude_argv(), which assembles the claude argv
# as a bash ARRAY into a caller-named variable. Because both the --dry-run
# preview and the real run are built from the SAME array, the preview can never
# drift from reality (e.g. omitting an --add-dir flag).
#
# Contract (flag order is stable):
#   claude -p [--model M] [--effort E] (--add-dir D)... \
#       --dangerously-skip-permissions --output-format stream-json --verbose

# Guard: refuse to run directly — this file only makes sense when sourced.
# ${BASH_SOURCE[0]} == ${0} means the script was executed, not sourced.
if [ "${BASH_SOURCE[0]}" = "${0}" ]; then
  echo "_claude_run.sh is a sourceable helper; source it, do not execute it." >&2
  exit 64
fi

# build_claude_argv OUT_ARRAY_NAME MODEL EFFORT [ADD_DIR ...]
#
#   OUT_ARRAY_NAME  name of the caller's array variable to populate (nameref).
#   MODEL           model id/ARN, or "" to omit the --model flag.
#   EFFORT          effort level, or "" to omit the --effort flag.
#   ADD_DIR...      zero or more directories; each becomes its own --add-dir D.
#
# The resulting array begins with `claude -p` and ends with the fixed trailing
# flags. The caller runs it (e.g. `"${argv[@]}"`) or prints it for --dry-run.
build_claude_argv() {
  local -n _out="$1"; shift
  local _model="$1"; shift
  local _effort="$1"; shift

  _out=(claude -p)
  [ -n "$_model" ]  && _out+=(--model "$_model")
  [ -n "$_effort" ] && _out+=(--effort "$_effort")
  local _d
  for _d in "$@"; do
    _out+=(--add-dir "$_d")
  done
  _out+=(--dangerously-skip-permissions --output-format stream-json --verbose)
}

# claude_argv_str ARRAY_ELEMENT...
#
# Render an argv array as a single shell-safe, copy-pasteable string for
# --dry-run previews. Call as: claude_argv_str "${argv[@]}".
claude_argv_str() {
  local out="" tok
  for tok in "$@"; do
    case "$tok" in
      *[!A-Za-z0-9_./:=-]*|'') tok="'${tok//\'/\'\\\'\'}'" ;;  # quote if it has shell-special chars
    esac
    out="${out:+$out }$tok"
  done
  printf '%s' "$out"
}
