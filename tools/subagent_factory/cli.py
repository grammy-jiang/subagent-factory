"""CLI entry point for subagent-factory tools."""

import sys
from pathlib import Path

import click
from rich.console import Console
from rich.table import Table

console = Console()


@click.group()
def main():
    """Subagent Factory — create Claude Code subagents from documents."""
    # Opt-in (SUBAGENT_FACTORY_USE_VENV=1): re-exec inside the managed .venv.
    # No-op by default; converters self-heal their deps in-process instead.
    from tools.subagent_factory.self_heal import ensure_environment

    ensure_environment()


@main.command("ingest")
@click.argument("source", nargs=-1, required=True)
@click.option("--slug", required=True, help="Subagent slug (kebab-case)")
@click.option("--topic", help="Topic description for create/update decision")
@click.option("--title", help="Override source title")
@click.option("--author", help="Source author")
@click.option("--year", type=int, help="Source publication year")
@click.option("--rights", default="distillation-only", help="Rights status")
def cmd_ingest(source, slug, topic, title, author, year, rights):
    """Ingest one or more source files into a subagent package."""
    from tools.subagent_factory.ingest_source import ingest_source

    repo_root = Path(__file__).parent.parent.parent
    subagent_dir = repo_root / "subagents" / slug
    subagent_dir.mkdir(parents=True, exist_ok=True)

    for src in source:
        console.print(f"[bold]Ingesting:[/bold] {src}")
        result = ingest_source(
            src,
            subagent_dir,
            slug,
            title=title,
            author=author,
            year=year,
            rights_status=rights,
        )
        if result.get("error"):
            console.print(f"[red]ERROR:[/red] {result['error']}")
            if result.get("needs_auth"):
                console.print(
                    "[yellow]This URL requires authentication. Provide a local downloaded copy.[/yellow]"
                )
            sys.exit(1)

        if result.get("already_ingested"):
            console.print(
                f"[yellow]SKIP:[/yellow] source already ingested as source_id={result['source_id']} (sha256 match)"
            )
            continue

        console.print(f"[green]OK:[/green] source_id={result['source_id']}")
        for dup in result.get("duplicate_source_slugs", []):
            console.print(
                f"[yellow]WARNING: DUPLICATE-SOURCE:[/yellow] identical content (sha256) already "
                f"ingested under slug '{dup['slug']}' (source_id={dup['source_id']}). "
                "Confirm a genuinely distinct role before authoring, or update that package instead."
            )
        cr = result["conversion_result"]
        console.print(
            f"  anchors={result['anchor_count']}  assets={result['asset_count']}  converter={cr.get('converter_used')}"
        )
        if cr.get("is_scanned"):
            console.print("[yellow]WARN: Possible scanned PDF — OCR may be needed[/yellow]")
        status = cr.get("conversion_status")
        if status and status != "ok":
            console.print(
                f"[yellow]WARN: conversion_status={status} — flagged for human review[/yellow]"
            )
            for reason in cr.get("quality", {}).get("reasons", []):
                console.print(f"  [yellow]- {reason}[/yellow]")


@main.command("selfcheck")
@click.argument("slug")
def cmd_selfcheck(slug):
    """Run the Phase 8 profile self-check gate and write tests/test-results.md."""
    from tools.subagent_factory.profile_self_check import profile_self_check
    from tools.subagent_factory.run_tests import write_test_results

    repo_root = Path(__file__).parent.parent.parent
    subagent_dir = repo_root / "subagents" / slug
    result = profile_self_check(subagent_dir)

    t = Table(title=f"Phase 8 Self-Check: {slug}")
    t.add_column("#", justify="right")
    t.add_column("Level", style="bold")
    t.add_column("Check")
    t.add_column("Message")
    for f in result["findings"]:
        color = {"FAIL": "red", "WARNING": "yellow", "PASS": "green", "INFO": "cyan"}.get(
            f["level"], "white"
        )
        t.add_row(str(f["num"]), f"[{color}]{f['level']}[/{color}]", f["check"], f["message"])
    console.print(t)

    results_path = write_test_results(subagent_dir, self_check_result=result)
    console.print(f"[green]Test results written:[/green] {results_path}")

    verdict = result["verdict"]
    vcolor = {"FAIL": "red", "WARNING": "yellow", "PASS": "green"}.get(verdict, "white")
    console.print(f"Phase 8 verdict: [{vcolor}]{verdict}[/{vcolor}]")
    if verdict == "FAIL":
        console.print("[red]Gate FAILED — do not export adapter until fixed.[/red]")
        sys.exit(1)


@main.command("export")
@click.argument("slug")
def cmd_export(slug):
    """Export subagent package to Claude Code adapter."""
    from tools.subagent_factory.export_claude_agent import export_claude_agent

    repo_root = Path(__file__).parent.parent.parent
    subagent_dir = repo_root / "subagents" / slug
    result = export_claude_agent(subagent_dir)
    if result.get("error"):
        console.print(f"[red]ERROR:[/red] {result['error']}")
        sys.exit(1)
    console.print(f"[green]Adapter exported:[/green] {result['adapter_path']}")
    console.print(f"[green]Installed:[/green] {result['installed_path']}")


@main.command("validate")
@click.argument("slug")
def cmd_validate(slug):
    """Validate a generated subagent package."""
    from tools.subagent_factory.validate_generated_package import validate_generated_package

    repo_root = Path(__file__).parent.parent.parent
    subagent_dir = repo_root / "subagents" / slug
    result = validate_generated_package(subagent_dir)

    t = Table(title=f"Validation: {slug}")
    t.add_column("Level", style="bold")
    t.add_column("Check")
    t.add_column("Message")
    for f in result["findings"]:
        color = {"FAIL": "red", "WARN": "yellow", "OK": "green"}.get(f["level"], "white")
        t.add_row(f"[{color}]{f['level']}[/{color}]", f["check"], f["message"])
    console.print(t)

    if result["passed"]:
        console.print("[green]VALIDATION PASSED[/green]")
    else:
        console.print("[red]VALIDATION FAILED[/red]")
        sys.exit(1)


@main.command("corpus-health")
@click.option("--json", "as_json", is_flag=True, help="Emit JSON instead of a table.")
def cmd_corpus_health(as_json):
    """Audit every generated package's structural health (converter, anchors, claims, flags)."""
    import json as _json
    from collections import Counter

    from tools.subagent_factory.corpus_health import scan_corpus

    repo_root = Path(__file__).parent.parent.parent
    rows = scan_corpus(repo_root / "subagents")
    if as_json:
        click.echo(_json.dumps(rows, indent=2))
        return

    t = Table(title=f"Corpus health ({len(rows)} packages)")
    for col in ("slug", "tier", "status", "conv", "anchors", "type", "claims", "dead", "health"):
        t.add_column(col)
    for r in rows:
        bad = {"empty-anchors", "dead-refs"} & set(r["health"])
        color = "green" if r["health"] == ["ok"] else "red" if bad else "yellow"
        t.add_row(
            r["slug"],
            str(r["tier"]),
            str(r["status"]),
            r["converter"],
            str(r["anchors"]),
            r["anchor_type"],
            str(r["claims"]),
            str(r["dead_refs"]),
            f"[{color}]{','.join(r['health'])}[/{color}]",
        )
    console.print(t)
    fc = Counter(f for r in rows for f in r["health"])
    console.print("summary: " + "  ".join(f"{k}={v}" for k, v in sorted(fc.items())))


@main.command("repair-faithfulness")
@click.argument("slug")
def cmd_repair_faithfulness(slug):
    """Strip invalid source_anchors from a faithfulness report (quarantine to a sidecar)."""
    from tools.subagent_factory.repair_faithfulness_report import repair_faithfulness_report

    repo_root = Path(__file__).parent.parent.parent
    rp = repo_root / "subagents" / slug / "reports" / "faithfulness-report.yaml"
    if not rp.exists():
        console.print(f"[yellow]No faithfulness report at {rp}[/yellow]")
        return
    res = repair_faithfulness_report(rp)
    if res["changed"]:
        console.print(
            f"[green]Repaired:[/green] dropped {res['n_dropped']} invalid anchor ref(s) "
            "→ reports/faithfulness-repair.yaml"
        )
    else:
        console.print("[green]Clean:[/green] no invalid anchor refs")


@main.command("grounding-check")
@click.argument("slug")
@click.argument("review")
@click.argument("doc", required=False)
def cmd_grounding_check(slug, review, doc):
    """Score a review's grounding vs the subagent's source; name cross-source borrows.

    SLUG = subagent; REVIEW = its review output file; DOC (optional) = the reviewed document
    (its quoted nouns are excluded). Cross-source borrows name the source to add (multi-source).
    """
    from tools.subagent_factory.grounding_check import grounding_check

    repo_root = Path(__file__).parent.parent.parent
    r = grounding_check(repo_root / "subagents" / slug, review, doc)
    console.print(
        f"grounding coverage [bold]{r['coverage']:.0%}[/bold] "
        f"({r['n_grounded']}/{r['n_concept_terms']} concept bigrams grounded; "
        f"{r['n_leak']} leak candidates; {r['n_doc_quoted_dropped']} doc-quoted dropped)"
    )
    for bg, n, sibs in r["cross_source_terms"]:
        console.print(f"  [yellow]borrow[/yellow] x{n} {bg} <- {', '.join(sibs)}")
    if r["suggested_sources"]:
        console.print(
            "suggested source(s) to add: "
            + ", ".join(f"{s}(+{w})" for s, w in r["suggested_sources"])
        )


@main.command("replay-score")
@click.argument("slug")
@click.option("--runner", default="examples/replay-runner.sh", help="Runner script (live model).")
def cmd_replay_score(slug, runner):
    """Replay the package's behaviour-tests against its adapter and score them (LIVE model calls).

    A1/A2 execution path: runs each tests/*.yaml prompt through the adapter (as system prompt) via
    RUNNER and scores the output with the deterministic grader. Burns model calls — use deliberately.
    """
    from tools.subagent_factory.behaviour_replay import (
        load_behaviour_tests,
        replay_suite,
        shell_runner,
    )

    repo_root = Path(__file__).parent.parent.parent
    base = repo_root / "subagents" / slug
    adapter = base / "adapters" / "claude-code" / f"{slug}.md"
    if not adapter.exists():
        console.print(f"[red]adapter not found:[/red] {adapter}")
        sys.exit(1)
    tests = load_behaviour_tests(base)
    if not tests:
        console.print(f"[yellow]no behaviour-tests under[/yellow] {base / 'tests'}")
        sys.exit(1)
    r = replay_suite(adapter.read_text(encoding="utf-8"), tests, shell_runner(runner))
    console.print(f"replay mean score [bold]{r['mean_score']:.2f}[/bold] over {r['n_tests']} tests")
    for tid, g in sorted(r["per_test"].items()):
        console.print(f"  {tid}: {g['score']:.2f}" + (f"  [red]{g['error']}[/red]" if "error" in g else ""))


@main.command("replay-gate")
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

    repo_root = Path(__file__).parent.parent.parent
    tests = load_behaviour_tests(repo_root / "subagents" / slug)
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


@main.command("score")
@click.argument("units_file")
@click.option("--worksheet", "worksheet_out", help="Write the Markdown shortlist to this path.")
def cmd_score(units_file, worksheet_out):
    """Phase 2.5 importance ranking — score candidate units before triage."""
    from tools.subagent_factory.score_extracted_units import format_worksheet, score_units_file

    result = score_units_file(units_file)
    s = result["summary"]

    t = Table(title=f"Importance ranking: {units_file}")
    t.add_column("Unit ID")
    t.add_column("Total /45", justify="right")
    t.add_column("Verdict", style="bold")
    t.add_column("Reason")
    vcolor = {"keep": "green", "review": "yellow", "discard": "blue", "invalid": "red"}
    for r in result["units"]:
        detail = "; ".join(r["reasons"] or r["errors"])
        c = vcolor.get(r["verdict"], "white")
        t.add_row(r["id"], str(r["total"]), f"[{c}]{r['verdict']}[/{c}]", detail)
    console.print(t)
    console.print(
        f"keep={s['keep']}  review={s['review']}  discard={s['discard']}  invalid={s['invalid']}"
    )

    if worksheet_out:
        Path(worksheet_out).write_text(format_worksheet(result), encoding="utf-8")
        console.print(f"[green]Worksheet written:[/green] {worksheet_out}")

    if not result["valid"]:
        console.print("[red]INVALID — fix malformed unit scores before triage.[/red]")
        sys.exit(1)


@main.command("extract-sample")
@click.argument("source")
def cmd_extract_sample(source):
    """Extract content sample for expert-role inference."""
    from tools.subagent_factory.detect_topic import (
        extract_content_sample,
        format_sample_for_inference,
    )

    sample = extract_content_sample(source)
    print(format_sample_for_inference(sample))


@main.command("search")
@click.argument("topic")
@click.option("--keywords", default="", help="Comma-separated domain keywords from content")
def cmd_search(topic, keywords):
    """Search existing subagents by topic + content keywords."""
    from tools.subagent_factory.find_related_subagents import find_related_subagents

    kw_list = [k.strip() for k in keywords.split(",") if k.strip()] if keywords else []
    candidates = find_related_subagents(topic, domain_keywords=kw_list)
    if not candidates:
        console.print("No related subagents found — create new.")
        return

    t = Table(title=f"Related subagents for: {topic}")
    t.add_column("Slug")
    t.add_column("Similarity")
    t.add_column("Recommendation")
    t.add_column("Matched terms")
    t.add_column("Role excerpt")
    for c in candidates:
        rec_color = {"update": "green", "consider-update": "yellow", "create-new": "blue"}.get(
            c["recommendation"], "white"
        )
        t.add_row(
            c["slug"],
            f"{c['similarity']:.2f}",
            f"[{rec_color}]{c['recommendation']}[/{rec_color}]",
            ", ".join(c.get("matched_terms", [])[:6]),
            c["role"][:60],
        )
    console.print(t)


@main.command("stubs")
@click.argument("slug")
def cmd_stubs(slug):
    """Scaffold skill/reference stub files from the profile's knowledge_partition."""
    from tools.subagent_factory.generate_stubs import generate_stubs

    repo_root = Path(__file__).parent.parent.parent
    result = generate_stubs(repo_root / "subagents" / slug)
    if result.get("error"):
        console.print(f"[red]ERROR:[/red] {result['error']}")
        sys.exit(1)
    console.print(
        f"[green]Stubs:[/green] skills +{result['skills_created']} "
        f"({result['skills_existing']} existing), references +{result['references_created']} "
        f"({result['references_existing']} existing)"
    )
    for p in result["skill_paths"] + result["reference_paths"]:
        console.print(f"  {p}")


@main.command("stale")
@click.argument("slug")
@click.option(
    "--stamp", is_flag=True, help="Write authored_from_digest into every ready doc (baseline)."
)
@click.option("--mark", is_flag=True, help="Flip drifted ready docs to status: stale.")
def cmd_stale(slug, stamp, mark):
    """Detect (or stamp/mark) stale authored skill/reference bodies — Step 9 maintenance."""
    from tools.subagent_factory.detect_stale import detect_stale

    repo_root = Path(__file__).parent.parent.parent
    findings = detect_stale(repo_root / "subagents" / slug, stamp=stamp, mark=mark)
    if not findings:
        console.print("[dim]no authored docs to check[/dim]")
        return
    palette = {"STALE": "red", "WARN": "yellow", "INFO": "cyan", "OK": "green"}
    for level, artifact, reason in findings:
        colour = palette.get(level, "white")
        console.print(f"[{colour}]{level:5s}[/{colour}] {artifact}: {reason}")


@main.command("catalog")
@click.option("--ready-only", is_flag=True, help="Only ready packages.")
@click.option("--md", is_flag=True, help="Emit Markdown to stdout (default: terminal table).")
def cmd_catalog(ready_only, md):
    """List generated subagents — local discovery/testing aid (writes no file)."""
    from tools.subagent_factory.catalog import build_catalog, format_markdown

    cat = build_catalog(ready_only=ready_only)
    if not cat:
        console.print("[yellow]No generated packages found under subagents/.[/yellow]")
        return
    if md:
        print(format_markdown(cat))
        return
    t = Table(title=f"Generated Subagents ({len(cat)})  ·  local, gitignored output")
    t.add_column("Expert")
    t.add_column("T", justify="right")
    t.add_column("Status")
    t.add_column("Modes")
    t.add_column("Sk/Rf", justify="right")
    t.add_column("Adapter")
    t.add_column("Source")
    for e in cat:
        adapter = "[green]ok[/green]" if e["adapter_installed"] else "[red]missing[/red]"
        scolor = {"ready": "green", "draft": "yellow"}.get(e["status"], "white")
        t.add_row(
            e["slug"],
            str(e["tier"]),
            f"[{scolor}]{e['status']}[/{scolor}]",
            ", ".join(e["modes"]),
            f"{e['skills']}/{e['references']}",
            adapter,
            e["source"],
        )
    console.print(t)
    console.print(
        '\nTest any expert: spawn [bold]Agent(subagent_type="<slug>")[/bold], or just prompt '
        "Claude Code with a matching task (it routes via the installed adapter's description).\n"
        "Packages + adapters are gitignored — nothing here is committed. "
        "Run [bold]cli catalog --md[/bold] for a copy-pasteable list."
    )


@main.command("doctor")
def cmd_doctor():
    """Report converter dependency health (no installs)."""
    from tools.subagent_factory.self_heal import doctor

    report = doctor()
    t = Table(title="Subagent Factory — converter health")
    t.add_column("Kind")
    t.add_column("Name")
    t.add_column("Status")
    t.add_column("Note")
    for name, ok in report["python_packages"].items():
        t.add_row(
            "python",
            name,
            "[green]ok[/green]" if ok else "[red]missing[/red]",
            "" if ok else "auto-installs on demand",
        )
    for name, info in report["system_tools"].items():
        ok = info["present"]
        t.add_row(
            "system",
            name,
            "[green]ok[/green]" if ok else "[yellow]missing[/yellow]",
            "" if ok else info["hint"],
        )
    console.print(t)
    venv = report.get("venv")
    console.print(
        f"Managed venv: {venv}" if venv else "Managed venv: not created (run `bootstrap --venv`)"
    )


@main.command("bootstrap")
@click.option(
    "--venv/--no-venv",
    default=False,
    help="Create a project .venv and install the convert extra into it.",
)
@click.option(
    "--extra",
    default="convert",
    help="Optional-dependency extra to install (convert|convert-full).",
)
def cmd_bootstrap(venv, extra):
    """Set up converter dependencies so ingestion works out of the box."""
    from tools.subagent_factory.self_heal import bootstrap_environment, ensure_converter_stack

    if venv:
        console.print(f"[bold]Bootstrapping managed .venv with [{extra}]...[/bold]")
        status = bootstrap_environment(extra=extra)
        if status.get("error"):
            console.print(f"[red]ERROR:[/red] {status['error']}")
            sys.exit(1)
        console.print(
            f"[green]venv ready:[/green] {status['venv']} (created={status['created']}, installed={status['installed']})"
        )
        console.print("Run with SUBAGENT_FACTORY_USE_VENV=1 to use it automatically.")
    else:
        console.print("[bold]Ensuring converter stack in current interpreter...[/bold]")
        report = ensure_converter_stack()
        if report["missing"]:
            console.print(f"[red]Still missing:[/red] {', '.join(report['missing'])}")
            sys.exit(1)
        console.print(
            f"[green]Converter stack ready[/green] (healed: {', '.join(report['healed']) or 'none needed'})"
        )
        for tool, info in report["system_tools"].items():
            if not info["present"]:
                console.print(
                    f"[yellow]Optional system tool '{tool}' missing:[/yellow] {info['hint']}"
                )


if __name__ == "__main__":
    main()
