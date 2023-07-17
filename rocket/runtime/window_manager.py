from rocket.runtime.main_window import MainWindow


class WindowManager:
    def __init__(self):
        self._windows = {}

    def get_runtime(self):
        return MainWindow()
