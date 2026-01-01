import tkinter as tk

from rocket.context import BuildContext
from rocket.renderer import rerender_component
from rocket.state import Signal
from rocket.state_widgets.base import Widget


class StatefullWidget(Widget):
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
            if self.context and hasattr(self.context.theme, "get_color"):
                bg_color = self.context.theme.get_color("bg")
                self.container.configure(bg=bg_color)

            rerender_component(self.container, self._rebuild)

    def _rebuild(self, parent):
        if self.context:
            self.build(self.context, parent)
