from rocket.core.context import BuildContext
from rocket.render.renderer import Renderer
from rocket.core.widget import WidgetSpec

class BasePage:
    """
    Root of a page.
    Manages the top-level Renderer and Theme context.
    """

    def __init__(self, window, theme, data_provider=None):
        self.window = window
        self.theme = theme
        self.data_provider = data_provider or {}
        
        self.renderer = Renderer(self.window)

        # Subscribe to theme changes
        if hasattr(self.theme, "subscribe"):
            self.theme.subscribe(self._on_theme_change)

    def _on_theme_change(self, _):
        self.render()

    def render(self):
        """Rerender the entire page."""
        # Create context
        context = BuildContext(window=self.window, theme=self.theme, **self.data_provider)
        
        # Build root spec
        root_spec = self.build(context)
        
        # Delegate to renderer
        if root_spec:
            self.renderer.render(root_spec, context)

    def build(self, context: BuildContext) -> WidgetSpec:
        """
        Subclasses implement this to return the root WidgetSpec.
        """
        raise NotImplementedError
