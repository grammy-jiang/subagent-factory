---
name: economical-scalability-and-tooling
kind: skill
status: ready
provenance:
  principles:
  - P030
  - P055
  - P028
  - P056
  claims:
  - C00016
  - C00046
  - C02209
  - C02210
  - C02227
  - C02228
  - C02334
  - C02335
  evidence:
  - E00001
  - E00011
  - E00295
  - E00296
  - E00310
  - E00311
  - E00379
  - E00380
  source_anchors:
  - 6b15bd8cd9ba-c0000
  - 6b15bd8cd9ba-c0001
  - 745dee448a5d-c0000
  - 745dee448a5d-c0002
  authored_from_digest: 2c282cee968a1e6f7c28815c1f066722c0d752a8c0cb8e6e3f50bddf41e155a9
---

# Economical scalability and storage-tool fit

## Purpose

Right-size *when* and *how much* to invest in scalability, and right-size *what* to store it in.
Overengineering and premature complexity cost money and actively limit scaling; staging the
investment just ahead of need keeps capacity from being paid for long before it is used. Forcing
every kind of data into a relational database is the storage equivalent of the same mistake.

## When to use

- A design adds complexity or capacity far ahead of demonstrated need, or is hard for peers to follow.
- The caller asks when, and how much, to invest in scalability.
- A design defaults all data to one relational database regardless of access pattern, or a new data
  type or storage technology is being chosen.

Do not invoke when a known, imminent demand spike makes maximal capacity the rational immediate
choice, or when the data genuinely needs relational integrity at a volume one RDBMS handles.

## Procedure

1. **Test for overengineering.** Check whether the solution exceeds useful requirements or is simply
   too complex. A practical test: can fellow engineers easily understand it? Complex solutions cost
   more to build and maintain and cap scalability.
2. **Stage the investment with D-I-D.** Apply Design–Implement–Deploy: design for roughly 20x
   capacity, implement (code) for roughly 3x, and deploy for roughly 1.5x. This builds scale just
   ahead of need rather than all at once. Treat the multipliers as heuristics, not laws.
3. **Match capacity to the demand curve.** Recommend deploying capacity shortly before it is needed,
   not far in advance; flag plans that pay for large headroom with no near-term demand.
4. **Choose storage by requirement, not habit.** For each data need, weigh volume, response time,
   relationship needs, and consistency. Do not put everything in an RDBMS by default.
5. **Reserve the RDBMS for what needs it.** Relational databases give ACID integrity but are harder,
   costlier, and less available to scale. Keep them for data that genuinely needs relational/ACID
   properties; route other data (logs, sessions, search, analytics, blobs) to fitter stores.
6. **State the trade-off.** Both right-sizing decisions trade some up-front capability/comfort for
   lower cost and better scalability; name what is given up.

## Inputs

- The proposed complexity/capacity plan, the demand forecast, and the data types with their access
  patterns and consistency needs.

## Output

A recommendation that flags overengineering, stages capacity via D-I-D against the demand curve, and
assigns each data type to an appropriate store (reserving the RDBMS for ACID/relational needs), with
trade-offs named.

## Provenance

Distilled from principle(s) **P024/P030/P020/P031**, claims **C00079/C00109/C00729/C00730/C00747/C00748**, evidence **E00027/E00031/E00109/E00110/E00114/E00115**, anchored in the cited architecture sources (`sources/anchors/`). Source is `distillation-only`: content is paraphrased, never quoted verbatim.
