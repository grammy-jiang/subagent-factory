"""Live-model measurement CLI commands (behaviour replay, optimize, grounding).

Registered on the main group in cli.py via add_command — flat command names unchanged.
"""

import sys
from dataclasses import dataclass
from pathlib import Path

import click

from tools.subagent_factory.cli_support import console, subagent_path


def _load_adapter_and_tests(slug):
    """Resolve SLUG → (package dir, adapter path, flattened behaviour-tests), or ``sys.exit(1)``.

    The shared preamble of the live-measurement commands: the adapter file must exist and the
    package must carry at least one behaviour-test, else the command prints why and exits non-zero.
    """
    from tools.subagent_factory.behaviour_replay import load_behaviour_tests

    base = subagent_path(slug)
    adapter = base / "adapters" / "claude-code" / f"{slug}.md"
    if not adapter.exists():
        console.print(f"[red]adapter not found:[/red] {adapter}")
        sys.exit(1)
    tests = load_behaviour_tests(base)
    if not tests:
        console.print(f"[yellow]no behaviour-tests under[/yellow] {base / 'tests'}")
        sys.exit(1)
    return base, adapter, tests


@click.command("replay-score")
@click.argument("slug")
@click.option("--runner", default="examples/replay-runner.sh", help="Runner script (live model).")
def cmd_replay_score(slug, runner):
    """Replay the package's behaviour-tests against its adapter and score them (LIVE model calls).

    A1/A2 execution path: runs each tests/*.yaml prompt through the adapter (as system prompt) via
    RUNNER and scores the output with the deterministic grader. Burns model calls — use deliberately.
    """
    from tools.subagent_factory.behaviour_replay import score_suite, shell_runner

    base, adapter, _tests = _load_adapter_and_tests(slug)
    r = score_suite(adapter, base, shell_runner(runner), tests=_tests)
    console.print(f"replay mean score [bold]{r['mean_score']:.2f}[/bold] over {r['n_tests']} tests")
    for tid, g in sorted(r["per_test"].items()):
        console.print(
            f"  {tid}: {g['score']:.2f}" + (f"  [red]{g['error']}[/red]" if "error" in g else "")
        )


@click.command("replay-gate")
@click.argument("slug")
@click.argument("before_adapter")
@click.argument("after_adapter")
@click.option("--runner", default="examples/replay-runner.sh", help="Runner script (live model).")
def cmd_replay_gate(slug, before_adapter, after_adapter, runner):
    """A2 assess-before-merge: FAIL if the after-adapter regresses any behaviour-test (LIVE).

    SLUG selects the behaviour-tests; BEFORE_ADAPTER and AFTER_ADAPTER are two adapter .md files
    (e.g. the installed version vs a re-exported candidate). Exit 1 when the gate fails.
    """
    from tools.subagent_factory.behaviour_replay import (
        load_behaviour_tests,
        replay_gate,
        shell_runner,
    )

    tests = load_behaviour_tests(subagent_path(slug))
    if not tests:
        console.print(f"[yellow]no behaviour-tests for[/yellow] {slug}")
        sys.exit(1)
    before = Path(before_adapter).read_text(encoding="utf-8")
    after = Path(after_adapter).read_text(encoding="utf-8")
    r = replay_gate(before, after, tests, shell_runner(runner))
    color = "green" if r["gate"] == "pass" else "red"
    console.print(
        f"replay-gate [{color}]{r['gate'].upper()}[/{color}] "
        f"(before {r['before_mean']:.2f} → after {r['after_mean']:.2f}, "
        f"net {r['net_delta']:+.2f})"
    )
    for reg in r["regressions"]:
        console.print(
            f"  [red]regress[/red] {reg['test_id']}: {reg['before']:.2f} → {reg['after']:.2f}"
        )
    for imp in r["improvements"]:
        console.print(
            f"  [green]improve[/green] {imp['test_id']}: {imp['before']:.2f} → {imp['after']:.2f}"
        )
    sys.exit(1 if r["gate"] == "fail" else 0)


@dataclass
class OptimizeConfig:
    """The optimize-adapter knobs, grouped so they ride through as one object rather than 13 params.

    Mirrors the CLI option surface 1:1 — the command unpacks its options into this and passes it on.
    """

    runner: str
    proposer: str
    budget: int
    variants: int
    minibatch: int
    pool_size: int
    patience: int
    tol: float
    grader_kind: str
    judge: str
    judge_samples: int


def _build_grader(cfg: OptimizeConfig):
    """Resolve the grader callable from the config (coarse deterministic, or live semantic judge)."""
    from tools.subagent_factory.behaviour_replay import grade_output, make_llm_grader, shell_llm

    if cfg.grader_kind == "coarse":
        return grade_output
    console.print(f"[cyan]semantic grader:[/cyan] {cfg.judge} (×{cfg.judge_samples})")
    return make_llm_grader(shell_llm(cfg.judge), samples=cfg.judge_samples)


def _report_baseline(adapter, base, run, grader_fn, tests=None):
    """--dry-run path: score the baseline suite and list each test with a pass/below-1.0 mark.

    ``tests`` may be passed pre-loaded (the caller already has the flattened suite from the shared
    preamble) so the baseline score does not re-read the same ``tests/*.yaml`` files.
    """
    from tools.subagent_factory.behaviour_replay import score_suite

    r = score_suite(adapter, base, run, grader_fn, tests=tests)
    console.print(f"baseline mean [bold]{r['mean_score']:.2f}[/bold] over {r['n_tests']} tests")
    for tid, g in sorted(r["per_test"].items()):
        mark = "[green]ok[/green]" if g["score"] >= 1.0 else "[yellow]below 1.0[/yellow]"
        err = f"  [red]{g['error']}[/red]" if "error" in g else ""
        console.print(f"  {tid}: {g['score']:.2f} {mark}{err}")


@click.command("optimize-adapter")
@click.argument("slug")
@click.option("--runner", default="examples/replay-runner.sh", help="Runner script (live model).")
@click.option(
    "--proposer", default="examples/optimize-proposer.sh", help="Proposer script (live model)."
)
@click.option("--budget", default=3, show_default=True, help="Max optimization rounds.")
@click.option("--variants", default=2, show_default=True, help="Variants proposed per round.")
@click.option(
    "--minibatch", default=0, show_default=True, help="Minibatch screen size (0 = full, no screen)."
)
@click.option("--pool", "pool_size", default=4, show_default=True, help="Beam pool size.")
@click.option(
    "--patience", default=2, show_default=True, help="Stop after N no-improvement rounds."
)
@click.option(
    "--tol",
    default=0.05,
    show_default=True,
    help="Per-test regression tolerance — absorbs the live model's sampling noise so a "
    "noise-level score dip is not counted as a regression. Use 0.0 for a deterministic runner.",
)
@click.option(
    "--grader",
    "grader_kind",
    type=click.Choice(["coarse", "llm"]),
    default="coarse",
    show_default=True,
    help="Scorer: 'coarse' = deterministic lexical proxy; 'llm' = semantic judge (judges meaning, "
    "not token overlap — needed for a MEANINGFUL gain, costs an extra judge call per test).",
)
@click.option(
    "--judge",
    default="examples/codex-judge.sh",
    show_default=True,
    help="Judge script for --grader llm. Default is cross-family (codex/gpt-5.5): a Claude judge "
    "scoring Claude output carries a same-family self-preference.",
)
@click.option(
    "--judge-samples",
    default=1,
    show_default=True,
    help="Calls per judge verdict, aggregated (route=majority, components=median). >1 damps the "
    "live judge's run-to-run variance — use 3+ for a trustworthy verdict (costs that many judge "
    "calls per test).",
)
@click.option(
    "--dry-run", is_flag=True, help="Score the baseline + list failing tests; propose nothing."
)
def cmd_optimize_adapter(
    slug,
    runner,
    proposer,
    budget,
    variants,
    minibatch,
    pool_size,
    patience,
    tol,
    grader_kind,
    judge,
    judge_samples,
    dry_run,
):
    """Step 12: tune SLUG's adapter against its behaviour-tests (LIVE model calls).

    Runs the propose->score->keep loop: scores the current adapter, asks the proposer for additive
    guidance variants, keeps a variant only if it improves with ZERO regressions (and passes the
    text-level policy gate). Writes the winner to <slug>.optimized.md for REVIEW -- it never
    overwrites the canonical adapter or profile (fold the winning edits into profile.yaml +
    re-export). --dry-run scores the baseline only (still burns baseline model calls).
    """
    from tools.subagent_factory.behaviour_replay import shell_runner
    from tools.subagent_factory.optimize_adapter import optimize_adapter_with_shell_proposer

    cfg = OptimizeConfig(
        runner=runner,
        proposer=proposer,
        budget=budget,
        variants=variants,
        minibatch=minibatch,
        pool_size=pool_size,
        patience=patience,
        tol=tol,
        grader_kind=grader_kind,
        judge=judge,
        judge_samples=judge_samples,
    )

    base, adapter, tests = _load_adapter_and_tests(slug)
    base_text = adapter.read_text(encoding="utf-8")
    run = shell_runner(cfg.runner)
    grader_fn = _build_grader(cfg)

    if dry_run:
        _report_baseline(adapter, base, run, grader_fn, tests=tests)
        return

    res = optimize_adapter_with_shell_proposer(
        base_text,
        tests,
        run,
        cfg.proposer,
        grader=grader_fn,
        n_variants=cfg.variants,
        budget=cfg.budget,
        minibatch=(cfg.minibatch or None),
        pool_size=cfg.pool_size,
        patience=cfg.patience,
        tol=cfg.tol,
    )
    color = "green" if res["improved"] else "yellow"
    console.print(
        f"optimize-adapter [{color}]{'IMPROVED' if res['improved'] else 'no gain'}[/{color}] "
        f"baseline {res['baseline_mean']:.2f} → winner {res['winner_mean']:.2f} "
        f"({res['rounds_used']} rounds, {res['eval_calls']} eval calls)"
    )
    if res["improved"]:
        out = adapter.parent / f"{slug}.optimized.md"
        out.write_text(res["winner_text"], encoding="utf-8")
        console.print(f"[green]winner written for review:[/green] {out}")
        console.print(
            "[dim]review the diff, fold the winning edits into profile.yaml, then re-export.[/dim]"
        )
    else:
        console.print(
            "[dim]no variant beat the baseline without regressions; adapter unchanged.[/dim]"
        )


@click.command("gen-behaviour-tests")
@click.argument("slug")
@click.option(
    "--ideator",
    default=None,
    help="Ideator script for natural / hard-negative prompts (LLM, e.g. "
    "examples/behaviour-test-ideator.sh). Omit for template-mode (deterministic, no model calls).",
)
@click.option(
    "--candidates",
    default=1,
    show_default=True,
    help="Ideate this many prompts per cell and keep the most novel (rare-weighted; needs --ideator "
    "+ an embedder to bite). >1 costs that many ideator calls per cell.",
)
@click.option(
    "--validate/--no-validate", default=True, help="Run the coverage validator after writing."
)
def cmd_gen_behaviour_tests(slug, ideator, candidates, validate):
    """Step 11: generate a behaviour-test suite (golden / negative-routing / missing-context).

    Reads the package's principles and writes tests/behaviour-tests.yaml. Template-mode by default
    (no model calls); --ideator wires an LLM to write realistic prompts and hard-negative
    out-of-scope requests; --candidates N ideates N per cell and keeps the most novel.
    """
    from tools.subagent_factory.gen_behaviour_tests import (
        gen_behaviour_tests,
        load_principles,
        shell_ideator,
        write_suite,
    )
    from tools.subagent_factory.validate_behaviour_test_coverage import (
        validate_behaviour_test_coverage,
    )

    base = subagent_path(slug)
    principles = load_principles(base)
    if not principles:
        console.print(
            f"[yellow]no principles under[/yellow] {base / 'principles' / 'principles.yaml'}"
        )
        sys.exit(1)
    ide = shell_ideator(ideator) if ideator else None
    suite = gen_behaviour_tests(principles, slug, ideator=ide, n_candidates=candidates)
    out = write_suite(base, suite)
    n = sum(
        len(suite.get(s, []))
        for s in ("golden_tests", "negative_routing_tests", "missing_context_tests")
    )
    mode = f"ideator={ideator}" if ideator else "template-mode"
    console.print(f"[green]wrote {n} behaviour tests[/green] ({mode}) → {out}")
    if validate:
        errs = validate_behaviour_test_coverage(out)
        if errs:
            for e in errs:
                console.print(f"  [red]{e}[/red]")
            sys.exit(1)
        console.print("[green]coverage validator PASS[/green]")


@click.command("ask-gate")
@click.argument("slug")
@click.option(
    "--strict",
    is_flag=True,
    help="Exit 1 if the gate would silently commit on any missing-context test, OR the test suite is "
    "unreadable / ambiguous. Opt-in only — NOT a package-validity gate (Step-13 is measured, not "
    "enforced); it never runs in validate.",
)
def cmd_ask_gate(slug, strict):
    """Step 13: run the deterministic Answer/Ask/Abstain gate over SLUG's OWN behaviour tests (no model calls).

    Silent-commit guard: every missing-context test omits the required context it declares
    (must_ask_for), so the gate MUST ask — a test it would answer instead is a false-fill (the prompt
    lexically names the slot). Over-ask diagnostic (packages with answerable twins): each twin
    supplies that context and ideally makes the gate answer; because slot-fill is a lexical
    approximation, a twin that signals sufficiency in prose reads as an over-ask, so this is a
    diagnostic, not a failure. Report-only by default; --strict fails on a silent commit or a broken suite.
    """
    from tools.subagent_factory.ask_gate import evaluate_tests
    from tools.subagent_factory.behaviour_replay import load_gate_tests

    base = subagent_path(slug)
    missing_context, twins, problems = load_gate_tests(base)
    # Surface a corrupted / ambiguous suite — never let it silently shrink into a false "clean" or a
    # false "no opt-in" (a green-but-smaller run is the silent overconfidence this gate exists to catch).
    for p in problems:
        console.print(f"  [red]suite problem[/red] {p}")
    if not missing_context and not twins:
        if problems:  # broken test files, not a genuine no-opt-in → fail loud under --strict
            console.print("[red]ask-gate: the test suite is unreadable — nothing evaluated.[/red]")
            if strict:
                sys.exit(1)
            return
        console.print(
            f"[yellow]no missing-context tests or twins under[/yellow] {base / 'tests'} — "
            "package does not opt into the ask-gate"
        )
        return
    r = evaluate_tests(missing_context, twins)
    sc, oa = r["silent_commit"], r["over_ask"]
    # 0/0 is not a verified pass — don't paint it green (it looks identical to a suite that ran).
    color = "yellow" if sc["total"] == 0 else ("green" if not sc["misses"] else "red")
    console.print(
        f"ask-gate silent-commit guard [{color}]{sc['asked']}/{sc['total']}[/{color}] "
        f"missing-context tests → ask (ASK-F1 {sc['f1']['f1']})"
    )
    for m in sc["misses"]:
        console.print(
            f"  [red]silent-commit[/red] {m['test_id']}: gate would {m['action']} "
            "(prompt lexically fills the declared slot)"
        )
    if oa["total"]:
        console.print(
            f"[dim]over-ask diagnostic (lexical approximation): answered {oa['answered']}/{oa['total']} "
            f"twins; {len(oa['over_asked'])} lexical over-ask — twins whose sufficiency is not "
            "lexically aligned with the declared slots (typical of template-mode tests).[/dim]"
        )
    # Fail closed under --strict on a silent commit OR an unresolved suite problem — both are the
    # false-confidence this gate exists to prevent.
    if strict and (sc["misses"] or problems):
        sys.exit(1)


@click.command("grounding-check")
@click.argument("slug")
@click.argument("review")
@click.argument("doc", required=False)
@click.option(
    "--record", "do_record", is_flag=True, help="Append this coverage to the calibration baseline."
)
def cmd_grounding_check(slug, review, doc, do_record):
    """Score a review's grounding vs the subagent's source; name cross-source borrows.

    SLUG = subagent; REVIEW = its review output file; DOC (optional) = the reviewed document
    (its quoted nouns are excluded). Cross-source borrows name the source to add (multi-source).
    Coverage is shown against the recorded calibration baseline (the rank is the signal, not %).
    """
    from tools.subagent_factory.grounding_check import (
        baseline_band,
        grounding_check,
        record_baseline,
    )

    r = grounding_check(subagent_path(slug), review, doc)
    if not r.get("scored", r["coverage"] is not None):
        console.print(
            "[yellow]grounding coverage: n/a[/yellow] — no distinctive concept vocabulary in the "
            f"review (all {r['n_generic_dropped']} generic / {r['n_doc_quoted_dropped']} doc-quoted "
            "dropped). Nothing to score; not recorded to baseline."
        )
        return
    console.print(
        f"grounding coverage [bold]{r['coverage']:.0%}[/bold] "
        f"({r['n_grounded']}/{r['n_concept_terms']} distinctive concept bigrams grounded; "
        f"{r['n_leak']} leak candidates; {r['n_generic_dropped']} generic dropped; "
        f"{r['n_doc_quoted_dropped']} doc-quoted dropped)"
    )
    band = baseline_band(r["coverage"])
    if band:
        console.print(
            f"  vs baseline (n={band['n']}): floor {band['floor']:.0%} / "
            f"median {band['median']:.0%} / ceiling {band['ceiling']:.0%} "
            f"— this run {band['percentile']}th pct"
        )
    for bg, n, sibs in r["cross_source_terms"]:
        console.print(f"  [yellow]borrow[/yellow] x{n} {bg} <- {', '.join(sibs)}")
    if r["suggested_sources"]:
        console.print(
            "suggested source(s) to add: "
            + ", ".join(f"{s}(+{w})" for s, w in r["suggested_sources"])
        )
    if do_record:
        record_baseline(slug, r["coverage"], doc)
        console.print(f"  [green]recorded[/green] {slug} coverage to grounding baseline")


@click.command("grounding-richness")
@click.argument("slug")
@click.option(
    "--vs", "vs_dir", default=None, help="Another package dir to diff against (before/after gate)."
)
def cmd_grounding_richness(slug, vs_dir):
    """Deterministic grounding SIZE (claims/principles/grounded vocab) — run-independent.

    The reliable strengthen keep/revert gate: adding a source must GROW these, never shrink
    (unlike review-coverage, which is stochastic). With --vs <dir>, prints the delta + PASS/FAIL.
    """
    from tools.subagent_factory.grounding_check import grounding_richness

    cur = grounding_richness(subagent_path(slug))
    console.print(
        f"{slug}: claims={cur['claims']} principles={cur['principles']} "
        f"uni={cur['grounded_unigrams']} bi={cur['grounded_bigrams']}"
    )
    if vs_dir:
        old = grounding_richness(vs_dir)
        d = {k: cur[k] - old[k] for k in cur}
        console.print(
            f"  vs {vs_dir}: Δclaims={d['claims']:+d} Δprinciples={d['principles']:+d} "
            f"Δuni={d['grounded_unigrams']:+d} Δbi={d['grounded_bigrams']:+d}"
        )
        grew = cur["claims"] >= old["claims"] and cur["grounded_bigrams"] >= old["grounded_bigrams"]
        console.print(f"  gate: {'PASS (grew/held)' if grew else 'FAIL (shrank)'}")


COMMANDS = [
    cmd_replay_score,
    cmd_replay_gate,
    cmd_optimize_adapter,
    cmd_gen_behaviour_tests,
    cmd_ask_gate,
    cmd_grounding_check,
    cmd_grounding_richness,
]
