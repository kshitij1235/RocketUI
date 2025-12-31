from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

# ============================================================
# Framework defaults (ALWAYS SAFE)
# ============================================================

PROJECT_NAME: str = "rocket_app"
VERSION: str = "0.0.0"
RELEASE: bool = False


@dataclass(slots=True)
class WindowConfig:
    title: str = "Rocket App"
    geometry: str = "800x600"
    resizable: bool = True
    icon: Optional[str] = None


# Public alias expected by runtime
MainWindowConfig = WindowConfig

# Default instance
MAIN_WINDOW = MainWindowConfig()


# ============================================================
# Safe project override loader
# ============================================================


def _load_project_config() -> None:
    global PROJECT_NAME, VERSION, RELEASE, MAIN_WINDOW

    project_root = Path.cwd()
    config_file = project_root / "project_config.py"

    if not config_file.is_file():
        return

    namespace: dict[str, object] = {}

    try:
        exec(config_file.read_text(encoding="utf-8"), namespace)
    except Exception as exc:
        print(
            f"[rocket] Warning: failed to load project_config.py ({exc})",
            file=sys.stderr,
        )
        return

    PROJECT_NAME = str(namespace.get("PROJECT_NAME", PROJECT_NAME))
    VERSION = str(namespace.get("VERSION", VERSION))
    RELEASE = bool(namespace.get("RELEASE", RELEASE))

    user_cfg = namespace.get("MainWindowConfig")
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


# ============================================================
# Load overrides safely (CLI-safe)
# ============================================================

_load_project_config()
