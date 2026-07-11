# employee-payment-scheme-advisor

**Version:** 0.3.0
**Status:** draft (skill/reference bodies need re-authoring against Docling anchors)

## Purpose

Advises managers on the participative design and implementation of employee incentive
payment and reward schemes, on the basis of *Payment Systems and Performance Improvement:
Participation in Payment System Design* (Bowey & Thorpe, 1989, *Employee Relations*). The
central message: an incentive scheme succeeds chiefly through consulting and involving
employees in designing and running it, not through the technical structure of the scheme.

This is an employee-relations / reward-management advisor. It is **not** about technical or
financial payment-processing systems, despite the source file's `System Design/` folder.

## Modes

- `advise` — how to design, install, and run a scheme through participation.
- `review` — diagnose why an existing scheme underperformed (weak consultation, missing
  controls, subversion, policy decay).
- `validate` — check a proposed or existing scheme against the source's success criteria.

## Required inputs

- A description of the payment or incentive scheme (purpose and current/proposed form).
- Organisation context: staff levels and sections affected, how their work is
  interdependent, and the productivity outcome the scheme is meant to improve.

## What you get

A reasoned set of evidence-grounded recommendations and guidelines, naming the
participative actions to take, the failure modes to avoid, and the link between
participation, productivity, and reward. The responsible managers own the final decision.

## Source

| Title | Author | Year | Rights |
|-------|--------|------|--------|
| Payment Systems and Performance Improvement: Participation in Payment System Design | Bowey, Angela; Thorpe, Richard | 1989 | distillation-only |

Converted with Docling (2026-06-12); 19 heading anchors (h0000–h0018).

## Package layout

```
subagents/employee-payment-scheme-advisor/
  profile.yaml                    canonical profile (source of truth)
  provenance-ledger.md            field-by-field derivation log
  CHANGELOG.md                    version history
  README.md                       this file
  tests/golden-tests.yaml         routing and output tests
  source-pack.manifest.yaml       ingested source metadata
  sources/                        ingested source files
  skills/                         skill bodies (need re-authoring against Docling anchors)
  references/                     reference bodies (need re-authoring against Docling anchors)
```

## Status

Package is `status: draft`. Skill and reference bodies were authored at 0.2.0 against the
old empty-anchor MarkItDown conversion. They need re-authoring against the Docling anchors
(h0005–h0018) before the package returns to `status: ready`.
