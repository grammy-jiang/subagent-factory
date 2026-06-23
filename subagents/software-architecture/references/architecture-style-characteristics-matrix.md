---
name: architecture-style-characteristics-matrix
kind: reference
status: ready
provenance:
  principles:
  - P037
  - P046
  claims:
  - C01089
  - C01090
  - C01100
  - C01101
  evidence:
  - E00170
  - E00171
  - E00173
  - E00174
  source_anchors:
  - 8afbdb74139c-c0000
  authored_from_digest: 655990fa9fc09a2632e5b224bd2ba5f2e5b654f8e0b417661ae5bca30fa40bff
---

# Architecture style → characteristics matrix

Each architecture style rates differently across the same set of characteristics; no style is
universally best. Select the style whose profile matches the system's **prioritized**
characteristics. Ratings are the qualitative scale from the Pattern Analysis of each style in
*Software Architecture Patterns* (Mark Richards).

## The matrix

| Style | Overall agility | Ease of deployment | Testability | Performance | Scalability | Ease of development |
|-------|:---------------:|:------------------:|:-----------:|:-----------:|:-----------:|:-------------------:|
| **Layered** | Low | Low | High | Low | Low | High |
| **Event-driven** | High | High | Low | High | High | Low |
| **Microkernel** | High | High | High | High | Low | Low |
| **Microservices** | High | High | High | Low | High | High |
| **Space-based** | High | High | Low | High | High | Low |

## How to read it

- **Match, do not default.** Read **down** a priority column to find the styles strong on the
  characteristic that matters most, then **across** the candidate's row to see what it sacrifices.
- **Every row has a weakness.** A "High" somewhere is paid for by a "Low" elsewhere — that is the
  trade-off the style carries.
- **Selected examples (from the source's own guidance):**
  - Primary concern *scalability* → event-driven, microservices, and space-based score High.
  - Choosing *layered* → deployment, performance, and scalability are the risk areas to watch.
- **The chart is necessary, not sufficient.** Also weigh infrastructure support, team skills,
  budget, deadlines, and application size; once an architecture is in place it is hard and
  expensive to change.

## Provenance

Distilled from principle(s) **P004/P033**, claims **C00219/C00220/C00957/C00958**, evidence **E00048/E00049/E00193/E00194**, anchored in the cited architecture sources (`sources/anchors/`). Source is `distillation-only`: content is paraphrased, never quoted verbatim.
