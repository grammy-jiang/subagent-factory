# product-blueprint-reviewer

A generated Claude Code subagent that critiques and guides **product blueprints** — the
implementation-neutral product artifacts teams produce when turning research synthesis into a
buildable product concept. It reviews at the **blueprint altitude**: holding the artifact to
implementation-neutral product primitives, shifting output-thinking to outcomes (escaping the build
trap), enforcing lean-startup hypothesis discipline, classifying engineering versus academic gaps and
staging a conservative MVP, reviewing adaptive downstream stage routing, and keeping the
product-experience direction inside the UX/architecture boundary — always naming the assumption, the
outcome it serves, and the trade-off. It advises and reviews; it does not author the blueprint's
product content, produce downstream architecture, tech-stack, UX, or code, or make the team's
decision.

## Canonical source of truth

`profile.yaml` — the portable profile. The installed Claude Code adapter
(`adapters/claude-code/product-blueprint-reviewer.md` and
`.claude/agents/generated/product-blueprint-reviewer.md`) is a derived artifact; do not edit it by
hand.

## Package layout

- `profile.yaml` — role, scope, quality bar, modes, knowledge partition, examples, sources.
- `principles/principles.yaml` — 191 promoted principles (63 high-confidence) from the map→reduce spine.
- `analysis/claims.jsonl`, `evidence/evidence-records.yaml`, `sources/anchors/` — the distilled spine.
- `reports/faithfulness-report.yaml` — per-rule claim-strength review against the evidence.
- `skills/` — six authored skills (altitude/neutrality, outcomes/build-trap, lean-startup discipline,
  research-to-blueprint & gap classification, stage routing, product-experience/UX boundary).
- `references/` — `blueprint-principles-index.md` and `stage-routing-decision-guide.md`.
- `tests/` — `principle-behaviour-tests.yaml` (one per high principle), `golden-tests.yaml`,
  `test-results.md`.
- `provenance-ledger.md`, `CHANGELOG.md` — provenance and version history.

## Sources

- Product Blueprint and Stage-Boundary Skill Contract — `distillation-only`.
- Architecture and UX Stage Boundaries — `distillation-only`.
- Escaping the Build Trap — Melissa Perri (2018), `distillation-only`.
- Lean Startup in Technology-Driven Teams — Katila et al. (2020), `distillation-only`.

## Validation

```bash
python -m tools.subagent_factory.validate_generated_package subagents/product-blueprint-reviewer
```
