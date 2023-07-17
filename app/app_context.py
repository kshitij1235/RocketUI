from rocket.core.state import Signal
from rocket.theme.manager import ThemeManager


class ServiceProvider:
    """
    Centralized container for global services/state.
    """

    def __init__(self):
        self.theme = ThemeManager()
        self.todo_store = Signal[int](0)

    def notify_task_change(self):
        current = self.todo_store.get()
        self.todo_store.set(current + 1)


# Global instance
services = ServiceProvider()

# Accessors
app_theme = services.theme
todo_store = services.todo_store
