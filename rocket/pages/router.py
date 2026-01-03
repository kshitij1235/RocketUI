from typing import Dict, Type

from rocket.core.context import BuildContext
from rocket.render.renderer import Renderer


class Router:
    """
    Simple SPA router.
    Controls which page is currently rendered.
    """

    def __init__(self, window, theme):
        self.window = window
        self.theme = theme
        self.renderer = Renderer(window)

        self._routes: Dict[str, Type] = {}
        self._current_page = None

        # re-render on theme change
        if hasattr(theme, "subscribe"):
            theme.subscribe(lambda _: self.render())

    def register(self, name: str, page_cls: Type) -> None:
        """Register a page under a route name."""
        self._routes[name] = page_cls

    def go(self, name: str) -> None:
        """Navigate to a page."""
        if name not in self._routes:
            raise ValueError(f"Route '{name}' not registered")

        self._current_page = self._routes[name]
        self.render()

    def render(self) -> None:
        """Render the active page."""
        if not self._current_page:
            return

        page = self._current_page(self.window)

        context = BuildContext(
            window=self.window,
            theme=self.theme,
            router=self,
        )

        root = page.build(context)
        if root:
            self.renderer.render(root, context)
