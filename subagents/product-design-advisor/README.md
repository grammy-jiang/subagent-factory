# product-design-advisor

A generated Claude Code subagent that critiques and guides product-design decisions for digital
product teams. It reframes work from output to outcomes, runs continuous discovery, frames work as
testable hypotheses validated with prototypes and small MVPs, maps and slices user stories, shapes
and bets fixed-appetite work, builds empowered teams, and designs human-centered AI interactions —
always naming the assumption, the outcome, and the trade-off. It advises and reviews; it does not
write production code, produce UI/visual design, or make the team's decision.

## Canonical source of truth

`profile.yaml` — the portable profile. The installed Claude Code adapter
(`adapters/claude-code/product-design-advisor.md` and `.claude/agents/generated/product-design-advisor.md`)
is a derived artifact; do not edit it by hand.

## Package layout

- `profile.yaml` — role, scope, quality bar, modes, knowledge partition, examples, sources.
- `principles/principles.yaml` — 110 promoted principles (87 high-confidence) from the map→reduce spine.
- `analysis/claims.jsonl`, `evidence/evidence-records.yaml`, `sources/anchors/` — the distilled spine.
- `skills/`, `references/` — authored knowledge-partition bodies, each grounded in its principles.
- `tests/` — `principle-behaviour-tests.yaml` (one per high-confidence principle) and `golden-tests.yaml`.
- `reports/faithfulness-report.yaml` — per-rule claim-strength review (no rule stronger than evidence).
- `provenance-ledger.md`, `CHANGELOG.md` — traceability and history.

## Sources

Grounded in six product-management/design works (Cagan, Torres, Perri, Patton, Singer,
Gothelf/Seiden) and the human-centered-AI literature (Amershi et al., Horvitz, Shneiderman). All
sources are `distillation-only`.

## Validate

```bash
python -m tools.subagent_factory.validate_generated_package subagents/product-design-advisor
```
