---
name: functions-arrays-and-structured-data
kind: skill
status: ready
provenance:
  principles:
  - P011
  - P039
  - P055
  - P083
  - P084
  - P095
  - P106
  - P107
  - P133
  - P141
  - P146
  claims:
  - C00505
  - C00506
  - C01228
  - C01229
  - C01230
  - C01231
  - C03459
  - C03460
  - C03461
  - C03462
  evidence:
  - E00237
  - E00238
  - E00599
  - E00600
  - E00601
  - E00602
  - E01708
  - E01709
  - E01710
  - E01711
  source_anchors:
  - ece374b583e8-c0005
  - fc16a0303ffc-c0017
  - c8604455f3d5-c0033
  - c8604455f3d5-c0034
  - 0a32f97f8de3-c0000
  - c8604455f3d5-c0035
  - ece374b583e8-c0006
  - c8604455f3d5-c0031
  - dd4e9d2506fb-c0001
  - dd4e9d2506fb-c0004
  authored_from_digest: 522a350a6cc8d15c32996ff5221f051c26a54dcbe5c4d5dfe6fbd8e99b782839
---

# Functions Arrays and Structured Data

## Purpose

Model multi-value and keyed state in the shell with arrays, associative arrays, `local`, and namerefs — and recognise when the data modelling has outgrown the shell.

## When this applies

- When a script accepts flags or option arguments.
- Adding options to shell scripts.
- The data is already available as shell arguments or a Bash array.
- Managing lists or counters in bash scripts.
- Reading keyboard, file, or delimited input into shell variables.
- You need string-keyed maps
- Printing associative-array values or keys.
- Forwarding arguments through functions or wrapper scripts.
- Defining or reviewing shell functions
- Arrays may be sparse or must be matched by index
- Factoring code into functions
- When a script repeats a command group or needs reusable behavior.

## Procedure

1. Identify the state being modelled — multiple values, key→value pairs, or per-call locals — and the target shell, since indexed/associative arrays and namerefs are Bash, not POSIX sh (P133).
2. Choose the container: an indexed array for ordered lists, an associative array for keyed data, quoting `"${arr[@]}"` and `"${!arr[@]}"` on every expansion so elements are not word-split (P083, P084, P106).
3. Scope function-local state with `local` (and `local -n` namerefs used deliberately) so values do not leak between calls or into the global namespace (P011, P055).
4. Confirm values containing spaces or newlines survive assignment, parameter passing, and iteration intact (P095, P107, P141).
5. Judge whether the data has outgrown the shell — nested or relational structure, quoting that fights you — and if so recommend a stronger language (P146; the escalation boundary is shared with scripting-portability-style-and-tooling).
6. Emit findings highest-risk first, each with the hazard, the safer modelling, and the portability caveat.

## Principles to apply

Each rule below is a promoted principle of this package; cite its ID in a finding.

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

## Review checklist

For the code under review, confirm each applicable principle holds; when one is violated, name the hazard, the failure it enables, the safer idiom, and the trade-off or portability caveat.

- [ ] (P011) Parse options with 'getopts optstring name' (which sets name, OPTIND, and OPTARG), always…
- [ ] (P039) Use Bash arrays for multi-value state in Bash-compatible scripts, accounting for…
- [ ] (P055) Control 'read' with its options: -a to fill an array, -d for a custom delimiter, -n/-N…
- [ ] (P083) Use associative arrays only when unordered key/value storage is acceptable; preserve…
- [ ] (P084) Inside functions, use the function positional parameters, FUNCNAME, and quoted argument…
- [ ] (P095) Define shell functions with valid names and compound-command bodies, knowing calls run…
- [ ] (P106) Loop over an array's indices with "${!arr[@]}" when you must correlate parallel arrays by…
- [ ] (P107) Use functions to isolate and reuse code, but in moderation (too many scattered functions…
- [ ] (P133) Write shell functions as named reusable blocks with local variables and named parameters…
- [ ] (P141) Use arrays and parameter expansion for simple structured shell data, but switch languages…
- [ ] (P146) Use array-to-pipeline transformations, unset semantics, and associative arrays to sort,…
