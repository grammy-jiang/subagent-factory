# Advertising Effectiveness Advisor

Generated subagent package. Critiques and guides advertising and marketing
decisions so that every dollar of spend is held accountable to selling — not to
brand awareness, differentiation, or creative acclaim for their own sake.

## Source

- **The End of Advertising As We Know It** — Sergio Zyman with Armin Brott
  (John Wiley & Sons, 2002, ISBN 0-471-22581-9)
- Rights: `distillation-only` (all rights reserved; no verbatim quotation)

## Modes

- `advise` — recommend how to spend so the spend sells
- `review` — critique an existing campaign or strategy against selling
- `compare` — rank bounded either/or marketing decisions by selling return
- `validate` — gate a spend against a measurable selling criterion

## Canonical artifact

`profile.yaml` is the single source of truth. Do not edit the installed adapter
at `.claude/agents/generated/advertising-effectiveness-advisor.md` by hand;
re-export from the profile instead.

## Status

`draft` — skills and references remain stubs until authored. See
`profile.yaml` `knowledge_partition` for the list.
