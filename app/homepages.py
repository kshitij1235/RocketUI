import tkinter as tk
from rocket import BasePage, BuildContext, Widget, StatelessWidget

from app.ControllerManager import services
from app.components.header_components import Header
from app.components.todo_components import TodoList
from app.components.bottom_bar_component import TaskEntry

class Homepage(BasePage):
    def __init__(self, window):
        super().__init__(window, services.theme)

        self.window = window

    def build(self, context: BuildContext) -> Widget:
        Header().mount(context, self.window, fill="x", side="top")
        TaskEntry().mount(context, self.window, fill="x", side="bottom")
        TodoList().mount(context, self.window, fill="both", expand=True)

