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
                console.print("[yellow]This URL requires authentication. Provide a local downloaded copy.[/yellow]")
            sys.exit(1)

        if result.get("already_ingested"):
            console.print(f"[yellow]SKIP:[/yellow] source already ingested as source_id={result['source_id']} (sha256 match)")
            continue

        console.print(f"[green]OK:[/green] source_id={result['source_id']}")
        cr = result["conversion_result"]
        console.print(f"  anchors={result['anchor_count']}  assets={result['asset_count']}  converter={cr.get('converter_used')}")
        if cr.get("is_scanned"):
            console.print("[yellow]WARN: Possible scanned PDF — OCR may be needed[/yellow]")
        status = cr.get("conversion_status")
        if status and status != "ok":
            console.print(f"[yellow]WARN: conversion_status={status} — flagged for human review[/yellow]")
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
        color = {"FAIL": "red", "WARNING": "yellow", "PASS": "green", "INFO": "cyan"}.get(f["level"], "white")
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
        rec_color = {"update": "green", "consider-update": "yellow", "create-new": "blue"}.get(c["recommendation"], "white")
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
        t.add_row("python", name, "[green]ok[/green]" if ok else "[red]missing[/red]",
                  "" if ok else "auto-installs on demand")
    for name, info in report["system_tools"].items():
        ok = info["present"]
        t.add_row("system", name, "[green]ok[/green]" if ok else "[yellow]missing[/yellow]",
                  "" if ok else info["hint"])
    console.print(t)
    venv = report.get("venv")
    console.print(f"Managed venv: {venv}" if venv else "Managed venv: not created (run `bootstrap --venv`)")


@main.command("bootstrap")
@click.option("--venv/--no-venv", default=False,
              help="Create a project .venv and install the convert extra into it.")
@click.option("--extra", default="convert", help="Optional-dependency extra to install (convert|convert-full).")
def cmd_bootstrap(venv, extra):
    """Set up converter dependencies so ingestion works out of the box."""
    from tools.subagent_factory.self_heal import bootstrap_environment, ensure_converter_stack

    if venv:
        console.print(f"[bold]Bootstrapping managed .venv with [{extra}]...[/bold]")
        status = bootstrap_environment(extra=extra)
        if status.get("error"):
            console.print(f"[red]ERROR:[/red] {status['error']}")
            sys.exit(1)
        console.print(f"[green]venv ready:[/green] {status['venv']} (created={status['created']}, installed={status['installed']})")
        console.print("Run with SUBAGENT_FACTORY_USE_VENV=1 to use it automatically.")
    else:
        console.print("[bold]Ensuring converter stack in current interpreter...[/bold]")
        report = ensure_converter_stack()
        if report["missing"]:
            console.print(f"[red]Still missing:[/red] {', '.join(report['missing'])}")
            sys.exit(1)
        console.print(f"[green]Converter stack ready[/green] (healed: {', '.join(report['healed']) or 'none needed'})")
        for tool, info in report["system_tools"].items():
            if not info["present"]:
                console.print(f"[yellow]Optional system tool '{tool}' missing:[/yellow] {info['hint']}")


if __name__ == "__main__":
    main()
