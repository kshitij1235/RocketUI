from __future__ import annotations

import click

from rocket.cli.core import cleanup


@click.command()
def clean() -> None:
    """Clean build artifacts."""
    cleanup(
        files_to_remove=("main.spec",),
        dirs_to_remove=("__pycache__", "build", "dist"),
        file_extensions=(".pyc", ".spec"),
    )
