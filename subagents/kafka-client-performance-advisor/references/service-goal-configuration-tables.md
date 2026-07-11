---
name: service-goal-configuration-tables
kind: reference
status: ready
provenance:
  principles: []
  claims: []
  source_anchors:
  - kafka-best-practices-20260608223304-t0685
  - kafka-best-practices-20260608223304-t0879
  - kafka-best-practices-20260608223304-t0151
  - optimizing-your-apac-20260608224518-t0591
  - optimizing-your-apac-20260608224518-t0275
  - optimizing-your-apac-20260608224518-t0504
---

# Service-goal configuration tables

The "Summary of Configurations" parameter sets, one table per Kafka service goal. Each
row gives the recommended client value (or range), the documented default, and the
trade-off the change buys. No single configuration maximises all four goals — pick the
goal first, then apply its table. Defaults drift across Kafka releases; cross-check exact
defaults and valid ranges against current Confluent documentation before production.

## Throughput

Maximise records/bytes moved per unit time by batching harder and compressing.

| Side | Parameter | Recommended | Default | Trade-off |
|------|-----------|-------------|---------|-----------|
| Producer | `batch.size` | 100000–200000 | 16384 | Larger batches raise throughput and compression ratio; cost is higher latency. |
| Producer | `linger.ms` | 10–100 | 0 | Waiting longer fills batches; cost is added send latency. |
| Producer | `compression.type` | `lz4` | none | Fewer bits on the wire; avoid `gzip` (much more compute-intensive). |
| Producer | `acks` | 1 | 1 | Leader-only ack keeps producer fast; weaker durability than `all`. |
| Producer | `buffer.memory` | increase when many partitions | 33554432 | More buffering prevents send stalls; uses more client memory. |
| Consumer | `fetch.min.bytes` | ~100000 | 1 | Bigger fetches cut request overhead and lift throughput; cost is higher latency (bounded by `fetch.max.wait.ms`). |

Parallelise with a consumer group; the parallelism ceiling is the topic partition count.

## Latency

Minimise end-to-end delay. Most Kafka defaults already favour latency, so this table is
largely "leave at defaults".

| Side | Parameter | Recommended | Default | Trade-off |
|------|-----------|-------------|---------|-----------|
| Producer | `linger.ms` | 0 | 0 | Send immediately; gives up batching throughput. |
| Producer | `compression.type` | none | none | No compression delay; more bytes on the wire. |
| Producer | `acks` | 1 | 1 | Leader-only ack avoids waiting on replicas; weaker durability. |
| Consumer | `fetch.min.bytes` | 1 | 1 | Return records as soon as available; more, smaller fetches. |
| Streams | `StreamsConfig.TOPOLOGY_OPTIMIZATION` | `OPTIMIZE` | `NO_OPTIMIZATION` | Collapses/reuses topology nodes to cut work; no latency downside. |

Fewer partitions per broker also reduces fetch/replication latency.

## Durability

Guarantee no message loss, duplication, or reordering. Buys durability at a latency and
throughput cost.

| Side | Parameter | Recommended | Default | Trade-off |
|------|-----------|-------------|---------|-----------|
| Producer | `replication.factor` | 3 | — | Copies on three brokers survive broker loss (enforced in Confluent Cloud). |
| Producer | `acks` | `all` | 1 | Leader waits for in-sync replicas before acking; adds latency. |
| Producer | `enable.idempotence` | `true` | false | Dedupes and preserves order across retries; small overhead. |
| Producer | `max.in.flight.requests.per.connection` | 1 | 5 | Prevents reorder on retry when **not** using the idempotent producer; lowers pipelining. |
| Topic | `min.insync.replicas` | 2 | 1 | With `acks=all`, fails the write unless a majority of replicas received it; raising it lowers availability. |
| Consumer | `enable.auto.commit` | `false` | true | Commit offsets deliberately (inside the transaction for EOS); more code, no silent loss. |
| Consumer | `isolation.level` | `read_committed` | read_uncommitted | Skips open/aborted transactions; reads only committed records. |
| Streams | `StreamsConfig.REPLICATION_FACTOR_CONFIG` | 3 | 1 | Replicates internal/changelog topics; uses more storage. |
| Streams | `StreamsConfig.PROCESSING_GUARANTEE_CONFIG` | `EXACTLY_ONCE` | `AT_LEAST_ONCE` | End-to-end exactly-once; lower throughput. |

## Availability

Recover from failures as fast as possible while avoiding needless rebalances.

| Side | Parameter | Recommended | Default | Trade-off |
|------|-----------|-------------|---------|-----------|
| Consumer | `session.timeout.ms` | as low as feasible | 10000 | Lower detects a dead consumer faster (faster recovery); too low and normal `poll()`/GC pauses are misread as soft failures, causing spurious rebalances. |
| Consumer | `max.poll.interval.ms` | raise if processing is slow | — | Wider idle bound stops slow `poll()` loops triggering rebalances; delays detection of a truly stuck consumer. |
| Consumer | `max.poll.records` | lower if processing is slow | — | Smaller batches finish inside the poll window; more poll round-trips. |
| Streams | `StreamsConfig.NUM_STANDBY_REPLICAS_CONFIG` | 1 or more | 0 | Standby restores state from the last checkpoint (smaller changelog replay) rather than from earliest; uses extra storage. |
| Topic/Broker* | `min.insync.replicas` | 1 | 1 | Lower tolerates more replica failures (writes keep succeeding), at the cost of durability — the inverse of the durability table. |

\* Broker-side levers (`min.insync.replicas`, `unclean.leader.election.enable`) are listed
for context only; broker/topic administration is **out of this advisor's client scope** —
coordinate with the cluster administrator.

> **Note:** the two source guides differ on `session.timeout.ms` for availability — one
> summary says "increase", the other "as low as feasible". The body reasoning (lower =
> faster failure detection = faster recovery) governs; the floor is "not so low that soft
> failures occur". Benchmark and confirm with `records-lag-max` and rebalance frequency.

## Provenance

Tier 0. Built from the four "Summary of Configurations" sections (Throughput, Latency,
Durability, Availability) of the Confluent source guides
(`kafka-best-practices-20260608223304`, `optimizing-your-apac-20260608224518`) and the
profile `always_on` rules and `forbidden_behaviours` (lz4 over gzip; no single config
maximises all goals). Rights: distillation-only — paraphrased, no verbatim quotation.
Defaults/ranges are from the 2020 source and must be re-checked against current Confluent
docs per the package source-of-truth policy.
