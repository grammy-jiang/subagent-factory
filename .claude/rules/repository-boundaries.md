# Repository Boundaries

## Generated subagent packages

All generated subagent packages live under:

```text
subagents/<slug>/
```

Never place generated package content directly under `.claude/`.

## Canonical profile location

```text
subagents/<slug>/profile.yaml
```

This is the single source of truth for each subagent.

## Installed adapter location

```text
.claude/agents/generated/<slug>.md
```

This is a generated artifact. Do not edit manually.

## Source files

Drop source documents here before authoring:

```text
inputs/
```

Or pass absolute paths directly to `/author-subagent`.

## Factory scripts

```text
tools/subagent_factory/
```

All deterministic scripts live here. Do not call external scripts.

## Allowed operations on generated adapters

- Read (for display/comparison)
- Overwrite via `cli export` (automated)

Never manually edit `.claude/agents/generated/*.md`.
