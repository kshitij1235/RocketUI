from app.components.bottom_bar_component import TaskEntry
from app.components.header_components import Header
from app.components.todo_components import TodoList
from app.ControllerManager import services
from rocket import BasePage, BuildContext
from rocket.layout import Column
from rocket.widget_core import WidgetSpec

class Homepage(BasePage):
    def __init__(self, window):
        super().__init__(window, services.theme)

    def build(self, context: BuildContext) -> WidgetSpec:
        # Layout Strategy:
        # 1. Header (Top)
        # 2. TaskEntry (Bottom) - Must be packed BEFORE the expanding middle content to stick to bottom.
        # 3. TodoList (Top, Expand) - Fills the remaining space in the middle.
        
        return Column(
            spacing=1,
            expand=True, # Ensure the root column fills the window
            children=[
                Header(),
                TaskEntry(side="bottom"), 
                TodoList(expand=True)
            ]
        )

def homepage(window):
    Homepage(window).render()
