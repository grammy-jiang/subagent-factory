---
name: consumer-group-rebalancing
kind: skill
status: ready
provenance:
  principles: []
  claims: []
  source_anchors:
  - kafka-best-practices-20260608223304-t0394
  - kafka-best-practices-20260608223304-t0867
  - kafka-best-practices-20260608223304-t0875
  - optimizing-your-apac-20260608224518-t0557
  - optimizing-your-apac-20260608224518-t0204
  - optimizing-your-apac-20260608224518-t0550
---

# Consumer group rebalancing

## Purpose

Tune how fast a consumer group detects and recovers from a failed consumer without
triggering needless rebalances. This is the availability service goal on the consumer
side: detection speed trades off against rebalance stability, and the source frames it as
a balance to be struck, not a value to be maximised.

## When to use

- Optimising consumer-group availability / recovery time after a consumer failure.
- A group rebalances too often (soft failures) or detects hard failures too slowly.
- A slow `poll()` loop or long GC pause is causing spurious group membership churn.

## Procedure

1. **Understand the two failure modes.** Kafka detects a dead consumer when it stops
   sending heartbeats or stops calling `poll()`. Hard failures (e.g. SIGKILL) and soft
   failures (expired session timeout) both trigger a rebalance across the surviving
   members.
2. **Tune `session.timeout.ms` for the goal.** Lowering it detects hard failures faster
   and shortens recovery — the availability optimisation. But set it too low and normal
   `poll()` delays or GC pauses are misread as failures, causing soft-failure
   rebalances. Set it as low as feasible without crossing into soft failures.
3. **Fix slow poll loops instead of just widening the timeout.** When processing per
   `poll()` batch is the cause, either raise `max.poll.interval.ms` (the upper bound on
   idle time before the consumer must fetch again) or lower `max.poll.records` (the
   maximum batch size returned) so processing finishes inside the allowed window.
4. **Account for GC pauses.** A long JVM GC pause is the other common soft-failure cause;
   address it in the JVM, not only by loosening Kafka timeouts.
5. **For stateful (Streams) consumers**, add standby replicas
   (`num.standby.replicas` ≥ 1) so a rebalanced task restores state from the last
   checkpoint rather than replaying the whole changelog (see
   `kafka-streams-topology-optimisation`).
6. **Verify with metrics.** Watch `records-lag-max` during and after a rebalance to
   confirm the group catches back up, and watch rebalance frequency to confirm soft
   failures stopped.

## Inputs

- The recovery-time target and current `session.timeout.ms`.
- Per-`poll()` processing time and observed GC pause durations.
- Whether consumers are stateful (Streams) or stateless.

## Output

A consumer membership configuration (`session.timeout.ms`, `max.poll.interval.ms`,
`max.poll.records`, optional standby replicas) that detects failures quickly without
inducing soft-failure rebalances, plus the metric to confirm recovery.

## References

- `service-goal-configuration-tables` — availability configuration table.
- `jmx-metric-catalogue` — `records-lag-max` for recovery verification.

## Provenance

Tier 0. Grounded in the profile `when_to_use` consumer-lag entry, `always_on` consumer
parameters and the `records-lag-max` lag indicator, and the Availability / consumer
rebalancing sections of the Confluent source guides (`kafka-best-practices-20260608223304`,
`optimizing-your-apac-20260608224518`). Rights: distillation-only — paraphrased, no
verbatim quotation.
