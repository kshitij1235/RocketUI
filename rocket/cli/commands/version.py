from __future__ import annotations

import click

from rocket.config import VERSION


@click.command()
def version() -> None:
    """Show Rocket version."""
    click.echo(f"Version: {VERSION}")
