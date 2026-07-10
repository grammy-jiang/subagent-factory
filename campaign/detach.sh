#!/usr/bin/env bash
# detach.sh — launch a forked-engine command SURVIVABLY. setsid puts the command in a NEW session +
# process group, reparented to init/systemd, so it OUTLIVES the caller's process group being killed.
#
# WHY: a headless engine session (`claude -p` / `codex exec` / `copilot -p`) started as a child of a
# Claude Code Bash-tool *background task* dies when that task is reaped — this killed a p2b run mid-work
# on 2026-07-10. `nohup` (SIGHUP-ignore) does NOT save it; only a new session (`setsid`) does.
#
# USE for the launchers that background a subshell inheriting an argv ARRAY and so cannot self-setsid
# internally (an internal `setsid bash -c "$(declare -f ...)"` drops the array + reintroduces a quoting
# bug those scripts deliberately fixed): map_book.sh / map_books.sh, generate-subagent.sh, faith-run.sh.
#   bash campaign/detach.sh bash campaign/map_books.sh --book B.md --engine codex --max-attempts 1
#   bash campaign/detach.sh bash campaign/faith-run.sh  --slug S --yes
#   bash campaign/detach.sh bash campaign/p2b_finish.sh --slug S --engine claude --fg   # also works
#
# precision_filter.sh / p2b_finish.sh already self-setsid in their NON-fg bg mode — for those just omit
# --fg instead of wrapping. Either way: GATE ON A COMPLETION MARKER (principles.yaml / ===P2B_SUMMARY===
# / the exported adapter file), NOT a task-notification — a detached session is intentionally not a
# tracked bg task. Verify detachment once: `ps -o pid,ppid,sid,cmd -p <engine-pid>` → parent chain
# should reach PID 1 (systemd/init).
set -uo pipefail
[ "$#" -ge 1 ] || { echo "usage: detach.sh <command> [args...]" >&2; exit 2; }
REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
log="${DETACH_LOG:-$REPO/campaign/logs/detach-$$.log}"
mkdir -p "$(dirname "$log")"
setsid "$@" </dev/null >"$log" 2>&1 &
pid=$!
disown 2>/dev/null || true
echo "[detach] setsid leader pid=$pid  log=$log"
echo "[detach] cmd: $*"
echo "[detach] gate on a completion marker, not a notification; verify: ps -o pid,ppid,sid,cmd -p $pid"
