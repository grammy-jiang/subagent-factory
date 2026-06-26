# Changelog — test-driven-development-advisor

## 0.2.0 — 2026-06-26

### Added

- Authored the bodies of all three skills (`red-green-refactor-cycle`,
  `get-to-green-then-refactor`, `getting-to-green-strategies`) and the
  `tdd-to-do-list` reference, each grounded in this package's own
  principles / claims / evidence / source anchors (Kent Beck, *Test-Driven
  Development By Example*) — no invention, no verbatim quotation
  (`distillation-only` source; quote-scan green). Stub markers removed.
- Drift baseline stamped (`provenance.authored_from_digest`) into every
  authored doc via `cli stale --stamp`.

### Changed

- Promoted package from `status: draft` to `status: ready`; bumped
  `agent_version` 0.1.0 → 0.2.0.
- Re-exported the Claude Code adapter under the refactored factory tooling.

## 0.1.0 — 2026-06-15

Initial Tier-1 package derived from Kent Beck, *Test-Driven Development By Example*
(Addison-Wesley, 2002), `distillation-only`.

- Source: 66-page partial — Introduction + Part I (The Money Example, Ch. 1–17). Parts
  II–III absent from the source file (recorded as an evidence gap).
- Evidence chain: source map (11 candidate units), 11 claims, 11 evidence records,
  7 principles (P001, P002, P004, P006, P008, P010, P009), importance scores.
- Modes: `advise`, `review`, `compare`. No `produce`/`patch-suggest` (no patch policy).
- Profile rules grounded in the red/green/refactor cycle, the two rules, the
  work-then-clean ordering, the three get-to-green strategies, and incremental design.
- Status: `draft` (skill/reference bodies are stubs pending authoring).
