---
name: variables-parameters-and-expansion
kind: skill
status: ready
provenance:
  principles:
  - P001
  - P015
  - P023
  - P035
  - P064
  - P074
  - P075
  - P115
  - P117
  - P118
  - P127
  - P058
  claims:
  - C00182
  - C00273
  - C00275
  - C00276
  - C00472
  - C00476
  - C00504
  - C01777
  - C01778
  - C01779
  evidence:
  - E00070
  - E00120
  - E00121
  - E00122
  - E00221
  - E00222
  - E00236
  - E00873
  - E00874
  - E00875
  source_anchors:
  - dd4e9d2506fb-c0001
  - dd4e9d2506fb-c0004
  - ece374b583e8-c0003
  - ece374b583e8-c0005
  - 07b8d355a162-c0002
  - 2583cb6ce003-c0001
  - c8604455f3d5-c0014
  - c8604455f3d5-c0015
  - 457d111305bf-c0001
  - dd4e9d2506fb-c0003
  authored_from_digest: 8a9490b99a1d4ab80cebd219efd1c448b8319cafac22d6aed084134175d926df
---

# Variables Parameters and Expansion

## Purpose

Handle shell variables, positional/special parameters, and parameter expansion with explicit scope and correct quoting, so a script never leaks state between functions, mangles values with spaces, or misreads its arguments.

## When this applies

- Passing data via the environment
- Prefixing VAR=value to a command and reasoning about whether it persists
- When configuring commands through environment variables.
- Configuring environment for commands or child processes.
- Writing a shell function
- Removing a single element from an array
- Removing a function or variable
- When the transformation is simple and shell-native.
- Manipulating shell parameters safely.
- Assigning a variable
- Creating shell variables or constants.
- The desired transformation matches Bash parameter-expansion or glob-pattern semantics.

## Procedure

1. Identify each variable's scope and lifetime, and whether its value may contain spaces, newlines, or glob characters.
2. Check assignment-prefix scope (P001): `VAR=value cmd` exports the variable only for that command before an ordinary utility but persists before a special built-in; assigning to a readonly variable is an error.
3. Confirm parameter expansions are quoted and use the right form for the intended effect — defaults `${x:-…}`, alternatives `${x:+…}`, length/substring, and pattern removal `${x#…}`/`${x%…}`/`${x//…}` (P015, P023, P074, P075, P115).
4. Read positional and special parameters with their exact meaning: `"$@"` vs `"$*"`, `$#`, `$0`, `$$`, `$!`, `$?` (P035, P117, P118, P127).
5. Keep state from leaking between functions by scoping with `local` (the boundary is shared with functions-arrays-and-structured-data) (P058, P064).
6. Emit findings highest-risk first, each with the expansion hazard, the safer form, and the caveat.

## Principles to apply

Each rule below is a promoted principle of this package; cite its ID in a finding.

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

## Review checklist

For the code under review, confirm each applicable principle holds; when one is violated, name the hazard, the failure it enables, the safer idiom, and the trade-off or portability caveat.

- [ ] (P001) Know that a variable assignment prefixed to a command scopes differently by target:…
- [ ] (P015) Declare function-private variables with 'local', and account for Bash's dynamic scoping:…
- [ ] (P023) Remove functions and variables with unset, disambiguating with -f (function) or -v…
- [ ] (P035) Use parameter expansion with quoting and braces for required values, alternates,…
- [ ] (P064) Assign shell variables without surrounding spaces, quote values containing spaces, and…
- [ ] (P074) Use special parameters for runtime state such as the last status, background PID,…
- [ ] (P075) Prefer Bash parameter expansion for routine string length, trimming, removal, case…
- [ ] (P115) Wrap a parameter name in braces (${name}) whenever the expansion is immediately followed…
- [ ] (P117) Use set -a (allexport) sparingly and know its scoping: it gives the export attribute to…
- [ ] (P118) Create a nameref with 'declare -n ref=name' to operate indirectly on another variable,…
- [ ] (P127) Manage shell variables, exports, quoting, and braces deliberately to prevent unintended…
- [ ] (P058) Validate and report script arguments with positional parameters, argument counts, brace…
