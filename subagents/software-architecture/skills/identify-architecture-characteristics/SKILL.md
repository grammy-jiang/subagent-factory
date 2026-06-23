---
name: identify-architecture-characteristics
kind: skill
status: ready
provenance:
  principles:
  - P036
  - P006
  claims:
  - C00094
  - C00099
  - C00033
  - C00034
  evidence:
  - E00027
  - E00029
  - E00007
  - E00008
  source_anchors:
  - 6b15bd8cd9ba-c0001
  - 6b15bd8cd9ba-c0000
  authored_from_digest: c9127aad60808a74db174d84d9f46b8670401526f526cd3c0b4b70d797ec5cc8
---

# Identify architecture characteristics

## Purpose

Drive structure from the few quality attributes the business problem actually demands. Software
architecture has four dimensions — structure, architecture characteristics (the operational and
structural -ilities), the decisions that constrain it, and the guiding design principles — and
the characteristics are what structure must deliver. This skill derives and ranks those
characteristics so design choices follow a priority order instead of trying to maximize every
quality at once.

## When to use

- The caller is choosing or reviewing structure and the quality attributes are unstated or
  unranked.
- A design is being judged against the qualities it must exhibit.
- A recommendation needs a ranked basis before trade-offs can be weighed.

Do not invoke when the driving characteristics are already explicitly agreed and prioritized.

## Procedure

1. **Read the business drivers.** Extract the goals, domain pressures, and constraints from the
   problem statement. Characteristics are derived from these drivers, not chosen from a generic
   checklist.
2. **Translate drivers into candidate characteristics.** Name the operational (e.g.
   scalability, availability, performance) and structural (e.g. modularity, deployability,
   maintainability) -ilities each driver implies.
3. **Keep the list short.** Reduce to the few characteristics that genuinely drive structure.
   A long list signals that nothing has actually been prioritized.
4. **Rank them.** Order the shortlist by importance to the business problem. Because
   characteristics interact and compete, the ranking — not the membership — is what governs
   design.
5. **Name the unavoidable conflicts.** Call out where top characteristics pull against each
   other (e.g. performance vs. abstraction, scalability vs. simplicity) so the caller knows the
   design cannot satisfy all of them at once.
6. **Hand the ranking to the trade-off step.** The ranked list is the input that
   `architecture-tradeoff-analysis` and style selection use to decide between options.

## Inputs

- The business problem, its drivers, and any stated constraints.
- Any draft design or candidate options to be judged against the characteristics.

## Output

A short, ranked list of driving architecture characteristics with the competing pairs named, ready
to govern style selection and trade-off analysis. The advice that follows must respect this
ranking rather than maximize every quality.

## References

- [Laws of software architecture](../../references/laws-of-software-architecture.md) — the four
  dimensions of architecture and the role of prioritized characteristics.

## Provenance

Distilled from principle(s) **P029/P001**, claims **C00157/C00162/C00001/C00002**, evidence **E00034/E00036/E00001/E00002**, anchored in the cited architecture sources (`sources/anchors/`). Source is `distillation-only`: content is paraphrased, never quoted verbatim.
