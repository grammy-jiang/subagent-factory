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

## Running the factory (two layers)

- **Skill = recipe.** `/author-subagent` runs the whole pipeline in one session
  (source → claims → evidence → principles → profile → faithfulness → adapter → validate).
- **`campaign/` bash = manager.** Drives the skill inside fresh headless `claude -p`
  sessions, adding per-session budgets (anti-dilution), gates, logs, and resume. It does
  not replace the skill.
- **Single source** → `campaign/generate-subagent.sh`. **Multi-book** → the per-book
  map→reduce path (`generate-subagent.sh` refuses ≥2 sources).

Full run + review→fix→improve workflow, the 5-phase map→reduce commands, MAP caching
rules, and the log-review tiers live in `docs/factory-ops.md` (section "Run and improve
the factory"). Back up `subagents/<slug>/` before a fresh map→reduce — assemble/finish
overwrites it.

## Materials catalog & duplication check

`docs/materials-catalog.md` (+ `catalog/materials.yaml`) records **every source processed in this
repo**, keyed by `sha256`. It is generated — DO NOT hand-edit; it is derived from every
`subagents/*/source-pack.manifest.yaml` + the MAP cache.

**On every new inbound book/paper, CHECK FIRST (before converting/MAPping):**

```bash
python -m tools.subagent_factory.materials_catalog check <md-path | sha256 | title>
```

It reports exact-content duplication (sha256) and the closest same-book / topic matches (title
tokens) with which subagent each feeds — so you never re-ingest a book already in the corpus and
you can see topical overlap before choosing a home. After processing new material, refresh:

```bash
python -m tools.subagent_factory.materials_catalog build
```

(Overlap that is not exact-dup is fine — the reduce step's cos-0.55 clustering de-dups principles at
build time; the check just prevents blind re-ingestion and informs home/`--select` choices.)

## Key docs (read when relevant)

- `docs/state-of-the-factory.md` — **start here.** Orientation: what's built, the A/B/C tracks, the
  repair toolset, the measured eval findings, what's open.
- `docs/factory-ops.md` — operational guide: corpus-health, Docling install + converter-keyed
  cache, re-author a package, faithfulness/anchor repair (remap / reground / heading / surgical),
  claim-recall, validate.
- `docs/output-quality-eval.md` — how to evaluate whether a generated subagent gives *good advice*
  (not just whether it validates), and the **eval-driven multi-source grounding** recipe: an
  output-eval grounding leak names the missing source → add it via multi-source authoring. Measured
  result: multi-source's robust win is **grounding/faithfulness** (deterministic, judge-independent);
  an advice-quality gain is **not** proven (judge-family-dependent — the "more capable" read was
  withdrawn at n=20). Read before assessing or improving a subagent's quality.
- `docs/enhancement-steps/` — per-step build specs (Steps 0–10, 20). `README.md` is the index;
  `research-integration-plan.md` is the A/B/C track status.
