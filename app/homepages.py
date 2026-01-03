from app.app_context import services
from app.components.bottom_bar_component import TaskEntry
from app.components.header_components import Header
from app.components.todo_components import TodoList
from rocket import BasePage, BuildContext, Column


class Homepage(BasePage):
    def __init__(self, window):
        super().__init__(window, services.theme)

    def build(self, context: BuildContext):
        return Column(
            spacing=1,
            expand=True,
            children=[Header(), TaskEntry(side="bottom"), TodoList(expand=True)],
        )


class SettingsPage(BasePage):
    def __init__(self, window):
        super().__init__(window, services.theme)

    def build(self, context: BuildContext):
        return Column(
            spacing=15,
            expand=True,
            children=[],
        )
