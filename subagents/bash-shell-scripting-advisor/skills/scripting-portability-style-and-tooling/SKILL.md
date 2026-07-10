---
name: scripting-portability-style-and-tooling
kind: skill
status: ready
provenance:
  principles:
  - P002
  - P013
  - P025
  - P028
  - P038
  - P046
  - P047
  - P053
  - P056
  - P061
  - P093
  - P108
  - P114
  - P128
  - P140
  - P142
  - P147
  claims:
  - C00039
  - C00156
  - C00157
  - C00242
  - C00562
  - C00611
  - C00612
  - C00613
  - C01709
  - C01710
  evidence:
  - E00008
  - E00058
  - E00059
  - E00107
  - E00254
  - E00259
  - E00260
  - E00261
  - E00847
  - E00848
  source_anchors:
  - 457d111305bf-c0000
  - dd4e9d2506fb-c0000
  - dd4e9d2506fb-c0003
  - ece374b583e8-c0007
  - ece374b583e8-c0009
  - 07b8d355a162-c0000
  - c8604455f3d5-c0030
  - dd4e9d2506fb-c0006
  - ece374b583e8-c0004
  - fc16a0303ffc-c0012
  authored_from_digest: 15b4a01a8826759a57a8c1f9f2f4e9f24c446bdaa2797e2115da42ceddfdfd11
---

# Scripting Portability Style and Tooling

## Purpose

Keep scripts portable, correctly interpreted, and readable: the right shebang, Bash-vs-POSIX awareness, `getopts`, scoped startup files, and knowing when to leave the shell for a stronger language.

## When this applies

- You need parameters, recursion, or scripting
- A script or reviewer is considering aliases as a mechanism for reusable behaviour
- Customizing interactive shell commands.
- Writing a Bash script
- When a script should run directly by path.
- When a command sequence is reused or must adapt to inputs, files, shells, or failures.
- When a workflow is repeated often enough to justify reuse.
- Creating reusable shell commands.
- When a change series is not ready to merge.
- When managing separate lines of Git work.
- When checking out a commit instead of a branch tip.
- When using Git or Subversion collaboratively.

## Procedure

1. Establish the target: Bash (and which version) or POSIX sh, and the environments the script must run in.
2. Confirm the interpreter is declared correctly — `#!/usr/bin/env bash` when Bash features are used, never an implicit `/bin/sh` that silently forces POSIX mode (P013).
3. For each construct, name whether it is Bash-only or POSIX, and whether its behaviour differs across shells or versions; call the difference out rather than assume it is uniform (P002, P025, P028, P056).
4. Parse options with `getopts`, scope any startup-file assumptions, and keep the script readable — consistent indentation, clear long options and line continuations, comments for the reasoning, quoting over escaping (P108, P114, P128, P140).
5. Judge when the problem has outgrown the shell (complexity, maintainability, data structure) and recommend moving to a stronger language (P053).
6. Emit findings highest-risk first, each with the portability or interpreter hazard, the safer/portable idiom, and the trade-off.

## Principles to apply

Each rule below is a promoted principle of this package; cite its ID in a finding.

- **P002** — Do not rely on aliases for script logic: alias substitution applies only to the command-name word of a simple command, never to reserved words in context, is not inherited by separate shell invocations or utility environments, and only chains to the next word when the alias value ends in a blank.
- **P013** — Use the correct interpreter: put #!/usr/bin/env bash on the very first line of a Bash script (never omit it or use #!/bin/sh, which forces POSIX features even when /bin/sh is really Bash); running via ./script uses the shebang while 'bash script' ignores it; keep LF-only line endings and do not add a .sh extension.
- **P025** — Automate repeated shell work with variables, conditionals, loops, functions, and explicit error handling rather than duplicated command text.
- **P028** — Use version-control branches to isolate unfinished or experimental work, inspect diffs, commit deliberately, and make changes reviewable before sharing.
- **P038** — Use the configure and make workflow for building Bash or similar source packages, treating configure errors and missing Makefiles as blockers and using staging or out-of-tree builds when needed.
- **P046** — Prepare source builds safely by inspecting archives, extracting into controlled directories, reading project instructions, installing build tools, configuring prefixes when appropriate, and installing only after a successful build.
- **P047** — Treat interactive shell conveniences as stateful tools: use completion and editing modes for accuracy, but use history expansion cautiously because it can re-run prior commands.
- **P053** — Move from shell to a stronger programming language when the problem exceeds shell scripting complexity or maintainability limits.
- **P056** — Learn command-line work hands-on on an available Linux system, using a full installation when sustained practice needs speed and persistence.
- **P061** — Keep login-shell, default-shell, login-environment, and interactive startup changes minimal, tested, and placed in the appropriate user startup files unless administering all users.
- **P093** — Understand that running a script as a child cannot change your current shell's working directory or variables (the child's environment is discarded); source it with the . (dot) command to run its commands in the current shell.
- **P108** — Prefer readable scripts: use consistent indentation and style, clear long options or continuations when helpful, comments for reasoning, and quoting instead of escape clutter.
- **P114** — In an interactive bash before 4.3, a `!` inside double quotes triggers csh-style history expansion (`event not found`); disable it with `set +H`/`set +o histexpand` or use single quotes. Scripts are unaffected.
- **P128** — Use Git to track configuration changes and assemble each commit through an explicit staging area.
- **P140** — Test dotfiles in fresh target shells and source symlinked fragments only after readability and path checks.
- **P142** — Build CLI programs incrementally from stdin reading to validation, lookup, subprocess checks, structured parsing, and graceful missing-data handling.
- **P147** — Scope startup-file customizations to interactive shells and avoid exits, noise, slow commands, and complex failure-prone logic during startup.

## Review checklist

For the code under review, confirm each applicable principle holds; when one is violated, name the hazard, the failure it enables, the safer idiom, and the trade-off or portability caveat.

- [ ] (P002) Do not rely on aliases for script logic: alias substitution applies only to the…
- [ ] (P013) Use the correct interpreter: put #!/usr/bin/env bash on the very first line of a Bash…
- [ ] (P025) Automate repeated shell work with variables, conditionals, loops, functions, and explicit…
- [ ] (P028) Use version-control branches to isolate unfinished or experimental work, inspect diffs,…
- [ ] (P038) Use the configure and make workflow for building Bash or similar source packages,…
- [ ] (P046) Prepare source builds safely by inspecting archives, extracting into controlled…
- [ ] (P047) Treat interactive shell conveniences as stateful tools: use completion and editing modes…
- [ ] (P053) Move from shell to a stronger programming language when the problem exceeds shell…
- [ ] (P056) Learn command-line work hands-on on an available Linux system, using a full installation…
- [ ] (P061) Keep login-shell, default-shell, login-environment, and interactive startup changes…
- [ ] (P093) Understand that running a script as a child cannot change your current shell's working…
- [ ] (P108) Prefer readable scripts: use consistent indentation and style, clear long options or…
- [ ] (P114) In an interactive bash before 4.3, a `!` inside double quotes triggers csh-style history…
- [ ] (P128) Use Git to track configuration changes and assemble each commit through an explicit…
- [ ] (P140) Test dotfiles in fresh target shells and source symlinked fragments only after…
- [ ] (P142) Build CLI programs incrementally from stdin reading to validation, lookup, subprocess…
- [ ] (P147) Scope startup-file customizations to interactive shells and avoid exits, noise, slow…
