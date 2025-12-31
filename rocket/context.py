class BuildContext:
    """
    Dependency bucket passed down the widget tree.
    Holds reference to theme, window, and global data.
    """
    def __init__(self, window, theme, **kwargs):
        self.window = window
        self.theme = theme
        self._data = kwargs

    def get(self, key):
        return self._data.get(key)
