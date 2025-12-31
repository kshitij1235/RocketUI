from rocket.state import State
from rocket.theme.default import DARK_COLORS, LIGHT_COLORS


class ThemeManager(State):
    def __init__(self, theme="light"):
        super().__init__()

        self.LIGHT_COLORS = LIGHT_COLORS

        self.DARK_COLORS = DARK_COLORS

        if theme == "dark":
            self.active_theme = "dark"
            self.COLORS = self.DARK_COLORS
        else:
            self.active_theme = "light"
            self.COLORS = self.LIGHT_COLORS

    # ✅ THIS METHOD MUST EXIST
    def toggle(self):
        self.switch_theme(not self.isdark())

    def switch_theme(self, dark_mode: bool):
        if dark_mode:
            self.active_theme = "dark"
            self.COLORS = self.DARK_COLORS
        else:
            self.active_theme = "light"
            self.COLORS = self.LIGHT_COLORS

        self.notify()

    def isdark(self):
        return self.active_theme == "dark"

    def get_color(self, key):
        return self.COLORS.get(key, "Key not found")
