---
name: monitoring-and-observability-for-scale
kind: skill
status: ready
provenance:
  principles: [P033, P050, P030, P029, P013]
  claims: [C00179, C00180, C00485, C00486, C00474, C00481, C00245]
  evidence: [E00149, E00150, E00242, E00243, E00237, E00240, E00184]
  source_anchors: [67c60e378753-c0004, a6c7e769c072-c0001, a6c7e769c072-c0005, a6c7e769c072-c0006]
---

# Design for observability: monitor from business metrics, set up before problems

## Purpose

Make problems visible before customers feel them: design applications to be monitored, instrument
business metrics first, stand up metric collection ahead of need, and turn the real-time log stream
into business-level monitors.

## When to use

- A team is adding or changing modules, or instrumenting a new service.
- Monitoring exists but cannot answer "is there a problem?" — only low-level resource graphs.
- Logs are batch-shipped or siloed, with no real-time view across the cluster.

Do not invoke to choose a specific monitoring product (out of scope) or to write the agents/exporters
(hand off).

## Procedure

1. **Design applications to be monitored (P033).** Drive monitoring from business metrics first
   ("Is there a problem?"), then "Where?", then "What?". Add the hooks as modules are written, not
   after.
2. **Set up collection before problems occur (P050).** Stand up metric collection and visualization
   ahead of need, define each metric precisely, and graph the right breakdown so anomalies are
   obvious at a glance.
3. **Deliver logs reliably in real time (P029).** Stream all logs over a publish/subscribe substrate
   with reliable delivery, and separate logging roles (publish, journal, analyze) so each scales
   independently.
4. **Turn the log stream into business monitors (P030).** Build real-time business-level monitors and
   your own cluster tooling from the stream; correlate technical and business metrics to spot a
   forming problem early.
5. **Require capable monitoring features (P013).** Demand automatic escalation, a service-dependency
   graph that suppresses downstream alert storms, maintenance windows and event acknowledgment
   (instead of disabling monitors), and scheduling by cost and volatility.
6. **State the trade-off.** Designed-in observability buys early detection and faster diagnosis at the
   cost of instrumentation effort, telemetry volume, and pipeline upkeep. Name it.

## Inputs

- What the monitoring can currently answer, which business metrics matter, how logs are delivered,
  and where instrumentation is missing.

## Output

An observability recommendation naming the business metrics to instrument, the collection to stand
up first, the log-delivery fix, and the telemetry cost accepted.

## References

- [Scalability Rules index](../../references/scalability-rules-index.md)

## Provenance

Distilled from principles **P033/P050/P030/P029/P013** and their claims/evidence, anchored in
`sources/anchors/`. Sources are `distillation-only`: paraphrased, never quoted verbatim.
