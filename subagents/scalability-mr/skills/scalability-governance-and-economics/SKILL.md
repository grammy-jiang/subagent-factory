---
name: scalability-governance-and-economics
kind: skill
status: ready
provenance:
  principles: [P007, P038, P012, P026, P016, P028, P034, P035, P040, P024, P027, P006]
  claims: [C00001, C00261, C00106, C00109, C00185, C00170, C00182, C00190, C00215, C00515, C00297, C00059]
  evidence: [E00001, E00193, E00083, E00086, E00155, E00143, E00152, E00160, E00169, E00248, E00206, E00043]
  source_anchors: [67c60e378753-c0000, 67c60e378753-c0004, a6c7e769c072-c0000, a6c7e769c072-c0007]
---

# Govern scalability by simplicity, economics, and ownership

## Purpose

Decide *which* scalability work to do and *how much*, keeping the architecture simple, the spend
justified, and the team in control of its own destiny — and never mistaking a fast component for a
scalable one.

## When to use

- A team is re-architecting a platform or selecting which scaling rules to adopt.
- A design is growing complex, or a vendor feature is being weighed for scaling.
- The team must judge build-vs-buy, capacity for spiky demand, or SSL/IP consumption.

Do not invoke to choose a specific product (out of scope) or to write the platform (hand off).

## Procedure

1. **Default to simplicity (P007, P038).** Avoid overengineering; simplify scope, design, and
   implementation, and reuse proven solutions before building your own. Independent components add
   complexity linearly while dependent ones add it exponentially, and complex systems only grow more
   complex when modified — keep it KISS.
2. **Prioritize by risk reduction minus cost (P016).** Choose scaling work by R − C = P, measure
   availability by revenue impact, and codify the chosen rules as enforced architectural principles.
3. **Separate scalability from performance (P035).** A fast component can still fail to scale, and a
   single slow or non-scaling component can cap or capsize the whole architecture. Judge them apart.
4. **Own your scalability (P028).** Scale your own system rather than relying on vendor/proprietary
   features, keeping destiny, simplicity, and total cost in your control.
5. **Stay competent in every component (P034, P040).** Build-vs-buy is not an excuse for
   incompetence — to the customer every problem is yours. Master the five aspects of a
   mission-critical environment (high availability, monitoring, software management, avoiding
   overcomplication, optimization) and never entrust the architecture to a single person.
6. **Know your tools (P024).** Pick features by principle, weigh the cost of features you do not
   need, match the delivery/consistency guarantee to the need, and keep configuration identical
   across nodes.
7. **Plan capacity and constraints deliberately (P006, P027).** Design for three or more live data
   centers and lean on the cloud for spiky demand rather than a two-site hot/cold pair; plan SSL/IP
   consumption knowing one IP serves at most one SSL common name and SSL blocks name-based virtual
   hosting.
8. **Build a learning organization (P012, P026).** Learn from customers via fast launches and A/B
   testing and from operations via blameless postmortems on every incident; use QA to lower cost and
   raise throughput and defect detection — you cannot test quality in.
9. **State the trade-off.** Governing for simplicity and ownership buys control and lower long-run
   cost at the price of more in-house capability and upfront discipline. Name it.

## Inputs

- The platform's growth and revenue context, the candidate rules or vendor features, the team's
  competence, and the spiky-demand and SSL/IP constraints.

## Output

A governance recommendation naming which scaling work to prioritize (R − C = P), the simplicity and
ownership stance, and the capability cost accepted.

## References

- [Scalability Rules index](../../references/scalability-rules-index.md)

## Provenance

Distilled from principles **P007/P038/P012/P026/P016/P028/P034/P035/P040/P024/P027/P006** and their
claims/evidence, anchored in `sources/anchors/`. Sources are `distillation-only`: paraphrased, never
quoted verbatim.
