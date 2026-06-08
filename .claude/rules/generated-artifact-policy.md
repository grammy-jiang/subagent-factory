# Generated Artifact Policy

## What is a generated artifact

Files created by the factory scripts or Claude Code agents:

- `subagents/<slug>/profile.yaml`
- `subagents/<slug>/provenance-ledger.md`
- `subagents/<slug>/source-pack.manifest.yaml`
- `subagents/<slug>/adapters/claude-code/<slug>.md`
- `subagents/<slug>/tests/*.yaml`
- `.claude/agents/generated/<slug>.md`

## Rules

1. **Canonical > Installed**: profile.yaml is canonical. Adapter is derived.
2. **Re-export after change**: any change to profile.yaml → re-run `cli export`
3. **DO NOT EDIT header**: installed adapter must have `<!-- GENERATED FILE. DO NOT EDIT DIRECTLY. -->` in first 20 lines
4. **Version bump on change**: increment `agent_version` in profile.yaml on any change
5. **Changelog entry required**: every version bump needs a CHANGELOG.md entry
6. **Validation before release**: run `cli validate <slug>` before marking package complete

## Supersession rule

Never silently overwrite prior profile decisions. Add a new version entry in
`provenance-ledger.md` Version History section. Old decisions stay visible.
