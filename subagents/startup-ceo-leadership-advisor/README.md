# startup-ceo-leadership-advisor

**Display name:** Startup CEO Leadership Advisor
**Version:** 0.1.0
**Status:** draft

## Purpose

Advises founder-CEOs on the hardest people and management decisions in
building a high-tech company — covering crisis leadership, layoffs, executive
hiring and separation, org design, culture, and wartime vs peacetime modes —
by surfacing experience-grounded principles and stepwise frameworks where no
universal recipe exists.

## Source

- **The Hard Thing About Hard Things** — Ben Horowitz, HarperBusiness
- Rights: distillation-only (copyrighted work; no verbatim quotation permitted)
- Volatility: low; review cadence: annual

## Modes

| Mode | Trigger |
|------|---------|
| advise | CEO describes a hard management decision and asks for guidance |
| produce | CEO needs a concrete written artifact (layoff message, firing structure, process design) |
| compare | CEO needs a structured contrast of two management approaches or candidate profiles |

## When to use

- CEO is in the Struggle (existential crisis, cash low, confidence failing)
- CEO must conduct a layoff while preserving culture and trust
- CEO must fire or demote a senior executive
- Company is experiencing political behavior requiring process intervention
- CEO must hire a senior executive for an unfamiliar role
- CEO needs to calibrate peacetime vs wartime management mode

## When NOT to use

- Product strategy, engineering architecture, or technical decisions
- Fundraising tactics, term sheet negotiation, or investor relations strategy
- Consumer market analysis, competitive intelligence, or go-to-market strategy

## Package contents

```
subagents/startup-ceo-leadership-advisor/
  profile.yaml                  — canonical profile (source of truth)
  provenance-ledger.md          — full distillation log
  CHANGELOG.md                  — version history
  README.md                     — this file
  interrogation-records.yaml    — source interrogation Q1–Q18
  source-pack.manifest.yaml     — source pack manifest
  tests/
    golden-tests.yaml           — routing and quality tests
  sources/
    metadata/                   — source metadata JSON
    markdown/                   — converted source text
    original/                   — original source PDF
  skills/                       — skill files (to be generated)
  references/                   — reference files (to be generated)
```

## Validation

```bash
python -m tools.subagent_factory.validate_generated_package subagents/startup-ceo-leadership-advisor
```
