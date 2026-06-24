# Cross-source conflict log — software-design

Generated from `principle-graph.json` (Step 7). Cross-source `conflicts` edges are kept as **multi-truth**: both principles stay valid, scoped by the resolution. Never silently dropped.

- conflicts: 1 (resolved/scoped: 1, **OPEN: 0**)

## Resolved / scoped (multi-truth)

### P025 ↔ P011
- **P025:** Treat patterns as a shared vocabulary and as targets for refactoring; classify a recurring problem by purpose (creational/structural/behavioral) and scope (class/object) to narrow the candidate patterns.
- **P011:** Be only as generic as present known needs require; treat any design that adds complexity instead of removing it as overengineering.
- **Resolution:** Scope by present need: introduce a pattern only when a problem actually recurs now (refactor TO patterns), never speculatively. With that gate both rules agree.

