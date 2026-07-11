---
name: kafka-benchmarking-perf-test-procedure
kind: skill
status: ready
provenance:
  principles: []
  claims: []
  source_anchors:
    - kafka-optimization-b-20260608223929-h0000
    - kafka-optimization-b-20260608223929-h0001
---

# Kafka Benchmarking Perf-Test Procedure

## Purpose

Run a reproducible Kafka producer/consumer benchmark whose Max Throughput (MB/s)
and Producer P99 Latency (ms) results can be trusted as comparable across CPU
generation, JDK version, compression method, and encryption setting. This is the
methodology every quantified claim in the source benchmark guide rests on; a test
that deviates from it produces numbers that cannot be compared to the source
figures.

## When to use

- A caller describes a benchmark setup and asks whether the results are valid
  (the profile `validate` mode).
- Before trusting a throughput/latency delta a team measured in-house against the
  source benchmark numbers.
- When standing up a new capacity-planning test tied to an SLA.

## Procedure

1. **Fix the two KPIs.** Measure exactly two things and always report them
   together: (a) Max Throughput — the sum of producer messages arriving at the
   broker per unit time, in MB/s; (b) Producer P99 Latency — the 99th-percentile
   end-to-end time from a record being produced to being fetched by the consumer,
   in ms. Higher throughput is better; lower P99 latency is better.
2. **Stand up the three roles as separate containers.** Use three Docker images —
   a producer (generates and sends messages), a Kafka + ZooKeeper server, and a
   consumer (reads messages back).
3. **Place each role on its own node.** Use a 3-node Kubernetes cluster with one
   producer POD, one broker POD, and one consumer POD, each pinned to a distinct
   node via anti-affinity (see `kafka-kubernetes-anti-affinity-setup`) so roles do
   not contend for the same CPUs.
4. **Set the scaling parameters from the vCPU count.** Set PARTITIONS, number of
   producers, and number of consumers to twice the vCPU count of the instance
   under test. Use REPLICATION_FACTOR 1 for a baseline run.
5. **Drive load with the bundled harness scripts.** Run the standard
   `kafka-producer-perf-test.sh` and `kafka-consumer-perf-test.sh` scripts rather
   than a custom client, so the harness matches the source methodology.
6. **Hold the workload constants fixed.** Pin RECORD_SIZE, NUM_RECORDS / MESSAGES,
   BATCH_SIZE, LINGER_MS, and CONSUMER_TIMEOUT, and record them with the result;
   see `kafka-benchmark-software-tables` for source values (e.g. RECORD_SIZE
   1,000; BATCH_SIZE 524,288; LINGER_MS 100).
7. **Run three times, take the median.** Execute each test case three times and
   report the median for both Max Throughput and P99 Latency to discard outliers.
8. **Change one variable at a time.** When comparing CPU generation, JDK,
   compression, or encryption on/off, vary a single dimension per comparison and
   call out every baseline change explicitly, or the delta is not attributable.

## Inputs

- Instance type / vCPU count under test.
- Encryption setting (TLS on/off), compression method, JDK version.
- The fixed workload constants (record size, batch size, linger, message count).
- KPI(s) being optimised: throughput, P99 latency, or both.

## Output

A validated benchmark result: median-of-three Max Throughput (MB/s) and Producer
P99 Latency (ms), each tagged with the exact instance / JDK / encryption /
compression conditions under which it was measured, plus a pass/fail note on any
methodology requirement the caller's setup missed and how to remediate it.

## References

- `kafka-benchmark-software-tables` — workload and Kafka config constants.
- `kafka-benchmark-hardware-tables` — instance/CPU configurations tested.
- `kafka-kubernetes-anti-affinity-setup` — POD placement requirement.

## Provenance

Derived (Tier 0) from the profile `always_on` benchmark-methodology rule and the
`validate` output mode, grounded in the source's Process/Methodology, KPI, and
Workload Architecture sections and the Appendix A Kafka configuration tables.
No verbatim quotation; figures paraphrased.
