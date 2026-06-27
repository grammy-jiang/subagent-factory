---
name: availability-and-load-balancing-review
kind: skill
status: ready
provenance:
  principles:
  - P054
  - P034
  - P039
  claims:
  - C01898
  - C01929
  - C02258
  - C02259
  - C02386
  - C02387
  evidence:
  - E00262
  - E00264
  - E00334
  - E00335
  - E00403
  - E00404
  source_anchors:
  - 760c81171459-c0022
  - 760c81171459-c0025
  - a6c7e769c072-c0000
  - a6c7e769c072-c0001
  - a6c7e769c072-c0003
  authored_from_digest: 0cb15319e2b9c7d923d7144614c28d5a72c2611cf512fc4fe1567d13a74b5aa4
---

# High availability vs load balancing review

## Purpose

Separate two concerns that vendors and teams routinely conflate. High availability is resilience
in the face of component failure; load balancing distributes work across a pool of systems. They
solve different problems, and neither implies the other. The job is to determine which the system
actually needs — often both — and have each designed deliberately rather than assumed.

## When to use

- A design treats a load balancer as if it also delivers high availability (or vice versa).
- The availability and capacity requirements of a system are being specified or reviewed.
- "We added a load balancer, so we're highly available now" appears in a plan.

Do not invoke when neither resilience nor request distribution is in question for the component.

## Procedure

1. **Pin the requirement first.** Ask whether the system needs availability, load distribution, or
   both. Define this before any implementation choice — it is the decision everything else follows.
2. **Test the load-balancing claim against availability.** A load-balancing pool can route around a
   dead machine, which *touches* availability — but it does not solve it; it relocates the problem
   (e.g. session/state loss, capacity shortfall) elsewhere. Flag "LB therefore HA" as a fallacy.
3. **Test the availability claim against load.** High availability means resilience only; it implies
   nothing about efficient resource use or added capacity. A hot-standby pair has one node at 100%
   and the other idle — available, but not balancing load or adding throughput.
4. **Decide what each layer must provide.** For each tier, state whether it needs HA, load
   balancing, or both, and choose a mechanism for each requirement explicitly.
5. **State the cost.** Availability mechanisms (standby capacity, failover) and load distribution
   (pool management, health checks, state handling) each carry their own cost; name them.

## Inputs

- The system's availability and capacity requirements, the current LB/HA mechanisms, and how
  failure and request distribution are handled per tier.

## Output

A review that names, per tier, whether high availability or load balancing (or both) is required,
corrects any conflation of the two, and recommends a deliberate mechanism for each with its cost.

## Provenance

Distilled from principle(s) **P047/P026/P046**, claims **C00418/C00449/C00778/C00779/C00906/C00907**, evidence **E00082/E00084/E00133/E00134/E00182/E00183**, anchored in the cited architecture sources (`sources/anchors/`). Source is `distillation-only`: content is paraphrased, never quoted verbatim.
