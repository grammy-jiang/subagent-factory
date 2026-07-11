---
name: availability-and-load-balancing-patterns
kind: reference
status: ready
provenance:
  principles: [P022, P023, P042, P043, P044, P045, P046, P047]
  claims: [C00243, C00290, C00271, C00298, C00319, C00331, C00355, C00375]
  evidence: [E00183, E00203, E00198, E00207, E00213, E00217, E00220, E00224]
  source_anchors: [a6c7e769c072-c0001, a6c7e769c072-c0002, a6c7e769c072-c0003, a6c7e769c072-c0004]
---

# Reference: Availability and load-balancing patterns

A field guide to the resilience and traffic-distribution patterns from *Scalable Internet
Architectures*. The load-bearing distinction: **high availability (HA) is resilience to failure;
load balancing (LB) is about scale.** They are orthogonal — decide which (or both) a system needs
before implementing (P022).

## High availability

- **Eliminate single points of failure (P042).** Avoid components in series; the load balancer is
  itself a SPOF — deploy two with an HA solution. Hardware needed for routine load is not redundant,
  and a vendor's selling points are not your buying points.
- **Prefer peer-based HA (P023).** The cluster owns the services and IP addresses and each node
  negotiates a subset, beating idle hot-standby pairs and dedicated HA hardware as you scale
  horizontally or across sites.
- **Make peers authoritative and test failover (P043).** Each active node must serve authoritatively
  and tolerate concurrent use; refresh neighbors' ARP caches with gratuitous ARP on IP failover, and
  test HA by *actually killing a node*.

## Load balancing

- **Let requirements pick the solution (P044).** If a web switch or IPVS cannot meet a functional
  need it is eliminated. Application-layer balancers buy features (SSL-content and business-rule
  routing) at a performance cost.
- **Segregate static from dynamic (P045).** Most content is static; serve it from a lightweight,
  single-purpose server separated from dynamic content so each scales independently.
- **Offload origins with a reverse-proxy cache (P046).** Serve previously seen content from cache and
  absorb slow-client TCP handling so expensive application servers move to the next job.
- **Route by network proximity (P047).** Optimize for the user's network proximity, not geography;
  combine Anycast DNS (connectionless UDP) with unique per-node IPs to reach the nearest cluster —
  Anycast breaks TCP.

## Choosing

1. State whether the goal is resilience (HA), scale (LB), or both (P022).
2. For HA: remove SPOFs (including the balancer), prefer peer clusters, and rehearse failover.
3. For LB: let functional requirements eliminate solutions, and split static/dynamic and origin
   offload so each tier scales on its own.

## Trade-off

Redundancy and app-layer routing buy availability and routing flexibility at the cost of duplicated
hardware, coordination, and throughput. Name the cost (P042/P044).

## Related

- Skill: [fault-isolation-and-availability](../skills/fault-isolation-and-availability/SKILL.md)
- Skill: [caching-and-statelessness](../skills/caching-and-statelessness/SKILL.md)

## Provenance

Distilled from principles **P022/P023/P042/P043/P044/P045/P046/P047** and their claims/evidence,
anchored in `sources/anchors/`. Sources are `distillation-only`: paraphrased, never quoted verbatim.
