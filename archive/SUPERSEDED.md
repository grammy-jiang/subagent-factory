# Superseded subagent packages

Visible record of retired packages (generated-artifact-policy supersession rule: old decisions
stay visible, never silently deleted). Full package contents are preserved in the dated zip.

## 2026-06-20 — software-design consolidation (3 → 1)

Retired in favour of the consolidated, topic-scoped **`software-design`** package (Tier 2,
multi-source: A Philosophy of Software Design + Code Simplicity + Clean Code + Refactoring + GoF
Design Patterns). The three retired packages were each book-scoped and overlapped heavily.

| Retired package | Source(s) | Folded into |
|-----------------|-----------|-------------|
| `software-design-reviewer` | A Philosophy of Software Design (Ousterhout) | `software-design` |
| `software-simplicity-advisor` | Code Simplicity (Kanat-Alexander) | `software-design` |
| `software-design-simplicity-advisor` | Code Simplicity + A Philosophy of Software Design (fused) | `software-design` |

- **Backup:** `archive/superseded-design-2026-06-20.zip` (189 files; full package dirs incl.
  profile.yaml, provenance-ledger.md, principles, evidence, skills, tests).
- **Adapters removed:** `.claude/agents/generated/{software-design-reviewer,software-simplicity-advisor,software-design-simplicity-advisor}.md`.
- **Restore:** `unzip archive/superseded-design-2026-06-20.zip` from the repo root, then
  `python -m tools.subagent_factory.cli export <slug>`.
- Residual mentions in `docs/` and synthetic test fixtures are historical records, intentionally
  left intact.

## 2026-06-20 — postgresql-sqlite-advisor supersedes postgres-query-performance-advisor

Retired in favour of **`postgresql-sqlite-advisor`** (Round 3) — a database schema-design &
fundamentals advisor (Elmasri, Silberschatz, Database Design for Mere Mortals) fitted to both
PostgreSQL and SQLite, which covers Postgres query performance plus much more.

| Retired package | Source | Folded into |
|-----------------|--------|-------------|
| `postgres-query-performance-advisor` | Best Practices for Optimizing Postgres Query Performance | `postgresql-sqlite-advisor` |

- **Backup:** `archive/superseded-postgres-query-performance-advisor-2026-06-20.zip`.
- **Adapter removed:** `.claude/agents/generated/postgres-query-performance-advisor.md`.
- mysql-at-scale-operations + mysql-replication-internals left intact (not in scope).
