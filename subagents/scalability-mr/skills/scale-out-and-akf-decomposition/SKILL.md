---
name: scale-out-and-akf-decomposition
kind: skill
status: ready
provenance:
  principles: [P001, P004, P037, P036, P017]
  claims: [C00049, C00050, C00030, C00031, C00203, C00206, C00197, C00007]
  evidence: [E00033, E00034, E00023, E00024, E00166, E00163, E00005]
  source_anchors: [67c60e378753-c0000, a6c7e769c072-c0000]
---

# Scale out, not up — decompose load along the AKF Scale Cube

## Purpose

Guide a growing system toward horizontal scale-out on commodity nodes and choose the partition axis
that relieves the real bottleneck. Scaling up (an ever-larger box) hits a hardware ceiling; scale-out
duplicates work across many inexpensive nodes and is the default for systems expected to grow.

## When to use

- A team must add capacity to a system, service, or database expected to grow rapidly.
- Cloning identical copies no longer relieves the bottleneck (data size, transaction mix, or
  customer count has become the limit).
- A plan assumes growth will be met by buying a bigger server.

Do not invoke for a small, fixed workload one node serves comfortably for its whole life, or when
the caller wants the implementation written (hand off — out of scope).

## Procedure

1. **Confirm the growth assumption (P017, P036).** Establish the system must grow and which parts
   will need it. Design those parts for scale from the start — size for current demand but architect
   so growth needs no application or architectural redesign. Apply D-I-D: design for ~20x, implement
   for ~3x, deploy for ~1.5x, so capacity arrives just in time.
2. **Reject the scale-up reflex (P001).** If the plan is "buy a bigger box", name the ceiling:
   scale-up runs out of larger/faster hardware. Prefer many small commodity systems over a few
   high-end servers. Reserve vertical scaling for a problem with no horizontally-scalable solution.
3. **Start on the X axis (P004).** The easiest split is horizontal cloning — duplicate the whole
   service or database so identical copies share the transaction load. Confirm this is exhausted
   before moving on.
4. **Move to Y when cloning stops helping (P004).** Split *different* things by function or resource
   (verbs/nouns): separate services and their data along responsibility lines. Y scales transactions
   *and* large data sets and gives fault isolation.
5. **Move to Z for very large similar data sets (P004).** Split *similar* things by a customer or
   data attribute (ID, geography) — sharding/podding — when customer growth outpaces other growth or
   per-customer fault isolation matters.
6. **Build from autonomous components (P037).** Compose the architecture from independently scalable
   components so a demand spike stresses only one or two; component architectures scale better than
   monoliths.
7. **State the trade-off.** Scaling out buys fast, cheap transaction scale at the cost of duplicated
   data and functionality and added operational surface. Name that cost in the recommendation.

## Inputs

- The growth expectation, the current bottleneck (transactions, data size, customers), and the
  present partitioning, if any.

## Output

A scale-out recommendation that names the chosen AKF axis (X/Y/Z) and why it fits the bottleneck,
the scale-up ceiling avoided, and the duplication/complexity cost accepted.

## References

- [AKF Scale Cube](../../references/akf-scale-cube.md) — the X/Y/Z axes and how to choose one.
- [Scalability Rules index](../../references/scalability-rules-index.md)

## Provenance

Distilled from principles **P001/P004/P037/P036/P017** and their claims/evidence in
`analysis/claims.jsonl` + `evidence/evidence-records.yaml`, anchored in `sources/anchors/`. Sources
are `distillation-only`: content is paraphrased, never quoted verbatim.
