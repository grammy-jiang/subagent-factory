---
name: stage-routing-decision-guide
kind: reference
status: ready
provenance:
  principles:
  - P029
  - P032
  - P033
  - P055
  - P056
  - P132
  - P145
  - P153
  - P155
  - P156
  - P157
  - P158
  - P159
  - P160
  - P161
  - P162
  - P163
  - P164
  - P165
  - P166
  - P167
  - P168
  claims:
  - C00003
  - C00004
  - C00056
  - C00057
  - C00079
  - C00080
  - C00081
  - C00099
  - C00085
  - C00086
  - C00100
  - C00111
  - C00082
  - C00083
  - C00084
  - C00087
  - C00116
  - C00062
  - C00038
  - C00069
  - C00054
  - C00055
  - C00067
  - C00071
  - C00058
  - C00059
  - C00060
  - C00061
  source_anchors:
  - 8707406d317e-c0000
  - 8707406d317e-c0001
  - 2a049107e960-c0000
  - 2a049107e960-c0001
  authored_from_digest: 24bd1af8087ccf21d02718d8da82f4f5155e340a43fafe9f69b1bb4075177fd6
---

# Stage-Routing Decision Guide

The blueprint is the first product-level routing point: product shape, users, MVP appetite,
interaction mode, risk, AI involvement, review needs, data sensitivity, workflow complexity,
and implementation ambiguity all become explicit here before any downstream stage runs (P155).
Use this guide to check that a blueprint's routing plan for architecture, tech-stack,
security-review, test-design, UX-design, and architecture-update/reconciliation stays a core
path plus optional gates that run only when risk, ambiguity, rework avoidance, or testing needs
justify them (P156) — presented as a linear path with visibly flagged conditional follow-ups,
never a flattened list (P157).

## Recommendation vocabulary

Every downstream stage recommendation carries exactly one controlled value. A recommendation
may point toward a path, but it must never silently widen the pipeline beyond what the evidence
supports (P029).

| Value | Applies when | What it must carry |
|---|---|---|
| **RUN** | The blueprint's signals justify running the stage now. | Cited evidence for why the stage is needed (P029, P168). |
| **SKIP** | The signals that would trigger the stage are absent. | A stated reason the trigger does not apply. |
| **DEFER** | The stage may be needed later but nothing yet requires it. | A named revisit trigger — the condition that reopens the decision. |
| **ASK_USER** | A high-impact unknown blocks a confident default. | The specific missing information — not a vague prompt (P167, P168). |

Reviewer check: flag any recommendation that is blank, mixes two values, or omits the support
column above — that is an uncontrolled or unevidenced recommendation (P029, P168).

## Stage-recommendation record

Represent each stage's recommendation as one dependency-aware row, not a bare verdict. This
mirrors the same controlled-field discipline used for open questions and next-stage
entries — owner or stage, blocking status, recommended action, decision, and required input
(P145) — so the routing table and the open-questions list stay consistent with each other.

| Column | What it records |
|---|---|
| **Stage** | The downstream stage this row routes: architecture, tech-stack, security-review, test-design, UX-design, or architecture-update/reconciliation. |
| **Decision** | Exactly one of RUN / SKIP / DEFER / ASK_USER (see Recommendation vocabulary above). |
| **Depends On** | Any stage(s) this decision presupposes — for example, tech-stack selection typically depends on architecture having at least a provisional design, unless the stack is already fixed (P033). |
| **Confidence** | How strongly the cited signal supports the decision: high, medium, or low. |
| **Reason** | The evidence or justification behind the decision; never left blank. |
| **Blocks Next Step** | Whether leaving this stage unresolved stops a later stage from proceeding, and which one. |
| **Revisit After** | For DEFER rows, the trigger or condition that reopens the decision (P166). |

Reviewer check: flag any row missing Depends On, Confidence, Reason, or Revisit After where the
Decision requires it — a routing table without these columns is not dependency-aware (P166,
P145).

## Per-stage routing signals

Product-experience signals feed routing decisions across all five downstream stages below —
UX-design, security-review, test-design, architecture-design, and tech-stack selection are each
pulled by their own subset of blueprint signals, not by one blanket rule (P153). The
architecture stage additionally resolves which of its own modes applies (design, stack,
review, update, reconcile, or materialize) before doing further work, honoring an explicit mode
first and otherwise inferring from the request and available artifacts (P055).

| Downstream stage | Default | Routes to RUN / DEFER when… |
|---|---|---|
| **Architecture-design** | RUN for a serious blueprint (P161). | The blueprint needs technical structure, responsibility boundaries, contracts, security posture, observability, or failure-handling design (P032). Skip only for conceptual notes, work with no planned implementation, or a trivial script whose architecture is already obvious (P161). Its own output stays architecture-only — implementation planning, code, deployment scripts, and migrations route to their own downstream stages, not into this recommendation (P032). |
| **Tech-stack selection** | Runs once architecture exists (provisional or fixed). | Technology choice materially affects architecture, data, deployment, provider/orchestration, performance, cost, or security (P162); ask the user instead when budget, hosting, compliance, licensing, or team constraints are the deciding factor (P162). Stack mode picks technologies that satisfy the architecture and reports a conflict rather than silently rewriting it (P033). |
| **Security-review** | Runs when a risk factor is present. | Data egress, sensitive data, authentication/authorization, meaningful MCP capability exposure, audit/compliance needs, multi-user access, secrets, or provider credentials are in scope (P163). |
| **Test-design** | Runs or defers by workflow criticality. | Workflow correctness, AI-output evaluation, failure/recovery paths, human review, user-story-driven tests, or multiple integration surfaces make end-to-end coverage important (P164). |
| **UX-design** | Runs or defers by interaction weight. | Roles, human review, non-trivial interaction, failure recovery, user-story-driven tests, non-technical users, or trust/control needs call for detailed experience design (P132). |
| **Architecture-update / reconciliation** | DEFER at blueprint stage (P165). | A downstream decision, review, or conflict actually requires an architecture change (P165). A bare existing-architecture request still defaults to non-mutating review unless the caller explicitly asks for update, reconciliation, or materialization (P056) — and whichever of those modes ends up selected must keep that same non-mutating or explicit-update boundary, never silently changing the canonical architecture document (P056). |

Reviewer check: an architecture-design SKIP on a serious blueprint, a tech-stack RUN before
architecture exists, or an architecture-update that runs with no triggering decision, review,
or conflict are all signal-default mismatches to flag (P161, P162, P165).

## Routing-complexity heuristic

Score routing complexity across seven dimensions: user-facing complexity, technical ambiguity,
security/privacy risk, AI uncertainty, integration complexity, human-review complexity, and
testing importance (P159).

Treat the resulting score as a routing heuristic that guides which optional gates to run —
never as a formal project estimate — and revisit it once architecture design has actually
happened, rather than letting an early score override later judgment (P160).

Reviewer check: flag any routing plan that treats the complexity score as authoritative (a
decision with no named signal behind it beyond "the score says so") or that never revisits the
score after architecture design (P159, P160).

## Warnings

Two severity tiers, matching the source's own distinction between a review-time flag and a
hard gate failure.

### Flag (raise on review)

- Skipping tech-stack, security-review, test-design, or UX-design even though its own risk
  signals are present in the blueprint (P158).
- A row with no Depends On value, or a DEFER row with no Revisit After trigger (P158, P166).
- A pipeline presented as a flat list rather than a core path plus visibly flagged conditional
  gates (P158, P157).
- The routing-complexity score treated as a formal estimate rather than a heuristic (P158,
  P160).
- An interaction-mode or stage label left ambiguous (P158).

### Block (fails the routing gate)

- A recommendation that is missing or does not use exactly one of RUN / SKIP / DEFER / ASK_USER
  (P168).
- A RUN with no cited evidence behind it (P168, P029).
- An ASK_USER that names no actual missing information (P168, P167).
- Architecture-design skipped without the conceptual-notes / no-implementation / trivial-script
  justification its default requires (P168, P161).
- A high-risk project, per the complexity heuristic, carrying no optional gates at all (P168).
- No ASK_USER anywhere in the plan while a high-impact unknown is not otherwise assigned to an
  answer, a downstream owner, or a review stage (P168, P167).

## Provenance

The recommendation vocabulary, stage-recommendation columns, and routing-complexity heuristic
are grounded in the Product Blueprint and Stage-Boundary Skill Contract
(`blueprint-contract-8707406d`); the architecture- and tech-stack-mode routing detail draws on
the Architecture and UX Stage Boundaries source (`stage-boundaries-f4cae146`). The frontmatter
provenance also carries anchors from Lean Startup in Technology-Driven Teams
(`lean-startup-katila-2a049107`), reflecting this package's shared cross-source provenance
record rather than a distinct claim drawn from that source for this table. Rights status for
every source above is distillation-only: this reference paraphrases throughout and contains no
verbatim source text. Principle IDs: P029, P032, P033, P055, P056, P132, P145, P153, P155,
P156, P157, P158, P159, P160, P161, P162, P163, P164, P165, P166, P167, P168.
