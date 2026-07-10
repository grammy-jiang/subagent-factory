---
name: bash-shell-scripting-principles-index
kind: reference
status: ready
provenance:
  principles:
  - P001
  - P002
  - P003
  - P004
  - P005
  - P006
  - P007
  - P008
  - P009
  - P010
  - P011
  - P012
  - P013
  - P014
  - P015
  - P016
  - P017
  - P018
  - P019
  - P020
  - P021
  - P022
  - P023
  - P024
  - P025
  - P026
  - P027
  - P028
  - P029
  - P030
  - P031
  - P032
  - P033
  - P034
  - P035
  - P036
  - P037
  - P038
  - P039
  - P040
  - P041
  - P042
  - P043
  - P044
  - P045
  - P046
  - P047
  - P048
  - P049
  - P050
  - P051
  - P052
  - P053
  - P054
  - P055
  - P056
  - P057
  - P058
  - P059
  - P060
  - P061
  - P062
  - P063
  - P064
  - P065
  - P066
  - P067
  - P068
  - P069
  - P070
  - P071
  - P072
  - P073
  - P074
  - P075
  - P076
  - P077
  - P078
  - P079
  - P080
  - P081
  - P082
  - P083
  - P084
  - P085
  - P086
  - P087
  - P088
  - P089
  - P090
  - P091
  - P092
  - P093
  - P094
  - P095
  - P096
  - P097
  - P098
  - P099
  - P100
  - P101
  - P102
  - P103
  - P104
  - P105
  - P106
  - P107
  - P108
  - P109
  - P110
  - P111
  - P112
  - P113
  - P114
  - P115
  - P116
  - P117
  - P118
  - P119
  - P120
  - P121
  - P122
  - P123
  - P124
  - P125
  - P126
  - P127
  - P128
  - P129
  - P130
  - P131
  - P132
  - P133
  - P134
  - P135
  - P136
  - P137
  - P138
  - P139
  - P140
  - P141
  - P142
  - P143
  - P144
  - P145
  - P146
  - P147
  - P148
  - P149
  - P150
  claims:
  - C00001
  - C00002
  - C00003
  - C00004
  - C00005
  - C00006
  - C00007
  - C00008
  - C00009
  - C00010
  - C00011
  - C00012
  evidence:
  - E00001
  - E00002
  - E00003
  - E00004
  - E00005
  - E00006
  - E00007
  - E00008
  - E00009
  - E00010
  - E00011
  - E00012
  source_anchors:
  - 457d111305bf-c0000
  - 457d111305bf-c0001
  - 05f06662f2b0-c0000
  - 05f06662f2b0-c0001
  - 05f06662f2b0-c0002
  - 05f06662f2b0-c0003
  - dd4e9d2506fb-c0000
  - dd4e9d2506fb-c0001
  - dd4e9d2506fb-c0002
  - dd4e9d2506fb-c0003
  - dd4e9d2506fb-c0004
  - dd4e9d2506fb-c0005
  authored_from_digest: 4a8e77e97506a089583fee7c9091076efc123f22612688b2da74f053423d3ec3
---

# Bash & Shell Scripting — Principles Index

The 150 promoted principles of this package, grouped by skill. Cite the principle ID (e.g. `P004`) in any finding. Each statement is the package's own distillation of its eleven sources; for exact behaviour, consult the source (GNU Bash manual / POSIX for defined behaviour).

## Quoting Splitting and Globbing

- **P004** — Double-quote every parameter expansion and command substitution used as data (filenames, arguments, test operands); unquoted, they undergo word splitting on $IFS and pathname expansion (globbing), corrupting any value that contains whitespace or glob characters. Note that quotes nest across a `$(...)` boundary as a separate pair.
- **P005** — Quote every character that has special meaning to the shell when it must be literal, and pick the quoting mechanism by its scope: single-quotes preserve everything (and cannot contain a single-quote), double-quotes preserve everything except the dollar-sign, backquote, and backslash, and an unquoted backslash escapes just the next character.
- **P007** — Double-quote expansions to control field splitting: only the unquoted results of parameter expansion, command substitution, and arithmetic expansion are split, IFS drives how they split (with a null IFS disabling splitting entirely), so quoting is the primary defence against accidental word-splitting.
- **P019** — Move filenames between tools NUL-delimited: `find -print0 | xargs -0`, `printf '%s\0'`, or `find -exec cmd {} +` — never bare `xargs`, which splits on whitespace and mishandles quotes; and pass `{}` to `find -exec sh -c` as a positional argument (`sh -c '... "$1"' x {}`), never interpolated into the code, which is a command-injection vector.
- **P020** — Quoting changes matching semantics: in `[[ ]]` the RHS of `=`/`==` is a glob pattern (quote it for a literal compare) and the RHS of `=~` is a regex (quote it for a literal, or store a long regex in a variable); `>`/`<` in `[[ ]]` compare by string collation, not numerically.
- **P030** — Quote find patterns and compose tests, grouping, and logical operators so the shell does not rewrite the search expression before find evaluates it.
- **P068** — Never build a filename list by iterating command output (`for f in $(ls)`/`$(find)`) or by parsing `ls`: command substitution provides no safe delimiter (a pathname may contain any byte but NUL, including newline), `ls` output is for humans and may mangle names, and quoting the whole substitution collapses it to one word. Use globs or `find` instead.
- **P089** — Treat tilde expansion as dependent on the user database and HOME: a bare tilde expands to HOME, an unset HOME makes it unspecified, and the resulting pathname is treated as quoted so it is not re-split or globbed.
- **P090** — Call `tr` without bracket ranges — `tr A-Z a-z` (the brackets in `tr [A-Z] [a-z]` are shell globs and tr translates them literally) — and force `LC_COLLATE=C` for the 26 ASCII letters or use the quoted `[:upper:]`/`[:lower:]` classes, since letter ranges are locale-dependent.
- **P094** — Generate strings textually with brace expansion ('{a,b,c}' or '{x..y..incr}') before any other expansion, knowing the files need not exist, endpoints of a sequence must be the same type, and '${' inhibits it.
- **P098** — Stop filenames that begin with `-` from being read as options: prefix expansions with `./` (so `-foo` becomes `./-foo`), or pass `--` end-of-options before filename arguments — repeated at every site, and knowing some programs (e.g. `echo`) do not honour it.
- **P099** — Quote filename patterns that must be literal (or use 'set -f'), and enable 'nullglob' or 'failglob' so an unmatched pattern is removed or raises an error instead of being passed through literally, which prevents the common bug of a loop running once over an unmatched '*'.
- **P100** — Treat command-substitution output as untrusted for splitting: null bytes in the output make the behaviour unspecified and embedded newlines can be split into separate fields per IFS, so quote the substitution or sanitize its output when the exact value matters.
- **P135** — Remember that shell expansions happen before command execution, so commands receive expanded arguments rather than the original syntax.
- **P014** — Protect dash-leading operands from option parsing by using --, ./ prefixes, quoting, escaping, or explicit dotfile handling as appropriate for the command.

## Variables Parameters and Expansion

- **P001** — Know that a variable assignment prefixed to a command scopes differently by target: before an ordinary utility it is exported only for that command, before a special built-in it persists in the current environment, before a function it applies during the call with unspecified persistence afterward, and any assignment to a readonly variable is an error.
- **P015** — Declare function-private variables with 'local', and account for Bash's dynamic scoping: a called function sees its caller's locals (which shadow globals) and the shadowed value is restored when the declaring function returns.
- **P023** — Remove functions and variables with unset, disambiguating with -f (function) or -v (variable) since variables win by default, and quote an array subscript in unset ('a[2]') so it is not treated as a glob.
- **P035** — Use parameter expansion with quoting and braces for required values, alternates, defaults, substrings, arrays, cleanup, prefix introspection, and simple path text manipulation before spawning external tools.
- **P064** — Assign shell variables without surrounding spaces, quote values containing spaces, and use braces when adjacent text would confuse variable names.
- **P074** — Use special parameters for runtime state such as the last status, background PID, argument count, script name, and positional parameters, quoting "$@" when preserving arguments.
- **P075** — Prefer Bash parameter expansion for routine string length, trimming, removal, case conversion, substitution, slicing, and default handling when shell patterns are sufficient.
- **P115** — Wrap a parameter name in braces (${name}) whenever the expansion is immediately followed by characters that are valid in a variable name.
- **P117** — Use set -a (allexport) sparingly and know its scoping: it gives the export attribute to every assigned variable, but an assignment preceding an ordinary utility does not persist that attribute (one preceding a special built-in does), while a standalone assignment or one from getopts or read persists until the variable is unset.
- **P118** — Create a nameref with 'declare -n ref=name' to operate indirectly on another variable, commonly to manipulate a variable whose name is passed as a function argument.
- **P127** — Manage shell variables, exports, quoting, and braces deliberately to prevent unintended expansion or environment damage.
- **P058** — Validate and report script arguments with positional parameters, argument counts, brace syntax, shift, script-name extraction, all-argument iteration, usage messages, and explicit exit codes.

## Functions Arrays and Structured Data

- **P011** — Parse options with 'getopts optstring name' (which sets name, OPTIND, and OPTARG), always resetting OPTIND to 1 before re-parsing a new argument set in the same shell because it is not reset automatically, and prefix optstring with ':' for silent error handling.
- **P039** — Use Bash arrays for multi-value state in Bash-compatible scripts, accounting for creation, iteration, indexing, ordering, sparseness, version, and non-empty-input assumptions.
- **P055** — Control 'read' with its options: -a to fill an array, -d for a custom delimiter, -n/-N for a fixed number of characters, -s to suppress echo, -p for a prompt, -u to read from a descriptor, and -t for a timeout (which returns a status above 128 and applies only to terminals, pipes, or special files).
- **P083** — Use associative arrays only when unordered key/value storage is acceptable; preserve values when expanding and sort output explicitly when presentation order matters.
- **P084** — Inside functions, use the function positional parameters, FUNCNAME, and quoted argument forwarding to build reusable wrappers safely.
- **P095** — Define shell functions with valid names and compound-command bodies, knowing calls run the body with temporary positional parameters and return the body or explicit return status.
- **P106** — Loop over an array's indices with "${!arr[@]}" when you must correlate parallel arrays by index or when the array may be sparse; never assume indices are contiguous or that the first iteration is index 0.
- **P107** — Use functions to isolate and reuse code, but in moderation (too many scattered functions hurt readability); inside a wrapper function named after a command, call the real command with the command builtin to avoid infinite recursion.
- **P133** — Write shell functions as named reusable blocks with local variables and named parameters where readability needs them.
- **P141** — Use arrays and parameter expansion for simple structured shell data, but switch languages when data modeling starts dominating the script.
- **P146** — Use array-to-pipeline transformations, unset semantics, and associative arrays to sort, delete, look up, count, and model keyed or multidimensional data.

## Control Flow Conditionals and Loops

- **P016** — Write robust 'test'/'[' conditions: give each operator and operand as a separate argument (with a closing ']'), quote operands because a one-argument test is true for any non-null string, and restrict each test to a single primary combined with '&&'/'||' instead of the POSIX-deprecated '-a', '-o', and parentheses.
- **P017** — Use && and || for short-circuit control flow: after && the next command runs only if the previous succeeded, after || only if it failed, commands are expanded only when they are actually executed, and the list status is that of the last command executed.
- **P022** — Prefer the double-quoted "$@" to preserve each positional parameter as its own field, and use "$*" only when a single IFS-joined string is intended, because unquoted @ and * are subject to field splitting and pathname expansion.
- **P027** — Use traditional for loops over generated words, positional parameters, and glob results while checking unmatched globs and preserving loop-variable clarity.
- **P032** — Format shell control flow so keywords appear at valid command boundaries, and choose if/elif, case, while, until, or for according to the branching or looping model.
- **P042** — Use shell arithmetic only for integer logic, being explicit about bases, division truncation, modulo, assignment versus equality, and increment semantics.
- **P063** — Choose calculator tools by complexity: shell arithmetic or expr for simple expressions, bc for precision and programmable arithmetic, and dc only for acceptable stack/RPN workflows.
- **P070** — Order case patterns from specific to catch-all, add a final * default when unmatched input should be handled, and remember that a case with no match returns success.
- **P073** — For recursive file iteration use `find -exec cmd {} \;`/`{} +` (portable), or in bash `find -print0 | while IFS= read -r -d '' f` (which also runs the loop body in the current shell so variables persist), or bash 4+ `globstar` (`**`).
- **P101** — Use the file-test primaries (-e exists, -f regular file, -d directory, -r/-w/-x permissions, -s non-empty, -L/-h symlink, -p FIFO, -S socket, -t terminal, and -nt/-ot/-ef comparisons), remembering they follow symbolic links and test the target unless the test is symlink-specific.
- **P116** — Choose comparison operators by operand type: string operators compare strings, while -eq/-ne/-lt/-le/-gt/-ge compare integers.
- **P132** — Choose string, integer, regex, pattern, and arithmetic test forms according to the value being validated or compared.
- **P150** — Choose the loop form that matches the problem: fixed ranges, numeric counters, unknown repetition, streamed lines, or interactive menus.

## Io Redirection Pipelines and Here Docs

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

## Error Handling Exit Status and Traps

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

## Shell Injection and Least Privilege

- **P006** — Run command-executing code with the least privileges needed and use isolated limited accounts for single-purpose command tasks where feasible.
- **P031** — Treat special permission and attribute mechanisms as security-sensitive controls: conditional execute, setuid/setgid, sticky bit, umask, immutable attributes, and filesystem-specific extended attributes all need explicit intent.
- **P071** — Use eval only for genuinely dynamic commands built from validated fragments, because eval performs a second round of shell parsing and can execute untrusted input.
- **P082** — Never evaluate untrusted input in an arithmetic context (`(( ))`, `let`, an array subscript, or a `[[ ]]` numeric comparison): the text is expanded — including command substitution — before evaluation, enabling arbitrary command injection (e.g. `a[$(reboot)]`). Use bare variable names, validate inputs to decimal integers, and prefer a quoted `[ "$x" -gt N ]`, which requires decimal operands.
- **P086** — Validate command arguments with narrow positive allowlists that constrain format, permitted characters, and length, and exclude metacharacters and whitespace where possible.
- **P087** — For Java command execution, account for whether a shell is invoked and pass the executable and arguments separately rather than relying on a single command string as a safety boundary.
- **P103** — Use the dot utility to run a file in the current shell environment, knowing it is located through PATH (and need not be executable) and deliberately does not search the current directory unless PATH permits, which is a guard against trojan-horse scripts.
- **P111** — Avoid eval, and treat any data placed into an eval string as executable code.
- **P121** — Prefer language, platform, or library APIs over direct operating-system command execution whenever they can perform the task.

## Text Processing and Regex Tools

- **P010** — Choose text inspection and transformation tools by data shape, composing narrow tools into pipelines and escalating to awk, sed, or a programming language when the structure demands it.
- **P024** — Build regular expressions iteratively against valid and invalid examples, using anchors, escapes, captures, character classes, quantifiers, and locale controls to encode the intended data constraint.
- **P026** — Use grep and its variants with quoted patterns and explicit options that match the needed search semantics, output, context, recursion, filenames, line numbers, and fixed-string or regex behavior.
- **P065** — Use in-place sed only when rewriting the target file is intended; prefer writing transformed output to a new file or using a templating tool when direct edits become risky or unclear.
- **P066** — Sort and deduplicate with semantics that match the data, remembering uniq only removes adjacent duplicates while sort -u can sort and deduplicate together.
- **P072** — Avoid broad or complicated pattern and regex matching against long strings when performance matters; test correctness and performance on realistic inputs or match smaller pieces.
- **P078** — Match POSIX extended regular expressions with '[[ =~ ]]' (0 match, 1 no match, 2 invalid regex), remembering it matches any substring unless anchored with '^' and '$', and that anchors and regex-special characters must be left unquoted.
- **P130** — Quote regular expressions and choose the dialect expected by the tool, using extended syntax, grouping, alternation, and repetition only so the shell and regex engine preserve the intended pattern.
- **P131** — Use tac, rev, comm, diff, and patch to inspect ordering, compare versions, review changes, and apply small text change sets.
- **P144** — Use sed for noninteractive stream editing with explicit commands, scripts, addresses, and print behavior appropriate to the selected lines.
- **P148** — Build sed commands from targeted addresses, ordered expressions, captures, and tested regexes rather than one opaque transformation.
- **P149** — Control xargs batching, placeholders, delimiters, tracing, and prompts according to the command shape and risk.

## Scripting Portability Style and Tooling

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

## Linux Command Line and System Operations

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
