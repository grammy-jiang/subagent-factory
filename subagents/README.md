# Generated Subagent Packages

Each subdirectory is a generated subagent package created by the subagent-authoring factory.

## Package layout

```text
<slug>/
├── README.md
├── profile.yaml          ← canonical source of truth
├── provenance-ledger.md  ← distillation provenance
├── source-pack.manifest.yaml
├── CHANGELOG.md
├── sources/
│   ├── original/         ← immutable source copies
│   ├── markdown/         ← canonical Markdown conversions
│   ├── assets/           ← extracted images and assets
│   ├── anchors/          ← anchor JSONL index files
│   ├── metadata/         ← source metadata JSON
│   └── reports/          ← conversion reports + human-review queue
├── skills/               ← extracted skill SKILL.md files
├── references/           ← reference files (glossaries, rubrics, etc.)
├── adapters/
│   └── claude-code/      ← Claude Code adapter (generated)
└── tests/                ← golden tests, negative routing tests
```

## Creating a new subagent

```text
/author-subagent ./inputs/my-document.pdf --topic "my reviewer"
```

## Validating a package

```bash
python -m tools.subagent_factory.cli validate <slug>
```
