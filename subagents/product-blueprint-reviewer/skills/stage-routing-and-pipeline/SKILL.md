---
name: stage-routing-and-pipeline
kind: skill
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

# Adaptive Downstream Stage Routing & Pipeline

## Purpose

Equip the reviewer to check a blueprint's downstream-routing recommendation — the blueprint
acting as the first product-level adaptive router (P155) — for evidence-based, dependency-aware,
overrideable RUN / SKIP / DEFER / ASK_USER decisions across architecture-design,
tech-stack-selection, ux-design, security-review, test-design, architecture-update, and
architecture-reconciliation (P029). The review never authors the downstream stage itself; it only
checks whether the blueprint's recommendation for that stage is justified, evidenced, and safe to
hand off.

## When to use

- The blueprint (or its recommended-next-stages / stage-gate section) is under review before the
  caller hands it to architecture, tech-stack, UX, security, or test-design work.
- The caller is deciding a specific RUN, SKIP, DEFER, or ASK_USER call for one downstream stage and
  wants it checked against the risk signals that should justify it.
- The blueprint presents its pipeline as one flat list, omits a stage's dependency or revisit
  trigger, or contains no ASK_USER despite an unresolved, high-impact unknown.
- The blueprint's complexity assessment (if present) needs checking for scope and for honesty
  about what it is and is not.

Not for: producing the architecture, tech stack, UX design, or test plan itself — this skill only
reviews the blueprint's recommendation that a stage should run, skip, wait, or be asked about; the
caller's own team or the downstream stage owns the actual authoring.

## Procedure

1. **Confirm the routing gate belongs here.** A blueprint that is a genuine product design should
   carry a downstream-routing recommendation, because it is the first artifact where product
   shape, users, MVP boundary, interaction mode, risk, AI involvement, review needs, data
   sensitivity, workflow complexity, and implementation ambiguity become explicit (P155). If a
   serious blueprint has no routing section at all, or defers the whole question to a later stage
   with no rationale, treat that as a missing gate rather than assuming a downstream stage will
   supply it.

2. **Check the pipeline's shape.** Confirm the blueprint separates a near-linear core path from
   optional gates that run only when risk, ambiguity, rework-avoidance, or testing needs justify
   them (P156), and that the presented pipeline is split into that core path plus a small, visible
   table of conditional follow-up gates — not one undifferentiated list that could hide a deferred
   stage (P157). Flag a flattened, single-list pipeline as a defect (P158).

3. **Check the complexity assessment, if the blueprint includes one.** Confirm it scores across
   all seven dimensions — user-facing complexity, technical ambiguity, security/privacy risk,
   AI/LLM uncertainty, integration complexity, human-review complexity, and testing importance
   (P159) — and that it is explicitly labeled a routing heuristic rather than a formal estimate,
   with a scheduled revisit after architecture-design instead of letting the number itself override
   judgment (P160). Flag a score presented as a formal estimate, or one that silently drives a
   decision with no accompanying reason, as a defect (P158).

4. **Review each stage's own recommendation against the signals that should drive it**, reading
   the blueprint's product-experience material (roles, review needs, data handling, interaction
   mode) as the shared input across all of them (P153):
   - **architecture-design** — expect RUN by default for any blueprint describing a real,
     implementable product; a SKIP is defensible only for a conceptual note, no-implementation
     work, or a trivial script with obvious architecture (P161). Because this is the stage that
     turns the blueprint into technical structure, responsibility boundaries, contracts, security,
     observability, failure handling, and handoff notes (P032), an unjustified SKIP here is one of
     the more serious findings the review can raise.
   - **tech-stack-selection** — check that the decision tracks whether technology choices
     materially affect architecture, data, deployment, provider or orchestration choice,
     performance, cost, security, budget, hosting, compliance, licensing, or team constraints
     (P162). If stack selection is deferred to a later mode, confirm that mode is expected to
     satisfy the architecture and surface any architecture-impacting conflict rather than quietly
     rewriting the architecture around it (P033).
   - **ux-design** — check that RUN or DEFER tracks user roles, human review, non-trivial
     interaction, failure recovery, user-story-driven tests, non-technical users, or trust/control
     needs; a backend-only or trivially simple product may legitimately skip or defer it (P132).
   - **security-review** — check that RUN tracks data egress, sensitive data, authentication or
     authorization, MCP capability exposure, audit or compliance needs, multi-user access,
     secrets, or provider credentials (P163).
   - **test-design** — check that RUN tracks workflow correctness, AI-output evaluation, failure
     and recovery paths, human review, user stories, or multiple integration surfaces that need
     end-to-end coverage (P164).
   - **architecture-update / architecture-reconciliation** — both should default to DEFER at
     blueprint stage; RUN is justified only once a downstream decision, review, or conflict
     actually forces an architecture change (P165). A blueprint that recommends either of these to
     run before any architecture exists has jumped ahead of the pipeline.

5. **Check dependency-awareness.** Each stage recommendation should be readable as Stage, Decision,
   Depends On, Confidence, Reason, Blocks Next Step, and Revisit Trigger (P166). Treat a
   recommendation with no stated dependency, or a DEFER with no revisit trigger, as a defect
   (P158) — the review should be able to tell, for every row, what has to happen first and what
   would reopen it.

6. **Check the ASK_USER discipline.** If no stage in the table is ASK_USER, the blueprint must show
   why every high-impact unknown (for example external data egress, deployment environment, data
   sensitivity, or a compliance requirement) is already answered, assigned to a downstream owner, or
   delegated to a review stage (P167). If a high-impact unknown fits none of those three outcomes,
   require that the blueprint add ASK_USER rather than accept a confident-looking table that has
   quietly assumed the answer.

7. **Check the open-question and next-stage field discipline more broadly.** Confirm open
   questions and recommended next stages use the same controlled fields throughout — an owner or
   stage, a blocking-status flag, a recommended action, a stage decision, and the required input —
   instead of free-text notes a downstream reader would have to interpret (P145).

8. **Check any architecture-mode language the routing recommendation touches.** Where the
   blueprint's recommendation reaches into how the architecture stage itself will resolve its mode
   (design, stack, review, update, reconcile, or materialize), confirm the resolution honors an
   explicit mode first and otherwise infers from the request plus available artifacts (P055), and
   confirm a bare request against an existing architecture defaults to non-mutating review rather
   than an update, reconciliation, or materialization absent an explicit ask (P056).

9. **Apply the routing gate as a pass/fail check, not a style note.** Fail the recommendation when
   it has a missing or uncontrolled decision value, an unevidenced RUN, an ASK_USER that names no
   missing information, an unjustified architecture-design SKIP, a high-risk project with no
   optional gates recommended at all, or an unresolved high-impact unknown with no ASK_USER
   (P168). Warn — but do not fail — when an optional stage is skipped despite matching risk
   signals, a dependency or a deferred-gate revisit trigger is missing, the pipeline is presented
   as a flat list, the complexity score is treated as a formal estimate, or an interaction-mode
   label is left ambiguous (P158).

10. **Frame every finding as an overrideable recommendation, not a mandate.** State the trade-off
    and the missing evidence or dependency a stage's routing needs, and let the caller keep or
    change the call — the review checks whether the recommendation is justified and visible, not
    whether the reviewer's own preference for RUN or SKIP wins (P029).

## Inputs

- The blueprint's downstream-routing material: its recommended-next-stages section, any
  complexity assessment, and the product-experience material it should be drawing signals from.
- The caller's outcome and risk context where the blueprint itself is silent on it (for example
  undisclosed data sensitivity or deployment environment), so the reviewer can judge whether a
  given SKIP, DEFER, or missing ASK_USER is actually justified.

## Output

A findings list, one entry per routing defect found, each naming: the stage affected, the
principle(s) it violates, whether the defect is fail-level or warn-level per step 9, and the
concrete fix (add the missing dependency or revisit trigger, add the missing evidence, change SKIP
to RUN, add ASK_USER, split a flattened pipeline, or relabel a misused complexity score). Every
finding states its trade-off and stays overrideable by the caller, consistent with the reviewer's
overall critique format.

## References

- `../../references/stage-routing-decision-guide.md` — the full per-stage RUN / SKIP / DEFER /
  ASK_USER criteria, the complexity-scoring rubric, the dependency defaults, and the adaptive
  stage-gate checklist this procedure checks against.
- `../../references/blueprint-principles-index.md` — the complete principle index, including the
  altitude, build-trap, and gap-classification principles that inform whether a stage
  recommendation's evidence is itself sound.

## Provenance

Distilled from principles P029, P032, P033, P055, P056, P132, P145, P153, and P155–P168 in
`principles/principles.yaml`, derived from claims C00003–C00004, C00038, C00054–C00062, C00067,
C00069, C00071, C00079–C00087, C00099–C00100, C00111, and C00116 in `analysis/claims.jsonl` —
tracing to the product-blueprint and stage-boundary skill contract's adaptive stage-gate routing
model and its architecture/UX stage-boundary material (source anchors `8707406d317e-c0000`,
`8707406d317e-c0001`, `2a049107e960-c0000`, `2a049107e960-c0001`). Both source documents are
`distillation-only`: this procedure paraphrases and restructures their routing rules; it does not
quote them.
