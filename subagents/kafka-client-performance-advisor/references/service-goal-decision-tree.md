---
name: service-goal-decision-tree
kind: reference
status: ready
provenance:
  principles: []
  claims: []
  source_anchors:
  - kafka-best-practices-20260608223304-t0685
  - kafka-best-practices-20260608223304-t0474
  - kafka-best-practices-20260608223304-t0484
  - optimizing-your-apac-20260608224518-t0275
  - optimizing-your-apac-20260608224518-t0019
  - optimizing-your-apac-20260608224518-t0024
---

# Service-goal decision tree

You cannot maximise all four Kafka service goals at once — every tuning choice trades one
against another. So the first move on any request is to fix the **primary** goal, then
apply that goal's parameter table. This reference routes a situation to a goal, the goal to
its configuration table (`service-goal-configuration-tables`), and the verifying metric
(`jmx-metric-catalogue`).

## Step 0 — gate before tuning

- Is the dataflow functionally validated end-to-end against the target cluster? **No → stop.**
  Performance tuning happens only after functional validation.
- Is there a benchmark baseline at default configuration? **No → run `kafka-benchmarking-procedure` first.**
  No parameter change is recommended without a before/after baseline.

## Step 1 — pick the primary goal

| If the caller's situation is… | Primary goal | Apply table | Verify with |
|-------------------------------|--------------|-------------|-------------|
| "Move more records/bytes per second"; produce/fetch throttle-time > 0; throughput-bound | **Throughput** | Throughput | `produce-throttle-time-*`, `fetch-throttle-time-*`, producer JMX throughput |
| "Lowest possible end-to-end delay"; interactive / real-time path | **Latency** | Latency | end-to-end latency; mostly defaults already favour latency |
| "No message loss / no duplicates / no reordering"; financial or audit-critical; consume-process-produce EOS | **Durability** | Durability | confirm no loss; `IsrShrinksPerSec`, `UnderReplicatedPartitions` (broker, via admin) |
| "Recover fast from a failed consumer/broker"; rising `records-lag-max`; frequent rebalances | **Availability** | Availability | `records-lag-max` trend, rebalance frequency |

If two goals are named, make the caller rank them — the tables conflict (e.g. `acks=all`
for durability vs `acks=1` for latency; large batches for throughput vs `linger.ms=0` for
latency).

## Step 2 — known tensions to surface explicitly

| Goal raised | What it costs | Opposing goal |
|-------------|---------------|---------------|
| Throughput (`batch.size`↑, `linger.ms`↑, `fetch.min.bytes`↑) | Higher latency | Latency |
| Durability (`acks=all`, `min.insync.replicas`↑) | Higher latency; more producer-send failures | Latency, Availability |
| Availability (`min.insync.replicas`↓) | Weaker delivery guarantee | Durability |
| Latency (`linger.ms=0`, no compression) | Lower throughput, more bytes/requests | Throughput |

## Step 3 — route to the skill

| Goal / situation | Skill |
|------------------|-------|
| Need a baseline / sweep parameters | `kafka-benchmarking-procedure` |
| Durability / exactly-once pipeline | `eos-configuration` |
| Failed-consumer recovery, rebalance churn | `consumer-group-rebalancing` |
| Streams/ksqlDB latency or state restoration | `kafka-streams-topology-optimisation` |
| Verify any change worked | `jmx-metric-collection` |
| Governed/versioned schemas | `schema-registry-avro-wiring` |

## Step 4 — close out

Every recommendation ships with (a) a concrete value or range, (b) its trade-off stated
explicitly, and (c) the named metric to confirm the change. Re-benchmark after the change
and compare against the Step 0 baseline before production.

## Provenance

Tier 0. Built from the profile `when_to_use` entries (goal selection, throttling, consumer
lag, Streams), the `always_on` rule that the four goals cannot all be maximised at once,
the `forbidden_behaviours` (benchmark before changing; no config maximises all goals), and
the goal/benchmarking framing of the Confluent source guides
(`kafka-best-practices-20260608223304`, `optimizing-your-apac-20260608224518`). Rights:
distillation-only — paraphrased, no verbatim quotation.
