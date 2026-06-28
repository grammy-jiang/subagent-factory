---
name: progressive-delivery-patterns-reference
kind: reference
status: ready
provenance:
  principles:
  - P013
  - P016
  - P014
  - P023
  - P031
  - P038
  claims:
  - C00949
  - C01121
  - C01122
  - C02076
  - C00483
  - C00594
  - C00595
  - C00042
  - C00043
  - C01933
  - C00815
  - C00816
  evidence:
  - E00392
  - E00419
  - E00420
  - E00570
  - E00259
  - E00302
  - E00303
  - E00027
  - E00028
  - E00561
  - E00351
  - E00352
  source_anchors:
  - 9fe26df35c80-c0019
  - 9fe26df35c80-c0027
  - 0bea4daa68ab-c0017
  - 50b64948b031-c0006
  - 9fe26df35c80-c0004
  - 9d4b1cf206e5-c0002
  - 0bea4daa68ab-c0010
  - 9fe26df35c80-c0013
  authored_from_digest: b1fee07605452a435ac0ad2c584b50b165cbc2cd93c1377c7823f3f2a544f100
---

# Progressive delivery patterns reference

The patterns for releasing change in controlled, reversible steps. The unifying idea is to decouple
**deployment** (code is in production) from **release** (users see the change), then expose the
change gradually with a fast, tested rollback (P005).

## Pattern catalogue

| Pattern | What it does | When to use | Rollback |
|---------|--------------|-------------|----------|
| Feature toggle | A switch that gates whether deployed code is active for users, so deploying ≠ releasing (CL009) | Deploy continuously while keeping unfinished or risky features hidden; turn features on per cohort | Flip the toggle off |
| Dark launch | Run new code in production without exposing its output to users, to exercise it under real load (CL009) | Validate behaviour/capacity of a change before any user sees it | Stop the dark traffic; nothing user-visible to revert |
| Blue-green | Two identical environments; switch traffic from old (blue) to new (green) (CL010) | Whole-environment cutover with little or no downtime and an instant reverse | Switch traffic back to the previous environment |
| Canary | Expose a small fraction of traffic to the new version first, then widen (CL056) | Limit blast radius and gather real signal before full exposure | Roll back quickly if the canary degrades |

Toggles and dark launches gate the **feature**; blue-green and canary gate the **traffic**. They
compose — e.g. a canary of code that is itself behind a feature toggle.

## Instrumentation and the abort condition

A rollout is only safe if you can see it failing and stop it. Wire production telemetry and
automated anomaly detection so a bad release is detected and acted on before customers are widely
affected (CL011). Define up front the metric and threshold that trips a rollback; an undefined abort
condition means there is no real rollback.

## Staged-exposure template

1. Dark launch (no user-visible output) → confirm behaviour and capacity.
2. Small canary → watch the named metric against its abort threshold.
3. Wider canary → repeat the check.
4. Full rollout (or blue-green cutover with a hold-and-watch window).

A go/abort check sits between every step; a big-bang cutover with no rollback is the anti-pattern.

## Provenance

Derived from principle P005 (claims CL009, CL010, CL056, CL011; evidence EV009, EV010, EV056, EV011)
across `the-devops-handbook-c4933b3c` and `comp500-15893c30` (both distillation-only — paraphrase,
no verbatim quotation). Pattern names are stable; specific tooling for toggles, traffic shifting, and
telemetry changes quickly — verify current vendor and project documentation.
