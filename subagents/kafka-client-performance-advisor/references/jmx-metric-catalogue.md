---
name: jmx-metric-catalogue
kind: reference
status: ready
provenance:
  principles: []
  claims: []
  source_anchors:
  - kafka-best-practices-20260608223304-t0279
  - kafka-best-practices-20260608223304-t0280
  - kafka-best-practices-20260608223304-t0298
  - optimizing-your-apac-20260608224518-t0275
  - optimizing-your-apac-20260608224518-t0617
  - optimizing-your-apac-20260608224518-t0638
---

# JMX / metrics catalogue

The metrics this advisor names when prescribing how to *verify* a configuration change.
Two surfaces, and the split is hard: **client JMX** carries client-side health (throttle,
lag, I/O attribution); the **Confluent Cloud Metrics API** carries server-side, topic- and
cluster-level numbers only and **cannot** return client-side metrics. Read each metric on
the side that owns it.

## Client JMX — producer

| Metric (`name=`) | MBean scope | Description | Reads as |
|------------------|-------------|-------------|----------|
| `produce-throttle-time-avg` | `producer-metrics`, per `client-id` | Average time (ms) a request was throttled by a broker | > 0 → broker is enforcing a produce quota; optimise for throughput or upgrade the cluster tier. |
| `produce-throttle-time-max` | `producer-metrics`, per `client-id` | Maximum time (ms) a request was throttled by a broker | Same as above; peak throttling. |
| `io-ratio` | `producer-metrics`, per `client-id` | Fraction of time the I/O thread spent doing I/O | Low `io-ratio` **and** low `io-wait-ratio` → user-processing time is high and is starving the single producer I/O thread. |
| `io-wait-ratio` | `producer-metrics`, per `client-id` | Fraction of time the I/O thread spent waiting | Used with `io-ratio` to attribute producer time; check callbacks running on the I/O thread. |

## Client JMX — consumer

| Metric (`name=`) | MBean scope | Description | Reads as |
|------------------|-------------|-------------|----------|
| `fetch-throttle-time-avg` | `consumer-fetch-manager-metrics`, per `client-id` | Average time (ms) a broker throttled a fetch | > 0 → broker is enforcing a fetch quota on the consumer. |
| `fetch-throttle-time-max` | `consumer-fetch-manager-metrics`, per `client-id` | Maximum time (ms) a broker throttled a fetch | Same; peak throttling. |
| `records-lag-max` | `consumer-fetch-manager-metrics`, per `client-id` | Maximum lag (records) over any partition in the window | An increasing value over time is the best indication the consumer group is **not keeping up** with producers. |

## Server-side JMX — cluster health (context)

Read only when you have broker JMX access; broker administration is out of client scope —
escalate to the cluster administrator.

| Metric (`name=`) | MBean scope | Description | Reads as |
|------------------|-------------|-------------|----------|
| `IsrShrinksPerSec` | `ReplicaManager` | Rate at which the in-sync replica set is shrinking | Thrashing without deliberate broker shutdown → brokers soft-failing or inter-broker connectivity issues. |
| `UnderReplicatedPartitions` | `ReplicaManager` | Partitions short of their replica count | Should always be 0; > 0 → a broker is not keeping up with replication. |

## Confluent Cloud Metrics API — server-side only

Enabled by default, aggregated at topic and cluster level, and tied to billing. Use for
cross-checks; it will **not** expose the client metrics above.

| Metric | Granularity | Use |
|--------|-------------|-----|
| Bytes produced per minute | grouped by topic | Server-side produce throughput cross-check. |
| Bytes consumed per minute | grouped by topic | Server-side consume throughput cross-check. |
| Max retained bytes per hour (over 2h) | per topic | Storage/retention and billing per topic. |
| Max retained bytes per hour (over 2h) | per cluster | Storage/retention and billing per cluster. |

## Provenance

Tier 0. Built from the Producers, Consumers, and Metrics API metric tables of the
Confluent source guides (`kafka-best-practices-20260608223304`,
`optimizing-your-apac-20260608224518`) and the profile `always_on` rules (`records-lag-max`
as the lag indicator; JMX vs Metrics API client/server split). Rights: distillation-only —
paraphrased, no verbatim quotation. Exact MBean object-name syntax must be confirmed
against current Confluent client documentation.
