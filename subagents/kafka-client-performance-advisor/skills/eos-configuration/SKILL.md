---
name: eos-configuration
kind: skill
status: ready
provenance:
  principles: []
  claims: []
  source_anchors:
  - kafka-best-practices-20260608223304-t0826
  - kafka-best-practices-20260608223304-t0835
  - kafka-best-practices-20260608223304-t0685
  - optimizing-your-apac-20260608224518-t0475
  - optimizing-your-apac-20260608224518-t0269
  - optimizing-your-apac-20260608224518-t0460
---

# Exactly-once semantics (EOS) configuration

## Purpose

Configure a Kafka client for exactly-once / durable delivery in a consume-process-produce
pattern, so messages are neither lost, duplicated, nor reordered. This is the durability
service goal expressed as concrete client parameters. It is a trade-off, not a free win:
the source is explicit that you cannot maximise all four service goals at once, so EOS
buys durability at some latency and throughput cost.

## When to use

- Durability is the stated service goal and message loss or duplication is unacceptable.
- A consume-process-produce pipeline must process each input record exactly once.
- A Kafka Streams application needs exactly-once processing guarantees.

## Procedure

1. **Make the producer idempotent.** Set `enable.idempotence=true` (default false) to
   stop duplicate messages and preserve ordering across retries.
2. **If you are not using the idempotent producer**, pin
   `max.in.flight.requests.per.connection=1` (default 5) to prevent reordering on
   retry. With idempotence enabled this clamp is not required.
3. **Require full acknowledgement.** Set producer `acks=all` (default 1) so the leader
   waits for the in-sync replicas before acknowledging.
4. **Set the durability floor on the topic.** Use `replication.factor=3` (enforced in
   Confluent Cloud) with `min.insync.replicas=2`, so a write fails fast if a majority of
   replicas have not received it. Raising `min.insync.replicas` raises durability but
   lowers availability — choose deliberately.
5. **Make the consumer transactional.** Set `enable.auto.commit=false` (default true) and
   do not commit offsets manually; instead commit them inside the transaction via the
   producer's `sendOffsetsToTransaction()`.
6. **Read only committed data.** Set consumer `isolation.level=read_committed` so the
   consumer skips open and aborted transactions and sees only committed records.
7. **For Kafka Streams**, set `processing.guarantee` to the exactly-once value (default
   at-least-once) and `StreamsConfig.REPLICATION_FACTOR_CONFIG=3` (default 1); Streams
   embeds its own producer and consumer, so the producer/consumer settings above apply
   through their prefixes too.
8. **Benchmark the durability cost.** Measure throughput and latency before and after
   enabling EOS so the trade-off is quantified, not assumed.

## Inputs

- The required durability guarantee (at-least-once vs exactly-once).
- Whether the workload is plain produce, consume-process-produce, or Kafka Streams.
- Topic replication factor and current `min.insync.replicas`.

## Output

A producer + consumer (+ Streams) parameter set delivering the requested guarantee, each
parameter annotated with its durability benefit and its latency/availability cost, plus
the metric to confirm no message loss in production.

## References

- `service-goal-configuration-tables` — the durability configuration table.
- `service-goal-decision-tree` — when to prioritise durability over throughput/latency.

## Provenance

Tier 0. Grounded in the profile `always_on` rules (idempotent producer, acks semantics,
replication factor / `min.insync.replicas` with `acks=all`) and the Durability sections
of the Confluent source guides (`kafka-best-practices-20260608223304`,
`optimizing-your-apac-20260608224518`). Rights: distillation-only — paraphrased, no
verbatim quotation.
