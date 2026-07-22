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
# Least privilege by session role via the CLAUDE_PERM_PROFILE env var (default "author"):
#   author  full authority to create/edit package files, but NO agent-initiated network. Author/fix
#           sessions read UNTRUSTED source content and hold powerful tools — the "lethal trifecta"
#           closes only if the third leg (network egress) is removed. URL sources are fetched by a
#           deterministic PREFETCH step BEFORE the session (fetch_url.py, SSRF-guarded), so the author
#           session never needs WebFetch/WebSearch; denying them (bare-tool deny IS honored) strips the
#           agent's own reach to the network after it has ingested untrusted text. Bash-level egress
#           (curl) can't be closed by a permission flag — that is contained by the environment/network
#           policy, which the prefetch + `SUBAGENT_FACTORY_OFFLINE` ingest make it safe to set to
#           no-egress (in-session URL ingest is then a cache hit, never a live fetch).
#   review  a REVIEW/VERIFY session must not modify the files under review; it only Writes its own
#           report and Reads/greps/spawns sub-reviewers. Add `--disallowedTools Edit` so it cannot
#           edit existing files in place. Deny rules apply even under --dangerously-skip-permissions,
#           and in headless mode a denied call fails the session loudly (it never hangs). This is the
#           conservative form; it does not yet scope Write to the report path. The stricter form
#           (`--permission-mode dontAsk` + an explicit --allowedTools allowlist including
#           `Write(subagents/*/reports/**)`, Read/Grep/Glob/Task and the Bash gate commands) fully
#           scopes Write but needs one live headless smoke test first, because an incomplete
#           allowlist auto-denies and aborts the session.
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
  # Permission flags by session role (CLAUDE_PERM_PROFILE). NOTE: `claude` rejects
  # --dangerously-skip-permissions when the process runs as root ("permissions cannot be used with
  # root/sudo privileges"); run these headless sessions as a non-root user so the bypass is accepted.
  case "${CLAUDE_PERM_PROFILE:-author}" in
    review)
      # Read-only-plus-report: keep bypass but deny in-place edits (bare-tool deny is honored —
      # verified `--disallowedTools Edit` blocks Edit). Write/Bash stay open: a review session can
      # still overwrite via Write / shell redirection.
      #
      # The fully-scoped form the security review asked for (`--permission-mode dontAsk` + a Write
      # rule scoped to the report dir) is NOT achievable on claude 2.1.217. Verified empirically:
      # bare `Write` in an allowlist works, but ANY `Write(<path>)` specifier matches nothing and
      # denies even the legitimate report write — tested glob, absolute (`/` and `//`), and an exact
      # full path, via both `--allowedTools` and a `--settings` permissions.allow file. So Write
      # cannot be path-scoped through the permission system in this version; deny-Edit is the best it
      # allows. Residual Write/Bash mutation is contained OUT-OF-BAND instead: review/verify sessions
      # run on a throwaway review/<slug> branch (standalone loop) or an isolated git worktree
      # (drive-review-merge.sh), gated by a fresh `validate`, with fixes applied by separate sessions.
      # Revisit if a future claude honours `Write(<path>)` — then this becomes a one-line change.
      # Also deny the agent's own network tools: a review/verify session reads code and writes its
      # report — it has no legitimate need to fetch a URL or search the web (same trifecta reasoning
      # as the author profile). Space-separated single value; bare-tool deny is honored.
      _out+=(--dangerously-skip-permissions --disallowedTools "Edit WebFetch WebSearch")
      ;;
    *)  # author (default): full authority to create/edit files, but deny the agent's own network
        # tools. URL fetching is a deterministic pre-session step (prefetch → fetch_url), so the
        # session never legitimately needs these; denying them removes the trifecta's network leg
        # from the agent's toolset. Space-separated single value (bare-tool deny, verified honored).
      _out+=(--dangerously-skip-permissions --disallowedTools "WebFetch WebSearch")
      ;;
  esac
  _out+=(--output-format stream-json --verbose)
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
