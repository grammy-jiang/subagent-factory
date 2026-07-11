---
name: release-rollback-and-change-management
kind: skill
status: ready
provenance:
  principles: [P014, P039, P041, P011]
  claims: [C00113, C00114, C00221, C00222, C00255, C00220, C00229]
  evidence: [E00090, E00091, E00173, E00174, E00190, E00172, E00176]
  source_anchors: [67c60e378753-c0002, a6c7e769c072-c0000, a6c7e769c072-c0001]
---

# Always be able to roll back: disciplined releases and change management

## Purpose

Make every production change reversible and low-risk: keep database changes additive, require a
tested push-and-rollback plan, run production-like environments, and keep code and configuration
under version control.

## When to use

- A team is releasing code or database changes to production.
- A change is hard to undo, or there is no rehearsed rollback.
- Configuration drifts between environments, or staging does not resemble production.

Do not invoke to write the deployment scripts themselves (hand off) or to pick a specific CI/CD
product (out of scope).

## Procedure

1. **Keep changes rollback-ready (P014).** Keep database changes additive, script and load-test the
   rollback, avoid in-release semantic data changes, and add a feature-flag (wire-on/wire-off)
   framework so behaviour can be disabled without a redeploy.
2. **Require a complete push plan (P039).** Every production change needs a forward plan, a tested
   rollback, a bare-metal restore path, and a *successful test* of both the forward and rollback
   plans before the change ships.
3. **Run three production-like environments (P041).** Maintain development, staging, and production;
   make staging as close to production as possible (ideally identical down to versions). Production
   should stay quiet — no ad-hoc changes.
4. **Put everything under version control (P011).** Track application code *and* production
   configuration alike, with atomic commits, on every platform you operate, and use version control
   for deployment and change-tracking — not just development.
5. **State the trade-off.** Rollback discipline and environment parity buy safety and fast recovery
   at the cost of additive-only schema work, feature-flag upkeep, and the expense of keeping staging
   production-like. Name it.

## Inputs

- The change being shipped, whether a tested rollback exists, how closely staging matches
  production, and what is (and is not) under version control.

## Output

A change-management recommendation naming the rollback gap, the push-plan steps missing, the
environment-parity fix, and the upkeep cost accepted.

## References

- [Scalability Rules index](../../references/scalability-rules-index.md)

## Provenance

Distilled from principles **P014/P039/P041/P011** and their claims/evidence, anchored in
`sources/anchors/`. Sources are `distillation-only`: paraphrased, never quoted verbatim.
