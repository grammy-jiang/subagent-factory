---
name: text-processing-and-regex-tools
kind: skill
status: ready
provenance:
  principles:
  - P010
  - P024
  - P026
  - P065
  - P066
  - P072
  - P078
  - P130
  - P131
  - P144
  - P148
  - P149
  claims:
  - C00968
  - C00969
  - C00970
  - C00971
  - C00972
  - C00973
  - C00974
  - C00975
  - C00976
  - C00977
  evidence:
  - E00415
  - E00416
  - E00417
  - E00418
  - E00419
  - E00420
  - E00421
  - E00422
  - E00423
  - E00424
  source_anchors:
  - fc16a0303ffc-c0010
  - 2583cb6ce003-c0005
  - c8604455f3d5-c0024
  - fc16a0303ffc-c0008
  - fc16a0303ffc-c0009
  - c8604455f3d5-c0022
  - c8604455f3d5-c0023
  - fc16a0303ffc-c0011
  - c8604455f3d5-c0026
  - ece374b583e8-c0003
  authored_from_digest: 2a228476f6f1f37b1a9cf6d298c051533d225a2e1c62845f8c74d693ff6a62e0
---

# Text Processing and Regex Tools

## Purpose

Choose and compose text tools — grep, sed, awk, sort, uniq, tr, diff/patch — by data shape, quote patterns, match the tool's regex dialect, and escalate to a language when a pipeline outgrows itself.

## When this applies

- When selecting a shell text-processing command.
- When manipulating line-oriented text.
- Preparing or inspecting line-oriented text.
- When authoring regexes for grep, sed, shell conditionals, or another tool.
- When a regex component must allow or forbid specific character forms.
- When regex output will drive validation, extraction, or replacement.
- Writing portable or precise regular expressions.
- When searching files, history, or stream output in a shared shell workflow.
- When basic inclusion, exclusion, and inspection solve the immediate text-filtering task.
- When searching text.
- When editing files or generating templates from shell transformations.
- Editing files directly with sed.

## Procedure

1. Describe the data shape — lines, fields, delimiters, size — and the transformation goal.
2. Choose the tool by fit: `grep` to filter, `sed` for line edits, `awk` for field and record logic, `sort`/`uniq`/`tr`/`cut` for set and column work, `diff`/`patch` for deltas (P024, P065, P066, P130).
3. Match the regex dialect to the tool (BRE vs ERE vs PCRE) and quote the pattern so the shell does not expand it first (P010, P072, P078, P131).
4. Confirm the pipeline handles its delimiters, NUL or newline characters embedded in data, and locale/collation correctly (P026, P144, P148).
5. Escalate to a language — an `awk` program or Python — when the pipeline grows fragile, stateful, or hard to read (P149).
6. Emit findings highest-risk first, each with the tool or regex hazard, the safer composition, and the caveat.

## Principles to apply

Each rule below is a promoted principle of this package; cite its ID in a finding.

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

## Review checklist

For the code under review, confirm each applicable principle holds; when one is violated, name the hazard, the failure it enables, the safer idiom, and the trade-off or portability caveat.

- [ ] (P010) Choose text inspection and transformation tools by data shape, composing narrow tools…
- [ ] (P024) Build regular expressions iteratively against valid and invalid examples, using anchors,…
- [ ] (P026) Use grep and its variants with quoted patterns and explicit options that match the needed…
- [ ] (P065) Use in-place sed only when rewriting the target file is intended; prefer writing…
- [ ] (P066) Sort and deduplicate with semantics that match the data, remembering uniq only removes…
- [ ] (P072) Avoid broad or complicated pattern and regex matching against long strings when…
- [ ] (P078) Match POSIX extended regular expressions with '[[ =~ ]]' (0 match, 1 no match, 2 invalid…
- [ ] (P130) Quote regular expressions and choose the dialect expected by the tool, using extended…
- [ ] (P131) Use tac, rev, comm, diff, and patch to inspect ordering, compare versions, review…
- [ ] (P144) Use sed for noninteractive stream editing with explicit commands, scripts, addresses, and…
- [ ] (P148) Build sed commands from targeted addresses, ordered expressions, captures, and tested…
- [ ] (P149) Control xargs batching, placeholders, delimiters, tracing, and prompts according to the…
