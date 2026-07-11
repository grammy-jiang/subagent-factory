---
name: kafka-benchmarking-procedure
kind: skill
status: ready
provenance:
  principles: []
  claims: []
  source_anchors:
  - kafka-best-practices-20260608223304-t0464
  - kafka-best-practices-20260608223304-t0451
  - kafka-best-practices-20260608223304-t0455
  - optimizing-your-apac-20260608224518-t0634
  - optimizing-your-apac-20260608224518-t0624
  - optimizing-your-apac-20260608224518-t0019
---

# Kafka benchmarking procedure

## Purpose

Establish a measured performance baseline for a Kafka client and validate every
configuration change against it. The source states there is no one-size-fits-all
configuration: correct values depend on the use case, the features enabled, and the
data profile. Tuning beyond defaults is therefore only defensible when benchmark
evidence backs it — this is why the package forbids recommending parameter changes
without a benchmark baseline first.

## When to use

- Before changing any non-default producer or consumer parameter for a stated service
  goal (throughput, latency, durability, availability).
- When sizing partitions and the number of producer / consumer processes per server.
- When validating a tuned configuration before promoting it to production.

## Procedure

1. **Functionally validate first.** Confirm the application's dataflows work end to end
   against the target cluster before any performance tuning. Performance work happens
   only after functional validation passes.
2. **Measure cluster bandwidth as a floor.** Run `kafka-producer-perf-test` and
   `kafka-consumer-perf-test` to get a baseline that takes application logic out of the
   equation — the best the cluster will do for your message profile.
3. **Build a representative producer baseline.** Remove upstream dependencies; have the
   producer generate mock data at a rate high enough that data generation is not the
   bottleneck. Use realistic data: payloads padded with zeros or repeated substrings
   compress unrealistically and distort results. Prefer copies of (cleansed) production
   data when testing compression.
4. **Benchmark from the defaults.** Start the client at default configuration and learn
   the default values before changing anything.
5. **Scale producer processes per server.** Run one producer on one server, measure
   throughput via the producer JMX metrics, then repeat while increasing the number of
   producer processes per server each iteration until throughput stops improving.
6. **Scale consumer processes per server.** Repeat step 5 for the consumer side to find
   the consumer processes-per-server count that maximises throughput. The parallelism
   ceiling is the topic partition count.
7. **Sweep service-goal parameters.** Run benchmarks across permutations of the
   parameters that map to the chosen service goal (see the
   `service-goal-configuration-tables` reference). Change one set of parameters at a
   time: tune, run, observe, tune again — do not change parameters whose system-wide
   effect you do not understand.
8. **Feed results back.** Use the measured profile to size partition count and process
   counts, and to confirm the tuned configuration meets the goal before production.

## Inputs

- Target service goal(s).
- A representative message size / data profile (or cleansed production data).
- Cluster connection details and topic partition count.

## Output

A documented before/after throughput (and latency) profile per configuration
permutation, the chosen producer/consumer process counts per server, and the validated
parameter set for the stated service goal.

## References

- `service-goal-configuration-tables` — the parameter set to sweep per goal.
- `jmx-metric-catalogue` — the client metrics to read during each run.

## Provenance

Tier 0. Grounded in the profile `always_on` rules and `forbidden_behaviours` (no
parameter change without a benchmark baseline), and the Benchmarking sections of both
Confluent source guides (`kafka-best-practices-20260608223304`,
`optimizing-your-apac-20260608224518`). Rights: distillation-only — paraphrased, no
verbatim quotation.
