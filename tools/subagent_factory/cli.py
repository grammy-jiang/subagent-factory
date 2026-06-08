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


@main.command("ingest")
@click.argument("source", nargs=-1, required=True)
@click.option("--slug", required=True, help="Subagent slug (kebab-case)")
@click.option("--topic", help="Topic description for create/update decision")
@click.option("--title", help="Override source title")
@click.option("--author", help="Source author")
@click.option("--rights", default="distillation-only", help="Rights status")
def cmd_ingest(source, slug, topic, title, author, rights):
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
            rights_status=rights,
        )
        if result.get("error"):
            console.print(f"[red]ERROR:[/red] {result['error']}")
            if result.get("needs_auth"):
                console.print("[yellow]This URL requires authentication. Provide a local downloaded copy.[/yellow]")
            sys.exit(1)

        console.print(f"[green]OK:[/green] source_id={result['source_id']}")
        console.print(f"  anchors={result['anchor_count']}  assets={result['asset_count']}")
        if result["conversion_result"].get("is_scanned"):
            console.print("[yellow]WARN: Possible scanned PDF — OCR may be needed[/yellow]")


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


@main.command("search")
@click.argument("topic")
def cmd_search(topic):
    """Search existing subagents by topic."""
    from tools.subagent_factory.find_related_subagents import find_related_subagents

    candidates = find_related_subagents(topic)
    if not candidates:
        console.print("No related subagents found.")
        return

    t = Table(title=f"Related subagents for: {topic}")
    t.add_column("Slug")
    t.add_column("Similarity")
    t.add_column("Recommendation")
    t.add_column("Role excerpt")
    for c in candidates:
        rec_color = {"update": "green", "consider-update": "yellow", "create-new": "blue"}.get(c["recommendation"], "white")
        t.add_row(
            c["slug"],
            f"{c['similarity']:.2f}",
            f"[{rec_color}]{c['recommendation']}[/{rec_color}]",
            c["role"][:80],
        )
    console.print(t)


if __name__ == "__main__":
    main()
