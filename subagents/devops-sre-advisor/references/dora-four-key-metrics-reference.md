---
name: dora-four-key-metrics-reference
kind: reference
status: ready
provenance:
  principles:
  - P036
  - P056
  - P067
  - P105
  - P003
  - P004
  claims:
  - C00037
  - C00038
  - C00039
  - C00040
  - C00041
  - C00044
  - C00045
  - C00046
  - C00047
  - C00064
  - C00031
  - C00032
  evidence:
  - E00022
  - E00023
  - E00024
  - E00025
  - E00026
  - E00029
  - E00030
  - E00031
  - E00032
  - E00043
  - E00016
  - E00017
  source_anchors:
  - 9d4b1cf206e5-c0002
  - 9d4b1cf206e5-c0003
  - 9d4b1cf206e5-c0001
  authored_from_digest: 16cd9e421e52c53210fd92811298cebad55b3c2ef988b3557a0cd741a6aaddfc
---

# DORA four key metrics reference

The four key metrics for software delivery performance, two per dimension. Throughput and stability
are measured **together**; the research finds high performers achieve both, with no trade-off
between delivery speed and reliability (CL016, CL017).

## The four metrics

| Metric | Dimension | What it measures | Improvement levers (sibling skill) |
|--------|-----------|------------------|-------------------------------------|
| Deployment frequency | Throughput | How often the team successfully releases to production | Small batches, trunk-based work, automated pipeline (`designing-deployment-pipelines`) |
| Lead time for changes | Throughput | Time from code committed to code running in production | Reduce batch size, automate the pipeline, cut handoffs (`designing-deployment-pipelines`) |
| Change failure rate | Stability | Share of changes to production that require remediation (rollback, hotfix, patch) | Progressive delivery, fail-fast automated tests, tested rollback (`planning-progressive-delivery`) |
| Time to restore service | Stability | How long it takes to recover from a failure in production | Symptom/burn-rate alerting, sustainable on-call, fast rollback (`defining-slos-and-error-budgets`, `reducing-toil-and-on-call-load`) |

## How to read them

- **Two dimensions, read as one verdict.** Deployment frequency and lead time describe *throughput*;
  change failure rate and time to restore describe *stability*. State both in any assessment.
- **No trade-off.** Do not treat a gain in one dimension as a justification for a loss in the other.
  The evidence shows the highest performers are superior on throughput *and* stability at the same
  time (CL017). Recommending one at the expense of the other contradicts the source.
- **Performance clusters into bands.** The research groups organisations into performance bands
  (from lowest to highest) on these metrics. The specific numeric thresholds for each band are
  revised in successive State of DevOps reports — consult the current report for exact figures
  rather than relying on fixed numbers here.
- **It predicts outcomes.** Software delivery performance statistically predicts organisational
  outcomes — profitability, productivity, and market share — making it a competitive capability,
  not merely an IT concern (CL018). This is a correlational finding; present it as predictive, not
  guaranteed.

## What does not belong on this scorecard

Activity proxies — story points, raw commit or ticket counts, utilisation — measure busyness, not
delivery performance, and are not substitutes for the four metrics.

## Provenance

Derived from principle P001 (claims CL016, CL017, CL018; evidence EV016–EV018) in
`accelerate-the-scien-7241289b` (distillation-only — paraphrase, no verbatim quotation). The metrics
and the no-trade-off result are correlational findings of the State of DevOps survey program; exact
band thresholds are intentionally not reproduced here because they change across report years.
