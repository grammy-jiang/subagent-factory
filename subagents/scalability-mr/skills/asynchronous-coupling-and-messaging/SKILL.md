---
name: asynchronous-coupling-and-messaging
kind: skill
status: ready
provenance:
  principles: [P021, P019]
  claims: [C00161, C00162, C00163, C00165, C00166, C00167]
  evidence: [E00134, E00135, E00136, E00138, E00139, E00140]
  source_anchors: [67c60e378753-c0003, 67c60e378753-c0004]
---

# Decouple with asynchronous communication and a disciplined message bus

## Purpose

Stop a slow or failing dependency from cascading through the system by making the right calls
asynchronous, bounding the synchronous ones, and treating the message bus as a scalable,
fault-isolated component rather than an unbounded firehose.

## When to use

- Services or tiers call each other and a failure or slowdown in one can stall the callers.
- A call is external, long-running, error-prone, or otherwise unconstrained.
- A message bus is part of the architecture, or is being considered.

Do not invoke to choose a specific broker product (out of scope) or to write the messaging code
(hand off).

## Procedure

1. **Favour asynchronous communication (P021).** Decouple services so a callee's failure does not
   cascade into the callers. Make external, long-running, error-prone, or unconstrained calls
   asynchronous by default.
2. **Bound every synchronous call (P021).** Where a call must stay synchronous, give it a timeout so
   a stuck dependency cannot hold the caller's resources indefinitely.
3. **Treat the bus as a scalable component (P019).** Scale the message bus with Y/Z splits (by
   function or data), not X cloning — cloning a bus does not relieve its real bottlenecks.
4. **Do not overcrowd the bus (P019).** Publish only value-justified traffic; every message has a
   cost, so avoid flooding the bus with low-value events.
5. **State the trade-off.** Asynchrony buys decoupling and resilience at the cost of eventual
   delivery, ordering and idempotency concerns, and harder end-to-end tracing. Name what the design
   now has to handle (retries, duplicates, out-of-order).

## Inputs

- The call graph between services, which calls are external/long-running/error-prone, and whether a
  bus already exists and what it carries.

## Output

A coupling recommendation naming which calls become asynchronous, the timeouts on the rest, the bus
split axis, and the delivery/ordering cost accepted.

## References

- [AKF Scale Cube](../../references/akf-scale-cube.md) — why the bus splits on Y/Z, not X.
- [Scalability Rules index](../../references/scalability-rules-index.md)

## Provenance

Distilled from principles **P021/P019** and their claims/evidence, anchored in `sources/anchors/`.
Sources are `distillation-only`: paraphrased, never quoted verbatim.
