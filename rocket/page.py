import tkinter as tk
from rocket.context import BuildContext
from rocket.widget import Widget

class BasePage:
    """
    Root of a page.
    Manages the top-level BuildContext and renders the root widget.
    """
    def __init__(self, window, theme, data_provider=None):
        self.window = window
        self.theme = theme
        self.data_provider = data_provider or {}
        
        # Subscribe to theme changes
        if hasattr(self.theme, 'subscribe'):
            class ThemeSubscriber:
                def invalidate(s):
                    self.reload()
            self.theme.subscribe(ThemeSubscriber())

    def reload(self):
        """Rerender the entire page (e.g. on theme switch)."""
        for child in self.window.winfo_children():
            child.destroy()
        self.render()

    def render(self):
        context = BuildContext(self.window, self.theme, **self.data_provider)
        root_widget = self.build(context)
        
        # Use the unified mount method
        # CRITICAL FIX: Ensure the root widget fills the window!
        if root_widget:
            root_widget.mount(context, self.window, fill="both", expand=True)

    def build(self, context: BuildContext) -> Widget:
        """
        Subclasses implement this to return the root Widget.
        """
        raise NotImplementedError
