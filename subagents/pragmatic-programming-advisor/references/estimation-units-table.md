---
name: estimation-units-table
kind: reference
status: ready
provenance:
  principles:
  - P006
  - P064
  - P054
  claims:
  - C00103
  - C00105
  - C00108
  - C00109
  - C00111
  - C00113
  - C00257
  - C00258
  source_anchors: []
  authored_from_digest: b9b481c200420d4cad7c74263c358039b792e886e7c2432be6ee05364551899c
---

# Estimation Units

Choose the unit of an estimate to convey its intended accuracy. Quoting a large job in
small units ("130 days") implies false precision; matching the unit to the duration
communicates the real uncertainty. Every estimate begins by understanding the scope of the
question being asked — that scope is part of the answer you deliver (C00105).

| Estimated duration | Quote the estimate in | Rationale |
|---|---|---|
| 1 – 15 days | **days** | Short work; day-level granularity is honest. |
| 3 – 8 weeks | **weeks** | Week units signal accuracy is roughly ±days, not exact. |
| 8 – 30 weeks | **months** | Month units signal the answer is approximate. |
| more than 30 weeks | **— pause first —** | Think hard before quoting at all; the question itself likely needs re-scoping. |

*Derived from C00103: match an estimate's accuracy to context and choose units to convey
the accuracy you intend — quoting "about six months" rather than 130 days when you do not
mean day-level precision.*

## Using the table

- **Scope before number.** Restate what is being asked before answering; the scope is often
  part of the answer you deliver (C00105, P006).
- **Pick the unit, then the value.** Decide the duration band first, then express the number
  in that band's unit rather than converting to a smaller, falsely precise unit (C00103).
- **The 30-week line is a stop sign**, not a value to quote confidently — treat any estimate
  beyond it as a signal to step back and re-examine the question itself.
- **When put on the spot, defer.** Answer that you will get back to them after working through
  the steps; off-the-cuff estimates come back to haunt you (C00113, P064).

## Building the estimate behind the unit

Once you know which unit to use, produce the value honestly:

1. **Model, then decompose.** Build a rough model of the system, break it into components,
   identify each component's parameters, and work out how the parameters combine (P006).
2. **Focus on high-impact parameters.** Parameters that multiply or divide the result matter
   more than those that add; concentrate accuracy there and have a justifiable way to
   calculate the critical ones (C00108).
3. **Watch for sub-estimate stacking.** Estimates built on sub-estimates accumulate the
   largest errors; flag cascaded assumptions explicitly (C00109).
4. **Ask someone who has done it.** A reliable shortcut is to consult someone with direct
   experience before building a model from scratch (P006).
5. **Iterate with the code.** For non-trivial projects, refine the schedule through each
   increment of development rather than locking it in up front (P064).

## Verifying and learning

- **Test against production reality.** Algorithm timing estimates only count when your code
  runs with real data; use profilers when accurate timing is hard (C00257, P054).
- **Avoid premature optimization.** Confirm a bottleneck is real before investing time
  improving it — do not optimize on estimated numbers alone (C00258, P054).
- **Record and compare.** Keep a log of estimates alongside actuals and find out why any
  estimate was wrong; the next estimate improves as a result (C00111).
- **Strange results are signals.** When calculated estimates seem odd but the arithmetic is
  correct, treat it as a sign that your model or understanding is wrong, not as noise (P006).

## Provenance

Derived from principles P006 (estimate to avoid surprises: match accuracy and units to
context, build and decompose a model, focus on high-impact parameters, beware sub-estimate
error accumulation, record and learn, ask someone who has done it before), P064 (iterate
the schedule with the code; defer on-the-spot estimate requests), and P054 (test estimates
against production reality; avoid premature optimization until a bottleneck is confirmed).
Core claims: C00103 (unit/accuracy matching), C00105 (scope before number), C00108
(high-impact parameters), C00109 (sub-estimate error accumulation), C00111 (record and
learn), C00113 (defer on-the-spot requests), C00257 (test against production reality),
C00258 (beware premature optimization). Source is distillation-only; all wording is
paraphrased.
