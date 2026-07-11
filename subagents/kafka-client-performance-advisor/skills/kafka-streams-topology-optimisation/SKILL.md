---
name: kafka-streams-topology-optimisation
kind: skill
status: ready
provenance:
  principles: []
  claims: []
  source_anchors:
  - kafka-best-practices-20260608223304-t0699
  - kafka-best-practices-20260608223304-t0879
  - kafka-best-practices-20260608223304-t0884
  - optimizing-your-apac-20260608224518-t0576
  - optimizing-your-apac-20260608224518-t0289
  - optimizing-your-apac-20260608224518-t0557
---

# Kafka Streams topology optimisation

## Purpose

Tune a Kafka Streams (or ksqlDB) application's topology and state handling so it meets a
latency or recovery target. Streams applications embed their own producers and consumers,
so the same service-goal trade-offs apply — plus two Streams-specific levers: topology
optimisation and standby replicas for faster state restoration.

## When to use

- A Streams / ksqlDB topology needs lower end-to-end latency.
- State-store restoration time after a rebalance or restart is too long.
- The application must meet a reliability target via standby state replicas.

## Procedure

1. **Enable topology optimisation.** Set `StreamsConfig.TOPOLOGY_OPTIMIZATION` to the
   optimised value (default no-optimisation). This lets Streams collapse and reuse parts
   of the topology rather than running the naive form. It is one of the latency levers in
   the source's latency configuration set.
2. **Add standby replicas for fast recovery.** Set
   `StreamsConfig.NUM_STANDBY_REPLICAS_CONFIG` to 1 or more (default 0). With a standby,
   a re-initialised task replays the changelog only from the last checkpointed offset
   (a smaller slice), instead of replaying from the earliest offset when no local state
   store exists — cutting restoration time.
3. **Keep the embedded clients' goal aligned.** Apply the producer and consumer settings
   for the same service goal (see `service-goal-configuration-tables`) through the
   Streams producer/consumer prefixes — the embedded clients are not configured for free.
4. **Protect the poll loop from soft failures.** If record processing per `poll()` is
   slow, either raise `max.poll.interval.ms` (the idle bound before more records are
   fetched) or lower `max.poll.records` (smaller returned batches) so a long-running
   batch does not trigger a needless rebalance (see `consumer-group-rebalancing`).
5. **Set the Streams replication factor for durability** where required:
   `StreamsConfig.REPLICATION_FACTOR_CONFIG=3` (default 1).
6. **Benchmark each change** against the latency / recovery metric before adopting it.

## Inputs

- The target: lower latency, faster state restoration, or higher reliability.
- Current topology config (optimisation flag, standby replicas, replication factor).
- Observed restoration time and poll-loop processing time.

## Output

A Streams configuration set (topology optimisation, standby replicas, replication factor,
poll-loop bounds) with each change tied to its latency or recovery benefit and its cost.

## References

- `service-goal-configuration-tables` — Streams rows of each goal's table.
- `consumer-group-rebalancing` — poll-loop and session-timeout interaction.

## Provenance

Tier 0. Grounded in the profile `when_to_use` Streams entry and the Latency / Availability
(state restoration, `num.standby.replicas`) sections of the Confluent source guides
(`kafka-best-practices-20260608223304`, `optimizing-your-apac-20260608224518`). Rights:
distillation-only — paraphrased, no verbatim quotation.
