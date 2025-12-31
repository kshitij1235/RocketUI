from rocket.state import Signal
from rocket.theme.default import DARK_COLORS, LIGHT_COLORS

class ThemeManager(Signal[str]):
    """
    Manages theme state as a Signal.
    Value is 'light' or 'dark'.
    """
    def __init__(self, theme="light"):
        super().__init__(theme)
        self.LIGHT_COLORS = LIGHT_COLORS
        self.DARK_COLORS = DARK_COLORS
        self._update_colors(theme)

    def _update_colors(self, theme):
        if theme == "dark":
            self.COLORS = self.DARK_COLORS
        else:
            self.COLORS = self.LIGHT_COLORS

    def set(self, value: str) -> None:
        self._update_colors(value)
        super().set(value)

    def toggle(self):
        new_theme = "light" if self.isdark() else "dark"
        self.set(new_theme)

    def isdark(self):
        return self.get() == "dark"

    def get_color(self, key):
        return self.COLORS.get(key, "Key not found")
