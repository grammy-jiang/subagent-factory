# Step 0 — Plumbing

> Master: `docs/subagent_enhancement_build_plan.md` §8 Step 0. Depth: **full**.

## Goal
Make later steps cheap and non-breaking: a shared source-text loader, a tier
classifier, a `tier` field, and a present/tier-gated convention in the composite
gate — with **zero behaviour change** for the 15 existing Tier-0 packages.

## New files
| Path | Kind | Responsibility |
|------|------|----------------|
| `tools/subagent_factory/source_text.py` | tool (deterministic) | Shared loader: `load_source_texts(base, source_ids=None)`, `normalize_ws(text)`, `contains_span(probe, source_texts)`. Extracted from `quote_scan.py`. |
| `tools/subagent_factory/classify_tier.py` | tool (deterministic) | `classify_tier(base) -> int` (0/1/2) from manifest source count + conversion-report length; `write_tier(base)` stamps `tier:` into `profile.yaml`. |
| `schemas/` (edit) | — | Add optional `tier` (integer 0–2, default 0) to the profile shape used by self-check. |
| `tests/fixtures/tier/` | fixtures | Minimal packages: 1-short-source→0, long-source→1, 2-source→2. |

## Reuse
- `quote_scan.py` — move `_load_source_texts`, `_normalize_ws`, `_is_verbatim` into
  `source_text.py`; `quote_scan` then imports them. **Behaviour-preserving refactor.**
- `source-pack.manifest.yaml` (source count), `sources/reports/*.conversion-report.md`
  (length/pages) for tier classification.

## Gate wiring (`validate_generated_package.py`)
Add two helpers near the top of `validate_generated_package`:

```python
def _tier(base) -> int:
    prof = yaml.safe_load((base / "profile.yaml").read_text()) or {}
    return int(prof.get("tier", 0) or 0)

# present-gated + tier-gated artifact check
def _require(base, rel_path, min_tier, validate_fn, findings, tier):
    p = base / rel_path
    if p.exists():
        findings.extend(validate_fn(p))          # validate if present (any tier)
    elif tier >= min_tier:
        fail("tier-artifact", f"tier {tier} requires {rel_path} (missing)")
    # else: not present, not required → silent OK
```

No new artifact is *required* yet (Steps 1+ pass `min_tier`). This step only adds the
mechanism. **`tier` absent ⇒ 0 ⇒ nothing new required** → existing packages untouched.

## LLM ↔ deterministic split
All deterministic. No skills/agents.

## Tier thresholds (initial, revisable)
| Tier | Rule (deterministic) |
|------|----------------------|
| 0 | 1 source AND total converted length < ~15k words |
| 1 | total length ≥ ~15k words OR a single book-length source |
| 2 | ≥ 2 sources flagged high-value (manifest) |

Thresholds are an **open decision** (master §10) — calibrate `classify_tier` over the
existing corpus before trusting Tier-1 promotion. Default stays 0 if unsure.

## Fixtures
- `tests/test_source_text.py` — parity: `source_text.load_source_texts` returns the same
  dict `quote_scan` produced before the refactor on a known package.
- `tests/test_classify_tier.py` — the 3 fixtures map to 0/1/2.

## Exit criteria + verify
1. `quote_scan` behaviour unchanged — its existing tests still pass.
2. `classify_tier` returns 0/1/2 on fixtures.
3. **All 15 packages still pass** (the load-bearing check):
   ```bash
   for d in subagents/*/; do python -m tools.subagent_factory.validate_generated_package "$d" || echo "FAIL $d"; done
   ```
   Expect zero `FAIL`.
4. `make verify` (or the repo's lint/test target) clean.

## Caveats
- Tier thresholds are provisional; do not auto-promote existing packages — leave them
  Tier 0 (no `tier:` field ⇒ 0).

## Risks
- **Refactor regresses `quote_scan`.** Mitigation: keep the moved functions byte-identical;
  `quote_scan` imports them; run its tests first (red→green).
- **Stamping `tier:` into 15 profiles** would be a change to canonical artifacts — **don't**.
  `classify_tier` is opt-in; existing packages stay implicit Tier 0.
