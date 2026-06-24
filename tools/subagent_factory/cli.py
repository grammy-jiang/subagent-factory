"""CLI entry point for subagent-factory tools."""

import click

from tools.subagent_factory import cli_maintain, cli_measure, cli_pipeline


@click.group()
def main():
    """Subagent Factory — create Claude Code subagents from documents."""
    # Opt-in (SUBAGENT_FACTORY_USE_VENV=1): re-exec inside the managed .venv.
    # No-op by default; converters self-heal their deps in-process instead.
    from tools.subagent_factory.self_heal import ensure_environment

    ensure_environment()


# Register every domain module's commands on the flat top-level group (names unchanged).
for _command in (*cli_pipeline.COMMANDS, *cli_measure.COMMANDS, *cli_maintain.COMMANDS):
    main.add_command(_command)


if __name__ == "__main__":
    main()
