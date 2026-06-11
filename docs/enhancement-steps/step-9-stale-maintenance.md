# Step 9 — Stale Maintenance Trigger

> Master: extends `docs/subagent_enhancement_build_plan.md` (post-roadmap). Depth: **full**.
> Realizes **process-cycle Phase 12** (Maintenance) for authored skill/reference bodies, and
> activates the `stale` value already in the `authored-doc-v1` `status` enum (Step 8).

## Goal

Detect when an authored skill/reference **body has drifted from its grounding** — the
principles/claims it was authored from changed (e.g. a source was re-ingested and principles
re-derived), or its source was replaced — flag it `stale`, and route it back through Step 8
re-authoring. Deterministic, git-safe (no mtimes), non-breaking (advisory WARN, never FAIL).

## Problem this fixes

`authored-doc-v1.status` allows `stale`, and `subagent-maintenance` exists, but **nothing
detects drift or sets `stale`** — the enum is a dangling affordance. When a Tier-1 source is
re-ingested, claims/evidence/principles re-derive, but skill bodies authored from the old
principles silently keep `status: ready` with stale content. This step closes that loop.

## Core signal — provenance digest drift

When `author-skills` finishes, each `ready` doc is stamped with
`provenance.authored_from_digest`: a sha256 over the **current statements** of the principles +
claims it cites (canonical, order-independent). A drift check recomputes that digest from
today's `principles.yaml` / `claims.jsonl`; **mismatch → stale**. This captures exactly the
re-ingest → re-derive → principle-statement-changed chain. Secondary signals: a cited ID now
missing → stale; `sources/original/*` sha ≠ manifest sha → WARN (source replaced in place).

Digest (deterministic):

```
parts = []
for pid in sorted(provenance.principles):  parts += f"P:{pid}\x1f{principle_statement[pid] or '<MISSING>'}"
for cid in sorted(provenance.claims):       parts += f"C:{cid}\x1f{claim_statement[cid] or '<MISSING>'}"
authored_from_digest = sha256("\x1e".join(parts))
```

Empty provenance (Tier-0 bodies, grounded on source/always_on not principles) → constant
digest → never auto-stale; accepted (matches the Step-8 "Tier-0 bodies are thinner" caveat).

## New / changed files

| Path | Kind | Responsibility |
|------|------|----------------|
| `schemas/authored-doc-v1.schema.json` (edit) | schema | add optional `provenance.authored_from_digest` (string) — backward-compatible |
| `tools/subagent_factory/detect_stale.py` | tool | `detect_stale(base) -> [(level, artifact, reason)]`; CLI: **check** (default), `--stamp`, `--mark` |
| `tools/subagent_factory/validate_generated_package.py` (edit) | gate | WARN block from `detect_stale` (never FAIL) |
| `tools/subagent_factory/validate_skill_authoring.py` (edit) | validator | classify `status: stale` as authored-but-flagged → WARN (not FAIL), so a marked-stale doc never hard-blocks a `ready` package |
| `tools/subagent_factory/cli.py` (edit) | cli | `cli stale <slug> [--mark]` ergonomic wrapper |
| `.claude/skills/author-skills/SKILL.md` (edit) | skill | final step `detect_stale --stamp`; treat `stale` like `stub` when re-authoring |
| `.claude/skills/subagent-maintenance/SKILL.md` (edit) | skill | run `detect_stale --check` / `--mark` as the maintenance entry point |
| `.claude/skills/author-subagent/SKILL.md` (edit, Step 8.7) | skill | stamp digests after authoring |
| `tests/subagent_factory/test_detect_stale.py` | tests | stamp→check clean; mutate principle → stale; removed id → stale; no-baseline → INFO |

## CLI modes

- `detect_stale <slug>` (check) → report `STALE` / `WARN` / `INFO` / `OK`; exit 0 (advisory).
- `detect_stale <slug> --stamp` → write `authored_from_digest` into every `ready` doc from
  current upstream (deterministic; no LLM). Called by `author-skills` as its last step.
- `detect_stale <slug> --mark` → flip drifted `ready` docs to `status: stale` (write).

Levels: `STALE` (digest mismatch / cited id missing), `WARN` (source sha drift), `INFO`
(`ready` doc with no baseline digest — authored before drift-tracking; re-stamp to enable),
`OK`.

## Reuse

- `_parse_frontmatter` from `validate_skill_authoring` (frontmatter read).
- `principles.yaml` statements + `claims.jsonl` statements (same loaders as `validate_principles`/
  `validate_claims`).
- `source-pack.manifest.yaml` sha256 + `sources/original/<id>/` for source-drift.
- `authored-doc-v1` schema (the digest field).

## Gate wiring

Dedicated block in `validate_generated_package` (like the scan blocks): map
`detect_stale(base)` → `warn` for STALE/WARN, `ok`/skip for INFO/OK. **Never FAIL** — process
cycle: a stale flag is human-reviewed before the next release, not a hard release block. The 15
draft packages have no `ready` docs → no output. caching-strategy-advisor (ready, no digest yet)
→ INFO until re-stamped.

## LLM ↔ deterministic split

100% deterministic — digesting, comparing, stamping, marking, source hashing. No LLM. (The only
LLM part is the *re-authoring* of a flagged doc, which is Step 8's existing `skill-author`.)

## Exit criteria + verify

1. `detect_stale --stamp` then `check` → all `OK`.
2. Mutate a cited principle's statement → `check` reports that doc `STALE`.
3. Remove a cited claim ID → `STALE` (missing).
4. `ready` doc with no digest → `INFO` no-baseline (not stale).
5. `--mark` flips drifted docs to `status: stale`; re-running Step 8 author-skills re-authors +
   re-stamps → clean.
6. All packages still validate (WARN-only); `make verify` green.
7. Proof: stamp `caching-strategy-advisor`'s 12 ready docs; mutate one principle → detect; re-author → clean.

## Caveats

- **Tier-0 bodies (empty provenance) are not drift-tracked** — no principle/claim baseline.
  Acceptable; they are thin by design.
- **Digest tracks statement text, not semantics** — a no-op reword of a principle marks dependents
  stale (false positive). Cheap to clear (re-stamp/re-author); err toward over-flagging.
- **Source-drift only fires if `sources/original/` is present** and changed in place; the normal
  path is re-ingest (new sha in manifest), which changes principles → caught by the digest.

## Risks

- **Frontmatter rewrite on `--stamp`/`--mark`** round-trips YAML (re-dumps the frontmatter block,
  body preserved verbatim). Acceptable: docs are generated artifacts. Mitigation: body is never
  touched; only the frontmatter block is re-emitted.
- **Double-signal** with `validate_skill_authoring` (marked-stale) vs `detect_stale` (undeclared
  drift): intentional and complementary — both WARN, neither FAILs.
