import os
import sys
import customtkinter as ctk


def apply_platform_scaling() -> None:
    """
    Apply sane DPI scaling defaults per OS.
    Must be called BEFORE any Tk / CTk window is created.
    """

    # Windows: Tk + CustomTkinter already handle DPI well
    if sys.platform.startswith("win"):
        return

    # macOS: CustomTkinter handles scaling reasonably
    if sys.platform == "darwin":
        return

    # Linux: Tk does NOT auto-scale → must fix manually
    if sys.platform.startswith("linux"):
        scale = (
            os.environ.get("GDK_SCALE")
            or os.environ.get("QT_SCALE_FACTOR")
        )

        try:
            scale = float(scale)
        except (TypeError, ValueError):
            scale = 1.3  # Safe default for HiDPI Linux

        ctk.set_widget_scaling(scale)
        ctk.set_window_scaling(scale)
