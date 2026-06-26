---
name: domain-distillation
kind: skill
status: ready
provenance:
  principles:
  - P013
  claims:
  - C088
  - C089
  - C090
  source_anchors:
  - domaindrivendesignqu-20260612231910-h0064
  authored_from_digest: e3468ef6b24ca79811b021ea32053e32dfd17035bb857f3bcb3d231bbc37618c
---

# Domain Distillation

## Purpose

Separate the Core Domain from the Generic Subdomains within a large model so that
development effort, talent, and investment concentrate where the system's unique
business value actually lives. The reviewer uses this skill to assess whether a
large or tangled model has been distilled, whether the Core is visible and small,
and whether staffing and implementation choices reflect that priority.

## When to use

- A model remains large and hard to navigate even after repeated refactorings,
  obscuring which concepts carry the system's distinctive business logic.
- A team must decide where to deploy its strongest developers, what to build
  in-house, and what to acquire or outsource.
- A reviewer must judge whether the Core Domain has been identified and kept
  separate from supporting generic material.
- Resource allocation or development priority appears mis-calibrated — core
  developers are working on supporting subdomains while the heart of the model
  receives inadequate design attention.

## Procedure

### 1. Identify the Core Domain

Determine which part of the model captures the essence of the system's unique
business purpose — the primary source of its competitive or operational value.
The Core is context-specific: a concept that is central to one system may be a
generic supporting concern in another (C091). Verify that the team can articulate
what the Core is and distinguish it from the surrounding model.

### 2. Check whether the Core is small and explicitly marked

Assess whether the model has been boiled down so that the Core concepts stand out
clearly from supporting material. A well-distilled Core is deliberately made small;
all other parts of the model should be justified by how they support it (C089).
Flag any model where Core concepts are indistinguishable from generic ones — this
is a distillation gap.

### 3. Assess talent allocation

Review whether the best available developers are assigned to the Core Domain. If
the Core receives less senior attention than supporting subdomains, or if core
developers are routinely pulled onto generic work, flag this as a priority
misalignment. Mistakes in Core Domain design are harder to recover from than
deficiencies elsewhere (P013, C089).

### 4. Identify Generic Subdomains

Locate cohesive parts of the model that are necessary to the system but are not
the project's motivating purpose — standard accounting logic, generic scheduling,
common charting, general currency handling, and similar concerns that appear in
many systems. These are Generic Subdomains. Verify that they have been factored
into separate Modules and that no project-specific specialties are embedded in
them (C090).

### 5. Evaluate Generic Subdomain implementation routes

For each Generic Subdomain, determine which of the four available routes has been
chosen or should be chosen (C092):

| Route | Description | Key trade-off |
|---|---|---|
| Off-the-shelf solution | Adopt an existing library or product | Reduces build effort; introduces version and compatibility dependencies |
| Outsourcing | Delegate design and implementation to another team | Frees core developers; requires a well-defined interface contract |
| Existing published model | Adapt an analysis pattern from the literature | Leverages proven design; may need tailoring to fit the specific context |
| In-house implementation | Build it internally | Highest integration control; consumes team capacity that could serve the Core |

Flag cases where core developers are building generic subdomains that could be
sourced externally without meaningful loss (C090).

### 6. Confirm lower priority for Generic Subdomains

Verify that Generic Subdomains receive lower development priority than the Core
and that core developers are not routinely assigned to them. The goal is to
preserve the team's best design capacity for the work that differentiates the
system (P013, C090).

### 7. Recognise that the Core emerges iteratively

The Core Domain does not appear fully formed in one step. It becomes clearer
through successive refactorings as the model matures. Check whether the team
treats Core identification as an ongoing activity and re-examines generic elements
in light of a newly clarified Core, rather than treating the initial distillation
as fixed (C088).

## Inputs

- The full domain model: class diagrams, module structure, code, or design
  documents showing the model's scope and organisation.
- A description of the system's business purpose sufficient to judge which
  concepts carry unique value versus which are general-purpose supporting
  infrastructure.
- Team composition, staffing assignments, and build-vs-acquire constraints.

## Output

A distillation assessment covering:

1. The identified Core Domain, with a brief rationale for why those concepts
   constitute the primary competitive or operational value.
2. The Generic Subdomains identified, each placed in a separate Module or
   flagged as a distillation gap if not yet separated.
3. A talent-allocation finding: whether the best developers are assigned to the
   Core or are mis-deployed on generic work.
4. An implementation-route recommendation for each Generic Subdomain, drawn
   from the four-option table above.
5. Any distillation gaps: concepts that obscure the Core, missing Module
   boundaries, or Core Domains that are too large or insufficiently highlighted.

## References

- `references/building-block-pattern-summaries.md` — Module pattern details
  relevant to factoring Generic Subdomains.
- `references/context-map-pattern-catalogue.md` — inter-context relationships
  that can emerge once distillation clarifies boundaries.

## Provenance

Grounded in principle P013 (Core Domain identification and staffing), claims
C088, C089, C090, and evidence records E037, E038, E039, all sourced from the
Distillation section of "Domain-Driven Design Quickly" (Avram & Marinescu,
InfoQ 2006), anchor `domaindrivendesignqu-20260612231910-h0064`.
Source rights status is `distillation-only`; all content is paraphrased — no
verbatim passages are reproduced.
