import tkinter as tk
from rocket import BasePage, BuildContext, Widget, StatelessWidget

from app.ControllerManager import services
from app.components.header_components import Header
from app.components.todo_components import TodoList
from app.components.bottom_bar_component import TaskEntry

class Homepage(BasePage):
    def __init__(self, window):
        super().__init__(window, services.theme)

    def build(self, context: BuildContext) -> Widget:
        # We can return the layout widget directly, or construct one on the fly.
        return HomepageLayout()

class HomepageLayout(StatelessWidget):
    def build(self, context: BuildContext, parent: tk.Frame):
        # Header (Top)
        Header().mount(context, parent, fill="x", side="top")
        
        # Task Entry (Bottom)
        TaskEntry().mount(context, parent, fill="x", side="bottom")
        
        # Todo List (Remaining Space)
        TodoList().mount(context, parent, fill="both", expand=True)

# Legacy adapter for main.py to call
# Updated to use the new structure
def homepage(window):
    # This shouldn't really be used if main.py was updated, but keeping for safety.
    Homepage(window).render()
