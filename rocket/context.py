from rocket.theme.theme_manager import ThemeManager


class BuildContext:
    """
    Dependency bucket passed down the widget tree.
    Holds reference to theme, window, and global data.
    """

    def __init__(self, window, theme: ThemeManager, **kwargs):
        self.window = window
        self.theme: ThemeManager = theme

        # glob storage
        self._data = kwargs

    def get(self, key):
        return self._data.get(key)
