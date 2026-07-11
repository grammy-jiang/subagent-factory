---
name: fault-isolation-and-availability
kind: skill
status: ready
provenance:
  principles: [P008, P009, P042, P022, P023, P043, P044]
  claims: [C00137, C00145, C00271, C00243, C00290, C00298, C00319]
  evidence: [E00112, E00120, E00198, E00183, E00203, E00207, E00213]
  source_anchors: [67c60e378753-c0003, a6c7e769c072-c0001, a6c7e769c072-c0002, a6c7e769c072-c0003]
---

# Isolate faults and engineer availability (HA is not load balancing)

## Purpose

Make the system survive component failure: eliminate single points of failure, contain blast radius
in share-nothing swimlanes, and keep high availability (resilience) separate from load balancing
(scale) so each is solved deliberately.

## When to use

- An architecture review or new design must withstand failure of any one component.
- A database or service is being split to scale and the team also wants fault isolation.
- A team is selecting availability or load-balancing technology, or has more than one active node
  holding virtual IPs.

Do not invoke to pick a specific load-balancer product (out of scope) or to write failover scripts
(hand off).

## Procedure

1. **Design fault-isolative swimlanes (P008).** Split along Y/Z boundaries into share-nothing
   swimlanes: allow no synchronous cross-swimlane calls, limit async ones, and keep swimlanes on
   physical boundaries so a failure stays contained.
2. **Eliminate single points of failure (P009).** Avoid components in series; strive for
   active/active and add parallel redundancy, especially at the database and network layers.
3. **Make the load balancer redundant too (P042).** Deploy two balancers with an HA solution.
   Hardware needed for routine load is not redundant, and a vendor's selling points are not your
   buying points.
4. **Separate HA from load balancing (P022).** HA is resilience to failure; load balancing is about
   scale. Decide which (or both) a system needs *before* implementing — they are orthogonal.
5. **Prefer peer-based HA (P023).** As you scale horizontally or across sites, prefer peer HA — the
   cluster owns the services and IP addresses and each node negotiates a subset — over idle
   hot-standby pairs and dedicated HA hardware.
6. **Make peer nodes authoritative and test failover (P043).** Each active node must serve
   authoritatively and tolerate concurrent use; refresh neighbors' ARP caches with gratuitous ARP on
   IP failover, and test HA by actually killing a node.
7. **Let requirements pick the balancer (P044).** If a web switch or IPVS cannot meet a functional
   need it is eliminated; application-layer balancers buy features (SSL-content and business-rule
   routing) at a performance cost.
8. **State the trade-off.** Redundancy and isolation buy availability at the cost of duplicated
   hardware, added coordination, and (for app-layer balancing) throughput. Name it.

## Inputs

- The components that must not fail, the current redundancy, whether nodes are active/active, and
  whether the need is resilience, scale, or both.

## Output

An availability recommendation naming the single points of failure, the swimlane boundaries, the
HA-vs-LB split, and the redundancy/coordination cost accepted.

## References

- [Availability and load-balancing patterns](../../references/availability-and-load-balancing-patterns.md)
- [Scalability Rules index](../../references/scalability-rules-index.md)

## Provenance

Distilled from principles **P008/P009/P042/P022/P023/P043/P044** and their claims/evidence, anchored
in `sources/anchors/`. Sources are `distillation-only`: paraphrased, never quoted verbatim.
