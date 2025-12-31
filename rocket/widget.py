import tkinter as tk
from abc import ABC, abstractmethod
from typing import List, Any

from rocket.context import BuildContext
from rocket.state import Signal
from rocket.renderer import rerender_component


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
        bg_color = context.theme.get_color("bg") if hasattr(context.theme, 'get_color') else None
        
        self.container = tk.Frame(parent, bg=bg_color)
        self.container.pack(**pack_kwargs)

        # CRITICAL FIX: Keep this widget instance alive as long as the frame exists.
        # Otherwise, weakref signal subscriptions will fail because this object gets GC'd.
        # We attach it to the Tkinter widget itself.
        self.container._widget_ref = self

        # Initial build
        self.build(context, self.container)

    @abstractmethod
    def build(self, context: BuildContext, parent: tk.Frame):
        """
        Render the UI inside the provided parent (which is self.container).
        """
        pass


class StatelessWidget(Widget):
    """
    Simple pass-through widget.
    """
    pass


class ReactiveWidget(Widget):
    """
    A widget that automatically re-renders when declared Signals change.
    """
    def __init__(self, *signals: Signal):
        super().__init__()
        self.signals = signals

    def mount(self, context: BuildContext, parent: tk.Frame, **pack_kwargs):
        # Perform standard mount
        super().mount(context, parent, **pack_kwargs)
        
        # Subscribe to all signals
        for signal in self.signals:
            signal.subscribe(self._on_signal_change)

    def _on_signal_change(self, _):
        # Signal changed, trigger re-render of self.container
        if self.container and self.container.winfo_exists():
            # Update container background if theme is available
            if self.context and hasattr(self.context.theme, 'get_color'):
                bg_color = self.context.theme.get_color("bg")
                self.container.configure(bg=bg_color)
            
            rerender_component(self.container, self._rebuild)

    def _rebuild(self, parent):
        self.build(self.context, parent)

    # Note: currently no auto-unsubscribe on destroy, 
    # relying on Python GC or app lifecycle for simplicity as requested.
