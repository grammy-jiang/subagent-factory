---
name: bash-shell-scripting-evidence-notes
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
  authored_from_digest: 3d7d3d9a3b51995908807b71b0aa34d94da5ac099c5b65532f181d1d524fa33e
---

# Bash & Shell Scripting — Evidence Notes

How this package is grounded, and how to weigh a principle when advising.

## Sources and what each is authoritative for

All eleven sources are `distillation-only`: distillation is permitted, verbatim quotation is not. Paraphrase; never copy passages. When two sources conflict, defined behaviour (GNU Bash manual, POSIX) outranks style or convenience guidance.

- **GNU Bash Reference Manual** (`gnu-bash-reference-m-ece374b5`) — defined Bash behaviour — the authority for what a construct does.
- **POSIX Shell Command Language (IEEE Std 1003.1)** (`posix-shell-command-07b8d355`) — the portability baseline — what every POSIX sh must do.
- **Greg's Wiki — BashGuide** (`greg-bashguide-full-dd4e9d25`) — idiomatic, correctness-first Bash guidance.
- **Greg's Wiki — Bash Pitfalls** (`greg-bash-pitfalls-05f06662`) — catalogue of common shell defects and their fixes.
- **Google Shell Style Guide** (`google-shell-style-g-457d1113`) — style and readability conventions for shell at scale.
- **pure-bash-bible** (`pure-bash-bible-0a32f97f`) — pure-Bash idioms that avoid external processes.
- **OWASP — Command Injection (attack reference)** (`owasp-command-inject-a1edef21`) — the attack model for OS command injection.
- **OWASP — OS Command Injection Defense Cheat Sheet** (`owasp-os-command-inj-10824bdf`) — the defensive controls: avoid the shell, allowlist, least privilege.
- **Effective Shell** (`effective-shell-fc16a030`) — practical end-to-end shell workflows.
- **Linux Pocket Guide** (`linux-pocket-guide-2583cb6c`) — concise reference for everyday Linux commands.
- **The Linux Command Line** (`the-linux-command-li-c8604455`) — comprehensive command-line and light-sysadmin grounding.

## Reading a principle's strength

Each principle carries a `confidence` (high or medium) set at promotion time, and resolves to backing claims in `analysis/claims.jsonl` and evidence records in `evidence/evidence-records.yaml` (each with an `evidence_strength`, `support_level`, and `limitations`).

- **high** — official/defined behaviour or a classic, well-corroborated idiom; state it plainly.
- **medium** — a strong convention or single-source recommendation; state it with its caveat and the portability/version condition.

Never state a rule more strongly than its backing evidence, and always name the trade-off or portability caveat (POSIX vs Bash, shell version) with the advice.
