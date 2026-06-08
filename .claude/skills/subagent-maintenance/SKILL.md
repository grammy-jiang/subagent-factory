# Skill: subagent-maintenance

**Purpose:** Maintain existing generated subagents when sources, converters,
platform behavior, or requirements change. Phase 12 of the authoring cycle.

---

## Maintenance trigger types

| Trigger | Re-enter at |
|---------|-------------|
| Source content changed materially | Phase 2 (re-interrogate) |
| New source adds a mode or changes quality bar | Phase 2 → multi-source merge |
| Platform adapter format changed | adapter-export only |
| Test failure after platform update | adapter-export → validate |
| Conflict re-opened by new evidence | multi-source merge |
| Profile body became bloated | profile-generation → Phase 8 |
| Rights status changed | Phase 1 — stop distillation if rights withdrawn |

---

## Steps for adding a new source

1. Run `source-ingestion` for the new source
2. Run `source-interrogation` on new source Markdown
3. Compare interrogation with existing profile
4. Identify conflicts using Phase 7 conflict classes
5. Resolve conflicts, update `profile.yaml`
6. Update `provenance-ledger.md` with new distillation rows
7. Append CHANGELOG entry
8. Re-run `adapter-export`
9. Re-run `validate`

---

## Steps for adapter-only update (platform change)

1. Check `.claude/agents/generated/<slug>.md` against canonical profile
2. Re-run `adapter-export`
3. Re-run `validate`

---

## Stale source policy

If a source is marked stale in the provenance ledger:
- Adapters generated from it are marked `status: stale`
- Human review required before next release
