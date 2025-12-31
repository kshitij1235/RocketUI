from rocket import LegacyState, ThemeManager

class ServiceProvider:
    """
    Centralized container for global services/state.
    Acts as the 'ControllerManager' requested.
    """
    def __init__(self):
        self.theme = ThemeManager()
        self.todo_store = LegacyState()

# Global instance
services = ServiceProvider()

# Backward compatibility proxies if needed, 
# but we should aim to use services.theme / services.todo_store
app_theme = services.theme
todo_store = services.todo_store
