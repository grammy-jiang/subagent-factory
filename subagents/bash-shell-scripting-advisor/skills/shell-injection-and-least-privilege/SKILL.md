---
name: shell-injection-and-least-privilege
kind: skill
status: ready
provenance:
  principles:
  - P006
  - P031
  - P071
  - P082
  - P086
  - P087
  - P103
  - P111
  - P121
  claims:
  - C00761
  - C00773
  - C00774
  - C00787
  - C00791
  - C00792
  - C00806
  - C01917
  - C01918
  - C02640
  evidence:
  - E00286
  - E00291
  - E00292
  - E00298
  - E00299
  - E00300
  - E00307
  - E00907
  - E00908
  - E01239
  source_anchors:
  - 10824bdf56f3-c0000
  - a1edef214807-c0000
  - 2583cb6ce003-c0001
  - c8604455f3d5-c0012
  - c8604455f3d5-c0013
  - 2583cb6ce003-c0004
  - 07b8d355a162-c0004
  - c8604455f3d5-c0036
  - 05f06662f2b0-c0000
  - 05f06662f2b0-c0002
  authored_from_digest: cae21a0c4e2eb2e0fadbdc3e6fe4b18f3e6a3ee1211e1aa01bee325fb98c8c8b
---

# Shell Injection and Least Privilege

## Purpose

Defend the OS-command-injection surface: keep untrusted input out of shell, `eval`, and arithmetic contexts, validate with positive allowlists, run with least privilege, and prefer APIs over shelling out. Grounded in the OWASP command-injection references.

## When this applies

- A process can invoke OS commands or external programs.
- A wrapper, helper, or application invokes operating-system commands with privileges beyond the attacker or caller.
- When a command needs administrative privileges.
- Administrative access is needed for a specific task.
- When adjusting access control beyond ordinary read/write bits.
- Changing modes or defaults for files and directories.
- Constructing and executing a command dynamically with eval
- A shell command must be constructed at runtime.
- Evaluating any expression that includes externally-sourced or unvalidated data
- Referencing an array element or variable inside an arithmetic expression with untrusted data
- Comparing externally-supplied or untrusted numeric input
- The application accepts or derives command arguments from external input.

## Procedure

1. Map every point where untrusted input (arguments, environment, files, network) can reach a shell, `eval`, `bash -c`, `system()`, or an arithmetic context (P082, P111).
2. Require a narrow positive allowlist — constraining format, permitted characters, and length, and excluding metacharacters and whitespace — not a blocklist or escaping as the only defence (P086, P087).
3. Prefer a language, platform, or library API over direct command execution; when a command must run, pass arguments as a vector, never a concatenated string (P121).
4. Confirm least privilege: the handler runs with only the privilege the single task needs, ideally in an isolated limited account (P006, P031, P103).
5. Restrict `eval` to genuinely dynamic commands built only from validated fragments, treating any data placed into an eval string as executable code (P071, P111).
6. Present no single guard as complete safety; emit findings highest-risk first, each with the injection path, the safer construct, and the residual risk. Do not produce a working exploit.

## Principles to apply

Each rule below is a promoted principle of this package; cite its ID in a finding.

- **P006** — Run command-executing code with the least privileges needed and use isolated limited accounts for single-purpose command tasks where feasible.
- **P031** — Treat special permission and attribute mechanisms as security-sensitive controls: conditional execute, setuid/setgid, sticky bit, umask, immutable attributes, and filesystem-specific extended attributes all need explicit intent.
- **P071** — Use eval only for genuinely dynamic commands built from validated fragments, because eval performs a second round of shell parsing and can execute untrusted input.
- **P082** — Never evaluate untrusted input in an arithmetic context (`(( ))`, `let`, an array subscript, or a `[[ ]]` numeric comparison): the text is expanded — including command substitution — before evaluation, enabling arbitrary command injection (e.g. `a[$(reboot)]`). Use bare variable names, validate inputs to decimal integers, and prefer a quoted `[ "$x" -gt N ]`, which requires decimal operands.
- **P086** — Validate command arguments with narrow positive allowlists that constrain format, permitted characters, and length, and exclude metacharacters and whitespace where possible.
- **P087** — For Java command execution, account for whether a shell is invoked and pass the executable and arguments separately rather than relying on a single command string as a safety boundary.
- **P103** — Use the dot utility to run a file in the current shell environment, knowing it is located through PATH (and need not be executable) and deliberately does not search the current directory unless PATH permits, which is a guard against trojan-horse scripts.
- **P111** — Avoid eval, and treat any data placed into an eval string as executable code.
- **P121** — Prefer language, platform, or library APIs over direct operating-system command execution whenever they can perform the task.

## Anti-patterns to flag

- Untrusted input concatenated into a shell string, `eval`, `bash -c`, `system()`, or an arithmetic context.
- Blocklist/escaping used as the only defence instead of a narrow positive allowlist.
- Running the command handler with more privilege than the single task needs.

## Review checklist

For the code under review, confirm each applicable principle holds; when one is violated, name the hazard, the failure it enables, the safer idiom, and the trade-off or portability caveat.

- [ ] (P006) Run command-executing code with the least privileges needed and use isolated limited…
- [ ] (P031) Treat special permission and attribute mechanisms as security-sensitive controls:…
- [ ] (P071) Use eval only for genuinely dynamic commands built from validated fragments, because eval…
- [ ] (P082) Never evaluate untrusted input in an arithmetic context (`(( ))`, `let`, an array…
- [ ] (P086) Validate command arguments with narrow positive allowlists that constrain format,…
- [ ] (P087) For Java command execution, account for whether a shell is invoked and pass the…
- [ ] (P103) Use the dot utility to run a file in the current shell environment, knowing it is located…
- [ ] (P111) Avoid eval, and treat any data placed into an eval string as executable code.…
- [ ] (P121) Prefer language, platform, or library APIs over direct operating-system command execution…
