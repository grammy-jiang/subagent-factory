---
name: write-use-case-scenarios
kind: skill
status: ready
provenance:
  principles:
  - P003
  - P005
  - P008
  - P026
  - P027
  - P028
  - P029
  - P032
  - P033
  - P048
  - P074
  claims: []
  evidence: []
  source_anchors: []
---

# Write Use-Case Scenarios

## Purpose

Write or review the body of a use case: the main success scenario, the extension
conditions, and the failure-handling fragments. The aim is a short, readable,
goal-driven story in plain prose where the actor is always visible and every step
moves the goal forward.

## When to use

- Drafting a use case body from a confirmed user-goal and primary actor.
- Reviewing a main scenario that is too long, branchy, or written as UI clicks.
- Extensions or failures are missing, malformed, or nested into unreadable depth.

## Procedure

### Step 1 — Set the end conditions first

Before the steps, write the two exits (P008): the **Success End Condition** (what is
guaranteed when the goal succeeds) and the **Failed End Protection** (what is
protected for every stakeholder when it fails). Writing the failure protection often
reveals the logging or recording the main scenario must include.

### Step 2 — State only enforceable preconditions

A precondition holds only what the system can guarantee and will never re-check
(P026). Do not overstate it with things that are not requirements or cannot be
enforced; record merely-usual context in a Context-of-use note instead.

### Step 3 — Write one main success scenario as the base

Choose one typical, failure-free path and tell that simple story first; add
complications afterward as extensions (P048). Expect the main scenario to look almost
trivial — that is correct.

### Step 4 — Write each step in the single-sentence style

Each step is a forward-moving, succeeding goal in one sentence (P005): present tense,
active voice, simple grammar, the actor visible and clearly "holding the ball". Avoid
the missing-actor and no-real-goal anti-patterns; reread each sentence for the
actor's real goal. Every step is one of exactly three action kinds (P074): an
**interaction** between actors, a **validation**, or an **internal state change** —
validations and state changes exist to protect a stakeholder's interest.

### Step 5 — Keep it short and raise the level if it runs long

Keep the main scenario to roughly 3-9 steps (typically 3-8). When it runs long, merge
steps and raise the goal level by asking why the actor does each step (P027).

### Step 6 — Express ordering and repetition in prose

Treat step order as a partial ordering, not a strict sequence (P032). Express
repetition, arbitrary ordering, optional timing, and cross-actor control in plain
prose and idioms — never in loops or formal notation.

### Step 7 — Brainstorm extension conditions

The most interesting requirements live in the extensions (P003). Brainstorm all
failures and alternative successes using a failure checklist that includes internal
failures; reduce the list by explicit criteria; when in doubt, include a condition.

### Step 8 — Write extension conditions in their own grammar

Each extension condition is a short "what is different" phrase, in a grammar distinct
from action steps (P033). Apply the numbering conventions (letter-and-colon, step
ranges, asterisk for any-time conditions) and flatten loops into named conditions
rather than nesting them.

### Step 9 — Write failure-handling fragments

Write each failure fragment in the same style as the main scenario, starting at the
named step (P028). A fragment ends one of three ways, usually needs no explicit
"go to step", and any new validation it reveals belongs back in the main success
scenario. Manage a failure-within-a-failure by indentation (P029); delay breaking a
fragment into its own use case (which costs tracking and maintenance) until about
three pages or four indent levels, handle the failure of every called sub-use case,
and rely on failure roll-up to avoid a scenario explosion.

## Inputs

- The confirmed user-goal, primary actor, and design scope (see
  `scope-and-goal-leveling`).
- Stakeholders and their interests, to set end conditions and find extensions.
- Any existing draft scenario or extension set under review.

## Output

A use-case body or review finding containing:

- **End conditions**: success and failure-protection statements.
- **Precondition check**: kept enforceable, with over-stated items flagged.
- **Main success scenario**: 3-9 numbered single-sentence steps, each a valid action
  kind, with over-long or UI-laden steps flagged and merged/raised.
- **Extensions**: condition list with correct grammar and numbering, plus
  failure-handling fragments, with nesting/breakout problems flagged.
- **Corrective steps**: one per finding, each grounded in a cited principle.

## Provenance

Grounded in principles P003, P005, P008, P026, P027, P028, P029, P032, P033, P048,
P074 of this package, derived from Alistair Cockburn, "Writing Effective Use Cases"
(2001). Source is `distillation-only` — all content is paraphrased; no verbatim
quotation.
