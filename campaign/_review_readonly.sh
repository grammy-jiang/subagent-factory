#!/usr/bin/env bash
# Sourceable helper for review-subagent-loop.sh: the read-only guard for review/verify sessions.
#
# Write cannot be permission-scoped in this claude version (see _claude_run.sh — bare `Write` is
# allow-all, `Write(<path>)` matches nothing). So a review session is prevented from PERSISTING
# changes to the package it reviews at the LOOP level instead: snapshot the package before the
# session, then after it revert every NON-report file it modified and delete every NON-report file it
# created. Its report under `subagents/<slug>/reports/` is the only permitted output.
#
# The snapshot is taken BEFORE the session so the guard reverts only THIS review's writes — never an
# uncommitted prior-round fix (tracked mods are captured by `git stash create`; a prior round's new
# untracked files are captured in the before-list and thus left intact).
#
# Two functions, no dependency on the caller's `say`/$LOGDIR (enforce echoes a count the caller logs).
# All git ops assume cwd == repo root (as review-subagent-loop.sh guarantees).

# review_readonly_snapshot PKG BEFORE_UNTRACKED_OUT  -> echoes PRE (stash SHA, or HEAD when clean)
# Call BEFORE the review session.
review_readonly_snapshot() {
  local pkg="$1" before_out="$2" pre
  git ls-files --others --exclude-standard -- "$pkg" 2>/dev/null \
    | grep -vE "^$pkg/reports/" | sort -u > "$before_out" 2>/dev/null || : > "$before_out"
  pre="$(git stash create 2>/dev/null || true)"
  printf '%s' "${pre:-HEAD}"
}

# review_readonly_enforce PKG PRE BEFORE_UNTRACKED_FILE  -> echoes count of files reverted (0 = clean)
# Call AFTER the review session.
review_readonly_enforce() {
  local pkg="$1" pre="$2" before_file="$3" strays newf f
  # NON-report tracked files the session modified (diff vs the pre-review snapshot).
  strays="$(git diff --name-only "$pre" -- "$pkg" 2>/dev/null | grep -vE "^$pkg/reports/" || true)"
  # NON-report files newly created by the session = current untracked minus the pre-review untracked.
  newf="$(comm -13 "$before_file" \
    <(git ls-files --others --exclude-standard -- "$pkg" 2>/dev/null \
        | grep -vE "^$pkg/reports/" | sort -u) 2>/dev/null || true)"
  printf '%s\n' "$strays" | while IFS= read -r f; do
    [ -n "$f" ] || continue
    git checkout "$pre" -- "$f" >/dev/null 2>&1 || true
  done
  printf '%s\n' "$newf" | while IFS= read -r f; do
    [ -n "$f" ] || continue
    git clean -fq -- "$f" >/dev/null 2>&1 || true
  done
  printf '%s' "$(printf '%s\n%s\n' "$strays" "$newf" | grep -c . || true)"
}
