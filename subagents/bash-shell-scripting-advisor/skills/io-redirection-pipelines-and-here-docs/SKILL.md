---
name: io-redirection-pipelines-and-here-docs
kind: skill
status: ready
provenance:
  principles:
  - P008
  - P018
  - P021
  - P050
  - P059
  - P077
  - P079
  - P088
  - P091
  - P097
  - P109
  - P110
  - P120
  - P136
  - P143
  claims:
  - C00207
  - C00233
  - C00284
  - C00361
  - C01800
  - C02542
  - C02543
  - C00037
  - C00083
  - C00084
  evidence:
  - E00084
  - E00099
  - E00128
  - E00178
  - E00879
  - E01195
  - E01196
  - E00006
  - E00037
  - E00038
  source_anchors:
  - dd4e9d2506fb-c0002
  - dd4e9d2506fb-c0003
  - dd4e9d2506fb-c0005
  - ece374b583e8-c0000
  - 07b8d355a162-c0002
  - c8604455f3d5-c0010
  - 457d111305bf-c0000
  - 05f06662f2b0-c0000
  - 05f06662f2b0-c0002
  - ece374b583e8-c0003
  authored_from_digest: 283686095e328fd06ad8eaf816e12dbf706dc2710501590f1185c5badd03166b
---

# Io Redirection Pipelines and Here Docs

## Purpose

Drive input, output, redirection, pipelines, subshells, and here-documents deliberately, knowing redirection order, truncation, FD duplication, and per-stage subshell semantics.

## When this applies

- Several commands should share one redirection
- Redirecting the combined output or input of a loop or group
- Multiple command outputs need the same destination.
- A loop or assignment on the right-hand side of a pipe must set variables the rest of the script reads
- A piped command sets a variable you need, or a pipeline grows long
- Redirecting both stdout and stderr
- Merging stdout and stderr
- Writing a here-document whose body should or should not be expanded
- Generating multi-line text or feeding commands from scripts.
- Redirecting a command's input or output
- When capturing, redirecting, or piping command output.
- Feeding inline or variable data to a command

## Procedure

1. Map the data flow: which file descriptors, which redirections, which pipeline stages, and where each subshell boundary falls.
2. Check redirection order and truncation: `>file 2>&1` is not `2>&1 >file` (order and FD-duplication differ), and confirm `>`/`>>` truncate-vs-append intent (P077, P079, P109).
3. Flag state set inside `… | while` that is expected to persist — each pipeline stage runs in its own subshell (P018); recommend process substitution or reading in the current shell when persistence is required.
4. Prefer `$(command)` over backquotes and `printf` over `echo` for reliable output (P088, P110); confirm here-doc / here-string quoting controls expansion as intended (`<<EOF` vs `<<'EOF'`) (P091, P097, P120).
5. Confirm the pipeline's exit status is read correctly — the last stage, or `PIPESTATUS`/`pipefail` where available (P021, P059).
6. Emit findings highest-risk first, each with the hazard, the failure it enables, the correct redirection/idiom, and the caveat.

## Principles to apply

Each rule below is a promoted principle of this package; cite its ID in a finding.

- **P008** — Apply a single redirection to a whole compound command (a loop's done or a { } group) to redirect every command inside it; Bash opens the file once before the construct and closes it after, and inner commands inherit the FD.
- **P018** — Each stage of a pipeline runs in a separate subshell, so variables modified inside `... | while` do not persist afterward; POSIX leaves whether the last stage is a subshell unspecified (lastpipe/ksh93 differ), so do not depend on it — feed the loop with process substitution or `read` instead.
- **P021** — Combine stdout and stderr in the correct order: >file 2>&1 duplicates the stdout FD into stderr (shared file position, no clobber), whereas 2>&1 >file leaves errors on the terminal, and >file 2>file must never be used (two independent FDs clobber each other).
- **P050** — Use here-documents for multi-line embedded input or output, quoting the delimiter to suppress body expansion and using <<- only when leading tabs should be stripped.
- **P059** — Know redirection semantics: > sends stdout to a file and truncates it (creating it if absent, performed before the command runs), >> appends instead, < feeds stdin from a file, and a leading number selects the FD; every process has FD 0/1/2 = stdin/stdout/stderr.
- **P077** — Use here-documents and here-strings to feed inline input, quoting the delimiter for literal here-doc bodies and using <<- only when leading tabs should be stripped.
- **P079** — Choose redirection operators by intent: > creates or truncates, >> appends, noclobber makes > fail unless >| is used, and combined-stream forms redirect or append stdout and stderr together.
- **P088** — Prefer the $(command) form over backquotes for command substitution: it runs the command in a subshell and substitutes its standard output with trailing newlines stripped, its result is not re-expanded, and it avoids the backslash and nesting pitfalls of backquotes.
- **P091** — Choose a subshell versus a command group deliberately: a subshell ( ) runs in a temporary child (cd, variable, and exit effects do not persist; each pipeline stage is one), while a { } group runs in the current shell (faster, side effects persist, and exit ends the whole script).
- **P097** — Use printf instead of echo for reliable script-grade formatted output, treating format and argument mismatches as bugs.
- **P109** — Commands run with & are asynchronous, and when job control is disabled their standard input defaults to a /dev/null-like source unless redirected explicitly.
- **P110** — Use tee with output process substitution when one stream must both remain visible and feed a secondary consumer.
- **P120** — Duplicate, move, open, or close file descriptors explicitly with the [n]<&word, [n]>&word, [n]<&digit-, [n]>&digit-, and [n]<>word redirection forms.
- **P136** — Build pipelines incrementally from clear transformations and use readability, not dogma, to decide whether a helper such as cat is acceptable.
- **P143** — Use printf in scripts for predictable formatted output, matching conversions and arguments and applying flags, width, precision, tabs, and newlines deliberately.

## Anti-patterns to flag

- Assuming `var` set inside `... | while` persists — each pipeline stage runs in its own subshell.
- `2>&1 >file` when you meant `>file 2>&1` — order and FD-duplication differ.
- Backquotes instead of `$(...)`, or `echo` where `printf` is needed for reliable output.

## Review checklist

For the code under review, confirm each applicable principle holds; when one is violated, name the hazard, the failure it enables, the safer idiom, and the trade-off or portability caveat.

- [ ] (P008) Apply a single redirection to a whole compound command (a loop's done or a { } group) to…
- [ ] (P018) Each stage of a pipeline runs in a separate subshell, so variables modified inside `... |…
- [ ] (P021) Combine stdout and stderr in the correct order: >file 2>&1 duplicates the stdout FD into…
- [ ] (P050) Use here-documents for multi-line embedded input or output, quoting the delimiter to…
- [ ] (P059) Know redirection semantics: > sends stdout to a file and truncates it (creating it if…
- [ ] (P077) Use here-documents and here-strings to feed inline input, quoting the delimiter for…
- [ ] (P079) Choose redirection operators by intent: > creates or truncates, >> appends, noclobber…
- [ ] (P088) Prefer the $(command) form over backquotes for command substitution: it runs the command…
- [ ] (P091) Choose a subshell versus a command group deliberately: a subshell ( ) runs in a temporary…
- [ ] (P097) Use printf instead of echo for reliable script-grade formatted output, treating format…
- [ ] (P109) Commands run with & are asynchronous, and when job control is disabled their standard…
- [ ] (P110) Use tee with output process substitution when one stream must both remain visible and…
- [ ] (P120) Duplicate, move, open, or close file descriptors explicitly with the [n]<&word,…
- [ ] (P136) Build pipelines incrementally from clear transformations and use readability, not dogma,…
- [ ] (P143) Use printf in scripts for predictable formatted output, matching conversions and…
