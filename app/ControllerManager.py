from rocket.state import Signal
from rocket.theme.theme_manager import ThemeManager

class ServiceProvider:
    """
    Centralized container for global services/state.
    """
    def __init__(self):
        self.theme = ThemeManager()
        # todo_store acts as a signal that notifies when lists change
        # The value itself isn't strictly important if we pull from DB, 
        # but we can use it to pass the list version or timestamp.
        self.todo_store = Signal[int](0)

    def notify_task_change(self):
        # Increment version to trigger subscribers
        current = self.todo_store.get()
        self.todo_store.set(current + 1)

# Global instance
services = ServiceProvider()

# Accessors
app_theme = services.theme
todo_store = services.todo_store
