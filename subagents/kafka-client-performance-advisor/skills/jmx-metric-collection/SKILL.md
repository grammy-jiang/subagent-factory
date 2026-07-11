---
name: jmx-metric-collection
kind: skill
status: ready
provenance:
  principles: []
  claims: []
  source_anchors:
  - kafka-best-practices-20260608223304-t0271
  - kafka-best-practices-20260608223304-t0350
  - kafka-best-practices-20260608223304-t0070
  - optimizing-your-apac-20260608224518-t0767
  - optimizing-your-apac-20260608224518-t0275
  - optimizing-your-apac-20260608224518-t0617
---

# JMX metric collection

## Purpose

Read the client-side JMX metrics that confirm whether a producer or consumer is
healthy and whether a configuration change had its intended effect. The source draws a
hard line: the Confluent Cloud Metrics API returns server-side cluster metrics only and
cannot return client-side metrics — for those you must scrape client JMX. Every
configuration recommendation in this package is paired with the metric that verifies it,
and this skill is how that verification is collected.

## When to use

- Verifying that a tuning change moved the metric it was meant to move.
- Diagnosing broker throttling (produce/fetch throttle time greater than zero).
- Detecting that a consumer group is falling behind (rising consumer lag).
- Deciding whether a producer is I/O-thread bound versus user-processing bound.

## Procedure

1. **Pick the side that owns the metric.** Client-side health → client JMX. Topic- or
   cluster-level byte throughput and retained bytes → Confluent Cloud Metrics API. Do
   not expect the Metrics API to expose client-side numbers.
2. **Enable JMX on the client JVM** and point a collector (JConsole, a JMX exporter, or
   your APM agent) at the producer / consumer process.
3. **Collect the throttling metrics first.** For producers read
   `produce-throttle-time-avg` and `produce-throttle-time-max`; for consumers read
   `fetch-throttle-time-avg` and `fetch-throttle-time-max`. A value above zero means the
   broker is throttling the client against a quota — optimise the client for throughput
   or escalate to upgrade the cluster tier.
4. **Collect consumer lag.** Read `records-lag-max` (max lag in records over any
   partition in the window). A value that trends upward over time is the primary signal
   that the consumer group is not keeping pace with producers.
5. **Attribute producer time.** Read `io-ratio` (fraction of time the I/O thread spent
   doing I/O) and `io-wait-ratio` (fraction waiting). When both are low, user-processing
   time is high and is keeping the single producer I/O thread busy — investigate
   callbacks and other non-blocking code on that thread.
6. **Cross-check at the cluster level** with the Metrics API for bytes produced/consumed
   per minute by topic and max retained bytes, which also drive billing.
7. **Interpret against the goal**, then record the reading as the before/after evidence
   for the change (see `kafka-benchmarking-procedure`).

## Inputs

- Access to the client JVM's JMX endpoint and the producer/consumer `client-id`.
- Confluent Cloud Metrics API credentials for server-side cross-checks.
- The service goal the metric is being read against.

## Output

A named set of metric readings with their interpretation thresholds and a verdict:
healthy, throttled, lagging, or I/O-bound — plus the remediation if a threshold is
breached.

## References

- `jmx-metric-catalogue` — the metric names, scopes, and descriptions.

## Provenance

Tier 0. Grounded in the profile `always_on` rules (JMX vs Metrics API distinction;
`records-lag-max` as the lag indicator) and the Producers / Consumers / Metrics API
sections of the Confluent source guides (`kafka-best-practices-20260608223304`,
`optimizing-your-apac-20260608224518`). Rights: distillation-only — paraphrased, no
verbatim quotation.
