---
name: skill-format-and-frontmatter-reference
kind: reference
status: ready
provenance:
  principles:
  - P025
  - P032
  - P034
  - P037
  - P040
  - P048
  - P055
  - P092
  - P112
  - P120
  - P122
  - P124
  - P135
  - P150
  claims:
  - C00187
  - C00198
  - C00879
  - C00880
  - C00881
  - C00903
  - C00089
  - C01641
  - C01642
  - C01643
  - C01644
  - C00588
  evidence:
  - E00099
  - E00104
  - E00398
  - E00399
  - E00400
  - E00412
  - E00064
  - E00692
  - E00693
  - E00694
  - E00695
  - E00258
  source_anchors:
  - a86591486b37-c0000
  - c86c41e74ac0-c0000
  - 50982633050d-c0000
  - 9d770de8f1b0-c0000
  - 2b076b2b50c8-c0000
  authored_from_digest: e954bed19b589adc550296ca470461b9ac79f84513b8d2f05775ff083dcbae99
---

# Reference: skill-format-and-frontmatter-reference

## Purpose

The exact structural and frontmatter rules for a valid Agent Skill — folder shape, entry file,
the `name`/`description` contract, tool grants, and invocation visibility. Use this as a lookup
when authoring or reviewing a `SKILL.md`. Grounded in P025, P032, P034, P092, P112, P135, P150.

## Folder & entry-file shape

| Element | Rule | Principle |
|---------|------|-----------|
| Folder name | kebab-case; one skill per folder | P120, P135 |
| Entry file | exactly `SKILL.md` at the folder root | P003, P115, P120 |
| Contents | self-contained: instructions + optional scripts, references, assets beside it | P003, P115 |
| `README.md` | kept outside the skill folder, not the entry file | P120 |
| Paths | always forward-slash, for cross-platform portability | P055 |

## Required frontmatter

A `SKILL.md` opens with a YAML frontmatter block (delimited by `---`) that the agent pre-loads at
startup for discovery [P112], [P135]:

| Field | Requirement | Principle |
|-------|-------------|-----------|
| `name` | lowercase letters, numbers, hyphens; 1–64 chars; no leading/trailing hyphen; no consecutive hyphens; no slashes/colons/dots/namespace prefixes; no XML tags or reserved words; typically matches the directory | P025, P032, P034, P040, P092, P150 |
| `description` | states what the skill does **and** when to use it; front-loads the primary use case and trigger words; precise enough for automatic loading | P025, P070, P150 |

The `name` + `description` are the always-loaded metadata; the agent reads the full body only
after a description match, so the description is the primary triggering signal [P002], [P150].

## Optional frontmatter

| Field | Purpose | Principle |
|-------|---------|-----------|
| allowed-tools | pre-approve tools the skill needs, avoiding a per-use confirmation prompt; a tool omitted from all grants is unavailable | P048 |
| user-invocable / disable-model-invocation | set invocation visibility: auto-load, user-only, or model-only; omit both for a slash command that also auto-loads | P037 |
| `paths` (scoped rules) | scope a rule to matching files; leave unscoped only when it truly must apply everywhere | P124 |

## Validity checklist

- [ ] Folder is kebab-case; entry file is exactly `SKILL.md` [P120].
- [ ] `name` obeys the character/length rules above [P032], [P034].
- [ ] `description` says what + when, with trigger words [P025], [P150].
- [ ] Only documented frontmatter fields are used — no invented fields.
- [ ] Tools the skill uses are granted via allowed-tools [P048].
- [ ] Invocation visibility is set intentionally [P037]; visibility managed via settings [P122].

## Grounding

Principles: P025, P032, P034, P037, P040, P048, P055, P092, P112, P120, P122, P124, P135, P150.
Distillation-only: no verbatim source quotation.
