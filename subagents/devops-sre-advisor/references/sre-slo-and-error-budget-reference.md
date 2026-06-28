---
name: sre-slo-and-error-budget-reference
kind: reference
status: ready
provenance:
  principles:
  - P059
  - P026
  - P010
  - P011
  - P115
  - P128
  claims:
  - C00646
  - C00647
  - C00648
  - C01301
  - C01302
  - C01303
  - C00624
  - C01797
  - C00620
  - C00621
  - C00622
  - C01727
  evidence:
  - E00313
  - E00314
  - E00315
  - E00430
  - E00431
  - E00432
  - E00308
  - E00556
  - E00305
  - E00306
  - E00307
  - E00554
  source_anchors:
  - 9fe26df35c80-c0006
  - 9fe26df35c80-c0035
  - 9fe26df35c80-c0005
  - 0bea4daa68ab-c0005
  - 0bea4daa68ab-c0003
  authored_from_digest: 9a4eb58d1a2e56a5b43e0f22b46f0ad4d81ba21d7764ef201225825ca6ce21cd
---

# SRE SLO and error-budget reference

The reliability vocabulary and the chain that links it together. SRE is a concrete implementation of
DevOps that applies software-engineering methods to operations (CL045); reliability is managed to a
chosen objective, not to perfection (CL046).

## Core terms

| Term | Definition | Key property |
|------|------------|--------------|
| SLI — Service Level Indicator | A measured signal of service behaviour as users experience it | Reflects user-facing experience; expressed as percentiles over a window, not single averages (CL050) |
| SLO — Service Level Objective | An explicit target on an SLI the team agrees is "reliable enough" | A deliberate choice below 100%; 100% is the wrong target because it forbids value-delivering change and risk (CL046) |
| Error budget | The amount of unreliability the service may spend, derived from the SLO | Turns the dev-vs-ops reliability argument into a shared, data-driven decision (CL048) |
| Error-budget policy | The agreed rule for what happens when the budget is exhausted | Slows or halts feature releases and redirects effort to reliability until back within objective (CL049) |
| Burn rate | How fast the service is consuming its error budget | Drives alerting via multiple windows — catch real problems early, limit false pages (CL051) |

## SLI categories (choose what users feel)

| Category | Captures |
|----------|----------|
| Availability | Whether requests succeed |
| Latency | Whether requests are fast enough |
| Correctness / quality | Whether responses are right |

Targets are stated as percentiles over a defined window so tail pain is not hidden by an average
(CL050).

## The reliability chain (use as a readiness checklist)

1. **User-facing SLIs** chosen (availability / latency / correctness).
2. **Explicit SLO** set on each SLI (a percentile target over a window).
3. **Error budget** derived from the SLO (CL048).
4. **Written error-budget policy** stating what happens when the budget is spent (CL049).
5. **Symptom + burn-rate alerting** rather than per-cause alerting (CL051).
6. **Sustainable on-call** — persistently high pager volume is treated as systemic reliability debt
   to engineer away, not heroics (CL052).

A missing link is a gap to close. A 100% target, or an absent error-budget policy, is a defect — not
a conservative choice.

## Why the shared budget aligns dev and ops

The error budget is a neutral, data-driven arbiter: a feature team that spends the budget through
outages owns the reliability cost, creating mutual accountability between development and SRE
(CL060).

## Provenance

Derived from principles P002 and P008 (claims CL045, CL046, CL048, CL049, CL050, CL051, CL052,
CL060; evidence EV045, EV046, EV048, EV049, EV050, EV051, EV052, EV060) in `comp500-15893c30` (The
Site Reliability Workbook; distillation-only — paraphrase, no verbatim quotation). Expert SRE
practice; specific numeric SLO targets and burn-rate windows are the team's to set against current
service data.
