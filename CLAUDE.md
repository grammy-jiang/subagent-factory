# Claude Code Instructions

This repository is a local Claude Code subagent-authoring factory.

Use `/author-subagent` to create or update generated subagent packages under `./subagents/`.

Generated subagent source packages must not be placed directly in `.claude/`.

Only exported Claude Code runtime adapters may be installed into:

```text
.claude/agents/generated/
```

Canonical source of truth for each generated subagent:

```text
subagents/<slug>/profile.yaml
```

Do not manually edit files under `.claude/agents/generated/`.

Run validation after generation:

```bash
python -m tools.subagent_factory.validate_generated_package subagents/<slug>
```

## Repository layout

```text
.claude/agents/             factory runtime agents
.claude/skills/             factory skills
.claude/rules/              factory policy rules
subagents/<slug>/           canonical generated subagent packages
.claude/agents/generated/   Claude Code runnable adapter files (DO NOT EDIT)
tools/subagent_factory/     deterministic Python scripts
schemas/                    JSON schemas for all generated artifacts
templates/                  Jinja2 templates
inputs/                     drop source files here before running /author-subagent
```

## Key docs (read when relevant)

- `docs/factory-ops.md` — operational guide: corpus-health, Docling install + converter-keyed
  cache, re-author a package, faithfulness repair, claim-recall, validate.
- `docs/output-quality-eval.md` — how to evaluate whether a generated subagent gives *good advice*
  (not just whether it validates), and the **eval-driven multi-source grounding** recipe: an
  output-eval grounding leak names the missing source → add it via multi-source authoring → the
  expert becomes more faithful *and* more capable (proven A/B). Read before assessing or improving
  a subagent's quality.
- `docs/enhancement-steps/` — per-step build specs (Steps 0–10, 20). `README.md` is the index.
