"""Authoring-pipeline CLI commands (source -> package -> validate -> export).

Registered on the main group in cli.py via add_command — flat command names unchanged.
"""

import sys
from pathlib import Path

import click
from rich.table import Table

from tools.subagent_factory.cli_support import console, subagent_path


@click.command("ingest")
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

    subagent_dir = subagent_path(slug)
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


@click.command("score")
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


@click.command("extract-sample")
@click.argument("source")
def cmd_extract_sample(source):
    """Extract content sample for expert-role inference."""
    from tools.subagent_factory.detect_topic import (
        extract_content_sample,
        format_sample_for_inference,
    )

    sample = extract_content_sample(source)
    print(format_sample_for_inference(sample))


@click.command("stubs")
@click.argument("slug")
def cmd_stubs(slug):
    """Scaffold skill/reference stub files from the profile's knowledge_partition."""
    from tools.subagent_factory.generate_stubs import generate_stubs

    result = generate_stubs(subagent_path(slug))
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


@click.command("selfcheck")
@click.argument("slug")
def cmd_selfcheck(slug):
    """Run the Phase 8 profile self-check gate and write tests/test-results.md."""
    from tools.subagent_factory.profile_self_check import profile_self_check
    from tools.subagent_factory.run_tests import write_test_results

    subagent_dir = subagent_path(slug)
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


@click.command("export")
@click.argument("slug")
def cmd_export(slug):
    """Export subagent package to Claude Code adapter."""
    from tools.subagent_factory.export_claude_agent import export_claude_agent

    subagent_dir = subagent_path(slug)
    result = export_claude_agent(subagent_dir)
    if result.get("error"):
        console.print(f"[red]ERROR:[/red] {result['error']}")
        sys.exit(1)
    console.print(f"[green]Adapter exported:[/green] {result['adapter_path']}")
    console.print(f"[green]Installed:[/green] {result['installed_path']}")


@click.command("validate")
@click.argument("slug")
def cmd_validate(slug):
    """Validate a generated subagent package."""
    from tools.subagent_factory.validate_generated_package import validate_generated_package

    subagent_dir = subagent_path(slug)
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


COMMANDS = [
    cmd_ingest,
    cmd_score,
    cmd_extract_sample,
    cmd_stubs,
    cmd_selfcheck,
    cmd_export,
    cmd_validate,
]
