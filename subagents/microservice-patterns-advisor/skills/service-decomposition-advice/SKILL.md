---
name: service-decomposition-advice
kind: skill
status: ready
provenance:
  principles:
  - P084
  - P096
  - P081
  - P101
  - P102
  - P119
  - P023
  - P029
  claims:
  - C00114
  - C00115
  - C00003
  - C00004
  - C00041
  - C00042
  - C00105
  - C00106
  - C00122
  - C00123
  - C00113
  - C00112
  - C00124
  source_anchors: []
  authored_from_digest: d0165449919ff97ee5e431fe4368a38ea02a97134e4d2310c629875b79347e27
---

# Service Decomposition Advice

## Purpose

Help a caller decide where service boundaries should fall, how large a service
should be, and how to migrate an existing monolith — using the decomposition and
refactoring patterns of the microservices pattern language. This is the specialised
walkthrough for the **Decomposition** group.

## When to use

Use when the caller is splitting an application into services, asking where a
capability or entity should live, sizing a service, or migrating a monolith. Do not
use for data-consistency, query, communication, or deployment concerns (route to the
matching skill), and never produce implementation code.

## Procedure

1. **Choose the decomposition axis.** Recommend Decompose by business capability
   and/or Decompose by subdomain, aligning boundaries to teams via Service-per-team
   and Self-contained service (C00003, C00004, P096). Business capabilities give a
   relatively stable architecture because they capture *what* the business does
   (stable) rather than *how* (changes), and are found by analysing the
   organisation's purpose, structure, and processes (C00114, C00115, P084).

2. **Organise around business concepts, not technical layers.** Every sound
   decomposition yields business-oriented services; do not carve services along
   technical tiers (C00113, P119).

3. **Size a service by team and responsibility, not lines of code.** Define a service
   by a focused, cohesive set of responsibilities — size metrics are not a useful
   design goal (C00041, C00042, P081). A good boundary lets a small team develop the
   service with minimal lead time and cross-team coordination; split a service that
   needs a large team or is slow to test, and treat a service that must constantly
   change with others as a distributed-monolith smell (C00105, C00106, P101).

4. **Apply SRP and CCP at the service level.** Give each service one reason to change
   (Single Responsibility Principle) and package components that change for the same
   reason together (Common Closure Principle) — the antidote to a distributed
   monolith (C00122, C00123, P102).

5. **Weigh the four obstacles before fixing boundaries.** Network round-trips
   (reduce with a batch API or by combining services); reduced availability from
   synchronous calls (prefer asynchronous messaging); data that must be atomically
   updated or seen consistently (keep in one service, or use sagas across services);
   and god classes (eliminate by giving each service its own subdomain model)
   (C00112, C00124, P023). If a boundary creates a chatty synchronous dependency or
   splits a consistency-critical operation, reconsider it.

6. **Flag cascading consequences.** Point out that private-per-service data (handled
   in `saga-transaction-design` and `cross-service-query-design`) is what forces
   sagas and CQRS once boundaries are drawn — decomposition is not a local choice.

7. **For an existing monolith, migrate incrementally.** Recommend the Strangler
   Application pattern — build services around the monolith and move functionality
   over gradually, never a big-bang rewrite (P029) — and treat the first
   decomposition as a revisable first attempt.

8. **Hand off.** The architecture owner makes the final boundary decisions; this
   skill informs them.

## Inputs

- **Required:** the application or domain to decompose (or the monolith to migrate),
  the capabilities/entities involved, and any consistency or team-ownership
  constraints.

## Output

A recommended decomposition (named capabilities/subdomains and their service
boundaries), the sizing rationale (team/responsibility, SRP/CCP), the obstacles that
shaped the boundaries, and — for a migration — a Strangler path, each tied to the
caller's forces.

## References

- `references/microservice-pattern-language-map.md` — the Decomposition and
  refactoring patterns in context.

## Provenance

Tier 2. Grounded in principles P084/P096 (decompose by capability/subdomain), P081
(define by responsibilities not size), P101 (size for a small team), P102 (SRP/CCP at
service level), P119 (organise around business concepts), P023 (the four obstacles),
and P029 (Strangler migration), from `chris-richardson-mic-19016f24` (Microservices
Patterns, Chris Richardson, Manning 2018, `distillation-only`). No verbatim
quotation.
