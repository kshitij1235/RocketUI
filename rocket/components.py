import tkinter as tk
from typing import Callable, List, Tuple

import customtkinter as ctk

from rocket.renderer import rerender_component
from rocket.state import State
from rocket.theme.theme_manager import ThemeManager

RenderTarget = Tuple[tk.Frame, Callable[[tk.Frame], None]]


class Components:
    """
    Core component factory + reactive rendering system.

    - Layout containers use tkinter.Frame (neutral, no styling)
    - Leaf widgets use CustomTkinter
    - Theme + State trigger rerender (destroy + recreate)
    """

    def __init__(self, window, theme: ThemeManager | None = None) -> None:
        self.window = window
        self.theme = theme or ThemeManager()

        # Containers explicitly owned by this Components instance
        self._containers: List[RenderTarget] = []

        # Bind theme as a reactive state
        self._bind_theme()

    def use_state(
        self,
        state: State,
        container: tk.Frame,
        render_fn: Callable[[tk.Frame], None],
    ) -> None:
        """
        Bind a render function to a container and re-render it
        when the given state changes.
        """

        target = (container, render_fn)
        self._containers.append(target)

        class _StateSubscriber:
            def invalidate(_: object) -> None:
                if container.winfo_exists():
                    rerender_component(container, render_fn)

        state.subscribe(_StateSubscriber())

        # Initial render
        rerender_component(container, render_fn)

    def _bind_theme(self) -> None:
        """
        Treat theme as global reactive state.
        Any theme change triggers rerender of all registered containers.
        """

        class _ThemeSubscriber:
            def invalidate(_: object) -> None:
                for container, render_fn in list(self._containers):
                    if container.winfo_exists():
                        rerender_component(container, render_fn)

        if hasattr(self.theme, "subscribe"):
            self.theme.subscribe(_ThemeSubscriber())

    # ============================================================
    # LAYOUT (NEUTRAL, UNSTYLED)
    # ============================================================

    def Rframe(self, master, **kwargs) -> tk.Frame:
        """
        Neutral layout container.
        No padding, no rounding, no styling assumptions.
        """
        return tk.Frame(
            master=master,
            bg=self.theme.get_color("bg"),
            **kwargs,
        )

    # ============================================================
    # LEAF WIDGETS (THEME-AWARE)
    # ============================================================

    def Rlabels(
        self,
        master,
        text: str = "",
        font=None,
        **kwargs,
    ):
        return ctk.CTkLabel(
            master=master,
            text=text,
            font=font or ("Helvetica", 14),
            text_color=self.theme.get_color("text"),
            bg_color=self.theme.get_color("bg"),
            **kwargs,
        )

    def Rcheckbox(
        self,
        master,
        text: str = "",
        font=None,
        command=None,
        **kwargs,
    ):
        return ctk.CTkCheckBox(
            master=master,
            text=text,
            font=font or ("Helvetica", 12),
            text_color=self.theme.get_color("text"),
            hover_color=self.theme.get_color("hover"),
            fg_color=self.theme.get_color("accent"),
            bg_color=self.theme.get_color("bg"),
            command=command,
            **kwargs,
        )

    def Rbutton(
        self,
        master,
        text: str = "",
        command=None,
        **kwargs,
    ):
        return ctk.CTkButton(
            master=master,
            text=text,
            command=command,
            fg_color=self.theme.get_color("accent"),
            hover_color=self.theme.get_color("hover"),
            text_color=self.theme.get_color("text"),
            **kwargs,
        )

    def Rentry(self, master, **kwargs):
        return ctk.CTkEntry(
            master=master,
            text_color=self.theme.get_color("text"),
            fg_color=self.theme.get_color("bg"),
            **kwargs,
        )
