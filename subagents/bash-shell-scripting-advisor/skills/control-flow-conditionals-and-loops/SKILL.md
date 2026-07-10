---
name: control-flow-conditionals-and-loops
kind: skill
status: ready
provenance:
  principles:
  - P016
  - P017
  - P022
  - P027
  - P032
  - P042
  - P063
  - P070
  - P073
  - P101
  - P116
  - P132
  - P150
  claims:
  - C00076
  - C00077
  - C00214
  - C00218
  - C00320
  - C00512
  - C00513
  - C00514
  - C00357
  - C00358
  evidence:
  - E00031
  - E00032
  - E00090
  - E00093
  - E00153
  - E00239
  - E00240
  - E00241
  - E00174
  - E00175
  source_anchors:
  - 05f06662f2b0-c0000
  - dd4e9d2506fb-c0002
  - dd4e9d2506fb-c0006
  - ece374b583e8-c0005
  - ece374b583e8-c0000
  - fc16a0303ffc-c0014
  - 07b8d355a162-c0002
  - 05f06662f2b0-c0001
  - 07b8d355a162-c0000
  - fc16a0303ffc-c0015
  authored_from_digest: 07974f8b50fc01d00bab2b0a644b3980a130559ef10fc2471b514602bb2c2077
---

# Control Flow Conditionals and Loops

## Purpose

Pick the control-flow construct that matches the branching or iteration, and write `test`/`[[ ]]` conditions and loops that are correct for the operand type, glob results, and arithmetic involved.

## When this applies

- Combining test conditions
- Using the [ / test command
- When compact command chaining replaces an explicit if block.
- Chaining commands conditionally on success or failure
- Looping over a script's or function's arguments
- Forwarding or iterating over positional parameters
- When iterating over arrays, variables, globs, files, or generated values.
- Iterating over command-line arguments or generated file lists.
- Looping over files, command output, or positional parameters.
- When shell behavior depends on input, file state, shell type, or another condition.
- When writing shell conditionals and loops.
- When shell scripts perform simple numeric operations.

## Procedure

1. Read the target: which shell and version, and whether each operand is a string, an integer, a glob, or command output — the operand type drives every later choice.
2. For each condition, check the test form: string operators for strings, `-eq/-ne/-lt/-le/-gt/-ge` for integers (P132, P116); give each operator and operand as a separate argument with a closing `]`, quote operands (a one-argument test is true for any non-null string), and combine one primary per test with `&&`/`||` rather than the deprecated `-a`/`-o` (P016).
3. For each command chain, confirm the `&&`/`||` short-circuit intent is correct and is not standing in for a real if/then/else (P017; the if/then/else trap itself is owned by error-handling).
4. For each branch or loop, pick the construct that matches the model (P032, P070, P150): `if`/`elif`, `case` (patterns specific→catch-all, add a final `*`), `while`/`until`, or `for`; confirm the iteration source is a glob or positional list — not parsed `ls`/`$(...)` — and that `"$@"` is quoted (P022, P027).
5. For recursive file iteration prefer `find -exec … {} \;`/`{} +`, or `find -print0 | while IFS= read -r -d '' f`, or bash `globstar` (P073); for numeric logic use integer arithmetic with explicit base, truncation, and assignment-vs-equality semantics, escalating to `bc` only when precision demands (P042, P063); apply file-test primaries per their symlink-following semantics (P101).
6. Emit findings highest-risk first: name the hazard, the failure it enables, the safer construct, and the portability caveat; flag the anti-patterns below; end with the concrete rewrite.

## Principles to apply

Each rule below is a promoted principle of this package; cite its ID in a finding.

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

## Anti-patterns to flag

- A one-argument `[ $x = y ]` with an empty/unquoted operand — quote operands and give each as a separate argument.
- Using string operators for integers (or `-eq` for strings).
- A `case` with no catch-all `*` when unmatched input must be handled.

## Review checklist

For the code under review, confirm each applicable principle holds; when one is violated, name the hazard, the failure it enables, the safer idiom, and the trade-off or portability caveat.

- [ ] (P016) Write robust 'test'/'[' conditions: give each operator and operand as a separate argument…
- [ ] (P017) Use && and || for short-circuit control flow: after && the next command runs only if the…
- [ ] (P022) Prefer the double-quoted "$@" to preserve each positional parameter as its own field, and…
- [ ] (P027) Use traditional for loops over generated words, positional parameters, and glob results…
- [ ] (P032) Format shell control flow so keywords appear at valid command boundaries, and choose…
- [ ] (P042) Use shell arithmetic only for integer logic, being explicit about bases, division…
- [ ] (P063) Choose calculator tools by complexity: shell arithmetic or expr for simple expressions,…
- [ ] (P070) Order case patterns from specific to catch-all, add a final * default when unmatched…
- [ ] (P073) For recursive file iteration use `find -exec cmd {} \;`/`{} +` (portable), or in bash…
- [ ] (P101) Use the file-test primaries (-e exists, -f regular file, -d directory, -r/-w/-x…
- [ ] (P116) Choose comparison operators by operand type: string operators compare strings, while…
- [ ] (P132) Choose string, integer, regex, pattern, and arithmetic test forms according to the value…
- [ ] (P150) Choose the loop form that matches the problem: fixed ranges, numeric counters, unknown…
