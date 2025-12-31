from __future__ import annotations

from pathlib import Path

import click

from rocket.cli.core import create_executable, detect_os


@click.command()
@click.option("-o", "--onefile", is_flag=True, help="Build single-file executable")
def build(onefile: bool) -> None:
    """Build application executable."""
    os_name = detect_os().value

    create_executable(
        script_path=Path("main.py"),
        resource_dir=Path("resources/images"),
        output_root=Path("build"),
        onefile=onefile,
        windowed=True,
    )

    click.echo(f"Build completed successfully for {os_name}")
