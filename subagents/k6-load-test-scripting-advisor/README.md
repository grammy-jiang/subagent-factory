# k6 Load-Test Scripting Advisor

Generated subagent package. **Canonical source of truth:** `profile.yaml`.
Do not edit the installed adapter (`.claude/agents/generated/k6-load-test-scripting-advisor.md`) by hand.

## What it does

Advises on the [k6](https://k6.io) open-source load-testing tool: explains k6 terminology and
guides how to configure a k6 test script and its options object — virtual users, iterations,
duration, stages, scenarios, thresholds, checks, and metrics — so a desired load profile and
pass/fail criteria are expressed correctly.

## Modes

- **advise** — recommend how to express a load profile or pass/fail criteria in k6 options,
  scenarios, thresholds, or checks.
- **compare** — contrast related k6 constructs (percentiles, the four metric types, checks vs
  thresholds) to help choose the right one.

## When to use / not use

See `when_to_use` and `when_not_to_use` in `profile.yaml`. In short: use it for **writing and
configuring k6 scripts**; do **not** use it to compare k6 against other tools, to tune the
system-under-test, or for k6 features the source cheat sheet does not cover (distributed/cloud
execution, custom metrics, xk6, CI).

## Tier

**Tier 1** — profile is grounded in an atomic evidence-backed principles layer
(`principles/principles.yaml`, k6-p001–k6-p008), derived from a claims layer
(`analysis/claims.jsonl`) with full provenance to the Docling-converted source
(source_id `k6-guideline-20260612112658`, anchors h0000–h0063).

## Source

| Source | Author | Rights | Conversion |
|--------|--------|--------|------------|
| Most commonly used terms in K6 | Anshita Bhasin | distillation-only (no verbatim quotation) | Docling (52 heading anchors) |

Authoritative reference for k6 behaviour is the official k6 documentation (k6.io); this package
is distilled from a secondary cheat-sheet summary.

## Status

`draft` — the 4 skills and 1 reference listed in `profile.yaml knowledge_partition` need their
bodies re-authored to cite the new Docling heading anchors from the re-ingested source
(k6-guideline-20260612112658). This is a SUPERSESSION re-author from v0.2.0, which was grounded
to an empty-anchor MarkItDown conversion.

## Regenerate

```bash
python -m tools.subagent_factory.cli selfcheck k6-load-test-scripting-advisor
python -m tools.subagent_factory.cli export    k6-load-test-scripting-advisor
python -m tools.subagent_factory.cli validate  k6-load-test-scripting-advisor
```
