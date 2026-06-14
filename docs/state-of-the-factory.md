# State of the factory

Orientation doc — what this factory is, what's built, what's open. Start here, then follow the
links. Snapshot: 2026-06-14.

## What it is

A local Claude Code factory that turns books/PDFs into reusable **expert subagent packages**. One
pipeline, every step gated:

```
source → claims → evidence → principles → behaviour-tests → adapter
         (atomic)  (support)  (operational) (golden/negative) (Claude Code runtime)
```

Canonical source of truth per subagent is `subagents/<slug>/profile.yaml`; the runnable adapter
(`.claude/agents/generated/<slug>.md`) is derived. Generated packages are gitignored **output** —
regenerable; the factory **code** (tools/schemas/templates/skills) is tracked.

**Core discipline:** every LLM step passes a *deterministic gate* before it can affect the adapter.
LLM proposes, deterministic decides + records provenance. Faithfulness rule: no generated rule may be
stronger than its source support.

## At a glance

- **23 packages**, all validating. **407 tests**, mypy + ruff clean.
- **64 tool modules**, **15 schemas**, **16 build-step specs** (`docs/enhancement-steps/`).
- Build steps **0–10 + 20** implemented (see `docs/enhancement-steps/README.md`).

## Capabilities (the three research tracks)

Status + plan in `docs/enhancement-steps/research-integration-plan.md`.

| track | what | status |
|---|---|---|
| **A — instruction-induction** | shape the adapter: example-by-utility (A1), replay gate (A2), compiled must-hold invariant layer (A3+A5), failure-recovery example gate (A4) | ✅ **A1–A5 done** |
| **B — agent-benchmarking** | measure output quality: Bradley-Terry + bootstrap CI ranking (B1), position-swapped judging (B2), cross-family judge ensemble + self-audit (B3, incl. codex/gpt-5.5), gold-set κ harness (B4), cost-parity (B5), deterministic hedge wiring (B6) | ✅ done **except B4 gold *data*** (human-gated) |
| **C — knowledge-graph** | the Step-7 principle graph (clusters + typed-edge graph + conflict log) | ✅ shipped. C1 embedding-dedup ✅ (margin-above-baseline). C3 Hearst is-a ⚠️ built but low-yield on factory data (WordNet lacks domain jargon — opt-in, not auto-wired). C2 PROV-O optional. |

## Provenance-repair toolset (deterministic)

For packages authored under older conventions (stale/slug anchors, markitdown-era sources). Full
recipe in `docs/factory-ops.md`. Decision order:

1. `remap_faithfulness_anchors` — line refs (`<sid>:L148`) → real anchors (recover, don't drop).
2. `reground_skill_anchors` — Tier-0 skills/references citing whole-source ids → top content-matched
   anchors (coarse "draws-on" provenance).
3. `reanchor_by_heading` — concept-slug claim anchors (`ch2-mirroring`) → recovered heading anchors,
   **after** re-converting the source in place with Docling (recovers the headings the slugs name).
4. `reanchor_claims` — surgical LLM (content-narrow → LLM picks the supporting span); only viable on a
   **clean** source. Last resort for headingless concepts.

Worked example: all 4 bulk-re-export failures fixed deterministically (advertising/startup-ceo via
remap, kafka via reground, negotiation via Docling re-convert + heading match) — zero model cost.

## Output-quality findings (measured, not assumed)

Method + findings in `docs/output-quality-eval.md`. The harness exists to *not* assume; twice it
declined to confirm an expected win:

- **Multi-source synthesis** delivers grounding/faithfulness (deterministic, judge-independent) but
  **not** measurably better advice (judge-family-dependent; Claude tie, Codex leans longer).
- **Invariant layer (A3/A5)** — benefit is **package-dependent** (n=3, 2 graders): big lift to a weak
  adapter (mysql-at-scale 0.366→~0.9), mild mid-range (software-design +0.084), slight *regression* to
  an already-strong one (DDD 0.880). Apply where a package's behaviour-test baseline is weak, not
  blanket. (The two graders agree on direction → grader-robust; the semantic grader also fixed the
  coarse `must_not_do` *inversion* that scored "rejects X" as "does X".)
- **Semantic LLM grader** (`make_llm_grader`, `behaviour_replay`) is the validated, grader-robust
  instrument for adherence/advice deltas; the coarse `must_not_do` is for relative regressions only.

## What's open (highest leverage first)

1. **B4 gold data** — human-label ~10–15 A/B comparisons → judge↔human κ (breaks circular eval).
   Harness built (`gold_eval.py`); needs human time, not model budget.
2. ✅ **Baseline-gate the invariant layer** — `invariant_policy.recommend_invariants` measures the
   no-invariant replay baseline and applies the rule (attach iff baseline < 0.80, the n=3 crossover);
   `export_claude_agent` honours a profile `attach_invariants` flag. Apply per package when desired.
3. ✅ **C1 embedding clustering — done, over-merge fixed.** Injectable `embedder` + validated
   `embed_minilm`; **C1(c) margin-above-baseline** (a pair must stand out above each principle's
   leave-one-out mean cosine to its cross-source peers) fixes the C1(b) raw-cosine over-merge — on a
   single-topic package the 19-principle blob becomes tight 2-member candidate pairs at every
   threshold. Defaults `cos_threshold=0.5`, `margin=0.15`. (C3 Hearst is-a still optional.)

## Where to read next

- `docs/factory-ops.md` — operate it (corpus-health, Docling, re-author, repair, validate).
- `docs/output-quality-eval.md` — judge whether an expert gives *good advice* (+ the findings above).
- `docs/enhancement-steps/README.md` — per-step build specs (0–10, 20).
- `docs/enhancement-steps/research-integration-plan.md` — A/B/C track plan + status.
- `CLAUDE.md` + `.claude/rules/` — repository boundaries, generated-artifact / rights / evidence /
  untrusted-source policies.
