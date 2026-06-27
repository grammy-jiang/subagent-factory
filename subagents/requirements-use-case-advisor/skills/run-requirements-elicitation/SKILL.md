---
name: run-requirements-elicitation
kind: skill
status: ready
provenance:
  principles:
  - P004
  - P011
  - P021
  - P022
  - P065
  - P067
  - P090
  claims: []
  evidence: []
  source_anchors: []
---

# Run Requirements Elicitation

## Purpose

Plan and facilitate the sessions that surface goals, roles, and stories: use-case
elicitation workshops, story-writing workshops, user-role modelling, and persona
work — and compensate for proxy-user bias when real users are scarce.

## When to use

- A team is about to gather requirements and needs a workshop or interview plan.
- The set of user roles is undefined, conflated, or generic ("the user").
- Real users are limited or absent and the team is relying on proxies.

## Procedure

### Step 1 — Choose the elicitation mix

Gather requirements with lightweight, continuous techniques and combine methods
rather than relying on one (P090): user interviews across roles, questionnaires,
observation, and story-writing workshops.

### Step 2 — Run use-case elicitation workshops well

When running a use-case workshop, get the right people in the room — too many beats
too few — scheduled via a kick-off (P004). Cap sessions at half a workday, use a
silent scribe, and unblock writer's block with daily-work stories. Separate role from
job title with concrete devices, keep an assumptions list, post use cases on the
walls, and keep discussion on intentions rather than screens.

### Step 3 — Run a story-writing workshop before each release

A story-writing workshop with developers, users, and the customer is the fastest way
to trawl for stories (P021). Combine brainstorming with low-fidelity paper
prototyping of conceptual workflows, walk it depth-first, prompt for missing stories,
and favour quantity over quality without judging ideas — then discard the prototype
within days.

### Step 4 — Model user roles in four steps

Run user-role modelling as four steps (P022): brainstorm roles with no discussion;
organise them by spatial overlap; consolidate equivalents and drop unimportant roles;
then refine with attributes. Keep each role a single individual, and stay
people-focused rather than system-focused.

### Step 5 — Add personas for the vital few

Refine important roles with attributes, and for only one or two vital roles create a
concrete **persona** with a name, face, and detail (P065). Write stories in terms of a
specific role or persona instead of the generic "the user".

### Step 6 — Compensate for proxy-user bias

When a user proxy stands in for real users, recognise that proxy's bias and
compensate (P011): the users' manager and the development manager have conflicting
goals or atypical usage; salespeople over-index on the last lost sale but are great
conduits to real users; domain experts suit domain models, not workflows; marketing
understands markets, not users; former users must be recent and aligned; trainers and
support bias toward trainability and supportability; analysts must actually talk to
users.

### Step 7 — Cope when real users are absent

When real users are limited or absent, establish a real-user task force as a sounding
board, use multiple differing proxy types, study competitors for stories, and release
early to expose proxy/real-user mismatches — never assuming developers can substitute
for users (P067).

## Inputs

- The goal of the elicitation (initial backlog, release set, or a specific feature).
- Who is available: real users, proxies, customer, developers; and their access
  constraints.
- Any existing role list or persona material.

## Output

An elicitation plan or review finding containing:

- **Session plan**: which workshops/interviews/observations to run, with attendees,
  timeboxing, and facilitation devices.
- **Role model**: a consolidated, attribute-refined role list and any personas for
  the vital few.
- **Proxy-risk note**: for each proxy in use, its likely bias and a compensating
  action; an escalation when real-user access is blocked.
- **Corrective steps**: one per finding, each grounded in a cited principle.

## Provenance

Grounded in principles P004, P011, P021, P022, P065, P067, P090 of this package,
derived from Alistair Cockburn, "Writing Effective Use Cases" (2001) and Mike Cohn,
"User Stories Applied" (2004). Sources are `distillation-only` — all content is
paraphrased; no verbatim quotation.
