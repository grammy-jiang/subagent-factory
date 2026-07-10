---
name: linux-command-line-and-system-operations
kind: skill
status: ready
provenance:
  principles:
  - P003
  - P009
  - P029
  - P033
  - P034
  - P036
  - P037
  - P040
  - P041
  - P043
  - P044
  - P045
  - P048
  - P049
  - P051
  - P052
  - P054
  - P057
  - P060
  - P062
  - P067
  - P080
  - P104
  - P122
  - P123
  - P124
  - P125
  - P126
  - P129
  - P134
  - P137
  - P138
  - P139
  - P145
  claims:
  - C00304
  - C00305
  - C00306
  - C00307
  - C00308
  - C00637
  - C00638
  - C01964
  - C01965
  - C01966
  evidence:
  - E00143
  - E00144
  - E00145
  - E00146
  - E00147
  - E00266
  - E00267
  - E00942
  - E00943
  - E00944
  source_anchors:
  - dd4e9d2506fb-c0006
  - ece374b583e8-c0011
  - 2583cb6ce003-c0002
  - c8604455f3d5-c0013
  - c8604455f3d5-c0014
  - fc16a0303ffc-c0024
  - fc16a0303ffc-c0025
  - 2583cb6ce003-c0011
  - c8604455f3d5-c0019
  - c8604455f3d5-c0020
  authored_from_digest: 301adc197b2847232d6ac44b079e82691286648c57cec386764dc2a2de4e07a0
---

# Linux Command Line and System Operations

## Purpose

Perform everyday Linux command-line and light-sysadmin operations safely: inspect before modifying, treat destructive commands as permanent, signal processes with least force, and name the storage/network/package layer before acting.

## When this applies

- When controlling interactive or long-running shell work.
- Managing commands launched from an interactive terminal.
- When connecting to remote machines.
- When copying files to or from an SSH-accessible machine.
- When connecting to or transferring files with remote machines.
- Authenticating or transferring data across a network.
- Connecting to remote hosts with SSH.
- When setting up sample data or handling unfamiliar files.
- When managing files and folders from the shell.
- When performing basic file operations.
- When find will delete files or execute commands on matches.
- Using find -delete, -exec, -ok, or xargs.

## Procedure

1. Establish blast radius first: is the command destructive, privileged, or irreversible, and does it run against the correct target host and path?
2. Inspect before modifying: list or preview before delete/move/overwrite, and treat `rm`, truncation, and overwrite as permanent — there is no undo (P037, P040, P048).
3. Signal processes with least force — try `TERM` before `KILL` — after confirming the target PID or pattern (P057, P060).
4. Name the layer under change — filesystem, permissions/ownership, storage/mounts, processes, network, packages, archives — and apply that layer's safe idiom with the least privilege that works (P029, P033, P034, P036, P041, P043, P044, P045).
5. For each command prefer the explicit, safe invocation (long options in scripts, `--` to end option parsing, quoted paths) and state the portability caveat where GNU, BSD, and POSIX tools differ (P049, P051, P054, P122).
6. Emit findings highest-risk first, each with the failure it enables (data loss, wrong host, over-privilege), the safer invocation, and the caveat; escalate to a script or stronger tool when the task has outgrown one-liners.

## Principles to apply

Each rule below is a promoted principle of this package; cite its ID in a finding.

- **P003** — Use job control deliberately for interactive jobs, knowing how process groups, backgrounding, suspension, fg/bg/jobs/disown, and terminal signals affect job lifetime and input.
- **P009** — Use SSH-family tools for encrypted remote login and file transfer, with explicit credentials, protected keys, host-key awareness, ports, agents, terminal options, and clean session closure.
- **P029** — Inspect files and directories before modifying them, and use interactive or attribute-preserving options when overwrites, copies, moves, or recursive deletion carry risk.
- **P033** — Before deleting or executing from find results, verify the result set with printing or prompts and choose safer per-file or batched execution modes deliberately.
- **P034** — Use Linux directory conventions as diagnostic hints, but take a read-only system-tour approach and verify actual contents and permissions before editing system files.
- **P036** — Before storage operations, name the storage layer precisely and map block devices, partitions, filesystems, mount points, and directories with df or lsblk.
- **P037** — Use backup and sync tools with exact source/destination semantics, dry runs, and transport choices, especially rsync for repeated attribute-preserving synchronization.
- **P040** — Favor symbolic links for routine references, understand which operations affect the link versus the target, and prefer relative targets for movable trees.
- **P041** — Choose the line-editing mode with 'editing-mode' in the inputrc or 'set -o emacs'/'set -o vi'; in vi mode a new line starts in insert mode and ESC enters command mode (k/j move through history).
- **P043** — Signal processes with the least force that can work, escalating from normal termination to named signals, timeouts, and KILL only after ordinary termination fails.
- **P044** — Handle archives by first choosing the archive family and action, naming the archive explicitly, selecting compression flags by format, and controlling extraction destination.
- **P045** — Learn a terminal editor for remote and shell-only editing, and store its reusable configuration in dotfiles.
- **P048** — Verify the current directory, listings, hidden files, and path forms before running location-dependent commands; use absolute paths or home-directory forms intentionally.
- **P049** — Treat rm and shell deletion as permanent; preview wildcard targets and prefer interactive or nonrecursive removal unless recursive deletion is clearly intended.
- **P051** — Use compression tools with awareness of file replacement, stdout modes, integrity testing, compression levels, viewing helpers, speed, and recovery behavior.
- **P052** — Treat raw device copying with dd as high risk, verifying input and output devices and media type before running as root because mistakes can destroy data.
- **P054** — Access clipboards only through mechanisms supported by the active graphical or terminal environment, and choose the correct X selection for the paste target.
- **P057** — Compare and verify files with tools and checksum strength that match the question, using quiet modes in scripts and saved strong checksums for later integrity checks.
- **P060** — Design prompts with safe PS syntax, bracketing non-printing terminal sequences and accounting for any later prompt expansion of dynamic fields.
- **P062** — Inspect host, interface, address, route, DHCP, and gateway facts with current tools, preferring iproute2 output over legacy interface tools.
- **P067** — Mount and unmount filesystems through fstab-aware commands when possible, and unmount writable removable media before removal while respecting busy-filesystem refusals.
- **P080** — Use terminal-native editing, history, and clipboard conventions to edit commands safely instead of relying on ordinary GUI shortcuts.
- **P104** — Create, truncate, or timestamp files intentionally; use shell redirection for simple empty-file creation or truncation when touch-specific timestamp behavior is not required.
- **P122** — Prefer repository-backed package management for ordinary software maintenance, using high-level tools for dependency-aware operations and low-level package-file installation only cautiously.
- **P123** — Master tmux panes, windows, sessions, attach, detach, naming, and cleanup before adding advanced customizations such as Vim-style keys, styling, plugins, or advanced pane operations.
- **P124** — Navigate by maintaining awareness of the current directory and choosing clear absolute, relative, home, or previous-directory path forms.
- **P125** — Manage user accounts, shells, passwords, locks, groups, and IDs conservatively as persistent security state affecting login access and file ownership.
- **P126** — Use tar modes and path handling deliberately for archive creation, extraction, ownership, selective restore, incremental archives, standard streams, compression, file-list input, and SSH pipelines.
- **P129** — Diagnose processes by understanding parent-child relationships, ownership, PID identity, daemon role, and snapshot versus live views.
- **P134** — Use tmux for persistent, organized, remote-friendly terminal sessions, including SSH sessions that should resume after disconnects.
- **P137** — Understand mounting through fstab, labels or UUIDs, mount points, mount listings, and filesystem types before manually attaching storage.
- **P138** — For copy, move, and remove operations, choose options that match overwrite, recursion, update, and confirmation requirements before executing.
- **P139** — Use lp and a2ps layout controls with upstream pagination alignment when print orientation, density, scaling, page ranges, or pretty PostScript output matter.
- **P145** — Understand Linux printing as a CUPS and Ghostscript workflow with queues, conversion, page description, and rasterization.

## Review checklist

For the code under review, confirm each applicable principle holds; when one is violated, name the hazard, the failure it enables, the safer idiom, and the trade-off or portability caveat.

- [ ] (P003) Use job control deliberately for interactive jobs, knowing how process groups,…
- [ ] (P009) Use SSH-family tools for encrypted remote login and file transfer, with explicit…
- [ ] (P029) Inspect files and directories before modifying them, and use interactive or…
- [ ] (P033) Before deleting or executing from find results, verify the result set with printing or…
- [ ] (P034) Use Linux directory conventions as diagnostic hints, but take a read-only system-tour…
- [ ] (P036) Before storage operations, name the storage layer precisely and map block devices,…
- [ ] (P037) Use backup and sync tools with exact source/destination semantics, dry runs, and…
- [ ] (P040) Favor symbolic links for routine references, understand which operations affect the link…
- [ ] (P041) Choose the line-editing mode with 'editing-mode' in the inputrc or 'set -o emacs'/'set -o…
- [ ] (P043) Signal processes with the least force that can work, escalating from normal termination…
- [ ] (P044) Handle archives by first choosing the archive family and action, naming the archive…
- [ ] (P045) Learn a terminal editor for remote and shell-only editing, and store its reusable…
- [ ] (P048) Verify the current directory, listings, hidden files, and path forms before running…
- [ ] (P049) Treat rm and shell deletion as permanent; preview wildcard targets and prefer interactive…
- [ ] (P051) Use compression tools with awareness of file replacement, stdout modes, integrity…
- [ ] (P052) Treat raw device copying with dd as high risk, verifying input and output devices and…
- [ ] (P054) Access clipboards only through mechanisms supported by the active graphical or terminal…
- [ ] (P057) Compare and verify files with tools and checksum strength that match the question, using…
- [ ] (P060) Design prompts with safe PS syntax, bracketing non-printing terminal sequences and…
- [ ] (P062) Inspect host, interface, address, route, DHCP, and gateway facts with current tools,…
- [ ] (P067) Mount and unmount filesystems through fstab-aware commands when possible, and unmount…
- [ ] (P080) Use terminal-native editing, history, and clipboard conventions to edit commands safely…
- [ ] (P104) Create, truncate, or timestamp files intentionally; use shell redirection for simple…
- [ ] (P122) Prefer repository-backed package management for ordinary software maintenance, using…
- [ ] (P123) Master tmux panes, windows, sessions, attach, detach, naming, and cleanup before adding…
- [ ] (P124) Navigate by maintaining awareness of the current directory and choosing clear absolute,…
- [ ] (P125) Manage user accounts, shells, passwords, locks, groups, and IDs conservatively as…
- [ ] (P126) Use tar modes and path handling deliberately for archive creation, extraction, ownership,…
- [ ] (P129) Diagnose processes by understanding parent-child relationships, ownership, PID identity,…
- [ ] (P134) Use tmux for persistent, organized, remote-friendly terminal sessions, including SSH…
- [ ] (P137) Understand mounting through fstab, labels or UUIDs, mount points, mount listings, and…
- [ ] (P138) For copy, move, and remove operations, choose options that match overwrite, recursion,…
- [ ] (P139) Use lp and a2ps layout controls with upstream pagination alignment when print…
- [ ] (P145) Understand Linux printing as a CUPS and Ghostscript workflow with queues, conversion,…
