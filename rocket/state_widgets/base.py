import tkinter as tk
from abc import ABC, abstractmethod

from rocket.context import BuildContext


class Widget(ABC):
    """
    Base class for all UI components.
    Every widget manages its own isolated generic container (Frame).
    """

    def __init__(self):
        self.container: tk.Frame | None = None
        self.context: BuildContext | None = None

    def mount(self, context: BuildContext, parent: tk.Frame, **pack_kwargs):
        """
        Mounts the widget to the parent frame.
        Creates a dedicated generic container for isolation.
        """
        self.context = context

        # Create dedicated container for isolation
        # By default, transparent/inherited background
        bg_color = context.theme.get_color("bg")

        self.container = tk.Frame(parent, bg=bg_color)
        self.container.pack(**pack_kwargs)

        self.container._widget_ref = self
        self.build(context, self.container)

    @abstractmethod
    def build(self, context: BuildContext, parent: tk.Frame):
        """
        Render the UI inside the provided parent (which is self.container).
        """
        pass
