from __future__ import annotations

import importlib.util
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

PROJECT_NAME: str = "rocket_app"
VERSION: str = "0.0.0"
RELEASE: bool = False


@dataclass(slots=True)
class WindowConfig:
    """Configuration for the main application window."""

    title: str = "Rocket App"
    geometry: str = "800x600"
    resizable: bool = True
    icon: Optional[str] = None


# Public alias expected by runtime
MainWindowConfig = WindowConfig

# Default instance
MAIN_WINDOW = MainWindowConfig()


def _load_project_config() -> None:
    """
    Load project configuration from `project_config.py`.

    This file is treated as trusted project code.
    Only known configuration values are read.
    """
    global PROJECT_NAME, VERSION, RELEASE, MAIN_WINDOW

    config_path = Path.cwd() / "project_config.py"
    if not config_path.is_file():
        return

    spec = importlib.util.spec_from_file_location("rocket_project_config", config_path)
    if spec is None or spec.loader is None:
        return

    module = importlib.util.module_from_spec(spec)

    try:
        spec.loader.exec_module(module)
    except Exception as exc:
        print(
            f"[rocket] Warning: failed to load project_config.py ({exc})",
            file=sys.stderr,
        )
        return

    # Read simple values safely
    PROJECT_NAME = str(getattr(module, "PROJECT_NAME", PROJECT_NAME))
    VERSION = str(getattr(module, "VERSION", VERSION))
    RELEASE = bool(getattr(module, "RELEASE", RELEASE))

    # Read window config safely
    user_cfg = getattr(module, "MainWindowConfig", None)
    if user_cfg:
        try:
            MAIN_WINDOW = MainWindowConfig(
                title=str(getattr(user_cfg, "title", MAIN_WINDOW.title)),
                geometry=str(getattr(user_cfg, "geometry", MAIN_WINDOW.geometry)),
                resizable=bool(getattr(user_cfg, "resizable", MAIN_WINDOW.resizable)),
                icon=getattr(user_cfg, "icon", MAIN_WINDOW.icon),
            )
        except Exception as exc:
            print(
                f"[rocket] Warning: invalid MainWindowConfig ({exc})",
                file=sys.stderr,
            )


_load_project_config()
