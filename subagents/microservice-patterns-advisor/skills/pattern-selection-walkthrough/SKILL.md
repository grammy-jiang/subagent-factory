---
name: pattern-selection-walkthrough
kind: skill
status: ready
provenance:
  principles:
  - P094
  - P118
  - P096
  - P069
  - P018
  - P126
  - P117
  - P079
  - P120
  claims:
  - C00001
  - C00002
  - C00108
  - C00003
  - C00004
  - C00021
  - C00022
  - C00037
  - C00065
  - C00005
  - C00073
  source_anchors: []
  authored_from_digest: 9f3ef5646fb2b8b029007665159916778ec324a88cba97d7542464a6a76c7498
---

# Pattern Selection Walkthrough

## Purpose

Turn a stated microservice architecture concern into a named shortlist of
candidate patterns from the microservices pattern language, each justified by the
problem it solves, the forces it resolves, and the drawbacks it carries, and end
with a recommendation tied to the caller's forces. This is the umbrella procedure
behind the advisor's `advise` and `compare` modes; the topic-specific skills
(decomposition, sagas, queries, communication, external API, testing, production
readiness) are specialisations of it. It exists because the mapping concern →
group → candidates → forces-weighted choice is a branching routine, too
procedural to inline in the profile body.

## When to use

Use this walkthrough whenever the caller describes a microservice architecture
decision and wants to know which pattern(s) apply and why, and you are not already
inside one of the specialised skills. It is also the entry point that routes to
those specialised skills.

Do **not** use it to produce implementation code, to pick a specific product or
vendor, or for concerns outside microservice architecture — those are out of scope
for this advisor.

## Procedure

1. **Restate the concern and surface the forces.** Extract the problem or quality
   attribute at stake and the constraints, and name the competing forces explicitly
   (consistency vs. coupling, latency vs. availability, team autonomy, failure
   isolation, operational cost). Evaluate the decision by its effect on
   quality-of-service attributes rather than features — any architecture can
   implement the same use cases (C00037, P126). If the forces are unstated, ask for
   them before recommending.

2. **Check whether microservices are even warranted.** If the caller is deciding
   whether to adopt or migrate at all, weigh that first: the monolith is a sound
   default for a small, simple application, and it is bad advice to say "always" or
   "never" use microservices — appropriateness depends on the application's context
   (C00065, P079, P117). Say so plainly when it applies.

3. **Locate the pattern group(s).** Every pattern belongs to one of three groups —
   application, application-infrastructure, infrastructure — and is a motivating
   problem paired with one or more solutions (C00001, C00002, P094). Map the concern
   to a group using the `microservice-pattern-language-map` reference:
   - decomposition / boundaries / ownership / monolith migration → **Decomposition**
     (route to `service-decomposition-advice`)
   - cross-service consistency → **Data / transactions** (route to
     `saga-transaction-design`)
   - cross-service querying or event sourcing → **Data / queries** (route to
     `cross-service-query-design`)
   - how services talk, reliability, reliable event publishing → **Communication**
     (route to `interservice-communication-selection`)
   - external clients, edge auth → **External API** (route to `external-api-design`)
   - verification → **Testing** (route to `microservice-testing-strategy`)
   - observability / config / security / deployment → **Production / deployment**
     (route to `production-readiness-review`)
   A concern may touch several groups (e.g. giving each service its own private
   datastore reachable only through its API is a cascading choice that pulls in sagas
   and CQRS — C00073, P120); pull candidates from each.

4. **List the candidate patterns in each group.** Read candidates straight from the
   reference — for decomposition, Decompose by business capability or by subdomain,
   aligned to teams via Service-per-team and Self-contained service (C00003, C00004,
   P096). Use only names present in the pattern language; never invent one.

5. **State problem, forces, and drawbacks per candidate.** For each candidate, name
   the recurring problem it solves, the forces it resolves, AND the drawback or new
   issue it introduces — a well-formed pattern description states drawbacks, not just
   benefits (C00021, C00022, P069, P018). A bare pattern name is not advice; use the
   `pattern-forces-and-tradeoffs-table` reference to keep this consistent.

6. **Compare alternatives within the group.** When two or more candidates solve the
   same problem, contrast them side by side rather than asserting one in isolation:
   Saga vs. distributed transaction; private datastore vs. shared database; API
   composition vs. CQRS; choreography vs. orchestration; RPI vs. Messaging;
   client-side vs. server-side discovery; container vs. VM vs. serverless.

7. **Recommend, tied to the forces.** Choose the candidate(s) whose resolved forces
   best fit the caller's constraints, say why in those terms, and state the residual
   trade-off they must accept (e.g. eventual consistency — C00005). Where the
   caller's forces conflict with a generic preference, the caller's forces govern.

8. **Situate within the three-step method.** For a whole-application decision, recall
   that the architecture is defined by an iterative three-step process: identify the
   system operations, decompose into services, and define each service's API and
   collaborations (C00108, P118). Hand off: the architect or engineering team owns
   the final selection and any implementation decision; this walkthrough informs it.

## Inputs

- **Required:** a statement of the microservice architecture concern or decision —
  the problem or quality attribute at stake and any constraints — sufficient to
  identify the group(s) and weigh the forces.

## Output

A named shortlist of candidate patterns from the relevant group(s), each with its
problem, forces, and drawbacks stated, alternatives compared where they solve the
same problem, and a recommendation tied to the caller's forces with the residual
trade-off named. At minimum: one correctly named pattern from the applicable group
with a one-sentence statement of the problem it solves or the trade-off it implies.

## References

- `references/microservice-pattern-language-map.md` — the full grouped catalogue
  and the concern → group index used in steps 3–4.
- `references/pattern-forces-and-tradeoffs-table.md` — per-pattern problem / forces
  / benefits / drawbacks, used in step 5.

## Provenance

Tier 2. Grounded in principles P094 (pattern-language groups), P118 (three-step
method), P096 (decomposition patterns), P069/P018 (pattern format; state forces AND
drawbacks), P126 (evaluate by quality attributes), P117/P079 (reject absolute advice;
monolith for small apps), and P120 (private datastore is cascading), from
`chris-richardson-mic-19016f24` and `microservicepatternl-a51cf685`
(`distillation-only`). No verbatim quotation; pattern names are the established field
vocabulary.
