---
name: error-handling-exit-status-and-traps
kind: skill
status: ready
provenance:
  principles:
  - P012
  - P069
  - P076
  - P081
  - P085
  - P092
  - P096
  - P102
  - P105
  - P112
  - P113
  - P119
  claims:
  - C00201
  - C00202
  - C00208
  - C00209
  - C00210
  - C01201
  - C01202
  - C01203
  - C01204
  - C01205
  evidence:
  - E00080
  - E00081
  - E00085
  - E00086
  - E00087
  - E00592
  - E00593
  - E00594
  - E00595
  - E00596
  source_anchors:
  - dd4e9d2506fb-c0001
  - dd4e9d2506fb-c0002
  - fc16a0303ffc-c0016
  - 2583cb6ce003-c0014
  - dd4e9d2506fb-c0007
  - ece374b583e8-c0007
  - ece374b583e8-c0000
  - ece374b583e8-c0003
  - 07b8d355a162-c0001
  - 457d111305bf-c0000
  authored_from_digest: 99881b452addb5f897f12ea08a004910c6747dd4205a50c633b65ebf2d646af2
---

# Error Handling Exit Status and Traps

## Purpose

Make scripts fail loud and clean: return and read exit status precisely, test commands directly, avoid the `&&`/`||` if-then-else trap, and use `trap` for cleanup and signal handling.

## When this applies

- When script failure should stop later actions or report a controlled problem.
- When writing or debugging shell scripts.
- A script misbehaves and the cause is not obvious
- Checking or reporting the exit status of a command
- Performing arithmetic or numeric tests
- Specifying which signals a trap handles in a portable script
- Terminating a shell or subshell with a specific status, or using an EXIT trap for cleanup
- Relying on traps across subshells, background jobs, or inherited-ignored signals
- Reasoning about how signals reach background jobs or when traps fire
- Choosing between two actions based on a test
- Mixing && and || where later commands must belong together
- The assignment value is provided by a command substitution

## Procedure

1. Establish what must fail loud and what cleanup must run on normal exit and on signals.
2. Trace exit status: every command exits 0–255, return non-zero on any unexpected failure (P012); read status precisely — 128+N means termination by signal N, values above 125 are reserved (P076); test a command's success directly with `if cmd; then …` and capture `$?` into a named variable immediately, only when the exact code is needed (P113).
3. Flag the `cmd1 && cmd2 || cmd3` if/then/else trap: the status carries through skipped commands, so a failure in `cmd2` can fire `cmd3` (P105). Recommend an explicit `if`.
4. Flag `local v=$(cmd)` (or `export`/`readonly`) combined with assignment on one line — the declaration's own status masks the command's exit code (P112); split declaration from assignment.
5. Check trap coverage (P085): `trap action sigspec`, `-` to reset a signal to its startup disposition, `''` to ignore; confirm cleanup of temp files/locks runs on the signals that matter, and review any `set -e`/`pipefail` assumptions and their documented gaps (P069, P081, P092, P096).
6. Emit findings highest-risk first, each with the failure it enables, the fail-loud idiom, and the caveat.

## Principles to apply

Each rule below is a promoted principle of this package; cite its ID in a finding.

- **P012** — Every command exits with a status 0-255 (0 = success by convention); make scripts fail loud by returning a non-zero code on any unexpected failure (e.g. cmd || { echo err >&2; exit 1; }); a leading ! negates a command's status and if branches on it.
- **P069** — Debug methodically: state the bug in one sentence, minimize to a 3-7 line reproduction, then trace with set -x (which prints each command after expansion and shows quoting so word-splitting is visible), scoping it with set -x/+x, redirecting it via BASH_XTRACEFD, and annotating it with a single-quoted PS4; step with a DEBUG trap, recheck the shebang and for carriage-return line endings, and reread the manual.
- **P076** — Interpret exit statuses precisely: 0 is success and any non-zero value is failure (8-bit, with values above 125 reserved), 128+N means termination by signal N, 127 means command-not-found, 126 means found-but-not-executable, and a builtin returns 2 for incorrect usage.
- **P081** — Use arithmetic contexts for math: (( )) is a test whose status is 0 for a true/non-zero expression and 1 for false/zero (the reverse of the exit convention — a known trap), while $(( )) substitutes the numeric result and is POSIX-portable; inside both you reference variables without $ and use C-like operators.
- **P085** — Register signal handlers with 'trap action sigspec' - using '-' to reset a signal to its startup disposition and an empty string to ignore it - relying on case-insensitive names (SIG prefix optional), 'trap -l' to list them, and 'trap' with no arguments to print reusable trap commands.
- **P092** — Use exit deliberately: it leaves the current execution environment (only the subshell when inside one) with the given status, defaults to the last command status when no operand is given, is undefined outside 0-255 and may be truncated above 255, and triggers a trap on EXIT before termination unless exit is called from within that trap.
- **P096** — Account for trap inheritance limits: signals ignored on entry to a non-interactive shell cannot be trapped or reset, entering a subshell resets non-ignored traps to their defaults, trap with no operands lists current traps in a form suitable for saving and restoring, and the ERR trap is a non-portable KornShell extension.
- **P102** — Account for signal handling in job control and traps: when job control is disabled, commands in an asynchronous list inherit an ignored action for SIGINT and SIGQUIT, and a trap for a signal received while the shell waits for a foreground command runs only after that command completes.
- **P105** — A cmd1 && cmd2 || cmd3 chain is not a safe if/then/else, because the exit status carries through skipped commands, so a failure in cmd1 can trigger the trailing || of a later command; group commands that belong together with { ...; } (a semicolon or newline is required before the closing brace).
- **P112** — Declare then assign on separate lines for `local`/`export`/`readonly` (`local v; v=$(cmd); rc=$?`): combined, the declaration's own exit status masks the command's, and in some shells the unquoted right-hand side undergoes word splitting.
- **P113** — Test a command's success directly (`if cmd; then ...`); only capture `$?` when you need the exact status, and save it immediately (`status=$?`) before other commands overwrite it.
- **P119** — Use the colon (:) null utility as a do-nothing placeholder where the grammar needs a command, remembering that as a special built-in it still performs its associated variable assignments (which persist) and redirections.

## Anti-patterns to flag

- `cmd1 && cmd2 || cmd3` used as if/then/else — the status carries through and `cmd3` can fire on a `cmd2` failure.
- `local v=$(cmd)` on one line — the declaration's own status masks `cmd`'s exit code.
- Reading `$?` after other commands have overwritten it, or limping on after an unchecked failure.

## Review checklist

For the code under review, confirm each applicable principle holds; when one is violated, name the hazard, the failure it enables, the safer idiom, and the trade-off or portability caveat.

- [ ] (P012) Every command exits with a status 0-255 (0 = success by convention); make scripts fail…
- [ ] (P069) Debug methodically: state the bug in one sentence, minimize to a 3-7 line reproduction,…
- [ ] (P076) Interpret exit statuses precisely: 0 is success and any non-zero value is failure (8-bit,…
- [ ] (P081) Use arithmetic contexts for math: (( )) is a test whose status is 0 for a true/non-zero…
- [ ] (P085) Register signal handlers with 'trap action sigspec' - using '-' to reset a signal to its…
- [ ] (P092) Use exit deliberately: it leaves the current execution environment (only the subshell…
- [ ] (P096) Account for trap inheritance limits: signals ignored on entry to a non-interactive shell…
- [ ] (P102) Account for signal handling in job control and traps: when job control is disabled,…
- [ ] (P105) A cmd1 && cmd2 || cmd3 chain is not a safe if/then/else, because the exit status carries…
- [ ] (P112) Declare then assign on separate lines for `local`/`export`/`readonly` (`local v;…
- [ ] (P113) Test a command's success directly (`if cmd; then ...`); only capture `$?` when you need…
- [ ] (P119) Use the colon (:) null utility as a do-nothing placeholder where the grammar needs a…
