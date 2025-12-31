from __future__ import annotations

import click

from rocket.cli.core import hot_reload_app


@click.command()
def dev() -> None:
    """Run with hot reload."""
    hot_reload_app()
