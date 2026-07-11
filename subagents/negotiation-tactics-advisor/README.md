# negotiation-tactics-advisor

**Display name:** Tactical Negotiation Advisor
**Version:** 0.2.0
**Tier:** 2
**Status:** draft

## What this subagent does

Advises and coaches a negotiator preparing for or conducting a real negotiation —
business, salary, purchasing, or dispute — using the FBI-derived tactical-empathy
method developed by Chris Voss. Recommends specific techniques (mirroring, labeling,
accusation audit, calibrated How and What questions, Ackerman bargaining, Black Swan
discovery) matched to the caller's situation, with concrete example phrasings and the
tactical-empathy reasoning behind each choice.

## Modes

- **advise** — recommend a technique sequence and phrasings for an upcoming negotiation.
- **review** — critique a planned approach or script against the source's principles and
  failure modes (counterfeit Yes, deadline anxiety, neediness, Why questions).
- **compare** — weigh alternative moves and counterpart styles (No versus Yes; positive,
  negative, and normative leverage; the three negotiator styles).

## Primary source

Chris Voss and Tahl Raz, *Never Split the Difference: Negotiating As If Your Life
Depended On It* (HarperBusiness, 2016). Ingested as full primary book
(`voss-chris-never-spl-20260610132145`). Rights: distillation-only — no verbatim
passage reproduction permitted; no explicit open-licence notice on the authored work,
so the distillation-only floor applies. See `provenance-ledger.md`.

Corroborating source: EssentialInsight Summaries (2021) — retained for corroboration
only; the primary book governs all technique and principle decisions.

## Tier 2 — principles grounding

Ten principles (PRIN-001–PRIN-010) were derived via the Tier-1 evidence chain from 64
extracted claims (CL001–CL064) and 64 evidence records (EV001–EV064). All quality-bar
items, forbidden behaviours, mode outputs, and `always_on` items cite principle IDs.

## Required inputs

1. A description of the negotiation: goal, counterpart identity, their known desires
   and constraints, and the stage the conversation has reached.
2. Constraints shaping technique choice: price range, deadline, relationship history,
   medium, or behind-the-table players.

## Package layout

```
profile.yaml                          Canonical profile (v0.2.0, Tier 2)
provenance-ledger.md                  Distillation log and version history
CHANGELOG.md                          Version change log
principles/principles.yaml            PRIN-001–PRIN-010
evidence/evidence-records.yaml        EV001–EV064
analysis/claims.jsonl                 CL001–CL064
skills/
  labeling-and-accusation-audit/SKILL.md
  calibrated-questions-and-illusion-of-control/SKILL.md
  ackerman-bargaining-and-anchoring/SKILL.md
  black-swan-and-leverage-discovery/SKILL.md
references/
  tactical-empathy-toolkit.md
  negotiator-styles-and-voices.md
tests/
  golden-tests.yaml                   GT-001, GT-002, GT-003, MC-001
source-pack.manifest.yaml             Two sources: primary book + summary
```

## Status notes

`draft` — the four skills and two references listed in `profile.yaml
knowledge_partition` are currently stubs and must be fully authored before the package
is promoted out of draft. The canonical profile and tests are validated.

## Canonical source of truth

`subagents/negotiation-tactics-advisor/profile.yaml` is the single source of truth. The
installed Claude Code adapter under `.claude/agents/generated/` is a generated artifact —
do not edit it by hand.
