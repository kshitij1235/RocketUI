import tkinter as tk
from rocket.component import StatefulComponent, StatelessComponent
from rocket.context import BuildContext
from rocket.elements import RButton, RCheckbox, RLabel, RDiv
from rocket.layout import ScrollableColumn, Row, Column
from rocket.widget_core import WidgetSpec
from rocket.state import Signal
from app.ControllerManager import services
from app.helper import database

class _TaskItem(StatelessComponent):

    def build(self, context: BuildContext) -> WidgetSpec:
        task = self.props["task"]
        status = self.props["status"]
        
        sig = Signal(bool(status), name=f"Task-{task}")
        
        return Row(
            spacing=10,
            children=[
                RCheckbox(
                    text=task,
                    variable=sig, 
                    command=lambda: self._update_status(sig.get()),
                    font=("Arial", 14),
                ),
                RButton(
                    text="Delete",
                    command=self._delete_task,
                    width=60,
                    height=28,
                    corner_radius=6
                )
            ]
        )

    def _update_status(self, is_done: bool):
        database.update_task_status(self.props["task"], is_done)

    def _delete_task(self):
        database.delete_task(self.props["task"])
        services.notify_task_change()

def TaskItem(task: str, status: bool, **kwargs) -> WidgetSpec:
    return WidgetSpec(widget_class=_TaskItem, props={"task": task, "status": status, **kwargs})

class _TodoList(StatefulComponent):
    def __init__(self, props=None):
        super().__init__(props=props)
        # Subscribe to todo store changes
        self.register_signal(services.todo_store)

    def build(self, context: BuildContext) -> WidgetSpec:
        tasks = database.get_all_tasks() # List of (task, status)

        if not tasks:
            return self._build_no_tasks(context)

        return ScrollableColumn(
            spacing=5,
            expand=self.props.get("expand", False),
            children=[
                TaskItem(task=t[0], status=t[1]) for t in tasks
            ]
        )

    def _build_no_tasks(self, context: BuildContext):
        should_expand = self.props.get("expand", False)
        return Column(
            spacing=10,
            expand=should_expand,
            children=[
                 RLabel(
                    text="No tasks here, why not add one?",
                    font=("Helvetica", 12, "italic"),
                    text_color=context.theme.get_color("text_dim"),
                    # Center the label in the expanded column
                    expand=should_expand,
                )
            ]
        )

def TodoList(**kwargs) -> WidgetSpec:
    return WidgetSpec(widget_class=_TodoList, props=kwargs)
