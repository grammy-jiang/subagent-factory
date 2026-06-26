# Software-Design Review — `tools/subagent_factory/cli.py`

**Document:** `tools/subagent_factory/cli.py` (827 lines, Click CLI, 21 commands — a dispatch layer delegating to `tools.subagent_factory.<module>` functions and rendering with `rich`).
**Reviewers:** `software-design` (1)
**Date:** 2026-06-26

---

## Reviewer: software-design

The reviewer treated this strictly as a structural-design review of a thin CLI dispatch layer. **Overall verdict:** healthy, well-organized layer. The flagged duplication is real but most of it is the *acceptable* kind for a CLI — each command stays flat, linear, readable in isolation. A sweeping "DRY it all" pass is **not** endorsed (would over-abstract a thin layer). Three duplications are worth fixing because they carry a correctness or maintenance risk, not merely cosmetics. Ranked by cost.

### Finding 1 — Inconsistent level→color maps are duplicated *knowledge* and have already diverged (highest cost)

- **Issue.** The level→color map is re-declared inline in ≥6 commands with divergent key sets: `selfcheck` `{"FAIL","WARNING","PASS","INFO"}` (line 103), `validate` `{"FAIL","WARN","OK"}` (line 151), `score` `{"keep","review","discard","invalid"}` (line 602), `stale` `{"STALE","WARN","INFO","OK"}` (line 702), `catalog` `{"ready","draft"}` (line 732), `corpus-health` ad-hoc green/red/yellow (line 182). `selfcheck` spells the advisory level `"WARNING"` (103) while `validate` spells it `"WARN"` (151); `selfcheck` re-declares its own verdict palette a second time at line 113.
- **Why it matters.** Duplicated *knowledge*, not just text. The "WARNING" vs "WARN" divergence proves the convention has already drifted. These maps fall back to `"white"` on an unrecognized key, so a producer-side rename silently degrades to white text with no error — a defect channel hidden in cosmetic-looking code.
- **Recommendation.** Hoist one canonical `SEVERITY_COLORS = {"FAIL":"red","WARN":"yellow","PASS":"green","OK":"green","INFO":"cyan"}` to module scope and pick a single spelling for the advisory level across producers and renderer. Keep genuinely distinct *domain* palettes (verdict `keep/review/discard/invalid` at 602; `ready/draft` at 732) as their own named constants — do not force-merge.

### Finding 2 — The findings-table render block is duplicated and one copy already differs (medium cost)

- **Issue.** `selfcheck` (97–107) and `validate` (146–153) build identical structure: a `Table` with Level/Check/Message columns, loop over `result["findings"]`, per-row color lookup, `add_row`, `console.print(t)`. They differ only in title, an extra `#`/`num` column in selfcheck, and the palette spelling from Finding 1.
- **Why it matters.** Two near-identical render blocks that have *already* diverged is the textbook signature of duplicated logic drifting apart. Any future column/styling change must be applied twice, risking a third divergence.
- **Recommendation.** Extract `render_findings_table(findings, title, *, numbered=False)` and have both commands call it with the canonical palette. **Stop there** — do NOT fold `corpus-health`, `score`, `catalog`, or `doctor` into the same helper; their distinct columns + domain palettes would force a flag-laden "generic table" abstraction that adds complexity.

### Finding 3 — Path-resolution boilerplate repeated ~17×; hoist the root, leave the rest (low cost, partial fix)

- **Issue.** `repo_root = Path(__file__).parent.parent.parent` appears in ~17 commands (35, 93, 126, 142/143, 171, 205, 240, 287, 319, 354, 465, 561, 673, 697, …); `repo_root / "subagents" / slug` follows in ~12.
- **Why it matters.** The triple `.parent.parent.parent` is structural knowledge ("where repo root sits relative to this file") repeated 17×; if the file moves, all 17 change together. The chained call is also mildly opaque. Lower cost than 1–2 because a wrong path fails loudly, not silently.
- **Recommendation.** Define module-level `REPO_ROOT = Path(__file__).resolve().parents[2]`; optionally a tiny `package_dir(slug) -> REPO_ROOT / "subagents" / slug` for the ~12 sites. Do NOT go further (base-command class / path-injecting decorator) — that would obscure the flat per-command readability that is this layer's main virtue.

### Judged FINE — do not "fix"

- **Lazy import-per-command** (18, 33, 90–91, 124, …): intentional, idiomatic — keeps `--help` and unrelated commands fast by deferring heavy imports. The repetition is the cost of that benefit; correct trade for a CLI entry point.
- **`if <fail>: print(...); sys.exit(1)`** (ingest 56, selfcheck 117, export 131, validate 159, score 618, replay-score 324/328, replay-gate 358/376, optimize-adapter 470/474, gen-behaviour-tests 568/583, stubs 677): shallow, varied per command, reads clearly inline. A one-line `die()` helper is a marginal nicety, not required.
- **Per-command flat structure** generally: each command short, linear, single-purpose — exactly what a dispatch layer should look like.

### Flagged but explicitly HANDED OFF (not decided)

- **`optimize-adapter`: 11 `@click.option` decorators, 14-parameter signature (379–442).** Past the long-parameter-list threshold, but the reviewer declined to recommend collapsing it: for a CLI command each parameter is the command's *public interface* — one documented `--flag` a user types. Bundling into an `OptimizeConfig` dataclass cleans the Python signature but does not reduce the user-facing interface surface. Whether bundling helps depends on whether the knobs cluster into meaningful sub-concepts (a "judge" group: `grader_kind`/`judge`/`judge_samples`; a "search" group: `budget`/`variants`/`minibatch`/`pool_size`/`patience`/`tol`) — a product/UX call the reviewer cannot make from the file alone. **Handoff to the CLI's UX owner.**

### Reviewer caveat

No tests appear to accompany this file. None of the three fixes change behaviour (pure extractions), so they are low-risk — **except** Finding 1's WARN/WARNING unification, which *does* change rendered output and could surface a producer-side mismatch. The owner should run a self-checking pass of the CLI's commands before/after.

---

## Cross-cutting summary

Single reviewer, so no inter-reviewer agreement/conflict to report. Top issues, in the reviewer's cost order:

1. **Severity palette drift (Finding 1)** — silent white-text degradation on key mismatch; `WARNING` vs `WARN` already diverged. Highest cost: a real defect channel.
2. **Duplicated findings-table renderer (Finding 2)** — two blocks already drifting.
3. **Repeated `repo_root` path knowledge (Finding 3)** — 17× repetition, but fails loud.

The unifying theme: the costly duplications are duplicated **knowledge** (palette conventions, repo-root location), whereas the duplications judged fine (lazy imports, exit-on-fail) are duplicated **shallow text** that aids per-command readability. The reviewer's consistent guardrail is *not* to over-abstract a thin dispatch layer.

## Prioritized action list (highest-impact first)

1. **[software-design]** Hoist one canonical `SEVERITY_COLORS` module constant; pick a single advisory spelling (`WARN` or `WARNING`) across producers + renderer. Keep distinct domain palettes (`keep/review/...`, `ready/draft`) as separate named constants. *(Behaviour-affecting — verify CLI output before/after.)*
2. **[software-design]** Extract `render_findings_table(findings, title, *, numbered=False)`; use it in `selfcheck` and `validate` only. Do not generalize to other tables.
3. **[software-design]** Define module-level `REPO_ROOT = Path(__file__).resolve().parents[2]`; optionally add `package_dir(slug)`. No base-class/decorator.
4. **[software-design — handoff]** Decide `optimize-adapter`'s option strategy (group into option clusters / dataclass / split sub-commands) as a UX call. Not a pure structural fix.
5. **[software-design — optional]** One-line `die(msg)` helper for exit-on-failure — marginal; only if the owner wants it.

*No findings were invented beyond the reviewer's output. The single reviewer declined to decide the `optimize-adapter` parameter question and handed it to the CLI UX owner.*
