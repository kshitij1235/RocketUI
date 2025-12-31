from __future__ import annotations

import click

from rocket.cli.commands.run import run
from rocket.cli.commands.build import build
from rocket.cli.commands.clean import clean
from rocket.cli.commands.dev import dev
from rocket.cli.commands.version import version


class CustomGroup(click.Group):
    def format_help(self, ctx, formatter):
        click.echo(
            """
██████╗  ██████╗  ██████╗██╗  ██╗███████╗████████╗
██╔══██╗██╔═══██╗██╔════╝██║ ██╔╝██╔════╝╚══██╔══╝
██████╔╝██║   ██║██║     █████╔╝ █████╗     ██║
██╔══██╗██║   ██║██║     ██╔═██╗ ██╔══╝     ██║
██║  ██║╚██████╔╝╚██████╗██║  ██╗███████╗   ██║
╚═╝  ╚═╝ ╚═════╝  ╚═════╝╚═╝  ╚═╝╚══════╝   ╚═╝

Rocket CLI
"""
        )
        super().format_help(ctx, formatter)


@click.group(cls=CustomGroup)
def rocket():
    """Rocket command-line interface."""
    pass


rocket.add_command(run)
rocket.add_command(build)
rocket.add_command(clean)
rocket.add_command(dev)
rocket.add_command(version)


def main() -> None:
    rocket()


if __name__ == "__main__":
    main()
