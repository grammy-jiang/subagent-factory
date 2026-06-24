"""Discovery / maintenance / environment CLI commands.

Registered on the main group in cli.py via add_command — flat command names unchanged.
"""

import sys

import click
from rich.table import Table

from tools.subagent_factory.cli_support import console, repo_root, subagent_path


@click.command("catalog")
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


@click.command("search")
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


@click.command("corpus-health")
@click.option("--json", "as_json", is_flag=True, help="Emit JSON instead of a table.")
def cmd_corpus_health(as_json):
    """Audit every generated package's structural health (converter, anchors, claims, flags)."""
    import json as _json
    from collections import Counter

    from tools.subagent_factory.corpus_health import scan_corpus

    rows = scan_corpus(repo_root() / "subagents")
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


@click.command("doctor")
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


@click.command("bootstrap")
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


@click.command("repair-faithfulness")
@click.argument("slug")
def cmd_repair_faithfulness(slug):
    """Strip invalid source_anchors from a faithfulness report (quarantine to a sidecar)."""
    from tools.subagent_factory.repair_faithfulness_report import repair_faithfulness_report

    rp = subagent_path(slug) / "reports" / "faithfulness-report.yaml"
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


@click.command("stale")
@click.argument("slug")
@click.option(
    "--stamp", is_flag=True, help="Write authored_from_digest into every ready doc (baseline)."
)
@click.option("--mark", is_flag=True, help="Flip drifted ready docs to status: stale.")
def cmd_stale(slug, stamp, mark):
    """Detect (or stamp/mark) stale authored skill/reference bodies — Step 9 maintenance."""
    from tools.subagent_factory.detect_stale import detect_stale

    findings = detect_stale(subagent_path(slug), stamp=stamp, mark=mark)
    if not findings:
        console.print("[dim]no authored docs to check[/dim]")
        return
    palette = {"STALE": "red", "WARN": "yellow", "INFO": "cyan", "OK": "green"}
    for level, artifact, reason in findings:
        colour = palette.get(level, "white")
        console.print(f"[{colour}]{level:5s}[/{colour}] {artifact}: {reason}")


COMMANDS = [
    cmd_catalog,
    cmd_search,
    cmd_corpus_health,
    cmd_doctor,
    cmd_bootstrap,
    cmd_repair_faithfulness,
    cmd_stale,
]
