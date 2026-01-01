import tkinter as tk

from app.components.bottom_bar_component import TaskEntry
from app.components.header_components import Header
from app.components.todo_components import TodoList
from app.ControllerManager import services
from rocket import BasePage, BuildContext, Widget


class Homepage(BasePage):
    def __init__(self, window):
        super().__init__(window, services.theme)

    def build(self, context: BuildContext) -> None:
        Header().mount(context, context.window, fill="x", side="top")
        TaskEntry().mount(context, context.window, fill="x", side="bottom")
        TodoList().mount(context, context.window, fill="both", expand=True)
        return


def homepage(window):
    Homepage(window).render()
