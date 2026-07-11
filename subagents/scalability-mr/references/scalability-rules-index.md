---
name: scalability-rules-index
kind: reference
status: ready
provenance:
  principles: [P001, P002, P003, P007, P008, P009, P010, P014, P016, P021, P031, P033, P037, P039, P050]
  claims: [C00049, C00068, C00088, C00001, C00137, C00145, C00154, C00113, C00185, C00161, C00085, C00179, C00203, C00221, C00485]
  evidence: [E00033, E00052, E00065, E00001, E00112, E00120, E00127, E00090, E00155, E00134, E00062, E00149, E00166, E00173, E00242]
  source_anchors: [67c60e378753-c0000, 67c60e378753-c0002, 67c60e378753-c0003, a6c7e769c072-c0000]
---

# Reference: Scalability rules index

A thematic index of the package's 50 promoted scalability principles (P001–P050), distilled from
*Scalability Rules: 50 Principles for Scaling Web Sites* and *Scalable Internet Architectures*. Use
it to locate the rule and the skill that operationalizes it. Every entry states the cost as well as
the benefit — there is no free scaling move.

## Scale-out and decomposition

- **P001** Scale out, not up. **P004** AKF Scale Cube (X/Y/Z). **P037** autonomous components.
  **P036** design for scale from the start. **P017** D-I-D (design 20x / implement 3x / deploy 1.5x).
  → skill `scale-out-and-akf-decomposition`.

## Caching and state

- **P003** cache in depth. **P010** statelessness. **P031** eventual consistency (BASE/CAP).
  **P048** cookie cache. **P046** reverse-proxy cache. **P045** static/dynamic split. **P047**
  network-proximity routing. **P025** don't duplicate work. **P005** trim browser work.
  → skill `caching-and-statelessness`.

## Data tier

- **P002** right storage tool. **P018** model up front. **P015** no lock-and-wait. **P020** manage
  locking. **P049** limit distinct products / read replicas. **P032** separate BI from transactions.
  → skill `data-tier-scaling-and-storage`.

## Fault isolation and availability

- **P008** swimlanes. **P009** eliminate SPOFs. **P042** redundant load balancer. **P022** HA vs LB.
  **P023** peer HA. **P043** authoritative peers + tested failover. **P044** requirements-led
  balancing. → skill `fault-isolation-and-availability`.

## Coupling and messaging

- **P021** asynchronous communication with timeouts. **P019** disciplined message bus.
  → skill `asynchronous-coupling-and-messaging`.

## Release and change management

- **P014** always be able to roll back. **P039** complete push plan. **P041** three production-like
  environments. **P011** version-control code and configuration.
  → skill `release-rollback-and-change-management`.

## Monitoring and observability

- **P033** design to be monitored (business metrics first). **P050** collection before problems.
  **P030** log stream → business monitors. **P029** real-time reliable log delivery. **P013** capable
  monitoring features. → skill `monitoring-and-observability-for-scale`.

## Governance and economics

- **P007** simplicity. **P038** KISS / complexity growth. **P016** R − C = P prioritization.
  **P028** own your scalability. **P034** competence in every component. **P035** scalability ≠
  performance. **P040** five aspects + no single owner. **P024** know your tools. **P027** SSL/IP
  planning. **P006** three+ data centers. **P012** learning organization. **P026** QA's role.
  → skill `scalability-governance-and-economics`.

## Provenance

Distilled from the 50 principles in `principles/principles.yaml` and their backing
claims/evidence/anchors. Representative IDs are cited in the frontmatter `provenance`. Sources are
`distillation-only`: paraphrased, never quoted verbatim.
