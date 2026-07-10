---
name: quoting-splitting-and-globbing
kind: skill
status: ready
provenance:
  principles:
  - P004
  - P005
  - P007
  - P019
  - P020
  - P030
  - P068
  - P089
  - P090
  - P094
  - P098
  - P099
  - P100
  - P135
  - P014
  claims:
  - C00027
  - C00057
  - C00067
  - C00071
  - C00074
  - C00075
  - C00091
  - C00150
  - C00151
  - C00152
  evidence:
  - E00001
  - E00013
  - E00023
  - E00027
  - E00029
  - E00030
  - E00039
  - E00054
  - E00055
  - E00056
  source_anchors:
  - 457d111305bf-c0000
  - 05f06662f2b0-c0000
  - dd4e9d2506fb-c0000
  - dd4e9d2506fb-c0002
  - dd4e9d2506fb-c0006
  - c8604455f3d5-c0011
  - ece374b583e8-c0000
  - 07b8d355a162-c0000
  - 2583cb6ce003-c0002
  - ece374b583e8-c0003
  authored_from_digest: a32e8bc6b976a37167d69d2ae87ce448c9a48c7d205bfec0f47442a976fc9b2a
---

# Quoting Splitting and Globbing

## Purpose

Catch the shell's number-one class of data-dependent bugs: expansions that word-split or glob-expand because they were left unquoted, and filename lists built by parsing `ls` or command output. This is the first correctness layer of any script that touches filenames, arguments, or arbitrary data.

## When this applies

- Expanding a variable or command substitution that will be used as data, a filename, or an argument
- Any parameter expansion or command substitution
- A value may contain whitespace or special characters
- Writing commands that include user data, filenames, or generated output.
- A value or argument may contain shell metacharacters, whitespace, or globbing characters
- When arguments contain whitespace, variables, metacharacters, or control characters.
- You intentionally rely on splitting an unquoted expansion
- When variables or command output become command arguments.
- An expansion result may contain IFS characters and must remain a single field
- Piping filenames to another command, or running a shell per found file
- Parsing a stream of filenames into elements
- When passing filesystem paths from find to another command.

## Procedure

1. Scan every expansion used as data — `$var`, `$(cmd)`, `${arr[@]}`, arithmetic results — and confirm it is double-quoted; unquoted, it undergoes word splitting on `$IFS` and pathname (glob) expansion (P004, P007, P135).
2. Flag any filename list built by parsing `ls` or iterating `$(ls)`/`$(find)`: command substitution provides no safe delimiter (P068, P100); require a glob or a NUL-delimited `find -print0 | while IFS= read -r -d '' f`.
3. For an operand that must stay literal, confirm the glob or regex is quoted, or `set -f` disables globbing (P089, P090, P098, P099).
4. Verify the few contexts where quoting is genuinely unnecessary (e.g. an RHS in `[[ ]]`, a bare assignment) are understood rather than guessed (P005, P019, P020).
5. Treat this as the first correctness pass — resolve quoting and splitting before reviewing deeper logic.
6. Emit findings highest-risk first, each naming the unquoted expansion, the data-dependent failure it enables, the quoted or NUL-delimited fix, and the caveat.

## Principles to apply

Each rule below is a promoted principle of this package; cite its ID in a finding.

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

## Anti-patterns to flag

- Unquoted `$var`, `$(cmd)`, or `${arr[@]}` used as data — word-splits and globs on whitespace/special chars.
- `for f in $(ls)` or `for f in $(find ...)` — command substitution gives no safe delimiter; use a glob or `-print0`.
- An unquoted glob or regex operand that must be literal — quote it or use `set -f`.

## Review checklist

For the code under review, confirm each applicable principle holds; when one is violated, name the hazard, the failure it enables, the safer idiom, and the trade-off or portability caveat.

- [ ] (P004) Double-quote every parameter expansion and command substitution used as data (filenames,…
- [ ] (P005) Quote every character that has special meaning to the shell when it must be literal, and…
- [ ] (P007) Double-quote expansions to control field splitting: only the unquoted results of…
- [ ] (P019) Move filenames between tools NUL-delimited: `find -print0 | xargs -0`, `printf '%s\0'`,…
- [ ] (P020) Quoting changes matching semantics: in `[[ ]]` the RHS of `=`/`==` is a glob pattern…
- [ ] (P030) Quote find patterns and compose tests, grouping, and logical operators so the shell does…
- [ ] (P068) Never build a filename list by iterating command output (`for f in $(ls)`/`$(find)`) or…
- [ ] (P089) Treat tilde expansion as dependent on the user database and HOME: a bare tilde expands to…
- [ ] (P090) Call `tr` without bracket ranges — `tr A-Z a-z` (the brackets in `tr [A-Z] [a-z]` are…
- [ ] (P094) Generate strings textually with brace expansion ('{a,b,c}' or '{x..y..incr}') before any…
- [ ] (P098) Stop filenames that begin with `-` from being read as options: prefix expansions with…
- [ ] (P099) Quote filename patterns that must be literal (or use 'set -f'), and enable 'nullglob' or…
- [ ] (P100) Treat command-substitution output as untrusted for splitting: null bytes in the output…
- [ ] (P135) Remember that shell expansions happen before command execution, so commands receive…
- [ ] (P014) Protect dash-leading operands from option parsing by using --, ./ prefixes, quoting,…
