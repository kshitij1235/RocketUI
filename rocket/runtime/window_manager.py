from rocket.runtime.main_window import MainWindow


class WindowManager:
    def __init__(self):
        self._windows = {}

    def get(self, name):
        if name not in self._windows:
            self._windows[name] = self._create(name)
        return self._windows[name]

    def _create(self, name):
        if name == "main_window":
            return MainWindow()
        raise ValueError(f"Unknown window: {name}")
