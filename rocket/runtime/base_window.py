import os
from tkinter import PhotoImage

import customtkinter as ctk


class BaseWindow(ctk.CTk):
    CONFIG = None

    def __init__(self):
        if self.CONFIG is None:
            raise RuntimeError("Window CONFIG not defined")

        super().__init__()
        cfg = self.CONFIG

        # ---- title / geometry ----
        self.title(cfg.title)
        self.geometry(cfg.geometry)

        self.resizable(
            getattr(cfg, "resizable", True),
            getattr(cfg, "resizable", True),
        )

        # ---- icon (cross-platform safe) ----
        icon_name = getattr(cfg, "icon", None)
        if icon_name:
            self._set_icon(icon_name)

    def _set_icon(self, icon_name: str):
        icon_path = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__), "..", "..", "resources", "images", icon_name
            )
        )

        if not os.path.exists(icon_path):
            print(f"[WARN] Icon not found: {icon_path}")
            return

        # PhotoImage works on Linux / Windows / macOS
        self._icon = PhotoImage(file=icon_path)
        self.iconphoto(True, self._icon)
