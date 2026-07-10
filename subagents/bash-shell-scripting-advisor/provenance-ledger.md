# Provenance Ledger — bash-shell-scripting-advisor

Every profile field traces to the distilled spine of this package: promoted principles in
`principles/principles.yaml` (each `derived_from_claims` resolves into `analysis/claims.jsonl`),
their evidence in `evidence/evidence-records.yaml`, and chunk anchors in
`sources/anchors/*.anchors.jsonl`. No profile value is an orphan.

## Sources

| source_id | title | rights_status |
|-----------|-------|---------------|
| gnu-bash-reference-m-ece374b5 | GNU Bash Reference Manual | distillation-only |
| posix-shell-command-07b8d355 | POSIX Shell Command Language (IEEE Std 1003.1) | distillation-only |
| greg-bashguide-full-dd4e9d25 | Greg's Wiki — BashGuide | distillation-only |
| greg-bash-pitfalls-05f06662 | Greg's Wiki — Bash Pitfalls | distillation-only |
| google-shell-style-g-457d1113 | Google Shell Style Guide | distillation-only |
| pure-bash-bible-0a32f97f | pure-bash-bible | distillation-only |
| owasp-command-inject-a1edef21 | OWASP — Command Injection (attack reference) | distillation-only |
| owasp-os-command-inj-10824bdf | OWASP — OS Command Injection Defense Cheat Sheet | distillation-only |
| effective-shell-fc16a030 | Effective Shell | distillation-only |
| linux-pocket-guide-2583cb6c | Linux Pocket Guide | distillation-only |
| the-linux-command-li-c8604455 | The Linux Command Line | distillation-only |

All sources are `distillation-only`: distillation is permitted; verbatim quotation is not. The
verbatim `sources/original` and `sources/markdown` layers are withheld from any rights-clean export
per `.claude/rules/rights-and-quotation-policy.md`.

## Field → grounding

Profile rules are grounded in promoted principles, cited by ID in each rule. The load-bearing map:

| Profile field | Grounded in principles |
|---------------|------------------------|
| role | P004, P006, P012, P053, P068, P108, P111, P121 (quoting, injection, fail-loud, scope) |
| quality_bar[0] (quoting / word-splitting / NUL-delimited) | P004, P007, P022, P068, P100, P135 |
| quality_bar[1] (fail loud) | P012, P076, P105, P112, P113, P085 |
| quality_bar[2] (injection surface) | P006, P071, P082, P086, P111, P121 |
| quality_bar[3] (portability / interpreter) | P013, P018, P022, P088 |
| quality_bar[4] (trade-off / no over-claim) | P053, P108, P086 |
| forbidden_behaviours | P004, P006, P013, P068, P082, P086, P105, P108, P111 |
| knowledge_partition.always_on | the ten skills below, covering all 150 principles |

## Skill partition → principles

Each skill in `skills/` groups a disjoint set of principles; together they cover all 150. The exact
map is `.build/authoring/partition.json` (generated). Summary:

| Skill | Principles |
|-------|------------|
| quoting-splitting-and-globbing | P004 P005 P007 P019 P020 P030 P068 P089 P090 P094 P098 P099 P100 P135 P014 |
| variables-parameters-and-expansion | P001 P015 P023 P035 P058 P064 P074 P075 P115 P117 P118 P127 |
| functions-arrays-and-structured-data | P011 P039 P055 P083 P084 P095 P106 P107 P133 P141 P146 |
| control-flow-conditionals-and-loops | P016 P017 P022 P027 P032 P042 P063 P070 P073 P101 P116 P132 P150 |
| io-redirection-pipelines-and-here-docs | P008 P018 P021 P050 P059 P077 P079 P088 P091 P097 P109 P110 P120 P136 P143 |
| error-handling-exit-status-and-traps | P012 P069 P076 P081 P085 P092 P096 P102 P105 P112 P113 P119 |
| shell-injection-and-least-privilege | P006 P031 P071 P082 P086 P087 P103 P111 P121 |
| text-processing-and-regex-tools | P010 P024 P026 P065 P066 P072 P078 P130 P131 P144 P148 P149 |
| scripting-portability-style-and-tooling | P002 P013 P025 P028 P038 P046 P047 P053 P056 P061 P093 P108 P114 P128 P140 P142 P147 |
| linux-command-line-and-system-operations | P003 P009 P029 P033 P034 P036 P037 P040 P041 P043 P044 P045 P048 P049 P051 P052 P054 P057 P060 P062 P067 P080 P104 P122 P123 P124 P125 P126 P129 P134 P137 P138 P139 P145 |

## Version History

### 1.0.0 — 2026-07-10

Initial LLM-authored layer (profile, faithfulness report, skills, references, tests, adapter) over the
deterministically-built distilled spine (150 principles, 3,614 claims, 1,789 evidence records, 11
sources). Distilled spine unchanged. No prior profile decisions superseded.
