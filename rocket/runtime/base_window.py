import os
import sys
from tkinter import PhotoImage

import customtkinter as ctk

from rocket.log import log
from rocket.runtime.scaling import apply_platform_scaling


class BaseWindow(ctk.CTk):
    CONFIG = None

    def __init__(self):
        if self.CONFIG is None:
            raise RuntimeError("Window CONFIG not defined")

        # Must be called BEFORE window creation
        apply_platform_scaling()

        super().__init__()
        cfg = self.CONFIG

        # ---- title / geometry ----
        self.title(cfg.title)
        self.geometry(cfg.geometry)

        self.resizable(
            getattr(cfg, "resizable", True),
            getattr(cfg, "resizable", True),
        )

        # ---- icon ----
        icon_name = getattr(cfg, "icon", None)
        if icon_name:
            self._set_icon(icon_name)

    def _set_icon(self, icon_name: str) -> None:
        icon_path = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                "..",
                "..",
                "resources",
                "images",
                icon_name,
            )
        )

        if not os.path.exists(icon_path):
            log(f"icon not found: {icon_path}")
            return

        # Keep reference to avoid GC
        self._icon = PhotoImage(file=icon_path)

        # ✅ Works on Linux & macOS (window + taskbar)
        self.iconphoto(True, self._icon)

        # ✅ Windows taskbar icon (required)
        if sys.platform.startswith("win"):
            try:
                self.iconbitmap(icon_path)
            except Exception:
                # iconbitmap may fail for non-ICO files
                pass
