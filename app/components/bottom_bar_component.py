from app.app_context import services
from app.helper import database
from rocket import (
    BuildContext,
    RButton,
    REntry,
    Row,
    Signal,
    StatefulComponent,
    WidgetSpec,
)


class _TaskEntry(StatefulComponent):
    def __init__(self, props=None):
        super().__init__(props=props)
        self.text_signal = Signal("")

    def build(self, context: BuildContext) -> WidgetSpec:
        return Row(
            spacing=10,
            children=[
                REntry(
                    text_variable=self.text_signal,
                    placeholder_text="Add task",
                    height=32,
                    side="left",
                    expand=True,
                ),
                RButton(
                    text="Add Task",
                    command=self._on_add,
                    width=80,
                    height=32,
                    corner_radius=6,
                    font=("Helvetica", 11),
                    side="right",
                ),
            ],
        )

    def _on_add(self):
        text = self.text_signal.get().strip()
        if not text:
            return

        database.add_task(text)
        self.text_signal.set("")
        services.notify_task_change()


def TaskEntry(**kwargs) -> WidgetSpec:
    return WidgetSpec(widget_class=_TaskEntry, props=kwargs)
