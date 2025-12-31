import tkinter as tk
from abc import ABC, abstractmethod
from typing import Callable

from rocket.context import BuildContext
from rocket.renderer import rerender_component


class Widget(ABC):
    """Base class for all UI components."""
    
    def mount(self, context: BuildContext, parent: tk.Frame, **pack_kwargs):
        """
        Mounts the widget to the parent frame.
        Handles the difference between Stateless and Stateful widgets.
        Creates a dedicated wrapper frame to isolate re-renders.
        
        Args:
            context: The build context.
            parent: The parent/container frame.
            **pack_kwargs: Arguments intended for the wrapper's .pack() (e.g. fill, expand, side).
        """
        # Create a dedicated container for this widget to isolate it.
        # This frame permanently sits in the parent.
        # Re-renders will only clear inside this wrapper.
        # We assume the wrapper should be transparent/unstyled effectively (same bg as parent usually).
        # But for now, let's just make it a standard Frame.
        # Since we don't know the exact pack intention of the *child content*,
        # we assume the user's layout intention (pack_kwargs) applies to the *whole component* (the wrapper).
        
        # We need the background color from context to blend in, ideally.
        bg_color = context.theme.get_color("bg") if hasattr(context, 'theme') else None
        
        wrapper = tk.Frame(parent, bg=bg_color)
        
        # Apply layout instructions to the wrapper
        wrapper.pack(**pack_kwargs)

        if isinstance(self, StatelessWidget):
            self.build(context, wrapper)
        elif isinstance(self, StatefulWidget):
            state = self.create_state()
            state.mount(context, self, wrapper)
            state.build(context, wrapper)


class StatelessWidget(Widget):
    """
    A widget that does not require mutable state.
    Override `build` to define the UI.
    """
    @abstractmethod
    def build(self, context: BuildContext, parent: tk.Frame):
        pass


class StatefulWidget(Widget):
    """
    A widget that has mutable state.
    Override `create_state` to return a State instance.
    """
    @abstractmethod
    def create_state(self) -> "State":
        pass


class State(ABC):
    """
    Logic and internal state for a StatefulWidget.
    """
    def __init__(self):
        self.context: BuildContext | None = None
        self.widget: StatefulWidget | None = None
        self._parent_frame: tk.Frame | None = None
        self._mounted = False

    def mount(self, context: BuildContext, widget: StatefulWidget, parent_frame: tk.Frame):
        self.context = context
        self.widget = widget
        self._parent_frame = parent_frame
        self._mounted = True
        self.init_state()

    def init_state(self):
        """Called when this state object is created."""
        pass

    def set_state(self, fn: Callable[[], None] = None):
        """
        Trigger a rebuild of the widget.
        Optionally run a function before rebuilding.
        """
        if fn:
            fn()
        
        if self._mounted and self._parent_frame and self._parent_frame.winfo_exists():
            rerender_component(self._parent_frame, self._rebuild)

    def _rebuild(self, parent):
        """Internal method to trigger build."""
        self.build(self.context, parent)

    @abstractmethod
    def build(self, context: BuildContext, parent: tk.Frame):
        """Render the UI."""
        pass
