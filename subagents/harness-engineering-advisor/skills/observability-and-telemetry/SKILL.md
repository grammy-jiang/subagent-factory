---
name: observability-and-telemetry
kind: skill
status: ready
provenance:
  principles:
  - P013
  - P034
  - P009
  - P030
  - P042
  - P064
  - P075
  claims:
  - C00005
  - C00006
  - C00029
  - C00090
  - C00125
  - C00178
  - C00193
  - C00228
  - C00009
  - C00010
  - C00119
  - C00120
  - C00146
  - C00147
  - C00161
  - C00030
  - C00053
  - C00121
  - C00044
  - C00047
  - C00142
  - C00248
  evidence: []
  source_anchors: []
---

# Observability and Telemetry

## Purpose

Capture runtime telemetry sufficient for replay and detect harm cumulatively across turns and traces, not only per input.

## When this applies

- the system must support diagnosis, audit, governance, or production monitoring.
- applying rich telemetry to sensitive environments.
- harms can be decomposed or aggregated across prompts, actions, sessions, or traces.
- diagnosing multi-turn harm or noncompliance.
- validating long-running or tool-using agents.
- assessing reliability, compliance, or safety.
- operating agents over repeated interactions.
- debugging long-horizon agent behavior.
- monitoring heterogeneous model fleets.
- When repeated calls, unchanged failures, evidence-free context growth, or plan oscillation is observed.

## Procedure

For each finding in this layer, name the harness weakness, apply the control, and state the trade-off or residual risk:

1. Capture cognitive, operational, and contextual telemetry at runtime, and design privacy controls when rich traces may expose sensitive data. (P013)
2. Capture live telemetry sufficient for replay, including runtime metadata, plans, tool calls, tool results, verification events, context decisions, environment state, human decisions, and append-only session logs. (P034)
3. Use cumulative session audits, multi-trace analysis, and trace-tree localization when harm or noncompliance can aggregate across turns or traces. (P009)
4. Inspect execution behavior, not only final outputs, because successful-looking results can hide noncompliant trajectories. (P030)
5. Track drift, parsing failures, repeated-output loops, safety conditions, trace differences, and replay evidence as distinct operational signals. (P042)
6. Use model-aware monitoring for heterogeneous model fleets because detectors may not generalize across model families. (P064)
7. When an agent loops, stop immediately, preserve trace and diff, diagnose the missing tool, bad output, ambiguity, or stale context, restart from a compacted narrower context, and add a detector if recurrence shows a pattern. (P075)

End with a concrete next step; never produce production harness code, and present no single control as complete harness safety.

## Principles

- **P013** (high) — Capture cognitive, operational, and contextual telemetry at runtime, and design privacy controls when rich traces may expose sensitive data.
- **P034** (medium) — Capture live telemetry sufficient for replay, including runtime metadata, plans, tool calls, tool results, verification events, context decisions, environment state, human decisions, and append-only session logs.
- **P009** (high) — Use cumulative session audits, multi-trace analysis, and trace-tree localization when harm or noncompliance can aggregate across turns or traces.
- **P030** (high) — Inspect execution behavior, not only final outputs, because successful-looking results can hide noncompliant trajectories.
- **P042** (high) — Track drift, parsing failures, repeated-output loops, safety conditions, trace differences, and replay evidence as distinct operational signals.
- **P064** (medium) — Use model-aware monitoring for heterogeneous model fleets because detectors may not generalize across model families.
- **P075** (medium) — When an agent loops, stop immediately, preserve trace and diff, diagnose the missing tool, bad output, ambiguity, or stale context, restart from a compacted narrower context, and add a detector if recurrence shows a pattern.

