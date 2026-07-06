---
name: product-experience-and-ux-architecture-boundary
kind: skill
status: ready
provenance:
  principles:
  - P012
  - P014
  - P018
  - P019
  - P053
  - P054
  - P057
  - P059
  - P060
  - P061
  - P095
  - P097
  - P098
  - P099
  - P100
  - P102
  - P104
  - P147
  - P148
  - P149
  - P150
  - P151
  - P152
  - P154
  - P170
  - P171
  - P172
  - P173
  - P174
  - P175
  - P176
  - P177
  - P178
  claims:
  - C00012
  - C00040
  - C00044
  - C00045
  - C00046
  - C00053
  - C00102
  - C00103
  - C00104
  - C00105
  - C00106
  - C00114
  - C00093
  - C00107
  - C00108
  - C00109
  - C00118
  - C00094
  - C00097
  - C00098
  - C00112
  - C00132
  - C00138
  - C00139
  - C00140
  - C00099
  - C00115
  - C00095
  source_anchors:
  - 8707406d317e-c0000
  - 8707406d317e-c0001
  - 2a049107e960-c0000
  - 2a049107e960-c0001
  authored_from_digest: 6f77a1d76eec8d0fb7992329a341beb21130a6eea303034e974d9357ec6f3cab
---

# Product experience direction & the UX/architecture boundary

## Purpose

Review a blueprint's product-experience direction for altitude and completeness, and keep the
review itself inside the UX/architecture boundary. This skill checks that product-experience
content stays at UX-intent and architecture-impacting altitude, that every interaction mode is
classified against a controlled taxonomy (with AI Skill correctly told apart from MCP), that
clarifying questions are asked only when they would change the outcome, and that unmet UX needs
are routed to architecture as feedback rather than designed inside the review itself (P012, P095,
P147, P148, P150, P154).

## When to use

- The blueprint (or a research synthesis being converted into one) has drafted a
  product-experience or UX-intent section and needs an altitude check before it is handed to
  architecture or a later UX-design stage.
- The section lists interaction modes — CLI, Web UI, API, AI Skill, MCP, hybrid — and those modes
  need a controlled classification, especially where "AI Skill" and "MCP" both appear (P147,
  P148).
- The caller is unsure whether a product-experience gap is worth a clarifying question or should
  simply be recorded as a default assumption (P150, P152).
- The review must confirm that architecture and UX-design remain two separate stages, that UX is
  not authored ahead of a resolved architecture, and that any UX need the architecture cannot
  support is captured as feedback rather than designed on the spot (P061, P104, P176).

## Procedure

### 1. Hold product-experience content at UX-intent altitude

Read the product-experience section first for what it *is*, not for its polish. It should state
who the primary user is, their job-to-be-done, the experience thesis, and the primary interaction
mode plus how each mode is classified — nothing more (P012, P095). Flag as too-detailed anything
that reads like downstream execution work: concrete user journeys, screen or wireframe layout,
exact CLI flags or command syntax, exact API routes, exact MCP tool schemas, copywriting, or
accessibility specifics. That material belongs to a later UX-design stage, not the blueprint
(P012, P104, P172). If the blueprint already sits at the right altitude, say so explicitly rather
than inventing a gap to fill.

### 2. Classify every interaction mode

For every mode named in the product-experience direction (primary or secondary/future), confirm it
carries one of four controlled classifications: a **primary surface** (the main runtime interface
users or operators drive at MVP), a **secondary surface** (present at MVP but not primary), a
**wrapper/integration surface** (a callable wrapper around another surface — not its own runtime
product), or a **future surface** (deferred, with a stated revisit trigger) (P147). If a mode is
listed with no classification, flag it — architecture cannot infer the intended runtime role from
a bare label (P095, P154). If one entry names two or more modes together (for example "CLI / AI
Skill"), check whether they share a classification; if they do not, require the entry be split
into separate rows so each mode's role stays unambiguous (P149).

### 3. Disambiguate AI Skill from MCP

Treat "AI Skill" and "MCP" as distinct concepts and never let a review pass an entry that merges
them. An AI Skill is how this workflow itself is invoked, and is usually a wrapper/integration
surface (occasionally a primary surface, if it is genuinely its own runtime); it must be
classified explicitly rather than left as a bare label. MCP is a tool surface for *external* AI
agents to call the system, and is a different concern (P148). Check that MCP is present only
because a reusable external tool or data-access boundary is actually justified and fully
specified — not included as a default or fashionable integration choice — and flag an MCP entry
that lacks that justification (P057, P154).

### 4. Decide: ask a clarifying question, or record a default

Before raising a clarifying question, check whether the answer would materially change product
direction, architecture, risk, or implementation, and whether it is already answered by the
supplied research or context. If it would not change any of those, do not ask it (P150). When a
question clears that bar, ask exactly one focused question at a time, and always attach why it
matters, a recommended answer, the alternatives, and the default the review will assume if the
question goes unanswered (P151, P018). Handle this according to the run's mode — interactive,
automatic, or hybrid — recording assumptions, review requirements, reversibility, and revisit
triggers consistently with that mode (P018).

### 5. Infer defaults for low-risk gaps; escalate high-impact ones

When a gap does not clear the clarify bar in step 4, or the run is automatic and no user answer is
available, infer a reasonable default and record it as an assumption rather than blocking the
review (P152, P053). Judge impact, not just presence: a low-risk default (for example, an
uncontroversial secondary-surface choice) can be recorded and the review can still be marked
complete when the remaining open items do not break the design (P053). A high-risk default —
content leaving a local boundary, review being deferred, users assumed technical, an interaction
mode left ambiguous — must be flagged forward as architecture feedback, not buried in an
assumptions list (P152, P175). A high-impact decision the review surfaces should be traceable to a
stated source (blueprint material, user clarification, a rule-pack decision, or an explicit
recorded assumption) and, where it affects architecture, should prompt a new or superseding ADR
rather than sit undocumented (P099, P054, P175).

### 6. Only design what the architecture supports

The product-experience review is not the place to design surfaces, states, or operations the
architecture does not already support. When a UX need in the blueprint exceeds or diverges from
what the architecture provides, record it as architecture feedback and recommend reconciliation
rather than resolving it in place (P061). This mirrors how a downstream UX-design stage must work:
it parses the architecture's surfaces, actors, state model, workflows, human-review flow, security
posture, observability, and failure/recovery behavior *before* authoring any interaction, and
preserves the blueprint's experience intent rather than re-deciding it (P097). If no architecture
has been resolved yet, treat that as a stop condition for detailed UX work, not something to paper
over by inventing structure (P176, P171).

### 7. Keep architecture and UX as distinct stages

Confirm the review does not blur architecture and UX-design into one activity, and that each
stage's own discipline stays intact:

- **Architecture consumes the blueprint's product-experience direction and any recommended
  next-stage routing**, preserves the UX intent, and emits its own downstream handoffs; when stack
  selection is deferred, the technology stack stays provisional rather than being fixed early
  (P098). Architecture pairs its structural decisions with operational controls — interface
  ownership and validation, data ownership and lifecycle, security and trust boundaries,
  observability and audit, failure recovery, testing architecture, rule-gate results, open
  questions, and implementation-handoff notes — and every major decision must trace to blueprint
  material, a user clarification, a rule-pack decision, or an explicit assumption (P014, P099).
  Architecture artifacts stay at the boundary level — proposed modules and namespaces are fine,
  but task tickets, code, migrations, and file-by-file implementation sequencing are not (P172) —
  and are named and placed deterministically, with a fallback filename recorded if writing files is
  unavailable (P170).
- **UX-design only starts once architecture is resolved.** It discovers the architecture (and the
  blueprint, when available) from explicit arguments, context, or common artifact locations before
  it does anything else, and stops if the architecture cannot be found rather than guessing at one
  (P176, P171). Its outputs — interaction flows, user stories, acceptance criteria, Gherkin-style
  E2E scenario seeds, and architecture feedback — must stay testable (roles, goals, preconditions,
  flows, failure recovery, visible states, acceptance criteria, phase tags, testability metadata)
  and must explicitly cover non-happy paths — error, empty, loading, degraded, recovery, and
  human-review experiences — not just the primary flow (P060, P178). It does not perform
  architecture, stack selection, implementation planning, executable-test authoring, visual
  layout, or final copy — those stay out of scope for UX-design just as they do for the blueprint
  (P104). A UX-design document is expected to carry contents, update history, metadata, a clear
  separation of skill-operator UX from target-software UX, scoped surfaces, user stories, scenario
  seeds, architecture feedback, and a self-check appendix (P177).
- **Review, update, and reconcile activities on either artifact resolve what already exists
  first**, stop when a required input is missing, and never silently mutate a document; when
  changes are accepted, only the accepted notes are merged, prior decisions are preserved, and
  blocking conflicts are stopped on rather than invented around (P173, P100).
- **Cross-cutting controls travel with the boundary, not around it.** Any model-backed evaluator or
  gating probe used along the way needs a stated availability policy — required availability,
  fallback behavior, auto-accept rules, and audit logging (P174). Where content may reach an
  external model, the review should expect an explicit data-egress decision, security gates
  expressed as verification evidence, and a default prohibition on raw source content in logs
  (P059). Underneath both stages, deterministic responsibilities — control flow, state, storage,
  security, audit, interfaces, telemetry, durable mutation, validation, workflow transitions — stay
  with ordinary software; AI is reserved for language-, judgment-, or reasoning-heavy work and must
  never bypass deterministic validation before a durable effect (P019). A canonical state model
  keeps lifecycle states, condition flags, audit events, user-visible states, human-review actions,
  progress items, failure behaviors, and handoffs consistent across both stages' documents (P102).

### 8. Close with the product-experience quality gate

Before ending the review, check the product-experience direction against its own quality gate:
primary user, primary job-to-be-done, experience thesis, primary interaction mode, mode
classification, trust/control/transparency needs, human-in-the-loop provision, failure-recovery
expectations, and the UX-to-architecture handoff (P095). Raise a warning-level finding — not
necessarily a stop — for any of: an unresolved primary interaction mode, an MCP surface without
justification, a mismatch between the chosen surface and the stated users, human review deferred
under high quality risk, unclear visibility into data egress, missing user-facing audit access, or
any interaction-mode label left ambiguous or unclassified (P154).

## Inputs

- The blueprint's product-experience / UX-intent section (or the research material from which it
  is being drafted), including any interaction-mode list.
- The architecture document, when the review is checking the UX side of the boundary against what
  architecture actually supports (P061, P097, P176).
- Any answers already given to prior clarifying questions, and the run's mode (interactive,
  automatic, or hybrid), so defaults are recorded consistently with that mode (P018, P053).
- The caller's stated outcome and MVP appetite, so a flagged gap can be judged high- or low-impact
  in context rather than in the abstract (P152, P150).

## Output

A findings list in the reviewer's usual review-mode shape: each finding names the boundary or
classification issue found (too-detailed content, a missing or merged classification, an
unjustified MCP surface, a clarify-versus-default call, an unsupported UX need), the principle it
checks against, the trade-off it implies, and a concrete remediation — plus the assumptions
recorded and any architecture-feedback items produced along the way, ending with the quality-gate
check from step 8 (P095, P154).

## References

- `../../references/blueprint-principles-index.md` — the full principle index for this package;
  look up any principle ID cited above (P012, P014, P018, P019, P053, P054, P057, P059, P060,
  P061, P095, P097–P100, P102, P104, P147–P152, P154, P170–P178) for its complete wording.
- The sibling skills `blueprint-altitude-and-neutrality` (implementation-neutrality checks) and
  `stage-routing-and-pipeline` (downstream RUN/SKIP/DEFER/ASK_USER routing) cover adjacent ground;
  use them for altitude or routing findings that fall outside the product-experience boundary.

## Provenance

Grounded in this package's `principles/principles.yaml` (P012, P014, P018, P019, P053, P054, P057,
P059, P060, P061, P095, P097, P098, P099, P100, P102, P104, P147, P148, P149, P150, P151, P152,
P154, P170, P171, P172, P173, P174, P175, P176, P177, P178) and the underlying claims in
`analysis/claims.jsonl`. Anchored to two passages each in *Product Blueprint and Stage-Boundary
Skill Contract* (`8707406d317e-c0000`, `8707406d317e-c0001`) and *Lean Startup in
Technology-Driven Teams* (Katila et al.) (`2a049107e960-c0000`, `2a049107e960-c0001`); the
architecture/UX-boundary claims behind P014, P018, P019, P097–P100, P102, and P170–P178 trace
through this package's evidence records to the same skill-contract corpus's architecture-and-UX
stage-boundary material. All four package sources are `distillation-only`: everything above is
paraphrased, never quoted verbatim.
