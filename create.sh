#!/usr/bin/env bash
set -e

echo "🚀 Setting up Rocket CLI integration..."

# -------------------------------------------------
# Create Rocket CLI directory structure
# -------------------------------------------------
mkdir -p Rocket/cli/commands

touch Rocket/cli/__init__.py
touch Rocket/cli/commands/__init__.py

# -------------------------------------------------
# Rocket CLI main entry
# -------------------------------------------------
cat > Rocket/cli/main.py << 'EOF'
from __future__ import annotations

import click

from Rocket.cli.commands.run import run
from Rocket.cli.commands.build import build
from Rocket.cli.commands.clean import clean
from Rocket.cli.commands.dev import dev
from Rocket.cli.commands.version import version


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
EOF

# -------------------------------------------------
# CLI commands
# -------------------------------------------------

cat > Rocket/cli/commands/run.py << 'EOF'
from __future__ import annotations

import subprocess
import sys
import importlib
import click

from core import cleanup, hot_reload_app


def load_app_entry():
    config = importlib.import_module("project_config")
    module_name, func_name = config.APP_ENTRY.split(":")
    module = importlib.import_module(module_name)
    return getattr(module, func_name)


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
        entry = load_app_entry()
        entry()
EOF

cat > Rocket/cli/commands/build.py << 'EOF'
from __future__ import annotations

from pathlib import Path
import click

from core import create_executable, detect_os


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
EOF

cat > Rocket/cli/commands/clean.py << 'EOF'
from __future__ import annotations

import click
from core import cleanup


@click.command()
def clean() -> None:
    """Clean build artifacts."""
    cleanup(
        files_to_remove=("main.spec",),
        dirs_to_remove=("__pycache__", "build", "dist"),
        file_extensions=(".pyc", ".spec"),
    )
EOF

cat > Rocket/cli/commands/dev.py << 'EOF'
from __future__ import annotations

import click
from core import hot_reload_app


@click.command()
def dev() -> None:
    """Run with hot reload."""
    hot_reload_app()
EOF

cat > Rocket/cli/commands/version.py << 'EOF'
from __future__ import annotations

import click
from project_config import VERSION


@click.command()
def version() -> None:
    """Show Rocket version."""
    click.echo(f"Version: {VERSION}")
EOF

# -------------------------------------------------
# project_config.py (only if missing)
# -------------------------------------------------
if [ ! -f project_config.py ]; then
  cat > project_config.py << 'EOF'
APP_NAME = "RocketApp"
APP_ENTRY = "main:main"
VERSION = "0.1.0"
EOF
  echo "📄 project_config.py created"
else
  echo "ℹ️ project_config.py already exists"
fi

# -------------------------------------------------
# Patch manage.py to proxy Rocket CLI
# -------------------------------------------------
if [ -f manage.py ]; then
  cat > manage.py << 'EOF'
from Rocket.cli.main import main

if __name__ == "__main__":
    main()
EOF
  echo "🔁 manage.py converted to Rocket CLI proxy"
fi

echo ""
echo "✅ Rocket CLI setup complete!"
echo ""
echo "Next steps:"
echo "  1. Add this to pyproject.toml:"
echo ""
echo "     [project.scripts]"
echo "     Rocket = \"Rocket.cli.main:main\""
echo ""
echo "  2. Install editable:"
echo "     pip install -e ."
echo ""
echo "  3. Run:"
echo "     Rocket --help"
echo ""
