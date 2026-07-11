---
name: kafka-kubernetes-anti-affinity-setup
kind: skill
status: ready
provenance:
  principles: []
  claims: []
  source_anchors:
    - kafka-optimization-b-20260608223929-h0006
---

# Kafka Kubernetes Anti-Affinity Setup

## Purpose

Place the producer, broker, and consumer PODs on separate Kubernetes nodes so a
Kafka benchmark measures the workload, not CPU contention between roles co-located
on one node. Anti-affinity is a methodology prerequisite: throughput/latency
figures gathered without it are not comparable to the source benchmark numbers.

## When to use

- Setting up the 3-node benchmark cluster for the perf-test procedure.
- Validating whether a caller's benchmark isolated the roles correctly.

## Procedure

1. **Provision three worker nodes.** Use a 3-node Kubernetes cluster, one node per
   Kafka role, so producer, broker, and consumer each get dedicated CPU.
2. **Run one POD per role.** Producer has one POD, broker has one POD, consumer
   has one POD — three PODs total. Do not stack two roles in one POD.
3. **Apply anti-affinity to pin each POD to a distinct node.** Assign each POD to
   its own node via an anti-affinity rule so the scheduler never co-locates two
   benchmark roles. This is what keeps a producer's compression CPU from stealing
   cycles from the broker's encryption CPU.
4. **Keep the baseline topology fixed.** Use REPLICATION_FACTOR 1 and one
   partition for the baseline placement test; scale partitions/producers/consumers
   per the perf-test procedure (twice the vCPU count) once isolation is confirmed.
5. **Validate the placement before trusting results.** Confirm the three PODs
   landed on three different nodes. If two share a node, the run is invalid —
   reschedule and re-measure.

## Inputs

- A 3-node Kubernetes cluster.
- The producer, broker (Kafka + ZooKeeper), and consumer container images.

## Output

A validated POD placement: one producer, one broker, one consumer POD, each on a
distinct node under anti-affinity — a pass/fail gate for the perf-test procedure.

## References

- `kafka-benchmarking-perf-test-procedure` — the full benchmark this setup feeds.

## Provenance

Derived (Tier 0) from the profile `validate`-mode anti-affinity requirement and
the source's Process/Methodology and Workload Architecture sections describing the
three-node K8s cluster with one POD per role under anti-affinity. No verbatim
quotation.
