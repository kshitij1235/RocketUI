from __future__ import annotations

import click

from rocket.cli.core import cleanup, hot_reload_app, run_app


@click.command()
@click.option("-c", "--clean", is_flag=True, help="Clean before run")
@click.option("-r", "--hotreload", is_flag=True, help="Enable hot reload")
def run(clean: bool, hotreload: bool) -> None:
    """Run the application."""
    if clean:
        cleanup(
            dirs_to_remove=("__pycache__", "build"),
            file_extensions=(".pyc",),
        )

    if hotreload:
        hot_reload_app()
    else:
        run_app()
