---
name: platform-customization-matrix
kind: reference
status: ready
provenance:
  principles:
  - P021
  - P027
  - P028
  - P050
  - P071
  - P076
  - P078
  - P079
  - P081
  - P082
  - P097
  - P123
  - P125
  - P136
  - P137
  - P138
  - P139
  - P140
  claims:
  - C00826
  - C00829
  - C00830
  - C00841
  - C00858
  - C00860
  - C00861
  - C00801
  - C00802
  - C00823
  - C00834
  - C00836
  evidence:
  - E00374
  - E00376
  - E00377
  - E00383
  - E00390
  - E00391
  - E00392
  - E00358
  - E00359
  - E00373
  - E00381
  - E00382
  source_anchors:
  - 3d65b6e6bdb9-c0000
  - fe2afcdae0a6-c0000
  - 59f8ec5e7b03-c0000
  authored_from_digest: 49a616537678f1b8de66f438f8beb07bef717b57d245667568bd4bff9f00642f
---

# Reference: platform-customization-matrix

## Purpose

A lookup for the instruction- and customization-file mechanisms across agent platforms — where
guidance lives, how precedence and scope work, and which surfaces support what. Use it when
deciding where to put a rule so it applies at the right scope. Grounded in P027, P028, P050,
P071, P138.

## Where guidance lives, by platform

| Platform | Mechanism | Location / rule | Principle |
|----------|-----------|-----------------|-----------|
| Claude | `CLAUDE.md` | lean, broadly-applicable, non-obvious project context (bash commands, non-default style, test runners, etiquette, gotchas) | P079 |
| Codex | `AGENTS.md` | one or more files anywhere in the repo; the nearest in the directory tree wins | P028 |
| Codex | precedence | within a directory `AGENTS.override.md` > `AGENTS.md` > configured fallbacks; files nearer the working dir win | P021, P027 |
| Copilot | `copilot-instructions.md` | repository-wide file at `.github/copilot-instructions.md` | P050 |
| Copilot | scoped instructions | `.github/instructions/NAME.instructions.md`; scope to matching files via a `paths` frontmatter | P082, P124 |

## Choosing the scope level

Select the level to match the scope the guidance should apply over, rather than defaulting to one
[P138]:

- **Personal** — applies to you across projects.
- **Repository** — applies to everyone working in the repo; recommend always-on custom
  instructions when a team needs standards applied automatically across a scope [P139].
- **Organization** — applies across repos.

Put files closer to the working directory to take precedence; use the global file for
communication-style guidance [P027].

## Feature-trigger model (Copilot customization)

Match a feature to its trigger model [P071]: automatic features (custom instructions, agent
skills, hooks) fire without being asked; invoked features run on demand. Enforce behaviour that
must happen (or be blocked) deterministically with hooks and permissions rather than a prose
request [P078]. Avoid custom output styles unless a significant role change is required; prefer
the built-in styles [P125].

## IDE / surface support

Support differs by surface — verify against the feature-support matrix before promising a feature
works, and recommend the latest stable version [P076], [P081]. Keep instruction files non-empty
and within size caps (e.g. Codex skips empty files and stops at its `project_doc_max_bytes`
default) [P136].

## Maintenance & troubleshooting

- **Maintain as a feedback loop.** When the agent makes a repeated mistake, reads too many files,
  or you repeat PR feedback, add or correct the rule [P097].
- **Onboarding.** Keep cloud-agent-generated instructions under two pages and non-task-specific;
  run the onboarding task only when appropriate [P140].
- **Discovery failures.** When nothing loads, confirm the workspace root and that files are
  non-empty; when the wrong guidance appears, hunt for a nearer or higher-precedence file [P137].
- **Match specificity to fragility.** High-freedom prose when many approaches are valid;
  medium-freedom parameterized patterns when a shape must hold; strict rules for fragile steps
  [P123].

## Grounding

Principles: P021, P027, P028, P050, P071, P076, P078, P079, P081, P082, P097, P123, P125, P136,
P137, P138, P139, P140. Distillation-only: no verbatim source quotation.
