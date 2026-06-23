---
name: laws-of-software-architecture
kind: reference
status: ready
provenance:
  principles:
  - P006
  - P025
  - P004
  claims:
  - C00033
  - C00034
  - C00626
  - C00633
  - C00263
  - C00268
  evidence:
  - E00007
  - E00008
  - E00148
  - E00149
  - E00070
  - E00071
  source_anchors:
  - 6b15bd8cd9ba-c0000
  - 1c336f5c12ec-c0000
  - 6b15bd8cd9ba-c0005
  authored_from_digest: a592ce397f8502aed8ede99077bae3c754f0c269cb5e31053798ced7abb869a5
---

# Laws and first principles of software architecture

The foundational principles a reviewer invokes when judging any architecture decision. They come
from *Fundamentals of Software Architecture* and underpin the trade-off and characteristics skills.

## The first law

| # | Principle | What it means in review |
|---|-----------|-------------------------|
| 1 | **Everything in software architecture is a trade-off.** | Every structural choice buys some properties at the expense of others. The honest first answer to "what is the right architecture?" is **"it depends"** — on the driving forces. If an answer has no "it depends" behind it, it is probably hiding a sacrifice. |

**Trade-off-analysis corollary.** A recommendation must explicitly analyze trade-offs: name what
each option *gains* and what it *sacrifices*, rather than present one option as universally best.
An option listed with only upside is an incomplete analysis, not a winner.

## The four dimensions of software architecture

Architecture is defined by four interacting dimensions; a review should account for all four.

| Dimension | What it covers |
|-----------|----------------|
| **Structure** | The architecture style(s) the system is built from (layered, event-driven, microservices, etc.). |
| **Architecture characteristics** | The operational and structural "-ilities" the system must exhibit (scalability, availability, deployability, modularity, …). |
| **Architecture decisions** | The rules and constraints that shape how the system is built. |
| **Design principles** | The guidelines that steer design where a hard rule is not warranted. |

## Driving characteristics are derived and prioritized

| Rule | Consequence for review |
|------|------------------------|
| Characteristics are **derived from the business problem and its drivers**, not chosen from a generic list. | Start from the drivers; a list with no driver behind each item is unranked noise. |
| Keep the driving set **few**. | A long "must-have" list means nothing was actually prioritized. |
| Characteristics **compete and interact**, so a design **cannot maximize them all**. | Rank them; design follows the ranking. Where top characteristics conflict, name the conflict instead of pretending both can win. |

## Provenance

Distilled from principle(s) **P001/P017/P018**, claims **C00001/C00002/C00034/C00041/C00326/C00331**, evidence **E00001/E00002/E00011/E00012/E00070/E00071**, anchored in the cited architecture sources (`sources/anchors/`). Source is `distillation-only`: content is paraphrased, never quoted verbatim.
